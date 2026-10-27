# -*- coding: utf-8 -*-
"""Tu kiem skill mà KHONG can video nao.

    python scripts/selftest.py

Kiem 5 nhom:
  A. --help cua moi script chay sach, khong loi import
  B. preflight bao dung khi thieu thu (video khong ton tai)
  C. --dry-run in ra du ke hoach cac buoc
  D. bo dung the chu -> .ass : dem dau phay dong Dialogue, chan glyph thieu,
     the dai tu xuong dong / thu nho
  E. cue sheet -> lop SFX : dung so mau, khong clip, co tieng dung moc

Moi thu deu dung du lieu tu tao trong thu muc tam. Khong dung toi file that.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()
HERE = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = ["preflight.py", "layout.py", "plan_cues.py", "check_cards.py",
           "punct.py", "build_sfx.py", "master.py", "verify_all.py",
           "frames.py", "fullpass.py", "selftest.py"]

MINI_ASS = u"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,{family},80,&H00FFFFFF&,&H0000D6FF&,&H00000000&,&H00000000&,1,0,0,0,100,100,0,0,1,7,0,2,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Text
Dialogue: 0,0:00:00.00,0:00:01.00,Sub,,0,0,0,{{\\an2\\pos(540,1500)}}xin chao
"""

OK, BAD = [], []


def check(name, cond, detail=""):
    (OK if cond else BAD).append((name, detail))
    print("    [%s] %-46s %s" % ("DAT" if cond else "SAI", name, detail))
    return cond


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# ------------------------------------------------------------------ A
def test_help():
    print("")
    print("  A. --help cua moi script")
    for s in SCRIPTS:
        rc, out = run([sys.executable, os.path.join(HERE, s), "--help"])
        bad = "Traceback" in out or "ModuleNotFoundError" in out
        check("%s --help" % s, rc == 0 and not bad,
              "exit %d%s" % (rc, ", CO TRACEBACK" if bad else ""))


# ------------------------------------------------------------------ B
def test_preflight():
    print("")
    print("  B. preflight bao dung khi thieu thu")
    rc, out = run([sys.executable, os.path.join(HERE, "preflight.py")])
    check("thieu --video -> exit != 0", rc != 0, "exit %d" % rc)
    check("thieu --video -> co khoi huong dan", "chua dua --video" in out, "")
    rc, out = run([sys.executable, os.path.join(HERE, "preflight.py"),
                   "--video", os.path.join(HERE, "khong_ton_tai_9x.mp4")])
    check("video khong ton tai -> exit != 0", rc != 0, "exit %d" % rc)
    check("video khong ton tai -> noi ro la khong tim thay",
          "khong tim thay video" in out, "")
    check("preflight khong bao gio nem traceback", "Traceback" not in out, "")
    rc, out = run([sys.executable, os.path.join(HERE, "preflight.py"),
                   "--resources", os.path.join(HERE, "khong_co_thu_muc_9x")])
    check("--resources sai -> khong am tham dung font kem san",
          rc != 0, "exit %d" % rc)


# ------------------------------------------------------------------ C
def test_dryrun(tmp):
    print("")
    print("  C. --dry-run in du ke hoach")
    rc, out = run([sys.executable, os.path.join(HERE, "fullpass.py"),
                   "--video", os.path.join(tmp, "khong_co.mp4"),
                   "--out", os.path.join(tmp, "ra.mp4"), "--dry-run"])
    check("fullpass --dry-run exit 0", rc == 0, "exit %d" % rc)
    for k in ("preflight", "cut_silence", "layout.py", "transcribe",
              "build_ass", "plan_cues", "check_cards", "cards_to_ass",
              "burn.py", "build_sfx", "master.py", "verify_all"):
        check("ke hoach co nhac %s" % k, k in out, "")
    check("ke hoach noi ro GATE cho duyet", "GATE" in out and "--go" in out, "")
    check("dry-run khong ghi file nao",
          not os.path.isfile(os.path.join(tmp, "ra.mp4")), "")


