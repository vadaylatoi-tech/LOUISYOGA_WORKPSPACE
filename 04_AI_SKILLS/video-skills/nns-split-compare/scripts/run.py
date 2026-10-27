# -*- coding: utf-8 -*-
"""Chay ca chuoi: preflight -> (cat khoang lang) -> plan -> chrome -> apply -> verify.

Chi truyen 1 file tho:
    python scripts/run.py --video "raw.mp4" --out "SO_SANH.mp4"
Da co san ban AI thi bo qua buoc cat:
    python scripts/run.py --video "raw.mp4" --right "ai.mp4" --out "SO_SANH.mp4"
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))


def step(cmd):
    print("")
    print(">>> " + " ".join(str(c) for c in cmd))
    p = subprocess.run(cmd)
    if p.returncode != 0:
        C.die("Buoc tren that bai (ma %d). Dung lai, khong chay tiep." % p.returncode,
              p.returncode)


def main():
    C.setup_io()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", "--left", dest="video", required=True,
                    help="video THO (se hien ben trai)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--right", default=None,
                    help="ban AI da cat. Bo qua = tu cat bang nns-cut-silence")
    ap.add_argument("--resources", default=None)
    ap.add_argument("--label-left", dest="ll", default="BẢN GỐC")
    ap.add_argument("--label-right", dest="lr", default="AI ĐÃ CẮT")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--keep-work", dest="keep", action="store_true",
                    help="giu lai thu muc lam viec (PNG chrome, frame verify)")
    ap.add_argument("--dry-run", dest="dry", action="store_true")
    a = ap.parse_args()

    py = sys.executable
    plan_p = C.sidecar(a.out, ".plan.json")
    work = C.sidecar(a.out, "_work")

    pre = [py, os.path.join(HERE, "preflight.py"), "--video", a.video, "--out", a.out]
    if a.right:
        pre += ["--right", a.right]
    if a.resources:
        pre += ["--resources", a.resources]
    step(pre)

    right = a.right
    if not right:
        cut = os.path.join(SKILLS, "nns-cut-silence", "scripts", "cut_silence.py")
        if not os.path.isfile(cut):
            C.die("Khong thay nns-cut-silence. Tu cat roi truyen qua --right.")
        right = C.sidecar(a.out, "_ai.mp4")
        print("")
        print("  Chua co --right -> tu cat khoang lang bang nns-cut-silence.")
        step([py, cut, "--video", a.video, "--out", right])

    step([py, os.path.join(HERE, "plan.py"), "--left", a.video, "--right", right,
          "--plan", plan_p, "--label-left", a.ll, "--label-right", a.lr]
         + (["--dry-run"] if a.dry else []))
    if a.dry:
        print("")
        print("  --dry-run: dung o day, khong ve, khong render.")
        return

    ch = [py, os.path.join(HERE, "chrome.py"), "--plan", plan_p, "--outdir", work]
    if a.resources:
        ch += ["--resources", a.resources]
    step(ch)

    step([py, os.path.join(HERE, "apply.py"), "--plan", plan_p, "--chrome", work,
          "--out", a.out, "--crf", str(a.crf), "--preset", a.preset])

    step([py, os.path.join(HERE, "verify.py"), "--plan", plan_p, "--out", a.out,
          "--workdir", os.path.join(work, "verify")])

    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)

    plan = C.load_json(plan_p)
    print("")
    print("  HOAN TAT.")
    print("    video so sanh : %s" % a.out)
    print("    ban AI da cat : %s" % right)
    print("    ke hoach      : %s" % plan_p)
    print("    %s -> %s  (tiet kiem %.2fs, %.1f%%)"
          % (plan["left"]["pill"], plan["right"]["pill"],
             plan["saving"]["sec"], plan["saving"]["pct"]))
    print("")


if __name__ == "__main__":
    main()
