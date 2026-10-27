# -*- coding: utf-8 -*-
"""BUOC 8 — dung lop SFX tu cue sheet. Vo boc quanh tools/sfx_pass/build_sfx_json.py.

    python scripts/build_sfx.py --cues <x.cues.json> --out <x.sfx.raw> \
        --total 79.233 [--lib <thu-muc-sfx>] [--drop-optional] [--max-t 20]

Vi sao co vo boc nay: build_sfx_json.py ghim cung mot duong dan thu vien SFX
cua may nguoi viet no. Skill nay phai chay tren may khac, nen no doi thu vien
(--lib, hoac --resources, hoac thu vien kem san cua nns-add-sfx) TRUOC khi goi.
Ban goc KHONG bi sua — no van chay doc lap y nhu cu.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(
        description="Dung lop SFX (raw f32le 48k stereo) tu cue sheet JSON")
    ap.add_argument("--cues")
    ap.add_argument("--out")
    ap.add_argument("--total", type=float, help="do dai lop SFX, giay")
    ap.add_argument("--lib", help="thu muc chua file .mp3/.wav")
    ap.add_argument("--resources", help="thu muc co sound-effects/ rieng")
    ap.add_argument("--max-t", dest="max_t", type=float, default=None,
                    help="chi giu cue bat dau <= moc nay")
    ap.add_argument("--drop-optional", dest="drop_optional", action="store_true",
                    help="bo moi cue co optional=true (bo phan ngoai hook)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not a.cues or not a.out or a.total is None:
        C.die("thieu tham so.\n"
              "    python scripts/build_sfx.py --cues <x.cues.json> "
              "--out <x.sfx.raw> --total <giay>")
    if not os.path.isfile(a.cues):
        C.die("khong thay cue sheet: %s" % a.cues)

    lib = a.lib
    if not lib:
        F.add_sfx_path()
        try:
            import _common as S
            lib, files, _src, _n = S.find_sfx_library(a.resources)
        except Exception:
            lib, files = None, []
        if not lib or not files:
            C.die("khong tim thay thu vien SFX.\n"
                  "  Dua thang: --lib \"<thu-muc-co-file-mp3-wav>\"\n"
                  "  hoac:      --resources \"<thu-muc-co-sound-effects>\"\n"
                  "  Chay preflight de xem huong dan day du.")
    if not os.path.isdir(lib):
        C.die("thu muc SFX khong ton tai: %s" % lib)

    F.banner("BUOC 8 — DUNG LOP SFX",
             ["cue sheet : %s" % a.cues,
              "thu vien  : %s" % lib,
              "do dai    : %.3fs" % a.total,
              "loc       : %s%s"
              % ("bo cue tuy chon; " if a.drop_optional else "",
                 ("chi <= %.2fs" % a.max_t) if a.max_t is not None else "giu het")])

    if a.dry_run:
        cues = C.read_json(a.cues)
        if isinstance(cues, dict):
            cues = cues.get("sfx") or cues.get("cues") or []
        keep = [c for c in cues
                if (a.max_t is None or c["t"] <= a.max_t)
                and not (a.drop_optional and c.get("optional"))]
        miss = sorted({c["file"] for c in keep
                       if not os.path.isfile(os.path.join(lib, c["file"]))})
        print("")
        print("  [dry-run] %d/%d cue se duoc dat, khong ghi file."
              % (len(keep), len(cues)))
        if miss:
            C.die("thieu %d file SFX trong %s:\n    %s"
                  % (len(miss), lib, "\n    ".join(miss)))
        print("  Tat ca file SFX can dung deu co trong thu vien.")
        print("")
        return

    F.add_tools_path()
    F.require("build_sfx_json", kind="tool")
    import build_sfx_json as B
    B.LIB = lib                      # doi thu vien, KHONG sua file goc

    argv = ["build_sfx_json", "--cues", a.cues, "--out", a.out,
            "--total", "%.6f" % a.total]
    if a.max_t is not None:
        argv += ["--max-t", "%.6f" % a.max_t]
    if a.drop_optional:
        argv += ["--drop-optional"]
    old = sys.argv
    sys.argv = argv
    try:
        B.main()
    finally:
        sys.argv = old
    print("")


if __name__ == "__main__":
    C.run_main(main)
