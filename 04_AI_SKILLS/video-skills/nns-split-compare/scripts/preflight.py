# -*- coding: utf-8 -*-
"""Kiem moi thu can truoc khi dung. THIEU thi dung han, khong doan."""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def row(ok, name, detail):
    print("    [%s]  %-22s %s" % ("OK" if ok else "!!", name, detail))


def main():
    C.setup_io()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", "--left", dest="video", required=True,
                    help="video THO (ben trai)")
    ap.add_argument("--right", default=None,
                    help="ban AI da cat (bo qua = skill tu cat bang nns-cut-silence)")
    ap.add_argument("--out", default=None)
    ap.add_argument("--resources", default=None)
    a = ap.parse_args()

    C.head("PREFLIGHT")
    miss = []

    for t in ("ffmpeg", "ffprobe"):
        p = C.tool(t)
        row(bool(p), t, p or "KHONG CO")
        if not p:
            miss.append((t, "Windows: winget install Gyan.FFmpeg  ·  macOS: brew install ffmpeg"
                            "  ·  Linux: sudo apt install ffmpeg. Mo lai terminal roi go '%s -version'." % t))

    row(True, "python", sys.version.split()[0])

    try:
        import PIL
        row(True, "Pillow", PIL.__version__)
    except Exception:
        row(False, "Pillow", "KHONG CO")
        miss.append(("Pillow", "pip install Pillow   (hoac: python -m pip install Pillow)"))

    fdir = C.font_dir(a.resources)
    row(bool(fdir), "font Be Vietnam Pro", fdir or "KHONG THAY")
    if not fdir:
        miss.append(("font Be Vietnam Pro",
                     "Tai o https://fonts.google.com/specimen/Be+Vietnam+Pro, giai nen vao\n"
                     "       <thu-muc>/Font/Be_Vietnam_Pro/ roi goi --resources \"<thu-muc>\".\n"
                     "       Font PHAI co dau tieng Viet — Arial/Impact khong co."))

    if not os.path.isfile(a.video):
        row(False, "video thO (trai)", "KHONG THAY: %s" % a.video)
        miss.append(("video thO", "Kiem lai duong dan --video."))
    elif C.tool("ffprobe"):
        v = C.probe(a.video)
        row(True, "video thO (trai)", "%dx%d %.3ffps %.2fs %d frame (%s)"
            % (v["w"], v["h"], v["fps"], v["dur_frames"], v["nframes"], v["codec"]))
        row(v["has_audio"], "  stream audio", ("%dHz %dch" % (v["ar"], v["ac"]))
            if v["has_audio"] else "KHONG CO TIENG")
        if not v["has_audio"]:
            miss.append(("tieng cua video thO",
                         "Video so sanh phat tieng cua tung ben. Ghep tieng vao truoc:\n"
                         "       ffmpeg -i silent.mp4 -i voice.wav -map 0:v -map 1:a -c:v copy -c:a aac co_tieng.mp4"))
        row(v["cfr"], "  fps co dinh (CFR)",
            "r_frame_rate == avg_frame_rate" if v["cfr"]
            else "VFR (%s vs %s)" % (v["r_frame_rate"], v["avg_frame_rate"]))
        if not v["cfr"]:
            miss.append(("fps co dinh",
                         "ffmpeg -i \"%s\" -c:v libx264 -crf 16 -r 30 -c:a copy cfr.mp4" % a.video))

    if a.right:
        if not os.path.isfile(a.right):
            row(False, "ban AI (phai)", "KHONG THAY: %s" % a.right)
            miss.append(("ban AI (--right)", "Kiem lai duong dan, hoac bo --right de skill tu cat."))
        elif C.tool("ffprobe"):
            r = C.probe(a.right)
            row(True, "ban AI (phai)", "%dx%d %.3ffps %.2fs %d frame"
                % (r["w"], r["h"], r["fps"], r["dur_frames"], r["nframes"]))
            row(r["has_audio"], "  stream audio",
                ("%dHz %dch" % (r["ar"], r["ac"])) if r["has_audio"] else "KHONG CO TIENG")
    else:
        cut = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), "nns-cut-silence", "scripts", "cut_silence.py")
        ok = os.path.isfile(cut)
        row(ok, "nns-cut-silence", cut if ok else "KHONG THAY")
        if not ok:
            miss.append(("skill nns-cut-silence",
                         "Bo --right nghia la skill nay tu cat khoang lang bang nns-cut-silence.\n"
                         "       Cai skill do vao .claude/skills/nns-cut-silence/, hoac tu cat roi\n"
                         "       truyen ban da cat qua --right \"<file>.mp4\"."))

    if a.out:
        d = os.path.dirname(os.path.abspath(a.out)) or "."
        ok = os.path.isdir(d) or not os.path.exists(d)
        row(ok, "--out", a.out)

    print("")
    if miss:
        print("  THIEU %d thu. Lam theo huong dan roi chay lai:" % len(miss))
        print("")
        for i, (what, how) in enumerate(miss, 1):
            print("   %d) %s" % (i, what))
            print("      %s" % how)
            print("")
        sys.exit(1)

    print("  DAY DU. Co the chay tiep.")
    print("")
    print("  Buoc tiep theo (1 phat ca chuoi):")
    print("      python scripts/run.py --video \"%s\" --out \"<ket-qua>.mp4\"" % a.video)
    print("")


if __name__ == "__main__":
    main()
