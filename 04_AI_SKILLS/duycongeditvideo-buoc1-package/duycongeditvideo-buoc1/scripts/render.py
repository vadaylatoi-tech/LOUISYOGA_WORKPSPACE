# -*- coding: utf-8 -*-
"""Buoc 4 — cat + ghep cac doan thanh video ngan (giu nguyen mau goc).

    python render.py --work "D:/.../du_an" --out "D:/.../Video ngan"
    python render.py --work ... --out ... --only 06,07
    python render.py --work ... --out ... --grade      # chi khi nguoi dung YEU CAU chinh mau

Moi doan cat tu video goc (seek chinh xac + ma hoa lai), fade tieng 10/30 ms
o 2 dau doan de khong nghe tieng "tach", roi concat. Do phan giai, fps giu nguyen.
Encoder: h264_nvenc neu co GPU NVIDIA, khong thi libx264.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dccommon as C  # noqa: E402

# Chinh mau nhe: trung tinh hoa ngả vang-xanh, nang trung tone, tang bao hoa, lam net.
GRADE = ("colorchannelmixer=rr=1.0:gg=0.98:bb=1.065,"
         "curves=all='0/0 0.06/0.05 0.25/0.29 0.5/0.63 0.75/0.87 1/1',"
         "eq=contrast=1.06:saturation=1.25,cas=strength=0.7")


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True, help="thu muc chua video ngan")
    ap.add_argument("--only")
    ap.add_argument("--grade", action="store_true", help="bat chinh mau (mac dinh TAT)")
    ap.add_argument("--cpu", action="store_true", help="ep dung libx264")
    a = ap.parse_args()
    C.need_ffmpeg()
    cuts = C.read_json(os.path.join(a.work, "cuts.json"))
    src = cuts["source"]
    info = C.probe(src)
    os.makedirs(a.out, exist_ok=True)
    only = set(x.strip() for x in a.only.split(",")) if a.only else None
    nv = (not a.cpu) and C.has_encoder("h264_nvenc")
    if nv:
        venc = ["-c:v", "h264_nvenc", "-preset", "p7", "-rc", "vbr", "-cq", "19",
                "-b:v", "14M", "-maxrate", "20M", "-profile:v", "high"]
    else:
        venc = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high"]
    fps = round(info["fps"]) or 30
    for v in cuts["videos"]:
        if only and v["id"] not in only:
            continue
        segs = v["segments"]
        args = ["ffmpeg", "-v", "error", "-y"]
        fc = []
        for i, s in enumerate(segs):
            d = s["out"] - s["in"]
            args += ["-ss", "%.3f" % s["in"], "-t", "%.3f" % d, "-i", src]
            fc.append("[%d:v]setpts=PTS-STARTPTS[v%d];[%d:a]asetpts=PTS-STARTPTS,"
                      "afade=t=in:d=0.01,afade=t=out:st=%.3f:d=0.03[a%d]" % (i, i, i, max(0, d - 0.03), i))
        n = len(segs)
        post = (GRADE + ",") if a.grade else ""
        fc.append("".join("[v%d][a%d]" % (i, i) for i in range(n)) +
                  "concat=n=%d:v=1:a=1[cv][ca];[cv]%sformat=yuv420p[ov]" % (n, post))
        out = os.path.join(a.out, v["name"] + ".mp4")
        args += ["-filter_complex", ";".join(fc), "-map", "[ov]", "-map", "[ca]"] + venc + [
            "-r", str(fps), "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out]
        r = subprocess.run(args)
        if r.returncode != 0:
            C.die("ffmpeg loi khi render %s" % v["name"])
        got = C.probe(out)["duration"]
        print("  %s  %.1fs  -> %s" % (v["id"], got, out), flush=True)


if __name__ == "__main__":
    main()
