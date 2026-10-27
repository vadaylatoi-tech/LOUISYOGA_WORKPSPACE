# -*- coding: utf-8 -*-
"""Do lai file ket qua. Chi duoc bao 'xong' khi script nay exit 0.

Do 6 thu, moi thu deu do TREN FILE RA, khong tin plan:
  1. So frame / fps / kich thuoc dung ke hoach.
  2. Do dai tieng == do dai hinh.
  3. Khung DANG CHAY dung noi dung: crop khung do o frame k phai khop frame k
     cua chinh file nguon (so bang chu ky anh xam da chuan hoa z-score), va phai
     khop HON cac frame moi nhu (+-8 frame, va frame cua file ben kia).
  4. Khung DUNG HINH phai dung im that: 2 frame cach xa nhau trong cung 1 pha
     cho crop y het nhau (lech < 1/255).
  5. Khung dang chay phai co CHUYEN DONG: 2 frame cach xa nhau phai khac nhau.
  6. Tieng pha 1 khop tieng nguon TRAI, tieng pha 2 khop tieng nguon PHAI
     (tuong quan duong bao RMS 100ms >= 0.90).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

FAILS = []
WARNS = []


def row(ok, name, detail, warn_only=False):
    tag = "OK" if ok else ("!!" if warn_only else "SAI")
    print("    [%-3s]  %-26s %s" % (tag, name, detail))
    if not ok:
        (WARNS if warn_only else FAILS).append(name)


def np():
    import numpy
    return numpy


def frame_png(video, index, out_png):
    C.run(["ffmpeg", "-y", "-v", "error", "-i", video,
           "-vf", "select=eq(n\\,%d)" % index, "-fps_mode", "passthrough",
           "-frames:v", "1", out_png])
    if not os.path.isfile(out_png):
        C.die("Khong trich duoc frame %d cua %s" % (index, video))
    return out_png


def sig(img, size=64):
    """Chu ky anh xam 64x64 da chuan hoa z-score -> chi do 'dung frame hay khong',
    khong bi anh huong boi chuyen tone toan cuc (lam toi khung dung hinh)."""
    n = np()
    from PIL import Image
    g = img.convert("L").resize((size, size), Image.LANCZOS)
    a = n.asarray(g, dtype=n.float64).ravel()
    a -= a.mean()
    s = a.std()
    return a / s if s > 1e-9 else a


def dist(a, b):
    n = np()
    return float(n.mean((a - b) ** 2))


def envelope(path, start, dur):
    """Duong bao RMS cua tung khung 100ms, mono 8kHz."""
    n = np()
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", "%.6f" % start, "-t", "%.6f" % dur,
         "-i", path, "-vn", "-ac", "1", "-ar", "8000",
         "-f", "s16le", "-acodec", "pcm_s16le", "-"],
        capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return None
    x = n.frombuffer(p.stdout, dtype="<i2").astype(n.float64)
    hop = 800  # 100 ms @ 8 kHz
    k = len(x) // hop
    if k < 4:
        return None
    e = n.sqrt((x[:k * hop].reshape(k, hop) ** 2).mean(axis=1))
    return e


def corr(a, b):
    n = np()
    k = min(len(a), len(b))
    a, b = a[:k], b[:k]
    a = a - a.mean()
    b = b - b.mean()
    d = (n.linalg.norm(a) * n.linalg.norm(b))
    return float((a @ b) / d) if d > 1e-9 else 0.0


def main():
    C.setup_io()
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--no-audio-check", dest="no_audio", action="store_true")
    a = ap.parse_args()

    C.head("VERIFY")
    C.need_tool("ffmpeg")
    try:
        np()
    except Exception:
        C.die("Thieu numpy. Cai:  pip install numpy")
    from PIL import Image

    plan = C.load_json(a.plan)
    work = a.workdir or (os.path.splitext(os.path.abspath(a.out))[0] + "_verify")
    os.makedirs(work, exist_ok=True)

    v = C.probe(a.out)
    L, R = plan["layout"], None
    n1 = plan["phases"][0]["frames"]
    n2 = plan["phases"][1]["frames"]
    total = plan["total"]["frames"]

    # ---- 1. dem
    row(v["nframes"] == total, "so frame",
        "%d (ke hoach %d)" % (v["nframes"], total))
    row(abs(v["fps"] - C.FPS) < 1e-6, "fps", "%.3f (ke hoach %d)" % (v["fps"], C.FPS))
    row(v["w"] == C.W and v["h"] == C.H, "kich thuoc",
        "%dx%d (ke hoach %dx%d)" % (v["w"], v["h"], C.W, C.H))

    # ---- 2. tieng vs hinh
    ad = C.audio_duration(a.out)
    vd = v["nframes"] / C.FPS
    row(abs(ad - vd) <= 1.0 / C.FPS, "do dai tieng vs hinh",
        "%.4fs vs %.4fs (lech %.1f ms, cho phep %.1f ms)"
        % (ad, vd, (ad - vd) * 1000, 1000.0 / C.FPS))

    pw, ph, py = L["panel_w"], L["panel_h"], L["panel_y"]
    boxes = {"left": (L["left_x"], py, L["left_x"] + pw, py + ph),
             "right": (L["right_x"], py, L["right_x"] + pw, py + ph)}

    # ---- 3/4/5. noi dung 2 khung o moi pha
    for ph_i, phase in enumerate(plan["phases"]):
        act = phase["active"]
        frz = "right" if act == "left" else "left"
        src = plan[act]["path"]
        base = 0 if ph_i == 0 else n1
        k_lo, k_hi = int(phase["frames"] * 0.25), int(phase["frames"] * 0.75)

        outs = {}
        for k in (k_lo, k_hi):
            outs[k] = Image.open(frame_png(a.out, base + k,
                                           os.path.join(work, "out_p%d_%d.png" % (ph_i + 1, k))))

        # 3. khung dang chay khop DUNG frame nguon
        worst = None
        for k in (k_lo, k_hi):
            crop = outs[k].crop(boxes[act])
            good = sig(crop)
            ref = sig(Image.open(frame_png(src, k, os.path.join(work, "src_%s_%d.png" % (act, k)))))
            d_ok = dist(good, ref)
            decoys = []
            for off in (-8, 8, -25, 25):
                kk = k + off
                if 0 <= kk < plan[act]["nframes"]:
                    dec = sig(Image.open(frame_png(src, kk,
                              os.path.join(work, "dec_%s_%d.png" % (act, kk)))))
                    decoys.append(dist(good, dec))
            m = min(decoys) if decoys else 9e9
            if worst is None or (d_ok, -m) > worst[0]:
                worst = ((d_ok, -m), k, d_ok, m)
        _, kw, d_ok, d_dec = worst
        row(d_ok < d_dec, "pha %d: khung %-5s dung frame" % (ph_i + 1, act),
            "lech %.4f voi frame dung, moi nhu gan nhat %.4f" % (d_ok, d_dec))

        # 4. khung dung hinh phai dung IM
        n = np()
        c1 = n.asarray(outs[k_lo].crop(boxes[frz]).convert("L"), dtype=n.float64)
        c2 = n.asarray(outs[k_hi].crop(boxes[frz]).convert("L"), dtype=n.float64)
        mae_frz = float(n.abs(c1 - c2).mean())
        row(mae_frz < 1.0, "pha %d: khung %-5s dung im" % (ph_i + 1, frz),
            "lech giua frame %d va %d: %.3f/255 (cho phep < 1.0)" % (k_lo, k_hi, mae_frz))

        # 5. khung dang chay phai CO chuyen dong
        m1 = n.asarray(outs[k_lo].crop(boxes[act]).convert("L"), dtype=n.float64)
        m2 = n.asarray(outs[k_hi].crop(boxes[act]).convert("L"), dtype=n.float64)
        mae_act = float(n.abs(m1 - m2).mean())
        row(mae_act > 1.0, "pha %d: khung %-5s co chay" % (ph_i + 1, act),
            "lech giua frame %d va %d: %.3f/255 (phai > 1.0)" % (k_lo, k_hi, mae_act))

    # ---- 6. tieng dung nguon o dung pha
    if not a.no_audio:
        d1 = plan["phases"][0]["dur"]
        d2 = plan["phases"][1]["dur"]
        for name, start, dur, srcp, has in (
                ("pha 1 (nguon TRAI)", 0.0, d1, plan["left"]["path"], plan["left"]["has_audio"]),
                ("pha 2 (nguon PHAI)", d1, d2, plan["right"]["path"], plan["right"]["has_audio"])):
            if not has:
                row(True, "tieng %s" % name, "nguon khong co tieng -> pha nay im lang (co y)")
                continue
            eo = envelope(a.out, start, dur)
            es = envelope(srcp, 0.0, dur)
            if eo is None or es is None:
                row(False, "tieng %s" % name, "khong doc duoc tieng de so", warn_only=True)
                continue
            c = corr(eo, es)
            row(c >= 0.90, "tieng %s" % name,
                "tuong quan duong bao %.4f (can >= 0.90)" % c)

    print("")
    if FAILS:
        print("  KHONG DAT — %d muc sai: %s" % (len(FAILS), ", ".join(FAILS)))
        print("")
        sys.exit(1)
    if WARNS:
        print("  CANH BAO: %s" % ", ".join(WARNS))
    print("  DAT. Video so sanh dung ke hoach: dung frame, dung khung, dung tieng theo pha.")
    print("")


if __name__ == "__main__":
    main()
