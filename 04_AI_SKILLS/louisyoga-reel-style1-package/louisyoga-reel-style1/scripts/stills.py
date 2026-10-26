# -*- coding: utf-8 -*-
"""Soat bo cuc nhanh: bundle project 1 lan roi chup nhieu khung -> 1 tam contact sheet.

    python stills.py --project <project> --out work/stills_sheet.jpg --times 0.5 1.6 4 9 15.2 ... [--scale 0.4]

--times tinh bang GIAY (timeline da cat). Moi khung ~3 s (truoc day goi `remotion still src/index.ts` tung khung
nen moi lan phai bundle lai). Xem sheet bang Read, sua Reel.tsx, chay lai chi nhung moc can xem.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--times", type=float, nargs="+", required=True)
    ap.add_argument("--scale", type=float, default=0.4)
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--port", default="3128")
    a = ap.parse_args()
    from PIL import Image, ImageDraw

    proj = os.path.abspath(a.project)
    npx = "npx.cmd" if os.name == "nt" else "npx"
    sdir = os.path.join(os.path.dirname(os.path.abspath(a.out)), "stills")
    os.makedirs(sdir, exist_ok=True)
    bundle = os.path.join(proj, "renders", "_stills_bundle")
    r = subprocess.run([npx, "remotion", "bundle", "src/index.ts", "--out-dir", bundle, "--log=error"], cwd=proj, capture_output=True)
    if r.returncode:
        K.die("bundle that bai:\n" + r.stderr.decode("utf-8", "replace")[-1500:])
    ims = []
    for t in a.times:
        p = os.path.join(sdir, f"t{t:06.2f}.png")
        r = subprocess.run([npx, "remotion", "still", bundle, "LouisYogaReel", p, f"--frame={round(t * 30)}", f"--scale={a.scale}",
                            f"--port={a.port}", "--log=error"], cwd=proj, capture_output=True)
        if r.returncode:
            print(f"  khung {t}s loi: {r.stderr.decode('utf-8', 'replace')[-300:]}")
            continue
        im = Image.open(p).convert("RGB")
        ImageDraw.Draw(im).text((6, 6), f"{t:.2f}s", fill=(255, 255, 0))
        ims.append(im)
    if not ims:
        K.die("khong chup duoc khung nao")
    w, h = ims[0].size
    cols = min(a.cols, len(ims))
    sheet = Image.new("RGB", (w * cols, h * ((len(ims) + cols - 1) // cols)))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(a.out, quality=85)
    print(f"  {len(ims)} khung -> {a.out}")


if __name__ == "__main__":
    main()
