# -*- coding: utf-8 -*-
"""Am thanh + mux 3 ban: python finish.py <ver...>. Hinh: renders/v<ver>.mp4 (Remotion, khong tieng)."""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "G:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA/"
LIB = BASE + "03_MEDIA_LIBRARY/MUSIC_LIBRARY/"
SFXD = "D:/LOUGA_WORKSPACE/03_MEDIA_LIBRARY/shared-sources/sound-effects/"
OUTD = BASE + "10_FINAL_DELIVERABLES/2026-10-31_review-san-pham/"
SR = 48000
NAME = {"1": "01 - Review thảm Louis Yoga - Cao trào trước_v2", "2": "02 - Review thảm Louis Yoga - Tĩnh rồi cao trào_v3", "3": "03 - Review thảm Louis Yoga - Tò mò rồi hé lộ_v2"}
spec = json.load(open(f"{HERE}/src/spec.json", encoding="utf-8"))


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2)


def tp(path):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True).stderr.decode("utf-8", "replace").split("Summary:")[-1]
    return float(o.split("I:")[1].split("LUFS")[0]), float(o.split("Peak:")[1].split("dBFS")[0])


for ver in sys.argv[1:] or ["1", "2", "3"]:
    c = spec[ver]
    total = c["total"] / 30
    N = int(total * SR)
    mus = np.zeros((N, 2), np.float32)
    src = load(LIB + c["music"]["file"])
    X = int(0.03 * SR)
    for vs, ss, d in c["music"]["parts"]:
        st, a = int(vs * SR), int(ss * SR)
        L = min(int(d * SR), N - st)
        seg = src[a:a + L].copy()
        if vs > 0:  # moi noi nho, dung phach
            seg[:X] *= np.linspace(0, 1, X)[:, None]
        mus[st:st + L] = seg
    env = np.ones(N)
    fi = max(1, int(c["music"]["fade_in"] * SR))
    env[:fi] = np.linspace(0, 1, fi)
    fo = int(2.2 * SR)
    env[-fo:] = np.linspace(1, 0, fo) ** 1.5
    mus = mus * env[:, None]
    sfx = np.zeros_like(mus)
    for name, rel, f, vol in c["sfx"]:
        for s in c["shots"]:
            if s["name"] == name:
                x = load(SFXD + f)[: 3 * SR] * vol
                st = int((s["from"] / 30 + rel) * SR)
                L = min(len(x), N - st)
                sfx[st:st + L] += x[:L]
    for name, rel in c.get("spray", []):  # tieng xit: on trang loc 2,5-11 kHz, tat nhanh
        n = int(0.34 * SR)
        rng = np.random.default_rng(int(rel * 100))
        noise = rng.standard_normal((n, 2))
        F = np.fft.rfft(noise, axis=0)
        fq = np.fft.rfftfreq(n, 1 / SR)
        F[(fq < 2500) | (fq > 11000)] = 0
        y = np.fft.irfft(F, n=n, axis=0)
        e = np.minimum(np.arange(n) / (0.012 * SR), 1) * np.exp(-np.arange(n) / (0.11 * SR))
        y = (y / np.abs(y).max() * e[:, None] * 0.3).astype(np.float32)
        for s in c["shots"]:
            if s["name"] == name:
                st = int((s["from"] / 30 + rel) * SR)
                sfx[st:st + n] += y
    raw = f"{HERE}/renders/a{ver}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", raw], input=(mus + sfx).astype(np.float32).tobytes(), check=True)
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True).stderr.decode("utf-8", "replace")
    j = json.loads(o[o.rindex("{"): o.rindex("}") + 1])
    af = f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000"
    out = OUTD + NAME[ver] + ".mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{HERE}/renders/v{ver}.mp4", "-i", raw, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(NAME[ver], round(total, 1), "s", "LUFS/TP", tp(out))
