# -*- coding: utf-8 -*-
"""BUOC 6a — de xuat cue sheet SFX + CHO DAT the chu, doc tu transcript that.

    python scripts/plan_cues.py --words <x.sub.fixed.json> --layout <x.layout.json> \
        --out-cues <x.cues.json> --out-cards <x.cards.json>

Khong bia. Moi cue deu neo vao mot thu DO DUOC: cat canh that, dau cau, hoac
dau tu. Mat do mac dinh la HOOK-WEIGHTED:

    hook (20s dau)  ~0.60 cue/giay   <- day
    phan giai thich ~0.12 cue/giay   <- thua han, VA chi danh vao cat canh that

Video ngan hon ~30s thi coi ca video la hook va rai deu.

Moi cue NGOAI hook deu duoc danh dau `"optional": true` thanh MOT KHOI, de bo
het bang mot tham so (`--drop-optional` cua build_sfx) ma khong phai render lai
hinh — lop SFX la buoc audio rieng.

THE CHU: script nay chi de xuat CHO DAT (start/end/y/style) + doan loi dang noi
o do, va de `"text": ""` cho nguoi viet. Ly do: luat cung cua the chu la "noi
thu ma man hinh va sub CHUA noi" — may khong tu biet duoc dieu do, con
check_cards.py thi kiem duoc (khong lap nguyen van loi thoai, khong in lai con
so dang hien).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()

SHORT_VIDEO = 30.0        # duoi muc nay: ca video la hook, rai deu
HOOK_LEN = 20.0
HOOK_DENSITY = 0.60       # cue/giay trong hook
TAIL_DENSITY = 0.12       # cue/giay ngoai hook
MIN_GAP = 0.45            # hai cue gan nhau nhat bao nhieu giay
CARD_EVERY = 12.0         # nhieu nhat 1 the / 12 giay
CARD_MAX_DUR = 2.5


def load_words(path):
    d = C.read_json(path)
    if isinstance(d, dict):
        d = d.get("words") or d.get("tokens") or []
    out = []
    for w in d:
        t = w.get("w") if "w" in w else w.get("word", "")
        s, e = w.get("start"), w.get("end")
        if s is None or e is None:
            continue
        out.append({"w": (t or "").strip(), "start": float(s), "end": float(e)})
    return out


def sentence_starts(words):
    """Dau cau. Bien cau la bien MO: tu dau tien SAU dau cham la mot cau moi."""
    st = []
    for i, w in enumerate(words):
        if i == 0:
            st.append(w["start"])
        elif re.search(r"[.!?]$", words[i - 1]["w"]):
            st.append(w["start"])
    return st


def candidates(words, cuts, t0, t1):
    """Moc co the dat cue, kem do uu tien. 3 = cat canh that (manh nhat)."""
    out = []
    for t in cuts:
        if t0 <= t < t1:
            out.append((3, round(t, 3), "cat canh"))
    for t in sentence_starts(words):
        if t0 <= t < t1:
            out.append((2, round(t, 3), "dau cau"))
    for w in words:
        if t0 <= w["start"] < t1 and len(w["w"]) >= 4:
            out.append((1, round(w["start"], 3), "dau tu '%s'" % w["w"]))
    return out


def thin(cands, n, gap, t0, t1):
    """Chon toi da n moc: uu tien cao truoc, va khong dinh nhau qua gan."""
    picked = []

    def ok(t):
        return all(abs(t - p[0]) >= gap for p in picked)

    for prio in (3, 2, 1):
        for _p, t, why in sorted([c for c in cands if c[0] == prio],
                                 key=lambda c: c[1]):
            if len(picked) >= n:
                break
            if ok(t):
                picked.append((t, why))
        if len(picked) >= n:
            break
    if len(picked) < n and t1 - t0 > gap:
        k = int((t1 - t0) / gap)
        for i in range(k):
            t = round(t0 + (i + 0.5) * (t1 - t0) / max(1, k), 3)
            if len(picked) >= n:
                break
            if ok(t):
                picked.append((t, "rai deu"))
    picked.sort()
    return picked


ROLE_CYCLE = ["impact", "transition", "accent", "accent", "transition", "confirm"]


def pick_files(lib_dir, files):
    """Chia thu vien theo vai, uu tien ten dung y nhat trong tung vai."""
    F.add_sfx_path()
    import _common as S
    by = {}
    for p in files:
        role = S.role_of(os.path.basename(p))
        by.setdefault(role, []).append(p)
    for role in by:
        by[role].sort(key=lambda p: (S.prefer_rank(role, p), os.path.basename(p)))
    return by, S


def cue_for(role, by, S, ana, want_t, align_peak=False):
    """Dung 1 cue: chon file, do onset/climax that, tinh gain ve muc dinh cua vai."""
    pool = by.get(role) or by.get("other") or []
    if not pool:
        for alt in ("accent", "transition", "impact", "confirm", "bed"):
            if by.get(alt):
                pool = by[alt]
                role = alt
                break
    if not pool:
        return None
    path = pool[0]
    name = os.path.basename(path)
    a = ana.get(name)
    if a is None:
        a = S.analyse_sfx(path)
        ana[name] = a
    if not a.get("usable", True):
        return None
    onset = float(a.get("onset", 0.0))
    seg_pk = float(a.get("seg_peak_dbfs", a.get("peak_dbfs", -12.0)))
    target = S.ROLE_TARGET_PEAK.get(role, -21.0)
    gain = round(target - seg_pk, 1)
    maxdur = S.ROLE_MAX_DUR.get(role, 1.2)

    off, dur, t = onset, None, want_t
    if align_peak:
        # File co dinh o GIUA (riser, whoosh dai): lay DOAN GIUA sao cho dinh
        # roi dung moc. lead = doan truoc dinh, tail = doan sau dinh.
        climax = float(a.get("climax", onset))
        lead = min(maxdur * 0.8, max(0.25, climax - onset))
        tail = min(maxdur * 0.2, max(0.08, float(a.get("dur", 1.0)) - climax))
        off = max(0.0, climax - lead)
        dur = round(lead + tail, 3)
        t = round(max(0.0, want_t - lead), 3)
    else:
        dur = round(min(maxdur, max(0.12, float(a.get("burst_end", maxdur)) - onset)), 3)
    return {"t": round(t, 3), "file": name, "gain_db": gain,
            "off": round(off, 3), "dur": dur, "fin": 0.0, "fout": 0.03,
            "role": role}


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(description="De xuat cue SFX + cho dat the chu")
    ap.add_argument("--words", help="<out>.sub.fixed.json (hoac .words.json)")
    ap.add_argument("--layout", help="<out>.layout.json tu buoc 2")
    ap.add_argument("--out-cues", dest="out_cues")
    ap.add_argument("--out-cards", dest="out_cards")
    ap.add_argument("--resources")
    ap.add_argument("--hook-len", dest="hook_len", type=float, default=HOOK_LEN)
    ap.add_argument("--density", type=float, default=HOOK_DENSITY,
                    help="cue/giay TRONG hook (mac dinh 0.60)")
    ap.add_argument("--tail-density", dest="tail_density", type=float,
                    default=TAIL_DENSITY, help="cue/giay ngoai hook (mac dinh 0.12)")
    ap.add_argument("--min-gap", dest="min_gap", type=float, default=MIN_GAP)
    ap.add_argument("--risers", type=int, default=1)
    ap.add_argument("--card-every", dest="card_every", type=float, default=CARD_EVERY)
    ap.add_argument("--no-cards", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.words or not a.layout:
        C.die("thieu tham so.\n"
              "    python scripts/plan_cues.py --words <x.sub.fixed.json> "
              "--layout <x.layout.json> --out-cues <x.cues.json> "
              "--out-cards <x.cards.json>")
    for p in (a.words, a.layout):
        if not os.path.isfile(p):
            C.die("khong thay file: %s" % p)

    lay = C.read_json(a.layout)
    words = load_words(a.words)
    if not words:
        C.die("transcript rong: %s" % a.words)
    dur = float(lay.get("dur") or words[-1]["end"])
    cuts = list(lay.get("cuts") or [])

    F.add_sfx_path()
    import _common as S
    lib_dir, files, src, _n = S.find_sfx_library(a.resources)
    if not lib_dir or not files:
        C.die("khong tim thay thu vien SFX. Chay preflight de xem huong dan.")
    by, S = pick_files(lib_dir, files)
    ana = {}

    short = dur <= SHORT_VIDEO
    hook_end = dur if short else min(a.hook_len, dur)

    F.banner("BUOC 6a — DE XUAT CUE SFX (hook-weighted)",
             ["transcript : %s (%d tu)" % (os.path.basename(a.words), len(words)),
              "thoi luong : %.2fs" % dur,
              "thu vien   : %d file — %s" % (len(files), lib_dir),
              "hook       : 0..%.2fs%s" % (hook_end,
                                           "  (video ngan -> ca video la hook, rai deu)"
                                           if short else ""),
              "mat do     : hook %.2f cue/s | ngoai hook %.2f cue/s"
              % (a.density, 0.0 if short else a.tail_density)])

    # ---------------- hook
    n_hook = max(1, int(round(a.density * hook_end)))
    hook_pts = thin(candidates(words, cuts, 0.0, hook_end), n_hook, a.min_gap,
                    0.0, hook_end)

    cues = []
    for i, (t, why) in enumerate(hook_pts):
        role = "impact" if i == 0 else ROLE_CYCLE[i % len(ROLE_CYCLE)]
        c = cue_for(role, by, S, ana, t)
        if not c:
            continue
        c["why"] = why
        c["optional"] = False
        cues.append(c)

    # riser: phai co DINH roi dung mot cat canh manh trong hook
    riser_at = [t for t in cuts if 1.0 < t <= hook_end]
    for k in range(min(a.risers, len(riser_at))):
        t = riser_at[len(riser_at) - 1 - k]
        c = cue_for("riser", by, S, ana, t, align_peak=True)
        if c:
            c["why"] = "riser leo len, DINH roi dung cat canh %.2fs" % t
            c["optional"] = False
            cues.append(c)

    # ---------------- ngoai hook: CHI cat canh that, va deu la optional
    tail = []
    if not short and dur > hook_end:
        n_tail = max(0, int(round(a.tail_density * (dur - hook_end))))
        tail_cands = [(3, t, "cat canh") for t in cuts if hook_end <= t < dur]
        pts = thin(tail_cands, n_tail, max(a.min_gap, 1.5), hook_end, dur)
        pts = [p for p in pts if p[1] == "cat canh"]     # ngoai hook: khong rai deu
        for i, (t, why) in enumerate(pts):
            c = cue_for("transition" if i % 2 == 0 else "accent", by, S, ana, t)
            if not c:
                continue
            c["why"] = why
            c["optional"] = True
            tail.append(c)
    cues.extend(tail)
    cues.sort(key=lambda c: c["t"])

    print("")
    print("  CUE SHEET — %d cue (%d trong hook, %d ngoai hook / tuy chon)"
          % (len(cues), len(cues) - len(tail), len(tail)))
    print("  " + F.hr("-"))
    print("  %-8s %-11s %-24s %7s %7s %7s  %s"
          % ("t", "vai", "file", "gain", "off", "dur", "vi sao"))
    print("  " + F.hr("-"))
    for c in cues:
        print("  %-8.2f %-11s %-24s %+6.1f %7.3f %7.3f  %s%s"
              % (c["t"], c["role"], c["file"][:24], c["gain_db"], c["off"],
                 c["dur"], c["why"], "  [tuy chon]" if c["optional"] else ""))
    print("  " + F.hr("-"))
    if tail:
        print("  %d cue ngoai hook deu co optional=true — bo het bang mot tham so:"
              % len(tail))
        print("      python scripts/build_sfx.py ... --drop-optional")
        print("      (lop SFX la buoc AUDIO rieng, bo di KHONG phai render lai hinh)")

    # ---------------- cho dat the chu
    cards = []
    if not a.no_cards:
        segs = lay.get("segments") or []

        def card_y_at(t):
            for s in segs:
                if s["start"] <= t < s["end"]:
                    return int(s.get("card_y") or s["y"])
            return int(segs[0]["card_y"]) if segs else int(lay["h"] * 0.35)

        st = sentence_starts(words)
        last = -1e9
        for t in st:
            if t - last < a.card_every or t > dur - 1.0:
                continue
            nxt = min([x for x in st if x > t] or [dur])
            end = round(min(t + CARD_MAX_DUR, nxt - 0.15, dur - 0.1), 3)
            if end - t < 0.6:
                continue
            spoken = " ".join(w["w"] for w in words
                              if t - 0.2 <= w["start"] <= end + 1.5)
            cards.append({"start": round(t, 3), "end": end,
                          "y": card_y_at(t), "style": "punch",
                          "plate": False, "text": "",
                          "dang_noi": spoken[:110]})
            last = t

        print("")
        print("  CHO DAT THE CHU — %d cho (toi da 1 the / %.0f giay)"
              % (len(cards), a.card_every))
        print("  " + F.hr("-"))
        for i, c in enumerate(cards, 1):
            print("  %2d. %6.2f-%6.2f  y=%4d  dang noi: \"%s\""
                  % (i, c["start"], c["end"], c["y"], c["dang_noi"]))
        print("  " + F.hr("-"))
        print("  Dien \"text\" cho tung the: TOI DA 4 chu, va phai noi thu ma sub")
        print("  KHONG noi. Khong chep lai loi thoai, khong in lai con so dang hien.")
        print("  check_cards.py se chan neu vi pham — no doi chieu voi transcript.")
        print("  The nao khong dung thi XOA khoi file, khong de text rong.")

    if a.dry_run:
        print("")
        print("  [dry-run] khong ghi file nao.")
        return

    if a.out_cues:
        C.write_json(a.out_cues, cues)
        print("")
        print("  da ghi: %s" % os.path.abspath(a.out_cues))
    if a.out_cards and not a.no_cards:
        C.write_json(a.out_cards, cards)
        print("  da ghi: %s" % os.path.abspath(a.out_cards))
    print("")


if __name__ == "__main__":
    C.run_main(main)
