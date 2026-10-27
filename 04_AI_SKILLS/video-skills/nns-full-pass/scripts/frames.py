# -*- coding: utf-8 -*-
"""Sau khi render — trich san vai frame o cac moc dang soi.

    python scripts/frames.py --video <final.mp4> --plan <x.sub.plan.json> \
        [--cards <x.cards.json>] [--layout <x.layout.json>] [--dir <thu-muc>]

Trich bang select=eq(n\\,N). KHONG dung -ss: -ss nhay toi keyframe gan nhat nen
frame lay ra khong phai frame minh muon xem.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()


def grab(video, idx, path):
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video,
                        "-vf", "select=eq(n\\,%d)" % idx, "-fps_mode", "passthrough",
                        "-frames:v", "1", path], capture_output=True)
    return p.returncode == 0 and os.path.isfile(path)


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(description="Trich frame o cac moc quan trong")
    ap.add_argument("--video")
    ap.add_argument("--plan", help="x.sub.plan.json — lay moc cum sub")
    ap.add_argument("--cards", help="x.cards.json — lay moc giua moi the")
    ap.add_argument("--layout", help="x.layout.json — lay moc dau moi doan")
    ap.add_argument("--dir", help="thu muc ghi anh (mac dinh <video>_frames)")
    ap.add_argument("--max", type=int, default=12)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.video:
        C.die("thieu --video.\n    python scripts/frames.py --video <final.mp4> "
              "--plan <x.sub.plan.json>")
    if not os.path.isfile(a.video):
        C.die("khong thay video: %s" % a.video)

    info = C.probe_video(a.video)
    fps = info["fps"] or 30.0
    out = a.dir or (os.path.splitext(os.path.abspath(a.video))[0] + "_frames")

    picks = []
    if a.layout and os.path.isfile(a.layout):
        for s in (C.read_json(a.layout).get("segments") or []):
            picks.append((s["start"] + 0.35, "dau doan %.2f-%.2f (y=%d)"
                          % (s["start"], s["end"], s["y"])))
    if a.cards and os.path.isfile(a.cards):
        cards = C.read_json(a.cards)
        if isinstance(cards, dict):
            cards = cards.get("cards") or cards.get("text_cards") or []
        for i, c in enumerate(cards, 1):
            if not (c.get("text") or "").strip():
                continue
            picks.append(((float(c["start"]) + float(c["end"])) / 2.0,
                          "the %d \"%s\"" % (i, c["text"])))
    if a.plan and os.path.isfile(a.plan):
        ch = C.read_json(a.plan).get("chunks") or []
        for c in (ch[:1] + ch[len(ch) // 2:len(ch) // 2 + 1] + ch[-1:]):
            picks.append(((c["start"] + c["end"]) / 2.0, "cum sub"))
    if not picks:
        picks = [(info["duration"] * k / 5.0, "rai deu") for k in range(1, 5)]

    seen, rows = set(), []
    for t, why in sorted(picks):
        idx = int(round(t * fps))
        if idx in seen or len(rows) >= a.max:
            continue
        seen.add(idx)
        rows.append((idx, t, why))

    F.banner("TRICH FRAME DE SOI",
             ["video : %s (%.4g fps)" % (os.path.basename(a.video), fps),
              "thu muc: %s" % out,
              "so anh : %d" % len(rows)])

    if a.dry_run:
        print("")
        for idx, t, why in rows:
            print("  [dry-run] frame %6d  t=%7.2fs  %s" % (idx, t, why))
        print("")
        return

    if not os.path.isdir(out):
        os.makedirs(out)
    print("")
    for idx, t, why in rows:
        p = os.path.join(out, "f%06d_%07.2fs.png" % (idx, t))
        ok = grab(a.video, idx, p)
        print("  %s frame %6d  t=%7.2fs  %-34s %s"
              % ("OK " if ok else "SAI", idx, t, why,
                 os.path.basename(p) if ok else "(khong trich duoc)"))
    print("")
    print("  Mo thu muc: %s" % out)
    print("")


if __name__ == "__main__":
    C.run_main(main)
