# -*- coding: utf-8 -*-
"""nns-cut-silence / verify.py — DO LAI KET QUA. Khong bao gio chi in "xong".

Kiem 6 nhom, moi thu deu la SO DO DUOC (khong bao gio chi in "xong"):

  1. So frame dau ra == so frame trong ke hoach (dem packet, khong tin metadata).
  2. Do dai tieng == do dai hinh, lech <= 1 frame.
  3. Tuong quan cheo: lay vai cua so 0.8s cua tieng DAU RA, doi chieu voi tieng
     DAU VAO tai vi tri ma time-map noi la tuong ung. Neu ban do thoi gian dung
     thi tuong quan ~1.0 va do tre ~0.
     Cua so nao vat qua mot moi cat thi BO QUA (ve ban chat khong the khop).
     Tuong quan tren tieng noi hay bam vao chu ky cao do, nen cho phep lech
     toi 1 frame.
  4. Moi moi cat: buoc nhay bien do giua 2 mau sat moi noi phai KHONG lon hon
     do doc p99.9 cua chinh tin hieu do -> chung minh khong sinh ra tieng "tach".
  5. Khong vung cat nao co peak > -34 dB (do LAI tren file goc, khong tin plan).
  6. HINH cung phai bi cat dung cho: lay chu ky anh xam cua vai frame dau ra roi
     doi chieu voi frame goc ma time-map chi ra, canh voi cac "moi nhu" (shift
     khac trong plan, va lech 1, 2, 8 frame). Chu ky duoc CHUAN HOA (z-score) nen
     phep do khong bi chuyen tone lam nhoe. Frame khop nhat PHAI la frame plan noi.
     Da tra gia: mot file co TIENG cat dung nhung HINH khong cat (677 frame dau
     cua ban goc) qua sach het phep kiem 1-5 -> phai co phep kiem 6 nay.
  6b. DAI MAU: muc sang / do tuong phan cua hinh ra phai bang hinh goc. Da tra gia:
     input yuvj420p (full range) bi encode ra yuv420p => dai mau bi nen 0-255 ->
     16-235, anh nhat di that (luma 29.9 -> 41.5) ma moi phep kiem khac van OK.

Vi du:
    python scripts/verify.py --video raw.mp4 --plan plan.json --out cut.mp4
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_io()

FAILS = []
WARNS = []
ROWS = []


def row(ok, name, detail):
    ROWS.append((ok, name, detail))
    if ok is False:
        FAILS.append("%s — %s" % (name, detail))
    elif ok is None:
        WARNS.append("%s — %s" % (name, detail))


def best_lag_corr(x, y, pad_left):
    """Tuong quan cheo chuan hoa giua x (N mau) va y (dai hon N).

    pad_left = so mau cua y nam TRUOC vi tri ky vong. Phai truyen dung, vi khi
    cua so o sat dau file thi y bi cat bot ben trai -> neu van gia dinh pad_left
    bang max_lag thi do tre bao ra se sai dung bang phan bi cat.

    Tra ve (lag tot nhat theo mau, gia tri tuong quan 0..1).
    """
    np = C._np()
    n = x.shape[0]
    if y.shape[0] < n + 1:
        return None, 0.0
    xn = float(np.sqrt((x * x).sum()))
    if xn <= 0:
        return None, 0.0
    num = np.correlate(y, x, mode="valid")            # dai = len(y)-n+1
    cs = np.concatenate([[0.0], np.cumsum(y.astype(np.float64) ** 2)])
    win_sq = cs[n:] - cs[:-n]                          # cung do dai voi num
    den = np.sqrt(np.maximum(win_sq, 1e-20)) * xn
    corr = num / den
    k = int(np.argmax(corr))
    return k - pad_left, float(corr[k])


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--video", required=True, help="video GOC (truoc khi cat)")
    ap.add_argument("--out", required=True, help="video KET QUA (sau khi cat)")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--wav", default=None, help="WAV kem theo (mac dinh <out>.wav neu co)")
    ap.add_argument("--windows", type=int, default=8, help="so cua so doi chieu, mac dinh 8")
    ap.add_argument("--win", type=float, default=0.8, help="do dai moi cua so (giay), mac dinh 0.8")
    ap.add_argument("--min-corr", dest="min_corr", type=float, default=0.85)
    ap.add_argument("--max-lag-frames", dest="max_lag_frames", type=float, default=1.0)
    ap.add_argument("--max-click-ratio", dest="max_click_ratio", type=float, default=1.0)
    ap.add_argument("--max-drop-peak-db", dest="max_drop_peak_db", type=float, default=-34.0)
    ap.add_argument("--video-probes", dest="video_probes", type=int, default=6,
                    help="so diem do khop frame HINH (mac dinh 6)")
    ap.add_argument("--video-min-margin", dest="video_min_margin", type=float, default=0.01,
                    help="cach biet toi thieu (don vi z) de ket luan / de bao sai (mac dinh 0.01)")
    ap.add_argument("--max-tone-shift", dest="max_tone_shift", type=float, default=2.0,
                    help="lech muc sang cho phep giua hinh ra va hinh goc (thang 0-255, mac dinh 2.0)")
    ap.add_argument("--max-tone-ratio", dest="max_tone_ratio", type=float, default=0.03,
                    help="lech ti le do tuong phan cho phep (mac dinh 0.03 = 3%%)")
    ap.add_argument("--no-video-check", dest="no_video_check", action="store_true",
                    help="bo qua phep kiem khop frame hinh (chi dung khi thuc su can nhanh)")
    ap.add_argument("--allow-no-audio", dest="allow_no_audio", action="store_true",
                    help="ket qua co chu y KHONG CO TIENG: ha cac phep kiem tieng xuong canh bao")
    a = ap.parse_args()

    np = C._np()
    if not os.path.isfile(a.plan):
        C.die("Khong tim thay plan: %s" % a.plan)
    plan = C.read_json(a.plan)
    if plan.get("skill") != C.SKILL_NAME:
        C.die("Plan khong phai cua %s." % C.SKILL_NAME)
    if not os.path.isfile(a.out):
        C.die("Khong tim thay file ket qua: %s\n       Chay apply.py truoc." % a.out)

    src = C.probe(a.video)
    dst = C.probe(a.out)
    exp = plan["expected"]
    fps = src["fps"]
    sr = plan["video"]["audio"]["sample_rate"]
    ch = plan["video"]["audio"]["channels"]
    frame_samples = int(round(sr * fps.denominator / float(fps.numerator)))

    print("")
    print("  nns-cut-silence — VERIFY")
    print("  " + "-" * 58)

    # ---- 1. so frame -------------------------------------------------------
    got = C.count_video_packets(a.out)
    row(got == exp["frames"], "so frame",
        "%s (ke hoach %d)" % (got, exp["frames"]))
    row(dst["fps_text"] == plan["video"]["fps"], "fps dau ra",
        "%s (ke hoach %s)" % (dst["fps_text"], plan["video"]["fps"]))

    # ---- 2. do dai tieng == do dai hinh ------------------------------------
    wav = a.wav or (os.path.splitext(a.out)[0] + ".wav")
    wav = wav if os.path.isfile(wav) else None
    v_dur = (got or 0) * fps.denominator / float(fps.numerator)
    tol = 1.0 * fps.denominator / float(fps.numerator)

    audio_ref = None
    if wav:
        w = C.ffprobe_all(wav)
        wsr = None
        wdur = None
        for s in w.get("streams", []):
            if s.get("codec_type") == "audio":
                wsr = int(s.get("sample_rate") or 0)
                try:
                    wdur = float(s.get("duration"))
                except Exception:
                    wdur = None
        if wdur is None:
            try:
                wdur = float(w.get("format", {}).get("duration"))
            except Exception:
                wdur = None
        row(wsr == sr, "WAV sample rate", "%s (goc %s)" % (wsr, sr))
        if wdur is not None:
            row(abs(wdur - v_dur) <= tol, "do dai WAV vs hinh",
                "%.4fs vs %.4fs (lech %.1f ms, cho phep %.1f ms)"
                % (wdur, v_dur, 1000 * (wdur - v_dur), 1000 * tol))
            audio_ref = wav
        else:
            row(None, "do dai WAV", "ffprobe khong cho biet")
    if dst["has_audio"]:
        adur = dst["a_duration"]
        if adur is None:
            row(None, "do dai tieng trong file", "ffprobe khong cho biet")
        else:
            ok = abs(adur - v_dur) <= tol
            row(ok if (audio_ref is None) else (True if ok else None),
                "do dai tieng trong file",
                "%.4fs vs hinh %.4fs (lech %.1f ms)" % (adur, v_dur, 1000 * (adur - v_dur)))
        if audio_ref is None:
            audio_ref = a.out
    elif audio_ref is None:
        row(None if a.allow_no_audio else False, "tieng dau ra",
            "file ket qua khong co tieng va cung khong co WAV"
            + (" (co --allow-no-audio nen chi canh bao; moi phep kiem tieng bi bo)"
               if a.allow_no_audio else
               ". Chay lai apply.py KHONG kem --no-wav de co WAV doi chieu."))

    # ---- 3. tuong quan cheo -----------------------------------------------
    segs = plan["keeps"]
    win = float(a.win)
    longest = max((s["new_end"] - s["new_start"]) for s in segs)
    if win > longest - 0.02:
        win = max(0.2, round((longest - 0.02) * 100) / 100.0)
        row(None, "do dai cua so", "giam xuong %.2fs vi doan giu dai nhat chi %.2fs"
            % (win, longest))
    win_n = int(round(win * sr))
    max_lag = int(round(3 * frame_samples))
    lag_limit = a.max_lag_frames * frame_samples

    cands = []
    used = set()
    for pas in (0.0, 0.4, 0.8):
        for i in range(a.windows):
            t = (i + 0.5) / a.windows * v_dur + pas
            seg = None
            for s in segs:
                if s["new_start"] <= t < s["new_end"]:
                    seg = s
                    break
            if seg is None:
                continue
            # cua so phai nam TRON trong 1 doan giu (khong vat qua moi cat)
            lo = seg["new_start"] + 0.01
            hi = seg["new_end"] - 0.01 - win
            if hi < lo:
                continue
            tt = min(max(t, lo), hi)
            key = round(tt, 3)
            if key in used:
                continue
            used.add(key)
            cands.append((tt, seg))
        if len(cands) >= a.windows:
            break

    if audio_ref is None:
        row(None if a.allow_no_audio else False, "tuong quan cheo",
            "khong co tieng dau ra de doi chieu")
    elif not cands:
        row(False, "tuong quan cheo",
            "khong co doan giu nao du dai %.2fs de doi chieu" % win)
    else:
        out_wins = [(int(round(t * sr)), int(round(t * sr)) + win_n) for t, _ in cands]
        in_wins = []
        pads = []
        for t, seg in cands:
            center = int(round((t + seg["shift"]) * sr))
            s0 = max(0, center - max_lag)
            pads.append(center - s0)          # bao nhieu mau thuc su nam ben trai
            in_wins.append((s0, s0 + win_n + pads[-1] + max_lag))
        xs = C.extract_windows(audio_ref, sr, ch, out_wins)
        ys = C.extract_windows(a.video, sr, ch, in_wins)

        checked = 0
        skipped_quiet = 0
        worst_corr = 1.0
        worst_lag = 0
        detail_lines = []
        for i, (t, seg) in enumerate(cands):
            x = xs[i]
            rms = float(np.sqrt(np.maximum((x * x).mean(), 1e-20)))
            if 20 * math.log10(rms) < -45.0:
                skipped_quiet += 1
                continue
            lag, corr = best_lag_corr(x, ys[i], pads[i])
            if lag is None:
                skipped_quiet += 1
                continue
            checked += 1
            worst_corr = min(worst_corr, corr)
            if abs(lag) > abs(worst_lag):
                worst_lag = lag
            detail_lines.append("      moi %s  <- goc %s   corr=%.4f  lech=%+d mau (%+.2f frame)"
                                % (C.fmt_hms(t), C.fmt_hms(t + seg["shift"]), corr, lag,
                                   lag / float(frame_samples)))
        if checked == 0:
            row(None, "tuong quan cheo", "khong co cua so nao du to tieng de do")
        else:
            row(worst_corr >= a.min_corr and abs(worst_lag) <= lag_limit,
                "tuong quan cheo",
                "%d cua so %.2fs: corr thap nhat %.4f, lech lon nhat %+d mau (%+.2f frame)"
                % (checked, win, worst_corr, worst_lag, worst_lag / float(frame_samples)))
        for line in detail_lines:
            print(line)

    # ---- 3b. khop mau TUYET DOI tai moi bien doan giu ----------------------
    # Day la phep kiem manh nhat co: apply.py chi COPY mau (khong resample,
    # khong doi sample rate), nen tieng dau ra phai TRUNG TUNG MAU voi tieng
    # goc tai vi tri ma plan noi. Cua so trai roi rac co the bo lot mot nhat cat
    # bi dich cho (da thu: dich nhat cat 10 frame trong vung im lang thi tuong
    # quan cheo khong thay) — kiem tung bien thi khong the bo lot.
    have_lossless = wav is not None
    if not have_lossless:
        row(None, "khop mau tung bien",
            "khong co WAV pcm nen khong so tuyet doi duoc (tieng AAC la lossy). "
            "Chay apply.py khong kem --no-wav de bat duoc phep kiem nay.")
    else:
        src_samples = plan["video"]["audio"].get("samples") or 0
        w = int(round(0.10 * sr))
        out_off = 0
        out_wins, in_wins, tags = [], [], []
        for si, s in enumerate(segs):
            n_seg = s["end_sample"] - s["start_sample"]
            ww = min(w, n_seg)
            if ww > 0:
                # dau doan
                if s["start_sample"] + ww <= src_samples:
                    out_wins.append((out_off, out_off + ww))
                    in_wins.append((s["start_sample"], s["start_sample"] + ww))
                    tags.append("dau doan %d @ %s" % (si, C.fmt_hms(s["new_start"])))
                # cuoi doan
                if s["end_sample"] <= src_samples and n_seg > ww:
                    out_wins.append((out_off + n_seg - ww, out_off + n_seg))
                    in_wins.append((s["end_sample"] - ww, s["end_sample"]))
                    tags.append("cuoi doan %d @ %s" % (si, C.fmt_hms(s["new_end"])))
            out_off += n_seg
        if not out_wins:
            row(None, "khop mau tung bien", "khong co bien nao do duoc")
        else:
            xs2 = C.extract_windows(wav, sr, ch, out_wins)
            ys2 = C.extract_windows(a.video, sr, ch, in_wins)
            worst_d = 0.0
            worst_tag = ""
            for i in range(len(out_wins)):
                n = min(xs2[i].shape[0], ys2[i].shape[0])
                if n <= 0:
                    continue
                d = float(np.abs((xs2[i][:n] - ys2[i][:n]) * 32768.0).max())
                if d > worst_d:
                    worst_d, worst_tag = d, tags[i]
            row(worst_d <= 2.0, "khop mau tung bien",
                "%d bien: lech lon nhat %.1f LSB (cho phep 2)%s"
                % (len(out_wins), worst_d, "" if worst_d <= 2.0 else "  <- %s" % worst_tag))

    # ---- 4. buoc nhay tai moi cat -----------------------------------------
    if audio_ref is None or len(segs) < 2:
        row(True, "buoc nhay moi cat", "khong co moi cat de kiem" if len(segs) < 2 else "bo qua")
    else:
        p999 = C.abs_diff_percentile(audio_ref, sr, ch, 99.9)
        allowed = max(p999 * a.max_click_ratio, 64.0)
        splice_wins = []
        for s in segs[1:]:
            idx = int(round(s["new_start"] * sr))
            splice_wins.append((max(0, idx - 2), idx + 2))
        chunks = C.extract_windows(audio_ref, sr, ch, splice_wins)
        steps = []
        for ck in chunks:
            if ck.shape[0] >= 3:
                steps.append(float(np.abs(np.diff(ck * 32768.0)).max()))
        worst_step = max(steps) if steps else 0.0
        row(worst_step <= allowed, "buoc nhay moi cat",
            "%d moi: lon nhat %.0f, do doc p99.9 = %.0f, cho phep %.0f (don vi int16)"
            % (len(steps), worst_step, p999, allowed))

    # ---- 5. do lai peak trong cac vung da cat ------------------------------
    drops = plan.get("drops", [])
    if not drops:
        row(True, "peak vung cat", "khong co vung nao bi cat")
    else:
        wins = [(d["start_sample"], d["end_sample"]) for d in drops]
        pks = C.window_peak_db(a.video, sr, ch, wins)
        worst = max(pks)
        bad = [(i, p) for i, p in enumerate(pks) if p > a.max_drop_peak_db]
        row(not bad, "peak vung cat",
            "%d vung, cao nhat %+.1f dB (nguong %+.1f dB)%s"
            % (len(drops), worst, a.max_drop_peak_db,
               "" if not bad else ", %d vung VUOT" % len(bad)))
        for i, p in bad[:10]:
            print("      vi pham: %s -> %s  peak %+.1f dB"
                  % (C.fmt_hms(drops[i]["start"]), C.fmt_hms(drops[i]["end"]), p))

    # ---- 6. HINH co bi cat dung cho khong (khop frame, khong chi dem frame) --
    # DAY LA PHEP KIEM DA TUNG THIEU. Da thu that: mot file co TIENG cat dung
    # nhung HINH la 677 frame DAU cua ban goc (tuc hinh khong he bi cat) van
    # qua het cac phep kiem 1-5 va verify bao DAT -> lech tieng/hinh toi 0.93s.
    # Cach do: lay chu ky anh xam cua vai frame dau ra, so voi frame goc ma
    # time-map noi la tuong ung VA voi cac frame "moi nhu" (cac shift khac trong
    # ke hoach + lech 8 frame). Frame khop nhat PHAI la frame ma plan chi ra.
    if a.no_video_check:
        row(None, "khop frame hinh", "bo qua theo yeu cau (--no-video-check)")
    else:
        shifts_f = sorted(set(s["old_start_frame"] - s["new_start_frame"] for s in segs))
        probes = []                                   # (frame_moi, shift_dung)
        n_want = max(2, int(a.video_probes))
        # rai deu tren cac doan giu, uu tien doan dai
        order = sorted(range(len(segs)),
                       key=lambda i: -(segs[i]["new_end_frame"] - segs[i]["new_start_frame"]))
        for i in order:
            s = segs[i]
            ln = s["new_end_frame"] - s["new_start_frame"]
            if ln < 3:
                continue
            sh = s["old_start_frame"] - s["new_start_frame"]
            probes.append((s["new_start_frame"] + ln // 2, sh, i))
            if len(probes) >= n_want:
                break
        # neu it doan qua thi lay them 1 diem nua trong moi doan
        if len(probes) < n_want:
            for i in order:
                s = segs[i]
                ln = s["new_end_frame"] - s["new_start_frame"]
                if ln < 8:
                    continue
                sh = s["old_start_frame"] - s["new_start_frame"]
                p = (s["new_start_frame"] + 2, sh, i)
                if p not in probes:
                    probes.append(p)
                if len(probes) >= n_want:
                    break
        probes.sort()

        n_src_frames = plan["video"]["nb_frames"] or src["nb_frames"]
        DECOY = 8
        cand_map = {}                 # frame_moi -> danh sach shift ung vien
        fine_map = {}                 # frame_moi -> tap shift "sat ke" (+-1, +-2)
        need_src = set()
        for nn, sh, si in probes:
            fine = set([sh - 2, sh - 1, sh + 1, sh + 2])
            cs = set(shifts_f) | {sh - DECOY, sh + DECOY} | fine | {sh}
            cs = sorted(c for c in cs if 0 <= nn + c < n_src_frames)
            cand_map[nn] = cs
            fine_map[nn] = fine
            for c in cs:
                need_src.add(nn + c)

        if not probes or len(cand_map) == 0:
            row(None, "khop frame hinh", "khong co doan giu nao du dai de doi chieu")
        else:
            sig_out = C.frame_signatures(a.out, [p[0] for p in probes])
            sig_src = C.frame_signatures(a.video, need_src)

            def zscore(v):
                """Chuan hoa chu ky ve trung binh 0 / do lech 1.

                PHAI chuan hoa: neu khong, mot thay doi TONE toan cuc (vd bi nen
                dai mau full->limited) lam MAE tho tang len ~12/255 o MOI ung vien
                va phep do het phan biet duoc. Chuan hoa xong thi phep nay chi do
                DUNG mot thu: frame nao khop, con chuyen tone do rieng o duoi.
                """
                v = v.astype(np.float64)
                sd = float(v.std())
                return (v - v.mean()) / (sd if sd > 1e-6 else 1.0)

            worst = None            # (margin, nn, sh, z_true)
            n_ok = 0
            n_bad = 0
            n_flat = 0
            bad_lines = []
            tone_dmean = []
            tone_ratio = []
            n_missing = 0
            for nn, sh, si in probes:
                if nn not in sig_out:
                    n_missing += 1
                    continue
                zo = zscore(sig_out[nn])
                scored = []
                for c in cand_map[nn]:
                    f = nn + c
                    if f in sig_src:
                        scored.append((float(np.abs(zo - zscore(sig_src[f])).mean()), c))
                if len(scored) < 2:
                    continue
                scored.sort()
                z_true = [m for m, c in scored if c == sh]
                if not z_true:
                    continue
                z_true = z_true[0]
                best_z, best_sh = scored[0]
                # SAI khi co ung vien khac RO RANG khop hon frame ma plan chi ra
                # (ke ca lech 1-2 frame — do la lech tieng/hinh that su).
                if best_sh != sh and (z_true - best_z) > a.video_min_margin:
                    n_bad += 1
                    bad_lines.append(
                        "      frame moi %d: plan noi khop goc %d (lech %.4f) nhung khop nhat lai la goc %d (lech %.4f)"
                        % (nn, nn + sh, z_true, nn + best_sh, best_z))
                    continue
                # tone: chi do tren cap frame ma plan noi la tuong ung
                if (nn + sh) in sig_src:
                    o = sig_out[nn].astype(np.float64)
                    r = sig_src[nn + sh].astype(np.float64)
                    tone_dmean.append(abs(float(o.mean() - r.mean())))
                    tone_ratio.append(float(o.std()) / max(float(r.std()), 1e-6))
                # Ket luan duoc hay khong thi chi tinh tren cac ung vien XA
                # (shift cua doan khac / lech 8 frame). Hai frame lien ke trong
                # doan im lang gan nhu giong nhau nen khong dung de ket luan.
                coarse = [m for m, c in scored
                          if c != sh and c not in fine_map[nn]]
                if not coarse:
                    n_flat += 1
                    continue
                margin = min(coarse) - z_true
                if margin < a.video_min_margin:
                    n_flat += 1
                    continue
                n_ok += 1
                if worst is None or margin < worst[0]:
                    worst = (margin, nn, sh, z_true)
            if n_bad:
                row(False, "khop frame hinh",
                    "%d/%d diem do KHONG khop frame goc ma plan chi ra -> HINH bi cat sai "
                    "(tieng va hinh lech nhau)" % (n_bad, n_bad + n_ok + n_flat))
                for ln in bad_lines[:8]:
                    print(ln)
            elif n_ok == 0 and n_flat == 0:
                row(False, "khop frame hinh",
                    "khong doc duoc frame nao trong %d diem can do tu file ket qua "
                    "(%d diem khong co frame do) -> file ket qua khong dung ke hoach"
                    % (len(probes), n_missing))
            elif n_ok == 0:
                row(None, "khop frame hinh",
                    "%d diem do deu khong phan biet duoc (hinh gan nhu tinh) — khong ket luan duoc%s"
                    % (n_flat, "" if not n_missing else
                       ", %d diem khong lay duoc frame" % n_missing))
            else:
                row(True, "khop frame hinh",
                    "%d diem do khop DUNG frame goc (lech %.4f, cach biet nho nhat %.4f)%s%s"
                    % (n_ok, worst[3], worst[0],
                       "" if not n_flat else ", %d diem hinh tinh khong ket luan" % n_flat,
                       "" if not n_missing else ", %d diem khong lay duoc frame" % n_missing))

            # ---- 6b. TONE/DAI MAU: hinh ra co bi lam nhat di khong ------------
            # Da tra gia: input yuvj420p (full range 0-255) bi encode ra yuv420p
            # => ffmpeg nen dai mau ve 16-235. Anh nhat di that su (luma trung binh
            # 29.9 -> 41.5) ma MOI phep kiem khac deu OK. Xem cac-cai-bay.md muc 14.
            if not tone_dmean:
                row(None, "dai mau (tone) hinh", "khong do duoc")
            else:
                dm = float(np.median(np.array(tone_dmean)))
                rt = float(np.median(np.array(tone_ratio)))
                ok_tone = dm <= a.max_tone_shift and abs(rt - 1.0) <= a.max_tone_ratio
                row(ok_tone, "dai mau (tone) hinh",
                    "lech muc sang trung vi %.2f/255 (cho phep %.2f), ti le do tuong phan %.3f "
                    "(cho phep 1+-%.3f)%s"
                    % (dm, a.max_tone_shift, rt, a.max_tone_ratio,
                       "" if ok_tone else
                       " -> nghi bi nen dai mau full<->limited: kiem -pix_fmt / -color_range trong apply.py"))

    # ---- bang ket qua ------------------------------------------------------
    print("")
    for ok, name, detail in ROWS:
        tag = "[OK]  " if ok is True else ("[CANH BAO]" if ok is None else "[SAI]  ")
        print("    %-10s %-24s %s" % (tag, name, detail))
    print("")
    if FAILS:
        print(C.LINE)
        print("  VERIFY THAT BAI — %d hang muc SAI" % len(FAILS))
        print(C.LINE)
        for f in FAILS:
            print("    - %s" % f)
        print("")
        print("  KHONG dung file ket qua nay. Doc references/cac-cai-bay.md,")
        print("  sua tham so hoac bao loi len, roi chay lai apply.py.")
        print("")
        sys.exit(1)
    if WARNS:
        print("  Co %d canh bao (khong chan): %s" % (len(WARNS), "; ".join(WARNS)))
        print("")
    print("  DAT. File ket qua dung ke hoach den tung frame va tung mau.")
    print("")


if __name__ == "__main__":
    main()
