# -*- coding: utf-8 -*-
"""Nghe lai MOT khung ngan de chot diem cat bang tay (dung khi refine_report bao
TIGHT/NOMATCH hoac verify_report bao CANH BAO).

    python listen.py --video "<video>" --at 1094.4-1095.9 [--at 1296-1304 ...]

In ra: tung chu kem moc (large-v3) + nang luong moi 20 ms (so = -dB; >= ~28 la lang,
<= ~20 la dang noi). Diem cat nen dat trong mot day so lon (>= 28) dai >= 80 ms.
Luu y: Whisper nghe khung ngan doi khi BIA cau ("Hay subscribe cho kenh...",
"Cam on cac ban da theo doi") — tin nang luong hon tin chu o nhung cho nay.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dccommon as C  # noqa: E402


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--at", action="append", required=True, help="t0-t1 (giay hoac HH:MM:SS.mmm)")
    ap.add_argument("--no-words", action="store_true", help="chi in nang luong (khong nap Whisper)")
    a = ap.parse_args()
    C.need_ffmpeg()
    m = None if a.no_words else C.load_whisper()[0]
    for rng in a.at:
        t0, t1 = [C.ts2s(x) for x in rng.split("-", 1)] if rng.count(":") == 0 else \
            [C.ts2s(x) for x in rng.split("-")]
        x = C.load_pcm(a.video, t0, t1 - t0)
        print("\n[%s -> %s]" % (C.s2ts(t0), C.s2ts(t1)))
        if m is not None:
            _, W = C.words_of(m, x, t0)
            print("  chu: " + " ".join("%s[%.2f-%.2f]" % (w["w"], w["start"], w["end"]) for w in W))
        env = C.envelope_db(x)
        row = []
        for k in range(0, len(env), 2):
            row.append("%.2f:%d" % (t0 + k / 100.0, int(-env[k:k + 2].mean())))
        for i in range(0, len(row), 10):
            print("  " + "  ".join(row[i:i + 10]))


if __name__ == "__main__":
    main()
