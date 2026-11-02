# -*- coding: utf-8 -*-
"""Tao 1 project Remotion moi cho 1 video tu remotion-template + assets cua skill.

    python new_project.py --dest "D:/Video/reel-04/project" [--clean work/clean.mp4] [--install]

- Chep remotion-template/ (kit + Reel.tsx mau) sang --dest
- Chep assets vao public/: fonts, sfx, music, brand, broll
- --clean: chep footage da cat vao public/footage/clean.mp4
- --install: chay npm install (lan dau ~1-3 phut, can mang)
Khong bao gio ghi de project da ton tai (tru khi --force).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402
import remotion_local as RL  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", required=True)
    ap.add_argument("--clean")
    ap.add_argument("--install", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if os.path.exists(os.path.join(a.dest, "src")) and not a.force:
        print(f"  project da co o {a.dest} -> chi cap nhat public/ (khong dong vao src/)")
    else:
        shutil.copytree(K.TEMPLATE, a.dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns("node_modules", "renders", "out"))
    pub = os.path.join(a.dest, "public")
    drive = RL.tren_drive(a.dest)
    for sub in () if drive else ("fonts", "sfx", "music", "brand", "broll", "louis-photos"):
        shutil.copytree(os.path.join(K.ASSETS, sub), os.path.join(pub, sub), dirs_exist_ok=True)
    os.makedirs(os.path.join(pub, "footage"), exist_ok=True)
    os.makedirs(os.path.join(pub, "img"), exist_ok=True)
    if a.clean:
        shutil.copy2(a.clean, os.path.join(pub, "footage", "clean.mp4"))
    print(f"  project -> {a.dest}")
    if a.install and not drive:
        npm = "npm.cmd" if os.name == "nt" else "npm"
        print("  npm install ...")
        r = subprocess.run([npm, "install", "--no-audit", "--no-fund"], cwd=a.dest)
        if r.returncode:
            K.die("npm install that bai")
    print("  Tiep: sua src/reel/Reel.tsx theo video; data.ts sinh bang gen_data.py")


if __name__ == "__main__":
    main()
