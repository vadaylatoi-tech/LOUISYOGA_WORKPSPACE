# -*- coding: utf-8 -*-
"""Dung stem SFX + stem nhac thang tu Reel.tsx (CUES, MUSIC_CURVE) bang numpy — vai giay, thay cho 2 lan
render Remotion --codec=wav (~3 phut/lan vi Remotion van chay het timeline trong Chromium).

    python build_stems.py --project <project> --out-dir <thu muc> [--composition-tail 54]

Ra: <out-dir>/sfx.wav, <out-dir>/music.wav (48 kHz stereo, dung do dai composition).
Mo phong dung kit/sound.tsx: moi cue vao o frame f(t - ONSET), cat sau 3 s, volume co dinh;
nhac theo MUSIC_CURVE (noi suy tuyen tinh theo frame, kep 2 dau).
Neu Reel.tsx viet CUES / MUSIC_CURVE kieu la (khong parse duoc) -> bao loi, render_all.py se lui ve Remotion.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

SR = 48000
FPS = 30
ONSET = {"swoosh.mp3": 0.07, "quick-swoosh.mp3": 0.04, "pop.mp3": 0.23, "pop-2.mp3": 0.066, "punch.mp3": 0.107, "riser-metallic.mp3": 1.809,
         "camera-shutter.mp3": 0.04, "digital-counting-1.mp3": 0.063, "ding.mp3": 0.149, "quick-ting.mp3": 0.019, "correct.mp3": 0.079}


def f(t: float) -> int:
    return int(round(t * FPS))  # Math.round in theme.ts (ties differ only on exact .5 frames)


def evaluate(expr: str, names: dict) -> float:
    """Arithmetic only: numbers, + - * / ( ), f(x), and the constants in `names`."""
    if not re.fullmatch(r"[\w\s.+\-*/()]*", expr):
        raise ValueError(f"bieu thuc la: {expr!r}")
    for w in re.findall(r"[A-Za-z_]\w*", expr):
        if w != "f" and w not in names:
            raise ValueError(f"khong biet {w!r} trong {expr!r}")
    return float(eval(expr, {"__builtins__": {}}, {"f": f, **names}))  # noqa: S307 - whitelisted above


def split_top(s: str) -> list[str]:
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def plan(project: str):
    reel = open(os.path.join(project, "src", "reel", "Reel.tsx"), encoding="utf-8").read()
    data = open(os.path.join(project, "src", "reel", "data.ts"), encoding="utf-8").read()
    clean = float(re.search(r"CLEAN_DURATION=([\d.]+)", data).group(1))
    names: dict = {"FPS": FPS}
    names["VIDEO_FRAMES"] = round(clean * FPS)
    # simple numeric consts used inside CUES / curve (HOOK_DROP, TAIL, ...)
    for k, v in re.findall(r"^const (\w+) = ([\d.]+);", reel, re.M):
        names[k] = float(v)
    names["DURATION"] = names["VIDEO_FRAMES"] + names.get("TAIL", 54)
    cue_block = reel.split("const CUES")[1].split("\n];")[0].split("= [", 1)[1]
    cues = []
    for item in re.findall(r"\[([^\[\]]+)\]", cue_block):
        t, name, vol = split_top(item)
        cues.append((evaluate(t, names), name.strip("\"' "), evaluate(vol, names)))
    m = re.search(r"const MUSIC_CURVE[^=]*=\s*\[\s*\[(.*?)\],\s*\[(.*?)\],?\s*\];", reel, re.S)
    frames = [evaluate(x, names) for x in split_top(m.group(1))]
    vols = [evaluate(x, names) for x in split_top(m.group(2))]
    music = re.search(r'const MUSIC = "([^"]+)"', reel).group(1)
    return cues, (frames, vols), music, int(names["DURATION"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    pub = os.path.join(a.project, "public")
    cues, (frames, vols), music, dur_frames = plan(a.project)
    n = int(dur_frames / FPS * SR)
    sfx = np.zeros((n, 2), np.float32)
    cache: dict = {}
    for t, name, vol in cues:
        if name not in cache:
            cache[name] = K.load_audio(os.path.join(pub, "sfx", name), SR, 2)
        x = cache[name]
        fr = f(t - ONSET.get(name, 0))
        skip = max(0, -fr)  # sound longer than t (riser): trimmed from the front, like startFrom
        x = x[int(skip / FPS * SR): int(skip / FPS * SR) + int((f(3)) / FPS * SR)]
        st = int(max(0, fr) / FPS * SR)
        seg = x[: max(0, n - st)] * vol
        sfx[st: st + len(seg)] += seg
    mus = K.load_audio(os.path.join(pub, music), SR, 2)[:n]
    mus = np.pad(mus, ((0, n - len(mus)), (0, 0)))
    fr_axis = np.arange(n) / SR * FPS
    mus = mus * np.interp(np.floor(fr_axis), frames, vols)[:, None].astype(np.float32)
    os.makedirs(a.out_dir, exist_ok=True)
    for name, x in (("sfx.wav", sfx), ("music.wav", mus)):
        raw = os.path.join(a.out_dir, name + ".f32")
        x.astype(np.float32).tofile(raw)
        K.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-c:a", "pcm_s16le", os.path.join(a.out_dir, name)], "ghi " + name)
        os.remove(raw)
    print(f"  {len(cues)} cue, nhac {len(frames)} moc, {dur_frames} frame -> {a.out_dir}/sfx.wav, music.wav")


if __name__ == "__main__":
    main()
