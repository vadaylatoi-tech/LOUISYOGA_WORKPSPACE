# -*- coding: utf-8 -*-
"""Ham dung chung cho skill nns-add-sfx.

Tat ca text xuat ra la tieng Viet KHONG DAU (ASCII) de khong bao gio vo tren
console Windows cp1252. File .md moi co dau day du.

KHONG import bat ky module nao ngoai stdlib + numpy.
KHONG dung duong dan tuyet doi cua may nao ca: moi thu suy ra tu __file__.
"""
from __future__ import print_function

import io
import json
import os
import re
import subprocess
import sys

SR = 48000          # sample rate lam viec, co dinh
HOP = 0.005         # 5 ms cho envelope cua file SFX
HOP_SPEECH = 0.010  # 10 ms cho envelope cua loi noi

# thu muc goc cua skill = cha cua scripts/
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLED_SFX = os.path.join(SKILL_ROOT, "assets", "sfx")

SFX_EXT = (".mp3", ".wav")
SFX_DIRNAMES = ("sound-effects", "sound_effects", "sfx", "sounds", "audio-sfx")


# ---------------------------------------------------------------- io / process

def setup_stdout():
    """Bat buoc goi o dau moi script: console Windows mac dinh cp1252 se crash."""
    for stream in ("stdout", "stderr"):
        s = getattr(sys, stream, None)
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            try:
                setattr(sys, stream, io.TextIOWrapper(s.buffer, encoding="utf-8",
                                                      errors="replace"))
            except Exception:
                pass


def die(msg, code=1):
    """Dung han, bao ro. Khong bao gio im lang."""
    print("")
    print("!! LOI: " + str(msg))
    sys.stdout.flush()
    sys.exit(code)


def die_block(head, lines, recheck_cmd=None, code=1):
    """Dung han + in KHOI HUONG DAN dung dinh dang hop dong muc 4.2.

    Dung cho cac buoc sau preflight, de nguoi dung doc y nguyen mot huong dan
    du ho goi truc tiep probe/plan/apply ma bo qua preflight.
    """
    line = "=" * 60
    print("")
    print("  " + line)
    print("    THIEU 1 THU. LAM THEO CAC BUOC SAU ROI CHAY LAI.")
    print("  " + line)
    print("")
    print("  1) " + str(head))
    for s in lines:
        print("     " + s)
    print("")
    if recheck_cmd:
        print("  Sau khi lam xong, chay lai lenh nay de kiem:")
        print("      " + recheck_cmd)
        print("")
    sys.stdout.flush()
    sys.exit(code)


def require_numpy(video=None):
    """Cac buoc lam viec deu can numpy de doc mau am thanh.

    Thieu -> in khoi huong dan + lenh cai, exit 1. KHONG de traceback lot ra
    ngoai (nguoi dung khong doc duoc traceback).
    """
    try:
        import numpy  # noqa: F401
        return
    except ImportError:
        pass
    recheck = None
    if video:
        recheck = "python scripts/preflight.py --video \"%s\"" % video
    die_block("Chua cai thu vien Python numpy (de doc va tron am thanh)",
              ["Buoc nay can numpy moi doc duoc mau am thanh.",
               "Chay lenh nay:",
               "    pip install numpy",
               "Neu may co nhieu ban Python, cai dung ban dang chay script nay:",
               "    python -m pip install numpy",
               "Kiem lai bang:",
               "    python -c \"import numpy; print(numpy.__version__)\""],
              recheck)


def run(cmd, capture=True, check=True, what=None):
    """Chay tien trinh con. Loi -> die() voi thong bao doc duoc."""
    try:
        p = subprocess.run(cmd, capture_output=capture)
    except OSError as ex:
        die("khong chay duoc '%s' (%s). %s" % (cmd[0], ex, what or ""))
    if check and p.returncode != 0:
        err = (p.stderr or b"").decode("utf-8", "replace").strip()
        die("lenh that bai (ma %d): %s\n%s\n%s"
            % (p.returncode, " ".join(cmd[:6]) + " ...", err[-1500:], what or ""))
    return p


def disp(p):
    """Duong dan de in ra: mot loai dau gach cho de doc."""
    return str(p).replace("\\", "/") if p else str(p)


def read_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False))


# ------------------------------------------------------------------ tool check

