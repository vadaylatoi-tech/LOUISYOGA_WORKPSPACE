"""Anh bia (thumbnail) cho video final: tim khung hook da du chu trong vai giay dau, luu JPG
cung ten canh video va gan lam anh bia (attached_pic) trong mp4 - KHONG ma hoa lai hinh/tieng
(kiem md5 tung goi truoc khi thay file, giu nguyen mtime). Chay lai se thay bia cu.

Mac dinh (chu thuong hieu duyet 27/10/2026): khung TRUOC luc gach chu + dau moc hien
-> du tieu de 2 dong, khong gach. --co-gach: khung co gach chu + dau moc.

  python make_cover.py <video.mp4> [...] [--co-gach] [--chi-anh] [--backup <thu muc>] [--debug]
  python make_cover.py <video.mp4> --t 1.3     # tu chon giay (hook tren B-roll, panel hien som...)
Luon soat anh: video co hook nam giua khung (B-roll) hoac panel/caption hien ngay -> dung --t.
"""
import argparse, json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image

W, H = 216, 384          # khung nho de cham diem
SCAN_S = 6.0             # hook nam trong 6 giay dau
KHONG_GACH = True        # False (--co-gach): lay khung co gach chu + dau moc


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=index,codec_type,codec_name,r_frame_rate:stream_disposition=attached_pic",
                          "-of", "json", path], capture_output=True, text=True, encoding="utf-8").stdout
    return json.loads(out)["streams"]


def frames_small(path):
    cmd = ["ffmpeg", "-v", "error", "-t", str(SCAN_S), "-i", path, "-map", "0:v:0",
           "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16)
    return arr


def score(fr):
    r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
    white = (r > 225) & (g > 225) & (b > 225)
    pink = (r > 200) & (g < 120) & (b > 110) & (b < 220)
    gold = (r > 200) & (g > 150) & (b < 90)
    top = slice(0, int(H * 0.24))
    title = (white[top] | pink[top]).mean()
    stamp = gold[int(H * 0.45):int(H * 0.92)].mean()
    gray = fr.mean(-1)
    sharp = np.abs(np.diff(gray, axis=0)).mean() + np.abs(np.diff(gray, axis=1)).mean()
    return title, stamp, sharp, gray.mean()


def pick(path, debug=False):
    fps_s = next(s for s in probe(path) if s["codec_type"] == "video")["r_frame_rate"]
    n, d = map(int, fps_s.split("/"))
    fps = n / d
    arr = frames_small(path)
    m = np.array([score(f) for f in arr])           # title, stamp, sharp, luma
    title, stamp, sharp, luma = m.T
    # khung "du chu": tieu de gan cuc dai VA (neu co dau moc) dau moc gan cuc dai
    # bo khung dang chop sang (flash)
    # (so voi trung vi +-0.2 s quanh no: sau dau moc nen bi lam toi nen trung vi ca doan khong dung duoc)
    w = max(2, round(fps * 0.2))
    near = np.array([np.median(luma[max(0, i - w):i + w + 1]) for i in range(len(luma))])
    ok = luma <= near * 1.08
    if KHONG_GACH and stamp.max() > 0.004:
        # gach chu hien cung luc voi dau moc -> chi lay khung TRUOC khi dau moc hien
        first = int(np.argmax(stamp > stamp.max() * 0.3))
        ok[first:] = False
        ok[max(0, first - 3):first] = False      # bo vai khung chop sang ngay truoc
    elif stamp.max() > 0.004:
        # dau moc xuat hien sau cung -> chi xet doan dau moc da hien, roi lay khung tieu de day du nhat
        ok &= stamp >= stamp.max() * 0.6
    # chu da DUNG YEN: vung tieu de gan nhu khong doi so voi 0.2 s sau (chu dang bat/phong to,
    # khung rung, mep cat deu lam doi manh)
    top = arr[:, :int(H * 0.24)].mean(-1)
    n = len(arr)
    k = max(1, round(fps * 0.2))
    stab = np.array([np.abs(top[i] - top[min(i + k, n - 1)]).mean() for i in range(n)])
    if ok.any():
        ok &= title >= np.percentile(title[ok], 90) * 0.9   # khong lay max: chu dang phong to cho dinh ao
    ok &= stab <= 1.5
    # lay dot "dung yen" DAU TIEN (sau do video bat dau hien caption/panel), khung o giua dot
    runs, start = [], None
    for i in range(n + 1):
        if i < n and ok[i]:
            start = i if start is None else start
        elif start is not None:
            runs.append((start, i - 1)); start = None
    long_runs = [r for r in runs if r[1] - r[0] + 1 >= 3] or runs
    if long_runs:
        a, b = long_runs[0]
        best = min(a + max(k, (b - a) // 2), b, a + round(fps * 0.5))
    else:
        best = int(np.argmax(title - 0.01 * stab))
    if debug:
        for i in range(0, len(m), 3):
            print(f"  f{i:3d} t={title[i]:.3f} s={stamp[i]:.4f} sharp={sharp[i]:.1f} L={luma[i]:.0f}"
                  f"{' <-' if i == best else ''}{' ok' if ok[i] else ''}")
    return best / fps, best


def make(path, backup=None, chi_anh=False, debug=False, t=None):
    base = os.path.splitext(path)[0]
    jpg = base + ".jpg"
    if t is None:
        t, f = pick(path, debug)
    else:
        f = '-'
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1",
                    "-q:v", "2", jpg], check=True)
    msg = f"khung {f} ({t:.2f}s) -> {os.path.basename(jpg)}"
    if chi_anh:
        return msg
    if backup:
        os.makedirs(backup, exist_ok=True)
        shutil.copy2(path, os.path.join(backup, os.path.basename(path)))
    tmp = base + ".cover-tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-i", jpg, "-map", "0:v:0", "-map", "0:a?", "-map", "1",
                    "-c", "copy", "-disposition:v:1", "attached_pic", "-map_metadata", "0",
                    "-movflags", "+faststart", tmp], check=True)
    # kiem tra: hinh + tieng giu nguyen tung goi
    def md5(p, sel):
        return subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-map", sel, "-c", "copy", "-f", "md5", "-"],
                              capture_output=True, text=True).stdout.strip()
    for sel in ("0:v:0", "0:a:0"):
        if md5(path, sel) != md5(tmp, sel):
            os.remove(tmp)
            raise SystemExit(f"LOI: luong {sel} bi doi o {path}")
    st = os.stat(path)
    os.replace(tmp, path)
    os.utime(path, (st.st_atime, st.st_mtime))      # giu mtime de khong lech ho so
    return msg + " ; da gan anh bia, hinh/tieng trung khop"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--backup")
    ap.add_argument("--chi-anh", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--co-gach", action="store_true")
    ap.add_argument("--t", type=float, help="giay lay anh (chi khi truyen 1 video)")
    a = ap.parse_args()
    if a.t is not None and len(a.videos) != 1:
        ap.error("--t chi dung voi 1 video")
    global KHONG_GACH
    KHONG_GACH = not a.co_gach
    for v in a.videos:
        print(os.path.basename(v), ":", make(v, a.backup, a.chi_anh, a.debug, a.t), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
