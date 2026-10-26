# -*- coding: utf-8 -*-
"""Do truoc mat do + do to SFX cua 1 Reel.tsx (dung lai lop SFX tu danh sach CUES, khong can render).

    python measure_sfx.py --reel <project>/src/reel/Reel.tsx --voice work/voice_proc.wav --sfx-dir <project>/public/sfx [--sfx-rel -2.5]

Chuan da duyet (reel 2 + reel 3 v4): 0.45-0.7 tieng/giay, tieng thuong ~ -3 dB, punch ~ +6..+8 dB so voi giong.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

SR = 48000
ONSET = {"swoosh.mp3": 0.07, "quick-swoosh.mp3": 0.04, "pop.mp3": 0.23, "pop-2.mp3": 0.066, "punch.mp3": 0.107, "riser-metallic.mp3": 1.809,
         "camera-shutter.mp3": 0.04, "digital-counting-1.mp3": 0.063, "ding.mp3": 0.149, "quick-ting.mp3": 0.019, "correct.mp3": 0.079}


def mom(x, w=0.05):
    n = int(w * SR)
    k = len(x) // n
    return 20 * np.log10(np.sqrt((x[: k * n].reshape(k, n) ** 2).mean(1)) + 1e-9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reel", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--sfx-dir", required=True)
    ap.add_argument("--sfx-rel", type=float, default=-2.5)
    a = ap.parse_args()
    src = open(a.reel, encoding="utf-8").read()
    block = src.split("const CUES")[1].split("];")[0]
    cues = [(float(t), n, float(v)) for t, n, v in re.findall(r'\[([\d.]+), "([\w\-.]+)", ([\d.]+)\]', block)]
    v = K.load_audio(a.voice, SR)
    s = np.zeros(len(v) + SR * 4, np.float32)
    for t, name, vol in cues:
        x = K.load_audio(os.path.join(a.sfx_dir, name), SR) * vol * 10 ** (a.sfx_rel / 20)
        start = int(round((t - ONSET.get(name, 0)) * 30)) / 30
        if start < 0:
            x = x[int(-start * SR):]
            start = 0
        st = int(start * SR)
        s[st: st + len(x)] += x[: len(s) - st]
    vm, sm = mom(v), mom(s[: len(v)])
    vmed = np.percentile(vm[vm > -45], 50)
    idx = np.where(sm > -50)[0]
    g = np.split(idx, np.where(np.diff(idx) > 2)[0] + 1)
    pk = np.array([sm[x].max() for x in g if len(x)])
    dur = len(v) / SR
    print(f"  {len(cues)} cue / {dur:.1f}s = {len(cues)/dur:.2f}/s | tieng nghe duoc {len(pk)} = {len(pk)/dur:.2f}/s")
    print(f"  so voi giong: thuong {np.median(pk)-vmed:+.1f} dB, p90 {np.percentile(pk,90)-vmed:+.1f}, to nhat {pk.max()-vmed:+.1f}")
    print("  chuan: 0.45-0.7/s; thuong ~ -3; punch +6..+8")


if __name__ == "__main__":
    main()
