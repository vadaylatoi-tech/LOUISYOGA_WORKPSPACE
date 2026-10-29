# -*- coding: utf-8 -*-
"""Bien 1 project Remotion phong cach 1 (tao bang new_project.py cua louisyoga-reel-style1) thanh phong cach 2.

    python apply_style2.py --project "D:/.../edit-NN-ten/project" [--force-reel]

- Chep remotion-overlay/src/kit/* (style2.tsx, sound.tsx co ONSET tieng moi, media.tsx nhan B-roll trong safe zone)
- Chep assets/sfx/* (4 tieng sang/choi: glitch, glasses-cheers-2, ting, new-item) vao public/sfx
- Reel.tsx mau (video 03 "Mua dong san lanh" v5) chi chep khi project chua co Reel cua video nay
  (Reel.tsx van la ban mau cua style 1) hoac co --force-reel.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
OVERLAY = os.path.join(SKILL, "remotion-overlay", "src")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--force-reel", action="store_true")
    a = ap.parse_args()
    src = os.path.join(a.project, "src")
    if not os.path.isdir(os.path.join(src, "kit")):
        sys.exit(f"  khong thay {src}/kit -> chay new_project.py cua louisyoga-reel-style1 truoc")
    for name in os.listdir(os.path.join(OVERLAY, "kit")):
        shutil.copy2(os.path.join(OVERLAY, "kit", name), os.path.join(src, "kit", name))
        print(f"  kit/{name}")
    reel = os.path.join(src, "reel", "Reel.tsx")
    style1_sample = os.path.join(os.path.dirname(SKILL), "..", "louisyoga-reel-style1-package", "louisyoga-reel-style1",
                                 "remotion-template", "src", "reel", "Reel.tsx")
    same = lambda p, q: os.path.isfile(p) and os.path.isfile(q) and open(p, "rb").read() == open(q, "rb").read()
    untouched = not os.path.isfile(reel) or same(reel, style1_sample)
    if a.force_reel or untouched:
        shutil.copy2(os.path.join(OVERLAY, "reel", "Reel.tsx"), reel)
        print("  reel/Reel.tsx (mau: Mua dong san lanh v5 — sua lai theo video)")
    else:
        print("  giu reel/Reel.tsx dang co (da sua cho video nay; --force-reel de thay bang mau style 2)")
    sfx = os.path.join(a.project, "public", "sfx")
    os.makedirs(sfx, exist_ok=True)
    for name in os.listdir(os.path.join(SKILL, "assets", "sfx")):
        shutil.copy2(os.path.join(SKILL, "assets", "sfx", name), os.path.join(sfx, name))
        print(f"  public/sfx/{name}")
    print("  XONG. Tiep: gen_data.py -> sua Reel.tsx (khoi ▼ EDIT ▼) -> stills.py -> render_all.py --music-under 11")


if __name__ == "__main__":
    main()
