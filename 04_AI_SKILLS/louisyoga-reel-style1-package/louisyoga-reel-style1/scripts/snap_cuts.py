# -*- coding: utf-8 -*-
"""Bien danh sach cat tho (theo moc tu cua ho so) thanh cuts.json an toan, KHONG can ngoi do tay tung mep.

    python snap_cuts.py --video raw.mp4 --rough work/cuts_rough.json --out work/cuts.json [--auto-pauses] [--report work/cuts_report.md]

cuts_rough.json: [[start, end, "ly do"], ...] giay file goc — lay thang tu moc tu trong .hoso.words.json
                 (vd bo cau lap: [start tu dau, end tu cuoi]). Doan cuoi co the ghi 999 = cat duoi.
- Moi mep duoc keo vao diem nang luong thap nhat trong ±0.15 s (uu tien vung lang that). Moc Whisper hay
  nuot khoang lang vao tu, nen mep tho thuong roi giua tieng noi -> buoc nay chua chinh xac.
- Mep van con to (> muc giong −10 dB) -> canh bao "NGHE LAI" trong bao cao.
- --auto-pauses: tu tim cho ngung >= 0.30 s giua loi (ke ca ben trong tu bi keo dai) va rut con ~0.12 s.
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

HOP = 0.01  # 10 ms frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--rough", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--auto-pauses", action="store_true")
    ap.add_argument("--min-pause", type=float, default=0.30)
    ap.add_argument("--report")
    a = ap.parse_args()
    x = K.load_audio(a.video, 16000)
    hop = int(16000 * HOP)
    n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    db = np.convolve(db, np.ones(3) / 3, "same")  # 30 ms smoothing
    dur = n * HOP
    speech = np.percentile(db[db > -45], 60)
    quiet = speech - 15

    def snap(t, win=0.15):
        if t <= 0.02 or t >= dur - 0.02:
            return max(0.0, min(t, dur))
        i0, i1 = max(0, int((t - win) / HOP)), min(n, int((t + win) / HOP))
        # lowest energy, but each 10 ms away from the rough mark costs 0.4 dB -> stays on the nearest real gap
        ts = np.arange(i0, i1) * HOP
        j = i0 + int(np.argmin(db[i0:i1] + 40 * np.abs(ts - t)))
        return round(j * HOP, 3)

    rows, cuts = [], []
    for item in K.read_json(a.rough):
        c0, c1 = float(item[0]), float(item[1])
        why = item[2] if len(item) > 2 else ""
        s0 = snap(c0)
        s1 = snap(c1) if c1 < dur else 999
        e0 = db[min(n - 1, int(s0 / HOP))]
        e1 = db[min(n - 1, int(s1 / HOP))] if s1 < 999 else -99
        flag = "NGHE LAI" if max(e0, e1) > speech - 10 else ""
        cuts.append([s0, s1])
        rows.append(f"| {c0:.2f}–{c1:.2f} | {s0:.3f}–{s1:.3f} | {e0:.0f} / {e1:.0f} dB | {why} | {flag} |")
    if a.auto_pauses:
        q = db < quiet
        k = 0
        while k < n:
            if q[k]:
                j = k
                while j < n and q[j]:
                    j += 1
                t0, t1 = k * HOP, j * HOP
                inside = any(c0 - 0.05 <= t0 and t1 <= c1 + 0.05 for c0, c1 in cuts)
                if t1 - t0 >= a.min_pause and t0 > 0.3 and t1 < dur - 0.3 and not inside:
                    cuts.append([round(t0 + 0.06, 3), round(t1 - 0.06, 3)])
                    rows.append(f"| (lang {t1 - t0:.2f}s) | {t0 + 0.06:.3f}–{t1 - 0.06:.3f} | lang | rut khoang ngung | |")
                k = j
            else:
                k += 1
    cuts.sort()
    merged = []
    for c in cuts:
        if merged and c[0] <= merged[-1][1] + 0.05:
            merged[-1][1] = max(merged[-1][1], c[1])
        else:
            merged.append(c)
    K.write_json(a.out, merged)
    removed = sum(min(c1, dur) - c0 for c0, c1 in merged)
    print(f"  {len(merged)} doan cat, bo {removed:.1f}s: {dur:.1f}s -> {dur - removed:.1f}s  -> {a.out}")
    warn = sum(1 for r in rows if "NGHE LAI" in r)
    if warn:
        print(f"  {warn} mep cat con tieng noi (NGHE LAI) — xem bao cao")
    if a.report:
        with open(a.report, "w", encoding="utf-8") as fh:
            fh.write(f"# Bang cat (muc giong ~{speech:.0f} dB)\n\n| tho (s) | sau khi keo (s) | nang luong 2 mep | ly do | |\n|---|---|---|---|---|\n")
            fh.write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
