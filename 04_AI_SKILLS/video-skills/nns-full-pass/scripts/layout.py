# -*- coding: utf-8 -*-
"""BUOC 2 — TU DO bo cuc hinh de quyet dinh dat chu o dau.

Truoc day viec nay lam bang tay: soi frame roi go --safe. Script nay lam thay,
va IN RA bang "doan -> y, ly do, so do" de nguoi duyet TRUOC khi render.

    python scripts/layout.py --video <video> --out <layout.json> [--font ...]

Do 4 thu, khong doan thu nao:
  1. cat canh that : select=gt(scene,THR) -> chia video thanh doan
  2. hop MAT       : model det_10g.onnx cua nns-face-highlight, tren frame that
  3. khung chu nhat: doan khong co mat (bo cuc PiP / quay man hinh) -> do phan bo
                     mau THEO HANG de tim day cua khung dang chiem hinh
  4. UI in san     : vung co noi dung nhung KHONG BAO GIO doi qua ca video
                     (vi du pill thoi luong) -> chu khong duoc de len

Roi chon y sao cho khoi chu khong cham ca 4, va khong tut xuong duoi vung an
toan cua nen tang (day khung ~330px bi UI TikTok/Facebook che).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()

# Day khung bi UI nen tang che. Do tren khung 1920: ~330px => chu phai tren 1590.
PLATFORM_BOTTOM_PX_AT_1920 = 330
GAP_FACE = 48          # cach hop mat it nhat bao nhieu px
GAP_RECT = 36          # cach day khung man hinh ghi
GAP_UI = 24            # cach UI in san
TOP_MARGIN_FRAC = 0.06  # day chu len tren thi khong duoc cao qua muc nay


# --------------------------------------------------------------- cat canh
def scene_cuts(video, thr, dur):
    """Moc cat canh THAT. Khong dung concat/demuxer gi o day, chi doc metadata."""
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", video,
           "-filter_complex", "select='gt(scene,%g)',metadata=print:file=-" % thr,
           "-an", "-f", "null", "-"]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    ts = []
    for m in re.finditer(r"pts_time:([0-9.]+)", (p.stdout or "") + (p.stderr or "")):
        t = float(m.group(1))
        if 0.05 < t < dur - 0.05:
            ts.append(round(t, 3))
    return sorted(set(ts))


def segments(cuts, dur, min_seg):
    """Gop doan qua ngan vao doan truoc — doi y lien tuc thi chu nhay nhay."""
    bounds = [0.0] + list(cuts) + [round(dur, 3)]
    segs = []
    for a, b in zip(bounds, bounds[1:]):
        if b - a < 1e-6:
            continue
        if segs and (b - a) < min_seg:
            segs[-1][1] = b
        else:
            segs.append([a, b])
    if len(segs) > 1 and segs[0][1] - segs[0][0] < min_seg:
        segs[1][0] = segs[0][0]
        segs.pop(0)
    return [(round(a, 3), round(b, 3)) for a, b in segs]


# ------------------------------------------------------------ doc frame
def gray_frames(video, times, w, h, scale=None):
    """Trich frame theo CHI SO FRAME (select=eq(n,N)), khong dung -ss.

    -ss tren mp4 nhay toi keyframe gan nhat, moc lech ca nua giay. Voi phep do
    bo cuc thi lech nua giay la do nham doan.
    """
    import numpy as np
    info = C.probe_video(video)
    fps = info["fps"] or 30.0
    sw, sh = (scale or (w, h))
    out = []
    for t in times:
        n = max(0, int(round(t * fps)))
        vf = "select=eq(n\\,%d),scale=%d:%d" % (n, sw, sh)
        p = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf,
             "-fps_mode", "passthrough", "-frames:v", "1", "-pix_fmt", "gray",
             "-f", "rawvideo", "-"],
            capture_output=True)
        buf = p.stdout
        if len(buf) < sw * sh:
            continue
        out.append((t, np.frombuffer(buf[:sw * sh], dtype=np.uint8)
                    .reshape(sh, sw).astype(np.int16)))
    return out


# --------------------------------------------------------------- hop mat
def face_boxes(video, times, thr):
    """Tra {t: [x1,y1,x2,y2]} cho cac moc bat duoc mat. Khong bat duoc -> vang."""
    F.add_face_path()
    try:
        import facelib as FL
    except Exception as e:
        return {}, "khong nap duoc facelib (%s)" % str(e)[:60]
    model, _src, _tried = FL.find_model(None)
    if not model:
        return {}, "khong tim thay det_10g.onnx"
    try:
        FL.require_onnxruntime()
        meta = FL.probe(video)
        scale, sw, sh = FL.det_scale(meta["w"], meta["h"])
        det = FL.Detector(model, thr)
    except SystemExit:
        return {}, "onnxruntime chua cai"
    except Exception as e:
        return {}, "khong khoi tao duoc detector (%s)" % str(e)[:60]
    fps = meta["fps"] or 30.0
    # frames_at_indices SAP XEP + BO TRUNG chi so, nen phai map nguoc idx -> t
    want = {}
    for t in times:
        want.setdefault(max(0, int(round(t * fps))), round(t, 3))
    try:
        frames = FL.frames_at_indices(video, sorted(want), sw, sh)
    except Exception as e:
        return {}, "khong doc duoc frame (%s)" % str(e)[:60]
    got = {}
    for idx, img in frames:
        try:
            cands = det(img, sw, sh, scale)   # tra hop theo TOA DO GOC
        except Exception:
            continue
        if not cands:
            continue
        b, _s = max(cands, key=lambda c: FL.box_area(c[0]))
        got[want.get(idx, idx)] = [float(x) for x in b]
    return got, None


# ------------------------------------------------- khung chu nhat theo hang
def rect_bottom(frames, h):
    """Doan khong co mat: tim khung dang chiem hinh bang phan bo mau theo hang.

    Hang thuoc ve khung noi dung thi mau trai dai theo chieu ngang (std cao);
    hang thuoc ve nen/letterbox/blur thi gan nhu mot mau (std thap). Lay dai
    lien tuc DAI NHAT co std cao -> day cua no la day khung.
    """
    import numpy as np
    if not frames:
        return None, None, None
    rows = np.median(np.stack([np.std(f.astype(np.float32), axis=1)
                               for _t, f in frames]), axis=0)
    if rows.max() < 1e-6:
        return None, None, None
    thr = max(3.0, 0.35 * float(rows.max()))
    on = rows > thr
    best = cur = None
    for y, v in enumerate(on):
        if v:
            cur = [y, y] if cur is None else [cur[0], y]
        elif cur is not None:
            if best is None or (cur[1] - cur[0]) > (best[1] - best[0]):
                best = cur
            cur = None
    if cur is not None and (best is None or (cur[1] - cur[0]) > (best[1] - best[0])):
        best = cur
    if best is None:
        return None, None, None
    sh = len(rows)
    k = h / float(sh)
    return int(round(best[1] * k)), int(round(best[0] * k)), float(thr)


# ------------------------------------------------------------- UI in san
def baked_ui(frames, h):
    """Vung CO noi dung nhung KHONG BAO GIO doi -> gan nhu chac chan la UI in san.

    Loc them: chi nhan dai HEP (< 12% chieu cao). Canh may co dinh thi ca khung
    deu "tinh", nen neu khong loc do rong thi ca video bi bao la UI.
    """
    import numpy as np
    if len(frames) < 4:
        return []
    st = np.stack([f for _t, f in frames]).astype(np.int16)
    rng = st.max(axis=0) - st.min(axis=0)           # bien do theo thoi gian
    static = (rng < 8).mean(axis=1)                 # ty le cot dung yen moi hang
    content = np.median(st, axis=0).std(axis=1)     # hang co noi dung khong
    flag = (static > 0.97) & (content > 12.0)
    sh = flag.shape[0]
    k = h / float(sh)
    bands, cur = [], None
    for y, v in enumerate(flag):
        if v:
            cur = [y, y] if cur is None else [cur[0], y]
        elif cur is not None:
            bands.append(cur)
            cur = None
    if cur is not None:
        bands.append(cur)
    out = []
    for y0, y1 in bands:
        if (y1 - y0 + 1) < 4:
            continue
        if (y1 - y0 + 1) > 0.12 * sh:               # qua day -> la canh tinh
            continue
        out.append((int(round(y0 * k)), int(round(y1 * k))))
    return out


# ------------------------------------------------------------- chon y
def pick_y(seg, obst, block_h, h, bottom_safe, ui_bands):
    """Tra (y, ly_do, ghi_chu). y la DAY cua khoi chu, dung hop dong --safe."""
    top_min = int(h * TOP_MARGIN_FRAC) + block_h
    ob_bottom = obst.get("bottom")
    ob_top = obst.get("top")
    gap = GAP_FACE if obst.get("kind") == "mat" else GAP_RECT

    def hits_ui(y):
        for a, b in ui_bands:
            if not (y < a - GAP_UI or (y - block_h) > b + GAP_UI):
                return (a, b)
        return None

    y = bottom_safe
    band = hits_ui(y)
    while band and y - block_h > top_min:
        y = band[0] - GAP_UI                        # day LEN tren dai UI
        if y - block_h < top_min:
            break
        band = hits_ui(y)

    if ob_bottom is None:
        return y, "khong thay vat can, dat sat vung an toan", {}

    clear = (y - block_h) - (ob_bottom + gap)
    if clear >= 0:
        return y, "duoi %s, con thua %dpx" % (obst["kind"], int(clear)), {
            "clearance_px": int(clear)}

    # Khong du cho o duoi -> DAY LEN TREN vat can (dung bao gio day xuong duoi
    # vung an toan: day khung bi UI nen tang che).
    if ob_top is not None:
        y_up = int(ob_top - gap)
        if y_up - block_h >= int(h * TOP_MARGIN_FRAC) and not hits_ui(y_up):
            return y_up, "KHONG du cho duoi %s (thieu %dpx) -> day LEN tren" % (
                obst["kind"], int(-clear)), {"pushed_up": True,
                                             "clearance_px": int(clear)}
    return y, "CHAT: de duoi %s thi thieu %dpx, day len cung khong vua" % (
        obst["kind"], int(-clear)), {"tight": True, "clearance_px": int(clear)}


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(
        description="Tu do bo cuc hinh -> quyet dinh cho dat chu")
    ap.add_argument("--video")
    ap.add_argument("--out", help="file layout.json ket qua")
    ap.add_argument("--resources")
    ap.add_argument("--font", help="de do chieu cao khoi chu that")
    ap.add_argument("--scene", type=float, default=0.25,
                    help="nguong cat canh (mac dinh 0.25)")
    ap.add_argument("--min-seg", type=float, default=2.5,
                    help="doan ngan hon muc nay thi gop vao doan truoc")
    ap.add_argument("--samples", type=int, default=4,
                    help="so frame lay mau trong moi doan")
    ap.add_argument("--ui-samples", type=int, default=14,
                    help="so frame rai deu ca video de tim UI in san")
    ap.add_argument("--font-size", type=int, default=None,
                    help="mac dinh cao_video/24, giong build_ass.py")
    ap.add_argument("--lines", type=int, default=1,
                    help="so dong sub toi da (mac dinh 1)")
    ap.add_argument("--bottom-safe", type=int, default=None,
                    help="y thap nhat cho phep (mac dinh cao - 330*cao/1920)")
    ap.add_argument("--thr", type=float, default=0.5, help="nguong tin cay mat")
    ap.add_argument("--no-face", action="store_true",
                    help="bo qua do mat (khong co onnxruntime)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.video or not a.out:
        C.die("thieu tham so.\n"
              "    python scripts/layout.py --video \"<video>\" --out layout.json")
    if not os.path.isfile(a.video):
        C.die("khong thay video: %s" % a.video)
    C.import_numpy()

    info = C.probe_video(a.video)
    w, h, dur = info["width"], info["height"], info["duration"]
    fps = info["fps"]
    size = a.font_size or max(8, h // 24)
    outline = max(1.0, 0.09 * size)
    block_h = int(size * 1.35 * max(1, a.lines) + 2 * outline)
    bottom_safe = (a.bottom_safe if a.bottom_safe is not None
                   else int(h - PLATFORM_BOTTOM_PX_AT_1920 * h / 1920.0))

    F.banner("BUOC 2 — DO BO CUC (khong doan, do that)",
             ["video      : %s" % a.video,
              "khung      : %dx%d  %.4g fps  %.2fs" % (w, h, fps, dur),
              "co chu     : %d px, vien %.1f -> khoi chu cao %d px (%d dong)"
              % (size, outline, block_h, a.lines),
              "vung an toan: y toi da %d (day khung %d px bi UI nen tang che)"
              % (bottom_safe, h - bottom_safe)])

    cuts = scene_cuts(a.video, a.scene, dur)
    segs = segments(cuts, dur, a.min_seg)
    print("")
    print("  cat canh   : %d moc (nguong %.2f)%s"
          % (len(cuts), a.scene,
             ("  " + ", ".join("%.2f" % t for t in cuts[:12])
              + (" ..." if len(cuts) > 12 else "")) if cuts else "  (khong co)"))
    print("  doan       : %d (gop doan ngan hon %.1fs)" % (len(segs), a.min_seg))

    # --- UI in san: rai deu ca video
    ui_times = [dur * (i + 0.5) / a.ui_samples for i in range(a.ui_samples)]
    sw = 320
    sh = max(2, int(round(320 * h / float(w))))
    ui_frames = gray_frames(a.video, ui_times, w, h, scale=(sw, sh))
    ui = baked_ui(ui_frames, h)
    if ui:
        print("  UI in san  : %d dai — %s"
              % (len(ui), ", ".join("y %d..%d" % (x, y) for x, y in ui)))
        print("               (vung CO noi dung nhung khong doi suot %d frame mau)"
              % len(ui_frames))
    else:
        print("  UI in san  : khong thay dai nao co noi dung ma dung yen")

    rows = []
    for (s0, s1) in segs:
        n = max(1, a.samples)
        times = [s0 + (s1 - s0) * (i + 0.5) / n for i in range(n)]
        obst = {}
        note = ""
        boxes = {}
        if not a.no_face:
            boxes, why = face_boxes(a.video, times, a.thr)
            if why:
                note = why
        if boxes:
            bs = list(boxes.values())
            obst = {"kind": "mat",
                    "bottom": max(b[3] for b in bs),
                    "top": min(b[1] for b in bs),
                    "n": len(bs), "of": n}
        else:
            fr = gray_frames(a.video, times, w, h, scale=(sw, sh))
            rb, rt, thr = rect_bottom(fr, h)
            if rb is not None and rb < h - 4:
                obst = {"kind": "khung hinh", "bottom": rb, "top": rt,
                        "row_thr": thr}
            elif rb is not None:
                obst = {"kind": "khung hinh", "bottom": None, "top": rt,
                        "row_thr": thr,
                        "why": "khung chiem tron chieu cao -> khong coi la vat can"}
        y, why, extra = pick_y((s0, s1), obst, block_h, h, bottom_safe, ui)
        # Cho dat THE CHU: tren vat can neu duoc, NHUNG luon phai cao hon khoi
        # sub it nhat mot khoi chu + 70px. Khong co ve nay thi o doan da bi day
        # len, the va sub ra dung mot y va de len nhau.
        top_min = int(h * TOP_MARGIN_FRAC) + block_h
        above = int((obst.get("top") or bottom_safe) - GAP_FACE)
        card_y = max(top_min, min(above, int(y - block_h - 70)))
        rows.append({"start": s0, "end": s1, "y": int(y), "reason": why,
                     "obstacle": obst, "note": note, "block_h": block_h,
                     "card_y": int(card_y), **extra})

    print("")
    print("  BANG BO CUC — doan -> y, ly do, so do")
    print("  " + F.hr("-"))
    print("  %-15s %6s %6s  %-13s %-46s" % ("doan (giay)", "y sub", "y the",
                                            "vat can", "ly do / so do"))
    print("  " + F.hr("-"))
    for r in rows:
        ob = r["obstacle"]
        if ob.get("kind") == "mat":
            desc = "mat y%d..%d" % (int(ob["top"]), int(ob["bottom"]))
        elif ob.get("kind") == "khung hinh":
            desc = ("khung day y%d" % int(ob["bottom"])
                    if ob.get("bottom") else "khung tron khung")
        else:
            desc = "-"
        print("  %-15s %6d %6d  %-13s %s"
              % ("%.2f-%.2f" % (r["start"], r["end"]), r["y"], r["card_y"],
                 desc, r["reason"]))
        if r["note"]:
            print("  %-15s %13s  %s" % ("", "", "(!) " + r["note"]))
    print("  " + F.hr("-"))

    safe = ",".join("%g-%g:%d" % (r["start"], r["end"], r["y"]) for r in rows)
    print("")
    print("  chuoi --safe cho build_ass.py:")
    print("      %s" % safe)
    tight = [r for r in rows if r.get("tight")]
    up = [r for r in rows if r.get("pushed_up")]
    if up:
        print("")
        print("  %d doan phai DAY CHU LEN TREN vat can (khong du cho o duoi):" % len(up))
        for r in up:
            print("      %.2f-%.2f  y=%d" % (r["start"], r["end"], r["y"]))
    if tight:
        print("")
        print("  CANH BAO: %d doan CHAT — chu se gan/cham vat can:" % len(tight))
        for r in tight:
            print("      %.2f-%.2f  y=%d  %s" % (r["start"], r["end"], r["y"],
                                                 r["reason"]))
        print("      Cach chua: giam --font-size, hoac tu dat --safe cho doan do.")

    if a.dry_run:
        print("")
        print("  [dry-run] khong ghi %s" % a.out)
        return

    C.write_json(a.out, {
        "video": os.path.abspath(a.video),
        "w": w, "h": h, "fps": fps, "dur": dur,
        "font_size": size, "outline": outline, "block_h": block_h,
        "lines": a.lines, "bottom_safe": bottom_safe,
        "scene_thr": a.scene, "cuts": cuts, "min_seg": a.min_seg,
        "ui_bands": [list(b) for b in ui],
        "segments": rows, "safe": safe})
    print("")
    print("  da ghi: %s" % os.path.abspath(a.out))
    print("")


if __name__ == "__main__":
    C.run_main(main)
