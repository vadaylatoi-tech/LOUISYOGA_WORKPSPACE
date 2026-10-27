# -*- coding: utf-8 -*-
"""nns-cut-silence / plan.py — LAP KE HOACH CAT (khong sua file nao).

Nguyen tac (xem references/nguong-im-lang.md):
  * Nguong im lang SUY RA TU PHAN BO NANG LUONG CUA CHINH FILE DO, khong ghim -30/-38 dB.
  * Da do tren file that: san on p1=-84 dB, muc noi p70=-17.6 dB, va vung -50..-35 dB
    chiem 14.6% thoi luong — do la PHU AM NHE VA HOI THO, cat vao la mat tieng.
  * Nguong bi CHAN CUNG o -45 dB: khong bao gio long hon the.
  * Moi khoang lang chi bi cat PHAN GIUA, con lai khe ho T (--keep, mac dinh 0.10s),
    va giu GUARD (--guard, mac dinh 0.03s) o hai dau.
  * SELF-CHECK: do peak thuc te tung mau trong moi vung sap cat; neu > -34 dB
    thi vung do co tieng noi -> BAO LOI VA TU CHOI, khong cat.

Vi du:
    python scripts/plan.py --video raw.mp4 --plan plan.json
    python scripts/plan.py --video raw.mp4 --plan plan.json --keep 0.14 --min-sil 0.45
    python scripts/plan.py --video raw.mp4 --plan plan.json --protect "12.5-19.0" --protect-cuts
"""
from __future__ import annotations

import argparse
import math
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_io()

# ---- hang so co ly do ro rang, xem references/nguong-im-lang.md ----------
FLOOR_MARGIN_DB = 6.0    # khong bao gio dat nguong sat san on (se khong bat duoc gi)
SPEECH_MARGIN_DB = 30.0  # nguong phai thap hon muc noi it nhat bay nhieu
HARD_CAP_DB = -45.0      # CHAN CUNG: nguong khong duoc long hon -45 dB
MIN_DROP_SEC = 0.05      # cat ngan hon the thi vo nghia, lai de rui ro click


