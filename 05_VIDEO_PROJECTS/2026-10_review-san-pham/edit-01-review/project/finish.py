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
NAME = {"1": "01 - Review thảm Louis Yoga - Cao trào trước_v2", "2": "02 - Review thảm Louis Yoga - Tĩnh rồi cao trào_v5", "3": "03 - Review thảm Louis Yoga - Tò mò rồi hé lộ_v2"}
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
    for name, rel in c.get("spray", []):  # tieng xit "pshh": hoi em, lien tuc, khong co canh sac
        n = int(0.46 * SR)
        rng = np.random.default_rng(int(rel * 100))
        noise = rng.standard_normal((n, 2))
        F = np.fft.rfft(noise, axis=0)
        fq = np.fft.rfftfreq(n, 1 / SR) + 1
        hiss = np.exp(-(np.log(fq / 5200) ** 2) / (2 * 0.62 ** 2))  # dinh mem quanh 5,2 kHz
        air = 0.3 * np.exp(-(np.log(fq / 1300) ** 2) / (2 * 0.5 ** 2))  # than hoi o tam thap
        y = np.fft.irfft(F * (hiss + air)[:, None], n=n, axis=0)
        ti = np.arange(n) / SR
        e = np.sin(np.minimum(ti / 0.045, 1) * np.pi / 2) ** 2 * np.where(ti < 0.16, 1, np.exp(-(ti - 0.16) / 0.075))
        y = (y / np.abs(y).max() * e[:, None] * 0.24).astype(np.float32)
        for s in c["shots"]:
            if s["name"] == name:
                st = int((s["from"] / 30 + rel) * SR)
                sfx[st:st + n] += y
    if c.get("ticks"):  # tieng go chu: moi chu hien mot phim that tach tu ban ghi ban phim co
        k = load(SFXD + "mechanical-keyboard.mp3")
        rng = np.random.default_rng(7)
        ek = np.convolve(np.abs(k[:, 0]), np.ones(96) / 96, "same")
        pk, j = [], 0
        while j < len(ek):
            if ek[j] > ek.max() * 0.25:
                m = j + int(np.argmax(ek[j:j + int(0.06 * SR)]))
                pk.append(m)
                j = m + int(0.07 * SR)
            else:
                j += 1
        L = int(0.07 * SR)
        keyset = []
        for m in pk:
            a = max(0, m - int(0.004 * SR))
            q = k[a:a + L].copy()
            q *= np.minimum(1, (L - np.arange(len(q))) / (0.02 * SR))[:, None]
            keyset.append(q / np.abs(q).max())
        for t in c["ticks"]:
            q = keyset[rng.integers(len(keyset))] * rng.uniform(0.085, 0.125)
            st = int(t * SR)
            L2 = min(len(q), N - st)
            sfx[st:st + L2] += q[:L2]
    if c.get("intro"):
        H = int(0.9 * SR)  # dinh nhac dau (nguon 56,56)
        a = int((55.66 + 0.9) * SR)
        sw = src[a:a + H][::-1].copy() * (np.linspace(0, 1, H)[:, None] ** 2) * 0.6  # chinh hop am cua bai, dao nguoc
        sfx[:H] += sw
        n = int(0.7 * SR)  # nhip tram mem dung dinh nhac
        ti = np.arange(n) / SR
        th = np.sin(2 * np.pi * np.cumsum(46 + 18 * np.exp(-ti / 0.06)) / SR) * np.minimum(ti / 0.006, 1) * np.exp(-ti / 0.17) * 0.34
        sfx[H:H + n] += th[:, None].astype(np.float32)
        fd = load(SFXD + "fairy-dust.mp3")[: int(2.4 * SR)] * 0.1
        fd *= np.minimum(1, (len(fd) - np.arange(len(fd))) / SR)[:, None]
        sfx[H:H + len(fd)] += fd
    for at, f, vol in c.get("hits", []):  # canh dinh tieng dung lop at
        x = load(SFXD + f)[: 3 * SR] * vol
        st = max(0, int(at * SR) - int(np.argmax(np.abs(x[:, 0]))))
        L = min(len(x), N - st)
        sfx[st:st + L] += x[:L]
    raw = f"{HERE}/renders/a{ver}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", raw], input=(mus + sfx).astype(np.float32).tobytes(), check=True)
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True).stderr.decode("utf-8", "replace")
    j = json.loads(o[o.rindex("{"): o.rindex("}") + 1])
    af = f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000"
    out = OUTD + NAME[ver] + ".mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{HERE}/renders/v{ver}.mp4", "-i", raw, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(NAME[ver], round(total, 1), "s", "LUFS/TP", tp(out))
