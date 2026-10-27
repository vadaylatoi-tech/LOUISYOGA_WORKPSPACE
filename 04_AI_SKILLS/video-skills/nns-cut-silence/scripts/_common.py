# -*- coding: utf-8 -*-
"""nns-cut-silence — ham dung chung.

Chi dung stdlib + numpy. numpy duoc import LAZY (trong _np()) de preflight.py
con bao duoc loi "thieu numpy" mot cach tu te thay vi no ImportError.

Khong import bat ky module nao cua project. Khong dung duong dan tuyet doi.
"""
from __future__ import annotations

import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
from fractions import Fraction

SKILL_NAME = "nns-cut-silence"
PLAN_VERSION = 1

# Buoc cua duong bao nang luong. 10ms la con so da do tren file that:
# du min de bat khoang lang 0.2s, du tho de khong bi nhieu tung mau.
HOP_MS = 10

LINE = "═" * 60  # ═

# ---------------------------------------------------------------- io / process


def setup_io():
    """Console Windows mac dinh cp1252 va se crash khi in tieng Viet -> bat utf-8."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # Python cu / stream bi thay the
            pass


def die(msg, code=1):
    """Bao loi RO RANG roi thoat voi ma khac 0. Khong bao gio im lang."""
    print("", flush=True)
    print("[LOI] " + str(msg), file=sys.stderr, flush=True)
    sys.exit(code)


def tool(name):
    """Tra ve duong dan cong cu, hoac None."""
    return shutil.which(name)


def need_tool(name):
    p = tool(name)
    if not p:
        die(
            "Khong tim thay '%s' trong PATH.\n"
            "       Chay truoc:  python scripts/preflight.py --video \"<video>\"" % name
        )
    return p


def run(cmd, check=True, binary=False):
    """Chay lenh, tra ve (returncode, stdout, stderr)."""
    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
    )
    out = proc.stdout if binary else proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace")
    if check and proc.returncode != 0:
        die("Lenh that bai (ma %d):\n       %s\n%s" % (proc.returncode, " ".join(cmd), err.strip()))
    return proc.returncode, out, err


def read_json(path):
    with io.open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path, obj):
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)


def _np():
    try:
        import numpy  # noqa: F401
    except Exception:
        die(
            "Thieu thu vien numpy.\n"
            "       Chay:  pip install numpy\n"
            "       Roi kiem lai:  python scripts/preflight.py --video \"<video>\""
        )
    import numpy

    return numpy


# ---------------------------------------------------------------- ffprobe


def ffmpeg_major():
    """So phien ban lon cua ffmpeg (7 cho '7.0.2'). 0 neu khong doc duoc."""
    exe = need_tool("ffmpeg")
    try:
        out = subprocess.run(
            [exe, "-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
        ).stdout.decode("utf-8", "replace")
        m = re.search(r"version\s+n?(\d+)", out)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def frame_signatures(path, frames, size=64):
    """Lay 'chu ky hinh' (anh xam size x size) cua DUNG nhung frame duoc yeu cau.

    Dung select=eq(n\\,N) trong MOT lan decode duy nhat — TUYET DOI khong dung
    -ss, vi fast seek nhay sang frame khac va se lam phep do lech (xem
    references/cac-cai-bay.md). '-frames:v k' de ffmpeg dung ngay sau frame
    cuoi can lay, khong decode het file.

    Tra ve dict {so_frame: mang int16 phang (size*size)}. Frame nao khong lay
    duoc thi khong co trong dict (nguoi goi phai tu xu ly).
    """
    np = _np()
    ffmpeg = need_tool("ffmpeg")
    fr = sorted(set(int(f) for f in frames if f is not None and int(f) >= 0))
    if not fr:
        return {}
    expr = "+".join("eq(n\\,%d)" % f for f in fr)
    vf = "select='%s',scale=%d:%d:flags=area,format=gray" % (expr, size, size)
    cmd = [ffmpeg, "-v", "error", "-nostdin", "-i", path, "-an", "-sn", "-vf", vf]
    cmd += (["-fps_mode", "passthrough"] if ffmpeg_major() >= 5 else ["-vsync", "0"])
    cmd += ["-frames:v", str(len(fr)), "-f", "rawvideo", "-"]
    rc, out, err = run(cmd, check=False, binary=True)
    n = size * size
    got = len(out) // n if out else 0
    if rc != 0 and got == 0:
        die(
            "Khong doc duoc frame hinh de doi chieu (ffmpeg ma %d):\n       %s\n%s"
            % (rc, path, (err or "").strip())
        )
    buf = np.frombuffer(out[: got * n], dtype=np.uint8)
    return dict((f, buf[i * n:(i + 1) * n].astype(np.int16)) for i, f in enumerate(fr[:got]))


def ffprobe_all(path):
    ffprobe = need_tool("ffprobe")
    rc, out, err = run(
        [ffprobe, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
        check=False,
    )
    if rc != 0:
        die("ffprobe khong doc duoc file:\n       %s\n%s" % (path, err.strip()))
    try:
        return json.loads(out)
    except Exception:
        die("ffprobe tra ve JSON khong hop le cho: %s" % path)


def count_video_packets(path):
    """Dem packet cua stream video — dang tin cay hon nb_frames trong metadata."""
    ffprobe = need_tool("ffprobe")
    rc, out, _ = run(
        [
            ffprobe, "-v", "error", "-select_streams", "v:0", "-count_packets",
            "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path,
        ],
        check=False,
    )
    txt = (out or "").strip().splitlines()
    for line in txt:
        line = line.strip().rstrip(",")
        if line.isdigit():
            return int(line)
    return None


def parse_fps(text):
    """'30/1' -> Fraction(30,1). Tra ve None neu khong doc duoc."""
    if not text:
        return None
    try:
        if "/" in text:
            num, den = text.split("/", 1)
            num, den = int(num), int(den)
            if den == 0:
                return None
            return Fraction(num, den)
        return Fraction(text)
    except Exception:
        return None


def probe(path):
    """Doc moi thu can biet ve video. Fail loudly neu thieu.

    Tra ve dict: width height fps(Fraction) fps_text nb_frames duration
                 has_audio a_sr a_ch a_codec v_codec color_* vfr
    """
    if not os.path.isfile(path):
        die("Khong tim thay file video:\n       %s" % path)
    info = ffprobe_all(path)
    vs = None
    as_ = None
    for s in info.get("streams", []):
        if s.get("codec_type") == "video" and vs is None:
            vs = s
        elif s.get("codec_type") == "audio" and as_ is None:
            as_ = s
    if vs is None:
        die("File nay khong co stream VIDEO:\n       %s" % path)

    fps = parse_fps(vs.get("r_frame_rate"))
    avg = parse_fps(vs.get("avg_frame_rate"))
    if fps is None or fps <= 0:
        die("Khong doc duoc fps cua video (r_frame_rate=%r)." % vs.get("r_frame_rate"))
    vfr = False
    if avg and avg > 0:
        vfr = abs(float(avg) - float(fps)) / float(fps) > 0.005

    nb = count_video_packets(path)
    if not nb:
        try:
            nb = int(vs.get("nb_frames"))
        except Exception:
            nb = None
    dur = None
    for src in (vs.get("duration"), info.get("format", {}).get("duration")):
        try:
            dur = float(src)
            break
        except Exception:
            continue
    if not nb and dur:
        nb = int(round(dur * float(fps)))
    if not nb:
        die("Khong xac dinh duoc so frame cua video. File co the bi hong.")
    if not dur:
        dur = nb / float(fps)

    out = {
        "path": path,
        "width": int(vs.get("width") or 0),
        "height": int(vs.get("height") or 0),
        "fps": fps,
        "fps_text": "%d/%d" % (fps.numerator, fps.denominator),
        "fps_float": float(fps),
        "nb_frames": int(nb),
        "duration": float(dur),
        "v_codec": vs.get("codec_name"),
        "pix_fmt": vs.get("pix_fmt"),
        "vfr": vfr,
        "avg_fps_float": float(avg) if avg else None,
        "has_audio": as_ is not None,
        "a_codec": None,
        "a_sr": None,
        "a_ch": None,
        "a_duration": None,
        "color_range": vs.get("color_range"),
        "color_space": vs.get("color_space"),
        "color_primaries": vs.get("color_primaries"),
        "color_transfer": vs.get("color_transfer"),
    }
    if as_ is not None:
        out["a_codec"] = as_.get("codec_name")
        try:
            out["a_sr"] = int(as_.get("sample_rate"))
        except Exception:
            out["a_sr"] = None
        try:
            out["a_ch"] = int(as_.get("channels"))
        except Exception:
            out["a_ch"] = None
        try:
            out["a_duration"] = float(as_.get("duration"))
        except Exception:
            out["a_duration"] = None
    return out


# ---------------------------------------------------------------- decode PCM


def pcm_blocks(path, sr, ch, block_frames=1 << 19):
    """Generator: decode audio ra s16le, yield mang int16 hinh (n, ch).

    Decode theo LUONG nen bo nho khong phinh theo do dai video.
    """
    np = _np()
    ffmpeg = need_tool("ffmpeg")
    cmd = [
        ffmpeg, "-v", "error", "-nostdin", "-i", path,
        "-map", "a:0", "-vn",
        "-ar", str(sr), "-ac", str(ch),
        "-f", "s16le", "-acodec", "pcm_s16le", "-",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    frame_bytes = 2 * ch
    want = block_frames * frame_bytes
    tail = b""
    try:
        while True:
            chunk = proc.stdout.read(want)
            if not chunk:
                break
            buf = tail + chunk
            n = (len(buf) // frame_bytes) * frame_bytes
            tail = buf[n:]
            if n:
                yield np.frombuffer(buf[:n], dtype="<i2").reshape(-1, ch)
    finally:
        try:
            proc.stdout.close()
        except Exception:
            pass
        err = proc.stderr.read().decode("utf-8", "replace")
        proc.stderr.close()
        rc = proc.wait()
        if rc != 0:
            die("ffmpeg decode audio that bai (ma %d):\n%s" % (rc, err.strip()))


def envelope(path, sr, ch, hop):
    """1 lan decode -> (rms_db, peak_lin, tong_so_sample).

    rms_db  : RMS (dBFS) cua ban downmix mono, moi hop.
    peak_lin: |mau| lon nhat TREN MOI KENH trong hop (0..1) — dung cho self-check.
    """
    np = _np()
    rms_parts, peak_parts = [], []
    total = 0
    buf = None
    for arr in pcm_blocks(path, sr, ch):
        total += int(arr.shape[0])
        buf = arr if buf is None else np.concatenate([buf, arr], axis=0)
        n = (buf.shape[0] // hop) * hop
        if n:
            blk = buf[:n].astype(np.float32) / 32768.0
            mono = blk.mean(axis=1).reshape(-1, hop)
            rms_parts.append(np.sqrt(np.maximum((mono * mono).mean(axis=1), 1e-20)))
            peak_parts.append(np.abs(blk).max(axis=1).reshape(-1, hop).max(axis=1))
            buf = buf[n:]
    if buf is not None and buf.shape[0] > 0:  # hop cuoi khong day
        blk = buf.astype(np.float32) / 32768.0
        mono = blk.mean(axis=1)
        rms_parts.append(np.array([math.sqrt(max(float((mono * mono).mean()), 1e-20))], dtype=np.float32))
        peak_parts.append(np.array([float(np.abs(blk).max())], dtype=np.float32))
    if not rms_parts:
        die("Stream audio rong (0 sample). Khong the lap ke hoach cat.")
    rms = np.concatenate(rms_parts)
    peak = np.concatenate(peak_parts)
    db = 20.0 * np.log10(np.maximum(rms, 1e-10))
    return db, peak, total


def window_peak_db(path, sr, ch, windows):
    """Do peak THAT (tung mau) trong tung cua so [s0,s1) — 1 lan decode.

    windows: list (s0, s1) chi so sample (theo frame audio, khong nhan kenh).
    Tra ve list dBFS cung thu tu. Cua so rong -> -inf.
    """
    np = _np()
    if not windows:
        return []
    order = sorted(range(len(windows)), key=lambda i: windows[i][0])
    peaks = [0.0] * len(windows)
    off = 0
    ptr = 0
    for arr in pcm_blocks(path, sr, ch):
        n = arr.shape[0]
        lo, hi = off, off + n
        # bo qua cua so da qua han
        while ptr < len(order) and windows[order[ptr]][1] <= lo:
            ptr += 1
        j = ptr
        while j < len(order):
            i = order[j]
            s0, s1 = windows[i]
            if s0 >= hi:
                break
            a = max(s0, lo) - off
            b = min(s1, hi) - off
            if b > a:
                v = int(np.abs(arr[a:b]).max())
                peaks[i] = max(peaks[i], v / 32768.0)
            j += 1
        off = hi
    return [(20.0 * math.log10(p) if p > 0 else float("-inf")) for p in peaks]


def extract_windows(path, sr, ch, windows):
    """Lay mau THAT cua tung cua so [s0,s1) — 1 lan decode, downmix mono float32."""
    np = _np()
    if not windows:
        return []
    outs = [np.zeros(max(0, w[1] - w[0]), dtype=np.float32) for w in windows]
    order = sorted(range(len(windows)), key=lambda i: windows[i][0])
    off = 0
    ptr = 0
    for arr in pcm_blocks(path, sr, ch):
        n = arr.shape[0]
        lo, hi = off, off + n
        while ptr < len(order) and windows[order[ptr]][1] <= lo:
            ptr += 1
        j = ptr
        while j < len(order):
            i = order[j]
            s0, s1 = windows[i]
            if s0 >= hi:
                break
            a = max(s0, lo)
            b = min(s1, hi)
            if b > a:
                seg = arr[a - off:b - off].astype(np.float32).mean(axis=1) / 32768.0
                outs[i][a - s0:b - s0] = seg
            j += 1
        off = hi
    return outs


def abs_diff_percentile(path, sr, ch, q):
    """Percentile cua |x[n+1]-x[n]| tren toan file (mono, don vi int16).

    Dung histogram nen bo nho co dinh, ket qua chinh xac (khong lay mau).
    """
    np = _np()
    hist = np.zeros(65537, dtype=np.int64)
    last = None
    total = 0
    for arr in pcm_blocks(path, sr, ch):
        mono = arr.astype(np.int32).mean(axis=1)
        if last is not None:
            mono = np.concatenate([np.array([last], dtype=mono.dtype), mono])
        if mono.shape[0] < 2:
            last = float(mono[-1])
            continue
        d = np.abs(np.diff(mono)).astype(np.int64)
        np.clip(d, 0, 65536, out=d)
        hist += np.bincount(d, minlength=65537)
        total += int(d.shape[0])
        last = float(mono[-1])
    if total == 0:
        return 0.0
    target = q / 100.0 * total
    csum = np.cumsum(hist)
    idx = int(np.searchsorted(csum, target))
    return float(idx)


# ---------------------------------------------------------------- range utils


def parse_ranges(text, label="--protect"):
    """'1.2-3.4,10-11' -> [(1.2,3.4),(10.0,11.0)] (giay)."""
    out = []
    if not text:
        return out
    for piece in str(text).replace(";", ",").split(","):
        piece = piece.strip()
        if not piece:
            continue
        sep = None
        for cand in ("-", ":", ".."):
            if cand in piece[1:]:
                sep = cand
                break
        if sep is None:
            die("%s sai cu phap o doan %r. Dung dang \"a-b,c-d\" (giay), vi du "
                "--protect \"12.5-19.0,44-50\"" % (label, piece))
        a, b = piece.split(sep, 1) if sep != ".." else piece.split("..", 1)
        try:
            a, b = float(a), float(b)
        except Exception:
            die("%s sai cu phap o doan %r: khong doc duoc so giay." % (label, piece))
        if b <= a:
            die("%s co doan %r voi diem cuoi <= diem dau." % (label, piece))
        out.append((a, b))
    return merge_ranges(out)


def merge_ranges(ranges):
    """Gop cac doan chong nhau / ke nhau."""
    if not ranges:
        return []
    rs = sorted((float(a), float(b)) for a, b in ranges)
    out = [list(rs[0])]
    for a, b in rs[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a, b) for a, b in out]


def subtract_ranges(seg, blocks):
    """seg=(a,b) tru di cac doan trong blocks -> list cac manh con lai."""
    a, b = seg
    pieces = [(a, b)]
    for ba, bb in blocks:
        nxt = []
        for pa, pb in pieces:
            if bb <= pa or ba >= pb:
                nxt.append((pa, pb))
                continue
            if ba > pa:
                nxt.append((pa, min(ba, pb)))
            if bb < pb:
                nxt.append((max(bb, pa), pb))
        pieces = nxt
        if not pieces:
            break
    return [(x, y) for x, y in pieces if y > x]


def fmt_hms(sec):
    sec = float(sec)
    m, s = divmod(sec, 60.0)
    h, m = divmod(int(m), 60)
    if h:
        return "%d:%02d:%06.3f" % (h, m, s)
    return "%02d:%06.3f" % (m, s)


def frame_to_sec(frame, fps):
    return float(Fraction(int(frame)) / fps)


def frame_to_sample(frame, fps, sr):
    """Chi so sample tuong ung frame — tinh bang Fraction, khong tich luy sai so."""
    return int(round(Fraction(int(frame)) * Fraction(int(sr)) / fps))
