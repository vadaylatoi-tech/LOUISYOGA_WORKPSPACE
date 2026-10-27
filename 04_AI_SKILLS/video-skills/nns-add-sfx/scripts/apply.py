# -*- coding: utf-8 -*-
"""apply.py - tron SFX len tieng goc roi chuan hoa do to.

Master: volume=<G>dB  ->  alimiter=limit=<L>:level=disabled
G duoc DO ROI DIEU CHINH VONG LAP tren file AAC that, khong tinh nham mot lan.

TUYET DOI KHONG dung loudnorm: no am tham chuyen sang che do `dynamic` va nen
LRA (do that trong project nay: 5.5 -> 3.2 LU). Va `alimiter` phai co
`level=disabled`, vi `level=1` (mac dinh) tu keo bien do len va UNDO gioi han.

Luong hinh duoc COPY nguyen (-c:v copy): anh khong doi mot bit, render nhanh.

  python scripts/apply.py --video "<video>" --out ket_qua.mp4 --cues sfx_cues.json
"""
from __future__ import print_function

import argparse
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_stdout()

MAX_ROUNDS = 6
TOL_LUFS = 0.30
AAC_GUARD = 0.30   # chua san true-peak vi AAC co the vuot so voi WAV


def build_bed(cues, sfx_dir, n_samples, verbose=True):
    """Tron cac cue thanh mot lop nen stereo (N,2). Cue im lang = LOI CUNG."""
    import numpy as np
    bed = np.zeros((n_samples, 2), dtype=np.float32)
    cache = {}
    rows = []
    for i, c in enumerate(cues, 1):
        name = c["file"]
        path = os.path.join(sfx_dir, name.replace("/", os.sep))
        if not os.path.isfile(path):
            C.die("cue %d: khong tim thay file SFX \"%s\" trong %s\n"
                  "Chay lai probe.py + plan.py voi --resources dung thu muc."
                  % (i, name, C.disp(sfx_dir)))
        if name not in cache:
            cache[name] = C.decode_audio(path, channels=2)
        src = cache[name]
        if len(src) == 0:
            C.die("cue %d: file \"%s\" giai ma ra 0 mau." % (i, name))

        off = int(round(float(c.get("offset", 0.0)) * C.SR))
        dur = float(c.get("dur", 0.0))
        nseg = int(round(dur * C.SR)) if dur > 0 else (len(src) - off)
        seg = src[off:off + nseg].astype(np.float32).copy()
        if len(seg) == 0:
            C.die("cue %d (%s @ %.2fs): cat tu offset %.3fs dai %.3fs ra DOAN RONG.\n"
                  "File chi dai %.3fs. Chay lai probe.py de do lai onset."
                  % (i, name, c["t"], c.get("offset", 0.0), dur, len(src) / float(C.SR)))

        raw_peak = float(np.abs(seg).max())
        if raw_peak <= 0.0:
            C.die("cue %d (%s @ %.2fs): doan cat ra IM LANG HOAN TOAN (peak = 0).\n"
                  "offset=%.3fs dur=%.3fs. Gan nhu chac chan offset dat truoc onset\n"
                  "cua file (nhieu file SFX co im lang o dau, vi du mouse-click.mp3\n"
                  "im 1.02s dau).\n"
                  "Sua: chay lai  python scripts/probe.py ...  roi  plan.py ..."
                  % (i, name, c["t"], c.get("offset", 0.0), dur))

        m = len(seg)
        fin = int(round(float(c.get("fade_in", 0.0)) * C.SR))
        fout = int(round(float(c.get("fade_out", 0.0)) * C.SR))
        if fin > 0:
            k = min(fin, m)
            seg[:k] *= np.linspace(0.0, 1.0, k, dtype=np.float32)[:, None]
        if fout > 0:
            k = min(fout, m)
            seg[m - k:] *= np.linspace(1.0, 0.0, k, dtype=np.float32)[:, None]
        seg *= np.float32(10.0 ** (float(c.get("gain_db", 0.0)) / 20.0))

        post_peak = float(np.abs(seg).max())
        if post_peak <= 0.0:
            C.die("cue %d (%s @ %.2fs): sau khi lam mo dan / nhan gain thi peak = 0.\n"
                  "fade_in %.3f + fade_out %.3f dai hon ca doan (%.3fs), hoac gain qua thap."
                  % (i, name, c["t"], c.get("fade_in", 0.0), c.get("fade_out", 0.0),
                     m / float(C.SR)))

        start_t = c["t"] - (m / float(C.SR)) if c.get("align") == "end" else c["t"]
        s = int(round(start_t * C.SR))
        if s < 0:
            seg = seg[-s:]
            s = 0
            if len(seg) == 0:
                C.die("cue %d (%s): dat truoc giay 0 va bi cat het." % (i, name))
        if s >= n_samples:
            C.die("cue %d (%s @ %.2fs): bat dau sau khi video het (%.2fs)."
                  % (i, name, c["t"], n_samples / float(C.SR)))
        e = min(s + len(seg), n_samples)
        bed[s:e] += seg[:e - s]
        rows.append((c["t"], name, c.get("role", "?"), c.get("gain_db", 0.0),
                     len(seg) / float(C.SR), post_peak, start_t))

    if verbose:
        print("  %-8s %-24s %-11s %7s %7s %9s  %s"
              % ("t", "file", "vai", "gain", "dur", "peak", "bat dau"))
        print("  " + "-" * 88)
        for t, name, role, g, d, pk, st in rows:
            print("  %-8.2f %-24s %-11s %+6.1f %7.3f %9.4f  %.2f"
                  % (t, name[:24], role, g, d, pk, st))
    return bed, rows


