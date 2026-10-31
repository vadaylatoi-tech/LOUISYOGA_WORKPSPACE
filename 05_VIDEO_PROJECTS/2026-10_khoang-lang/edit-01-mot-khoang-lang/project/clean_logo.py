"""Xoa logo hang ao (Livan) tren 3 shot: bam theo mau roi va vai sach ben canh, ghi ra plate khong nen.
Phim goc khong bi dong vao. Chay: python clean_logo.py  (plate vao work/plates/, build.py tu dung)
"""
import json, subprocess
from pathlib import Path
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view as swv

HERE = Path(__file__).parent
MEDIA = Path("G:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA")
OUT = MEDIA / "05_VIDEO_PROJECTS/2026-10_khoang-lang/edit/01-mot-khoang-lang/work/plates"
OUT.mkdir(exist_ok=True)
E = json.loads((HERE / "edit.json").read_text(encoding="utf-8"))
FILM = str(MEDIA / E["film"])
W, H = 1920, 1080
COLOR = "in_color_matrix=bt709:out_color_matrix=bt709:in_range=tv:out_range=tv"


def feather(w, h, edge):
    ramp = lambda n: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / edge, 0, 1)
    m = np.outer(ramp(h), ramp(w)).astype(np.float32)
    return (m * m * (3 - 2 * m))[..., None]


def match(area, tpl):
    # Tim vi tri lech it nhat (tuong duong matchTemplate SQDIFF, bo do sang chung).
    v = swv(area, tpl.shape).astype(np.float32)
    v = v - v.mean((2, 3), keepdims=True)
    t = tpl - tpl.mean()
    e = ((v - t) ** 2).sum((2, 3))
    return np.unravel_index(e.argmin(), e.shape)


def clean(s):
    c = s["clean"]
    x, y, pw, ph = c["start"]
    dx, dy = c.get("from", (0, 0))
    dur = s["out"] - s["in"]
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(s["in"]), "-t", str(dur), "-i", FILM, "-vf", f"scale={COLOR},format=bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    name = OUT / f"{s['clean']['id']}.mkv"
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-vf", f"scale={COLOR},format=yuv444p", "-c:v", "ffv1", str(name)], stdin=subprocess.PIPE)
    mask = feather(pw, ph, c.get("edge", 12))
    tpl = None
    n = 0
    track = []
    while True:
        b = rd.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        f = np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()
        g = f[..., 1].astype(np.float32)
        l, t = int(x - pw / 2), int(y - ph / 2)
        if tpl is None:
            tpl = g[t:t + ph, l:l + pw].copy()
        else:
            r = 12
            area = g[t - r:t + ph + r, l - r:l + pw + r]
            my, mx = match(area, tpl)
            x += mx - r
            y += my - r
            l, t = int(x - pw / 2), int(y - ph / 2)
            # Mau cap nhat cham de bam duoc khi nep vai doi nhe.
            tpl = 0.9 * tpl + 0.1 * g[t:t + ph, l:l + pw]
        dst = f[t:t + ph, l:l + pw].astype(np.float32)
        if c.get("vinterp"):
            # Logo rat nho nam giua dai ao: noi mep tren/duoi cua chinh dai ao, moi cot mot lan.
            top, bot = dst[0], dst[-1]
            a = np.linspace(0, 1, ph)[:, None, None]
            src = top[None] * (1 - a) + bot[None] * a
        else:
            src = f[t + dy:t + dy + ph, l + dx:l + dx + pw].astype(np.float32)
        # Khop sang toi theo vien de mieng va khong lo mau.
        ring = (mask[..., 0] < 0.15)
        src += (dst[ring].mean(0) - src[ring].mean(0))
        f[t:t + ph, l:l + pw] = np.clip(dst * (1 - mask) + src * mask, 0, 255).astype(np.uint8)
        wr.stdin.write(f.tobytes())
        track.append((n, x, y))
        n += 1
    wr.stdin.close()
    wr.wait()
    print(name.name, n, "frames, cuoi", track[-1][1:])


for s in E["shots"]:
    if "clean" in s:
        clean(s)
