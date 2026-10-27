# -*- coding: utf-8 -*-
"""Gom tu thanh cum roi xuat file .ASS sub karaoke word-by-word.

    python scripts/build_ass.py --video <video> --out <video_ra.mp4> \
        [--max-words 4] [--max-chars 22] [--gap 0.35] \
        [--y 1536] [--safe "0-12:1100,12-30:1536"] \
        [--font-size 80] [--outline 7] \
        [--active-color "#FFD600"] [--base-color "#FFFFFF"]

KHONG DUNG TAG \\k. Da kiem tren may nay: \\k boi mau phan CHUA doc toi,
tuc nguoc y muon. Cach dung o day: moi TU phat MOT dong Dialogue rieng,
dong nao cung cho ca cum, chi khac o cho tu dang doc duoc boc bang
{\\c&H..&} ... {\\c&H..&} — mau ghi thang, khong nho vao \\k.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nnscommon as C  # noqa: E402

END_PUNCT = u".!?…:;"
SOFT_PUNCT = u","

# Cum ngan hon nguong nay thi khong cat theo ranh vung an toan nua — thay vao
# do cho no y cua doan sau. 0.15s = ~4-5 frame, duoi muc do la nhay nhay.
MIN_CHUNK_DUR = 0.15


# --------------------------------------------------------------------------
# mau: nhan #RRGGBB hoac &HAABBGGRR, luon xuat ra dang ASS &HAABBGGRR
# --------------------------------------------------------------------------

def to_ass_color(text, what="mau"):
    s = str(text).strip()
    if s.lower().startswith("&h"):
        body = s[2:].rstrip("&")
        if not re.fullmatch(r"[0-9a-fA-F]{6,8}", body or ""):
            C.die("%s '%s' khong dung dang &HAABBGGRR" % (what, text))
        return "&H" + body.upper().rjust(8, "0") + "&"
    s = s.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        C.die("%s '%s' khong hieu duoc.\n"
              "  Dung dang #RRGGBB (vd #FFD600) hoac &HAABBGGRR (vd &H0000D6FF&)"
              % (what, text))
    r, g, b = s[0:2], s[2:4], s[4:6]
    # ASS la &HAABBGGRR — dao thu tu so voi HTML, AA=00 la duc hoan toan
    return ("&H00%s%s%s&" % (b, g, r)).upper()


def ass_escape(text):
    """Chu trong Dialogue khong duoc chua { } (libass hieu la tag)."""
    return (text.replace("\\", "/").replace("{", "(").replace("}", ")")
                .replace("\r", " ").replace("\n", " "))


# --------------------------------------------------------------------------
# vung an toan theo thoi gian: --safe "a-b:y,c-d:y"
# --------------------------------------------------------------------------

def parse_safe(spec, video_h):
    """Tra ve list (start, end, y) da sap xep."""
    if not spec:
        return []
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*-\s*([0-9]*\.?[0-9]+)\s*:"
                         r"\s*(-?[0-9]+)\s*", part)
        if not m:
            C.die("--safe sai dang o doan '%s'.\n"
                  '  Dung dang:  --safe "0-12:1100,12-30:1536"\n'
                  "  nghia la: giay 0..12 dat sub o y=1100, giay 12..30 dat o y=1536"
                  % part)
        a, b, y = float(m.group(1)), float(m.group(2)), int(m.group(3))
        if b <= a:
            C.die("--safe doan '%s': giay ket thuc phai lon hon giay bat dau"
                  % part)
        if not (0 <= y <= video_h):
            C.die("--safe doan '%s': y=%d nam ngoai khung cao %d px"
                  % (part, y, video_h))
        out.append((a, b, y))
    out.sort()
    for i in range(len(out) - 1):
        if out[i][1] > out[i + 1][0] + 1e-9:
            C.die("--safe co 2 doan chong nhau: %.2f-%.2f va %.2f-%.2f"
                  % (out[i][0], out[i][1], out[i + 1][0], out[i + 1][1]))
    return out


class Layout(object):
    def __init__(self, safe, default_y):
        self.safe = safe
        self.default_y = default_y
        # moc GIAO NHAU giua cac vung — cum sub KHONG duoc vat qua cac moc nay
        self.bounds = sorted({t for a, b, _y in safe for t in (a, b)})

    def y_at(self, t):
        for a, b, y in self.safe:
            if a - 1e-9 <= t < b:
                return y
        return self.default_y

    def next_change(self, t, y):
        """Moc dau tien sau t ma y doi khac -> dung de CAT NGAN cum."""
        for b in self.bounds:
            if b > t + 1e-9 and self.y_at(b) != y:
                return b
        return None


# --------------------------------------------------------------------------
# do BE RONG chu that bang libass (khong doan)
# --------------------------------------------------------------------------

CALIB_TEXT = u"những đường cong ắt phải đủ rộng ẩm ướt AI Claude 0123"


def calibrate_char_px(font, family, bold, size):
    h = max(120, int(size * 2.5))
    r = C.render_ink(CALIB_TEXT, font, family, bold, size=size, w=3200, h=h)
    if r["ink"] <= 0 or r["w"] <= 0:
        C.die("khong do duoc be rong chu — libass ve ra khung trong.\n"
              "  Chay lai preflight de kiem font.")
    return r["w"] / float(len(CALIB_TEXT)), r


def measure_text_px(text, font, family, bold, size):
    h = max(120, int(size * 2.5))
    r = C.render_ink(text, font, family, bold, size=size, w=3200, h=h)
    return r["w"]


# --------------------------------------------------------------------------
# gom tu thanh cum
# --------------------------------------------------------------------------

def chunk_words(words, layout, max_words, max_chars, gap, px_budget,
                char_px, break_punct):
    chunks = []
    cur = []
    reasons = []

    def flush(reason):
        if not cur:
            return
        start = cur[0]["start"]
        y = layout.y_at(start)
        end = max(w["end"] for w in cur)
        cut = layout.next_change(start, y)
        clamped = snapped = False
        if cut is not None and end > cut:
            if cut - start < MIN_CHUNK_DUR:
                # Cum nay gan nhu nam tron ben kia ranh gioi. Cat ngan no chi
                # con vai frame se thanh cai nhay nhay. Cho no luon y cua doan
                # SAU ranh gioi va giu nguyen do dai — dung cho hon la de sai
                # cho gan nua giay.
                y = layout.y_at(cut + 1e-6)
                snapped = True
            else:
                end = cut
                clamped = True
        chunks.append({"words": [dict(w) for w in cur],
                       "start": start, "end": round(end, 3),
                       "y": y, "clamped_to_boundary": clamped,
                       "snapped_to_next_zone": snapped,
                       "break_reason": reason})
        reasons.append(reason)
        del cur[:]

    for w in words:
        if cur:
            y_cur = layout.y_at(cur[0]["start"])
            y_new = layout.y_at(w["start"])
            text_try = " ".join(x["w"] for x in cur + [w])
            why = None
            if y_new != y_cur:
                # LUAT CUNG: khong bao gio de 1 cum vat qua ranh vung an toan.
                # Neu vat, cum se giu y cua doan truoc va co the de len mat.
                why = "ranh vung an toan (y %d -> %d)" % (y_cur, y_new)
            elif w["start"] - cur[-1]["end"] >= gap:
                why = "khoang nghi %.2fs" % (w["start"] - cur[-1]["end"])
            elif len(cur) + 1 > max_words:
                why = "du %d tu" % max_words
            elif len(text_try) > max_chars:
                why = "du %d ky tu" % max_chars
            elif char_px and len(text_try) * char_px > px_budget:
                why = "uoc rong %d px > %d px" % (
                    int(len(text_try) * char_px), px_budget)
            elif break_punct and cur[-1]["w"][-1:] in END_PUNCT:
                why = "het cau"
            elif (break_punct and cur[-1]["w"][-1:] in SOFT_PUNCT
                  and len(cur) >= 2):
                why = "dau phay"
            if why:
                flush(why)
        cur.append(w)
    flush("het transcript")
    return chunks


def karaoke_events(chunk, base_c, active_c, video_w):
    """Moi TU mot dong Dialogue; ca dong cho ca cum; tu dang doc doi mau."""
    ws = chunk["words"]
    ev = []
    for i, w in enumerate(ws):
        start = max(w["start"], chunk["start"])
        if i + 1 < len(ws):
            end = max(ws[i + 1]["start"], start + 0.04)
        else:
            end = chunk["end"]
        end = min(end, chunk["end"])
        if end <= start + 1e-4:
            continue
        parts = []
        for j, x in enumerate(ws):
            t = ass_escape(x["w"])
            if j == i:
                parts.append("{\\c%s}%s{\\c%s}" % (active_c, t, base_c))
            else:
                parts.append(t)
        ev.append({"start": round(start, 3), "end": round(end, 3),
                   "y": chunk["y"], "active": i,
                   "text": "{\\an2\\pos(%d,%d)}%s"
                           % (video_w // 2, chunk["y"], " ".join(parts))})
    return ev


ASS_HEADER = u"""[Script Info]
; sinh boi nns-auto-sub
ScriptType: v4.00+
PlayResX: %(w)d
PlayResY: %(h)d
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: None

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,%(family)s,%(size)d,%(base)s,%(base)s,%(outline_c)s,%(shadow_c)s,%(bold)d,0,0,0,100,100,%(spacing).1f,0,1,%(outline).1f,%(shadow).1f,2,%(margin)d,%(margin)d,%(margin)d,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Text
"""


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--resources")
    ap.add_argument("--font", help="chi dinh thang 1 file .ttf/.otf")
    ap.add_argument("--max-words", type=int, default=4)
    ap.add_argument("--max-chars", type=int, default=22)
    ap.add_argument("--gap", type=float, default=0.35,
                    help="khoang nghi (giay) thi tach cum")
    ap.add_argument("--y", type=int, default=None,
                    help="vi tri DAY cua khoi chu, tinh bang pixel (mac dinh 0.80*cao)")
    ap.add_argument("--safe", default=None,
                    help='doi cho theo doan: "0-12:1100,12-30:1536"')
    ap.add_argument("--font-size", type=int, default=None,
                    help="mac dinh = cao_video/24")
    ap.add_argument("--outline", type=float, default=None,
                    help="do day vien, mac dinh = 0.09*co chu")
    ap.add_argument("--shadow", type=float, default=0.0)
    ap.add_argument("--spacing", type=float, default=0.0)
    ap.add_argument("--margin", type=int, default=None,
                    help="le trai/phai, mac dinh 0.06*rong")
    ap.add_argument("--base-color", default="#FFFFFF")
    ap.add_argument("--active-color", default="#FFD600")
    ap.add_argument("--outline-color", default="#000000")
    ap.add_argument("--no-break-punct", action="store_true",
                    help="khong tach cum o dau cau / dau phay")
    ap.add_argument("--no-measure", action="store_true",
                    help="bo buoc do be rong chu bang libass (nhanh hon, kem chac)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    C.require_video_out(a, "build_ass.py")

    info = C.probe_video(a.video)
    W, H = info["width"], info["height"]

    src = C.side_path(a.out, ".fixed.json")
    if not os.path.isfile(src):
        alt = C.side_path(a.out, ".words.json")
        if os.path.isfile(alt):
            src = alt
        else:
            C.die("chua co transcript. Chay 2 buoc truoc:\n"
                  '      python scripts/transcribe.py --video "%s" --out "%s"\n'
                  '      python scripts/fix_tokens.py --video "%s" --out "%s"'
                  % (a.video, a.out, a.video, a.out))
    data = C.read_json(src)
    words = [w for w in data["words"] if w.get("w")]
    if not words:
        C.die("transcript khong co tu nao: %s" % src)

    font = C.resolve_font(a.resources, a.font)
    if not font["file"]:
        C.die("khong co font tieng Viet dung duoc.\n"
              '  Chay:  python scripts/preflight.py --video "%s"%s\n'
              "  roi lam theo huong dan no in ra."
              % (a.video, ' --resources "%s"' % a.resources if a.resources else ""))
    if font.get("resources_unused"):
        # KHONG lang le doi sang font kem san khi nguoi dung da chi --resources
        C.die("thu muc --resources ban dua khong co font tieng Viet nao dung duoc.\n"
              + "\n".join("  " + ln
                          for ln in C.huong_dan_font_resources(font)))

    size = a.font_size or max(24, int(round(H / 24.0)))
    outline = a.outline if a.outline is not None else max(3.0, round(size * 0.09, 1))
    margin = a.margin if a.margin is not None else int(round(W * 0.06))
    y_def = a.y if a.y is not None else int(round(H * 0.80))
    if not (0 <= y_def <= H):
        C.die("--y %d nam ngoai khung cao %d px" % (y_def, H))
    base_c = to_ass_color(a.base_color, "--base-color")
    act_c = to_ass_color(a.active_color, "--active-color")
    out_c = to_ass_color(a.outline_color, "--outline-color")

    layout = Layout(parse_safe(a.safe, H), y_def)
    px_budget = W - 2 * margin

    print("")
    print("  " + C.hr("-"))
    print("  BUOC 3/4 — gom cum va xuat file .ass")
    print("  " + C.hr("-"))
    print("  video     : %dx%d %.4gfps %.2fs" % (W, H, info["fps"], info["duration"]))
    print("  transcript: %s (%d tu)" % (os.path.basename(src), len(words)))
    print("  font      : %s" % font["file"])
    print('  ten ho ASS: "%s"  (Bold=%d, co chu %d px, vien %.1f px)'
          % (font["family"], font["bold"], size, outline))
    print("  mau       : thuong %s / dang doc %s / vien %s"
          % (base_c, act_c, out_c))
    print("  cho dat   : y=%d px (day khoi chu), le %d px, be rong dung duoc %d px"
          % (y_def, margin, px_budget))
    if layout.safe:
        for s0, s1, yy in layout.safe:
            print("              vung an toan %.2fs-%.2fs -> y=%d" % (s0, s1, yy))
    else:
        print("              (khong dat --safe: dung 1 cho cho ca video)")

    char_px = None
    if not a.no_measure:
        char_px, calib = calibrate_char_px(font["file"], font["family"],
                                          font["bold"], size)
        print("  do that    : chuoi mau %d ky tu rong %d px -> %.1f px/ky tu"
              % (len(CALIB_TEXT), calib["w"], char_px))

    chunks = chunk_words(words, layout, a.max_words, a.max_chars, a.gap,
                         px_budget, char_px, not a.no_break_punct)

    # do THAT be rong 3 cum dai nhat -> khong tin uoc luong
    widest = sorted(chunks, key=lambda c: -len(" ".join(w["w"] for w in c["words"])))[:3]
    over = []
    if not a.no_measure:
        print("")
        print("  do be rong THAT cua 3 cum dai nhat:")
        for c in widest:
            txt = " ".join(w["w"] for w in c["words"])
            px = measure_text_px(txt, font["file"], font["family"],
                                 font["bold"], size)
            flag = "OK" if px <= px_budget else "TRAN LE"
            if px > px_budget:
                over.append((txt, px))
            print('      "%s"  = %d px  (%s)' % (txt, px, flag))

    events = []
    for c in chunks:
        events.extend(karaoke_events(c, base_c, act_c, W))

    print("")
    print("  ket qua: %d cum, %d dong Dialogue (1 dong / 1 tu dang doc)"
          % (len(chunks), len(events)))
    clamped = [c for c in chunks if c["clamped_to_boundary"]]
    if clamped:
        print("  co %d cum bi cat ngan tai ranh vung an toan (dung y cu de len mat):"
              % len(clamped))
        for c in clamped[:5]:
            print("      [%6.2f-%6.2f] y=%d  %s"
                  % (c["start"], c["end"], c["y"],
                     " ".join(w["w"] for w in c["words"])))
    snapped = [c for c in chunks if c["snapped_to_next_zone"]]
    if snapped:
        print("  co %d cum qua ngan o cuoi vung nen duoc doi sang y cua vung sau:"
              % len(snapped))
        for c in snapped[:5]:
            print("      [%6.2f-%6.2f] y=%d  %s"
                  % (c["start"], c["end"], c["y"],
                     " ".join(w["w"] for w in c["words"])))
    print("")
    print("  10 cum dau:")
    for c in chunks[:10]:
        print("      [%6.2f-%6.2f] y=%-5d %-26s  (tach vi: %s)"
              % (c["start"], c["end"], c["y"],
                 " ".join(w["w"] for w in c["words"]), c["break_reason"]))

    if over:
        C.die("co %d cum ve ra rong hon vung dung duoc (%d px).\n"
              "  Giam bot bang 1 trong cac cach:\n"
              "      --max-chars %d      (dang %d)\n"
              "      --max-words %d      (dang %d)\n"
              "      --font-size %d      (dang %d)\n"
              % (len(over), px_budget, max(8, a.max_chars - 4), a.max_chars,
                 max(2, a.max_words - 1), a.max_words, int(size * 0.85), size))

    ass_path = C.side_path(a.out, ".ass")
    plan_path = C.side_path(a.out, ".plan.json")
    if a.dry_run:
        print("")
        print("  [dry-run] khong ghi file. Se ghi:")
        print("      %s" % ass_path)
        print("      %s" % plan_path)
        return

    body = [ASS_HEADER % {"w": W, "h": H, "family": font["family"],
                          "size": size, "base": base_c, "outline_c": out_c,
                          "shadow_c": out_c, "bold": font["bold"],
                          "outline": outline, "shadow": a.shadow,
                          "spacing": a.spacing, "margin": margin}]
    for e in events:
        body.append("Dialogue: 0,%s,%s,Sub,,0,0,0,%s\n"
                    % (C.ass_time(e["start"]), C.ass_time(e["end"]), e["text"]))
    C.write_text(ass_path, "".join(body))

    C.write_json(plan_path, {
        "video": os.path.abspath(a.video), "out": os.path.abspath(a.out),
        "ass": os.path.abspath(ass_path),
        "video_w": W, "video_h": H, "fps": info["fps"],
        "nb_frames": info["nb_frames"],
        "font_file": font["file"], "font_dir": font["dir"],
        "font_family": font["family"], "font_bold": font["bold"],
        "font_size": size, "outline": outline, "margin": margin,
        "default_y": y_def, "safe": layout.safe,
        "base_color": base_c, "active_color": act_c,
        "chunks": chunks, "n_events": len(events)})
    print("")
    print("  da ghi: %s" % ass_path)
    print("  da ghi: %s" % plan_path)


if __name__ == "__main__":
    C.run_main(main)
