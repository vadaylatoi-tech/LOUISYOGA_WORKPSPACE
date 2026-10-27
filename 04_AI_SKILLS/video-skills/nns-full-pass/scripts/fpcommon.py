# -*- coding: utf-8 -*-
"""Ham dung chung cho skill nns-full-pass.

Skill nay KHONG viet lai nhung gi cac skill cu da lam dung. No goi lai:

    nns-cut-silence/scripts/cut_silence.py
    nns-auto-sub/scripts/{transcribe,fix_tokens,build_ass,burn}.py
    nns-face-highlight/scripts/facelib.py   (do hop mat)
    tools/sfx_pass/{build_sfx_json,cards_to_ass,verify_sfx_ab}.py

Module nay lo phan "tim cho cac script do o dau" va bao loi ro rang neu thieu,
thay vi de python nem traceback.
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)                 # .../skills/nns-full-pass
SKILLS = os.path.dirname(SKILL)               # .../skills


def _find_repo():
    """Di nguoc len tim thu muc goc project (cho co tools/sfx_pass)."""
    d = SKILL
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "tools", "sfx_pass")):
            return d
    return None


REPO = _find_repo()
SFX_TOOLS = os.path.join(REPO, "tools", "sfx_pass") if REPO else None

SIBLINGS = {
    "cut": ("nns-cut-silence", "cut_silence.py"),
    "transcribe": ("nns-auto-sub", "transcribe.py"),
    "fix": ("nns-auto-sub", "fix_tokens.py"),
    "build_ass": ("nns-auto-sub", "build_ass.py"),
    "burn": ("nns-auto-sub", "burn.py"),
    "subverify": ("nns-auto-sub", "verify.py"),
    "track": ("nns-face-highlight", "track.py"),
}

TOOLS = {
    "build_sfx_json": "build_sfx_json.py",
    "cards_to_ass": "cards_to_ass.py",
    "verify_cards": "verify_cards.py",
    "verify_sfx_ab": "verify_sfx_ab.py",
}

# nnscommon cua nns-auto-sub la thu vien nen tang (probe, font, ass_time...).
_AUTOSUB = os.path.join(SKILLS, "nns-auto-sub", "scripts")
if os.path.isdir(_AUTOSUB) and _AUTOSUB not in sys.path:
    sys.path.insert(0, _AUTOSUB)

try:
    import nnscommon as C            # noqa: E402
except Exception:                    # pragma: no cover
    C = None


def need_C():
    if C is None:
        print("!! LOI: khong nap duoc nns-auto-sub/scripts/nnscommon.py")
        print("   Skill nns-full-pass CAN skill nns-auto-sub nam canh no trong")
        print("   cung thu muc .claude/skills/. Da tim o: %s" % _AUTOSUB)
        sys.exit(1)
    return C


def sib(key):
    """Duong dan tuyet doi toi 1 script cua skill anh em. None neu chua co."""
    skill, script = SIBLINGS[key]
    p = os.path.join(SKILLS, skill, "scripts", script)
    return p if os.path.isfile(p) else None


def tool(key):
    if not SFX_TOOLS:
        return None
    p = os.path.join(SFX_TOOLS, TOOLS[key])
    return p if os.path.isfile(p) else None


def require(key, kind="sib"):
    p = sib(key) if kind == "sib" else tool(key)
    if not p:
        if kind == "sib":
            skill, script = SIBLINGS[key]
            need_C().die(
                "thieu script bat buoc: %s/scripts/%s\n"
                "  nns-full-pass dung lai script cua cac skill anh em, no khong\n"
                "  viet lai tu dau. Copy ca thu muc %s/ vao .claude/skills/ roi\n"
                "  chay lai." % (skill, script, skill))
        need_C().die(
            "thieu script bat buoc: tools/sfx_pass/%s\n"
            "  Tim thu muc goc project (cho co tools/sfx_pass/) khong ra: %s"
            % (TOOLS[key], REPO or "(khong tim thay)"))
    return p


def add_tools_path():
    """Cho phep `import cards_to_ass`, `import build_sfx_json`."""
    if SFX_TOOLS and os.path.isdir(SFX_TOOLS) and SFX_TOOLS not in sys.path:
        sys.path.insert(0, SFX_TOOLS)


def add_face_path():
    p = os.path.join(SKILLS, "nns-face-highlight", "scripts")
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
    return p


def add_sfx_path():
    p = os.path.join(SKILLS, "nns-add-sfx", "scripts")
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
    return p


# ---------------------------------------------------------------- duong dan ra
def stem_paths(out):
    """Moi file phu deu treo canh --out, dat ten theo cung mot goc.

    Quan trong: cac script cua nns-auto-sub suy file phu tu --out cua CHUNG,
    nen ta dua cho chung `<goc>.sub.mp4` de co
    `<goc>.sub.words.json`, `.sub.fixed.json`, `.sub.ass`, `.sub.plan.json`.
    """
    out = os.path.abspath(out)
    d = os.path.dirname(out)
    stem = os.path.splitext(os.path.basename(out))[0]
    j = lambda x: os.path.join(d, stem + x)          # noqa: E731
    return {
        "dir": d, "stem": stem, "final": out,
        "cut": j(".cut.mp4"),
        "layout": j(".layout.json"),
        "sub": j(".sub.mp4"),                # video da burn (con tieng goc)
        "words": j(".sub.words.json"),
        "fixed": j(".sub.fixed.json"),
        "ass": j(".sub.ass"),
        "subplan": j(".sub.plan.json"),
        "cards": j(".cards.json"),
        "merged": j(".merged.ass"),
        "cues": j(".cues.json"),
        "bed": j(".sfx.raw"),
        "master": j(".master.m4a"),
        "ab": j(".ab.json"),
        "work": j(".work"),
        "report": j(".report.json"),
    }


def hr(ch="=", n=74):
    return ch * n


def banner(title, lines=()):
    print("")
    print("  " + hr())
    print("  " + title)
    print("  " + hr())
    for ln in lines:
        print("  " + ln)


def step(name, cmd, cwd=None):
    """Chay 1 buoc con. That bai la DUNG NGAY, khong chay tiep."""
    print("")
    print("  " + hr("#"))
    print("  >>> %s" % name)
    print("  " + hr("#"))
    sys.stdout.flush()
    sys.stderr.flush()
    rc = subprocess.call(cmd, cwd=cwd)
    sys.stdout.flush()
    if rc != 0:
        print("")
        print("  " + hr("!"))
        print("  DUNG LAI o buoc: %s  (exit %d)" % (name, rc))
        print("  Khong chay tiep buoc nao nua. Sua loi tren roi chay lai.")
        print("  " + hr("!"))
        sys.exit(rc)


def py(script, args):
    return [sys.executable, script] + [str(x) for x in args]
