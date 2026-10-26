# -*- coding: utf-8 -*-
"""Mix uu tien GIONG: giong (da xu ly) to nhat, SFX thu hai, nhac nhe va tu ha khi co loi; master -14 LUFS.

    python mix_stems.py --voice work/voice_proc.wav --sfx r/sfx.wav --music r/music.wav \
        --video r/video_muted.mp4 --out final.mp4 [--sfx-rel -2.5] [--music-under 19] [--work tmpdir]

--sfx-rel: SFX giu dung muc da dat trong Remotion, cong them N dB so voi giong.
           -2.5 dB cho ra dung ti le reel chuan (tieng thuong ~ -3.5 dB, punch ~ +7 dB so voi giong).
--music-under: nhac thap hon giong N dB truoc khi duck (duck them -5 dB khi co loi -> ~24 dB khi noi).
In ra so do kiem tra (dB so voi giong) de ghi bao cao.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

SR = 48000


def momentary(x, win=0.4):
    n = int(win * SR)
    m = x.mean(1) if x.ndim > 1 else x
    k = len(m) // n
    return 20 * np.log10(np.sqrt((m[: k * n].reshape(k, n) ** 2).mean(1)) + 1e-9)


def events(sfx_mono, vmed):
    sm = momentary(sfx_mono, 0.05)
    idx = np.where(sm > -50)[0]
    if not len(idx):
        return 0, 0, 0, 0
    g = np.split(idx, np.where(np.diff(idx) > 2)[0] + 1)
    pk = np.array([sm[x].max() for x in g if len(x)])
    return len(pk), np.median(pk) - vmed, np.percentile(pk, 90) - vmed, pk.max() - vmed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True)
    ap.add_argument("--sfx", required=True)
    ap.add_argument("--music", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sfx-rel", type=float, default=-2.5)
    ap.add_argument("--music-under", type=float, default=19.0)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    work = a.work or tempfile.mkdtemp()
    os.makedirs(work, exist_ok=True)

    v, s, m = (K.load_audio(p, SR, 2) for p in (a.voice, a.sfx, a.music))
    total = max(len(v), len(s), len(m))
    v, s, m = (np.pad(x, ((0, total - len(x)), (0, 0))) for x in (v, s, m))

    voice_gain = 10 ** ((-16 - K.lufs(a.voice)) / 20)  # voice -> -16 LUFS pre-master
    v = v * voice_gain
    s = s * voice_gain * 10 ** (a.sfx_rel / 20)
    vm = momentary(v)
    voice_level = np.percentile(vm[vm > -45], 60)
    mm = momentary(m)
    m = m * 10 ** ((voice_level - a.music_under - np.percentile(mm[mm > -70], 50)) / 20)
    # ducking: extra -5 dB while the voice is active (150 ms attack / 400 ms release)
    env = np.repeat(momentary(v, 0.05), int(0.05 * SR))[:total]
    env = np.pad(env, (0, total - len(env)), constant_values=-90)
    target = np.where(env > voice_level - 18, -5.0, 0.0)
    g = np.zeros_like(target)
    a_up, a_dn = np.exp(-1 / (0.4 * SR)), np.exp(-1 / (0.15 * SR))
    acc = 0.0
    for i in range(0, total, 240):
        t = target[i]
        acc = t + (acc - t) * (a_dn if t < acc else a_up) ** 240
        g[i: i + 240] = acc
    m = m * (10 ** (g / 20))[:, None]

    mix = (v + s + m).astype(np.float32)
    raw = os.path.join(work, "mix.f32")
    mix.tofile(raw)
    wav = os.path.join(work, "mix.wav")
    K.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-c:a", "pcm_f32le", wav], "ghi mix")
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True).stderr.decode("utf-8", "replace")
    j = json.loads(o[o.rindex("{"): o.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000")
    K.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af,
           "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", a.out], "mux")

    vmed = np.percentile(momentary(v, 0.05)[momentary(v, 0.05) > -45], 50)
    n, med, p90, mx = events(s.mean(1), vmed)
    act = momentary(v) > -45
    under = np.median(momentary(v)[act]) - np.median(momentary(m)[act])
    dur = total / SR
    print(f"  SFX: {n} tieng ({n/dur:.2f}/s) | thuong {med:+.1f} dB, p90 {p90:+.1f}, to nhat {mx:+.1f} (so voi giong)")
    print(f"  Nhac: thap hon giong {under:.1f} dB khi dang noi")
    print(f"  Master: {K.loudness_report(a.out)}  -> {a.out}")


if __name__ == "__main__":
    main()
