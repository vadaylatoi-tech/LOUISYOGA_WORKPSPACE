# -*- coding: utf-8 -*-
"""Render tron goi: stem SFX + nhac (build_stems.py, vai giay) -> bundle -> hinh (muted) -> mix voi giong da xu ly -> master.

    python render_all.py --project <project> --voice work/voice_proc.wav --out "Output/Ten_Video_v1.mp4"
                         [--composition LouisYogaReel] [--sfx-rel -2.5] [--port 3123] [--concurrency 4]

Cac file trung gian nam trong <project>/renders/<ten-out>/. Khong ghi de file --out da co (them _v2, _v3...).
Stem am thanh dung bang numpy tu CUES/MUSIC_CURVE (truoc day render Remotion --codec=wav mat ~3 phut/stem);
Reel.tsx viet la khong parse duoc -> tu lui ve Remotion. Hinh: jpeg-quality 95 + crf 14 (mac dinh Remotion 80/18 lam mo them).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def npx(args, cwd):
    exe = "npx.cmd" if os.name == "nt" else "npx"
    print("  > npx " + " ".join(args)[:140])
    r = subprocess.run([exe, *args], cwd=cwd)
    if r.returncode:
        K.die("remotion that bai (xem log o tren)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--composition", default="LouisYogaReel")
    ap.add_argument("--sfx-rel", type=float, default=-2.5)
    ap.add_argument("--port", default="3123")
    ap.add_argument("--concurrency", default="4")
    a = ap.parse_args()
    a.project = os.path.abspath(a.project)
    out = a.out
    base, ext = os.path.splitext(out)
    k = 2
    while os.path.exists(out):
        out = f"{base}_v{k}{ext}"
        k += 1
    name = os.path.splitext(os.path.basename(out))[0]
    rdir = os.path.join(a.project, "renders", name)
    os.makedirs(rdir, exist_ok=True)
    bundle = os.path.join(rdir, "bundle")
    npx(["remotion", "bundle", "src/index.ts", "--out-dir", bundle], a.project)
    common = ["--port=" + a.port]
    st = subprocess.run([sys.executable, os.path.join(HERE, "build_stems.py"), "--project", a.project, "--out-dir", rdir])
    if st.returncode:
        print("  build_stems khong dung duoc -> render stem bang Remotion (cham)")
        npx(["remotion", "render", bundle, a.composition, os.path.join(rdir, "sfx.wav"), "--codec=wav", "--props=" + json.dumps({"stem": "sfx"}), *common], a.project)
        npx(["remotion", "render", bundle, a.composition, os.path.join(rdir, "music.wav"), "--codec=wav", "--props=" + json.dumps({"stem": "music"}), *common], a.project)
    npx(["remotion", "render", bundle, a.composition, os.path.join(rdir, "video_muted.mp4"), "--muted", "--props=" + json.dumps({"stem": "none"}),
         "--crf=14", "--jpeg-quality=95", "--x264-preset=medium", "--concurrency=" + a.concurrency, *common], a.project)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, "mix_stems.py"), "--voice", a.voice, "--sfx", os.path.join(rdir, "sfx.wav"),
                        "--music", os.path.join(rdir, "music.wav"), "--video", os.path.join(rdir, "video_muted.mp4"), "--out", out,
                        "--sfx-rel", str(a.sfx_rel), "--work", os.path.join(rdir, "mix")])
    if r.returncode:
        K.die("mix that bai")
    print(f"\n  XONG -> {out}")


if __name__ == "__main__":
    main()