def encode_audio(raw_path, out_path, gain_db, limit_lin, abr):
    """Ma hoa audio-only ra AAC voi master hien tai. Khong co duong dan trong filter."""
    af = "volume=%.3fdB,alimiter=limit=%.6f:level=disabled" % (gain_db, limit_lin)
    C.run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
           "-f", "f32le", "-ar", str(C.SR), "-ac", "2", "-i", raw_path,
           "-af", af, "-c:a", "aac", "-b:a", abr, out_path],
          what="ma hoa audio that bai (filter: %s)" % af)


def main():
    ap = argparse.ArgumentParser(description="Tron SFX + chuan hoa do to")
    C.add_common_args(ap, need_out=True)
    ap.add_argument("--cues", required=True, help="cue sheet JSON tu plan.py")
    ap.add_argument("--target", type=float, default=None,
                    help="do to muc tieu, LUFS (mac dinh -14, hoac lay tu cue sheet)")
    ap.add_argument("--tp", type=float, default=None,
                    help="tran true peak, dBTP (mac dinh -1.5)")
    ap.add_argument("--abr", default="256k", help="bitrate AAC (mac dinh 256k)")
    ap.add_argument("--max-t", type=float, default=None,
                    help="chi dung cue trong N giay dau")
    ap.add_argument("--keep-temp", action="store_true",
                    help="giu lai file tam de xem xet")
    a = ap.parse_args()
    C.require_numpy(a.video)

    import numpy as np

    if not os.path.isfile(a.video):
        C.die("khong tim thay video: %s" % a.video)
    if not os.path.isfile(a.cues):
        C.die("khong tim thay cue sheet: %s\n"
              "Chay plan.py truoc:\n"
              "    python scripts/plan.py --video \"%s\" --out \"%s\" --onsets sfx_onsets.json"
              % (a.cues, a.video, a.cues))

    plan = C.read_json(a.cues)
    cues = plan.get("cues")
    if not isinstance(cues, list) or not cues:
        C.die("cue sheet khong co cue nao: %s" % a.cues)
    if a.max_t is not None:
        cues = [c for c in cues if c["t"] <= a.max_t + 1e-6]
        if not cues:
            C.die("--max-t %.2f loc het cue. Bo --max-t hoac tang lai." % a.max_t)

    target = a.target if a.target is not None else float(plan.get("target_lufs", -14.0))
    tp = a.tp if a.tp is not None else float(plan.get("target_tp", -1.5))

    sfx_dir = plan.get("sfx_dir")
    if a.resources:
        d2, f2, _s, _n = C.find_sfx_library(a.resources)
        if d2:
            sfx_dir = d2
    if not sfx_dir or not os.path.isdir(sfx_dir):
        C.die("khong tim thay thu muc SFX \"%s\".\n"
              "Goi lai voi --resources \"<thu-muc-chua-sound-effects>\"" % C.disp(sfx_dir))

    vid = C.probe_media(a.video)
    if not vid["has_audio"]:
        C.die("video khong co tieng goc. Chay preflight de xem huong dan.")

    print("")
    print("  nns-add-sfx / APPLY")
    print("  video    : %s  %.2fs" % (C.disp(a.video), vid["duration"]))
    print("  cue      : %d cue tu %s" % (len(cues), C.disp(a.cues)))
    print("  SFX      : %s" % C.disp(sfx_dir))
    print("  muc tieu : %.1f LUFS, true peak <= %.1f dBTP, AAC %s"
          % (target, tp, a.abr))
    print("")

    orig = C.decode_audio(a.video, channels=2)
    n_video = int(round(vid["duration"] * C.SR))
    n = max(len(orig), n_video)
    if len(orig) < n:
        orig = np.vstack([orig, np.zeros((n - len(orig), 2), dtype=np.float32)])
    print("  tieng goc: %.3fs (%d mau), khung lam viec %.3fs"
          % (len(orig) / float(C.SR), len(orig), n / float(C.SR)))
    print("")

    bed, rows = build_bed(cues, sfx_dir, n)
    bed_peak = float(np.abs(bed).max())
    print("")
    print("  lop SFX  : peak %.4f = %.1f dBFS" % (bed_peak, C.db(bed_peak)))
    if bed_peak >= 1.0:
        print("  LUU Y    : lop SFX tu no da >= 0 dBFS, se bi limiter keo lai nhieu")

    mix = (orig + bed).astype(np.float32)
    mix_peak = float(np.abs(mix).max())
    print("  ban tron : peak %.4f = %.1f dBFS" % (mix_peak, C.db(mix_peak)))

    if a.dry_run:
        print("")
        print("  --dry-run: da tron trong bo nho va kiem het cue, KHONG xuat file.")
        print("             %d cue, khong cue nao im lang." % len(rows))
        print("")
        return

    tmp = tempfile.mkdtemp(prefix="nns_sfx_")
    raw = os.path.join(tmp, "mix.f32")
    wav = os.path.join(tmp, "mix.wav")
    m4a = os.path.join(tmp, "master.m4a")
    m4a_ok = os.path.join(tmp, "master_ok.m4a")
    try:
        mix.tofile(raw)
        # do do to cua ban tron THO de biet diem xuat phat cua gain
        C.run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
               "-f", "f32le", "-ar", str(C.SR), "-ac", "2", "-i", raw,
               "-c:a", "pcm_f32le", wav])
        base = C.measure_loudness(wav)
        print("  ban tron : I=%.2f LUFS  LRA=%.2f LU  TP=%.2f dBFS (truoc master)"
              % (base["I"], base["LRA"], base["TP"]))
        print("")

        gain = target - base["I"]
        limit = 10.0 ** ((tp - AAC_GUARD) / 20.0)
        hist = []
        best = None
        print("  %-6s %8s %9s %9s %8s %8s"
              % ("vong", "gain dB", "limit", "I LUFS", "LRA", "TP dBFS"))
        print("  " + "-" * 56)
        for rnd in range(1, MAX_ROUNDS + 1):
            encode_audio(raw, m4a, gain, limit, a.abr)
            m = C.measure_loudness(m4a)
            hist.append({"round": rnd, "gain_db": round(gain, 3),
                         "limit": round(limit, 6), "I": m["I"],
                         "LRA": m["LRA"], "TP": m["TP"]})
            print("  %-6d %+8.2f %9.5f %9.2f %8.2f %8.2f"
                  % (rnd, gain, limit, m["I"], m["LRA"], m["TP"]))
            ok_i = abs(m["I"] - target) <= TOL_LUFS
            ok_tp = m["TP"] <= tp + 1e-6
            if ok_i and ok_tp:
                best = (gain, limit, m)
                shutil.copyfile(m4a, m4a_ok)
                break
            # Tran dang chan: TP dinh tran, VA them gain nhung I khong len theo
            # (limiter an het). Do bang ty le dI/dG chu khong doan.
            pinned = (m["TP"] >= tp - 0.15) and (m["I"] < target - TOL_LUFS)
            if pinned and len(hist) >= 3:
                dg = hist[-1]["gain_db"] - hist[-2]["gain_db"]
                di = hist[-1]["I"] - hist[-2]["I"]
            else:
                dg = di = 0.0
            if pinned and dg > 0.30 and di < 0.5 * dg:
                C.die("TRAN TRUE PEAK DANG CHAN.\n"
                      "Voi tai lieu nay, tran %.1f dBTP chi cho phep len toi\n"
                      "khoang %.2f LUFS, khong the dat %.2f LUFS.\n"
                      "Chon 1 trong 2:\n"
                      "  - noi tran ra:   --tp -1.5   (hoac -1.0)\n"
                      "  - ha muc tieu:   --target %.1f\n"
                      "(Muon vua to vua giu tran thi phai nen dong luc - skill nay\n"
                      " co y KHONG lam, vi se pha LRA. LRA hien tai %.2f LU.)"
                      % (tp, m["I"], target, round(m["I"] * 2) / 2.0, m["LRA"]))
            if not ok_tp:
                limit *= 10.0 ** (-(m["TP"] - tp + 0.20) / 20.0)
            if not ok_i:
                gain += (target - m["I"])
        else:
            C.die("khong dat duoc muc tieu sau %d vong.\n"
                  "Lan cuoi: I=%.2f (muc tieu %.2f +-%.2f), TP=%.2f (tran %.2f)\n"
                  "Thu: --target cao hon, hoac --tp cao hon (vi du --tp -1.0),\n"
                  "hoac ha gain_db cua cac cue trong cue sheet."
                  % (MAX_ROUNDS, hist[-1]["I"], target, TOL_LUFS, hist[-1]["TP"], tp))

        gain, limit, final_m = best
        src_audio = m4a_ok

        # ------------------------------------------------ ghep lai, COPY luong hinh
        outdir = os.path.dirname(os.path.abspath(a.out))
        if outdir and not os.path.isdir(outdir):
            os.makedirs(outdir)
        C.run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
               "-i", a.video, "-i", src_audio,
               "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "copy", "-c:a", "copy",
               "-movflags", "+faststart", a.out],
              what="ghep video + audio that bai")

        rep = {
            "version": 1,
            "video_in": C.disp(os.path.abspath(a.video)),
            "video_out": C.disp(os.path.abspath(a.out)),
            "cues_file": C.disp(os.path.abspath(a.cues)),
            "sfx_dir": C.disp(sfx_dir),
            "n_cues": len(rows),
            "target_lufs": target,
            "target_tp": tp,
            "abr": a.abr,
            "gain_db": round(gain, 3),
            "limit": round(limit, 6),
            "bed_peak_dbfs": round(C.db(bed_peak), 2),
            "mix_peak_dbfs": round(C.db(mix_peak), 2),
            "pre_master": {"I": base["I"], "LRA": base["LRA"], "TP": base["TP"]},
            "final": {"I": final_m["I"], "LRA": final_m["LRA"], "TP": final_m["TP"]},
            "rounds": hist,
            "cue_peaks": [{"t": t, "file": nm, "role": rl, "gain_db": g,
                           "dur": d, "peak": round(pk, 6),
                           "peak_dbfs": round(C.db(pk), 2), "start": round(st, 3)}
                          for t, nm, rl, g, d, pk, st in rows],
        }
        rep_path = os.path.splitext(a.out)[0] + ".sfxreport.json"
        C.write_json(rep_path, rep)

        print("")
        print("  master   : gain %+.2f dB, alimiter limit %.5f (level=disabled)"
              % (gain, limit))
        print("  ket qua  : I=%.2f LUFS  LRA=%.2f LU  TP=%.2f dBFS (do tren AAC that)"
              % (final_m["I"], final_m["LRA"], final_m["TP"]))
        print("  LRA      : %.2f -> %.2f LU (mat %.2f LU)"
              % (base["LRA"], final_m["LRA"], base["LRA"] - final_m["LRA"]))
        print("  hinh     : -c:v copy, khong ma hoa lai")
        print("")
        print("  da ghi   : %s" % C.disp(a.out))
        print("  bao cao  : %s" % C.disp(rep_path))
        print("")
        print("  Buoc cuoi (BAT BUOC): python scripts/verify.py --video \"%s\" "
              "--out \"%s\" --cues \"%s\"" % (a.video, a.out, a.cues))
        print("")
    finally:
        if a.keep_temp:
            print("  file tam giu lai o: %s" % C.disp(tmp))
        else:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
