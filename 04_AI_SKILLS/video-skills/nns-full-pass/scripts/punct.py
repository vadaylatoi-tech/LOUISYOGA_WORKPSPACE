# -*- coding: utf-8 -*-
"""BUOC 4b — dau cau cho transcript, TRUOC khi gom cum sub.

    python scripts/punct.py --words <x.sub.fixed.json>

Hai viec, deu nho nhung deu tung lam hong ban dung:

1. THEM DAU CHAM CUOI CAU. build_ass.py tach cum theo END_PUNCT (".!?...:;").
   Whisper rat hay bo quen dau cham o tu cuoi cung va o cho nguoi noi nghi dai.
   Thieu no thi cum cuoi bi dinh vao cum truoc, va plan_cues.py cung khong
   nhan ra dau cau de neo cue.

2. BIEN CAU LA BIEN MO. Cau moi bat dau tu tu NGAY SAU dau cham — chu khong
   phai tu chinh tu co dau cham. Moi cho trong skill nay dung dung mot luat do.

Mac dinh BO DAU PHAY khoi sub (giu trong ban dung ke hoach). Ly do: sub karaoke
chay tung tu, dau phay lo lung giua khung trong rat ban, va no con lam tach dong
sai cho. Muon giu thi them --keep-commas.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()

END_PUNCT = u".!?…:;"


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(description="Them dau cham cuoi cau cho transcript")
    ap.add_argument("--words", help="file .fixed.json (hoac .words.json)")
    ap.add_argument("--out", help="mac dinh ghi de len chinh --words")
    ap.add_argument("--gap-sentence", dest="gap_sentence", type=float, default=0.80,
                    help="nghi lau hon bao nhieu giay thi coi la het cau")
    ap.add_argument("--keep-commas", dest="keep_commas", action="store_true",
                    help="giu dau phay trong sub (mac dinh bo)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.words:
        C.die("thieu --words.\n    python scripts/punct.py --words <x.sub.fixed.json>")
    if not os.path.isfile(a.words):
        C.die("khong thay file: %s" % a.words)

    raw = C.read_json(a.words)
    words = raw.get("words") if isinstance(raw, dict) else raw
    if not words:
        C.die("transcript rong: %s" % a.words)

    key = "w" if "w" in words[0] else "word"
    added_gap = added_end = commas = 0

    for i, w in enumerate(words):
        t = (w.get(key) or "").strip()
        if not t:
            continue
        if not a.keep_commas and "," in t:
            t = t.replace(",", "")
            commas += 1
        last = i == len(words) - 1
        has_end = bool(t) and t[-1] in END_PUNCT
        if not has_end:
            if last:
                t += "."
                added_end += 1
            else:
                nxt = words[i + 1]
                pause = float(nxt.get("start", 0)) - float(w.get("end", 0))
                if pause >= a.gap_sentence:
                    t += "."
                    added_gap += 1
        w[key] = t

    n_sent = 1 + sum(1 for i, w in enumerate(words[:-1])
                     if (w.get(key) or "")[-1:] in END_PUNCT)

    F.banner("BUOC 4b — DAU CAU CHO TRANSCRIPT",
             ["file          : %s" % os.path.basename(a.words),
              "so tu         : %d" % len(words),
              "them '.' cuoi : %d (tu cuoi cung cua ca bai)" % added_end,
              "them '.' vi nghi lau (>= %.2fs): %d" % (a.gap_sentence, added_gap),
              "bo dau phay   : %s" % ("giu nguyen (--keep-commas)" if a.keep_commas
                                      else "%d tu" % commas),
              "so cau sau khi sua: %d  (bien cau la bien MO: cau moi bat dau tu"
              % n_sent,
              "                     tu NGAY SAU dau cham)"])

    if a.dry_run:
        print("")
        print("  [dry-run] khong ghi file.")
        print("")
        return

    out = a.out or a.words
    C.write_json(out, raw)
    print("")
    print("  da ghi: %s" % os.path.abspath(out))
    print("")


if __name__ == "__main__":
    C.run_main(main)
