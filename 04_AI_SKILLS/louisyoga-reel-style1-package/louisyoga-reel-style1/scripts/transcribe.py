# -*- coding: utf-8 -*-
"""Chep loi tieng Viet co moc thoi gian TUNG TU (faster-whisper large-v3).

    python transcribe.py --video raw.mp4 --out work/src.words.json [--model large-v3] [--device auto|cpu|cuda]

Lan dau tu tai model (~1.5 GB). GPU khong co cuBLAS/cuDNN thi tu lui ve CPU.
Ket qua: {"segments":[{start,end,text}], "words":[{w,start,end,p}]}
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402


def add_cuda_dlls():
    """Windows: cublas/cudnn cai bang pip nam trong site-packages/nvidia/*/bin, khong nam tren PATH
    -> phai add_dll_directory truoc khi nap model, neu khong se 'cublas64_12.dll not found' roi lui CPU."""
    if os.name != "nt":
        return
    import site

    for base in site.getsitepackages() + [site.getusersitepackages()]:
        for lib in ("cublas", "cudnn", "cuda_nvrtc"):
            d = os.path.join(base, "nvidia", lib, "bin")
            if os.path.isdir(d):
                os.add_dll_directory(d)
                os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--language", default="vi")
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    a = ap.parse_args()
    add_cuda_dlls()
    from faster_whisper import WhisperModel

    wav = os.path.join(tempfile.mkdtemp(), "a.wav")
    K.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vn", "-ac", "1", "-ar", "16000", wav], "tach tieng")

    def go(device):
        ct = "int8_float16" if device == "cuda" else "int8"  # GTX 1660: int8_float16 ~2x nhanh hon float16
        print(f"  model {a.model} on {device}/{ct} ...")
        m = WhisperModel(a.model, device=device, compute_type=ct)
        segs, _ = m.transcribe(wav, language=a.language, word_timestamps=True, vad_filter=True, condition_on_previous_text=False)
        return list(segs)

    segs = None
    if a.device in ("auto", "cuda"):
        try:
            segs = go("cuda")
        except Exception as e:  # missing cublas/cudnn -> CPU
            if a.device == "cuda":
                K.die(f"CUDA loi: {e}")
            print(f"  GPU khong dung duoc ({str(e)[:80]}...), chuyen CPU")
    if segs is None:
        segs = go("cpu")

    out = {"video": os.path.abspath(a.video), "segments": [], "words": []}
    for s in segs:
        out["segments"].append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()})
        for w in s.words or []:
            out["words"].append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "p": round(w.probability, 3)})
        print(f"  [{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
    K.write_json(a.out, out)
    print(f"\n  {len(out['words'])} tu -> {a.out}")


if __name__ == "__main__":
    main()
