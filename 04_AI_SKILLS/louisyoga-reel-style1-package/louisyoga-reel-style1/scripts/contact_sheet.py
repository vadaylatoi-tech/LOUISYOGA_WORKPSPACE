# -*- coding: utf-8 -*-
"""Anh luoi khung hinh co ghi giay — de soi bo cuc / chon B-roll / QC ban cuoi.

    python contact_sheet.py --video in.mp4 --out sheet.jpg [--every 1] [--cols 14] [--width 135] [--start 0] [--dur 0]
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--every", type=float, default=1.0)
    ap.add_argument("--cols", type=int, default=14)
    ap.add_argument("--width", type=int, default=135)
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--dur", type=float, default=0)
    a = ap.parse_args()
    dur = float(K.ffprobe(a.video)["format"]["duration"]) - a.start if not a.dur else a.dur
    n = int(dur / a.every) + 1
    rows = (n + a.cols - 1) // a.cols
    fontfile = "C\\:/Windows/Fonts/arial.ttf" if os.name == "nt" else "/System/Library/Fonts/Supplemental/Arial.ttf" if sys.platform == "darwin" else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    draw = f"drawtext=fontfile='{fontfile}':text='%{{pts}}':x=3:y=3:fontsize=16:fontcolor=yellow:box=1:boxcolor=black" if os.path.exists(fontfile.replace("\\", "")) else "null"
    vf = f"fps=1/{a.every},scale={a.width}:-2,{draw},tile={a.cols}x{rows}"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(a.start), "-i", a.video]
    if a.dur:
        cmd += ["-t", str(a.dur)]
    K.run(cmd + ["-vf", vf, "-frames:v", "1", a.out], "contact sheet")
    print(f"  -> {a.out}")


if __name__ == "__main__":
    main()
