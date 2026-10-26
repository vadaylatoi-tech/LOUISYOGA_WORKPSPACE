# -*- coding: utf-8 -*-
"""Cat avatar san pham Louis Yoga (nen trang, tham dung giua) thanh the doc 440x920 cho MatCard / Polaroid.

    python prep_products.py --src "<...>/4. Avatar thảm final" --dest <project>/public/img [--pick asana=cam moon=xanh ...]

Thu muc avatar: <Dong>/<n. Mau>/<Mau>_màu <mau> JPG.jpg  (Harmony: Sunflower, Aura, Asana, Moon;
Balance: Asana25, Basic, BasicZen, Queen; Mastery: Lilium, Nature, F23, Diamond — da xac nhan voi chu thuong hieu).
Ra: <dest>/<ten mau viet thuong>.jpg cho moi mau (mau sac dau tien, hoac theo --pick ten=chu-trong-ten-file).
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--pick", nargs="*", default=[])
    a = ap.parse_args()
    from PIL import Image

    pick = dict(p.split("=", 1) for p in a.pick)
    os.makedirs(a.dest, exist_ok=True)
    for d in sorted(glob.glob(os.path.join(a.src, "[123]. *", "*. *"))):
        model = os.path.basename(d).split(". ", 1)[1]
        key = model.lower().replace(" ", "")
        files = sorted(glob.glob(os.path.join(d, "*JPG.jpg")))
        want = pick.get(key)
        if want:
            files = [p for p in files if want.lower() in os.path.basename(p).lower()] or files
        if not files:
            continue
        im = Image.open(files[0]).convert("RGB")
        w, h = im.size
        im.crop((int(w * 0.27), int(h * 0.02), int(w * 0.73), int(h * 0.98))).resize((440, 920), Image.LANCZOS).save(os.path.join(a.dest, key + ".jpg"), quality=90)
        print(f"  {key:10s} <- {os.path.relpath(files[0], a.src)}")


if __name__ == "__main__":
    main()
