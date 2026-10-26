# -*- coding: utf-8 -*-
"""Goi y cho cat: tu dem, cau lap, ngap ngung — kem ho so nang luong de dat diem cat vao IM LANG THAT.

    python analyze_pauses.py --video raw.mp4 --words work/src.words.json --out work/cut_suggestions.md

Khong tu cat. In ra bang goi y + ho so am (moi ky tu = 50 ms: '_' < -45 dB, '.' -45..-35, '#' tieng noi)
de Claude chon cuts.json roi DUA NGUOI DUNG DUYET.
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

FILLERS = [
    ["ví", "dụ", "như", "là"], ["ví", "dụ", "như"], ["chẳng", "hạn"], ["kiểu", "như"], ["nói", "chung", "là"],
    ["các", "cái"], ["cái"], ["thì", "là"], ["ừ"], ["ờ"], ["à"], ["ừm"], ["ậm"], ["đấy"], ["nhá"], ["ấy"],
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--words", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = K.read_json(a.words)
    ws = d["words"]
    x = K.load_audio(a.video, 16000)
    hop = 160
    n = len(x) // hop
    r = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)

    def prof(t0, t1):
        seg = r[int(t0 * 100): int(t1 * 100)][::5]
        return "".join("_" if v < -45 else ("." if v < -35 else "#") for v in seg)

    low = [w["w"].lower().strip(".,?!") for w in ws]
    rows = []
    # fillers
    for i in range(len(ws)):
        for pat in FILLERS:
            if low[i: i + len(pat)] == pat:
                a0, b0 = ws[i]["start"], ws[i + len(pat) - 1]["end"]
                ctx = " ".join(w["w"] for w in ws[max(0, i - 5): i]) + " [" + " ".join(w["w"] for w in ws[i: i + len(pat)]) + "] " + " ".join(w["w"] for w in ws[i + len(pat): i + len(pat) + 5])
                rows.append((a0, b0, "tu dem", ctx))
                break
    # long gaps / dragged words
    for i in range(1, len(ws)):
        gap = ws[i]["start"] - ws[i - 1]["end"]
        if gap > 0.45:
            rows.append((ws[i - 1]["end"], ws[i]["start"], f"lang {gap:.2f}s", " ".join(w["w"] for w in ws[max(0, i - 4): i + 4])))
        if ws[i]["end"] - ws[i]["start"] > 0.9:
            rows.append((ws[i]["start"], ws[i]["end"], f"keo dai '{ws[i]['w']}' {ws[i]['end']-ws[i]['start']:.2f}s", ""))
    # repeated phrases (3-8 words said twice within 8 s): report only the longest, non-overlapping
    covered: set[int] = set()
    for L in (8, 7, 6, 5, 4, 3):
        for i in range(len(low) - L):
            if covered.intersection(range(i, i + L)):
                continue
            for j in range(i + L, min(len(low) - L, i + 30)):
                if low[i: i + L] == low[j: j + L] and ws[j]["start"] - ws[i]["start"] < 8:
                    rows.append((ws[i]["start"], ws[i + L - 1]["end"], f"lap {L} tu (giu lan sau, lan 2 o {ws[j]['start']:.2f}s)", " ".join(ws[k]["w"] for k in range(i, i + L))))
                    covered.update(range(i, i + L))
                    covered.update(range(j, j + L))
                    break
    rows.sort()
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("# Goi y cat (CHUA CAT) — duyet roi viet cuts.json: [[start,end],...] theo giay file goc\n\n")
        fh.write("Ho so am moi ky tu 50 ms: '_' im lang, '.' tho/rat nho, '#' tieng noi. Dat diem cat vao '_' hoac '.'.\n\n")
        fh.write("| tu (s) | den (s) | loai | ngu canh | ho so am (±0.3 s) |\n|---|---|---|---|---|\n")
        for a0, b0, kind, ctx in rows:
            fh.write(f"| {a0:.2f} | {b0:.2f} | {kind} | {ctx} | `{prof(max(0, a0 - 0.3), b0 + 0.3)}` |\n")
    print(f"  {len(rows)} goi y -> {a.out}")
    head = r[:100]
    print(f"  lang dau file: {np.argmax(head > -40) / 100:.2f}s (cat phan truoc moc nay)")


if __name__ == "__main__":
    main()
