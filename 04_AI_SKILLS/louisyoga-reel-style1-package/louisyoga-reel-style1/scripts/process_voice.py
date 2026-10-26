# -*- coding: utf-8 -*-
"""Lam giong noi RO + AM: loc rumble, khu on nhe, giu am 180 Hz, giam 'tieng hop' 450 Hz,
tang ro loi 3,2 / 5,5 kHz, them 'air' 9 kHz, nen 2.5:1, khu xi, chan dinh.

    python process_voice.py --in work/voice_raw.wav --out work/voice_proc.wav [--analyze]

--analyze in phan bo nang luong theo dai tan truoc/sau de quyet dinh co can chinh EQ khong
(giong goc bi duc khi dai 5-8 kHz < -25 dB so voi tong; bi 'hop' khi 300-600 Hz troi hon 150-300 Hz).
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

CHAIN = (
    "highpass=f=75,afftdn=nr=8:nf=-42,"
    "equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=450:t=q:w=1.2:g=-2.5,"
    "equalizer=f=3200:t=q:w=1:g=3,equalizer=f=5500:t=q:w=1.2:g=2.5,treble=g=2.5:f=9000,"
    "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2,deesser=i=0.25,alimiter=limit=0.89"
)


def bands(path):
    x = K.load_audio(path, 48000)
    hop = 4800
    fr = x[: len(x) // hop * hop].reshape(-1, hop)
    r = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    sp = fr[r > np.percentile(r, 40)]
    S = np.abs(np.fft.rfft(sp * np.hanning(hop), axis=1)).mean(0)
    fq = np.fft.rfftfreq(hop, 1 / 48000)
    tot = (S ** 2).sum()
    out = {}
    for a0, b0 in [(80, 150), (150, 300), (300, 600), (600, 1200), (1200, 2500), (2500, 5000), (5000, 8000), (8000, 12000)]:
        out[f"{a0}-{b0}"] = round(10 * np.log10((S[(fq >= a0) & (fq < b0)] ** 2).sum() / tot), 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--chain", default=CHAIN)
    ap.add_argument("--analyze", action="store_true")
    a = ap.parse_args()
    K.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-af", a.chain, "-ar", "48000", a.out], "xu ly giong")
    print(f"  -> {a.out}")
    if a.analyze:
        b1, b2 = bands(a.src), bands(a.out)
        print("  dai tan (dB so voi tong)   truoc   sau")
        for k in b1:
            print(f"  {k:>12} Hz            {b1[k]:6.1f} {b2[k]:6.1f}")


if __name__ == "__main__":
    main()
