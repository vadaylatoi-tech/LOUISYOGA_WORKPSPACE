# -*- coding: utf-8 -*-
"""nns-auto-sub / BUOC 0 — kiem input truoc khi lam bat cu viec gi.

    python scripts/preflight.py --video "<video>" [--resources "<thu-muc>"]

In bang PASS/FAIL. Neu thieu bat ky thu gi: in KHOI HUONG DAN tung buoc
roi exit 1. Khong bao gio doan, khong bao gio tu thay the.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nnscommon as C  # noqa: E402

OK, MISS, NOTE = "OK", "THIEU", "LUU Y"


class Report(object):
    def __init__(self):
        self.rows = []
        self.problems = []

    def add(self, status, label, detail):
        self.rows.append((status, label, detail))

    def problem(self, title, steps):
        self.problems.append((title, steps))

    def missing_count(self):
        return sum(1 for s, _l, _d in self.rows if s == MISS)

    def dump(self):
        print("")
        print("  " + C.hr("-"))
        print("  nns-auto-sub — KIEM INPUT (preflight)")
        print("  " + C.hr("-"))
        for status, label, detail in self.rows:
            tag = "[%s]" % status
            print("  %-8s %-22s %s" % (tag, label, detail))
        print("")
        n_miss = self.missing_count()
        if not self.problems and not n_miss:
            print("  => DAY DU. Chay tiep duoc.")
            print("")
            return 0
        if not self.problems:
            # chan lo: co dong THIEU ma quen dang ky buoc huong dan
            self.problem(
                "Co %d thu con THIEU o bang tren" % n_miss,
                ["Xem lai cac dong [THIEU] o bang tren va bo sung thu con thieu.",
                 "Neu khong ro thieu gi, chay lai lenh nay va gui nguyen ket qua:",
                 '    python scripts/preflight.py --video "<video>"'])
        n = len(self.problems)
        print("  " + C.hr("="))
        print("    THIEU %d THU. LAM THEO CAC BUOC SAU ROI CHAY LAI." % n)
        print("  " + C.hr("="))
        print("")
        for i, (title, steps) in enumerate(self.problems, 1):
            print("  %d) %s" % (i, title))
            for line in steps:
                print("     " + line)
            print("")
        print("  Sau khi lam xong, chay lai lenh nay de kiem:")
        print('      python scripts/preflight.py --video "<video>" '
              '[--resources "<thu-muc>"]')
        print("")
        return 1


# ---------------------------------------------------------------------------

def check_tools(rep):
    for exe, why in (("ffmpeg", "de ve chu vao video"),
                     ("ffprobe", "de doc thong so video")):
        ver = C.tool_version(exe)
        if ver:
            rep.add(OK, exe, ver)
        else:
            rep.add(MISS, exe, "khong tim thay trong PATH")
            rep.problem(
                "Chua co %s (%s)" % (exe, why),
                ['Windows: tai ban "full" tai  https://www.gyan.dev/ffmpeg/builds/',
                 '  giai nen ra vd  C:\\ffmpeg  roi them  C:\\ffmpeg\\bin  vao PATH.',
                 'macOS:   brew install ffmpeg',
                 'Linux:   sudo apt install ffmpeg',
                 'Kiem lai:  %s -version' % exe])


def check_libass(rep):
    if not C.which("ffmpeg"):
        return
    out, _err, _rc = C.run(["ffmpeg", "-v", "quiet", "-filters"], check=False)
    has_sub = any(line.split()[1] == "subtitles"
                  for line in out.splitlines()
                  if len(line.split()) > 1)
    if has_sub:
        rep.add(OK, "libass (subtitles)", "ffmpeg co filter subtitles")
    else:
        rep.add(MISS, "libass (subtitles)", "ffmpeg khong co filter subtitles")
        rep.problem(
            "Ban ffmpeg dang co KHONG duoc build kem libass, khong ve duoc sub",
            ['Can 1 ban ffmpeg co  --enable-libass  (kem --enable-libfreetype,',
             '  --enable-libfribidi, --enable-libharfbuzz de dau tieng Viet dung cho).',
             'Windows: tai ban "full" tai  https://www.gyan.dev/ffmpeg/builds/',
             'macOS:   brew install ffmpeg',
             'Kiem lai:  ffmpeg -filters | findstr subtitles     (Windows)',
             '           ffmpeg -filters | grep subtitles        (macOS/Linux)'])


def check_python_libs(rep, need_whisper=True):
    try:
        import numpy
        rep.add(OK, "numpy", numpy.__version__)
    except Exception:
        rep.add(MISS, "numpy", "chua cai")
        rep.problem(
            "Chua cai numpy (de do pixel khi kiem font va kiem ket qua)",
            ["Chay lenh nay:", "    pip install numpy",
             "Kiem lai:  python -c \"import numpy; print(numpy.__version__)\""])
    if not need_whisper:
        return
    try:
        import faster_whisper
        ver = getattr(faster_whisper, "__version__", "?")
        rep.add(OK, "faster-whisper", ver)
    except Exception:
        rep.add(MISS, "faster-whisper", "chua cai")
        rep.problem(
            "Chua cai thu vien faster-whisper (de nhan dang loi noi ra chu)",
            ["Chay lenh nay:", "    pip install faster-whisper",
             "Lan chay dau tien no se TU TAI model ve (large-v3 ~1.5 GB), can mang.",
             "May yeu / khong muon tai nhieu: dung model nho hon bang",
             "    --model small     (hoac  --model medium )",
             "Kiem lai:  python -c \"import faster_whisper; print('ok')\""])


def check_model_cache(rep, model):
    """Model Whisper da tai ve chua — thieu thi chi CANH BAO, khong chan."""
    home = os.path.expanduser("~")
    roots = [os.environ.get("HF_HOME"), os.environ.get("HUGGINGFACE_HUB_CACHE"),
             os.path.join(home, ".cache", "huggingface", "hub")]
    tag = "models--Systran--faster-whisper-%s" % model
    for r in roots:
        if not r:
            continue
        for cand in (os.path.join(r, tag), os.path.join(r, "hub", tag)):
            if os.path.isdir(cand):
                rep.add(OK, "model %s" % model, "da tai san trong may")
                return
    if os.path.isdir(model):
        rep.add(OK, "model %s" % model, "dung thu muc model tai cho")
        return
    rep.add(NOTE, "model %s" % model,
            "chua co trong cache — lan chay dau se tai ve, can mang")


def check_video(rep, video):
    if not video:
        rep.add(MISS, "video", "chua dua --video")
        rep.problem(
            "Chua chi ra video can chen sub",
            ["Goi lai voi duong dan video tho cua ban:",
             '    python scripts/preflight.py --video "D:\\quay\\video_tho.mp4"'])
        return None
    if not os.path.isfile(video):
        rep.add(MISS, "video", "khong thay file: %s" % video)
        parent = os.path.dirname(os.path.abspath(video))
        steps = ["Duong dan da nhan: %s" % video]
        if os.path.isdir(video):
            steps += ["Duong dan nay la mot THU MUC, khong phai file video.",
                      "Chi thang vao 1 file .mp4/.mov/.mkv ben trong no."]
        elif os.path.isdir(parent):
            steps += ["Thu muc co that, nhung khong co file ten nhu vay.",
                      "Chay lenh nay de xem ten file dung trong thu muc do:",
                      '    dir "%s"                 (Windows)' % parent,
                      '    ls -la "%s"              (macOS/Linux)' % parent,
                      "roi copy dung ten file vao --video."]
        else:
            steps += ["Ca thu muc chua no cung khong ton tai:",
                      "    %s" % parent,
                      "Chay lenh nay de xem thu muc cha co gi:",
                      '    dir "%s"' % os.path.dirname(parent),
                      "Neu video con nam trong dien thoai / the nho thi copy vao",
                      "may truoc, doi copy XONG han roi hay goi lai."]
        steps += ["Neu duong dan co dau cach thi PHAI boc trong dau ngoac kep:",
                  '    --video "D:\\thu muc co dau cach\\video.mp4"']
        rep.problem("Duong dan video khong ton tai", steps)
        return None
    try:
        info = C.probe_video(video)
    except C.ThieuCongCu as exc:
        # chua co ffmpeg/ffprobe -> khong do duoc gi. Buoc cai ffmpeg da co o tren.
        rep.add(NOTE, "video", "chua doc duoc vi thieu %s (xem buoc 1)" % exc.exe)
        return None
    except SystemExit:
        rep.add(MISS, "video", "ffprobe khong doc duoc file nay")
        rep.problem(
            "File dua vao khong phai video hop le (ffprobe khong doc duoc)",
            ["Kiem thu bang tay:", '    ffprobe -hide_banner "%s"' % video,
             "Neu file quay tu dien thoai chua copy xong thi copy lai cho du."])
        return None
    rep.add(OK, "video", "%dx%d %.4gfps %.2fs %d frame"
            % (info["width"], info["height"], info["fps"], info["duration"],
               info["nb_frames"]))
    if C.has_audio(video):
        rep.add(OK, "tieng trong video", "co (de nhan dang loi noi)")
    else:
        rep.add(MISS, "tieng trong video", "video khong co tieng")
        rep.problem(
            "Video khong co tieng nen khong nhan dang duoc loi noi",
            ["Skill nay chen sub theo loi noi, nen video BAT BUOC phai co tieng.",
             "Neu ban co file tieng rieng, ghep tieng vao video truoc:",
             '    ffmpeg -i "video.mp4" -i "tieng.wav" -c:v copy -c:a aac '
             '-shortest "video_co_tieng.mp4"',
             "roi goi skill voi video_co_tieng.mp4."])
    return info


def check_font(rep, resources, explicit, res_dir_missing=False):
    try:
        res = C.resolve_font(resources, explicit)
    except C.ThieuCongCu as exc:
        # kiem font phai render bang ffmpeg -> chua co ffmpeg thi hoan lai.
        rep.add(NOTE, "kiem font tieng Viet",
                "chua kiem duoc vi thieu %s (xem buoc 1)" % exc.exe)
        return None
    except C.ThieuThuVien as exc:
        # vd thieu numpy -> KHONG do duoc pixel. Da co dong THIEU cho thu vien do
        # o tren, o day chi noi ro la phan kiem font phai hoan lai.
        rep.add(MISS, "kiem font tieng Viet",
                "chua kiem duoc vi thieu %s (xem buoc cai o duoi)" % exc.lib)
        if not any(s == MISS and t == exc.lib for s, t, _d in rep.rows):
            rep.problem(exc.title(), exc.steps())
        return None
    except Exception as exc:  # khong bao gio de traceback lot ra nguoi dung
        rep.add(MISS, "kiem font tieng Viet", "loi khi kiem font: %s" % exc)
        rep.problem(
            "Khong kiem duoc font (loi bat thuong khi do pixel)",
            ["Chi tiet loi: %s" % exc,
             "Thu 2 viec nay:",
             "  1) Kiem ffmpeg co filter subtitles:",
             "         ffmpeg -filters | findstr subtitles     (Windows)",
             "  2) Chi thang 1 file font co dau tieng Viet:",
             '         --font "<duong-dan>/BeVietnamPro-ExtraBold.ttf"',
             "Neu van loi, dung font kem san: bo tham so --resources va --font."])
        return None
    if res["file"] and res.get("resources_unused") and res_dir_missing:
        # Thu muc --resources khong ton tai — da co 1 buoc huong dan rieng cho
        # viec do o tren roi, khong nhac lai thanh 2 loi cho cung 1 nguyen nhan.
        rep.add(NOTE, "font tieng Viet",
                "chua chon duoc — --resources khong ton tai (xem buoc 1)")
        return None
    if res["file"] and res.get("resources_unused"):
        # Nguoi dung DA dua --resources ma trong do khong co font dung duoc.
        # Hop dong muc 4: khong duoc lang le thay bang font khac roi chay tiep.
        rep.add(MISS, "font tieng Viet",
                "--resources khong co font tieng Viet nao dung duoc")
        steps = C.huong_dan_font_resources(res)
        if res["tried"]:
            steps.append("Cac font trong --resources da thu va ly do bi loai:")
            for path, source, reasons in res["tried"][:6]:
                if source != C.SRC_RESOURCES:
                    continue
                steps.append("    - %s" % os.path.basename(path))
                for r in reasons[:2]:
                    steps.append("        %s" % r)
        rep.problem("Thu muc --resources ban dua KHONG co font tieng Viet", steps)
        return None
    if res["file"]:
        chk = res["check"]
        where = res["file"]
        if where.startswith(C.skill_dir()):
            where = "assets/" + os.path.relpath(where, os.path.join(
                C.skill_dir(), "assets")).replace("\\", "/")
        src = res["source"]
        if src == C.SRC_BUNDLED and not resources:
            # PHAI noi ro dang dung phuong an du phong, de nguoi dung khong
            # bi bat ngo (hop dong muc 4.3).
            src = "khong co --resources -> dung font kem san trong skill"
        rep.add(OK, "font tieng Viet", "%s: %s" % (src, where))
        rep.add(OK, "ten ho font (ASS)",
                '"%s"  (weight %s, Style Bold=%d)'
                % (res["family"], res["weight"], res["bold"]))
        rep.add(OK, "do pixel chu co dau",
                "co dau %d px / khong dau %d px = %.3f lan, cao hon %.3f lan"
                % (chk["ink_vn"], chk["ink_ascii"], chk["ratio"], chk["h_ratio"]))
        rep.add(OK, "khong bi fallback",
                "font he thong ve ra %d px, font nay ve %d px -> dung dung font"
                % (chk["ink_fallback"], chk["ink_vn"]))
        return res
    if res.get("explicit_failed"):
        rep.add(MISS, "font tieng Viet",
                "font ban chi dinh khong dung duoc: %s"
                % os.path.basename(res["explicit_failed"]))
        rep.problem(
            "Font ban chi dinh bang --font khong ve duoc tieng Viet co dau",
            ["File: %s" % res["explicit_failed"]]
            + ["Ly do: %s" % r for r in res["explicit_reasons"]]
            + ["Toi KHONG tu doi sang font khac, vi ban da chi dinh font nay.",
               "Chon 1 trong 2:",
               "  - Bo tham so --font di, skill se dung",
               "    assets/fonts/BeVietnamPro-ExtraBold.ttf kem san.",
               "  - Hoac chi --font sang 1 file .ttf co day du dau tieng Viet",
               "    (Be Vietnam Pro, Inter, Roboto, Noto Sans)."])
        return None
    rep.add(MISS, "font tieng Viet", "khong co font nao ve duoc chu co dau")
    steps = ["Cach A — nhanh nhat, dung font kem san trong skill:",
             "    bo han tham so --resources di, skill se dung",
             "    assets/fonts/BeVietnamPro-ExtraBold.ttf",
             "    (neu file do bi mat, tai lai o Cach B)",
             "Cach B — dung font cua ban:",
             '    - Tao thu muc:   <duong-dan-ban-chon>/Font/',
             "    - Tai Be Vietnam Pro (mien phi) tai",
             "        https://fonts.google.com/specimen/Be+Vietnam+Pro",
             "      giai nen, copy file BeVietnamPro-ExtraBold.ttf vao thu muc tren",
             '    - Goi lai voi:   --resources "<duong-dan-ban-chon>"',
             "  (Font khac cung duoc, nhung PHAI co day du dau tieng Viet:",
             "   Inter, Roboto, Noto Sans deu duoc. Arial/Times cua Windows cung co dau",
             "   nhung nhin khong dep bang.)"]
    if res["tried"]:
        steps.append("Cac font da thu va ly do bi loai:")
        for path, source, reasons in res["tried"][:6]:
            steps.append("    - %s (%s)" % (os.path.basename(path), source))
            for r in reasons[:2]:
                steps.append("        %s" % r)
    rep.problem("Chua co font ve duoc chu tieng Viet co dau", steps)
    return None


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--resources")
    ap.add_argument("--font", help="chi dinh thang 1 file .ttf/.otf")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--no-whisper", action="store_true",
                    help="chi kiem phan ve chu, bo qua faster-whisper")
    ap.add_argument("--dry-run", action="store_true",
                    help="khong co tac dung o preflight (luon chi kiem)")
    a = ap.parse_args()

    rep = Report()
    check_tools(rep)
    check_libass(rep)
    check_python_libs(rep, need_whisper=not a.no_whisper)
    if not a.no_whisper:
        check_model_cache(rep, a.model)
    check_video(rep, a.video)
    res_dir_missing = bool(a.resources and not os.path.isdir(a.resources))
    if res_dir_missing:
        rep.add(MISS, "--resources", "khong thay thu muc: %s" % a.resources)
        rep.problem(
            "Thu muc --resources khong ton tai",
            ["Duong dan da nhan: %s" % a.resources,
             "Chon 1 trong 2 cach:",
             "  Cach A — NHANH NHAT: bo han tham so --resources di.",
             "      Skill se dung font kem san",
             "      assets/fonts/BeVietnamPro-ExtraBold.ttf",
             "  Cach B — dung thu muc tai nguyen rieng cua ban:",
             '      - Tao thu muc:  "%s/Font/"'
             % str(a.resources).replace("\\", "/"),
             "      - Tai Be Vietnam Pro (mien phi) tai",
             "          https://fonts.google.com/specimen/Be+Vietnam+Pro",
             "        giai nen roi copy BeVietnamPro-ExtraBold.ttf vao thu muc do",
             '      - Goi lai voi:  --resources "%s"' % a.resources])
    check_font(rep, a.resources, a.font, res_dir_missing=res_dir_missing)

    sys.exit(rep.dump())


if __name__ == "__main__":
    C.run_main(main)
