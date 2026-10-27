# -*- coding: utf-8 -*-
"""nns-cut-silence / cut_silence.py — chay ca 4 buoc mot phat.

    preflight -> plan -> apply -> verify

Bat ky buoc nao that bai thi DUNG NGAY, khong chay buoc sau.

Vi du:
    python scripts/cut_silence.py --video raw.mp4 --out cut.mp4
    python scripts/cut_silence.py --video raw.mp4 --out cut.mp4 --keep 0.14 --protect "12.5-19.0"
    python scripts/cut_silence.py --video raw.mp4 --out cut.mp4 --dry-run
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _common as C  # noqa: E402

C.setup_io()


def step(name, args):
    cmd = [sys.executable, os.path.join(HERE, name)] + args
    print("")
    print(">>> " + " ".join(('"%s"' % c if " " in c else c) for c in cmd))
    rc = subprocess.call(cmd, stdin=subprocess.DEVNULL)
    if rc != 0:
        print("")
        print("  DUNG LAI o buoc %s (ma thoat %d). Khong chay buoc sau." % (name, rc))
        print("")
        sys.exit(rc)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--resources", default=None, help="khong can cho skill nay")
    ap.add_argument("--plan", default=None)
    ap.add_argument("--dry-run", dest="dry_run", action="store_true")
    # tham so cua plan.py
    ap.add_argument("--keep", default=None)
    ap.add_argument("--guard", default=None)
    ap.add_argument("--min-sil", dest="min_sil", default=None)
    ap.add_argument("--threshold-db", dest="threshold_db", default=None)
    ap.add_argument("--max-drop-peak-db", dest="max_drop_peak_db", default=None)
    ap.add_argument("--protect", default=None)
    ap.add_argument("--protect-cuts", dest="protect_cuts", action="store_true")
    ap.add_argument("--protect-cut-pad", dest="protect_cut_pad", default=None)
    ap.add_argument("--scene-threshold", dest="scene_threshold", default=None)
    ap.add_argument("--trim-edges", dest="trim_edges", action="store_true")
    ap.add_argument("--allow-vfr", dest="allow_vfr", action="store_true")
    # tham so cua apply.py
    ap.add_argument("--crf", default=None)
    ap.add_argument("--preset", default=None)
    ap.add_argument("--no-wav", dest="no_wav", action="store_true")
    ap.add_argument("--no-mux-audio", dest="no_mux_audio", action="store_true")
    ap.add_argument("--allow-no-audio", dest="allow_no_audio", action="store_true")
    # tham so cua verify.py
    ap.add_argument("--no-video-check", dest="no_video_check", action="store_true")
    a = ap.parse_args()

    plan_path = a.plan or (os.path.splitext(a.out)[0] + ".plan.json")

    pre_args = ["--video", a.video, "--out", a.out]
    if a.allow_vfr:
        pre_args.append("--allow-vfr")
    step("preflight.py", pre_args)

    plan_args = ["--video", a.video, "--plan", plan_path, "--out", a.out]
    for flag, val in (("--keep", a.keep), ("--guard", a.guard), ("--min-sil", a.min_sil),
                      ("--threshold-db", a.threshold_db),
                      ("--max-drop-peak-db", a.max_drop_peak_db),
                      ("--protect", a.protect),
                      ("--protect-cut-pad", a.protect_cut_pad),
                      ("--scene-threshold", a.scene_threshold)):
        if val is not None:
            plan_args += [flag, str(val)]
    for flag, on in (("--protect-cuts", a.protect_cuts), ("--trim-edges", a.trim_edges),
                     ("--allow-vfr", a.allow_vfr)):
        if on:
            plan_args.append(flag)
    if a.dry_run:
        plan_args.append("--dry-run")
    step("plan.py", plan_args)

    if a.dry_run:
        print("")
        print("  --dry-run: da in ke hoach, khong xuat file nao. Dung tai day.")
        print("")
        return

    apply_args = ["--video", a.video, "--plan", plan_path, "--out", a.out]
    for flag, val in (("--crf", a.crf), ("--preset", a.preset)):
        if val is not None:
            apply_args += [flag, str(val)]
    for flag, on in (("--no-wav", a.no_wav), ("--no-mux-audio", a.no_mux_audio),
                     ("--allow-no-audio", a.allow_no_audio)):
        if on:
            apply_args.append(flag)
    step("apply.py", apply_args)

    verify_args = ["--video", a.video, "--plan", plan_path, "--out", a.out]
    if a.no_video_check:
        verify_args.append("--no-video-check")
    if a.allow_no_audio and a.no_wav and a.no_mux_audio:
        verify_args.append("--allow-no-audio")
    step("verify.py", verify_args)

    tm = os.path.splitext(plan_path)[0] + ".timemap.json"
    print("")
    print("  HOAN TAT.")
    print("    video ket qua : %s" % os.path.abspath(a.out))
    if not a.no_wav:
        print("    tieng goc WAV : %s" % os.path.abspath(os.path.splitext(a.out)[0] + ".wav"))
    print("    ke hoach      : %s" % os.path.abspath(plan_path))
    print("    time map      : %s" % os.path.abspath(tm))
    print("")
    print("  Dua time map cho buoc sau (sub / SFX / overlay) de re-time theo")
    print("  timeline moi — neu khong caption se lech dan. Xem references/time-map.md.")
    print("")


if __name__ == "__main__":
    main()
