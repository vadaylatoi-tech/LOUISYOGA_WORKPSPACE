# -*- coding: utf-8 -*-
"""plan.py - chon cac doan PUNCH-IN, va bao SAFE ZONE do duoc.

HAI che do:

A) LAP KE HOACH PUNCH-IN (mac dinh) - chon moc, tinh zoom + tam, ghi plan.json
   Chon moc bang 1 trong 3 cach:
       --at "12.5,40,73.2"     moc chi dinh tay
       --from-transcript t.json bam vao cac tu NHAN MANH trong transcript
       --every 20              cu N giay 1 lan (nhip mac dinh, don gian nhat)

B) BAO SAFE ZONE (--report-safe-zones) - xuat hop mat DO DUOC theo tung khoang
   thoi gian, de skill khac dat overlay MA KHONG DE LEN MAT.
   Doc references/safe-zone-do-that.md truoc khi dung so nay.

Moi punch co: ramp-in (0.5s) -> hold (1.5s) -> ramp-out (0.5s), zoom 1.12.
Zoom LUON bi ha xuong neu can, de hop mat nam TRON trong khung sau khi crop.
KHONG BAO GIO cat vao mat.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facelib as F  # noqa: E402

DEFAULT_WORDS = os.path.join(F.SKILL_DIR, "assets", "emphasis_words_vi.txt")


# ------------------------------------------------------------------ transcript
def load_words(path):
    """Doc transcript ra danh sach tu [{start,end,text}].

    Nhan nhieu dang: {"words":[..]}, {"segments":[{...,"words":[..]}]},
    list o cap cao nhat, va segment KHONG co words (khi do lay ca segment lam
    1 'tu', moc = start cua segment).
    """
    data = F.read_json(path)
    if isinstance(data, dict):
        if data.get("words"):
            raw, level = data["words"], "words"
        elif data.get("segments"):
            raw, level = data["segments"], "segments"
        else:
            raise RuntimeError(
                "transcript khong co khoa 'words' hay 'segments': %s" % path)
    elif isinstance(data, list):
        raw, level = data, "list"
    else:
        raise RuntimeError("transcript khong phai JSON object/list: %s" % path)

    words = []
    if level == "segments":
        for seg in raw:
            if seg.get("words"):
                for w in seg["words"]:
                    words.append(_one_word(w))
            else:
                words.append(_one_word(seg))
    else:
        for w in raw:
            if isinstance(w, dict) and w.get("words"):
                for ww in w["words"]:
                    words.append(_one_word(ww))
            else:
                words.append(_one_word(w))
    words = [w for w in words if w and w["text"]]
    words.sort(key=lambda w: w["start"])
    if not words:
        raise RuntimeError("transcript doc duoc 0 tu: %s" % path)
    return words


def _one_word(w):
    if not isinstance(w, dict):
        return None
    txt = w.get("word", w.get("text", w.get("w", "")))
    st = w.get("start", w.get("s", w.get("t")))
    en = w.get("end", w.get("e"))
    if st is None:
        return None
    try:
        st = float(st)
        en = float(en) if en is not None else st + 0.3
    except (TypeError, ValueError):
        return None
    return {"start": st, "end": en, "text": (txt or "").strip()}


def score_words(words, phrases, pause_min):
    """Cham diem NHAN MANH cho tung tu.

    CAI BAY DA GAP: viet regex cho cum nhieu tu (vd "quan trong nhat") thi
    KHONG BAO GIO khop, vi transcript la mot chuoi TOKEN DON. Vi vay o day
    ghep 1..4 tu lien nhau thanh cum roi moi do khop - do la cach duy nhat
    bat duoc cum nhieu tu o muc tu.

    Diem cong:
      +2.0  khop tu/cum nhan manh
      +1.5  co khoang nghi >= pause_min ngay TRUOC tu (nghi roi noi = nhan manh)
      +1.0  co chu so (so lieu thuong la cho can nhin vao mat nguoi noi)
    """
    n = len(words)
    norm = [F.norm_vi(w["text"]) for w in words]
    maxlen = max((len(p.split()) for p in phrases), default=1)
    maxlen = min(4, max(1, maxlen))
    out = []
    for i, w in enumerate(words):
        score, why = 0.0, []
        for k in range(1, maxlen + 1):
            if i + k > n:
                break
            joined = " ".join(x for x in norm[i:i + k] if x).strip()
            if joined and joined in phrases:
                score += 2.0
                why.append("tu nhan manh '%s'" % joined)
                break
        if i > 0:
            gap = w["start"] - words[i - 1]["end"]
            if gap >= pause_min:
                score += 1.5
                why.append("nghi %.2fs truoc do" % gap)
        if any(c.isdigit() for c in norm[i]):
            score += 1.0
            why.append("co chu so")
        if score > 0:
            out.append({"t": w["start"], "score": round(score, 2),
                        "text": w["text"], "why": "; ".join(why)})
    out.sort(key=lambda d: (-d["score"], d["t"]))
    return out


# -------------------------------------------------------------------- an chon
def pick_anchors(cands, dur, span, min_gap, max_n):
    """Chon moc theo diem cao dan, bao dam 2 punch cach nhau >= min_gap giay
    va nam tron trong video."""
    chosen = []
    for c in cands:
        t = c["t"]
        if t - 0.0 < 0 or t + span > dur:
            continue
        if any(abs(t - o["t"]) < (span + min_gap) for o in chosen):
            continue
        chosen.append(c)
        if len(chosen) >= max_n:
            break
    chosen.sort(key=lambda d: d["t"])
    return chosen


# ------------------------------------------------------------------ safe zones
def safe_zones(track, zone_step, pad):
    """Hop mat DO DUOC theo tung khoang thoi gian + khoang trong con lai.

    CHI dung box_det. KHONG dung hop da lam min: trung vi cat mat dinh cuc tri,
    tuc no BAO NHO HON su that - dat overlay theo so nho hon = de len mat.
    """
    w, h = track["w"], track["h"]
    dur = track["dur"]
    rows, no_face = [], []
    t0 = 0.0
    while t0 < dur - 1e-6:
        t1 = min(dur, t0 + zone_step)
        got = F.measured_boxes_in(track, t0, t1)
        if not got:
            no_face.append([round(t0, 2), round(t1, 2)])
        else:
            box = F.box_union([s["box_det"] for s in got])
            b = F.box_round(box)
            rows.append({
                "t0": round(t0, 2), "t1": round(t1, 2), "n_do": len(got),
                "face": b,
                "score_min": round(min(s["score"] for s in got), 3),
                "trong_ben_trai": max(0, b[0] - pad),
                "trong_ben_phai": max(0, w - (b[2] + pad)),
                "trong_ben_tren": max(0, b[1] - pad),
                "trong_ben_duoi": max(0, h - (b[3] + pad)),
            })
        t0 = t1
    allb = [s["box_det"] for s in track["samples"] if s.get("box_det")]
    uni = F.box_round(F.box_union(allb)) if allb else None
    pad_box = None
    if uni:
        pad_box = [max(0, uni[0] - pad), max(0, uni[1] - pad),
                   min(w, uni[2] + pad), min(h, uni[3] + pad)]
    # Bien PHONG XA: gop MOI ung vien cua model, ke ca cac hop bi luat chon loai
    # (mat trong anh, contact sheet, nguoi phu). Ai muon chac chan 100% khong de
    # len bat cu cai gi giong mat thi dung so nay.
    every = []
    for s in track["samples"]:
        for b, _sc in s.get("cands", []):
            every.append(b)
    uni_all = F.box_round(F.box_union(every)) if every else None
    return {
        "nguon": "box_det (hop DO DUOC tren frame that, chua lam min)",
        "zone_step": zone_step, "pad": pad,
        "union_do_duoc": uni,
        "union_cong_pad": pad_box,
        "union_moi_ung_vien": uni_all,
        "union_moi_ung_vien_la_gi": ("gop MOI hop model tra ve, ke ca hop bi luat "
                                     "chon loai (mat trong anh/contact sheet). "
                                     "Bien phong xa nhat."),
        "cot_an_toan_trai": [0, pad_box[0]] if pad_box else None,
        "cot_an_toan_phai": [pad_box[2], w] if pad_box else None,
        "hang_an_toan_tren": [0, pad_box[1]] if pad_box else None,
        "hang_an_toan_duoi": [pad_box[3], h] if pad_box else None,
        # no_face phu thuoc --zone-step (mot mau roi dung bien window la du xoa
        # dau ca khoang trong). Nen kem theo khoang CHINH XAC ma track.py do duoc.
        "khoang_khong_do_duoc": no_face,
        "khoang_khong_do_duoc_chinh_xac": track.get("gaps_no_face", []),
        "windows": rows,
        "canh_bao": ("Cac so tren la toa do KHUNG GOC. Neu ban cung ap punch-in, "
                     "trong doan punch vung nhin bi thu lai theo 'crop' cua tung "
                     "window trong plan - phai tinh lai overlay theo do."),
    }


def print_safe_zones(sz, w, h):
    print("")
    print("  SAFE ZONE - DO TREN FRAME THAT (khong phai gia dinh)")
    print("  khung %dx%d, gop moi %.0fs, pad %d px" % (w, h, sz["zone_step"], sz["pad"]))
    print("")
    if not sz["union_do_duoc"]:
        print("  Khong do duoc hop mat nao.")
        return
    u, p = sz["union_do_duoc"], sz["union_cong_pad"]
    print("  HOP MAT GOP CA VIDEO   x %d..%d   y %d..%d" % (u[0], u[2], u[1], u[3]))
    print("  cong pad %d px         x %d..%d   y %d..%d"
          % (sz["pad"], p[0], p[2], p[1], p[3]))
    if sz.get("union_moi_ung_vien"):
        q = sz["union_moi_ung_vien"]
        print("  moi ung vien (phong xa) x %d..%d   y %d..%d"
              % (q[0], q[2], q[1], q[3]))
    print("")
    print("  DAT OVERLAY DUOC O:")
    print("    cot ben trai   x 0..%d        (rong %d px)" % (p[0], p[0]))
    print("    cot ben phai   x %d..%d      (rong %d px)" % (p[2], w, w - p[2]))
    print("    hang ben tren  y 0..%d        (cao %d px)" % (p[1], p[1]))
    print("    hang ben duoi  y %d..%d      (cao %d px)" % (p[3], h, h - p[3]))
    print("")
    print("    %-14s %-26s %s" % ("khoang", "hop mat do duoc", "trong: trai/phai/tren/duoi"))
    for r in sz["windows"]:
        print("    %5.0f-%5.0fs  x %4d..%4d y %4d..%4d   %4d /%4d /%4d /%4d"
              % (r["t0"], r["t1"], r["face"][0], r["face"][2],
                 r["face"][1], r["face"][3], r["trong_ben_trai"],
                 r["trong_ben_phai"], r["trong_ben_tren"], r["trong_ben_duoi"]))
    gaps = sz.get("khoang_khong_do_duoc_chinh_xac") or sz["khoang_khong_do_duoc"]
    if gaps:
        print("")
        print("    KHONG do duoc mat o: %s" % ", ".join(
            "%.1f-%.1fs" % (g[0], g[1]) for g in gaps))
        print("    -> o day skill KHONG BIET GI. Dung coi la 'trong'.")
    print("")
    print("  %s" % sz["canh_bao"])


# ------------------------------------------------------------------------ main
def main():
    F.setup_io()
    F.require_numpy()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--track", required=True, help="file track JSON tu track.py")
    ap.add_argument("--out", required=True, help="file plan JSON ket qua")
    ap.add_argument("--resources", default=None)
    # chon moc
    ap.add_argument("--at", default=None, help='moc chi dinh tay: "12.5,40,73.2"')
    ap.add_argument("--from-transcript", default=None,
                    help="transcript JSON (word-level) de bam vao tu nhan manh")
    ap.add_argument("--every", type=float, default=None,
                    help="cu N giay 1 punch (nhip don gian)")
    ap.add_argument("--report-safe-zones", action="store_true",
                    help="che do BAO SAFE ZONE, khong lap ke hoach punch")
    # hinh dang punch
    ap.add_argument("--zoom", type=float, default=1.12)
    ap.add_argument("--ramp-in", type=float, default=0.5)
    ap.add_argument("--hold", type=float, default=1.5)
    ap.add_argument("--ramp-out", type=float, default=0.5)
    ap.add_argument("--margin", type=float, default=40.0,
                    help="mat phai cach vien khung ket qua it nhat bao nhieu px")
    ap.add_argument("--center-band", type=float, default=0.30,
                    help="tam mat phai vao dai giua nay cua khung (0.30 = 30%% giua)")
    ap.add_argument("--max-zoom", type=float, default=2.5,
                    help="tran zoom khi phai nang len de keo mat vao dai giua")
    ap.add_argument("--center-safety", type=float, default=0.75,
                    help="nham vao bao nhieu phan cua dai giua (0.75 = nham "
                         "dai 22.5%% de con du hao khi do lai; 1.0 = nham sat "
                         "vien 15%% va rat de truot khi verify do lai)")
    ap.add_argument("--no-recenter", action="store_true",
                    help="KHONG tu nang zoom; giu dung --zoom da yeu cau")
    ap.add_argument("--allow-offcenter", action="store_true",
                    help="giu ca window khong keo duoc mat vao dai giua "
                         "(mac dinh: bo, vi verify se bao that bai)")
    ap.add_argument("--min-gap", type=float, default=3.0,
                    help="hai punch phai cach nhau it nhat bao nhieu giay")
    ap.add_argument("--max-punch", type=int, default=None,
                    help="toi da bao nhieu punch (mac dinh: 1 punch moi 25s)")
    # transcript
    ap.add_argument("--emphasis-file", default=DEFAULT_WORDS)
    ap.add_argument("--pause", type=float, default=0.30,
                    help="khoang nghi truoc tu, tu day tro len thi tinh la nhan manh")
    # an toan
    ap.add_argument("--allow-interpolated", action="store_true",
                    help="cho phep punch o doan KHONG do duoc mat (mac dinh: khong)")
    ap.add_argument("--allow-shot-change", action="store_true",
                    help="cho phep punch VAT qua cho doi canh (mac dinh: khong, vi "
                         "mat nhay cho giua cu zoom nen khong the giu dung tam)")
    ap.add_argument("--face-max-age", type=float, default=None,
                    help="mau do duoc phai cach tam punch khong qua bao nhieu giay "
                         "(mac dinh 1.5 x step cua track)")
    # safe zone
    ap.add_argument("--zone-step", type=float, default=5.0)
    ap.add_argument("--pad", type=float, default=24.0)
    ap.add_argument("--dry-run", action="store_true",
                    help="in ke hoach ra man hinh, KHONG ghi file")
    a = ap.parse_args()

    if not os.path.isfile(a.track):
        F.die("khong thay file track: %s\n"
              "     Chay truoc: python scripts/track.py --video \"%s\" --out track.json"
              % (a.track, a.video))
    track = F.read_json(a.track)
    for k in ("w", "h", "fps", "dur", "samples"):
        if k not in track:
            F.die("file track thieu khoa '%s' -> khong phai file do track.py tao ra: %s"
                  % (k, a.track))
    w, h, fps, dur = track["w"], track["h"], track["fps"], track["dur"]
    nbf = track.get("nb_frames") or int(round(dur * fps))
    step = float(track.get("step", 1.0))

    if os.path.abspath(a.video) != os.path.abspath(track.get("video", "")):
        print("  CANH BAO: --video khac video da track.")
        print("            track: %s" % track.get("video"))
        print("            hien tai: %s" % os.path.abspath(a.video))
        try:
            m2 = F.probe(a.video)
        except Exception as exc:
            F.die(str(exc))
        if (m2["w"], m2["h"]) != (w, h) or abs(m2["fps"] - fps) > 0.01:
            F.die("kich thuoc/fps khong khop track (%dx%d %.2ffps vs %dx%d %.2ffps).\n"
                  "     Toa do hop mat se sai. Chay lai track.py cho dung video nay."
                  % (m2["w"], m2["h"], m2["fps"], w, h, fps))

    # ---- che do B: safe zone
    if a.report_safe_zones:
        sz = safe_zones(track, a.zone_step, a.pad)
        print_safe_zones(sz, w, h)
        out = {"video": track.get("video"), "w": w, "h": h, "fps": fps, "dur": dur,
               "track": os.path.abspath(a.track), "che_do": "report-safe-zones",
               "safe_zones": sz}
        if a.dry_run:
            print("")
            print("  --dry-run: khong ghi file.")
            print("")
            return
        F.write_json(a.out, out)
        print("")
        print("  -> %s" % os.path.abspath(a.out))
        print("")
        return

    # ---- che do A: lap ke hoach punch
    span = a.ramp_in + a.hold + a.ramp_out
    if span <= 0:
        F.die("ramp-in + hold + ramp-out phai > 0")
    if a.zoom < 1.0:
        F.die("--zoom phai >= 1.0 (1.0 = khong zoom), dang nhan %.3f" % a.zoom)
    n_modes = sum(1 for x in (a.at, a.from_transcript, a.every) if x)
    if n_modes == 0:
        F.die("phai chon 1 cach dat moc: --at \"t1,t2\" HOAC --from-transcript <json>\n"
              "     HOAC --every <giay>. Muon xem safe zone thi dung --report-safe-zones.")
    if n_modes > 1:
        F.die("chi duoc chon 1 cach dat moc (--at / --from-transcript / --every).")

    max_n = a.max_punch if a.max_punch else max(1, int(dur / 25.0))
    cands, mode = [], ""
    if a.at:
        mode = "at"
        for tok in a.at.replace(";", ",").split(","):
            tok = tok.strip()
            if not tok:
                continue
            try:
                cands.append({"t": float(tok), "score": 9.9, "text": "",
                              "why": "moc chi dinh tay"})
            except ValueError:
                F.die("--at co gia tri khong phai so: '%s'" % tok)
        max_n = max(max_n, len(cands))
    elif a.every:
        mode = "every"
        if a.every <= 0:
            F.die("--every phai > 0")
        t = a.every
        while t + span <= dur:
            cands.append({"t": t, "score": 5.0, "text": "",
                          "why": "nhip moi %.1fs" % a.every})
            t += a.every
        max_n = max(max_n, len(cands))
    else:
        mode = "transcript"
        if not os.path.isfile(a.from_transcript):
            F.die("khong thay file transcript: %s" % a.from_transcript)
        if not os.path.isfile(a.emphasis_file):
            F.die("khong thay file tu nhan manh: %s\n"
                  "     File kem san le ra o: %s" % (a.emphasis_file, DEFAULT_WORDS))
        try:
            words = load_words(a.from_transcript)
        except Exception as exc:
            F.die("%s\n"
                  "     Transcript can dang: {\"segments\":[{\"start\":..,\"end\":..,"
                  "\"words\":[{\"start\":..,\"end\":..,\"word\":\"..\"}]}]}\n"
                  "     (dung dang faster-whisper word_timestamps=True xuat ra)" % exc)
        phrases = set(F.norm_vi(x) for x in F.read_lines(a.emphasis_file))
        phrases.discard("")
        cands = score_words(words, phrases, a.pause)
        print("  transcript     %d tu, %d tu co diem nhan manh"
              % (len(words), len(cands)))

    if not cands:
        F.die("khong tim duoc moc nao de punch.\n"
              "     Thu --every 20, hoac ha --pause, hoac them tu vao %s"
              % a.emphasis_file)

    anchors = pick_anchors(cands, dur, span, a.min_gap, max_n)
    if not anchors:
        F.die("moc nao cung bi loai (ra ngoai video, hoac qua sat nhau).\n"
              "     Video dai %.1fs, moi punch chiem %.1fs, cach nhau >= %.1fs.\n"
              "     Thu giam --hold hoac --min-gap." % (dur, span, a.min_gap))

    face_max_age = a.face_max_age if a.face_max_age is not None else 1.5 * step
    if step > a.hold:
        print("")
        print("  CANH BAO: track lay mau moi %.1fs nhung doan giu chi %.1fs."
              % (step, a.hold))
        print("            Vi tri mat tai giua doan giu se la SO NOI SUY, sai so lon,")
        print("            va verify co the bao lech. Nen chay lai track.py voi")
        print("            --step %.1f (hoac nho hon) roi lap plan lai."
              % max(0.25, a.hold / 2.0))
    windows, dropped = [], []
    for c in anchors:
        t_start = max(0.0, c["t"] - a.ramp_in)
        t_hold0 = t_start + a.ramp_in
        t_hold1 = t_hold0 + a.hold
        t_end = t_hold1 + a.ramp_out
        t_mid = (t_hold0 + t_hold1) / 2.0
        if t_end > dur:
            dropped.append({"t": round(c["t"], 2),
                            "vi_sao": "punch vuot qua cuoi video (%.2fs > %.2fs)"
                                      % (t_end, dur)})
            continue

        # Punch VAT qua cho doi canh thi vo nghia: mat nhay sang cho khac ngay
        # giua cu zoom, mot khung crop co dinh khong the om ca hai cho. Do that:
        # mot window 79.5-82.0s vat qua cu doi canh o t=80 da lech tam 16.0% x
        # 15.8% du plan du kien 9.3% x 13.5% -> verify bao that bai. Nen bo tu dau.
        near_jump = [s for s in track["samples"]
                     if t_start - step <= s["t"] <= t_end + step
                     and str(s.get("pick", "")).startswith("nhay-xa-da-xac-nhan")]
        if near_jump and not a.allow_shot_change:
            dropped.append({
                "t": round(c["t"], 2),
                "vi_sao": "doan %.1f-%.1fs vat qua cho DOI CANH (mat nhay cho o "
                          "t=%.1fs) -> mot tam zoom khong om duoc ca hai vi tri. Bo. "
                          "Muon lam that thi them --allow-shot-change."
                          % (t_start, t_end, near_jump[0]["t"])})
            continue

        measured = F.measured_boxes_in(track, t_start, t_end)
        age = F.nearest_measured_age(track, t_mid)
        if not measured and not a.allow_interpolated:
            dropped.append({
                "t": round(c["t"], 2),
                "vi_sao": "khong DO DUOC mat nao trong doan %.1f-%.1fs (mau do gan "
                          "nhat cach %.1fs) -> zoom se bam vao hop SUY RA. Bo. "
                          "Muon lam that thi them --allow-interpolated."
                          % (t_start, t_end, age if age is not None else -1)})
            continue
        if age is not None and age > face_max_age and not a.allow_interpolated:
            dropped.append({
                "t": round(c["t"], 2),
                "vi_sao": "mau do duoc gan nhat cach %.1fs (> --face-max-age %.1fs)"
                          % (age, face_max_age)})
            continue

        box_mid, src = F.track_face_at(track, t_mid, field="box")
        if box_mid is None:
            dropped.append({"t": round(c["t"], 2), "vi_sao": "track khong co hop mat nao"})
            continue
        # Hop phai om TRON: gop ca doan (khong chi frame giua), neu khong thi
        # dau/cuoi doan mat co the loi ra khoi khung da crop.
        fit_src = [s["box_det"] for s in measured] if measured else []
        for tt in (t_start, t_mid, t_end):
            b, _s = F.track_face_at(track, tt, field="box")
            if b:
                fit_src.append(b)
        face_fit = F.box_union(fit_src)
        mid_c = F.box_center(box_mid)
        sol = F.solve_window(a.zoom, face_fit, w, h, a.margin, desired=mid_c)

        # Tam mat co vao duoc dai giua khong? Neu khong, NANG ZOOM len muc toi
        # thieu du de keo vao - zoom nho thi khung nhin gan nhu khong doi duoc
        # (xem facelib.zoom_to_center). Day la ly do zoom thuc te co the khac
        # --zoom da yeu cau.
        # CAI BAY DA DO DUOC: nham SAT vien dai giua (he so 0.9 -> lech du kien
        # 13.5% so voi tran 15%) thi khi verify do lai tren file that, sai lech
        # cua chinh may nhan dien (do duoc 1-2% khung) day con so len 14.7% -
        # gan nhu truot. Vi vay nham vao GIUA dai (he so 0.75 -> 11.25%) de
        # con it nhat 3 diem % du tru.
        safety = max(0.05, min(1.0, a.center_safety))
        z_need = F.zoom_to_center(mid_c[0], mid_c[1], w, h,
                                  a.center_band * safety)
        nang = False
        if (not a.no_recenter) and z_need > sol["zoom"] + 1e-6:
            z_try = min(max(a.zoom, z_need), a.max_zoom)
            sol2 = F.solve_window(z_try, face_fit, w, h, a.margin, desired=mid_c)
            if sol2["zoom"] > sol["zoom"] + 1e-6:
                sol, nang = sol2, True

        z = sol["zoom"]
        ocx, ocy = F.out_center(mid_c, sol["crop"], z)
        lech_x, lech_y = abs(ocx - w / 2.0), abs(ocy - h / 2.0)
        center_ok = (lech_x <= (a.center_band / 2.0) * w + 0.5 and
                     lech_y <= (a.center_band / 2.0) * h + 0.5)
        if not center_ok and not a.allow_offcenter:
            # Noi RO ly do THAT, khong noi chung chung: 3 nguyen nhan khac nhau
            # va cach chua khac nhau han.
            if a.no_recenter:
                why = ("khong keo duoc tam mat vao dai giua %.0f%% khung: can zoom "
                       ">= %.2f nhung ban dua --no-recenter nen zoom bi giu o %.2f. "
                       "Bo --no-recenter (de skill tu nang zoom), hoac dat --zoom "
                       ">= %.2f, hoac them --allow-offcenter."
                       % (a.center_band * 100, z_need, z, z_need))
            elif z_need > a.max_zoom + 1e-6:
                why = ("khong keo duoc tam mat vao dai giua %.0f%% khung: can zoom "
                       ">= %.2f nhung tran --max-zoom chi cho %.2f. Tang --max-zoom "
                       ">= %.2f, ha --center-band, hoac them --allow-offcenter."
                       % (a.center_band * 100, z_need, a.max_zoom, z_need))
            else:
                why = ("khong keo duoc tam mat vao dai giua %.0f%% khung: can zoom "
                       ">= %.2f nhung zoom toi da ma van KHONG CAT mat chi la %.2f "
                       "(mat qua to / qua sat vien). Ha --margin, ha --center-band, "
                       "hoac them --allow-offcenter."
                       % (a.center_band * 100, z_need, sol["zoom_cap"]))
            dropped.append({
                "t": round(c["t"], 2),
                "vi_sao": why + " Lech %.0f x %.0f px." % (lech_x, lech_y)})
            continue

        cx0, cy0, cw, ch = sol["crop"]
        face_out = [round((face_fit[0] - cx0) * z, 1), round((face_fit[1] - cy0) * z, 1),
                    round((face_fit[2] - cx0) * z, 1), round((face_fit[3] - cy0) * z, 1)]
        windows.append({
            "i": len(windows),
            "t_start": round(t_start, 3), "t_hold_start": round(t_hold0, 3),
            "t_hold_mid": round(t_mid, 3), "t_hold_end": round(t_hold1, 3),
            "t_end": round(t_end, 3),
            "f_start": F.frame_of(t_start, fps, nbf),
            "f_hold_start": F.frame_of(t_hold0, fps, nbf),
            "f_hold_mid": F.frame_of(t_mid, fps, nbf),
            "f_hold_end": F.frame_of(t_hold1, fps, nbf),
            "f_end": F.frame_of(t_end, fps, nbf),
            "ramp_in": a.ramp_in, "hold": a.hold, "ramp_out": a.ramp_out,
            "zoom": z, "zoom_req": round(a.zoom, 4),
            "zoom_capped": sol["zoom_capped"], "zoom_cap": sol["zoom_cap"],
            "zoom_nang_de_vao_giua": nang,
            "zoom_can_de_vao_giua": round(z_need, 4),
            "cx": sol["cx"], "cy": sol["cy"], "crop": sol["crop"],
            "margin_x": sol["margin_x"], "margin_y": sol["margin_y"],
            "tam_mat_ra_du_kien": [round(ocx, 1), round(ocy, 1)],
            "lech_tam_du_kien": [round(lech_x, 1), round(lech_y, 1)],
            "lech_tam_du_kien_pct": [round(100.0 * lech_x / w, 2),
                                     round(100.0 * lech_y / h, 2)],
            "center_band": a.center_band,
            "center_safety": round(safety, 3),
            "center_ok": bool(center_ok),
            "face_mid": F.box_round(box_mid), "face_mid_src": src,
            "face_fit": F.box_round(face_fit),
            "face_out_du_kien": face_out,
            "n_do_duoc_trong_doan": len(measured),
            "do_duoc": bool(measured),
            "score": c.get("score"), "text": c.get("text", ""),
            "vi_sao": c.get("why", ""),
        })

    # khong cho 2 window dinh nhau / lan nhau (bieu thuc zoompan phai roi rac)
    windows.sort(key=lambda x: x["f_start"])
    clean = []
    for wd in windows:
        if clean and wd["f_start"] <= clean[-1]["f_end"]:
            dropped.append({"t": wd["t_start"],
                            "vi_sao": "chong lan window truoc (frame %d <= %d)"
                                      % (wd["f_start"], clean[-1]["f_end"])})
            continue
        wd["i"] = len(clean)
        clean.append(wd)
    windows = clean

    plan = {
        "video": os.path.abspath(a.video),
        "w": w, "h": h, "fps": fps, "dur": dur, "nb_frames": nbf,
        "track": os.path.abspath(a.track),
        "che_do": mode,
        "mac_dinh": {"zoom": a.zoom, "ramp_in": a.ramp_in, "hold": a.hold,
                     "ramp_out": a.ramp_out, "margin": a.margin,
                     "min_gap": a.min_gap, "max_punch": max_n,
                     "face_max_age": face_max_age,
                     "allow_interpolated": bool(a.allow_interpolated)},
        "n_punch": len(windows),
        "windows": windows,
        "bo_bot": dropped,
    }

    print("")
    print("  KE HOACH PUNCH-IN  (che do %s)" % mode)
    print("  video %dx%d %.2ffps %.2fs, %d frame" % (w, h, fps, dur, nbf))
    print("  hinh dang: %.2fs vao + %.2fs giu + %.2fs ra, zoom %.3f, mat cach vien >= %.0f px"
          % (a.ramp_in, a.hold, a.ramp_out, a.zoom, a.margin))
    print("")
    if windows:
        print("   #  giay            frame         zoom     tam (x,y)     lech tam ra")
        for wd in windows:
            mark = "!" if wd["zoom_capped"] else ("^" if wd["zoom_nang_de_vao_giua"] else " ")
            print("  %2d  %6.2f-%6.2f  %5d-%5d  %6.3f%s  %4.0f,%4.0f   %4.1f%% x %4.1f%%%s"
                  % (wd["i"], wd["t_start"], wd["t_end"], wd["f_start"], wd["f_end"],
                     wd["zoom"], mark, wd["cx"], wd["cy"],
                     wd["lech_tam_du_kien_pct"][0], wd["lech_tam_du_kien_pct"][1],
                     "" if wd["center_ok"] else "  LECH GIUA"))
        print("")
        if any(x["zoom_nang_de_vao_giua"] for x in windows):
            print("  ^ = da NANG zoom len (%.2f -> muc ghi o tren) vi zoom yeu cau qua"
                  % a.zoom)
            print("      nho de keo tam mat vao dai giua %.0f%% khung."
                  % (a.center_band * 100))
        if any(x["zoom_capped"] for x in windows):
            print("  ! = zoom bi HA XUONG so voi yeu cau, de hop mat khong bi cat.")
        print("  lech tam ra = tam mat lech bao nhieu phan tram so voi tam khung KET QUA;")
        print("      nguong dat la %.1f%% moi ben, ta nham vao %.1f%% (--center-safety %.2f)"
              % (a.center_band / 2.0 * 100,
                 a.center_band / 2.0 * 100 * max(0.05, min(1.0, a.center_safety)),
                 a.center_safety))
        print("      de con du hao khi verify.py DO LAI tren file that.")
        print("")
        for wd in windows:
            print("  #%d t=%.2f  mat %s -> trong ket qua du kien %s  (%s)"
                  % (wd["i"], wd["t_hold_mid"], wd["face_fit"],
                     [int(v) for v in wd["face_out_du_kien"]], wd["vi_sao"][:60]))
    else:
        print("  KHONG co punch nao duoc chon.")
    if dropped:
        print("")
        print("  DA BO %d moc:" % len(dropped))
        for d in dropped[:12]:
            print("    t=%.2f  %s" % (d["t"], d["vi_sao"]))
    print("")

    if not windows:
        F.die("khong con punch nao sau khi loc -> khong ghi plan.\n"
              "     Doc phan 'DA BO' o tren de biet vi sao, roi noi long tham so.")

    if a.dry_run:
        print("  --dry-run: khong ghi file.")
        print("")
        return

    F.write_json(a.out, plan)
    print("  -> %s" % os.path.abspath(a.out))
    print("")
    print("  Buoc tiep theo:")
    print("      python scripts/apply.py --video \"%s\" \\" % a.video)
    print("          --plan \"%s\" --out ket_qua.mp4" % a.out)
    print("")


if __name__ == "__main__":
    main()
