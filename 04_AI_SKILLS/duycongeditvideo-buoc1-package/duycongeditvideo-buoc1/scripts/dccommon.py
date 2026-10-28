# -*- coding: utf-8 -*-
"""Ham dung chung cho bo Duycongeditvideo_Buoc1 (cat ghep video dai -> video ngan).

Khong phu thuoc thu muc cai dat: moi script tu them thu muc scripts/ vao sys.path.
"""
import json
import os
import re
import shutil
import site
import subprocess
import sys
import unicodedata

import numpy as np


def setup_stdout():
    """Windows console mac dinh cp1252 -> in tieng Viet bi loi. Ep UTF-8."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def die(msg):
    print("\n  LOI: " + msg + "\n", file=sys.stderr)
    sys.exit(1)


def read_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(p, data, indent=1):
    os.makedirs(os.path.dirname(os.path.abspath(p)) or ".", exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    os.replace(tmp, p)


# ---------------------------------------------------------------- thoi gian
def ts2s(t):
    """'HH:MM:SS.mmm' | 'MM:SS.mmm' | so giay -> float giay."""
    if isinstance(t, (int, float)):
        return float(t)
    t = str(t).strip().replace(",", ".")
    parts = t.split(":")
    sec = 0.0
    for p in parts:
        sec = sec * 60 + float(p)
    return sec


def s2ts(s):
    s = max(0.0, float(s))
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    return "%02d:%02d:%06.3f" % (h, m, s % 60)


# ---------------------------------------------------------------- ffmpeg
def need_ffmpeg():
    for exe in ("ffmpeg", "ffprobe"):
        if not shutil.which(exe):
            die("khong tim thay %s. Cai ffmpeg roi mo terminal moi." % exe)


def probe(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,width,height,r_frame_rate:format=duration",
         "-of", "json", video], capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        die("ffprobe khong doc duoc: %s" % video)
    j = json.loads(out.stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    a = any(s["codec_type"] == "audio" for s in j["streams"])
    num, den = (v.get("r_frame_rate") or "30/1").split("/")
    return {"duration": float(j["format"]["duration"]), "width": v.get("width"),
            "height": v.get("height"), "fps": float(num) / float(den or 1), "audio": a}


def load_pcm(video, t0=0.0, dur=None, sr=16000):
    """Tieng mono float32 16 kHz cua [t0, t0+dur]."""
    cmd = ["ffmpeg", "-v", "error", "-ss", "%.3f" % max(0.0, t0)]
    if dur is not None:
        cmd += ["-t", "%.3f" % dur]
    cmd += ["-i", video, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def envelope_db(x, hop=160):
    """RMS dB moi 10 ms (hop=160 mau @16 kHz)."""
    n = len(x) // hop
    if n == 0:
        return np.zeros(0)
    r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(r)


def has_encoder(name):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"],
                         capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return name in out.stdout


# ---------------------------------------------------------------- whisper
def add_cuda_dll_dirs():
    """Windows: cuBLAS/cuDNN cai bang pip nam trong site-packages/nvidia/*/bin."""
    if os.name != "nt":
        return
    dirs = list(site.getsitepackages())
    try:
        dirs.append(site.getusersitepackages())
    except Exception:
        pass
    for sp in dirs:
        for sub in ("cublas", "cudnn", "cuda_nvrtc", "cuda_runtime"):
            d = os.path.join(sp, "nvidia", sub, "bin")
            if os.path.isdir(d):
                try:
                    os.add_dll_directory(d)
                except Exception:
                    pass
                os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")


def load_whisper(model="large-v3", device="auto", compute_type=None):
    """Tu chon GPU neu chay duoc, khong thi CPU. Tra ve (model, mo_ta)."""
    add_cuda_dll_dirs()
    try:
        from faster_whisper import WhisperModel
    except Exception as exc:
        die("chua cai faster-whisper (%s). Chay: pip install faster-whisper" % exc)
    tries = []
    if device in ("auto", "cuda"):
        tries.append(("cuda", compute_type or "int8_float16"))
    if device in ("auto", "cpu"):
        tries.append(("cpu", compute_type if device == "cpu" and compute_type else "int8"))
    last = None
    for dev, ct in tries:
        try:
            m = WhisperModel(model, device=dev, compute_type=ct)
            if dev == "cuda":
                # nap model thanh cong chua chac chay duoc (thieu cuBLAS chi lo khi encode)
                list(m.transcribe(np.zeros(16000, np.float32), language="vi")[0])
            return m, "%s/%s" % (dev, ct)
        except Exception as exc:
            last = exc
            print("  (khong dung duoc %s/%s: %s)" % (dev, ct, str(exc).splitlines()[0]))
    die("khong nap duoc Whisper: %s" % last)


def words_of(model, audio, offset=0.0, language="vi"):
    """Nhan dang word-level. audio: duong dan file hoac mang float32 16 kHz."""
    segs, _ = model.transcribe(audio, language=language, word_timestamps=True,
                               beam_size=5, vad_filter=False,
                               condition_on_previous_text=False)
    S, W = [], []
    for s in segs:
        ws = []
        for w in (s.words or []):
            t = w.word.strip()
            if not t:
                continue
            ws.append({"w": t, "start": round(offset + w.start, 3),
                       "end": round(offset + w.end, 3),
                       "p": round(float(getattr(w, "probability", 0) or 0), 3)})
        W += ws
        S.append({"start": round(offset + s.start, 3), "end": round(offset + s.end, 3),
                  "text": s.text.strip(), "words": ws})
    return S, W


# ---------------------------------------------------------------- chu
def norm(s):
    s = unicodedata.normalize("NFC", s.lower())
    return re.sub(r"[^\w\s]", "", s).strip()


def strip_accents(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").replace("đ", "d").replace("Đ", "D")


def loose(s):
    return strip_accents(norm(s))


def load_terms(path):
    """terms.json: [["mau regex", "thay bang"], ...] — sua ten rieng Whisper hay nghe sai."""
    if not path or not os.path.isfile(path):
        return []
    rules = read_json(path)
    # JSON doc "\b" (1 gach) thanh ky tu backspace -> regex khong bao gio khop (file mau cu bi vay).
    # Phai viet "\\b" trong JSON; file viet sai thi tu sua va bao.
    if any("\x08" in a for a, _ in rules):
        print("  CANH BAO %s: viet \"\\b\" 1 gach (JSON doc thanh backspace) -> tu sua thanh ranh gioi tu."
              " Nen sua file thanh \"\\\\b\"." % path)
        rules = [(a.replace("\x08", r"\b"), b) for a, b in rules]
    return [(re.compile(a, re.I), b) for a, b in rules]


def fix_text(s, terms):
    for rx, rep in terms:
        s = rx.sub(rep, s)
    return s


def here(*p):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *p)
