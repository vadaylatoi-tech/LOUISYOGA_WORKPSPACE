# -*- coding: utf-8 -*-
"""Kiem tra may co du dieu kien chay skill louisyoga-reel-style1.

    python preflight.py [--video raw.mp4]

In ra DAY DU hoac danh sach THIEU kem lenh cai. Exit 0 khi du.
"""
from __future__ import annotations

import argparse
import importlib
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

missing: list[str] = []


def ok(msg):
    print("  [OK]    " + msg)


def bad(msg, fix):
    print("  [THIEU] " + msg)
    print("          -> " + fix)
    missing.append(msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video")
    a = ap.parse_args()
    print("\n  KIEM TRA MOI TRUONG — louisyoga-reel-style1\n")

    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool):
            ok(tool)
        else:
            bad(tool, "Windows: winget install --id Gyan.FFmpeg -e  | macOS: brew install ffmpeg | Ubuntu: sudo apt install ffmpeg (mo lai terminal)")
    if shutil.which("ffmpeg"):
        flt = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True).stdout.decode("utf-8", "replace")
        for need in ("loudnorm", "ebur128", "afftdn", "deesser", "acompressor", "equalizer"):
            (ok if f" {need} " in flt else lambda m: bad(m, "Cai ban ffmpeg FULL (gyan.dev full build)"))(f"ffmpeg filter {need}")

    if sys.version_info >= (3, 9):
        ok(f"python {sys.version.split()[0]}")
    else:
        bad("python >= 3.9", "https://www.python.org/downloads/")

    for mod, pipname in (("numpy", "numpy"), ("PIL", "Pillow"), ("faster_whisper", "faster-whisper"), ("onnxruntime", "onnxruntime")):
        try:
            importlib.import_module(mod)
            ok(f"python: {pipname}")
        except Exception:
            bad(f"python: {pipname}", f"python -m pip install {pipname}")
    try:
        import av  # noqa: F401

        major = int(av.__version__.split(".")[0])
        if major >= 16:
            bad(f"PyAV {av.__version__} (faster-whisper 1.2 loi voi av>=16)", 'python -m pip install "av>=11,<16"')
        else:
            ok(f"PyAV {av.__version__}")
    except Exception:
        pass

    for tool, fix in (("node", "https://nodejs.org (ban LTS >= 20)"), ("npm", "di kem Node.js")):
        if shutil.which(tool):
            v = subprocess.run([tool, "--version"], capture_output=True, shell=os.name == "nt").stdout.decode().strip()
            ok(f"{tool} {v}")
        else:
            bad(tool, fix)

    for rel in ("det_10g.onnx", "fonts/Montserrat-Variable.ttf", "music/Inspired_KevinMacLeod_CCBY4.mp3", "broll/louisyoga_brand_film_30fps.mp4", "sfx/punch.mp3"):
        p = os.path.join(K.ASSETS, rel)
        (ok if os.path.isfile(p) else lambda m: bad(m, "chep lai thu muc assets/ cua skill"))(f"asset {rel}")

    if a.video:
        if not os.path.isfile(a.video):
            bad(f"video {a.video}", "kiem tra duong dan")
        else:
            info = K.ffprobe(a.video)
            v = [s for s in info["streams"] if s["codec_type"] == "video"]
            au = [s for s in info["streams"] if s["codec_type"] == "audio"]
            if v:
                ok(f"video {v[0]['width']}x{v[0]['height']} {v[0]['r_frame_rate']} fps, {float(info['format']['duration']):.1f}s")
            if not au:
                bad("video khong co tieng", "can file co giong noi")

    print()
    if missing:
        print(f"  THIEU {len(missing)} thu. Cai xong chay lai preflight.")
        sys.exit(1)
    print("  DAY DU. CHAY DUOC ROI.")


if __name__ == "__main__":
    main()
