# -*- coding: utf-8 -*-
"""probe.py - DO onset cua TUNG file SFX truoc khi dung.

Tai sao bat buoc: rat nhieu file trong thu vien co IM LANG O DAU. Do that
tren may nay: mouse-click.mp3 1.02s, buzzer.mp3 0.66s, digital-counting-2.mp3
0.66s, new-item.wav 0.65s, funny.mp3 0.52s, pop.mp3 0.23s.
Neu cu cat 0.2s tu diem 0 thi cue ra IM RU.

Ngoai onset, probe con do:
  burst_end - het cu danh dau tien (file whoosh.wav danh 2 lan: 0.14-0.41,
              im, roi danh lai o 1.40 -> phai cat o 0.41, khong lay ca file)
  climax    - dinh nang luong
  riser     - file leo dan roi tat: PHAI cat de KET THUC dung dinh, khong
              lay het file, neu khong riser no len som roi im truoc luc can hit

Ket qua ghi ra JSON (cache theo size+mtime, chay lai rat nhanh).

  python scripts/probe.py --video "<video>" --out sfx_onsets.json [--resources "<dir>"]
"""
from __future__ import print_function

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_stdout()

CACHE_VERSION = 4


def key_of(sfx_dir, path):
    return C.disp(os.path.relpath(path, sfx_dir))


def build_table(sfx_dir, sfx_files, old, tags, only=None, quiet=False):
    """Do (hoac lay lai tu cache) onset cho tung file. Tra ve (table, n_do_moi)."""
    table = {}
    fresh = 0
    t0 = time.time()
    total = len(sfx_files)
    for i, p in enumerate(sfx_files, 1):
        k = key_of(sfx_dir, p)
        if only is not None and os.path.basename(p) not in only and k not in only:
            # --only khong duoc lam mat cache cua nhung file khac
            if k in old:
                table[k] = old[k]
            continue
        try:
            st = os.stat(p)
            sig = [int(st.st_size), int(st.st_mtime)]
        except OSError as ex:
            table[k] = {"usable": False, "reason": "khong doc duoc file: %s" % ex}
            continue
        prev = old.get(k)
        if prev and prev.get("sig") == sig and prev.get("v") == CACHE_VERSION:
            table[k] = prev
            continue
        info = C.analyse_sfx(p)
        info["sig"] = sig
        info["v"] = CACHE_VERSION
        info["role"] = C.role_of(k, tags.get(os.path.basename(p)),
                                 is_riser=bool(info.get("riser")))
        table[k] = info
        fresh += 1
        if not quiet and fresh % 20 == 0:
            print("  ... da do %d/%d file (%.1fs)" % (i, total, time.time() - t0))
    return table, fresh


def main():
    ap = argparse.ArgumentParser(description="Do onset tung file SFX")
    C.add_common_args(ap, need_out=True)
    ap.add_argument("--only", default=None,
                    help="chi do nhung file nay (ten cach nhau bang dau phay)")
    ap.add_argument("--show", type=int, default=25,
                    help="in ra bao nhieu dong bang (0 = het)")
    a = ap.parse_args()
    C.require_numpy(a.video)

    if not os.path.isfile(a.video):
        C.die("khong tim thay video: %s\nGoi lai voi --video dung duong dan."
              % a.video)

    # Nguoi dung dua --resources thi phai dung dung do, khong am tham doi nguon.
    res_prob = C.resources_problem(a.resources)
    if res_prob:
        head, lines = C.resources_guidance(res_prob[0], res_prob[1])
        C.die_block(head, lines,
                    "python scripts/preflight.py --video \"%s\"" % a.video)

    sfx_dir, sfx_files, src, notes = C.find_sfx_library(a.resources)
    if not sfx_files:
        C.die("khong tim thay thu vien SFX.\n"
              "Chay preflight de xem huong dan day du:\n"
              "    python scripts/preflight.py --video \"%s\"%s"
              % (a.video, (" --resources \"%s\"" % a.resources) if a.resources else ""))

    only = None
    if a.only:
        only = set(x.strip() for x in a.only.split(",") if x.strip())

    old = {}
    if os.path.isfile(a.out):
        try:
            prev = C.read_json(a.out)
            if prev.get("version") == CACHE_VERSION:
                old = prev.get("files", {})
        except Exception:
            old = {}

    tags = C.load_library_tags(sfx_dir)

    print("")
    print("  nns-add-sfx / PROBE ONSET")
    print("  thu vien : %s  (%d file, nguon: %s)" % (C.disp(sfx_dir), len(sfx_files), src))
    if tags:
        print("  library.json : co, %d file co tag" % len(tags))
    for n in notes:
        print("  luu y    : " + n)
    print("")

    table, fresh = build_table(sfx_dir, sfx_files, old, tags, only=only)

    good = {k: v for k, v in table.items() if v.get("usable")}
    bad = {k: v for k, v in table.items() if not v.get("usable")}
    risers = {k: v for k, v in good.items() if v.get("riser")}
    lead = {k: v for k, v in good.items() if v.get("onset", 0.0) >= 0.15}

    if not good:
        C.die("khong file SFX nao dung duoc trong %s.\n"
              "Tat ca %d file deu im lang hoac khong giai ma duoc.\n"
              "Kiem thu: ffplay \"<mot-file-trong-do>\""
              % (C.disp(sfx_dir), len(table)))

    obj = {
        "version": CACHE_VERSION,
        "sr": C.SR,
        "hop": C.HOP,
        "sfx_dir": C.disp(sfx_dir),
        "source": src,
        "files": table,
    }
    C.write_json(a.out, obj)

    # ------------------------------------------------------------------ bao cao
    rows = sorted(good.items(), key=lambda kv: -kv[1].get("onset", 0.0))
    show = rows if a.show == 0 else rows[:a.show]
    print("  %-26s %6s %8s %9s %8s %7s %6s %s"
          % ("file", "dur", "onset", "burst_end", "climax", "rec_dur", "align", "role"))
    print("  " + "-" * 92)
    for k, v in show:
        print("  %-26s %6.2f %8.3f %9.3f %8.3f %7.3f %6s %s"
              % (k[:26], v["dur"], v["onset"], v["burst_end"], v["climax"],
                 v["rec_dur"], v["rec_align"], v.get("role", "?")))
    if a.show and len(rows) > a.show:
        print("  ... con %d file nua (dung --show 0 de xem het)" % (len(rows) - a.show))

    print("")
    print("  do moi         : %d file (con lai lay tu cache)" % fresh)
    print("  dung duoc      : %d/%d" % (len(good), len(table)))
    print("  co im lang dau : %d file onset >= 0.15s  <- day la ly do phai probe"
          % len(lead))
    if lead:
        worst = sorted(lead.items(), key=lambda kv: -kv[1]["onset"])[:6]
        print("                   " + ", ".join("%s %.2fs" % (k, v["onset"])
                                                for k, v in worst))
    print("  riser          : %d file (phai cat de KET THUC dung dinh)" % len(risers))
    for k, v in sorted(risers.items()):
        print("                   %-24s onset %.3f -> climax %.3f (rec_dur %.3f)"
              % (k, v["onset"], v["climax"], v["rec_dur"]))
    if bad:
        print("  KHONG dung duoc: %d file" % len(bad))
        for k, v in sorted(bad.items())[:10]:
            print("                   %-24s %s" % (k, v.get("reason", "?")))
    print("")
    print("  da ghi: %s" % C.disp(a.out))
    print("")


if __name__ == "__main__":
    main()
