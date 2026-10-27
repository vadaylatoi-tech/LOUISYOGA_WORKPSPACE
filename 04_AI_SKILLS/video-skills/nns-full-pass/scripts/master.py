# -*- coding: utf-8 -*-
"""BUOC 9 — tron tieng goc + lop SFX, chuan hoa, roi mux voi `-c:v copy`.

    python scripts/master.py --video <x.sub.mp4> --bed <x.sfx.raw> --out <final.mp4>

HINH KHONG BAO GIO BI MA HOA LAI o buoc nay. Buoc 7 (burn) da ma hoa hinh dung
mot lan; o day chi lam tieng roi ghep vao.

Duong loudness:
  1. loudnorm 2 pass (linear=true) — giu nguyen dai dong.
  2. Neu no khong dat (thuong vi input_tp cao, loudnorm tu chuyen sang dynamic
     hoac khong len duoc muc): chuyen sang `volume=<gain>dB` + `alimiter`.
     alimiter PHAI co `level=disabled` — `level=1` (mac dinh) tu keo bien do
     len va UNDO chinh phan limiting vua lam.

Do lai bang cach GIAI MA file mp4 cuoi ra f32 roi lay dinh THAT.
`volumedetect` clamp gia tri nen no giau loi.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()

SR = 48000
TOL_LUFS = 0.5
AAC_GUARD = 0.3        # AAC co the vuot dinh mot chut so voi truoc khi ma hoa
MAX_ROUNDS = 6

MIX = ("[0:a]aresample=%d:resampler=soxr[a0];"
       "[1:a]aresample=%d[a1];"
       "[a0][a1]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[am]"
       % (SR, SR))


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.stdout or "", p.stderr or "", p.returncode


def decode_f32(path, stream=None):
    import numpy as np
    cmd = ["ffmpeg", "-v", "error", "-i", path]
    if stream:
        cmd += ["-map", stream]
    cmd += ["-f", "f32le", "-ar", str(SR), "-ac", "2", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0 or not p.stdout:
        C.die("khong giai ma duoc tieng cua %s" % path)
    return np.frombuffer(p.stdout, dtype="<f4").reshape(-1, 2)


def measure_loudness(path):
    """I / LRA / TP bang ebur128. Doc tu stderr cua ffmpeg."""
    _o, err, _rc = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
                        "-map", "0:a:0", "-af", "ebur128=peak=true",
                        "-f", "null", "-"])
    out = {}
    tail = err[-4000:]
    for key, pat in (("I", r"I:\s*(-?\d+\.?\d*)\s*LUFS"),
                     ("LRA", r"LRA:\s*(-?\d+\.?\d*)\s*LU"),
                     ("TP", r"Peak:\s*(-?\d+\.?\d*)\s*dBFS")):
        m = re.findall(pat, tail)
        if m:
            out[key] = float(m[-1])
    for k in ("I", "LRA", "TP"):
        out.setdefault(k, float("nan"))
    return out


def loudnorm_pass1(raw_voice, raw_bed, I, TP, LRA):
    graph = MIX + ";[am]loudnorm=I=%g:TP=%g:LRA=%g:print_format=json[out]" % (I, TP, LRA)
    _o, err, rc = run(["ffmpeg", "-hide_banner", "-nostats",
                       "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw_voice,
                       "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw_bed,
                       "-filter_complex", graph, "-map", "[out]",
                       "-f", "null", "-"])
    if rc != 0:
        return None
    blocks = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    if not blocks:
        return None
    try:
        return json.loads(blocks[-1])
    except Exception:
        return None


TAIL_PAD = 0.20        # im lang du ra o duoi, xem giai thich trong audio_chain


def audio_chain(af, total):
    """Chuoi xu ly tieng, KEM chong cut duoi. HAI cho cat duoi, khong phai mot.

    1. `loudnorm` xu ly theo khoi 100 ms va NEM DI khoi cuoi chua du 100 ms.
       Do that tren project nay: mat 72 ms, dung vao doan SFX cuoi cung.
    2. Bo ma hoa AAC con an them ~29 ms nua (priming delay): dua vao dung
       700800 mau thi giai ma ra chi con 699392.

    Ca hai cho deu KHONG lo ra qua metadata — `ffprobe` van bao gan du do dai.
    Chi khi GIAI MA dem mau moi thay.

    Nen o day pad DU RA 0.20s im lang roi de `-shortest` luc mux cat theo HINH.
    Pad dung bang do dai hinh la thieu: AAC an mat phan duoi, `-shortest` quay
    ra cat HINH cho bang tieng (438 -> 434 frame).
    """
    return (af + ",aresample=%d,apad,atrim=0:%.6f,asetpts=N/SR/TB"
            % (SR, total + TAIL_PAD))


def encode(raw_voice, raw_bed, af, out, abr, total):
    """Ma hoa tieng ra m4a. KHONG co duong dan nao nam trong chuoi filter."""
    graph = MIX + ";[am]" + audio_chain(af, total) + "[a]"
    _o, err, rc = run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
                       "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw_voice,
                       "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw_bed,
                       "-filter_complex", graph, "-map", "[a]",
                       "-c:a", "aac", "-b:a", abr, "-ar", str(SR), out])
    if rc != 0:
        C.die("ma hoa tieng that bai.\n  filter: %s\n%s" % (af, err[-2500:]))
    return af


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(
        description="Tron SFX + chuan hoa loudness + mux (-c:v copy)")
    ap.add_argument("--video", help="video DA burn chu, con tieng goc")
    ap.add_argument("--bed", help="lop SFX raw f32le 48k stereo")
    ap.add_argument("--out")
    ap.add_argument("--resources")
    ap.add_argument("--target", type=float, default=-14.0, help="LUFS")
    ap.add_argument("--tp", type=float, default=-2.0, help="dBTP")
    ap.add_argument("--lra", type=float, default=11.0)
    ap.add_argument("--abr", default="256k")
    ap.add_argument("--work", help="thu muc lam viec (giu lai de verify A/B)")
    ap.add_argument("--no-sfx", action="store_true",
                    help="khong co lop SFX, chi chuan hoa")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.video or not a.out:
        C.die("thieu tham so.\n"
              "    python scripts/master.py --video <x.sub.mp4> "
              "--bed <x.sfx.raw> --out <final.mp4>")
    if not os.path.isfile(a.video):
        C.die("khong thay video: %s" % a.video)
    if not a.no_sfx and (not a.bed or not os.path.isfile(a.bed)):
        C.die("khong thay lop SFX: %s\n"
              "  Chay buoc 8 truoc, hoac them --no-sfx neu co y khong chen SFX."
              % a.bed)
    np = C.import_numpy()

    info = C.probe_video(a.video)
    work = a.work or (os.path.splitext(os.path.abspath(a.out))[0] + ".work")

    F.banner("BUOC 9 — TRON SFX + CHUAN HOA + MUX",
             ["video vao : %s (%.2fs, %d frame)"
              % (os.path.basename(a.video), info["duration"], info["nb_frames"]),
              "lop SFX   : %s" % (os.path.basename(a.bed) if not a.no_sfx
                                  else "(khong co, --no-sfx)"),
              "muc tieu  : %.1f LUFS, true peak <= %.1f dBTP, AAC %s"
              % (a.target, a.tp, a.abr),
              "HINH      : copy nguyen, KHONG ma hoa lai"])

    if a.dry_run:
        print("")
        print("  [dry-run] khong ghi file nao. Se lam:")
        print("      1) giai ma tieng goc ra f32 (%d Hz stereo)" % SR)
        print("      2) loudnorm 2 pass tren ban da tron")
        print("      3) khong dat -> gain + alimiter level=disabled")
        print("      4) mux: -map 0:v -map 1:a -c:v copy")
        print("")
        return

    if not os.path.isdir(work):
        os.makedirs(work)
    voice_raw = os.path.join(work, "voice.raw")
    bed_raw = os.path.join(work, "bed.raw")
    m4a = os.path.join(work, "master.m4a")

    voice = decode_f32(a.video)
    n_video = int(round(info["duration"] * SR))
    n = max(len(voice), n_video)
    if len(voice) < n:
        voice = np.vstack([voice, np.zeros((n - len(voice), 2), dtype=np.float32)])
    voice = np.ascontiguousarray(voice[:n], dtype=np.float32)

    if a.no_sfx:
        bed = np.zeros((n, 2), dtype=np.float32)
    else:
        bed = np.fromfile(a.bed, dtype="<f4").reshape(-1, 2)
        if len(bed) < n:
            bed = np.vstack([bed, np.zeros((n - len(bed), 2), dtype=np.float32)])
        bed = np.ascontiguousarray(bed[:n], dtype=np.float32)

    voice.tofile(voice_raw)
    bed.tofile(bed_raw)
    print("")
    print("  tieng goc : %.3fs (%d mau), dinh %.4f"
          % (n / float(SR), n, float(np.abs(voice).max())))
    print("  lop SFX   : dinh %.4f = %.1f dBFS"
          % (float(np.abs(bed).max()),
             20 * np.log10(max(float(np.abs(bed).max()), 1e-9))))

    # ---------- duong 1: loudnorm 2 pass, linear
    af = None
    how = None
    m = loudnorm_pass1(voice_raw, bed_raw, a.target, a.tp, a.lra)
    if m:
        print("")
        print("  loudnorm pass 1: input_i=%s input_tp=%s input_lra=%s thresh=%s"
              % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"]))
        cand = ("loudnorm=I=%g:TP=%g:LRA=%g:measured_I=%s:measured_TP=%s"
                ":measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
                ":print_format=summary"
                % (a.target, a.tp, a.lra, m["input_i"], m["input_tp"],
                   m["input_lra"], m["input_thresh"], m["target_offset"]))
        encode(voice_raw, bed_raw, cand, m4a, a.abr, n / float(SR))
        got = measure_loudness(m4a)
        ok = (abs(got["I"] - a.target) <= TOL_LUFS and got["TP"] <= a.tp + 1e-6)
        print("  loudnorm pass 2: I=%.2f LUFS  LRA=%.2f  TP=%.2f dBFS  -> %s"
              % (got["I"], got["LRA"], got["TP"], "DAT" if ok else "KHONG DAT"))
        if ok:
            af, how = cand, "loudnorm 2 pass (linear)"
        else:
            print("  -> chuyen sang gain + alimiter (input_tp=%s qua cao cho "
                  "loudnorm linear)" % m["input_tp"])
    else:
        print("")
        print("  loudnorm pass 1 khong doc duoc so do -> dung gain + alimiter")

    # ---------- duong 2: gain + alimiter (level=disabled)
    if af is None:
        wav = os.path.join(work, "mix.wav")
        raw_mix = os.path.join(work, "mix.raw")
        (voice + bed).astype(np.float32).tofile(raw_mix)
        run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
             "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw_mix,
             "-c:a", "pcm_f32le", wav])
        base = measure_loudness(wav)
        print("  ban tron : I=%.2f LUFS  LRA=%.2f  TP=%.2f dBFS (truoc master)"
              % (base["I"], base["LRA"], base["TP"]))
        gain = a.target - base["I"]
        limit = 10.0 ** ((a.tp - AAC_GUARD) / 20.0)
        print("")
        print("  %-5s %9s %9s %9s %8s %8s"
              % ("vong", "gain dB", "limit", "I LUFS", "LRA", "TP dBFS"))
        print("  " + F.hr("-", 56))
        for rnd in range(1, MAX_ROUNDS + 1):
            cand = ("volume=%.3fdB,alimiter=limit=%.6f:level=disabled"
                    % (gain, limit))
            encode(voice_raw, bed_raw, cand, m4a, a.abr, n / float(SR))
            got = measure_loudness(m4a)
            print("  %-5d %+9.2f %9.5f %9.2f %8.2f %8.2f"
                  % (rnd, gain, limit, got["I"], got["LRA"], got["TP"]))
            if abs(got["I"] - a.target) <= TOL_LUFS and got["TP"] <= a.tp + 1e-6:
                af, how = cand, "gain %+.2f dB + alimiter (level=disabled)" % gain
                break
            if got["TP"] > a.tp:
                limit *= 10.0 ** ((a.tp - got["TP"]) / 20.0)
            gain += (a.target - got["I"])
        if af is None:
            C.die("khong dat duoc %.1f LUFS voi tran %.1f dBTP sau %d vong.\n"
                  "  Chon mot trong hai:\n"
                  "    - noi tran ra:  --tp -1.5\n"
                  "    - ha muc tieu:  --target %.1f"
                  % (a.target, a.tp, MAX_ROUNDS, a.target + 1))

    # ---------- mux: HINH COPY NGUYEN
    out_abs = os.path.abspath(a.out)
    d = os.path.dirname(out_abs)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    _o, err, rc = run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
                       "-i", os.path.abspath(a.video), "-i", m4a,
                       "-map", "0:v:0", "-map", "1:a:0",
                       "-c:v", "copy", "-c:a", "copy", "-shortest",
                       "-movflags", "+faststart", out_abs])
    if rc != 0:
        C.die("mux that bai:\n%s" % err[-2500:])

    # ---------- do lai TREN CHINH FILE MP4 CUOI
    fin = measure_loudness(out_abs)
    x = decode_f32(out_abs)
    peak = float(np.abs(x).max())
    over = int((np.abs(x) > 1.0).sum())
    got_v = C.probe_video(out_abs)

    print("")
    print("  " + F.hr("-"))
    print("  master   : %s" % how)
    print("  do TREN FILE MP4 CUOI (khong phai tren ban truoc khi ma hoa):")
    print("      I  = %.2f LUFS   (muc tieu %.1f)" % (fin["I"], a.target))
    print("      TP = %.2f dBFS   (tran %.1f)" % (fin["TP"], a.tp))
    print("      LRA= %.2f LU" % fin["LRA"])
    print("      dinh mau THAT sau khi giai ma = %.6f, so mau vuot 1.0 = %d"
          % (peak, over))
    print("  hinh     : %dx%d %.4gfps %d frame  (copy nguyen)"
          % (got_v["width"], got_v["height"], got_v["fps"], got_v["nb_frames"]))
    print("  " + F.hr("-"))

    # ho so cho verify: chuoi filter DUNG y het de dung lai ban A/B
    C.write_json(os.path.splitext(out_abs)[0] + ".ab.json", {
        "voice_raw": voice_raw, "bed_raw": bed_raw,
        "chain": MIX + ";[am]" + audio_chain(af, n / float(SR)),
        "master_af": af, "how": how, "target": a.target, "tp": a.tp,
        "final": {"I": fin["I"], "TP": fin["TP"], "LRA": fin["LRA"],
                  "sample_peak": peak, "over_1_0": over},
        "src_video": os.path.abspath(a.video), "out": out_abs})
    print("")
    print("  da ghi: %s" % out_abs)
    print("")


if __name__ == "__main__":
    C.run_main(main)
