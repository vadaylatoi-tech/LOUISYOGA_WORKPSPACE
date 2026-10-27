# -*- coding: utf-8 -*-
"""DO LAI ket qua. Khong in "xong" suong.

    python scripts/verify.py --video <video vao> --out <video ra>

Kiem 4 thu:
  1. so frame file ra == so frame file vao (DEM that, khong tin nb_frames)
  2. do dai tieng khong doi
  3. 3 moc dang le phai co chu: so frame ra voi frame vao, dem pixel khac han
     nhau BEN TRONG dai chu. Do that moi biet chu co hien, chu khong phai
     libass am tham ve ra khung trong.
  4. 1 moc dang le KHONG co chu: phai gan nhu khong co pixel nao khac.

Nguong da hieu chuan tren may nay (video 1080x1920, co chu 80 px):
  frame co chu  : 4.0% - 6.9% dien tich dai bi doi, 100% pixel doi nam trong dai
  frame khong chu: 0 pixel doi
=> lay nguong an toan: >= 0.5% dien tich dai, >= 90% pixel doi nam trong dai.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nnscommon as C  # noqa: E402

DIFF_LEVEL = 60          # chenh muc xam coi la "chu", tren nhieu nen x264
BAND_MIN_FRAC = 0.005    # >= 0.5% dien tich dai
IN_BAND_MIN = 0.90       # >= 90% pixel doi phai nam trong dai
GAP_MAX_FRAC = 0.001     # cho khung khong chu: < 0.1%


def events_from_ass(path):
    """Du phong khi khong co plan.json: doc thang cac dong Dialogue."""
    evs = []
    for line in C.read_text(path).splitlines():
        if not line.startswith("Dialogue:"):
            continue
        parts = line.split(",", 9)
        if len(parts) < 10:
            continue
        try:
            st = C.parse_ass_time(parts[1])
            en = C.parse_ass_time(parts[2])
        except Exception:
            continue
        m = re.search(r"\\pos\(\s*[-0-9.]+\s*,\s*([-0-9.]+)\s*\)", parts[9])
        y = int(float(m.group(1))) if m else None
        evs.append({"start": st, "end": en, "y": y})
    return evs


def spans_from_events(evs, default_y):
    """Gop cac dong Dialogue lien nhau thanh doan CO CHU."""
    spans = []
    for e in sorted(evs, key=lambda x: x["start"]):
        y = e["y"] if e["y"] is not None else default_y
        if spans and abs(spans[-1]["end"] - e["start"]) < 0.02 \
                and spans[-1]["y"] == y:
            spans[-1]["end"] = max(spans[-1]["end"], e["end"])
        else:
            spans.append({"start": e["start"], "end": e["end"], "y": y})
    return spans


def band_of(y, size, height):
    top = max(0, int(y - 1.7 * size))
    bot = min(height, int(y + 0.4 * size))
    if bot <= top:
        top, bot = max(0, height - 200), height
    return top, bot


def measure(vid_in, vid_out, frame_no, W, H, band):
    np = C.import_numpy()
    a = C.gray_frame(vid_in, frame_no, W, H).astype(np.int16)
    b = C.gray_frame(vid_out, frame_no, W, H).astype(np.int16)
    d = np.abs(b - a) > DIFF_LEVEL
    top, bot = band
    sub = d[top:bot, :]
    total = int(d.sum())
    inband = int(sub.sum())
    return {"total": total, "inband": inband,
            "band_area": int(sub.size),
            "frac": inband / float(sub.size),
            "ratio": inband / float(total) if total else 0.0}


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", help="video GOC (truoc khi ve sub)")
    ap.add_argument("--out", help="video KET QUA")
    ap.add_argument("--resources")
    ap.add_argument("--ass", default=None)
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    C.require_video_out(a, "verify.py")

    for p, what in ((a.video, "video goc"), (a.out, "video ket qua")):
        if not os.path.isfile(p):
            C.die("khong thay %s: %s" % (what, p))

    print("")
    print("  " + C.hr("-"))
    print("  KIEM KET QUA (verify)")
    print("  " + C.hr("-"))

    fails = []
    src = C.probe_video(a.video)
    dst = C.probe_video(a.out)

    # --- 1. so frame ---
    n_src = C.count_frames(a.video)
    n_dst = C.count_frames(a.out)
    if n_src == n_dst:
        print("  [OK]     so frame              vao %d  ==  ra %d" % (n_src, n_dst))
    else:
        print("  [LOI]    so frame              vao %d  !=  ra %d (lech %d)"
              % (n_src, n_dst, n_dst - n_src))
        fails.append("so frame file ra (%d) khac file vao (%d). Thuong la do "
                     "fps bi doi — kiem lai tham so -r khi ma hoa."
                     % (n_dst, n_src))
    if abs(dst["fps"] - src["fps"]) > 0.01:
        print("  [LOI]    fps                   vao %.4g -> ra %.4g"
              % (src["fps"], dst["fps"]))
        fails.append("fps bi doi tu %.4g thanh %.4g" % (src["fps"], dst["fps"]))
    else:
        print("  [OK]     fps                   %.4g" % dst["fps"])
    if (src["width"], src["height"]) != (dst["width"], dst["height"]):
        print("  [LOI]    kich thuoc            %dx%d -> %dx%d"
              % (src["width"], src["height"], dst["width"], dst["height"]))
        fails.append("kich thuoc khung bi doi")
    else:
        print("  [OK]     kich thuoc            %dx%d" % (dst["width"], dst["height"]))

    # --- 2. tieng ---
    da, db = C.audio_duration(a.video), C.audio_duration(a.out)
    if da is None and db is None:
        print("  [LUU Y]  tieng                 ca 2 file khong co tieng")
    elif da is None or db is None:
        print("  [LOI]    tieng                 vao %s / ra %s" % (da, db))
        fails.append("mat tieng o file ra")
    elif abs(da - db) > 0.05:
        print("  [LOI]    do dai tieng          vao %.3fs != ra %.3fs" % (da, db))
        fails.append("do dai tieng lech %.3fs" % abs(da - db))
    else:
        print("  [OK]     do dai tieng          %.3fs (lech %.3fs)"
              % (db, abs(da - db)))

    # --- lay ke hoach sub ---
    plan_path = C.side_path(a.out, ".plan.json")
    ass_path = a.ass or C.side_path(a.out, ".ass")
    size, default_y, spans = None, None, None
    plan = None
    if os.path.isfile(plan_path):
        plan = C.read_json(plan_path)
        size = plan["font_size"]
        default_y = plan["default_y"]
        spans = [{"start": c["start"], "end": c["end"], "y": c["y"]}
                 for c in plan["chunks"]]
        print("  [OK]     ke hoach sub          %s (%d cum)"
              % (os.path.basename(plan_path), len(spans)))
    elif os.path.isfile(ass_path):
        evs = events_from_ass(ass_path)
        m = re.search(r"^Style:\s*Sub,[^,]*,\s*([0-9]+)",
                      C.read_text(ass_path), re.M)
        size = int(m.group(1)) if m else max(24, dst["height"] // 24)
        ys = [e["y"] for e in evs if e["y"] is not None]
        default_y = ys[0] if ys else int(dst["height"] * 0.80)
        spans = spans_from_events(evs, default_y)
        print("  [OK]     ke hoach sub          doc tu %s (%d doan)"
              % (os.path.basename(ass_path), len(spans)))
    else:
        C.die("khong thay ca %s va %s — khong biet chu dang le phai o dau."
              % (os.path.basename(plan_path), os.path.basename(ass_path)))
    if not spans:
        C.die("khong co doan sub nao trong ke hoach — khong co gi de kiem.")

    # --- 2-BIS. file .ass co KHOP ke hoach khong (khong ton chi phi decode) ---
    # Chi do pixel o vai moc thi khong bat duoc truong hop .ass bi ghi thieu /
    # bi sua tay o giua. So dong Dialogue va moc cuoi thi bat duoc ngay.
    if plan is not None and os.path.isfile(ass_path):
        evs = events_from_ass(ass_path)
        n_plan = int(plan.get("n_events") or 0)
        if n_plan and len(evs) != n_plan:
            print("  [LOI]    .ass vs ke hoach      .ass co %d dong Dialogue, "
                  "ke hoach ghi %d" % (len(evs), n_plan))
            fails.append(
                "file %s co %d dong Dialogue nhung ke hoach ghi %d dong -> "
                ".ass khong khop ke hoach (bi ghi thieu hoac sua tay). Chay lai:"
                " python scripts/build_ass.py --video \"%s\" --out \"%s\""
                % (os.path.basename(ass_path), len(evs), n_plan, a.video, a.out))
        elif evs:
            end_plan = max(c["end"] for c in plan["chunks"])
            end_ass = max(e["end"] for e in evs)
            if abs(end_ass - end_plan) > 0.05:
                print("  [LOI]    .ass vs ke hoach      moc cuoi .ass %.2fs != "
                      "ke hoach %.2fs" % (end_ass, end_plan))
                fails.append(
                    "cum sub cuoi trong .ass ket thuc o %.2fs nhung ke hoach la "
                    "%.2fs -> phan cuoi video bi thieu chu. Chay lai build_ass.py."
                    % (end_ass, end_plan))
            else:
                print("  [OK]     .ass vs ke hoach      %d dong Dialogue, moc cuoi "
                      "%.2fs — khop" % (len(evs), end_ass))

    if a.dry_run:
        print("  [dry-run] dung o day, khong chup frame.")
        return

    # --- 3. cac moc CO chu ---
    W, H, fps = dst["width"], dst["height"], dst["fps"]
    n = max(1, min(a.samples, len(spans)))
    # LUON kiem cum DAU va cum CUOI: cach chia deu o duoi khong bao gio cham
    # vao 2 cum nay, nen 1 loi o hook hay o duoi cuoi video se lot qua.
    idx = [0, len(spans) - 1]
    if len(spans) > 1:
        idx += [int(round((i + 0.5) * (len(spans) - 1) / max(n, 1)))
                for i in range(n)]
    seen, picks = set(), []
    for i in sorted(set(idx)):
        i = min(max(i, 0), len(spans) - 1)
        if i in seen:
            continue
        seen.add(i)
        picks.append(spans[i])
    print("")
    print("  do %d moc DANG LE CO CHU (so frame ra voi frame vao):" % len(picks))
    for sp in picks:
        t = (sp["start"] + sp["end"]) / 2.0
        fno = min(n_dst - 1, max(0, int(round(t * fps))))
        band = band_of(sp["y"], size, H)
        m = measure(a.video, a.out, fno, W, H, band)
        ok = m["frac"] >= BAND_MIN_FRAC and m["ratio"] >= IN_BAND_MIN
        print("      %s  t=%6.2fs frame %-5d dai y %d..%d: %d px doi trong dai"
              " = %.3f%% dien tich, %.1f%% pixel doi nam trong dai"
              % ("[OK]  " if ok else "[LOI] ", t, fno, band[0], band[1],
                 m["inband"], 100 * m["frac"], 100 * m["ratio"]))
        if not ok:
            if m["frac"] < BAND_MIN_FRAC:
                fails.append(
                    "o giay %.2f dang le co chu nhung dai chu chi doi %.4f%% "
                    "(can >= %.1f%%) -> chu KHONG duoc ve ra. Thuong la libass "
                    "khong tim thay font: kiem ten ho font trong file .ass."
                    % (t, 100 * m["frac"], 100 * BAND_MIN_FRAC))
            else:
                fails.append(
                    "o giay %.2f chi %.1f%% pixel doi nam trong dai chu "
                    "(can >= %.0f%%) -> co gi khac dang bi ve ngoai dai."
                    % (t, 100 * m["ratio"], 100 * IN_BAND_MIN))

    # --- 4. moc KHONG co chu (kiem nguoc) ---
    gaps = []
    ss = sorted(spans, key=lambda x: x["start"])
    for i in range(len(ss) - 1):
        g0, g1 = ss[i]["end"], ss[i + 1]["start"]
        if g1 - g0 >= 0.25:
            gaps.append((g0, g1, ss[i]["y"]))
    print("")
    if gaps:
        g0, g1, gy = max(gaps, key=lambda g: g[1] - g[0])
        t = (g0 + g1) / 2.0
        fno = min(n_dst - 1, max(0, int(round(t * fps))))
        band = band_of(gy, size, H)
        m = measure(a.video, a.out, fno, W, H, band)
        ok = m["frac"] <= GAP_MAX_FRAC
        print("  do 1 moc DANG LE KHONG CO CHU (%.2f-%.2fs):" % (g0, g1))
        print("      %s  t=%6.2fs frame %-5d: %d px doi trong dai = %.4f%%"
              % ("[OK]  " if ok else "[LOI] ", t, fno, m["inband"],
                 100 * m["frac"]))
        if not ok:
            fails.append(
                "o giay %.2f dang le khong co chu nhung dai chu doi %.3f%% "
                "-> co cum sub bi dinh lai tren man hinh." % (t, 100 * m["frac"]))
    else:
        print("  (khong co khoang trong >= 0.25s nao de kiem nguoc)")

    # --- ket luan ---
    print("")
    if fails:
        print("  " + C.hr("="))
        print("    KHONG DAT — %d loi." % len(fails))
        print("  " + C.hr("="))
        for i, f in enumerate(fails, 1):
            print("    %d) %s" % (i, f))
        print("")
        sys.exit(1)
    print("  " + C.hr("="))
    print("    DAT. Chu co that su hien tren video, so frame khong doi.")
    print("  " + C.hr("="))
    print("    file: %s" % os.path.abspath(a.out))
    print("")


if __name__ == "__main__":
    C.run_main(main)
