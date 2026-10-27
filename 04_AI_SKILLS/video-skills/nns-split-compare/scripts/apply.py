# -*- coding: utf-8 -*-
"""Dung video so sanh bang MOT filtergraph duy nhat.

Cau truc: moi pha = nen den + 1 video dang chay dat vao o khung + lop chrome PNG
de len tren. Hai pha noi bang filter `concat` (KHONG dung concat demuxer — cai
do tut fps ve 25 tren mot so build ffmpeg).

Duong dan file luon di qua -i, khong bao gio nhet vao chuoi filter.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def build_filter(plan, has_a_l, has_a_r):
    L = plan["layout"]
    d1, d2 = plan["phases"][0]["dur"], plan["phases"][1]["dur"]
    bg = "0x%02X%02X%02X" % C.BG[:3]
    pw, ph, py = L["panel_w"], L["panel_h"], L["panel_y"]

    f = []
    # --- pha 1: TRAI chay
    f.append("color=c=%s:s=%dx%d:r=%d:d=%.6f,format=rgba[bg1]" % (bg, C.W, C.H, C.FPS, d1))
    f.append("[0:v]fps=%d,scale=%d:%d:flags=lanczos,setsar=1,format=rgba[lv]"
             % (C.FPS, pw, ph))
    f.append("[bg1][lv]overlay=%d:%d:shortest=1[o1]" % (L["left_x"], py))
    f.append("[o1][2:v]overlay=0:0:eof_action=repeat,format=yuv420p[p1]")
    # --- pha 2: PHAI chay
    f.append("color=c=%s:s=%dx%d:r=%d:d=%.6f,format=rgba[bg2]" % (bg, C.W, C.H, C.FPS, d2))
    f.append("[1:v]fps=%d,scale=%d:%d:flags=lanczos,setsar=1,format=rgba[rv]"
             % (C.FPS, pw, ph))
    f.append("[bg2][rv]overlay=%d:%d:shortest=1[o2]" % (L["right_x"], py))
    f.append("[o2][3:v]overlay=0:0:eof_action=repeat,format=yuv420p[p2]")

    # --- tieng: pha 1 lay tieng ben trai, pha 2 lay tieng ben phai
    af = "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"
    if has_a_l:
        f.append("[0:a]%s,atrim=0:%.6f,asetpts=N/SR/TB[a1]" % (af, d1))
    else:
        f.append("anullsrc=r=48000:cl=stereo,atrim=0:%.6f,%s[a1]" % (d1, af))
    if has_a_r:
        f.append("[1:a]%s,atrim=0:%.6f,asetpts=N/SR/TB[a2]" % (af, d2))
    else:
        f.append("anullsrc=r=48000:cl=stereo,atrim=0:%.6f,%s[a2]" % (d2, af))

    f.append("[p1][a1][p2][a2]concat=n=2:v=1:a=1[v][a]")
    return ";".join(f)


def main():
    C.setup_io()
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--chrome", required=True, help="thu muc chua chrome_p1/p2.png")
    ap.add_argument("--out", required=True)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--audio-bitrate", dest="abr", default="256k")
    ap.add_argument("--dry-run", dest="dry", action="store_true")
    a = ap.parse_args()

    C.head("APPLY (dung video)")
    C.need_tool("ffmpeg")
    plan = C.load_json(a.plan)

    c1 = os.path.join(a.chrome, "chrome_p1.png")
    c2 = os.path.join(a.chrome, "chrome_p2.png")
    for p in (plan["left"]["path"], plan["right"]["path"], c1, c2):
        if not os.path.isfile(p):
            C.die("Thieu file dau vao: %s\n       Chay chrome.py truoc." % p)

    fc = build_filter(plan, plan["left"]["has_audio"], plan["right"]["has_audio"])
    cmd = ["ffmpeg", "-y", "-v", "error", "-stats",
           "-i", plan["left"]["path"],
           "-i", plan["right"]["path"],
           "-i", c1, "-i", c2,
           "-filter_complex", fc,
           "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-crf", str(a.crf), "-preset", a.preset,
           "-pix_fmt", "yuv420p", "-r", str(C.FPS),
           "-c:a", "aac", "-b:a", a.abr, "-ar", "48000",
           "-movflags", "+faststart", a.out]

    print("  Ra        : %s" % a.out)
    print("  Pha 1     : 0.000 -> %.3fs (trai chay, %d frame)"
          % (plan["phases"][0]["dur"], plan["phases"][0]["frames"]))
    print("  Pha 2     : %.3f -> %.3fs (phai chay, %d frame)"
          % (plan["phases"][1]["start"], plan["total"]["dur"], plan["phases"][1]["frames"]))
    print("  Du kien   : %d frame, %.3fs" % (plan["total"]["frames"], plan["total"]["dur"]))
    print("")

    if a.dry:
        print("  --dry-run: khong render. Filtergraph:")
        for line in fc.split(";"):
            print("      " + line)
        print("")
        return

    C.run(cmd, capture=True)
    n = C.count_frames(a.out)
    print("")
    print("  Xong. So frame dau ra: %d (du kien %d)" % (n, plan["total"]["frames"]))
    if n != plan["total"]["frames"]:
        C.die("So frame KHONG khop ke hoach (%d vs %d). Khong bao 'xong'."
              % (n, plan["total"]["frames"]))
    print("")


if __name__ == "__main__":
    main()
