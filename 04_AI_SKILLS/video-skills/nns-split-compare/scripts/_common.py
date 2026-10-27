# -*- coding: utf-8 -*-
"""nns-split-compare — ham dung chung.

Chi dung stdlib + Pillow. Pillow import LAZY de preflight con bao loi tu te.
Moi duong dan deu di qua -i cua ffmpeg, KHONG bao gio nhet vao chuoi filter
(duong dan Windows co dau ':' va '\' se lam vo filtergraph).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from fractions import Fraction

SKILL_NAME = "nns-split-compare"
PLAN_VERSION = 1

# ---------------------------------------------------------------- layout
# Do tu anh mau: 2 khung 9:16 canh nhau, nhan tren, pill duoi, badge VS giua.
W, H = 1080, 1920
FPS = 30

PANEL_W, PANEL_H = 496, 882          # 496 * 1920/1080 = 881.8 -> 882 (giu dung 9:16)
LEFT_X, RIGHT_X = 24, 560            # 24 + 496 + 40 + 496 + 24 = 1080
PANEL_Y = 540
RADIUS = 28

LABEL_CY = 450                       # tam dong chu nhan
LABEL_SIZE = 78
PILL_Y = 1452
PILL_H = 62
PILL_TEXT = 34
VS_R = 46
VS_TEXT = 34
AI_BADGE_H = 48
AI_TEXT = 28

BG = (10, 11, 13, 255)
GRID = (22, 25, 30, 255)
GRID_STEP = 60

YELLOW = (245, 166, 35, 255)
WHITE = (255, 255, 255, 255)
DIM_BORDER = (46, 49, 56, 255)
PILL_GREY_BG = (36, 38, 43, 255)
PILL_GREY_FG = (185, 190, 199, 255)
PILL_YEL_FG = (16, 17, 18, 255)
VS_BG = (38, 40, 46, 255)
VS_BORDER = (58, 61, 69, 255)

DIM_BRIGHT = 0.32                    # khung dang dung hinh toi con 32%
DIM_SAT = 0.35
DIM_UI_ALPHA = 0.45                  # nhan + pill cua ben khong chay mo bot

LINE = "-" * 58


# ---------------------------------------------------------------- io
def setup_io():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def die(msg, code=1):
    print("", flush=True)
    print("[LOI] " + str(msg), file=sys.stderr, flush=True)
    sys.exit(code)


def head(title):
    print("")
    print("  %s — %s" % (SKILL_NAME, title))
    print("  " + LINE)


def tool(name):
    return shutil.which(name)


def need_tool(name):
    p = tool(name)
    if not p:
        die("Khong tim thay '%s' trong PATH.\n"
            "       Chay truoc:  python scripts/preflight.py --video \"<video>\"" % name)
    return p


def run(cmd, check=True, capture=True):
    p = subprocess.run(cmd, capture_output=capture, text=True,
                       encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        die("Lenh that bai (ma %d):\n  %s\n%s"
            % (p.returncode, " ".join(str(c) for c in cmd), (p.stderr or "")[-3000:]))
    return p


# ---------------------------------------------------------------- ffprobe
def probe(path):
    """Tra ve dict thong tin video: w,h,fps,dur,nframes,has_audio,ar,ac."""
    need_tool("ffprobe")
    if not os.path.isfile(path):
        die("Khong thay file: %s" % path)
    p = run(["ffprobe", "-v", "error", "-print_format", "json",
             "-show_streams", "-show_format", path])
    d = json.loads(p.stdout)
    v = a = None
    for s in d.get("streams", []):
        if s.get("codec_type") == "video" and v is None:
            v = s
        elif s.get("codec_type") == "audio" and a is None:
            a = s
    if v is None:
        die("File khong co stream hinh: %s" % path)

    rfr = Fraction(v.get("r_frame_rate", "0/1") or "0/1")
    afr = Fraction(v.get("avg_frame_rate", "0/1") or "0/1")
    dur = float(d.get("format", {}).get("duration") or 0.0)

    n = count_frames(path)
    fps = float(rfr) if rfr else (float(afr) if afr else FPS)
    return {
        "path": path,
        "w": int(v["width"]), "h": int(v["height"]),
        "fps": fps, "r_frame_rate": str(rfr), "avg_frame_rate": str(afr),
        "cfr": (rfr == afr and rfr != 0),
        "dur": dur, "nframes": n,
        "dur_frames": (n / fps) if fps else dur,
        "codec": v.get("codec_name", "?"),
        "has_audio": a is not None,
        "ar": int(a["sample_rate"]) if a and a.get("sample_rate") else 0,
        "ac": int(a["channels"]) if a and a.get("channels") else 0,
        "pix_fmt": v.get("pix_fmt", "?"),
    }


def count_frames(path):
    """Dem packet hinh — khong tin metadata nb_frames."""
    p = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-count_packets", "-show_entries", "stream=nb_read_packets",
             "-print_format", "csv=p=0", path])
    try:
        return int((p.stdout or "0").strip().splitlines()[0])
    except Exception:
        return 0


def audio_duration(path):
    p = run(["ffprobe", "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=duration", "-print_format", "csv=p=0", path],
            check=False)
    try:
        return float((p.stdout or "").strip().splitlines()[0])
    except Exception:
        return 0.0


# ---------------------------------------------------------------- font
def font_dir(explicit=None):
    """Tim thu muc font Be Vietnam Pro. Uu tien --resources, roi shared-sources."""
    cands = []
    if explicit:
        cands += [os.path.join(explicit, "Font", "Be_Vietnam_Pro"),
                  os.path.join(explicit, "Be_Vietnam_Pro"),
                  explicit]
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = here
    for _ in range(6):
        cands.append(os.path.join(root, "shared-sources", "Font", "Be_Vietnam_Pro"))
        root = os.path.dirname(root)
    cands.append(os.path.join(here, "assets", "font"))
    for c in cands:
        if os.path.isdir(c) and any(f.lower().endswith((".ttf", ".otf"))
                                    for f in os.listdir(c)):
            return c
    return None


def font_file(fdir, weight="Black"):
    if not fdir:
        return None
    for f in os.listdir(fdir):
        if f.lower().endswith((".ttf", ".otf")) and ("-%s." % weight).lower() in f.lower():
            return os.path.join(fdir, f)
    for f in sorted(os.listdir(fdir)):
        if f.lower().endswith((".ttf", ".otf")):
            return os.path.join(fdir, f)
    return None


# ---------------------------------------------------------------- misc
def vn_seconds(sec):
    """9.7667 -> '9,8 GIAY' (dau phay kieu Viet, 1 chu so thap phan)."""
    return ("%.1f" % round(sec + 1e-9, 1)).replace(".", ",")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def sidecar(out, suffix):
    base = os.path.splitext(os.path.abspath(out))[0]
    return base + suffix
