# -*- coding: utf-8 -*-
"""Tao project review: chep template, font, logo, anh san pham. Khong ghi de project da co."""
import argparse
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", required=True)
    ap.add_argument("--anh-san-pham", required=True, help="anh tren the goc phai va CTA")
    ap.add_argument("--config", help="review.json co san, mac dinh chep vi du Aura de sua")
    a = ap.parse_args()
    if os.path.exists(os.path.join(a.dest, "src")):
        sys.exit("Project da co, khong ghi de: " + a.dest)
    shutil.copytree(os.path.join(SKILL, "remotion-template"), a.dest, dirs_exist_ok=True)
    img = os.path.join(a.dest, "public", "img")
    shutil.copytree(os.path.join(SKILL, "assets", "fonts"), os.path.join(img, "fonts"))
    shutil.copy2(os.path.join(SKILL, "assets", "logo_louisyoga_white.svg"), img)
    shutil.copy2(a.anh_san_pham, os.path.join(img, "product.jpg"))
    shutil.copy2(a.config or os.path.join(SKILL, "examples", "aura.review.json"), os.path.join(a.dest, "review.json"))
    print("XONG ->", a.dest)


if __name__ == "__main__":
    main()
