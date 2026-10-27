# -*- coding: utf-8 -*-
"""Chay ca day: preflight -> nhan dang -> sua tu -> xuat .ass -> ve -> kiem.

    python scripts/autosub.py --video <video> --out <video_ra.mp4> \
        [--resources <thu-muc>] [--y 1536] [--safe "0-12:1100,12-30:1536"] \
        [--fixes luat.json] [--max-words 4] [--dry-run]

Bat ky buoc nao that bai la DUNG NGAY, khong chay tiep.
Chi bao thanh cong khi verify.py tra ve 0.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nnscommon as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def step(name, script, args, allow_fail_msg=None):
    print("")
    print("  " + C.hr("#"))
    print("  >>> %s" % name)
    print("  " + C.hr("#"))
    cmd = [sys.executable, os.path.join(HERE, script)] + args
    # PHAI flush: neu khong, chu cua tien trinh con in ra truoc tieu de nay
    sys.stdout.flush()
    sys.stderr.flush()
    rc = subprocess.call(cmd)
    sys.stdout.flush()
    if rc != 0:
        print("")
        print("  " + C.hr("!"))
        print("  DUNG LAI o buoc: %s  (exit %d)" % (name, rc))
        if allow_fail_msg:
            print("  " + allow_fail_msg)
        print("  " + C.hr("!"))
        sys.exit(rc)


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    # KHONG dung required=True: argparse se in loi tieng Anh + dump usage.
    # Tu kiem de bao bang tieng Viet, noi ro phai lam gi.
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--resources")
    ap.add_argument("--dry-run", action="store_true")
    # nhan dang
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--language", default="vi")
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    ap.add_argument("--compute-type", default=None)
    ap.add_argument("--no-vad", action="store_true")
    ap.add_argument("--force", action="store_true", help="nhan dang lai, bo cache")
    # sua tu
    ap.add_argument("--fixes")
    ap.add_argument("--no-default-fixes", action="store_true")
    ap.add_argument("--no-dur-fix", action="store_true")
    # gom cum / kieu chu
    ap.add_argument("--font")
    ap.add_argument("--max-words", type=int, default=4)
    ap.add_argument("--max-chars", type=int, default=22)
    ap.add_argument("--gap", type=float, default=0.35)
    ap.add_argument("--y", type=int, default=None)
    ap.add_argument("--safe", default=None)
    ap.add_argument("--font-size", type=int, default=None)
    ap.add_argument("--outline", type=float, default=None)
    ap.add_argument("--base-color", default="#FFFFFF")
    ap.add_argument("--active-color", default="#FFD600")
    ap.add_argument("--outline-color", default="#000000")
    ap.add_argument("--no-break-punct", action="store_true")
    ap.add_argument("--no-measure", action="store_true")
    # ve
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    a = ap.parse_args()

    if not a.video or not a.out:
        thieu = []
        if not a.video:
            thieu.append("--video (video co tieng noi, can chen sub)")
        if not a.out:
            thieu.append("--out (duong dan file video KET QUA se ghi ra)")
        C.die("thieu tham so bat buoc: %s\n"
              "  Goi lai day du 2 tham so nay:\n"
              '      python scripts/autosub.py --video "D:\\quay\\video_tho.mp4" '
              '--out "D:\\quay\\video_co_sub.mp4"\n'
              "  Neu ban co thu muc font rieng thi them:\n"
              '      --resources "D:\\shared-sources"'
              % ", ".join(thieu))

    base = ["--video", a.video, "--out", a.out]
    if a.resources:
        base += ["--resources", a.resources]
    dry = ["--dry-run"] if a.dry_run else []

    print("")
    print("  " + C.hr("="))
    print("  nns-auto-sub — chen sub karaoke word-by-word tieng Viet")
    print("  " + C.hr("="))
    print("  video vao : %s" % a.video)
    print("  video ra  : %s" % a.out)
    print("  tai nguyen: %s" % (a.resources or "(dung assets kem san trong skill)"))
    if a.dry_run:
        print("  CHE DO DRY-RUN: chi lap ke hoach, khong xuat file nao.")

    pf = ["--video", a.video, "--model", a.model]
    if a.resources:
        pf += ["--resources", a.resources]
    if a.font:
        pf += ["--font", a.font]
    step("BUOC 0 — preflight (kiem input)", "preflight.py", pf,
         "Lam theo dung khoi huong dan o tren roi chay lai lenh nay.")

    tr = base + ["--model", a.model, "--language", a.language,
                 "--device", a.device] + dry
    if a.compute_type:
        tr += ["--compute-type", a.compute_type]
    if a.no_vad:
        tr += ["--no-vad"]
    if a.force:
        tr += ["--force"]
    step("BUOC 1 — nhan dang loi noi", "transcribe.py", tr)

    words_path = C.side_path(a.out, ".words.json")
    if a.dry_run and not os.path.isfile(words_path):
        # DRY-RUN tren video CHUA tung nhan dang: khong co transcript thi khong
        # the lap ke hoach cum chu duoc. Bao ro va DUNG BINH THUONG (exit 0),
        # tuyet doi khong bao loi cho 1 tham so hop le.
        print("")
        print("  " + C.hr("="))
        print("    DRY-RUN dung o day: chua co transcript nen chua lap duoc")
        print("    ke hoach chi tiet (cum chu / mau / cho dat).")
        print("  " + C.hr("="))
        print("    Da kiem xong va DAT: ffmpeg, thu vien Python, video, font.")
        print("    Cac buoc SE chay khi ban lam that:")
        print("      1. transcribe.py  — nhan dang loi noi (model %s)" % a.model)
        print("         se ghi: %s" % os.path.basename(words_path))
        print("      2. fix_tokens.py  — sua ten rieng (Cloud->Claude...) "
              "va chan do dai tu")
        print("      3. build_ass.py   — gom cum <=%d tu, xuat %s"
              % (a.max_words, os.path.basename(C.side_path(a.out, ".ass"))))
        print("      4. burn.py        — ve chu vao video, ghi %s"
              % os.path.basename(a.out))
        print("      5. verify.py      — do lai bang pixel xem chu co hien that")
        print("")
        print("    Muon xem ke hoach CHI TIET ma van chua ve gi vao video:")
        print("      1) nhan dang truoc (chi ghi 1 file .words.json):")
        print('             python scripts/transcribe.py --video "%s" --out "%s"'
              % (a.video, a.out))
        print("      2) roi chay lai dung lenh nay voi --dry-run.")
        print("    Hoac bo --dry-run de lam that ngay bay gio.")
        print("")
        return

    fx = base + dry
    if a.fixes:
        fx += ["--fixes", a.fixes]
    if a.no_default_fixes:
        fx += ["--no-default-fixes"]
    if a.no_dur_fix:
        fx += ["--no-dur-fix"]
    step("BUOC 2 — sua ten rieng va do dai tu", "fix_tokens.py", fx)

    bd = base + ["--max-words", str(a.max_words), "--max-chars", str(a.max_chars),
                 "--gap", str(a.gap), "--base-color", a.base_color,
                 "--active-color", a.active_color,
                 "--outline-color", a.outline_color] + dry
    for flag, val in (("--y", a.y), ("--safe", a.safe),
                      ("--font-size", a.font_size), ("--outline", a.outline),
                      ("--font", a.font)):
        if val is not None:
            bd += [flag, str(val)]
    if a.no_break_punct:
        bd += ["--no-break-punct"]
    if a.no_measure:
        bd += ["--no-measure"]
    step("BUOC 3 — gom cum va xuat .ass", "build_ass.py", bd)

    if a.dry_run:
        print("")
        print("  " + C.hr("="))
        print("    DRY-RUN xong. Chua ve gi vao video.")
        print("    Bo --dry-run de lam that.")
        print("  " + C.hr("="))
        return

    step("BUOC 4 — ve sub vao video", "burn.py",
         base + ["--crf", str(a.crf), "--preset", a.preset])
    step("BUOC 5 — kiem ket qua", "verify.py", base)

    print("")
    print("  " + C.hr("="))
    print("    XONG. verify.py da do va bao DAT.")
    print("  " + C.hr("="))
    print("    video : %s" % os.path.abspath(a.out))
    print("    sub   : %s" % C.side_path(a.out, ".ass"))
    print("")
    print("    Muon sua chu / doi cho dat sub thi KHONG can nhan dang lai:")
    print("      1. sua %s" % os.path.basename(C.side_path(a.out, ".words.json")))
    print("         (hoac lam file --fixes rieng, xem references/sua-token.md)")
    print("      2. chay lai tu buoc 2:")
    print('         python scripts/fix_tokens.py --video "%s" --out "%s"'
          % (a.video, a.out))
    print('         python scripts/build_ass.py  --video "%s" --out "%s" --y <y moi>'
          % (a.video, a.out))
    print('         python scripts/burn.py       --video "%s" --out "%s"'
          % (a.video, a.out))
    print('         python scripts/verify.py     --video "%s" --out "%s"'
          % (a.video, a.out))
    print("")


if __name__ == "__main__":
    C.run_main(main)