# ------------------------------------------------------------------ D
def test_cards(tmp):
    print("")
    print("  D. the chu -> .ass (bo dung thuan du lieu)")
    F.add_tools_path()
    import cards_to_ass as K
    res = C.resolve_font(None, None, verbose=False)
    font = res.get("file")
    if not font:
        check("tim duoc font kem san", False, "khong co font de do")
        return
    family = res.get("family")

    ass = os.path.join(tmp, "sub.ass")
    C.write_text(ass, MINI_ASS.format(family=family))
    cards = [
        {"start": 1.0, "end": 3.0, "y": 900, "style": "punch", "text": "nhanh gap ba"},
        {"start": 20.0, "end": 22.0, "y": 900, "style": "stat", "plate": True,
         "text": "mot cau the rat dai de ep xuong hai dong"},
    ]
    cj = os.path.join(tmp, "cards.json")
    C.write_json(cj, cards)
    out = os.path.join(tmp, "merged.ass")
    rc, log = run([sys.executable, F.require("cards_to_ass", kind="tool"),
                   "--ass", ass, "--cards", cj, "--out", out,
                   "--width", "1080", "--font", font])
    if not check("gop the vao .ass chay duoc", rc == 0, "exit %d" % rc):
        print(log[-900:])
        return

    text = io.open(out, encoding="utf-8").read()
    dia = [ln for ln in text.splitlines() if ln.startswith("Dialogue:")]
    check("co du dong Dialogue (1 sub + 2 the + 2 khung)", len(dia) >= 5,
          "%d dong" % len(dia))

    bad = []
    for ln in dia:
        head = ln.split(":", 1)[1]
        parts = head.split(",", 8)
        if len(parts) != 9:
            bad.append(ln[:60])
            continue
        # Layer,Start,End,Style,Name,MarginL,MarginR,MarginV = 8 truong
        if not re.fullmatch(r"\s*\d+", parts[0]):
            bad.append(ln[:60])
        for m in parts[5:8]:
            if not re.fullmatch(r"\s*-?\d+", m):
                bad.append(ln[:60])
    check("moi dong Dialogue co DUNG 8 dau phay truoc Text", not bad,
          "%d dong sai%s" % (len(bad), (": " + bad[0]) if bad else ""))

    check("the co khung dung \\an7 + toa do tinh san (khong \\an5 toa do am)",
          "\\an7" in text and "\\p1" in text and "\\an5" not in text, "")
    check("khung ve tu (0,0) — ban ve bat dau bang 'm <r> 0'",
          re.search(r"\\p1[^}]*}m \d+ 0 ", text) is not None, "")
    check("the co khung dung truot+fade, KHONG pop-scale",
          "\\move(" in text and "\\fscx112" not in text.split("CardStat")[-1][:400],
          "")

    long_ev = [ln for ln in dia if "CardStat" in ln]
    wrapped = any("\\N" in ln for ln in long_ev)
    smaller = any(re.search(r"\\fs(\d+)", ln)
                  and int(re.search(r"\\fs(\d+)", ln).group(1))
                  < K.CARD_STYLES["stat"]["size"] for ln in long_ev)
    check("the dai tu xuong dong hoac tu thu nho", wrapped or smaller,
          "xuong dong=%s, thu nho=%s" % (wrapped, smaller))

    # glyph thieu phai BI CHAN
    wj0 = os.path.join(tmp, "words0.json")
    lay0 = os.path.join(tmp, "layout0.json")
    C.write_json(wj0, [{"w": u"khac", "start": 30.0, "end": 30.4}])
    C.write_json(lay0, {"w": 1080, "h": 1920, "bottom_safe": 1600})
    miss_ch = None
    from PIL import ImageFont
    f = ImageFont.truetype(font, 60)
    for ch in u"\u2192\u2713\U0001F600\u2717":
        try:
            if f.getmask(ch).size[1] == 0:
                miss_ch = ch
                break
        except Exception:
            miss_ch = ch
            break
    if miss_ch:
        C.write_json(cj, [{"start": 1.0, "end": 3.0, "y": 900, "style": "punch",
                           "text": u"nhanh %s gap" % miss_ch}])
        rc, log = run([sys.executable, os.path.join(HERE, "check_cards.py"),
                       "--cards", cj, "--words", wj0, "--layout", lay0,
                       "--font", font])
        check("glyph font khong co -> BI CHAN, khong ve ra khoang trong",
              rc != 0, "exit %d (ky tu thu: U+%04X)" % (rc, ord(miss_ch)))
        check("bao dung ten ky tu thieu",
              "U+%04X" % ord(miss_ch) in log, "")
        # Ghi lai vi sao guard nay phai nam o check_cards chu khong dua vao
        # cards_to_ass.missing_glyphs: ham do so voi getmask("")=(0,0), con ky
        # tu thieu tra ve (rong>0, cao=0) -> no khong bao gio bat duoc.
        import cards_to_ass as K2
        check("da biet: cards_to_ass.missing_glyphs KHONG bat duoc (nen guard "
              "that nam o check_cards.py)",
              K2.missing_glyphs(font, 118, u"x%sx" % miss_ch) == [],
              "xac nhan lai hanh vi cua ban cu")
    else:
        check("glyph font khong co -> BI CHAN", True,
              "(font co du glyph thu nghiem, bo qua)")

    # check_cards: cac luat cung
    words = [{"w": u"the", "start": 1.0, "end": 1.3},
             {"w": u"nay", "start": 1.3, "end": 1.6},
             {"w": u"lap", "start": 1.6, "end": 2.0},
             {"w": u"y.", "start": 2.0, "end": 2.4},
             {"w": u"con", "start": 2.5, "end": 2.8},
             {"w": u"so", "start": 2.8, "end": 3.0},
             {"w": u"47", "start": 3.0, "end": 3.4}]
    wj = os.path.join(tmp, "words.json")
    C.write_json(wj, words)
    lay = os.path.join(tmp, "layout.json")
    C.write_json(lay, {"w": 1080, "h": 1920, "bottom_safe": 1600})

    cases = [
        ("text rong bi chan", [{"start": 1, "end": 2.5, "y": 900,
                                "style": "punch", "text": ""}]),
        ("qua 4 chu bi chan", [{"start": 1, "end": 2.5, "y": 900, "style": "punch",
                                "text": "mot hai ba bon nam"}]),
        ("dai qua 2.5s bi chan", [{"start": 1, "end": 6.0, "y": 900,
                                   "style": "punch", "text": "nhanh gap ba"}]),
        ("lap nguyen van loi thoai bi chan",
         [{"start": 1, "end": 2.5, "y": 900, "style": "punch",
           "text": "the nay lap y"}]),
        ("in lai con so dang noi bi chan",
         [{"start": 2.0, "end": 4.0, "y": 900, "style": "punch", "text": "47 lan"}]),
        ("y tut duoi vung an toan bi chan",
         [{"start": 1, "end": 2.5, "y": 1750, "style": "punch",
           "text": "nhanh gap ba"}]),
        ("hai the qua gan nhau bi chan",
         [{"start": 1, "end": 2.5, "y": 900, "style": "punch", "text": "nhanh gap ba"},
          {"start": 5, "end": 7.0, "y": 900, "style": "punch", "text": "cham gap ba"}]),
    ]
    for name, cc in cases:
        C.write_json(cj, cc)
        rc, log = run([sys.executable, os.path.join(HERE, "check_cards.py"),
                       "--cards", cj, "--words", wj, "--layout", lay,
                       "--font", font])
        check("check_cards: %s" % name, rc != 0, "exit %d" % rc)

    C.write_json(cj, [{"start": 1.0, "end": 3.0, "y": 900, "style": "punch",
                       "text": "cach nghi khac"}])
    rc, log = run([sys.executable, os.path.join(HERE, "check_cards.py"),
                   "--cards", cj, "--words", wj, "--layout", lay, "--font", font])
    check("check_cards: the hop le thi DAT", rc == 0, "exit %d" % rc)


