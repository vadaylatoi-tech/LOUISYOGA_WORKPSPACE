# -*- coding: utf-8 -*-
"""Shared helpers for the louisyoga-reel-style1 scripts (stdlib + numpy only)."""
from __future__ import annotations

import json
import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL_DIR, "assets")
TEMPLATE = os.path.join(SKILL_DIR, "remotion-template")

# Windows consoles default to cp1252 and crash on Vietnamese text.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def die(msg: str, code: int = 1):
    print("\n[LOI] " + msg, file=sys.stderr)
    sys.exit(code)


def run(cmd: list[str], what: str = "") -> subprocess.CompletedProcess:
    """Run a command (bytes I/O); stop with its stderr tail on failure."""
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        die(f"{what or cmd[0]} that bai:\n{p.stderr.decode('utf-8', 'replace')[-2000:]}")
    return p


def ffprobe(path: str) -> dict:
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate,nb_frames", "-of", "json", path],
        capture_output=True,
    )
    if p.returncode != 0:
        die(f"ffprobe khong doc duoc {path}")
    return json.loads(p.stdout.decode("utf-8"))


def load_audio(path: str, sr: int = 48000, channels: int = 1):
    import numpy as np

    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(channels), "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    return x.reshape(-1, channels) if channels > 1 else x


def read_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: str, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)


def lufs(path: str) -> float:
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True).stderr.decode("utf-8", "replace")
    return float(o.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])


def loudness_report(path: str) -> str:
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True).stderr.decode("utf-8", "replace")
    summ = o.split("Summary:")[-1]
    i = summ.split("I:")[1].split("LUFS")[0].strip()
    pk = summ.split("Peak:")[1].split("dBFS")[0].strip()
    return f"I = {i} LUFS, true peak = {pk} dBTP"
