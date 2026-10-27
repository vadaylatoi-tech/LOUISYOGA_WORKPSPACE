# -*- coding: utf-8 -*-
"""BUOC 0 — kiem MOI thu truoc khi dung toi mot frame nao.

    python scripts/preflight.py --video "<video>" [--resources "<thu-muc>"]

In "DAY DU" -> chay tiep. In "THIEU n thu" -> DUNG, exit 1, va in dung lenh cai.
Khong bao gio doan, khong bao gio "chay tam".
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()

PIP = {
    "numpy": ("numpy", "tinh toan lop SFX, do pixel khi verify"),
    "PIL": ("Pillow", "do be rong chu that de auto-fit the chu"),
    "faster_whisper": ("faster-whisper", "nhan dang loi noi co moc tung tu"),
    "onnxruntime": ("onnxruntime", "chay model do hop mat o buoc layout"),
}

FILTERS = [
    ("subtitles", "ve sub + the chu vao hinh (can libass)"),
    ("alimiter", "chan true peak khi master"),
    ("ebur128", "do loudness LUFS"),
    ("amix", "tron tieng goc voi lop SFX"),
    ("aresample", "dong bo sample rate"),
    ("loudnorm", "chuan hoa loudness 2 pass"),
]


class Report(object):
    def __init__(self):
        self.miss = []
        self.ok = []
        self.warn = []

    def good(self, what, detail=""):
        self.ok.append((what, detail))

    def bad(self, what, steps):
        self.miss.append((what, steps))

    def note(self, msg):
        self.warn.append(msg)


def check_tools(r):
    for exe in ("ffmpeg", "ffprobe"):
        if C.which(exe):
            r.good(exe, C.tool_version(exe) or "")
        else:
            r.bad("chua co %s trong PATH" % exe, [
                "Windows:  winget install --id Gyan.FFmpeg -e",
                "          (hoac tai ban FULL o https://www.gyan.dev/ffmpeg/builds/,",
                "           giai nen ra C:\\ffmpeg, them C:\\ffmpeg\\bin vao PATH)",
                "macOS:    brew install ffmpeg",
                "Ubuntu:   sudo apt install ffmpeg",
                "Kiem lai: %s -version" % exe])
    if not C.which("ffmpeg"):
        return
    try:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"],
                             capture_output=True, text=True,
                             encoding="utf-8", errors="replace").stdout or ""
    except Exception:
        out = ""
    names = set()
    for ln in out.splitlines():
        p = ln.split()
        if len(p) >= 2:
            names.add(p[1])
    for f, why in FILTERS:
        if f in names:
            r.good("filter %s" % f, why)
        else:
            r.bad("ffmpeg thieu filter `%s` (%s)" % (f, why), [
                "Ban ffmpeg dang dung bi cat bot bo loc.",
                "Cai ban FULL: https://www.gyan.dev/ffmpeg/builds/ "
                "(chon ffmpeg-release-full)",
                "Kiem lai: ffmpeg -filters | findstr %s" % f])


def check_libs(r):
    import importlib
    for mod in PIP:
        pipname, why = PIP[mod]
        try:
            m = importlib.import_module(mod)
            r.good("python %s" % mod,
                   "%s — %s" % (getattr(m, "__version__", "?"), why))
        except Exception as e:
            r.bad("chua cai thu vien Python %s (%s)" % (pipname, why), [
                "Chay:     pip install %s" % pipname,
                "Nhieu ban python thi dung dung ban dang chay skill nay:",
                "          %s -m pip install %s" % (sys.executable, pipname),
                "Kiem lai: python -c \"import %s; print('ok')\"" % mod,
                "(loi that: %s)" % str(e)[:90]])


def check_scripts(r):
    for key in F.SIBLINGS:
        skill, script = F.SIBLINGS[key]
        p = F.sib(key)
        if p:
            r.good("%s/%s" % (skill, script), "")
        else:
            r.bad("thieu %s/scripts/%s" % (skill, script), [
                "nns-full-pass goi lai script cua cac skill anh em.",
                "Copy ca thu muc %s/ vao %s" % (skill, F.SKILLS),
                "Kiem lai: dir \"%s\""
                % os.path.join(F.SKILLS, skill, "scripts")])
    if not F.REPO:
        r.bad("khong tim thay thu muc goc project (cho co tools/sfx_pass/)", [
            "Skill nay can tools/sfx_pass/ cua project.",
            "Dat .claude/skills/nns-full-pass/ ben trong project co tools/sfx_pass/,",
            "hoac copy thu muc tools/sfx_pass/ vao goc project."])
        return
    for key in F.TOOLS:
        p = F.tool(key)
        if p:
            r.good("tools/sfx_pass/%s" % F.TOOLS[key], "")
        else:
            r.bad("thieu tools/sfx_pass/%s" % F.TOOLS[key], [
                "Copy file nay tu project goc vao %s" % F.SFX_TOOLS])


def check_font(r, resources, explicit):
    try:
        res = C.resolve_font(resources, explicit, verbose=False)
    except SystemExit:
        raise
    except Exception as e:
        r.bad("khong do duoc font: %s" % e, [
            "Kiem lai duong dan --font / --resources."])
        return None
    if res.get("resources_unused"):
        r.bad("thu muc --resources khong co font tieng Viet dung duoc",
              C.huong_dan_font_resources(res))
        return None
    if not res.get("file"):
        r.bad("khong tim thay font co dau tieng Viet",
              C.huong_dan_font_resources(res))
        return None
    r.good("font", "%s (ho '%s')"
           % (os.path.basename(res["file"]), res.get("family")))
    return res


def check_glyphs(r, font_file):
    """The chu hay dung mui ten / dau tick. Font thieu -> libass ve khoang trong."""
    if not font_file:
        return
    try:
        from PIL import ImageFont
        f = ImageFont.truetype(font_file, 60)
    except Exception:
        return
    want = u"\u2192\u2713\u2717\u2022\u00d7\u2014"
    bad = []
    for ch in want:
        try:
            if f.getmask(ch).size[1] == 0:
                bad.append(ch)
        except Exception:
            bad.append(ch)
    if bad:
        r.note("font khong co ky tu: %s  -> KHONG duoc dung cac ky tu nay trong "
               "the chu (check_cards.py se chan lai chu khong ve ra khoang trong)"
               % " ".join("%s(U+%04X)" % (c, ord(c)) for c in bad))
    else:
        r.good("glyph the chu", "font co du \u2192 \u2713 \u2717 \u2022 \u00d7 \u2014")


def check_sfx(r, resources):
    F.add_sfx_path()
    d, files = None, []
    try:
        import _common as S
        d, files, _src, _n = S.find_sfx_library(resources)
    except Exception:
        pass
    if d and files:
        r.good("thu vien SFX", "%d file o %s" % (len(files), d))
        return d
    r.bad("khong tim thay thu vien SFX (.mp3/.wav)", [
        "Cach 1: dung thu vien kem san cua skill nns-add-sfx",
        "        (bo han tham so --resources di la tu tim thay)",
        "Cach 2: tao <thu-muc>/sound-effects/, bo file .mp3/.wav vao",
        "        (tai free: pixabay.com/sound-effects, freesound.org)",
        "        roi goi them --resources \"<thu-muc>\""])
    return None


def check_video(r, path):
    if not path:
        r.bad("chua dua --video", [
            "Goi lai co duong dan video tho:",
            "    python scripts/preflight.py --video \"D:\\quay\\tho.mp4\""])
        return None
    if not os.path.isfile(path):
        r.bad("khong tim thay video: %s" % path, [
            "Kiem lai duong dan.",
            "Duong dan co dau cach thi phai boc trong dau nhay kep."])
        return None
    try:
        info = C.probe_video(path)
    except Exception as e:
        r.bad("ffprobe khong doc duoc video: %s" % e, [
            "File co the hong hoac khong phai video.",
            "Kiem: ffprobe -hide_banner \"%s\"" % path])
        return None
    w, h, fps = info["width"], info["height"], info["fps"]
    dur = info["duration"]
    r.good("video", "%dx%d  %.4g fps  %.2fs  %d frame"
           % (w, h, fps, dur, info["nb_frames"]))
    if not C.has_audio(path):
        r.bad("video KHONG co tieng", [
            "Ca day nay can tieng noi: cat khoang lang, nhan dang, tron SFX.",
            "Ghep tieng vao truoc:",
            "    ffmpeg -i \"%s\" -i tieng.wav -c:v copy -c:a aac -b:a 256k "
            "-shortest co_tieng.mp4" % path])
    else:
        r.good("tieng", "%.2fs" % C.audio_duration(path))
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=r_frame_rate,avg_frame_rate",
             "-of", "csv=p=0", path],
            capture_output=True, text=True).stdout.strip()
        rr, av = p.split(",")[:2]

        def _f(x):
            a, _, b = x.partition("/")
            return float(a) / float(b or 1)
        if abs(_f(rr) - _f(av)) > 0.02:
            r.note("video co ve VFR (r_frame_rate=%s, avg_frame_rate=%s). "
                   "Buoc cat se ep ve CFR %.4g fps." % (rr, av, _f(rr)))
        else:
            r.good("CFR", "r=%s = avg=%s" % (rr, av))
    except Exception:
        pass
    if h and h < 720:
        r.note("khung cao %d px — co chu mac dinh (cao/24 = %d px) rat nho."
               % (h, max(8, h // 24)))
    if dur and dur < 3.0:
        r.note("video chi %.2fs — ngan hon 3 giay thi cue SFX bi don het vao "
               "mot cho." % dur)
    return info


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(
        description="Kiem moi thu can cho nns-full-pass truoc khi lam viec that")
    ap.add_argument("--video")
    ap.add_argument("--out", help="khong bat buoc o buoc nay")
    ap.add_argument("--resources")
    ap.add_argument("--font")
    ap.add_argument("--dry-run", action="store_true",
                    help="preflight von khong ghi file nao, co nay chi de dong bo")
    a = ap.parse_args()

    F.banner("nns-full-pass — BUOC 0: PREFLIGHT",
             ["video     : %s" % (a.video or "(chua dua)"),
              "tai nguyen: %s" % (a.resources or "(dung assets kem san)")])

    r = Report()
    check_tools(r)
    check_libs(r)
    check_scripts(r)
    font = check_font(r, a.resources, a.font)
    check_glyphs(r, font["file"] if font else None)
    check_sfx(r, a.resources)
    check_video(r, a.video)

    print("")
    print("  DA CO (%d):" % len(r.ok))
    for what, detail in r.ok:
        print("    OK   %-32s %s" % (what, detail))
    if r.warn:
        print("")
        print("  LUU Y (%d) — khong chan, nhung nen doc:" % len(r.warn))
        for m in r.warn:
            print("    !    %s" % m)

    if not r.miss:
        print("")
        print("  " + F.hr())
        print("  DAY DU. Chay tiep duoc.")
        print("  " + F.hr())
        print("")
        return 0

    print("")
    print("  " + F.hr("!"))
    print("  THIEU %d thu. DUNG LAI o day — khong cat, khong render, khong ghi"
          % len(r.miss))
    print("  file nao ca. Lam theo dung tung khoi duoi day roi chay lai preflight.")
    print("  " + F.hr("!"))
    for i, item in enumerate(r.miss, 1):
        what, steps = item
        print("")
        print("  [%d/%d] %s" % (i, len(r.miss), what))
        for s in steps:
            print("        " + s)
    print("")
    print("  Chay lai:")
    print("      python scripts/preflight.py --video \"%s\"%s"
          % (a.video or "<video>",
             " --resources \"%s\"" % a.resources if a.resources else ""))
    print("")
    sys.exit(1)


if __name__ == "__main__":
    C.run_main(main)
