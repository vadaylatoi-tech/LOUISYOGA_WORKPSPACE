# -*- coding: utf-8 -*-
"""BUOC 10 — do lai TAT CA. Chua exit 0 thi chua duoc bao "xong".

    python scripts/verify_all.py --src <x.cut.mp4> --out <final.mp4> \
        --plan <x.sub.plan.json> --cards <x.cards.json> --cues <x.cues.json> \
        --ab <final.ab.json> --font <font.ttf>

6 phep do:
  1. so frame ra khop ke hoach, fps va kich thuoc khong doi
  2. do dai tieng == do dai hinh, lech <= 1 frame
  3. sub co that su hien: do pixel doi trong dai chu
  4. the chu co that su hien, va khong co gi ve ra ngoai dai the + dai sub
     (dai the tinh tu so do THAT: auto-fit, so dong, padding+vien+bong cua khung)
  5. SFX vao dung cho: render 2 lan cung chuoi filter — mot lan lop SFX that,
     mot lan lop SFX im lang — roi tru. KHONG dung final - source*gain.
  6. loudness do tren chinh file mp4 cuoi, va 0 mau vuot 1.0
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()

SUB_BAND_ABOVE = 150     # dai sub: tu y-150 den y+30 (giong verify cua auto-sub)
SUB_BAND_BELOW = 30
DIFF_THR = 24            # muc chenh gray coi la "co ve gi do"
MIN_PX = 600             # so pixel doi toi thieu de coi la "co hien"
OUTSIDE_MAX = 0.10       # toi da 10% pixel doi duoc phep nam ngoai cac dai


class Res(object):
    def __init__(self):
        self.rows = []

    def add(self, ok, name, detail):
        self.rows.append((bool(ok), name, detail))
        print("    [%s] %-34s %s" % ("DAT" if ok else "SAI", name, detail))
        return ok

    def failed(self):
        return [r for r in self.rows if not r[0]]


def gray(video, idx, w, h):
    import numpy as np
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", video,
         "-vf", "select=eq(n\\,%d)" % idx, "-vsync", "0", "-frames:v", "1",
         "-pix_fmt", "gray", "-f", "rawvideo", "-"], capture_output=True)
    if len(p.stdout) < w * h:
        return None
    return np.frombuffer(p.stdout[:w * h], dtype=np.uint8).reshape(h, w).astype(np.int16)


def card_band(card, font, w, h):
    """Dai pixel THAT cua mot the — tinh tu chinh bo dung the, khong uoc."""
    F.add_tools_path()
    import cards_to_ass as K
    from PIL import ImageFont
    size = K.CARD_STYLES.get(card.get("style") or "punch",
                             K.CARD_STYLES["punch"])["size"]
    size, text = K.fit(font, size, card["text"], w - 120)
    f = ImageFont.truetype(font, size)
    asc, desc = f.getmetrics()
    lines = len(text.split("\\N"))
    th = (asc + desc) * lines
    y1 = int(card["y"]) + 24
    y0 = y1 - th - 20
    if card.get("plate"):
        pw, ph, px, py = K.plate_box(font, size, text, w // 2, int(card["y"]))
        y0 = min(y0, py - 4)
        y1 = max(y1, py + ph + K.PLATE["shadow_dy"] + 4)
    return max(0, y0), min(h, y1 + K.RISE_PX)


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(description="Do lai tat ca sau khi render")
    ap.add_argument("--src", help="video TRUOC khi ve chu (thuong la x.cut.mp4)")
    ap.add_argument("--out", help="video KET QUA cuoi cung")
    ap.add_argument("--plan", help="x.sub.plan.json")
    ap.add_argument("--cards", help="x.cards.json")
    ap.add_argument("--cues", help="x.cues.json")
    ap.add_argument("--ab", help="final.ab.json do master.py ghi")
    ap.add_argument("--font")
    ap.add_argument("--resources")
    ap.add_argument("--target", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-2.0)
    ap.add_argument("--tol", type=float, default=0.5)
    ap.add_argument("--samples", type=int, default=4, help="so moc do sub")
    ap.add_argument("--skip-sfx", action="store_true",
                    help="bo phep do 5 (chi khi CO Y khong chen SFX)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.src or not a.out:
        C.die("thieu tham so.\n"
              "    python scripts/verify_all.py --src <x.cut.mp4> --out <final.mp4> "
              "--plan <x.sub.plan.json> --cards <x.cards.json>")
    for p in (a.src, a.out):
        if not os.path.isfile(p):
            C.die("khong thay file: %s" % p)
    np = C.import_numpy()

    F.banner("BUOC 10 — VERIFY (khong dat thi khong duoc bao xong)",
             ["vao : %s" % a.src, "ra  : %s" % a.out])

    if a.dry_run:
        print("")
        print("  [dry-run] se do 6 thu: frame/fps/kich thuoc, dong bo tieng-hinh,")
        print("            sub hien, the chu hien + khong tran, SFX dung cho, loudness.")
        print("")
        return

    r = Res()
    si = C.probe_video(a.src)
    oi = C.probe_video(a.out)

    # ---------------- 1. frame / fps / kich thuoc
    print("")
    print("  1) SO FRAME, FPS, KICH THUOC")
    n_src = C.count_frames(a.src)
    n_out = C.count_frames(a.out)
    r.add(n_src == n_out, "so frame khop ke hoach",
          "vao %d frame, ra %d frame" % (n_src, n_out))
    r.add(abs(si["fps"] - oi["fps"]) < 0.01, "fps khong doi",
          "%.4g -> %.4g" % (si["fps"], oi["fps"]))
    r.add(si["width"] == oi["width"] and si["height"] == oi["height"],
          "kich thuoc khong doi",
          "%dx%d -> %dx%d" % (si["width"], si["height"], oi["width"], oi["height"]))

    # ---------------- 2. tieng vs hinh
    print("")
    print("  2) DO DAI TIENG == DO DAI HINH")
    # PHAI dem mau da GIAI MA, khong duoc tin metadata cua ffprobe.
    # Da tra gia: `loudnorm` xu ly theo khoi 100 ms va nem di khoi cuoi chua du,
    # lam mat 72 ms tieng o duoi — nhung metadata van bao 14.599/14.600s nen
    # phep do nay BAO DAT trong khi file that su bi cut duoi.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import master as _M
    n_samp = len(_M.decode_f32(a.out))
    ad = n_samp / float(_M.SR)
    ad_meta = C.audio_duration(a.out)
    vd = n_out / float(oi["fps"] or 30.0)
    one = 1.0 / (oi["fps"] or 30.0)
    r.add(abs(ad - vd) <= one + 1e-6, "lech <= 1 frame",
          "tieng %.4fs (%d mau GIAI MA THAT; metadata bao %.4fs), hinh %.4fs, "
          "lech %.4fs (1 frame = %.4fs)"
          % (ad, n_samp, ad_meta, vd, abs(ad - vd), one))

    W, H = oi["width"], oi["height"]
    font = a.font
    plan = C.read_json(a.plan) if a.plan and os.path.isfile(a.plan) else {}
    if not font:
        font = plan.get("font_file")
    if not font or not os.path.isfile(font):
        res = C.resolve_font(a.resources, None, verbose=False)
        font = res.get("file")

    # ---------------- 3. sub co hien
    print("")
    print("  3) SUB CO THAT SU HIEN (do pixel trong dai chu)")
    chunks = plan.get("chunks") or []
    diffs = {}
    if not chunks:
        r.add(False, "co ke hoach sub de do", "thieu --plan / khong co chunks")
    else:
        pick = [chunks[0], chunks[-1]]
        for k in range(1, max(1, a.samples - 1)):
            pick.append(chunks[min(len(chunks) - 1,
                                   int(len(chunks) * k / float(a.samples)))])
        seen = set()
        for ch in pick:
            t = (ch["start"] + ch["end"]) / 2.0
            idx = int(round(t * oi["fps"]))
            if idx in seen:
                continue
            seen.add(idx)
            A = gray(a.src, idx, W, H)
            B = gray(a.out, idx, W, H)
            if A is None or B is None:
                r.add(False, "doc duoc frame %d" % idx, "ffmpeg khong tra du pixel")
                continue
            d = np.abs(A - B) > DIFF_THR
            diffs[idx] = d
            y0 = max(0, int(ch["y"]) - SUB_BAND_ABOVE)
            y1 = min(H, int(ch["y"]) + SUB_BAND_BELOW)
            px = int(d[y0:y1].sum())
            frac = 100.0 * px / max(1, (y1 - y0) * W)
            r.add(px > MIN_PX, "sub hien o frame %d (t=%.2f)" % (idx, t),
                  "%d px doi trong dai y%d..%d (%.2f%% dai)" % (px, y0, y1, frac))

    # ---------------- 4. the chu
    print("")
    print("  4) THE CHU HIEN, VA KHONG CO GI VE RA NGOAI DAI")
    cards = []
    if a.cards and os.path.isfile(a.cards):
        cards = C.read_json(a.cards)
        if isinstance(cards, dict):
            cards = cards.get("text_cards") or cards.get("cards") or []
        cards = [c for c in cards if (c.get("text") or "").strip()]
    if not cards:
        print("    (khong co the chu — bo qua phep do nay)")
    elif not font:
        r.add(False, "co font de tinh dai the", "khong tim ra font da burn")
    else:
        for i, c in enumerate(cards, 1):
            t = (float(c["start"]) + float(c["end"])) / 2.0
            idx = int(round(t * oi["fps"]))
            A = gray(a.src, idx, W, H)
            B = gray(a.out, idx, W, H)
            if A is None or B is None:
                r.add(False, "doc duoc frame the %d" % i, "ffmpeg khong tra du pixel")
                continue
            d = np.abs(A - B) > DIFF_THR
            y0, y1 = card_band(c, font, W, H)
            px = int(d[y0:y1].sum())
            tot = int(d.sum())
            inside = px
            ys = None
            for ch in chunks:
                if ch["start"] <= t <= ch["end"]:
                    ys = (max(0, int(ch["y"]) - SUB_BAND_ABOVE),
                          min(H, int(ch["y"]) + SUB_BAND_BELOW))
                    break
            if ys:
                lo, hi = ys
                if hi <= y0 or lo >= y1:
                    inside += int(d[lo:hi].sum())
                else:
                    lo2, hi2 = min(lo, y0), max(hi, y1)
                    inside = int(d[lo2:hi2].sum())
            outside = 1.0 - (inside / float(tot)) if tot else 0.0
            ok = px > MIN_PX and outside <= OUTSIDE_MAX
            r.add(ok, "the %d \"%s\"" % (i, (c["text"] or "")[:18]),
                  "%d px trong dai the y%d..%d, %.1f%% pixel doi nam NGOAI dai"
                  % (px, y0, y1, outside * 100))

    # ---------------- 5. SFX
    print("")
    print("  5) SFX VAO DUNG CHO (2 ban mix: co SFX / SFX im lang, roi tru)")
    if a.skip_sfx:
        print("    (bo qua theo --skip-sfx)")
    elif not a.ab or not os.path.isfile(a.ab):
        r.add(False, "co ho so A/B cua master", "thieu --ab <final.ab.json>")
    elif not a.cues or not os.path.isfile(a.cues):
        r.add(False, "co cue sheet de doi chieu", "thieu --cues")
    else:
        ab = C.read_json(a.ab)
        tool = F.require("verify_sfx_ab", kind="tool")
        work = tempfile.mkdtemp(prefix="fpab_")
        cues = C.read_json(a.cues)
        if isinstance(cues, dict):
            cues = cues.get("sfx") or cues.get("cues") or []
        cue_file = os.path.join(work, "cues.json")
        C.write_json(cue_file, cues)
        miss = [p for p in (ab.get("voice_raw"), ab.get("bed_raw"))
                if not p or not os.path.isfile(p)]
        if miss:
            r.add(False, "con file raw cua master de dung lai ban A/B",
                  "thieu %s — dung master.py voi --work de giu lai" % ", ".join(miss))
        else:
            sys.stdout.flush()
            rc = subprocess.call(F.py(tool, [
                "--voice", ab["voice_raw"], "--bed", ab["bed_raw"],
                "--cues", cue_file, "--chain", ab["chain"], "--workdir", work]))
            r.add(rc == 0, "moi cue nghe thay va khong lech",
                  "verify_sfx_ab.py exit %d" % rc)

    # ---------------- 6. loudness tren file mp4 cuoi
    print("")
    print("  6) LOUDNESS DO TREN CHINH FILE MP4 CUOI")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import master as M
    fin = M.measure_loudness(a.out)
    x = M.decode_f32(a.out)
    peak = float(np.abs(x).max())
    over = int((np.abs(x) > 1.0).sum())
    r.add(abs(fin["I"] - a.target) <= a.tol, "do to I",
          "%.2f LUFS (muc tieu %.1f +-%.1f)" % (fin["I"], a.target, a.tol))
    r.add(fin["TP"] <= a.tp + 1e-6, "true peak",
          "%.2f dBFS (tran %.1f)" % (fin["TP"], a.tp))
    r.add(over == 0, "khong mau nao vuot 1.0",
          "dinh mau THAT sau giai ma = %.6f, so mau vuot = %d" % (peak, over))

    bad = r.failed()
    print("")
    print("  " + F.hr())
    if bad:
        print("  KHONG DAT — %d/%d phep do that bai:" % (len(bad), len(r.rows)))
        for _ok, name, detail in bad:
            print("      - %s: %s" % (name, detail))
        print("  " + F.hr())
        print("  KHONG duoc bao voi nguoi dung la xong.")
        print("")
        sys.exit(1)
    print("  DAT CA %d PHEP DO. File nay dang duoc." % len(r.rows))
    print("  " + F.hr())
    print("      %s" % os.path.abspath(a.out))
    print("")


if __name__ == "__main__":
    C.run_main(main)
