# -*- coding: utf-8 -*-
"""Ve file .ass vao video (burn-in). Tieng giu nguyen, khong ma hoa lai.

    python scripts/burn.py --video <video> --out <video_ra.mp4> [--crf 18]

Hai cai bay da tranh o day:
  1. KHONG dung drawtext (segfault "Fontconfig error: Cannot load default
     config file"). Dung subtitles=<file>.ass:fontsdir=<dir>.
  2. KHONG nhet duong dan tuyet doi vao filter: 'C:/...' co dau hai cham,
     ffmpeg hieu la dau phan cach option roi bao loi. Cach lam: copy .ass va
     font vao 1 thu muc tam, chay ffmpeg voi cwd la thu muc do, filter chi
     dung ten file tuong doi.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nnscommon as C  # noqa: E402


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--resources")
    ap.add_argument("--ass", default=None,
                    help="mac dinh la <out-stem>.ass do build_ass.py sinh ra")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--reencode-audio", action="store_true",
                    help="ma hoa lai tieng thanh aac 192k thay vi copy")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    C.require_video_out(a, "burn.py")

    if not os.path.isfile(a.video):
        C.die("khong thay video: %s" % a.video)
    ass = a.ass or C.side_path(a.out, ".ass")
    if not os.path.isfile(ass):
        C.die("chua co file .ass: %s\n"
              "  Chay buoc truoc:\n"
              '      python scripts/build_ass.py --video "%s" --out "%s"'
              % (ass, a.video, a.out))
    plan_path = C.side_path(a.out, ".plan.json")
    font_dir = font_file = None
    if os.path.isfile(plan_path):
        plan = C.read_json(plan_path)
        font_file = plan.get("font_file")
        font_dir = plan.get("font_dir")
    if not font_file or not os.path.isfile(font_file):
        res = C.resolve_font(a.resources, None)
        if not res["file"]:
            C.die("khong tim lai duoc font de ve chu.\n"
                  '  Chay:  python scripts/preflight.py --video "%s"' % a.video)
        if res.get("resources_unused"):
            C.die("thu muc --resources ban dua khong co font tieng Viet nao "
                  "dung duoc.\n"
                  + "\n".join("  " + ln
                              for ln in C.huong_dan_font_resources(res)))
        font_file, font_dir = res["file"], res["dir"]

    info = C.probe_video(a.video)
    print("")
    print("  " + C.hr("-"))
    print("  BUOC 4/4 — ve sub vao video")
    print("  " + C.hr("-"))
    print("  vao   : %s (%d frame, %.4g fps)"
          % (a.video, info["nb_frames"], info["fps"]))
    print("  sub   : %s" % ass)
    print("  font  : %s" % font_file)
    print("  ra    : %s" % a.out)
    print("  hinh  : libx264 crf %d preset %s | tieng: %s"
          % (a.crf, a.preset, "aac 192k" if a.reencode_audio else "copy nguyen"))

    if a.dry_run:
        print("  [dry-run] khong ma hoa gi.")
        return

    out_abs = os.path.abspath(a.out)
    d = os.path.dirname(out_abs)
    if d and not os.path.isdir(d):
        os.makedirs(d)

    tmp = tempfile.mkdtemp(prefix="nnsburn_")
    try:
        fdir = os.path.join(tmp, "fonts")
        os.makedirs(fdir)
        shutil.copy2(font_file, os.path.join(fdir, os.path.basename(font_file)))
        shutil.copy2(ass, os.path.join(tmp, "sub.ass"))
        audio = (["-c:a", "aac", "-b:a", "192k"] if a.reencode_audio
                 else ["-c:a", "copy"])
        cmd = ["ffmpeg", "-v", "error", "-stats", "-y",
               "-i", os.path.abspath(a.video),
               "-vf", "subtitles=sub.ass:fontsdir=fonts",
               "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
               "-pix_fmt", "yuv420p", "-r", "%.10g" % info["fps"]] + audio + [
               "-movflags", "+faststart", out_abs]
        t0 = time.time()
        _out, err, rc = C.run(cmd, cwd=tmp, check=False)
        if rc != 0 and not a.reencode_audio and "copy" in err.lower():
            print("  copy tieng khong duoc, ma hoa lai thanh aac...")
            cmd = [c for c in cmd]
            i = cmd.index("-c:a")
            cmd[i:i + 2] = ["-c:a", "aac", "-b:a", "192k"]
            _out, err, rc = C.run(cmd, cwd=tmp, check=False)
        if rc != 0:
            C.die("ffmpeg ve sub that bai (exit %d).\n%s" % (rc, err[-3000:]))
        print("  xong sau %.1fs" % (time.time() - t0))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if not os.path.isfile(out_abs) or os.path.getsize(out_abs) < 10000:
        C.die("file ra khong hop le hoac qua nho: %s" % out_abs)
    got = C.probe_video(out_abs)
    print("  file ra: %dx%d %.4gfps %.2fs %d frame"
          % (got["width"], got["height"], got["fps"], got["duration"],
             got["nb_frames"]))
    print("")
    print("  Con 1 buoc nua — PHAI chay de biet chu co that su hien khong:")
    print('      python scripts/verify.py --video "%s" --out "%s"'
          % (a.video, a.out))


if __name__ == "__main__":
    C.run_main(main)
