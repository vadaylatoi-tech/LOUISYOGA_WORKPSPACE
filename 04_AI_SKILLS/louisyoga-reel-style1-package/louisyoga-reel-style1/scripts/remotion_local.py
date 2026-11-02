# -*- coding: utf-8 -*-
"""Project Remotion nam tren Drive; Drive khong cai duoc node_modules nen render qua ban sao tam tren may.

Moi noi dung that (src, footage, img) song tren Drive. Ban sao tam + node_modules dung chung + file trung gian
nam o LOUGA_CACHE (mac dinh D:/LOUGA_CACHE, khong bao gio o C:), xoa di luc nao cung duoc: lan chay sau tu dung lai.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess

import common as K

CONFIG = ("package.json", "package-lock.json", "remotion.config.ts", "tsconfig.json")
ASSET = ("fonts", "sfx", "music", "brand", "broll", "louis-photos")
THU_MUC_DRIVE = ("footage", "img")


def tren_drive(path: str) -> bool:
    p = os.path.abspath(path).replace("\\", "/").lower()
    return p.startswith("g:/") or "/my drive/" in p


def goc_cache() -> str:
    root = os.environ.get("LOUGA_CACHE") or ("D:/LOUGA_CACHE" if os.path.isdir("D:/") else "")
    if not root:
        K.die("May nay khong co o D: -> dat bien LOUGA_CACHE tro toi o may khac C: roi chay lai.")
    if os.path.abspath(root).lower().startswith("c:"):
        K.die("LOUGA_CACHE khong duoc nam tren o C:.")
    os.makedirs(root, exist_ok=True)
    return root


def _junction(link: str, target: str):
    if os.path.lexists(link):
        return
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "mklink", "/J", link.replace("/", "\\"), target.replace("/", "\\")], check=True, capture_output=True)
    else:
        os.symlink(target, link)


def _lien_ket_asset(goc: str, dich: str):
    """Remotion khong chep duoc junction trong public/: dung hard link, khac o thi chep that."""
    if os.path.lexists(dich) and os.path.isjunction(dich):
        os.rmdir(dich)
    for r, _, fs in os.walk(goc):
        d = os.path.join(dich, os.path.relpath(r, goc))
        os.makedirs(d, exist_ok=True)
        for f in fs:
            b = os.path.join(d, f)
            if os.path.exists(b):
                continue
            try:
                os.link(os.path.join(r, f), b)
            except OSError:
                shutil.copy2(os.path.join(r, f), b)


def _dong_bo_thu_muc(goc: str, dich: str):
    if os.path.isdir(dich):
        shutil.rmtree(dich)
    if os.path.isdir(goc):
        shutil.copytree(goc, dich)
    else:
        os.makedirs(dich, exist_ok=True)


def chuan_bi(project: str) -> str:
    """Tra ve thu muc chay Remotion cho project. Project khong nam tren Drive thi dung nguyen."""
    project = os.path.abspath(project)
    if not tren_drive(project):
        return project
    root = goc_cache()
    tmp = os.path.join(root, "tmp")
    os.makedirs(tmp, exist_ok=True)
    os.environ.update(TEMP=tmp, TMP=tmp, TMPDIR=tmp, npm_config_cache=os.path.join(root, "npm"))
    ten = re.sub(r"[^A-Za-z0-9._-]+", "_", "__".join(project.replace("\\", "/").split("/")[-4:-1]))
    dst = os.path.join(root, "projects", ten)
    shutil.rmtree(os.path.join(dst, "renders"), ignore_errors=True)
    os.makedirs(os.path.join(dst, "public"), exist_ok=True)
    runtime = os.path.join(root, "runtime")
    if not os.path.isdir(os.path.join(runtime, "node_modules")):
        os.makedirs(runtime, exist_ok=True)
        for f in ("package.json", "package-lock.json"):
            if os.path.exists(os.path.join(project, f)):
                shutil.copy2(os.path.join(project, f), runtime)
        print(f"  npm install mot lan trong {runtime} ...")
        npm = "npm.cmd" if os.name == "nt" else "npm"
        if subprocess.run([npm, "install", "--no-audit", "--no-fund"], cwd=runtime).returncode:
            K.die("npm install that bai")
    _junction(os.path.join(dst, "node_modules"), os.path.join(runtime, "node_modules"))
    _dong_bo_thu_muc(os.path.join(project, "src"), os.path.join(dst, "src"))
    for f in CONFIG:
        if os.path.exists(os.path.join(project, f)):
            shutil.copy2(os.path.join(project, f), dst)
    for sub in THU_MUC_DRIVE:
        _dong_bo_thu_muc(os.path.join(project, "public", sub), os.path.join(dst, "public", sub))
    for sub in ASSET:
        _lien_ket_asset(os.path.join(K.ASSETS, sub), os.path.join(dst, "public", sub))
    print(f"  Project tren Drive, chay qua ban tam: {dst}")
    return dst
