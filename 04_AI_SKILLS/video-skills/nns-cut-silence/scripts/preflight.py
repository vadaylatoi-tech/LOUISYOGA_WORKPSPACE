# -*- coding: utf-8 -*-
"""nns-cut-silence / preflight.py — KIEM INPUT TRUOC KHI LAM BAT CU VIEC GI.

In bang PASS/FAIL. Neu thieu bat ky thu gi: in khoi huong dan tung buoc (tieng Viet)
roi exit 1. Khong bao gio "chay tam".

Vi du:
    python scripts/preflight.py --video "raw.mp4"
    python scripts/preflight.py --video "raw.mp4" --out "cut.mp4"
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_io()

ROWS = []
FIX = []


def row(ok, name, detail):
    ROWS.append((bool(ok), name, detail))


def fix(title, body):
    FIX.append((title, body))


def _ver(exe):
    try:
        out = subprocess.run(
            [exe, "-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
        ).stdout.decode("utf-8", "replace")
        m = re.search(r"version\s+(\S+)", out)
        return m.group(1) if m else "?"
    except Exception:
        return "?"


def check_tools():
    for name in ("ffmpeg", "ffprobe"):
        p = shutil.which(name)
        if p:
            row(True, name, _ver(p))
        else:
            row(False, name, "khong tim thay trong PATH")
            fix(
                "Chua co %s (cong cu xu ly video/am thanh — bat buoc)" % name,
                "   Windows:  winget install Gyan.FFmpeg\n"
                "   macOS  :  brew install ffmpeg\n"
                "   Linux  :  sudo apt install ffmpeg\n"
                "   Sau khi cai, mo lai terminal roi go 'ffmpeg -version' de kiem.",
            )
            return False
    return True


def check_python():
    v = sys.version_info
    ok = v >= (3, 8)
    row(ok, "python", "%d.%d.%d" % (v[0], v[1], v[2]))
    if not ok:
        fix(
            "Python qua cu (%d.%d) — can 3.8 tro len" % (v[0], v[1]),
            "   Tai Python moi tai https://www.python.org/downloads/\n"
            "   roi chay lai bang chinh python moi do.",
        )
    try:
        import numpy

        row(True, "numpy", numpy.__version__)
    except Exception:
        row(False, "numpy", "chua cai")
        fix(
            "Chua cai thu vien numpy (de do nang luong am thanh)",
            "   Chay lenh nay:\n"
            "       pip install numpy\n"
            "   Neu may co nhieu ban Python, dung:  python -m pip install numpy",
        )
    return ok


VIDEO_EXT = (".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v", ".mts", ".m2ts")


def _list_videos(folder, limit=5):
    """Liet ke vai file video trong 1 thu muc, de goi y duong dan dung."""
    try:
        names = sorted(os.listdir(folder))
    except Exception:
        return []
    out = []
    for n in names:
        if n.lower().endswith(VIDEO_EXT):
            p = os.path.join(folder, n)
            if os.path.isfile(p):
                out.append(p)
        if len(out) >= limit:
            break
    return out


def check_video(path, allow_vfr=False):
    if not path:
        row(False, "video", "chua truyen --video")
        fix(
            "Chua chi ra video dau vao",
            "   Goi lai kem duong dan file video tho:\n"
            "       python scripts/preflight.py --video \"D:/duong/dan/raw.mp4\"",
        )
        return None
    if os.path.isdir(path):
        # Rat hay gap: nguoi dung dua THU MUC chua video thay vi chinh file.
        row(False, "video", "day la THU MUC, khong phai file video: %s" % path)
        vids = _list_videos(path)
        if vids:
            body = ("   Ban dua vao mot THU MUC. Skill can DUNG MOT file video.\n"
                    "   Trong thu muc do co nhung file video sau — chon 1 roi goi lai:\n")
            for v in vids:
                body += "       python scripts/preflight.py --video \"%s\"\n" % v.replace("\\", "/")
        else:
            body = ("   Ban dua vao mot THU MUC va trong do KHONG co file video nao\n"
                    "   (.mp4 .mov .mkv .avi .webm .m4v).\n"
                    "   Copy file video tho vao thu muc do, roi goi lai voi duong dan DEN FILE:\n"
                    "       python scripts/preflight.py --video \"%s/ten-file.mp4\"\n"
                    % path.replace("\\", "/"))
        fix("Duong dan --video la thu muc, khong phai file video", body.rstrip("\n"))
        return None
    if not os.path.isfile(path):
        row(False, "video", "khong ton tai: %s" % path)
        parent = os.path.dirname(os.path.abspath(path)) or "."
        if not os.path.isdir(parent):
            body = ("   Duong dan da nhap:  %s\n"
                    "   Ca THU MUC chua file cung khong ton tai:  %s\n"
                    "   Kiem lai chinh ta (dau \\ va / deu duoc), va nho bo duong dan trong\n"
                    "   dau ngoac kep neu co dau cach hoac dau tieng Viet.\n"
                    "   Xem thu muc cha co gi:\n"
                    "       Windows:  dir \"%s\"\n"
                    "       macOS/Linux:  ls -la \"%s\""
                    % (path, parent,
                       (os.path.dirname(parent) or parent), (os.path.dirname(parent) or parent)))
        else:
            vids = _list_videos(parent)
            body = ("   Duong dan da nhap:  %s\n"
                    "   Thu muc co that, nhung KHONG co file ten nhu vay trong do.\n" % path)
            if vids:
                body += "   Trong thu muc do dang co nhung file video sau — chon 1 roi goi lai:\n"
                for v in vids:
                    body += "       python scripts/preflight.py --video \"%s\"\n" % v.replace("\\", "/")
            else:
                body += ("   Thu muc do khong co file video nao (.mp4 .mov .mkv .avi .webm .m4v).\n"
                         "   Copy file video tho vao day roi goi lai. Xem thu muc co gi:\n"
                         "       Windows:  dir \"%s\"\n"
                         "       macOS/Linux:  ls -la \"%s\"\n" % (parent, parent))
            body = body.rstrip("\n")
        fix("Khong tim thay file video", body)
        return None
    try:
        info = C.probe(path)
    except SystemExit:
        row(False, "video", "ffprobe khong doc duoc (file hong hoac khong phai video)")
        fix(
            "File khong doc duoc bang ffprobe",
            "   Thu mo file bang trinh phat xem co phat duoc khong.\n"
            "   Neu la file dang tai/ghi do dang thi doi xong roi chay lai.\n"
            "   Kiem tay:  ffprobe -hide_banner \"%s\"" % path,
        )
        return None

    row(
        True,
        "video",
        "%dx%d %.3ffps %.2fs %d frame (%s)"
        % (info["width"], info["height"], info["fps_float"], info["duration"],
           info["nb_frames"], info["v_codec"]),
    )

    if info["has_audio"]:
        row(
            True,
            "stream audio",
            "%s %dHz %dch" % (info["a_codec"], info["a_sr"] or 0, info["a_ch"] or 0),
        )
    else:
        row(False, "stream audio", "video KHONG co tieng")
        fix(
            "Video khong co stream am thanh",
            "   Skill nay cat khoang LANG nen bat buoc phai co tieng.\n"
            "   Neu ban co file tieng roi (vd voice.wav) thi ghep vao truoc:\n"
            "       ffmpeg -i \"%s\" -i voice.wav -map 0:v -map 1:a -c:v copy -c:a aac co_tieng.mp4\n"
            "   Roi goi lai skill voi:  --video co_tieng.mp4" % path,
        )

    if info["vfr"] and allow_vfr:
        row(True, "fps co dinh (CFR)",
            "nghi la VFR (r=%.3f, avg=%.3f) nhung co --allow-vfr nen bo qua"
            % (info["fps_float"], info["avg_fps_float"] or 0.0))
    elif info["vfr"]:
        row(
            False,
            "fps co dinh (CFR)",
            "nghi la VFR: r=%.3f nhung avg=%.3f"
            % (info["fps_float"], info["avg_fps_float"] or 0.0),
        )
        fix(
            "Video co fps KHONG co dinh (VFR) — toan cat theo frame se lech",
            "   Thuong gap voi file quay tu dien thoai / ghi man hinh.\n"
            "   Chuyen sang fps co dinh truoc (giu nguyen chat luong hinh):\n"
            "       ffmpeg -i \"%s\" -c:v libx264 -crf 16 -r %d -c:a copy cfr.mp4\n"
            "   Roi goi lai voi:  --video cfr.mp4\n"
            "   (Neu ban chac chan file van deu frame, co the bo qua bang co --allow-vfr\n"
            "    khi chay plan.py — nhung khi do phai kiem ky ket qua verify.)"
            % (path, int(round(info["fps_float"]))),
        )
    else:
        row(True, "fps co dinh (CFR)", "r_frame_rate == avg_frame_rate")

    return info


def check_out(out):
    if not out:
        row(True, "--out", "chua truyen (khong sao voi buoc preflight)")
        return
    d = os.path.dirname(os.path.abspath(out))
    if os.path.isdir(d):
        if os.access(d, os.W_OK):
            row(True, "thu muc ket qua", d)
        else:
            row(False, "thu muc ket qua", "khong co quyen ghi: %s" % d)
            fix("Khong co quyen ghi vao thu muc ket qua",
                "   Doi --out sang mot thu muc khac ma ban ghi duoc.")
        return
    # chua ton tai: apply.py se tu tao, mien la thu muc cha gan nhat ghi duoc
    anc = d
    while anc and not os.path.isdir(anc):
        parent = os.path.dirname(anc)
        if parent == anc:
            break
        anc = parent
    if anc and os.path.isdir(anc) and os.access(anc, os.W_OK):
        row(True, "thu muc ket qua", "chua co, se tu tao: %s" % d)
    else:
        row(False, "thu muc ket qua", "khong tao duoc: %s" % d)
        fix(
            "Khong tao duoc thu muc de ghi file ket qua",
            "   Duong dan --out:  %s\n"
            "   O cap tren cung khong ghi duoc (%s).\n"
            "   Tao tay thu muc nay, hoac doi --out sang cho khac:\n       %s"
            % (out, anc or "?", d),
        )


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--video", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--resources", default=None)
    ap.add_argument("--allow-vfr", dest="allow_vfr", action="store_true")
    a = ap.parse_args()

    print("")
    print("  nns-cut-silence — PREFLIGHT")
    print("  " + "-" * 58)

    ok_tools = check_tools()
    check_python()
    info = check_video(a.video, a.allow_vfr) if ok_tools else None
    if not ok_tools and a.video:
        row(False, "video", "chua kiem duoc — lam buoc 1 (cai ffmpeg) roi chay lai")
    check_out(a.out)

    # Skill nay KHONG can tai nguyen ngoai (font/sfx/model onnx). Noi RO ra de
    # nguoi dung khong di tim thu muc --resources ma khong bao gio can den.
    if a.resources:
        extra = ""
        if not os.path.isdir(a.resources):
            extra = " (thu muc do khong ton tai, nhung khong sao)"
        elif not os.listdir(a.resources):
            extra = " (thu muc do dang rong, nhung khong sao)"
        row(True, "--resources",
            "KHONG can cho skill nay nen da bo qua%s" % extra)
    else:
        row(True, "tai nguyen ngoai",
            "khong can font/sfx/model — chi can ffmpeg + python + numpy")

    print("")
    for ok, name, detail in ROWS:
        tag = "[OK]  " if ok else "[THIEU]"
        print("    %-8s %-20s %s" % (tag, name, detail))
    print("")

    if FIX:
        print(C.LINE)
        print("  THIEU %d THU. LAM THEO CAC BUOC SAU ROI CHAY LAI." % len(FIX))
        print(C.LINE)
        print("")
        for i, (title, body) in enumerate(FIX, 1):
            print("  %d) %s" % (i, title))
            print("\n".join("   " + ln for ln in body.splitlines()))
            print("")
        print("  Sau khi lam xong, chay lai lenh nay de kiem:")
        print("      python scripts/preflight.py --video \"%s\"" % (a.video or "<video>"))
        print("")
        sys.exit(1)

    print("  DAY DU. Co the chay tiep.")
    print("")
    print("  Buoc tiep theo:")
    print("      python scripts/plan.py  --video \"%s\" --plan plan.json" % a.video)
    print("      python scripts/apply.py --video \"%s\" --plan plan.json --out \"%s\""
          % (a.video, a.out or "<ket-qua>.mp4"))
    print("      python scripts/verify.py --video \"%s\" --plan plan.json --out \"%s\""
          % (a.video, a.out or "<ket-qua>.mp4"))
    print("")
    if info:
        print("  Hoac lam 1 phat ca 3 buoc:")
        print("      python scripts/cut_silence.py --video \"%s\" --out \"%s\""
              % (a.video, a.out or "cut.mp4"))
        print("")
    sys.exit(0)


if __name__ == "__main__":
    main()