def tool_version(exe):
    """Tra ve chuoi version, hoac None neu khong co exe."""
    try:
        p = subprocess.run([exe, "-version"], capture_output=True)
    except OSError:
        return None
    if p.returncode != 0:
        return None
    first = (p.stdout or b"").decode("utf-8", "replace").splitlines()
    if not first:
        return None
    m = re.search(r"version\s+(\S+)", first[0])
    return m.group(1) if m else first[0][:40]


def ffmpeg_has(kind, name):
    """kind: 'filters' | 'muxers'. Kiem tra ffmpeg build co thanh phan do khong."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-" + kind], capture_output=True)
    txt = (p.stdout or b"").decode("utf-8", "replace")
    return re.search(r"^\s*\S*\s+%s\s" % re.escape(name), txt, re.M) is not None


# ------------------------------------------------------------------- ffprobe

def probe_media(path):
    """Doc thong so video/audio. Tra ve dict. Loi -> die()."""
    if not os.path.isfile(path):
        die("khong tim thay file: %s" % path)
    p = run(["ffprobe", "-v", "error", "-print_format", "json",
             "-show_format", "-show_streams", path],
            what="ffprobe khong doc duoc file nay, co the khong phai video.")
    try:
        d = json.loads(p.stdout.decode("utf-8", "replace"))
    except ValueError:
        die("ffprobe tra ve du lieu khong doc duoc cho: %s" % path)
    out = {"path": os.path.abspath(path), "has_video": False, "has_audio": False,
           "width": 0, "height": 0, "fps": 0.0, "nb_frames": 0,
           "vcodec": "", "acodec": "", "sample_rate": 0, "channels": 0,
           "duration": 0.0, "adur": 0.0}
    try:
        out["duration"] = float(d.get("format", {}).get("duration", 0.0) or 0.0)
    except (TypeError, ValueError):
        out["duration"] = 0.0
    for s in d.get("streams", []):
        if s.get("codec_type") == "video" and not out["has_video"]:
            out["has_video"] = True
            out["vcodec"] = s.get("codec_name", "")
            out["width"] = int(s.get("width", 0) or 0)
            out["height"] = int(s.get("height", 0) or 0)
            rate = s.get("avg_frame_rate") or s.get("r_frame_rate") or "0/1"
            try:
                num, den = rate.split("/")
                out["fps"] = (float(num) / float(den)) if float(den) else 0.0
            except (ValueError, ZeroDivisionError):
                out["fps"] = 0.0
            try:
                out["nb_frames"] = int(s.get("nb_frames", 0) or 0)
            except (TypeError, ValueError):
                out["nb_frames"] = 0
        elif s.get("codec_type") == "audio" and not out["has_audio"]:
            out["has_audio"] = True
            out["acodec"] = s.get("codec_name", "")
            try:
                out["sample_rate"] = int(s.get("sample_rate", 0) or 0)
            except (TypeError, ValueError):
                out["sample_rate"] = 0
            try:
                out["channels"] = int(s.get("channels", 0) or 0)
            except (TypeError, ValueError):
                out["channels"] = 0
            try:
                out["adur"] = float(s.get("duration", 0.0) or 0.0)
            except (TypeError, ValueError):
                out["adur"] = 0.0
    return out


def count_frames(path, stream="v:0", decode=False):
    """Dem frame THAT - khong tin nb_frames trong header.

    decode=False (mac dinh): dem GOI TIN (-count_packets). Voi h264 trong mp4 thi
      1 goi = 1 frame, va do that tren video 215s: 6463 goi == 6463 frame giai ma,
      nhung nhanh hon 400 lan (0.09s so voi 36.5s). Ket hop voi stream_hash() -
      cai da chung minh tung bit - thi the la du.
    decode=True: giai ma that (-count_frames), cham, dung khi muon chac tuyet doi.
    """
    if decode:
        args = ["-count_frames", "-show_entries", "stream=nb_read_frames"]
    else:
        args = ["-count_packets", "-show_entries", "stream=nb_read_packets"]
    p = run(["ffprobe", "-v", "error", "-select_streams", stream] + args
            + ["-of", "default=nw=1:nk=1", path])
    txt = p.stdout.decode("utf-8", "replace").strip().splitlines()
    for line in txt:
        line = line.strip()
        if line.isdigit():
            return int(line)
    return -1


def stream_hash(path, stream="v:0"):
    """MD5 cua goi tin nen (khong giai ma). -c copy giu nguyen -> hash trung nhau."""
    p = run(["ffmpeg", "-v", "error", "-nostats", "-i", path,
             "-map", "0:" + stream, "-c", "copy",
             "-f", "streamhash", "-hash", "md5", "-"], check=False)
    txt = p.stdout.decode("utf-8", "replace").strip()
    for line in txt.splitlines():
        parts = line.strip().split("=")
        if len(parts) == 2:
            return parts[1].strip()
    return None


# ------------------------------------------------------------------- loudness

_EBUR = {
    "I": re.compile(r"^\s*I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", re.M),
    "LRA": re.compile(r"^\s*LRA:\s*(-?\d+(?:\.\d+)?)\s*LU", re.M),
    "TP": re.compile(r"^\s*Peak:\s*(-?(?:inf|\d+(?:\.\d+)?))\s*dBFS", re.M),
}


def measure_loudness(path):
    """Do I / LRA / true peak bang ebur128.

    QUAN TRONG: goi ham nay tren FILE DA MA HOA cuoi cung (AAC), khong phai WAV
    trung gian - AAC co the vuot true-peak so voi WAV.
    """
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-map", "0:a:0", "-af", "ebur128=peak=true:framelog=quiet",
             "-f", "null", "-"],
            what="khong do duoc do to (loudness) cua: %s" % path)
    txt = (p.stderr or b"").decode("utf-8", "replace")
    out = {}
    for k, rx in _EBUR.items():
        m = rx.search(txt)
        if not m:
            die("khong doc duoc %s tu ebur128 cho %s.\nDau ra ffmpeg:\n%s"
                % (k, path, txt[-1200:]))
        v = m.group(1)
        out[k] = float("-inf") if v == "-inf" else float(v)
    return out


# ------------------------------------------------------------- decode / envelope

def decode_audio(path, channels=1, sr=SR, start=None, dur=None):
    """Giai ma ra numpy float32. channels 1 = mono, 2 = stereo (N,2)."""
    import numpy as np
    cmd = ["ffmpeg", "-v", "error"]
    if start:
        cmd += ["-ss", "%.6f" % start]
    cmd += ["-i", path]
    if dur:
        cmd += ["-t", "%.6f" % dur]
    cmd += ["-map", "0:a:0", "-f", "f32le", "-ar", str(sr), "-ac", str(channels), "-"]
    p = run(cmd, what="khong giai ma duoc audio cua: %s" % path)
    a = np.frombuffer(p.stdout, dtype="<f4")
    if channels == 2:
        a = a[:(len(a) // 2) * 2].reshape(-1, 2)
    return a.copy()


def env_db(x, hop=HOP, sr=SR):
    """Envelope RMS theo dB, moi khung `hop` giay. x = mono float."""
    import numpy as np
    h = max(1, int(round(hop * sr)))
    n = len(x) // h
    if n == 0:
        return np.zeros(0)
    f = np.asarray(x[:n * h], dtype=np.float64).reshape(n, h)
    return 20.0 * np.log10(np.maximum(np.sqrt((f * f).mean(axis=1)), 1e-10))


def find_lag(a, b, max_lag=4800, avoid=None, sr=SR, win=4.0):
    """Do lech MAU NGUYEN giua 2 tin hieu mono (b tre hon a bao nhieu mau).

    Bat buoc phai co: ffmpeg ma hoa lai AAC thi bo giai ma tra ve tin hieu
    LECH VAI TRAM MAU so voi file goc (do that: 239 mau). Neu tru truc tiep
    khong can chinh thi tuong quan chi 0.25 va phan du cao -15 dB - phep do
    thanh vo nghia. Sau khi chinh: tuong quan 0.9995, phan du -67 dB.
    """
    import numpy as np
    n = min(len(a), len(b))
    w = int(min(win * sr, max(sr, n // 3)))
    if n <= 2 * max_lag + w:
        return 0
    avoid = avoid or []
    best_s = None
    for frac in (0.5, 0.35, 0.65, 0.2, 0.8, 0.05):
        s = int(frac * (n - w - max_lag)) + max_lag
        t0, t1 = s / float(sr), (s + w) / float(sr)
        if any(not (t1 < x0 or t0 > x1) for x0, x1 in avoid):
            continue
        best_s = s
        break
    if best_s is None:
        best_s = max_lag + (n - w - 2 * max_lag) // 2
    s = best_s
    x = np.asarray(a[s:s + w], dtype=np.float64)
    x = x - x.mean()
    lo, hi = max(0, s - max_lag), min(n, s + w + max_lag)
    y = np.asarray(b[lo:hi], dtype=np.float64)
    y = y - y.mean()
    if x.std() < 1e-9 or y.std() < 1e-9:
        return 0
    L = 1
    while L < len(x) + len(y):
        L *= 2
    cc = np.fft.irfft(np.fft.rfft(y, L) * np.conj(np.fft.rfft(x, L)), L)
    k = int(np.argmax(cc[:2 * max_lag + 1]))
    return k - (s - lo)


def db(v):
    import numpy as np
    return 20.0 * np.log10(max(float(v), 1e-10)) if not isinstance(v, np.ndarray) \
        else 20.0 * np.log10(np.maximum(v, 1e-10))


# ---------------------------------------------------- phan tich 1 file SFX

# nguong phan loai riser (do that tren thu vien 86 file, xem references/)
RISER_MIN_SPAN = 1.00
RISER_MIN_FRAC = 0.65
RISER_MIN_RISE = 8.0
RISER_MIN_DECAY = 5.0
RISER_MIN_CORR = 0.45


def analyse_sfx(path):
    """Do onset / burst_end / climax / riser cho MOT file SFX.

    Tra ve dict, hoac dict co usable=False + reason neu file khong dung duoc.
    Khong bao gio nem exception ra ngoai vi mot file xau khong duoc pha ca me.
    """
    import numpy as np
    try:
        x = decode_audio(path, channels=1)
    except SystemExit:
        return {"usable": False, "reason": "ffmpeg khong giai ma duoc"}
    if len(x) < int(0.02 * SR):
        return {"usable": False, "reason": "ngan hon 20 ms"}
    x = x.astype(np.float64)
    peak_lin = float(np.abs(x).max())
    if peak_lin <= 0.0:
        return {"usable": False, "reason": "file im lang hoan toan (peak = 0)"}
    e = env_db(x, HOP)
    if len(e) < 3:
        return {"usable": False, "reason": "qua ngan de do envelope"}
    pk = float(e.max())
    floor = float(np.percentile(e, 5))
    # nguong onset: 30 dB duoi dinh, nhung KHONG BAO GIO cao hon dinh - 6 dB
    # (file da nen manh nhu temple-bell.mp3 co floor + 8 > peak -> se khong tim ra gi)
    thr = max(pk - 30.0, min(floor + 8.0, pk - 6.0), -70.0)
    idx = np.nonzero(e > thr)[0]
    if len(idx) == 0:
        return {"usable": False, "reason": "khong tim ra diem bat dau tieng"}
    i0 = int(idx[0])
    back = max(thr - 12.0, min(floor + 3.0, thr - 3.0))
    while i0 > 0 and e[i0 - 1] > back:
        i0 -= 1
    onset = i0 * HOP

    # burst_end: cho im >= 120 ms dau tien sau onset.
    # Day la cach bat file "danh 2 lan" (whoosh.wav: hit 0.14-0.41, im, hit 1.40).
    lo = thr - 6.0
    need = int(round(0.120 / HOP))
    n = len(e)
    burst_end = n * HOP
    run_len = 0
    for j in range(i0, n):
        if e[j] < lo:
            run_len += 1
            if run_len >= need:
                burst_end = (j - run_len + 1) * HOP
                break
        else:
            run_len = 0
    if burst_end <= onset:
        burst_end = min(n * HOP, onset + HOP)

    ic = int(np.argmax(e))
    climax = ic * HOP
    span = burst_end - onset

    riser = False
    frac = -1.0
    rise = 0.0
    decay = 0.0
    corr = 0.0
    if span >= RISER_MIN_SPAN and onset < climax < burst_end:
        frac = (climax - onset) / span
        head_n = max(1, int(round(0.20 * span / HOP)))
        rise = pk - float(e[i0:i0 + head_n].mean())
        tail = e[ic + 1:min(n, ic + 1 + int(round(0.40 / HOP)))]
        decay = pk - float(tail.mean()) if len(tail) else 99.0
        seg = e[i0:ic + 1]
        if len(seg) >= 4 and float(seg.std()) > 1e-6:
            t = np.arange(len(seg), dtype=np.float64)
            corr = float(np.corrcoef(t, seg)[0, 1])
        riser = (frac >= RISER_MIN_FRAC and rise >= RISER_MIN_RISE
                 and decay >= RISER_MIN_DECAY and corr >= RISER_MIN_CORR)

    if riser:
        rec_dur = round(climax - onset + 0.05, 3)
        rec_align = "end"
    else:
        rec_dur = round(min(span, 2.50), 3)
        rec_align = "start"
    rec_dur = max(rec_dur, 0.05)

    seg_pk = float(np.abs(x[int(round(onset * SR)):
                            int(round((onset + rec_dur) * SR))]).max()) \
        if rec_dur > 0 else 0.0

    return {
        "usable": seg_pk > 0.0,
        "reason": "" if seg_pk > 0.0 else "cat theo onset ra doan im (peak = 0)",
        "dur": round(len(x) / float(SR), 3),
        "peak_dbfs": round(db(peak_lin), 2),
        "onset": round(onset, 3),
        "burst_end": round(burst_end, 3),
        "climax": round(climax, 3),
        "riser": bool(riser),
        "riser_frac": round(frac, 3),
        "riser_rise_db": round(rise, 2),
        "riser_decay_db": round(min(decay, 99.0), 2),
        "riser_corr": round(corr, 3),
        "rec_dur": rec_dur,
        "rec_align": rec_align,
        "seg_peak_dbfs": round(db(seg_pk), 2),
    }


# ------------------------------------------------------- vai (role) cua file SFX

# tra tu khoa theo TEN FILE -> vai. Xet theo thu tu, khop dau tien thang.
ROLE_KEYS = [
    ("riser",      ("riser", "build-up", "buildup", "build_up", "sweep", "rise")),
    ("transition", ("whoosh", "swoosh", "swish", "transition", "fast-forward",
                    "take-off", "weee", "glitch")),
    ("impact",     ("punch", "impact", "hit", "boom", "slam", "thud", "dun-dun")),
    ("confirm",    ("correct", "arcade-bonus", "ta-da", "tada", "new-item",
                    "ka-ching", "success", "level-up", "money", "buy")),
    ("negative",   ("error", "fail", "wrong", "buzzer", "shock", "crickets")),
    ("accent",     ("ting", "ding", "chime", "bell", "click", "pop", "bubble",
                    "camera", "snap", "tick", "beep", "digital-counting")),
    ("bed",        ("keyboard", "typing", "heartbeat", "counter", "crowd",
                    "ambience", "rain", "foley")),
]

# muc dinh (peak dBFS) mong muon cho tung vai SAU khi da nhan gain.
# Do doi chieu tu 4 cue-sheet that da duyet trong project nay.
ROLE_TARGET_PEAK = {
    "impact": -12.0,
    "transition": -21.0,
    "accent": -22.0,
    "riser": -24.0,
    "confirm": -20.0,
    "negative": -19.0,
    "bed": -34.0,
    "other": -21.0,
}


# do dai TOI DA cua mot cue theo vai. File dai hon se bi cat bot.
# Voi align="end" (riser) thi cat tu DAU, giu nguyen doan ket -> van dung dinh.
ROLE_MAX_DUR = {
    "impact": 0.70,
    "transition": 0.70,
    "accent": 0.80,
    "riser": 2.50,
    "confirm": 1.30,
    "negative": 1.10,
    "bed": 4.00,
    "other": 1.20,
}

# uu tien ten file trong tung vai (khop dau tien duoc chon truoc)
ROLE_PREFER = {
    "transition": ("whoosh", "swoosh", "swish"),
    "accent": ("ting", "ding", "pop", "click", "chime", "bell"),
    "impact": ("punch", "impact", "hit"),
    "confirm": ("correct", "arcade-bonus", "new-item", "ta-da"),
    "negative": ("error", "buzzer", "wrong", "fail"),
    "riser": ("riser", "build"),
}


def prefer_rank(role, name):
    """0 = dung y nhat. Dung de sap xep pool trong Picker."""
    low = os.path.basename(name).lower()
    keys = ROLE_PREFER.get(role, ())
    for i, k in enumerate(keys):
        if k in low:
            return i
    return len(keys) + 1


def role_of(name, tags=None, is_riser=False):
    """Suy ra vai tu ten file (+ tag trong library.json neu co)."""
    if is_riser:
        return "riser"
    low = os.path.basename(name).lower()
    for role, keys in ROLE_KEYS:
        for k in keys:
            if k in low:
                return role
    for t in (tags or []):
        tl = str(t).lower()
        for role, keys in ROLE_KEYS:
            if tl in keys or tl == role:
                return role
    return "other"


# ------------------------------------------------- tim thu vien SFX (tim mem)

def _collect_sfx(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith(SFX_EXT):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def _sfx_from_resources(resources):
    """Lay thu vien SFX tu --resources. Tra ve (dir, files, nhan) hoac None.

    Tim DE QUY, chap nhan nhieu ten thu muc: sound-effects/ sfx/ audio/sfx/ ...
    Neu --resources tro thang vao thu muc chua mp3/wav thi cung nhan.
    """
    if not os.path.isdir(resources):
        return None
    hits = []
    for dirpath, dirnames, _fn in os.walk(resources):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        if os.path.basename(dirpath).lower() in SFX_DIRNAMES:
            hits.append(dirpath)
    best = None
    best_files = []
    for h in hits:
        fs = _collect_sfx(h)
        if len(fs) > len(best_files):
            best, best_files = h, fs
    if best_files:
        return best, best_files, "--resources"
    direct = _collect_sfx(resources)
    if direct:
        return (os.path.abspath(resources), direct, "--resources (thu muc phang)")
    return None


def _sep_of(path):
    """Dau gach ma nguoi dung dang dung trong duong dan do ('/' hay '\\')."""
    if "\\" in path and "/" not in path:
        return "\\"
    return "/"


def resources_problem(resources):
    """--resources nguoi dung dua co dung duoc khong?

    Tra ve None neu tot (hoac neu nguoi dung khong dua --resources),
    hoac ("notdir"|"empty", duong-dan) neu dua ma khong dung duoc.

    LUAT (hop dong muc 4.2 + "khong duoc tu thay the"): nguoi dung DA CHI RO
    --resources thi khong duoc am tham quay ve assets/sfx kem san. Phai bao
    THIEU + chi cach lam roi DUNG.
    """
    if not resources:
        return None
    if not os.path.isdir(resources):
        return ("notdir", resources)
    if _sfx_from_resources(resources) is None:
        return ("empty", resources)
    return None


def n_bundled_sfx():
    """Dem so file SFX kem san trong skill."""
    if not os.path.isdir(BUNDLED_SFX):
        return 0
    return len(_collect_sfx(BUNDLED_SFX))


def resources_guidance(kind, path):
    """Khoi huong dan cho truong hop --resources khong dung duoc.

    Tra ve (tieu de, [cac dong]) - dung chung cho preflight va cac buoc sau,
    de nguoi dung luon doc cung mot huong dan.
    """
    n = n_bundled_sfx()
    if kind == "notdir":
        head = "Duong dan --resources khong ton tai (hoac khong phai thu muc)"
        first = ["Duong dan ban dua: %s" % path,
                 "Khong tim thay thu muc nay tren may."]
    else:
        head = "Thu muc --resources khong co file hieu ung am thanh (SFX) nao"
        first = ["Thu muc ban dua: %s" % path,
                 "Da tim DE QUY trong do, khong thay file .mp3/.wav nao.",
                 "Skill KHONG tu doi sang thu vien khac vi ban da chi ro --resources."]
    lines = list(first)
    lines += [
        "",
        "Chon 1 trong 2 cach:",
        "",
        "Cach A - dung %d file SFX kem san trong skill (nhanh nhat):" % n,
        "    BO HAN tham so --resources roi chay lai. Vi du:",
        "        python scripts/preflight.py --video \"<video>\"",
        "    (skill co san thu muc assets/sfx/ trong chinh no)",
    ]
    if n == 0:
        lines += [
            "    CANH BAO: hien assets/sfx/ dang RONG hoac bi mat khi copy skill.",
            "    -> copy lai ca thu muc skill, giu nguyen thu muc assets/.",
        ]
    lines += [
        "",
        "Cach B - dung thu vien SFX rieng cua ban:",
        "    1. Tao thu muc con ten sound-effects/ ben trong thu muc ban dua:",
        # giu nguyen kieu dau gach cua duong dan nguoi dung dua, khong tron 2 kieu
        "           %s%ssound-effects%s" % (path.rstrip("/\\"), _sep_of(path),
                                           _sep_of(path)),
        "       (ten khac cung duoc: sfx/  hoac  audio/sfx/)",
        "    2. Copy vao do cac file .mp3 hoac .wav - can it nhat 5-10 file kieu:",
        "       whoosh, swoosh, pop, ting, punch, riser, correct, buzzer",
        "       Tai mien phi (khong can dang ky): pixabay.com/sound-effects",
        "       Hoac: freesound.org  |  mixkit.co/free-sound-effects",
        "    3. Goi lai voi:  --resources \"%s\"" % path,
    ]
    return head, lines


def find_sfx_library(resources=None):
    """Tim thu vien SFX. Tra ve (dir, [duong dan file], nhan nguon, ghi chu).

    Thu tu uu tien theo hop dong muc 4.3:
      1. --resources nguoi dung dua
      2. assets/sfx kem san trong skill

    LUU Y: neu --resources co dua ma khong dung duoc thi day KHONG phai truong
    hop de fallback am tham - nguoi goi phai kiem resources_problem() truoc va
    DUNG lai. Ham nay van tra ve assets/sfx de cac cho chi can "mot thu muc nao
    do" khong bi vo, nhung notes se noi ro.
    """
    notes = []
    if resources:
        got = None
        if not os.path.isdir(resources):
            notes.append("--resources khong phai thu muc: %s" % resources)
        else:
            got = _sfx_from_resources(resources)
            if got is None:
                notes.append("trong --resources khong co file .mp3/.wav nao duoi "
                             "sound-effects/ | sfx/ | audio/sfx/")
        if got is not None:
            d, fs, src = got
            return d, fs, src, notes
    if os.path.isdir(BUNDLED_SFX):
        fs = _collect_sfx(BUNDLED_SFX)
        if fs:
            return BUNDLED_SFX, fs, "assets/sfx kem san trong skill", notes
    return None, [], "khong co", notes


def load_library_tags(sfx_dir):
    """Doc library.json canh thu vien SFX neu co (khong bat buoc)."""
    if not sfx_dir:
        return {}
    p = os.path.join(sfx_dir, "library.json")
    if not os.path.isfile(p):
        return {}
    try:
        d = read_json(p)
    except Exception:
        return {}
    out = {}
    if isinstance(d, list):
        for it in d:
            if isinstance(it, dict) and it.get("file"):
                out[str(it["file"])] = it.get("tags") or []
    return out


# ------------------------------------------------------- bang PASS / THIEU

class Report(object):
    """Bang trang thai + danh sach thu thieu, dung chung cho preflight."""

    def __init__(self):
        self.rows = []
        self.missing = []

    def ok(self, label, detail):
        self.rows.append(("[OK]", label, detail))

    def warn(self, label, detail):
        self.rows.append(("[LUU Y]", label, detail))

    def fail(self, label, detail, title, steps):
        self.rows.append(("[THIEU]", label, detail))
        self.missing.append((title, list(steps)))

    def print_table(self):
        w = max([len(r[1]) for r in self.rows] + [10])
        for mark, label, detail in self.rows:
            print("  %-8s %-*s  %s" % (mark, w, label, detail))

    def finish(self, recheck_cmd):
        """In ket luan. Neu thieu -> in khoi huong dan roi exit 1."""
        line = "=" * 60
        print("")
        if not self.missing:
            print("  " + line)
            print("    DAY DU. Chay tiep duoc.")
            print("  " + line)
            return
        print("  " + line)
        print("    THIEU %d THU. LAM THEO CAC BUOC SAU ROI CHAY LAI."
              % len(self.missing))
        print("  " + line)
        print("")
        for i, (title, steps) in enumerate(self.missing, 1):
            print("  %d) %s" % (i, title))
            for s in steps:
                print("     " + s)
            print("")
        print("  Sau khi lam xong, chay lai lenh nay de kiem:")
        print("      " + recheck_cmd)
        print("")
        sys.exit(1)


def add_common_args(ap, need_out=True):
    """Cac co dung chung theo hop dong muc 3."""
    ap.add_argument("--video", required=True, help="video dau vao (bat buoc)")
    ap.add_argument("--out", required=need_out, default=None,
                    help="file ket qua" + ("" if need_out else " (khong bat buoc)"))
    ap.add_argument("--resources", default=None,
                    help="thu muc tai nguyen (chua sound-effects/ hoac sfx/)")
    ap.add_argument("--dry-run", action="store_true",
                    help="chi lap ke hoach va in ra, KHONG xuat file")
    return ap
