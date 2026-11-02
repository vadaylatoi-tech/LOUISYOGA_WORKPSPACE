# -*- coding: utf-8 -*-
"""Dong bo workspace Louis Yoga giua cac may (GitHub = code/skill/quy tac, Google Drive = media/asset/nhat ky).

    python dong_bo.py cai-dat          # 1 lan tren moi may: noi skill vao repo, chep asset, bat hook dau phien
    python dong_bo.py session-start    # hook SessionStart cua Claude Code goi moi khi mo phien
    python dong_bo.py ghi-nhat-ky --viec "..." [--file "..."] [--con-lai "..."]
    python dong_bo.py kiem-tra         # in trang thai, khong sua gi

Duong dan Drive tu do: bien moi truong LOUGA_DRIVE, neu khong co thi tim
"<o>:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA" tren moi o dia.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import socket
import string
import subprocess
import sys

for s in (sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOME_CLAUDE = os.path.join(os.path.expanduser("~"), ".claude")
SKILLS_DIR = os.path.join(HOME_CLAUDE, "skills")
SETTINGS = os.path.join(HOME_CLAUDE, "settings.json")
NHAT_KY_REL = "00_SYSTEM/NHAT-KY-LAM-VIEC.md"  # tren Drive
SO_BUG_REL = "00_SYSTEM/SO-BUG.md"  # so bug dung chung, quy tac 2 lan (CLAUDE.md)

# Skill dung chung: ten skill -> thu muc trong repo (cung duong dan tuong doi tren Drive cho asset)
SKILLS = {
    "louisyoga-reel-style1": "04_AI_SKILLS/louisyoga-reel-style1-package/louisyoga-reel-style1",
    "louisyoga-reel-style2": "04_AI_SKILLS/louisyoga-reel-style2-package/louisyoga-reel-style2",
    "louisyoga-reel-review": "04_AI_SKILLS/louisyoga-reel-review-package/louisyoga-reel-review",
    "duycongeditvideo-buoc1": "04_AI_SKILLS/duycongeditvideo-buoc1-package/duycongeditvideo-buoc1",
}
# Bo skill dung video (nns-* goi nhau qua thu muc anh em -> phai nam chung 1 thu muc)
for _n in ("nns-add-sfx", "nns-auto-sub", "nns-cut-silence", "nns-face-highlight", "nns-full-pass",
           "nns-split-compare", "edit-nns-v1", "edit-remotion-nns", "edit-style-gpt-secret-code",
           "edit-style-nns", "extract-edit-style", "script-writer"):
    SKILLS[_n] = f"04_AI_SKILLS/video-skills/{_n}"
# Bo IART AI (motion graphics, MIT, ban chep trong repo — xem 04_AI_SKILLS/iart-ai/NGUON.md)
for _n in ("iart-caption-animation", "iart-countdown-video", "iart-lower-thirds", "iart-short-form-video",
           "iart-kinetic-typography", "iart-talking-head-b-roll"):
    SKILLS[_n] = f"04_AI_SKILLS/iart-ai/{_n}"
# Thu vien dung chung (font Be Vietnam Pro, ~90 SFX, ~120 logo): skill nns-*/edit-* goi qua --resources.
# svg/mp3/ttf khong len git -> dong bo qua Drive nhu asset skill (KHONG phai skill, khong noi vao ~/.claude/skills).
SHARED = {"shared-sources": "03_MEDIA_LIBRARY/shared-sources"}
MEMORY_REL = "00_SYSTEM/claude-memory/workspace"  # memory chung, cai-dat nap vao ~/.claude/projects/<thu muc>/memory
SKIP_NAMES = {"desktop.ini", "Thumbs.db", ".DS_Store"}
SKIP_DIRS = {"node_modules", "__pycache__", ".git"}


def drive_root():
    env = os.environ.get("LOUGA_DRIVE")
    if env and os.path.isdir(env):
        return env
    for d in string.ascii_uppercase[2:]:
        p = f"{d}:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA"
        if os.path.isdir(p):
            return p
    return None


def git(*args, timeout=25):
    try:
        r = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).rstrip()
    except Exception as e:  # khong co mang / khong co git
        return 1, str(e)


def is_link(p):
    try:
        return os.path.islink(p) or (hasattr(os.path, "isjunction") and os.path.isjunction(p))
    except OSError:
        return False


def tracked_files(rel):
    code, out = git("ls-files", rel)
    return {os.path.normpath(os.path.join(REPO, l)) for l in out.splitlines()} if code == 0 else set()


def sync_assets(drive, quiet=False):
    """Dong bo 2 chieu, CHI THEM (khong xoa): asset tren Drive <-> thu muc skill trong repo.
    File do git quan ly thi git thang; file media khac kich thuoc thi lay ban tren Drive."""
    msgs = []
    for name, rel in {**SKILLS, **SHARED}.items():
        local = os.path.join(REPO, rel)
        remote = os.path.join(drive, rel)
        if not os.path.isdir(local):
            continue
        os.makedirs(remote, exist_ok=True)  # skill moi: tao cho tren Drive de day asset len
        tracked = tracked_files(rel)
        down = up = 0
        for root, dirs, files in os.walk(remote):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in files:
                if fn in SKIP_NAMES:
                    continue
                src = os.path.join(root, fn)
                dst = os.path.normpath(os.path.join(local, os.path.relpath(src, remote)))
                if dst in tracked:
                    continue
                if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    down += 1
        for root, dirs, files in os.walk(local):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in files:
                if fn in SKIP_NAMES:
                    continue
                src = os.path.normpath(os.path.join(root, fn))
                if src in tracked:
                    continue
                dst = os.path.join(remote, os.path.relpath(src, local))
                if not os.path.exists(dst):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)
                    up += 1
        if down or up:
            msgs.append(f"asset {name}: tai ve {down}, day len Drive {up}")
    return msgs


def last_entries(drive, n=3):
    p = os.path.join(drive, NHAT_KY_REL)
    if not os.path.isfile(p):
        return None
    text = open(p, encoding="utf-8").read()
    parts = text.split("\n## ")
    entries = ["## " + x.strip() for x in parts[1:]]
    return entries[-n:]


def open_bugs(drive):
    """Cac loai bug chua [ĐÃ XONG] trong so bug (tieu de '## [TRANG THAI] ...') kem so lan da thu."""
    p = os.path.join(drive, SO_BUG_REL)
    if not os.path.isfile(p):
        return None
    out, cur, fence = [], None, False
    for line in open(p, encoding="utf-8"):
        if line.startswith("```"):
            fence = not fence          # bo qua mau trong khoi code
            continue
        if fence:
            continue
        if line.startswith("## ["):
            cur = None
            if "[ĐÃ XONG]" not in line and "[KHÔNG SỬA]" not in line:
                cur = [line[3:].strip(), 0]
                out.append(cur)
        elif cur and line.startswith("- Lần "):
            cur[1] += 1
    return [f"- {t} — da thu {n} lan" for t, n in out]


def cmd_session_start(_a):
    try:
        info = json.loads(sys.stdin.read() or "{}")
    except Exception:
        info = {}
    # Khong biet phien mo o dau -> coi nhu ngoai repo (chen quy tac cho chac).
    cwd = os.path.normcase(os.path.abspath(info["cwd"])) if info.get("cwd") else ""

    out = ["# DONG BO WORKSPACE LOUIS YOGA (tu dong khi mo phien)"]

    code, msg = git("pull", "--ff-only", "--quiet")
    head = git("log", "-1", "--format=%h %s (%cr)")[1]
    out.append(f"- GitHub: {'da cap nhat' if code == 0 else 'KHONG pull duoc: ' + msg[:300]} · ban hien tai: {head}")
    dirty = git("status", "--porcelain", "--untracked-files=no")[1]
    if dirty:
        out.append("- Repo co thay doi CHUA commit (skill/quy tac). Nho commit + push khi xong:\n  "
                   + dirty.replace("\n", "\n  "))

    drive = drive_root()
    if not drive:
        out.append("- KHONG tim thay Google Drive (LOUGA_WORKSPACE_MEDIA). Mo Google Drive for desktop truoc khi lam.")
    else:
        try:
            for m in sync_assets(drive):
                out.append("- " + m)
        except Exception as e:
            out.append(f"- Loi dong bo asset: {e}")
        ent = last_entries(drive)
        out.append(f"\n## Nhat ky lam viec gan nhat ({drive}/{NHAT_KY_REL})")
        out.append("\n\n".join(ent) if ent else "(chua co muc nao)")
        bugs = open_bugs(drive)
        if bugs:
            out.append(f"\n## Bug chua xong ({drive}/{SO_BUG_REL}) — doc so truoc khi sua; lan 2 khong xong thi DUNG, de xuat huong moi")
            out.append("\n".join(bugs))

    # Skill moi keo ve tu GitHub -> tu noi vao ~/.claude/skills (chi khi may chua co thu muc trung ten)
    for name, rel in SKILLS.items():
        link = os.path.join(SKILLS_DIR, name)
        if not os.path.isdir(os.path.join(REPO, rel)) or is_link(link):
            continue
        if os.path.exists(link):
            out.append(f"- CANH BAO: skill {name} tren may la ban rieng, chua noi vao repo -> chay: python \"{os.path.abspath(__file__)}\" cai-dat")
            continue
        try:
            os.makedirs(SKILLS_DIR, exist_ok=True)
            if os.name == "nt":
                subprocess.run(["cmd", "/c", "mklink", "/J", link, os.path.normpath(os.path.join(REPO, rel))], capture_output=True, check=True)
            else:
                os.symlink(os.path.join(REPO, rel), link)
            out.append(f"- Skill moi {name}: da noi vao Claude (mo phien moi de Claude thay skill)")
        except Exception as e:
            out.append(f"- Loi noi skill {name}: {e}")
    for m in install_node_deps():
        out.append("- " + m)
    if drive:
        for m in seed_memory(drive):
            if not m.endswith(": them 0 file"):
                out.append("- " + m)

    if cwd != os.path.normcase(REPO):
        cm = os.path.join(REPO, "CLAUDE.md")
        if os.path.isfile(cm):
            out.append(f"\n## Quy tac workspace (tu {cm} — phien nay mo ngoai repo nen chen vao day)\n")
            out.append(open(cm, encoding="utf-8").read())
    out.append("\nKHI XONG VIEC: ghi nhat ky bang `python \"" + os.path.abspath(__file__).replace("\\", "/")
               + "\" ghi-nhat-ky --viec \"...\" --file \"...\" --con-lai \"...\"`; sua skill/quy tac thi commit + push.")
    print("\n".join(out))


def cmd_ghi_nhat_ky(a):
    drive = drive_root()
    if not drive:
        sys.exit("Khong tim thay Google Drive.")
    p = os.path.join(drive, NHAT_KY_REL)
    if not os.path.exists(p):
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("# Nhật ký làm việc — Louis Yoga workspace\n\nMỗi phiên Claude ghi 1 mục khi xong việc "
                     "(script: D:/LOUGA_WORKSPACE/00_SYSTEM/sync/dong_bo.py ghi-nhat-ky). Mới nhất ở cuối. Hook đầu phiên đọc 3 mục cuối.\n")
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"\n## {now} · máy {socket.gethostname()}", f"- Việc: {a.viec}"]
    if a.file:
        lines.append(f"- File: {a.file}")
    if a.con_lai:
        lines.append(f"- Còn dở / tiếp theo: {a.con_lai}")
    with open(p, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"Da ghi nhat ky -> {p}")


def link_skills():
    msgs = []
    os.makedirs(SKILLS_DIR, exist_ok=True)
    for name, rel in SKILLS.items():
        target = os.path.normpath(os.path.join(REPO, rel))
        link = os.path.normpath(os.path.join(SKILLS_DIR, name))
        if not os.path.isdir(target):
            msgs.append(f"bo qua {name}: repo khong co {rel}")
            continue
        if is_link(link):
            msgs.append(f"{name}: da noi san")
            continue
        if os.path.exists(link):
            bak = os.path.join(HOME_CLAUDE, "skills-backup", f"{name}_{dt.date.today():%Y-%m-%d}")
            os.makedirs(os.path.dirname(bak), exist_ok=True)
            shutil.move(link, bak)
            msgs.append(f"{name}: ban cu chuyen sang {bak}")
        if os.name == "nt":
            r = subprocess.run(["cmd", "/c", "mklink", "/J", link, target], capture_output=True, text=True)
            if r.returncode:
                raise RuntimeError(f"mklink loi ({name}): {r.stdout} {r.stderr}")
        else:
            os.symlink(target, link)
        msgs.append(f"{name}: noi {link} -> {target}")
    return msgs


NODE_DIRS = ["04_AI_SKILLS/iart-ai"]  # thu muc co package.json can `npm i` (node_modules khong len git)


def install_node_deps():
    """npm ci cho thu muc nao chua co node_modules; cache + file tam de tren o cua repo (khong ghi C:)."""
    msgs = []
    for rel in NODE_DIRS:
        d = os.path.join(REPO, rel)
        if not os.path.isfile(os.path.join(d, "package.json")) or os.path.isdir(os.path.join(d, "node_modules")):
            continue
        cache = os.path.join(REPO, "_npm-cache")
        tmp = os.path.join(cache, "tmp")
        os.makedirs(tmp, exist_ok=True)
        env = dict(os.environ, npm_config_cache=cache, TEMP=tmp, TMP=tmp)
        npm = shutil.which("npm") or "npm"
        cmd = [npm, "ci" if os.path.isfile(os.path.join(d, "package-lock.json")) else "install", "--silent"]
        try:
            r = subprocess.run(cmd, cwd=d, env=env, capture_output=True, text=True, timeout=300)
            msgs.append(f"npm {rel}: {'da cai thu vien' if r.returncode == 0 else 'LOI ' + (r.stderr or r.stdout)[-300:]}")
        except Exception as e:
            msgs.append(f"npm {rel}: LOI {e} (cai tay: cd {d} && npm i)")
    return msgs


def seed_memory(drive):
    """Nap memory chung vao thu muc memory cua Claude Code cho repo va thu muc workspace tren Drive.
    Chi them file con thieu, khong ghi de memory da co tren may."""
    src = os.path.join(REPO, MEMORY_REL)
    if not os.path.isdir(src):
        return []
    roots = [REPO] + ([os.path.dirname(drive)] if drive else [])
    msgs = []
    for root in roots:
        slug = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(root))
        mem = os.path.join(HOME_CLAUDE, "projects", slug, "memory")
        os.makedirs(mem, exist_ok=True)
        index = os.path.join(mem, "MEMORY.md")
        have = open(index, encoding="utf-8").read() if os.path.exists(index) else ""
        added = 0
        for fn in sorted(os.listdir(src)):
            if not fn.endswith(".md") or fn == "MEMORY.md" or os.path.exists(os.path.join(mem, fn)):
                continue
            shutil.copy2(os.path.join(src, fn), os.path.join(mem, fn))
            line = next((l for l in open(os.path.join(src, "MEMORY.md"), encoding="utf-8")
                         if f"({fn})" in l), f"- [{fn}]({fn})\n")
            if f"({fn})" not in have:
                have += ("" if not have or have.endswith("\n") else "\n") + line.rstrip("\n") + "\n"
            added += 1
        with open(index, "w", encoding="utf-8") as fh:
            fh.write(have)
        msgs.append(f"memory {mem}: them {added} file")
    return msgs


def install_hook():
    cfg = {}
    if os.path.exists(SETTINGS):
        cfg = json.load(open(SETTINGS, encoding="utf-8"))
        shutil.copy2(SETTINGS, SETTINGS + ".bak")
    script = os.path.abspath(__file__).replace("\\", "/")
    py = sys.executable.replace("\\", "/")
    command = f'"{py}" "{script}" session-start'
    groups = cfg.setdefault("hooks", {}).setdefault("SessionStart", [])
    for g in groups:
        for h in g.get("hooks", []):
            if "dong_bo.py" in h.get("command", ""):
                h["command"] = command
                break
        else:
            continue
        break
    else:
        groups.append({"hooks": [{"type": "command", "command": command, "timeout": 120}]})
    with open(SETTINGS, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=2)
    return f"hook SessionStart -> {command}"


def cmd_cai_dat(_a):
    print(f"Repo: {REPO}")
    if git("rev-parse", "--is-inside-work-tree")[0] != 0:
        sys.exit("Thu muc nay khong phai repo git. Clone truoc: git clone https://github.com/vadaylatoi-tech/LOUISYOGA_WORKPSPACE D:/LOUGA_WORKSPACE")
    drive = drive_root()
    print(f"Drive: {drive or 'KHONG TIM THAY — cai Google Drive for desktop roi chay lai'}")
    print("- git pull:", git("pull", "--ff-only")[1] or "ok")
    if drive:
        for m in sync_assets(drive) or ["asset da du"]:
            print("-", m)
    for m in link_skills():
        print("-", m)
    for m in seed_memory(drive):
        print("-", m)
    for m in install_node_deps() or ["thu vien node da du"]:
        print("-", m)
    print("-", install_hook())
    print("\nXONG. Dong va mo lai Claude Code de hook + skill co hieu luc.")


def cmd_kiem_tra(_a):
    print(f"Repo: {REPO}\nDrive: {drive_root()}")
    for name in SKILLS:
        link = os.path.join(SKILLS_DIR, name)
        print(f"- skill {name}: {'noi vao repo' if is_link(link) else ('ban rieng (CHUA noi)' if os.path.exists(link) else 'chua cai')}")
    hooked = os.path.exists(SETTINGS) and "dong_bo.py" in open(SETTINGS, encoding="utf-8").read()
    print(f"- hook dau phien: {'da bat' if hooked else 'CHUA bat'}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("cai-dat").set_defaults(fn=cmd_cai_dat)
    sub.add_parser("session-start").set_defaults(fn=cmd_session_start)
    sub.add_parser("kiem-tra").set_defaults(fn=cmd_kiem_tra)
    g = sub.add_parser("ghi-nhat-ky")
    g.add_argument("--viec", required=True)
    g.add_argument("--file")
    g.add_argument("--con-lai")
    g.set_defaults(fn=cmd_ghi_nhat_ky)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
