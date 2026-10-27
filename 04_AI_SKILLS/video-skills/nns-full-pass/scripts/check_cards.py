# -*- coding: utf-8 -*-
"""BUOC 6b — kiem the chu TRUOC khi ve. Khong dat thi khong duoc burn.

    python scripts/check_cards.py --cards <x.cards.json> --words <x.sub.fixed.json> \
        --layout <x.layout.json> --font <font.ttf>

Luat cung (vi pham la exit 1):
  1. text khong rong, <= 4 chu, <= 2.5s, >= 0.4s
  2. hai the cach nhau >= 12s, khong chong thoi gian
  3. KHONG lap nguyen van loi thoai — doi chieu voi transcript
  4. KHONG in lai con so dang duoc noi quanh do
  5. font phai co du glyph (thieu -> libass ve khoang trong, khong bao loi)
  6. y nam trong khung va khong tut duoi vung an toan cua nen tang
  7. sau auto-fit van phai vua be ngang khung
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()

MAX_WORDS = 4
MAX_DUR = 2.5
MIN_DUR = 0.4
MIN_GAP = 12.0
ECHO_WINDOW = 6.0        # lap nguyen van: xet transcript trong +-6s
NUM_WINDOW = 4.0         # in lai con so: xet +-4s


def missing_glyphs(font_path, size, text):
    """Ky tu font KHONG co -> libass ve khoang trong, khong bao loi gi ca.

    KHONG dung cards_to_ass.missing_glyphs: no so voi getmask("") = (0,0), ma
    ky tu thieu lai tra ve (rong>0, cao=0) — nen phep so do khong bao gio khop
    va guard do im lang cho qua. Do that tren BeVietnamPro-ExtraBold:
        'a' -> (78, 65)      co glyph
        '→' -> (59,  0)      KHONG co glyph, van co be rong
    Luat dung: CAO == 0 trong khi ky tu khong phai khoang trang.
    """
    from PIL import ImageFont
    f = ImageFont.truetype(font_path, size)
    bad = []
    for ch in sorted(set(text)):
        if ch.isspace() or ch in "\\N":
            continue
        try:
            if f.getmask(ch).size[1] == 0:
                bad.append(ch)
        except Exception:
            bad.append(ch)
    return bad


def norm(s):
    s = unicodedata.normalize("NFC", (s or "").lower())
    s = s.replace("\\N", " ")
    s = re.sub(r"[^0-9a-zÀ-ỹ\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def load_words(path):
    d = C.read_json(path)
    if isinstance(d, dict):
        d = d.get("words") or d.get("tokens") or []
    out = []
    for w in d:
        t = w.get("w") if "w" in w else w.get("word", "")
        if w.get("start") is None:
            continue
        out.append({"w": (t or "").strip(), "start": float(w["start"]),
                    "end": float(w.get("end", w["start"]))})
    return out


def spoken_between(words, t0, t1):
    return norm(" ".join(w["w"] for w in words
                         if t0 <= w["start"] <= t1 or t0 <= w["end"] <= t1))


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(description="Kiem the chu truoc khi ve")
    ap.add_argument("--cards")
    ap.add_argument("--words")
    ap.add_argument("--layout")
    ap.add_argument("--font")
    ap.add_argument("--resources")
    ap.add_argument("--min-gap", dest="min_gap", type=float, default=MIN_GAP)
    ap.add_argument("--max-words", dest="max_words", type=int, default=MAX_WORDS)
    ap.add_argument("--allow-echo", dest="allow_echo", action="store_true",
                    help="TAT luat 'khong lap loi thoai' (chi khi co y)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.cards:
        C.die("thieu --cards.\n"
              "    python scripts/check_cards.py --cards <x.cards.json> "
              "--words <x.sub.fixed.json> --layout <x.layout.json>")
    if not os.path.isfile(a.cards):
        C.die("khong thay file the: %s" % a.cards)
    cards = C.read_json(a.cards)
    if isinstance(cards, dict):
        cards = cards.get("text_cards") or cards.get("cards") or []

    lay = C.read_json(a.layout) if a.layout and os.path.isfile(a.layout) else {}
    w = int(lay.get("w") or 1080)
    h = int(lay.get("h") or 1920)
    bottom_safe = int(lay.get("bottom_safe") or (h - 330 * h / 1920.0))
    words = load_words(a.words) if a.words and os.path.isfile(a.words) else []

    font = a.font
    if not font:
        res = C.resolve_font(a.resources, None, verbose=False)
        font = res.get("file")
    if not font or not os.path.isfile(font):
        C.die("khong tim ra font de do the chu. Dua --font \"<file.ttf>\".")

    F.add_tools_path()
    import cards_to_ass as K

    F.banner("BUOC 6b — KIEM THE CHU",
             ["file the : %s (%d the)" % (os.path.basename(a.cards), len(cards)),
              "font     : %s" % os.path.basename(font),
              "khung    : %dx%d, y toi da %d" % (w, h, bottom_safe),
              "transcript: %s" % ("%d tu" % len(words) if words
                                  else "(khong co -> BO QUA luat lap loi thoai)")])

    bad = []

    def fail(i, c, msg, how=""):
        bad.append((i, c.get("text", ""), msg, how))

    if not cards:
        C.die("khong co the nao trong %s.\n"
              "  Muon bo han the chu thi chay lai voi --no-cards, dung de file rong."
              % a.cards)

    order = sorted(enumerate(cards, 1), key=lambda x: float(x[1]["start"]))
    prev = None
    for i, c in order:
        text = (c.get("text") or "").strip()
        st, en = float(c["start"]), float(c["end"])

        if not text:
            fail(i, c, "text CON RONG (cho dat do plan_cues.py de ra)",
                 "Dien noi dung, hoac XOA the nay khoi file.")
            continue
        nw = len([x for x in re.split(r"\s+", text.replace("\\N", " ")) if x])
        if nw > a.max_words:
            fail(i, c, "%d chu, qua %d" % (nw, a.max_words), "Rut ngan lai.")
        if en - st > MAX_DUR + 1e-6:
            fail(i, c, "dai %.2fs, qua %.1fs" % (en - st, MAX_DUR),
                 "Ha `end` xuong.")
        if en - st < MIN_DUR:
            fail(i, c, "chi %.2fs, ngan hon %.1fs -> nhay mot cai la mat"
                 % (en - st, MIN_DUR), "Keo `end` ra.")
        if prev is not None:
            if st < prev["end"] - 1e-6:
                fail(i, c, "chong thoi gian voi the truoc (%.2f-%.2f)"
                     % (prev["start"], prev["end"]), "Doi mot trong hai.")
            elif st - prev["start"] < a.min_gap - 1e-6:
                fail(i, c, "chi cach the truoc %.2fs (toi thieu %.0fs)"
                     % (st - prev["start"], a.min_gap),
                     "Bo bot mot the, hoac keo xa ra.")
        prev = c

        # --- lap nguyen van loi thoai
        if words and not a.allow_echo:
            around = spoken_between(words, st - ECHO_WINDOW, en + ECHO_WINDOW)
            n = norm(text)
            if n and n in around:
                fail(i, c, "LAP NGUYEN VAN loi thoai quanh %.2fs" % st,
                     "The phai noi thu sub CHUA noi. Doi cach dien dat.")
            nums = set(re.findall(r"\d+", text))
            if nums:
                near = spoken_between(words, st - NUM_WINDOW, en + NUM_WINDOW)
                dup = [x for x in nums if re.search(r"\b%s\b" % re.escape(x), near)]
                if dup:
                    fail(i, c, "in lai con so dang duoc noi: %s" % ", ".join(dup),
                         "Man hinh/sub da co so nay roi. Bo so di.")

        # --- glyph
        size = K.CARD_STYLES.get(c.get("style") or "punch",
                                 K.CARD_STYLES["punch"])["size"]
        miss = missing_glyphs(font, size, text)
        if miss:
            fail(i, c, "font khong co ky tu %s"
                 % " ".join("U+%04X(%s)" % (ord(x), x) for x in miss),
                 "libass se ve KHOANG TRONG chu khong bao loi. Doi ky tu khac.")
            continue

        # --- vi tri + be rong sau auto-fit
        y = int(c.get("y", 0))
        if not (0 < y <= h):
            fail(i, c, "y=%d nam ngoai khung cao %d" % (y, h), "")
        elif y > bottom_safe:
            fail(i, c, "y=%d tut duoi vung an toan (%d) -> UI TikTok/Facebook che"
                 % (y, bottom_safe), "Day the LEN, dung day xuong.")
        budget = w - 120
        fs, ftext = K.fit(font, size, text, budget)
        wpx = K.measure(font, fs, ftext)
        if wpx > budget + 1:
            fail(i, c, "rong %.0fpx > khung cho phep %dpx du da thu nho + xuong dong"
                 % (wpx, budget), "Rut ngan chu.")
        c["_size"], c["_text"] = fs, ftext
        if c.get("plate"):
            pw, ph, px, py = K.plate_box(font, fs, ftext, w // 2, y)
            if px < 10 or px + pw > w - 10:
                fail(i, c, "khung the tran le (x %d..%d, khung rong %d)"
                     % (px, px + pw, w), "Rut ngan chu.")
            if py < 10:
                fail(i, c, "khung the tran mep tren (y=%d)" % py, "Ha y xuong.")

    print("")
    print("  %-3s %-13s %5s %-6s %-5s %s"
          % ("#", "thoi gian", "y", "co chu", "khung", "noi dung sau auto-fit"))
    print("  " + F.hr("-"))
    for i, c in order:
        print("  %-3d %-13s %5s %-6s %-5s %s"
              % (i, "%.2f-%.2f" % (float(c["start"]), float(c["end"])),
                 c.get("y", "?"),
                 "%dpx" % c["_size"] if c.get("_size") else "-",
                 "co" if c.get("plate") else "-",
                 (c.get("_text") or c.get("text") or "(rong)").replace("\\N", " / ")))
    print("  " + F.hr("-"))

    if bad:
        print("")
        print("  KHONG DAT — %d loi. Khong duoc burn khi con loi nao." % len(bad))
        for i, text, msg, how in bad:
            print("")
            print("    the %d \"%s\"" % (i, text or "(rong)"))
            print("      %s" % msg)
            if how:
                print("      -> %s" % how)
        print("")
        sys.exit(1)

    print("")
    print("  DAT. %d the deu hop le: du ngan, du thua, khong lap loi thoai," % len(cards))
    print("       font co du glyph, va nam trong vung an toan.")
    print("")


if __name__ == "__main__":
    C.run_main(main)
