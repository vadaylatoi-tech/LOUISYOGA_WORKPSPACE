# -*- coding: utf-8 -*-
"""Kiem tra moi truong truoc khi dung skill. Chi in ASCII de khong vo font console."""
import shutil, subprocess, sys, os

TEN_GOI   = "TRON BO 12 SKILL"
PIP_CAN   = [('numpy', 'numpy', ''), ('faster_whisper', 'faster-whisper', ''), ('onnxruntime', 'onnxruntime', ''), ('PIL', 'Pillow', '')]          # [(ten_import, ten_pip, mo_ta)]
LENH_SAU  = ['python .claude\\skills\\nns-full-pass\\scripts\\preflight.py --video "raw.mp4"', '', 'Lan chay nns-auto-sub dau tien se tu tai model Whisper (~1.5GB).']         # cac dong in ra o buoc ke tiep

W = 74
def line(c="-"): print("  " + c * W)
def row(tag, ten, ghi=""):
    print("  [%-6s] %-22s %s" % (tag, ten, ghi))

thieu = []
pip_thieu = []

print()
line("=")
print("  KIEM TRA MOI TRUONG  --  " + TEN_GOI)
line("=")
print()

# --- python ---
v = sys.version_info
if v >= (3, 9):
    row("OK", "python", "%d.%d.%d" % (v.major, v.minor, v.micro))
else:
    row("THIEU", "python", "can >= 3.9, dang co %d.%d" % (v.major, v.minor))
    thieu.append("Cai Python 3.9 tro len: https://www.python.org/downloads/\n"
                 "      (khi cai NHO TICK o 'Add python.exe to PATH')")

# --- ffmpeg / ffprobe ---
for exe in ("ffmpeg", "ffprobe"):
    p = shutil.which(exe)
    if p:
        try:
            out = subprocess.run([exe, "-version"], capture_output=True, text=True,
                                 timeout=20).stdout.splitlines()[0]
            ver = out.split("version", 1)[1].strip().split()[0] if "version" in out else "?"
        except Exception:
            ver = "?"
        row("OK", exe, ver)
    else:
        row("THIEU", exe, "khong goi duoc tu terminal")
        if "ffmpeg" not in " ".join(thieu):
            thieu.append("Cai ffmpeg (co ca ffprobe di kem):\n"
                         "         Windows :  winget install Gyan.FFmpeg\n"
                         "         macOS   :  brew install ffmpeg\n"
                         "         Ubuntu  :  sudo apt install ffmpeg\n"
                         "      Cai xong PHAI MO LAI terminal thi PATH moi an.")

# --- thu vien python ---
for mod, pipname, mota in PIP_CAN:
    try:
        m = __import__(mod)
        ver = getattr(m, "__version__", "") or ""
        row("OK", pipname, (ver + "  " + mota).strip())
    except Exception:
        row("THIEU", pipname, mota)
        pip_thieu.append(pipname)

if pip_thieu:
    thieu.append("Cai thu vien python con thieu:\n"
                 "         pip install " + " ".join(pip_thieu))

print()
if not thieu:
    line("=")
    print("  DU HET. CHAY DUOC ROI.")
    line("=")
    print()
    print("  Buoc tiep theo:")
    for d in LENH_SAU:
        print("  " + d)
else:
    line("=")
    print("  CON %d VIEC PHAI LAM. LAM XONG CHAY LAI FILE NAY." % len(thieu))
    line("=")
    print()
    for i, t in enumerate(thieu, 1):
        print("  %d) %s" % (i, t))
        print()
print()