# ------------------------------------------------------------------ E
def test_sfx(tmp):
    print("")
    print("  E. cue sheet -> lop SFX")
    np = C.import_numpy()
    lib = os.path.join(tmp, "sfxlib")
    os.makedirs(lib)
    # File thu: 0.30s IM LANG o dau roi moi co tieng. Neu bo dung khong tu do
    # onset thi cue se im ru — day dung la cai bay da tra gia.
    sr = 48000
    n = int(0.9 * sr)
    t = np.arange(n) / float(sr)
    x = np.zeros(n, dtype=np.float32)
    k = int(0.30 * sr)
    x[k:] = (0.6 * np.sin(2 * np.pi * 900 * t[:n - k])
             * np.exp(-4.0 * t[:n - k])).astype(np.float32)
    wav = os.path.join(lib, "beep-test.wav")
    raw = os.path.join(tmp, "beep.raw")
    x.tofile(raw)
    rc, log = run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr),
                   "-ac", "1", "-i", raw, "-c:a", "pcm_s16le", wav])
    if not check("tao duoc file SFX thu nghiem", rc == 0 and os.path.isfile(wav),
                 "exit %d" % rc):
        return

    cues = [{"t": 1.0, "file": "beep-test.wav", "gain_db": -12.0,
             "off": None, "dur": None, "fin": 0.0, "fout": 0.03,
             "optional": False},
            {"t": 3.0, "file": "beep-test.wav", "gain_db": -12.0,
             "off": None, "dur": None, "fin": 0.0, "fout": 0.03,
             "optional": True}]
    cj = os.path.join(tmp, "cues.json")
    C.write_json(cj, cues)
    bed = os.path.join(tmp, "bed.raw")
    total = 5.0
    rc, log = run([sys.executable, os.path.join(HERE, "build_sfx.py"),
                   "--cues", cj, "--out", bed, "--total", "%.6f" % total,
                   "--lib", lib])
    if not check("build_sfx chay duoc", rc == 0, "exit %d" % rc):
        print(log[-900:])
        return

    a = np.fromfile(bed, dtype="<f4").reshape(-1, 2)
    check("dung so mau (%.1fs x 48k x 2 kenh)" % total,
          len(a) == int(round(total * sr)),
          "%d mau, mong doi %d" % (len(a), int(round(total * sr))))
    pk = float(np.abs(a).max())
    check("lop SFX khong clip", pk < 0.98, "dinh %.4f" % pk)

    def peak_at(s, e):
        return float(np.abs(a[int(s * sr):int(e * sr)]).max())
    check("cue 1.00s co tieng NGAY tai moc (da tu cat im lang dau)",
          peak_at(1.00, 1.05) > 0.02, "dinh %.4f trong 50ms dau" % peak_at(1.00, 1.05))
    check("truoc cue 1.00s van im", peak_at(0.0, 0.95) < 1e-6,
          "dinh %.6f" % peak_at(0.0, 0.95))
    check("cue tuy chon o 3.00s co tieng", peak_at(3.00, 3.10) > 0.02, "")

    rc, log = run([sys.executable, os.path.join(HERE, "build_sfx.py"),
                   "--cues", cj, "--out", bed, "--total", "%.6f" % total,
                   "--lib", lib, "--drop-optional"])
    b = np.fromfile(bed, dtype="<f4").reshape(-1, 2)
    check("--drop-optional bo dung khoi cue ngoai hook",
          rc == 0 and float(np.abs(b[int(3.0 * sr):]).max()) < 1e-6
          and float(np.abs(b[int(1.0 * sr):int(1.2 * sr)]).max()) > 0.02, "")

    rc, log = run([sys.executable, os.path.join(HERE, "build_sfx.py"),
                   "--cues", cj, "--out", bed, "--total", "%.6f" % total,
                   "--lib", os.path.join(tmp, "khong_co_thu_muc"), "--dry-run"])
    check("thu vien SFX sai -> bao loi ro, khong chay tiep", rc != 0,
          "exit %d" % rc)


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(description="Tu kiem skill khong can video")
    ap.add_argument("--keep", action="store_true", help="giu thu muc tam")
    ap.add_argument("--only", help="chi chay 1 nhom: A B C D E")
    a = ap.parse_args()

    F.banner("nns-full-pass — TU KIEM (khong can video)",
             ["skill : %s" % F.SKILL,
              "python: %s" % sys.version.split()[0]])

    tmp = tempfile.mkdtemp(prefix="fpselftest_")
    only = (a.only or "ABCDE").upper()
    try:
        if "A" in only:
            test_help()
        if "B" in only:
            test_preflight()
        if "C" in only:
            test_dryrun(tmp)
        if "D" in only:
            test_cards(tmp)
        if "E" in only:
            test_sfx(tmp)
    finally:
        if a.keep:
            print("")
            print("  giu thu muc tam: %s" % tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    print("")
    print("  " + F.hr())
    print("  KET QUA: %d dat, %d sai (tong %d)"
          % (len(OK), len(BAD), len(OK) + len(BAD)))
    print("  " + F.hr())
    if BAD:
        for name, detail in BAD:
            print("    SAI  %s  %s" % (name, detail))
        print("")
        sys.exit(1)
    print("")


if __name__ == "__main__":
    C.run_main(main)
