# -*- coding: utf-8 -*-
"""Buoc 0 — kiem moi truong: ffmpeg, python, faster-whisper, GPU.

    python preflight.py            # chi kiem
    python preflight.py --gpu      # kiem them GPU co chay Whisper duoc khong (nap model)
"""
import argparse
import importlib
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dccommon as C  # noqa: E402


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", action="store_true", help="thu nap Whisper tren GPU")
    a = ap.parse_args()
    ok = True
    print("\n  KIEM MOI TRUONG — Duycongeditvideo_Buoc1\n")
    print("  python      : %s" % sys.version.split()[0])
    if sys.version_info < (3, 9):
        ok = False
        print("    -> can Python 3.9+")
    for exe in ("ffmpeg", "ffprobe"):
        p = shutil.which(exe)
        print("  %-11s : %s" % (exe, p or "THIEU"))
        if not p:
            ok = False
            print("    -> Windows: winget install Gyan.FFmpeg   |  macOS: brew install ffmpeg")
    for mod, pipname in (("faster_whisper", "faster-whisper"), ("numpy", "numpy")):
        try:
            importlib.import_module(mod)
            print("  %-11s : co" % pipname)
        except Exception:
            ok = False
            print("  %-11s : THIEU  -> pip install %s" % (pipname, pipname))
    if shutil.which("ffmpeg"):
        enc = "h264_nvenc (GPU)" if C.has_encoder("h264_nvenc") else "libx264 (CPU)"
        print("  ma hoa video: %s" % enc)
    try:
        import ctranslate2
        n = ctranslate2.get_cuda_device_count()
        print("  GPU CUDA    : %d thiet bi" % n)
        if n and os.name == "nt":
            C.add_cuda_dll_dirs()
            try:
                import ctypes
                ctypes.WinDLL("cublas64_12.dll")
                print("  cuBLAS      : co")
            except Exception:
                print("  cuBLAS      : THIEU -> pip install nvidia-cublas-cu12 \"nvidia-cudnn-cu12==9.*\"")
                print("                (khong cai thi Whisper chay CPU, cham hon 5-10 lan)")
    except Exception:
        print("  GPU CUDA    : khong kiem duoc (chay CPU)")
    if a.gpu and ok:
        m, desc = C.load_whisper()
        print("  Whisper     : chay tren %s" % desc)
    print("\n  %s\n" % ("DU HET. CHAY DUOC ROI." if ok else "CON THIEU — cai theo goi y o tren roi chay lai."))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
