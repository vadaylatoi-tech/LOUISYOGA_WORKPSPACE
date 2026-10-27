# -*- coding: utf-8 -*-
"""preflight.py - KIEM INPUT truoc khi lam bat cu viec gi.

In bang PASS/THIEU. Neu thieu -> in khoi huong dan tieng Viet roi exit 1.
Khong bao gio doan, khong bao gio tu thay the.

  python scripts/preflight.py --video "<video>" [--resources "<thu-muc>"]
"""
from __future__ import print_function

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_stdout()

PIP = "pip install numpy"


def main():
    ap = argparse.ArgumentParser(description="Kiem input cho nns-add-sfx")
    C.add_common_args(ap, need_out=False)
    ap.add_argument("--target", type=float, default=-14.0,
                    help="do to muc tieu, LUFS (mac dinh -14)")
    ap.add_argument("--tp", type=float, default=-1.5,
                    help="tran true peak, dBTP (mac dinh -1.5)")
    a = ap.parse_args()

    print("")
    print("  nns-add-sfx / PREFLIGHT")
    print("  " + "-" * 58)
    r = C.Report()

    # ---------------------------------------------------------- 1. cong cu
    have = {}
    for exe in ("ffmpeg", "ffprobe"):
        v = C.tool_version(exe)
        have[exe] = bool(v)
        if v:
            r.ok(exe, v)
        else:
            r.fail(exe, "khong tim thay trong PATH",
                   "Chua co %s (bo cong cu xu ly video/am thanh)" % exe,
                   ["Windows - mo PowerShell roi chay:",
                    "    winget install --id Gyan.FFmpeg -e",
                    "macOS:",
                    "    brew install ffmpeg",
                    "Linux (Debian/Ubuntu):",
                    "    sudo apt install ffmpeg",
                    "Sau khi cai, mo lai terminal roi go `ffmpeg -version` de kiem.",
                    "Phai co ca 2 file: ffmpeg VA ffprobe."])

    have_np = True
    if have["ffprobe"] and have["ffmpeg"]:
        print("  %-8s %s" % ("[..]", "dang do do to cua video, cho vai giay..."))

    try:
        import numpy as np
        r.ok("numpy", np.__version__)
    except ImportError:
        have_np = False
        r.fail("numpy", "chua cai",
               "Chua cai thu vien Python numpy (de tron am thanh)",
               ["Chay lenh nay:", "    " + PIP,
                "Neu may co nhieu ban Python, cai dung ban dang chay script nay:",
                "    python -m pip install numpy",
                "Kiem lai bang: python -c \"import numpy; print(numpy.__version__)\""])

    # ffmpeg build phai co alimiter + ebur128 (khong phai build nao cung day du)
    if have["ffmpeg"]:
        for filt in ("alimiter", "ebur128", "volume"):
            if C.ffmpeg_has("filters", filt):
                r.ok("filter " + filt, "co")
            else:
                r.fail("filter " + filt, "ffmpeg nay khong co filter do",
                       "ffmpeg thieu filter `%s`" % filt,
                       ["Ban ffmpeg dang cai bi cat bot bo loc.",
                        "Cai ban day du (gyan.dev / BtbN full build), vi du:",
                        "    winget install --id Gyan.FFmpeg -e",
                        "Kiem lai: ffmpeg -filters | findstr %s" % filt])

    # ---------------------------------------------------------- 2. video vao
    vid = None
    if not os.path.isfile(a.video):
        # Noi ro la SAI TEN FILE hay SAI THU MUC - hai loi nay sua khac nhau.
        parent = os.path.dirname(os.path.abspath(a.video))
        steps = ["Duong dan ban dua: %s" % C.disp(a.video)]
        if os.path.isdir(a.video):
            steps += ["Day la mot THU MUC, khong phai file video.",
                      "Chi ra dung file, vi du: --video \"%s/ten-video.mp4\""
                      % C.disp(a.video.rstrip("/\\"))]
        elif not os.path.isdir(parent):
            steps += ["Thu muc chua no cung khong ton tai: %s" % C.disp(parent),
                      "Kiem lai tu dau duong dan (o dia dung chua? ten thu muc dung chua?).",
                      "Windows: mo File Explorer, bam vao o duong dan, copy nguyen van,",
                      "roi dan vao trong dau ngoac kep.",
                      "Goi lai voi:  --video \"<duong-dan-video-that>\""]
        else:
            vids = []
            try:
                for f in sorted(os.listdir(parent)):
                    if f.lower().endswith((".mp4", ".mov", ".mkv", ".webm", ".m4v",
                                           ".avi")):
                        vids.append(f)
            except OSError:
                pass
            steps += ["Thu muc co that, nhung khong co file ten do -> gan nhu chac"
                      " chan la SAI TEN FILE."]
            if vids:
                steps += ["Trong thu muc %s co %d file video:" % (C.disp(parent),
                                                                 len(vids))]
                for f in vids[:6]:
                    steps.append("    %s" % f)
                if len(vids) > 6:
                    steps.append("    ... con %d file nua" % (len(vids) - 6))
                steps += ["Copy dung ten o tren, vi du:",
                          "    --video \"%s/%s\"" % (C.disp(parent), vids[0])]
            else:
                steps += ["Thu muc do khong co file video nao (.mp4/.mov/.mkv/...).",
                          "Kiem lai ban dat video o dau.",
                          "Goi lai voi:  --video \"<duong-dan-video-that>\""]
        r.fail("video", "khong ton tai: %s" % a.video,
               "Khong tim thay file video dau vao", steps)
    elif not have["ffprobe"]:
        r.warn("video", "chua kiem duoc vi thieu ffprobe (xem muc ffprobe o tren)")
    else:
        vid = C.probe_media(a.video)
        if not vid["has_video"]:
            r.fail("video", "file khong co luong hinh",
                   "File dua vao khong phai video",
                   ["File: %s" % a.video,
                    "Skill nay chen SFX vao video va COPY nguyen luong hinh,",
                    "nen file phai co hinh. Neu ban chi co am thanh, dung ffmpeg truc tiep."])
        else:
            r.ok("video", "%dx%d %.3ffps %.2fs %d frame (header)"
                 % (vid["width"], vid["height"], vid["fps"], vid["duration"],
                    vid["nb_frames"]))
        if not vid["has_audio"]:
            r.fail("audio goc", "video khong co luong tieng",
                   "Video khong co am thanh",
                   ["File: %s" % a.video,
                    "Skill nay TRON SFX LEN TREN tieng goc, nen phai co tieng goc.",
                    "Neu ban muon dat SFX len video im lang, hay ghep loi noi vao truoc:",
                    "    ffmpeg -i \"<video-im-lang>\" -i \"<loi-noi.wav>\" \\",
                    "           -c:v copy -c:a aac -b:a 256k -shortest \"<video-co-tieng.mp4>\"",
                    "Roi goi lai skill voi file vua ghep."])
        else:
            r.ok("audio goc", "%s %d Hz %dch %.2fs"
                 % (vid["acodec"], vid["sample_rate"], vid["channels"],
                    vid["adur"] or vid["duration"]))

    # ---------------------------------------------------------- 3. thu vien SFX
    # Nguoi dung DA CHI RO --resources thi khong duoc am tham quay ve assets/sfx.
    res_prob = C.resources_problem(a.resources)
    sfx_dir, sfx_files, src, notes = C.find_sfx_library(a.resources)
    usable = []
    if res_prob:
        kind, path = res_prob
        head, lines = C.resources_guidance(kind, path)
        detail = ("duong dan khong ton tai" if kind == "notdir"
                  else "khong co file .mp3/.wav nao trong do")
        r.fail("--resources", "%s: %s" % (detail, C.disp(path)), head, lines)
        notes = []
    elif not sfx_files:
        detail = "; ".join(notes) if notes else "khong tim thay file .mp3/.wav nao"
        n_bundled = 0
        if os.path.isdir(C.BUNDLED_SFX):
            n_bundled = len([f for f in os.listdir(C.BUNDLED_SFX)
                             if f.lower().endswith(C.SFX_EXT)])
        notes = []  # da noi trong dong THIEU roi, khong lap lai
        r.fail("thu vien SFX", detail,
               "Khong co thu vien hieu ung am thanh (SFX)",
               ["Cach A - dung file kem san trong skill (nhanh nhat):",
                "    Bo han tham so --resources. Skill co san %d file trong assets/sfx/."
                % n_bundled,
                "    Neu cach nay cung bao thieu thi thu muc assets/sfx/ da bi mat khi copy",
                "    -> copy lai ca thu muc skill, giu nguyen assets/.",
                "Cach B - dung thu vien rieng cua ban:",
                "    1. Tao thu muc:   <duong-dan-ban-chon>/sound-effects/",
                "    2. Copy cac file .mp3 hoac .wav vao do (whoosh, pop, ting, punch,",
                "       riser... tai mien phi tren pixabay.com/sound-effects hoac freesound.org)",
                "    3. Goi lai voi:   --resources \"<duong-dan-ban-chon>\"",
                "    Skill tim DE QUY, chap nhan ten thu muc: sound-effects/ sfx/ audio/sfx/"])
    elif not (have["ffmpeg"] and have_np):
        r.warn("thu vien SFX", "%d file - chua giai ma kiem duoc vi thieu %s"
               % (len(sfx_files),
                  "ffmpeg" if not have["ffmpeg"] else "numpy"))
        r.warn("thu muc SFX", "%s (nguon: %s)" % (C.disp(sfx_dir), src))
    else:
        # kiem THAT: giai ma va do onset vai file, khong tin ten file
        try:
            import numpy  # noqa: F401
            probe_n = min(len(sfx_files), 12)
            step = max(1, len(sfx_files) // probe_n)
            sample = sfx_files[::step][:probe_n]
            for p in sample:
                info = C.analyse_sfx(p)
                if info.get("usable"):
                    usable.append(p)
            if not usable:
                r.fail("thu vien SFX", "%d file nhung khong file nao dung duoc"
                       % len(sfx_files),
                       "Thu vien SFX co file nhung khong file nao phat ra tieng",
                       ["Thu muc: %s" % sfx_dir,
                        "Da thu giai ma %d file, tat ca im lang hoac loi." % len(sample),
                        "Kiem thu bang:  ffplay \"<mot-file-trong-do>\"",
                        "Neu file hong, tai lai bo SFX moi roi tro --resources vao do."])
            else:
                r.ok("thu vien SFX", "%d file (.mp3/.wav) - nguon: %s"
                     % (len(sfx_files), src))
                r.ok("SFX dung duoc", "%d/%d file thu nghiem co onset ro rang"
                     % (len(usable), len(sample)))
                r.ok("thu muc SFX", C.disp(sfx_dir))
        except ImportError:
            r.warn("thu vien SFX", "%d file - chua kiem duoc vi thieu numpy"
                   % len(sfx_files))
    for n in notes:
        r.warn("ghi chu", n)

    # ------------------------------------------- 4. do do to hien tai cua video
    if vid and vid.get("has_audio") and have["ffmpeg"]:
        m = C.measure_loudness(a.video)
        r.ok("do to hien tai", "I=%.1f LUFS  LRA=%.1f LU  TP=%.1f dBFS"
             % (m["I"], m["LRA"], m["TP"]))
        gain = a.target - m["I"]
        r.ok("du kien can", "gain %+.1f dB de len %.1f LUFS (tran TP %.1f dBTP)"
             % (gain, a.target, a.tp))
        if m["I"] > a.target + 3.0:
            r.warn("canh bao", "video goc DA to hon muc tieu %.1f LU - se phai HA gain"
                   % (m["I"] - a.target))
        if m["LRA"] < 2.0:
            r.warn("canh bao", "LRA %.1f LU rat hep, file nay co the da bi nen san"
                   % m["LRA"])

    # ---------------------------------------------------------- ket luan
    print("")
    r.print_table()
    cmd = "python scripts/preflight.py --video \"%s\"" % a.video
    if a.resources:
        cmd += " --resources \"%s\"" % a.resources
    r.finish(cmd)

    print("")
    print("  Buoc tiep theo:")
    print("    1) python scripts/probe.py   --video \"%s\" --out sfx_onsets.json%s"
          % (a.video, (" --resources \"%s\"" % a.resources) if a.resources else ""))
    print("    2) python scripts/plan.py    --video \"%s\" --out sfx_cues.json "
          "--onsets sfx_onsets.json%s"
          % (a.video, (" --resources \"%s\"" % a.resources) if a.resources else ""))
    print("    3) python scripts/apply.py   --video \"%s\" --out ket_qua.mp4 "
          "--cues sfx_cues.json" % a.video)
    print("    4) python scripts/verify.py  --video \"%s\" --out ket_qua.mp4 "
          "--cues sfx_cues.json" % a.video)
    print("")


if __name__ == "__main__":
    main()