def fceil(fr):
    return -((-fr.numerator) // fr.denominator)


def ffloor(fr):
    return fr.numerator // fr.denominator


def fr(x):
    """float/str -> Fraction chinh xac theo thap phan (tranh sai so nhi phan)."""
    return Fraction(str(x))


# ---------------------------------------------------------------- nguong


def derive_threshold(p1, p70, cap=HARD_CAP_DB):
    """Suy ra nguong im lang tu phan bo nang luong cua chinh file.

    floor  = p1  (san on)      speech = p70 (muc noi)
    mid    = diem giua floor va speech (theo dB)
    cand   = min(mid, speech - 30)      -> luon cach xa tieng noi
    cand   = max(cand, floor + 6)       -> khong sat san on den muc vo dung
    thr    = min(cand, -45)             -> CHAN CUNG, khong bao gio long hon -45 dB
    """
    floor = float(p1)
    speech = float(p70)
    mid = floor + 0.5 * (speech - floor)
    cand = min(mid, speech - SPEECH_MARGIN_DB)
    cand = max(cand, floor + FLOOR_MARGIN_DB)
    thr = min(cand, cap)
    steps = [
        "%-18s = %+.1f dB" % ("san on p1", floor),
        "%-18s = %+.1f dB" % ("muc noi p70", speech),
        "%-18s = %+.1f dB" % ("diem giua", mid),
        "%-18s = %+.1f dB" % ("muc noi - %.0f dB" % SPEECH_MARGIN_DB, speech - SPEECH_MARGIN_DB),
        "%-18s = %+.1f dB" % ("san on + %.0f dB" % FLOOR_MARGIN_DB, floor + FLOOR_MARGIN_DB),
        "%-18s = %+.1f dB" % ("chan cung", cap),
        "%-18s = %+.1f dB" % ("=> NGUONG", thr),
    ]
    return thr, steps


# ---------------------------------------------------------------- scene cut


def detect_hard_cuts(path, scene_th):
    """Tim cac cat cung bang scene detection cua ffmpeg. Tra ve list giay."""
    ffmpeg = C.need_tool("ffmpeg")
    # file=- => in ra stdout. KHONG duoc dung file=C:/... vi dau hai cham
    # bi ffmpeg hieu la dau phan cach option (xem references/cac-cai-bay.md).
    vf = "select='gt(scene\\,%s)',metadata=print:file=-" % ("%.4f" % scene_th)
    cmd = [ffmpeg, "-v", "error", "-nostdin", "-i", path, "-map", "v:0",
           "-filter:v", vf, "-an", "-f", "null", "-"]
    rc, out, err = C.run(cmd, check=False)
    if rc != 0:
        C.die("Scene detection that bai (--protect-cuts):\n%s" % err.strip())
    times = []
    for line in (out or "").splitlines():
        line = line.strip()
        idx = line.find("pts_time:")
        if idx >= 0:
            try:
                times.append(float(line[idx + 9:].split()[0]))
            except Exception:
                pass
    return sorted(set(times))


# ---------------------------------------------------------------- runs


def find_runs(db, thr, min_hops, hop_sec):
    """Tim cac doan lien tiep co db < thr, dai >= min_hops. Tra ve list (t0,t1) Fraction."""
    n = int(db.shape[0])
    out = []
    i = 0
    below = db < thr
    while i < n:
        if below[i]:
            j = i
            while j < n and below[j]:
                j += 1
            if (j - i) >= min_hops:
                out.append((Fraction(i) * hop_sec, Fraction(j) * hop_sec))
            i = j
        else:
            i += 1
    return out


# ---------------------------------------------------------------- main


def build_plan(a):
    info = C.probe(a.video)
    if not info["has_audio"]:
        C.die("Video khong co stream audio — khong the tim khoang lang.\n"
              "       Chay preflight.py de xem cach ghep tieng vao truoc.")
    if info["vfr"] and not a.allow_vfr:
        C.die("Video co ve la VFR (r_frame_rate=%.3f, avg_frame_rate=%.3f).\n"
              "       Cat theo frame se bi lech tieng. Chuyen sang CFR truoc:\n"
              "         ffmpeg -i \"%s\" -c:v libx264 -crf 16 -r %d -c:a copy cfr.mp4\n"
              "       Hoac chay lai voi --allow-vfr neu ban chac chan file deu frame."
              % (info["fps_float"], info["avg_fps_float"] or 0.0, a.video,
                 int(round(info["fps_float"]))))

    fps = info["fps"]
    sr = info["a_sr"] or 48000
    ch = info["a_ch"] or 1
    hop = int(round(sr * C.HOP_MS / 1000.0))
    hop_sec = Fraction(hop, sr)
    np = C._np()

    print("")
    print("  nns-cut-silence — KE HOACH CAT")
    print("  " + "-" * 58)
    print("  Video     : %s" % a.video)
    print("  Hinh      : %dx%d  %s fps  %d frame  %.3fs"
          % (info["width"], info["height"], info["fps_text"], info["nb_frames"], info["duration"]))
    print("  Tieng     : %s %dHz %dch" % (info["a_codec"], sr, ch))
    print("  Do nang luong (hop %dms)..." % C.HOP_MS)

    db, peak_hop, n_samples = C.envelope(a.video, sr, ch, hop)
    pct = {q: float(np.percentile(db, q)) for q in (1, 5, 50, 70, 99)}
    band = float(np.mean((db >= -50.0) & (db <= -35.0)) * 100.0)

    print("    p1=%+.1f  p5=%+.1f  p50=%+.1f  p70=%+.1f  p99=%+.1f dBFS"
          % (pct[1], pct[5], pct[50], pct[70], pct[99]))
    print("    vung -50..-35 dB (phu am nhe + hoi tho) = %.1f%% thoi luong" % band)

    if a.threshold_db is not None:
        thr = float(a.threshold_db)
        steps = ["nguong do nguoi dung ap dat: %+.1f dB" % thr]
        thr_src = "override"
        if thr > HARD_CAP_DB:
            print("")
            print("    CANH BAO: nguong %+.1f dB LONG HON chan cung %+.1f dB."
                  % (thr, HARD_CAP_DB))
            print("    Vung -50..-35 dB la phu am nhe/hoi tho. Rat de cat mat tieng.")
    else:
        thr, steps = derive_threshold(pct[1], pct[70], cap=a.max_threshold_db)
        thr_src = "derived"
    print("")
    print("  Suy ra nguong im lang:")
    for s in steps:
        print("    %s" % s)

    keep = fr(a.keep)
    guard = fr(a.guard)
    min_sil = fr(a.min_sil)
    if keep < 0:
        C.die("--keep phai >= 0.")
    if guard < 0:
        C.die("--guard phai >= 0.")
    if min_sil <= keep + 2 * guard:
        C.die("--min-sil (%s) phai LON HON --keep + 2*--guard (%s). "
              "Neu khong thi khong con gi de cat." % (a.min_sil, float(keep + 2 * guard)))

    min_hops = max(1, fceil(min_sil / hop_sec))
    runs = find_runs(db, thr, min_hops, hop_sec)
    print("")
    print("  Khoang lang tim duoc (>= %.2fs) : %d" % (float(min_sil), len(runs)))

    # --- vung PHAI GIU NGUYEN -------------------------------------------------
    protect = C.parse_ranges(a.protect, "--protect")
    hard_cuts = []
    if a.protect_cuts:
        hard_cuts = detect_hard_cuts(a.video, a.scene_threshold)
        pad = float(a.protect_cut_pad)
        protect = C.merge_ranges(protect + [(t - pad, t + pad) for t in hard_cuts])
        print("  Cat cung phat hien duoc        : %d (bao ve +-%.2fs quanh moi cat)"
              % (len(hard_cuts), pad))
    if protect:
        print("  Vung bao ve (KHONG cat)        : %d doan, tong %.2fs"
              % (len(protect), sum(b - aa for aa, b in protect)))

    # --- tinh vung bo -------------------------------------------------------
    min_drop_frames = max(1, fceil(fr(MIN_DROP_SEC) * fps))
    drops = []
    skipped_protect = 0
    skipped_short = 0
    for (rs, re_) in runs:
        L = re_ - rs
        room = L - 2 * guard
        target = L - keep
        drop_len = target if target < room else room
        if drop_len <= 0:
            skipped_short += 1
            continue
        edge_head = a.trim_edges and rs <= hop_sec
        edge_tail = a.trim_edges and re_ >= Fraction(info["nb_frames"]) / fps - hop_sec
        if edge_head and not edge_tail:
            t0, t1 = rs, rs + drop_len          # bo tu dau video vao
        elif edge_tail and not edge_head:
            t0, t1 = re_ - drop_len, re_        # bo tu cuoi video ra
        else:
            center = (rs + re_) / 2
            t0, t1 = center - drop_len / 2, center + drop_len / 2

        pieces = C.subtract_ranges((float(t0), float(t1)), protect) if protect else [(float(t0), float(t1))]
        if protect and len(pieces) == 0:
            skipped_protect += 1
            continue
        if protect and (len(pieces) != 1 or abs(pieces[0][0] - float(t0)) > 1e-9
                        or abs(pieces[0][1] - float(t1)) > 1e-9):
            skipped_protect += 1  # bi cat bot boi vung bao ve
        for (pa, pb) in pieces:
            f0 = fceil(fr("%.6f" % pa) * fps)   # lam TRON VAO TRONG: tha cat it hon
            f1 = ffloor(fr("%.6f" % pb) * fps)
            f0 = max(0, f0)
            f1 = min(info["nb_frames"], f1)
            if f1 - f0 < min_drop_frames:
                continue
            drops.append([f0, f1, float(rs), float(re_)])

    # gop cac vung bo cham/chong nhau
    drops.sort(key=lambda d: d[0])
    merged = []
    for d in drops:
        if merged and d[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], d[1])
            merged[-1][3] = max(merged[-1][3], d[3])
        else:
            merged.append(list(d))
    drops = merged

    # --- SELF-CHECK: do peak THAT trong tung vung sap cat -------------------
    windows = [(C.frame_to_sample(d[0], fps, sr), C.frame_to_sample(d[1], fps, sr)) for d in drops]
    print("")
    print("  Self-check: do peak thuc te trong %d vung sap cat..." % len(drops))
    peaks = C.window_peak_db(a.video, sr, ch, windows) if windows else []
    bad = []
    for i, d in enumerate(drops):
        pk = peaks[i]
        d.append(pk)
        if pk > a.max_drop_peak_db:
            bad.append((i, d, pk))
    if bad:
        print("")
        print(C.LINE)
        print("  TU CHOI CAT — %d vung co TIENG NOI (peak > %+.1f dB)"
              % (len(bad), a.max_drop_peak_db))
        print(C.LINE)
        for i, d, pk in bad[:20]:
            print("    #%-3d %s -> %s  (frame %d..%d)  peak = %+.1f dB"
                  % (i, C.fmt_hms(C.frame_to_sec(d[0], fps)),
                     C.fmt_hms(C.frame_to_sec(d[1], fps)), d[0], d[1], pk))
        if len(bad) > 20:
            print("    ... va %d vung nua" % (len(bad) - 20))
        print("")
        print("  Nghia la nguong dang dung con LONG. Cach xu ly:")
        print("    1) Ha nguong xuong (so am hon), vi du:")
        print("         --threshold-db %.1f" % (min(thr, -55.0)))
        print("    2) Hoac bao ve rieng doan do:")
        print("         --protect \"%.2f-%.2f\"" %
              (max(0.0, C.frame_to_sec(bad[0][1][0], fps) - 0.2),
               C.frame_to_sec(bad[0][1][1], fps) + 0.2))
        print("    3) Neu doan do la video long tieng thuyet minh (cat la lech hinh/tieng)")
        print("       thi BAT BUOC dung --protect cho ca doan do.")
        print("")
        C.die("Ke hoach khong an toan — khong ghi file plan. Sua tham so roi chay lai.")

    worst = max([d[4] for d in drops], default=float("-inf"))

    # --- doan GIU + time map ------------------------------------------------
    total_frames = info["nb_frames"]
    keeps = []
    cur = 0
    for d in drops:
        if d[0] > cur:
            keeps.append([cur, d[0]])
        cur = max(cur, d[1])
    if cur < total_frames:
        keeps.append([cur, total_frames])
    if not keeps:
        C.die("Ke hoach se xoa toan bo video. Tham so sai — dung lai.")

    expected_frames = sum(k[1] - k[0] for k in keeps)
    removed_frames = total_frames - expected_frames
    segments = []
    new_f = 0
    for k in keeps:
        seg = {
            "old_start_frame": k[0],
            "old_end_frame": k[1],
            "new_start_frame": new_f,
            "new_end_frame": new_f + (k[1] - k[0]),
            "old_start": C.frame_to_sec(k[0], fps),
            "old_end": C.frame_to_sec(k[1], fps),
            "new_start": C.frame_to_sec(new_f, fps),
            "new_end": C.frame_to_sec(new_f + (k[1] - k[0]), fps),
            "shift": C.frame_to_sec(k[0] - new_f, fps),
            "start_sample": C.frame_to_sample(k[0], fps, sr),
            "end_sample": C.frame_to_sample(k[1], fps, sr),
        }
        segments.append(seg)
        new_f += k[1] - k[0]

    expected_samples = C.frame_to_sample(expected_frames, fps, sr)
    src_samples_needed = sum(s["end_sample"] - s["start_sample"] for s in segments)

    # --- in tom tat ---------------------------------------------------------
    lens = [C.frame_to_sec(d[1] - d[0], fps) for d in drops]
    print("    peak cao nhat trong cac vung cat = %s dB (nguong tu choi %+.1f)"
          % (("%+.1f" % worst) if worst > float("-inf") else "-inf", a.max_drop_peak_db))
    print("")
    print("  KET QUA KE HOACH")
    print("    So nhat cat            : %d" % len(drops))
    if skipped_short:
        print("    Bo qua (qua ngan)      : %d" % skipped_short)
    if skipped_protect:
        print("    Bi vung bao ve chan    : %d" % skipped_protect)
    print("    Thoi luong bo di       : %.3fs (%d frame, %.1f%%)"
          % (C.frame_to_sec(removed_frames, fps), removed_frames,
             100.0 * removed_frames / max(1, total_frames)))
    print("    Do dai cu -> moi       : %.3fs -> %.3fs"
          % (C.frame_to_sec(total_frames, fps), C.frame_to_sec(expected_frames, fps)))
    print("    So frame cu -> moi     : %d -> %d" % (total_frames, expected_frames))
    if lens:
        srt = sorted(lens)
        print("    Do dai nhat cat        : min %.3fs / trung vi %.3fs / max %.3fs"
              % (srt[0], srt[len(srt) // 2], srt[-1]))
        buckets = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.8), (0.8, 1.6), (1.6, 1e9)]
        print("    Phan bo:")
        for lo, hi in buckets:
            cnt = sum(1 for x in lens if lo <= x < hi)
            if cnt:
                name = ("%.1f-%.1fs" % (lo, hi)) if hi < 1e9 else (">%.1fs" % lo)
                print("      %-10s %s (%d)" % (name, "#" * min(40, cnt), cnt))

    have = n_samples
    if src_samples_needed > have + 1:
        print("")
        print("    LUU Y: audio nguon ngan hon video %.3fs — apply.py se dem im lang"
              % ((src_samples_needed - have) / float(sr)))
        print("           vao cuoi de tieng dai bang hinh.")

    plan = {
        "skill": C.SKILL_NAME,
        "plan_version": C.PLAN_VERSION,
        "video": {
            "path": os.path.abspath(a.video),
            "width": info["width"], "height": info["height"],
            "fps": info["fps_text"], "fps_float": info["fps_float"],
            "nb_frames": total_frames, "duration": C.frame_to_sec(total_frames, fps),
            "v_codec": info["v_codec"],
            "audio": {"codec": info["a_codec"], "sample_rate": sr, "channels": ch,
                      "samples": n_samples},
            "color": {k: info[k] for k in
                      ("color_range", "color_space", "color_primaries", "color_transfer")},
        },
        "params": {
            "keep": float(keep), "guard": float(guard), "min_sil": float(min_sil),
            "threshold_db": thr, "threshold_source": thr_src,
            "max_threshold_db": a.max_threshold_db,
            "max_drop_peak_db": a.max_drop_peak_db,
            "hop_ms": C.HOP_MS, "min_drop_sec": MIN_DROP_SEC,
            "trim_edges": bool(a.trim_edges),
            "protect": [[x, y] for x, y in protect],
            "protect_cuts": bool(a.protect_cuts),
            "scene_threshold": a.scene_threshold,
            "protect_cut_pad": a.protect_cut_pad,
            "allow_vfr": bool(a.allow_vfr),
        },
        "energy": {
            "hop_ms": C.HOP_MS,
            "p1": pct[1], "p5": pct[5], "p50": pct[50], "p70": pct[70], "p99": pct[99],
            "band_m50_m35_pct": band,
            "threshold_db": thr,
            "derivation": steps,
        },
        "hard_cuts": hard_cuts,
        "silence_runs": [[float(x), float(y)] for x, y in runs],
        "drops": [
            {"start_frame": d[0], "end_frame": d[1],
             "start": C.frame_to_sec(d[0], fps), "end": C.frame_to_sec(d[1], fps),
             "run_start": d[2], "run_end": d[3], "peak_db": (None if d[4] == float("-inf") else d[4]),
             "start_sample": C.frame_to_sample(d[0], fps, sr),
             "end_sample": C.frame_to_sample(d[1], fps, sr)}
            for d in drops
        ],
        "keeps": segments,
        "expected": {
            "frames": expected_frames,
            "duration": C.frame_to_sec(expected_frames, fps),
            "audio_samples": expected_samples,
            "removed_frames": removed_frames,
            "removed_sec": C.frame_to_sec(removed_frames, fps),
            "cuts": len(drops),
            "worst_drop_peak_db": (None if worst == float("-inf") else worst),
        },
    }
    timemap = build_timemap(plan)
    return plan, timemap


def build_timemap(plan):
    """Ban do thoi gian cu -> moi, de skill khac (sub/SFX/overlay) re-time theo."""
    segs = []
    for s in plan["keeps"]:
        segs.append({
            "old_start": s["old_start"], "old_end": s["old_end"],
            "new_start": s["new_start"], "new_end": s["new_end"],
            "shift": s["shift"],
            "old_start_frame": s["old_start_frame"], "old_end_frame": s["old_end_frame"],
            "new_start_frame": s["new_start_frame"], "new_end_frame": s["new_end_frame"],
        })
    return {
        "skill": C.SKILL_NAME,
        "plan_version": C.PLAN_VERSION,
        "fps": plan["video"]["fps"],
        "fps_float": plan["video"]["fps_float"],
        "source": plan["video"]["path"],
        "source_duration": plan["video"]["duration"],
        "output_duration": plan["expected"]["duration"],
        "how_to_use": (
            "Tim segment co old_start <= t < old_end, roi new_t = t - shift. "
            "Neu t nam trong mot 'removed' thi diem do da bi xoa: dung "
            "collapsed_to (moc moi ma ca vung bi xoa gom vao)."
        ),
        "segments": segs,
        "removed": [
            {"old_start": d["start"], "old_end": d["end"],
             "collapsed_to": _map_time(segs, d["start"])}
            for d in plan["drops"]
        ],
    }


def _map_time(segs, t):
    for s in segs:
        if s["old_start"] <= t < s["old_end"]:
            return t - s["shift"]
    # t nam trong vung bi xoa -> gom vao cuoi segment truoc do
    best = 0.0
    for s in segs:
        if s["old_end"] <= t:
            best = s["new_end"]
    return best


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--video", required=True, help="video dau vao")
    ap.add_argument("--plan", default=None, help="file JSON ke hoach (mac dinh <video>.plan.json)")
    ap.add_argument("--timemap", default=None, help="file JSON ban do thoi gian (mac dinh <plan>.timemap.json)")
    ap.add_argument("--out", default=None, help="chi de ghi vao plan cho de doc; plan.py khong xuat video")
    ap.add_argument("--keep", type=float, default=0.10, help="khe ho con lai o moi cho cat (giay), mac dinh 0.10")
    ap.add_argument("--guard", type=float, default=0.03, help="chua ra o hai dau khoang lang (giay), mac dinh 0.03")
    ap.add_argument("--min-sil", dest="min_sil", type=float, default=0.35,
                    help="khoang lang ngan hon nay thi bo qua (giay), mac dinh 0.35")
    ap.add_argument("--threshold-db", dest="threshold_db", type=float, default=None,
                    help="ap dat nguong dBFS (mac dinh: suy ra tu file)")
    ap.add_argument("--max-threshold-db", dest="max_threshold_db", type=float, default=HARD_CAP_DB,
                    help="chan cung, nguong khong duoc long hon (mac dinh -45)")
    ap.add_argument("--max-drop-peak-db", dest="max_drop_peak_db", type=float, default=-34.0,
                    help="peak toi da cho phep trong vung cat; cao hon la co tieng noi (mac dinh -34)")
    ap.add_argument("--protect", default=None,
                    help='vung KHONG duoc cat, "a-b,c-d" tinh bang giay')
    ap.add_argument("--protect-cuts", dest="protect_cuts", action="store_true",
                    help="tu tim cat cung va bao ve quanh no")
    ap.add_argument("--protect-cut-pad", dest="protect_cut_pad", type=float, default=0.25,
                    help="ban kinh bao ve quanh moi cat cung (giay), mac dinh 0.25")
    ap.add_argument("--scene-threshold", dest="scene_threshold", type=float, default=0.30,
                    help="nguong scene detection cho --protect-cuts, mac dinh 0.30")
    ap.add_argument("--trim-edges", dest="trim_edges", action="store_true",
                    help="khoang lang o dau/cuoi video thi bo tu phia ngoai vao (mac dinh: tat)")
    ap.add_argument("--allow-vfr", dest="allow_vfr", action="store_true",
                    help="cho chay du video co ve la VFR (rui ro lech tieng)")
    ap.add_argument("--dry-run", dest="dry_run", action="store_true",
                    help="chi in ke hoach, khong ghi file JSON")
    a = ap.parse_args()

    plan, timemap = build_plan(a)
    if a.out:
        plan["intended_out"] = os.path.abspath(a.out)

    if a.dry_run:
        print("")
        print("  --dry-run: khong ghi file nao.")
        print("")
        return

    plan_path = a.plan or (os.path.splitext(a.video)[0] + ".plan.json")
    tm_path = a.timemap or (os.path.splitext(plan_path)[0] + ".timemap.json")
    C.write_json(plan_path, plan)
    C.write_json(tm_path, timemap)
    print("")
    print("  Da ghi ke hoach : %s" % os.path.abspath(plan_path))
    print("  Da ghi time map : %s" % os.path.abspath(tm_path))
    print("")
    print("  Buoc tiep theo:")
    print("      python scripts/apply.py --video \"%s\" --plan \"%s\" --out \"<ket-qua>.mp4\""
          % (a.video, plan_path))
    print("")


if __name__ == "__main__":
    main()
