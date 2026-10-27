# -*- coding: utf-8 -*-
"""nns-full-pass — ca day hau ky video talking-head tieng Viet, MOT lenh.

    python scripts/fullpass.py --video "tho.mp4" --out "xong.mp4"        # lap ke hoach
    python scripts/fullpass.py --video "tho.mp4" --out "xong.mp4" --go   # render that

MAC DINH la DUNG LAI SAU KHI LAP KE HOACH (buoc 0..6a). Ly do: bang vung an
toan, cue sheet SFX va danh sach the chu phai duoc nguoi duyet TRUOC khi render.
Them --go de chay not.

Buoc da co ket qua thi bo qua (chay lai khong lam lai tu dau). --force lam lai het.

    0) preflight    kiem ffmpeg / thu vien / font / video
    1) cut          cat khoang lang            -> <goc>.cut.mp4     (bo qua neu --no-cut)
    2) layout       TU DO bo cuc               -> <goc>.layout.json
    3) transcribe   faster-whisper word-level  -> <goc>.sub.words.json  (co cache)
    4) fix          sua token + dau cham cuoi cau -> <goc>.sub.fixed.json
    5) sub          .ass karaoke theo --safe do duoc -> <goc>.sub.ass
    6) cards        de xuat cue + cho the, kiem, gop vao CUNG file .ass
    ------------------------------- CHO DUYET -------------------------------
    7) burn         ve chu — MA HOA HINH DUNG 1 LAN, tieng copy nguyen
    8) sfx          dung lop SFX tu cue sheet -> <goc>.sfx.raw
    9) master       tron + chuan hoa + mux -c:v copy -> --out
   10) verify       do lai tat ca. Khong exit 0 thi khong duoc bao xong.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpcommon as F  # noqa: E402

C = F.need_C()
HERE = os.path.dirname(os.path.abspath(__file__))


def mine(script):
    return os.path.join(HERE, script)


def fresh(path, force):
    return (not force) and path and os.path.isfile(path) and os.path.getsize(path) > 0


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser(
        description="Ca day hau ky: cat lang -> sub -> the chu -> SFX -> master")
    ap.add_argument("--video", help="video THO dau vao")
    ap.add_argument("--out", help="video HOAN CHINH ghi ra")
    ap.add_argument("--resources", help="thu muc co Font/ va sound-effects/ rieng")
    ap.add_argument("--go", action="store_true",
                    help="render that (mac dinh chi lap ke hoach roi dung cho duyet)")
    ap.add_argument("--force", action="store_true", help="lam lai moi buoc")
    ap.add_argument("--dry-run", action="store_true",
                    help="chi in ke hoach cac buoc, khong dung toi file nao")
    # buoc 1
    ap.add_argument("--no-cut", dest="no_cut", action="store_true",
                    help="khong cat khoang lang, dung thang video vao")
    ap.add_argument("--keep", help="chuyen thang cho cut_silence.py")
    ap.add_argument("--guard", help="chuyen thang cho cut_silence.py")
    # buoc 2
    ap.add_argument("--scene", type=float, default=0.25)
    ap.add_argument("--min-seg", dest="min_seg", type=float, default=2.5)
    ap.add_argument("--safe", help="tu dat --safe, bo qua ket qua do tu dong")
    ap.add_argument("--no-face", dest="no_face", action="store_true")
    # buoc 3-5
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--language", default="vi")
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    ap.add_argument("--fixes")
    ap.add_argument("--keep-commas", dest="keep_commas", action="store_true",
                    help="giu dau phay trong sub (mac dinh bo)")
    ap.add_argument("--font")
    ap.add_argument("--font-size", dest="font_size", type=int)
    ap.add_argument("--max-words", dest="max_words", type=int, default=4)
    ap.add_argument("--max-chars", dest="max_chars", type=int, default=22)
    ap.add_argument("--active-color", dest="active_color", default="#FFD600")
    # buoc 6
    ap.add_argument("--no-cards", dest="no_cards", action="store_true")
    ap.add_argument("--card-every", dest="card_every", type=float, default=12.0)
    ap.add_argument("--hook-len", dest="hook_len", type=float, default=20.0)
    ap.add_argument("--density", type=float, default=0.60)
    ap.add_argument("--tail-density", dest="tail_density", type=float, default=0.12)
    ap.add_argument("--risers", type=int, default=1)
    # buoc 7-9
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--no-sfx", dest="no_sfx", action="store_true")
    ap.add_argument("--drop-optional", dest="drop_optional", action="store_true",
                    help="bo moi cue SFX ngoai hook (KHONG phai render lai hinh)")
    ap.add_argument("--max-t", dest="max_t", type=float, default=None)
    ap.add_argument("--target", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-2.0)
    a = ap.parse_args()

    if not a.video or not a.out:
        thieu = [x for x, v in (("--video (video tho)", a.video),
                                ("--out (file ket qua)", a.out)) if not v]
        C.die("thieu tham so bat buoc: %s\n"
              "  Goi day du:\n"
              "      python scripts/fullpass.py --video \"D:\\quay\\tho.mp4\" "
              "--out \"D:\\quay\\xong.mp4\"" % ", ".join(thieu))

    P = F.stem_paths(a.out)
    res = ["--resources", a.resources] if a.resources else []

    F.banner("nns-full-pass — ca day hau ky trong MOT lenh",
             ["video vao : %s" % a.video,
              "video ra  : %s" % a.out,
              "tai nguyen: %s" % (a.resources or "(dung assets kem san)"),
              "che do    : %s" % ("RENDER THAT (--go)" if a.go
                                  else "LAP KE HOACH roi dung cho duyet"),
              "cat lang  : %s" % ("KHONG (--no-cut)" if a.no_cut else "co"),
              "SFX       : %s" % ("KHONG (--no-sfx)" if a.no_sfx else "co"),
              "the chu   : %s" % ("KHONG (--no-cards)" if a.no_cards else "co")])

    if a.dry_run:
        src = a.video if a.no_cut else P["cut"]
        rows = [
            ("0", "preflight.py", "kiem ffmpeg/thu vien/font/video", "-"),
            ("1", "cut_silence.py (nns-cut-silence)",
             "bo qua (--no-cut)" if a.no_cut else "cat khoang lang",
             "-" if a.no_cut else P["cut"]),
            ("2", "layout.py", "do bo cuc -> chuoi --safe", P["layout"]),
            ("3", "transcribe.py (nns-auto-sub)",
             "faster-whisper %s, word-level, co cache" % a.model, P["words"]),
            ("4", "fix_tokens.py (nns-auto-sub)",
             "sua token nghe sai (Cloud->Claude...)", P["fixed"]),
            ("4b", "punct.py", "them dau cham cuoi cau, bo dau phay", P["fixed"]),
            ("5", "build_ass.py (nns-auto-sub)",
             "sub karaoke theo --safe do duoc", P["ass"]),
            ("6a", "plan_cues.py", "de xuat cue SFX + cho the chu",
             "%s, %s" % (os.path.basename(P["cues"]), os.path.basename(P["cards"]))),
            ("6b", "check_cards.py", "kiem the chu (khong dat = khong burn)", "-"),
            ("6c", "cards_to_ass.py (tools/sfx_pass)",
             "gop the vao CUNG file .ass", P["merged"]),
            ("7", "burn.py (nns-auto-sub)",
             "ve chu, MA HOA HINH 1 LAN, tieng copy", P["sub"]),
            ("8", "build_sfx.py", "dung lop SFX tu cue sheet", P["bed"]),
            ("9", "master.py", "tron + chuan hoa + mux -c:v copy", P["final"]),
            ("10", "verify_all.py", "do lai 6 thu", "-"),
        ]
        print("")
        print("  KE HOACH — %d buoc" % len(rows))
        print("  " + F.hr("-"))
        print("  %-4s %-38s %s" % ("#", "script", "lam gi"))
        print("  " + F.hr("-"))
        for n, s, what, outp in rows:
            print("  %-4s %-38s %s" % (n, s, what))
            if outp != "-":
                print("  %-4s %-38s -> %s" % ("", "", outp))
        print("  " + F.hr("-"))
        print("  nguon cho buoc 2..7 : %s" % src)
        print("  GATE               : mac dinh dung sau buoc 6, cho duyet bang,")
        print("                       cue sheet va the chu. Them --go de render.")
        print("")
        print("  [dry-run] khong dung toi file nao.")
        print("")
        return

    # ---------------------------------------------------------------- 0
    pf = ["--video", a.video] + res
    if a.font:
        pf += ["--font", a.font]
    F.step("BUOC 0 — preflight", F.py(mine("preflight.py"), pf))

    # ---------------------------------------------------------------- 1
    if a.no_cut:
        src = os.path.abspath(a.video)
        print("")
        print("  BUOC 1 — bo qua cat khoang lang (--no-cut)")
    elif fresh(P["cut"], a.force):
        src = P["cut"]
        print("")
        print("  BUOC 1 — da co %s, bo qua (them --force de cat lai)"
              % os.path.basename(P["cut"]))
    else:
        args = ["--video", a.video, "--out", P["cut"]]
        for flag, v in (("--keep", a.keep), ("--guard", a.guard)):
            if v:
                args += [flag, v]
        F.step("BUOC 1 — cat khoang lang", F.py(F.require("cut"), args))
        src = P["cut"]

    # ---------------------------------------------------------------- 2
    if fresh(P["layout"], a.force) and not a.safe:
        print("")
        print("  BUOC 2 — da co %s, bo qua" % os.path.basename(P["layout"]))
    else:
        args = ["--video", src, "--out", P["layout"], "--scene", a.scene,
                "--min-seg", a.min_seg] + res
        if a.font:
            args += ["--font", a.font]
        if a.font_size:
            args += ["--font-size", a.font_size]
        if a.no_face:
            args += ["--no-face"]
        F.step("BUOC 2 — do bo cuc, chon cho dat chu",
               F.py(mine("layout.py"), args))
    lay = C.read_json(P["layout"]) if os.path.isfile(P["layout"]) else {}
    safe = a.safe or lay.get("safe")

    # ---------------------------------------------------------------- 3
    base = ["--video", src, "--out", P["sub"]] + res
    if fresh(P["words"], a.force):
        print("")
        print("  BUOC 3 — da co transcript %s, bo qua" % os.path.basename(P["words"]))
    else:
        F.step("BUOC 3 — nhan dang loi noi (word-level)",
               F.py(F.require("transcribe"),
                    base + ["--model", a.model, "--language", a.language,
                            "--device", a.device]))

    # ---------------------------------------------------------------- 4
    args = list(base)
    if a.fixes:
        args += ["--fixes", a.fixes]
    F.step("BUOC 4 — sua token nghe sai",
           F.py(F.require("fix"), args))
    F.step("BUOC 4b — dau cham cuoi cau (truoc khi gom cum sub)",
           F.py(mine("punct.py"),
                ["--words", P["fixed"] if os.path.isfile(P["fixed"]) else P["words"]]
                + (["--keep-commas"] if a.keep_commas else [])))

    # ---------------------------------------------------------------- 5
    args = base + ["--max-words", a.max_words, "--max-chars", a.max_chars,
                   "--active-color", a.active_color]
    if safe:
        args += ["--safe", safe]
    if a.font:
        args += ["--font", a.font]
    if a.font_size:
        args += ["--font-size", a.font_size]
    F.step("BUOC 5 — dung sub karaoke (.ass)",
           F.py(F.require("build_ass"), args))

    # ---------------------------------------------------------------- 6a
    if fresh(P["cues"], a.force) and (a.no_cards or fresh(P["cards"], a.force)):
        print("")
        print("  BUOC 6a — da co cue sheet / the chu, bo qua (--force de de xuat lai)")
    else:
        args = ["--words", P["fixed"] if os.path.isfile(P["fixed"]) else P["words"],
                "--layout", P["layout"], "--out-cues", P["cues"],
                "--hook-len", a.hook_len, "--density", a.density,
                "--tail-density", a.tail_density, "--risers", a.risers,
                "--card-every", a.card_every] + res
        if a.no_cards:
            args += ["--no-cards"]
        else:
            args += ["--out-cards", P["cards"]]
        F.step("BUOC 6a — de xuat cue SFX + cho dat the chu",
               F.py(mine("plan_cues.py"), args))

    # ------------------------------------------------------------- GATE
    if not a.go:
        print("")
        print("  " + F.hr())
        print("  DUNG O DAY — cho duyet. Chua ve gi vao video.")
        print("  " + F.hr())
        print("    Doc lai 3 thu o tren:")
        print("      1. BANG BO CUC       (buoc 2) — chu se dat o dau, vi sao")
        print("      2. CUE SHEET SFX     (buoc 6a) — %s"
              % os.path.basename(P["cues"]))
        if not a.no_cards:
            print("      3. CHO DAT THE CHU   (buoc 6a) — %s"
                  % os.path.basename(P["cards"]))
            print("")
            print("    The chu dang de text RONG. Dien noi dung cho tung the")
            print("    (<=4 chu, va phai noi thu sub CHUA noi), the nao khong")
            print("    dung thi xoa han khoi file.")
        print("")
        print("    Sua file JSON o tren tuy y, roi chay lai co --go:")
        print("        python scripts/fullpass.py --video \"%s\" --out \"%s\" --go"
              % (a.video, a.out))
        print("")
        return

    # ---------------------------------------------------------------- 6b/6c
    ass_for_burn = P["ass"]
    cards_ok = False
    if not a.no_cards:
        if not os.path.isfile(P["cards"]):
            C.die("khong thay file the chu: %s\n"
                  "  Chay lai khong co --go de de xuat cho dat, hoac them --no-cards."
                  % P["cards"])
        cards = C.read_json(P["cards"])
        cards = [c for c in cards if (c.get("text") or "").strip()]
        if not cards:
            print("")
            print("  BUOC 6b — moi the deu con text rong -> BO HAN lop the chu.")
            print("            (video van co sub va SFX binh thuong)")
        else:
            C.write_json(P["cards"], cards)
            args = ["--cards", P["cards"], "--layout", P["layout"],
                    "--words", P["fixed"] if os.path.isfile(P["fixed"]) else P["words"]] + res
            if a.font:
                args += ["--font", a.font]
            F.step("BUOC 6b — kiem the chu", F.py(mine("check_cards.py"), args))
            plan = C.read_json(P["subplan"])
            args = ["--ass", P["ass"], "--cards", P["cards"], "--out", P["merged"],
                    "--width", plan["video_w"], "--font", plan["font_file"]]
            F.step("BUOC 6c — gop the vao CUNG file .ass (1 lan ma hoa hinh)",
                   F.py(F.require("cards_to_ass", kind="tool"), args))
            ass_for_burn = P["merged"]
            cards_ok = True

    # ---------------------------------------------------------------- 7
    F.step("BUOC 7 — ve chu vao video (ma hoa hinh DUNG 1 lan)",
           F.py(F.require("burn"),
                base + ["--ass", ass_for_burn, "--crf", a.crf,
                        "--preset", a.preset]))

    # ---------------------------------------------------------------- 8
    cut_info = C.probe_video(src)
    total = C.count_frames(P["sub"]) / float(cut_info["fps"] or 30.0)
    if a.no_sfx:
        print("")
        print("  BUOC 8 — bo qua lop SFX (--no-sfx)")
        bed = None
    else:
        args = ["--cues", P["cues"], "--out", P["bed"], "--total", "%.6f" % total] + res
        if a.drop_optional:
            args += ["--drop-optional"]
        if a.max_t is not None:
            args += ["--max-t", a.max_t]
        F.step("BUOC 8 — dung lop SFX", F.py(mine("build_sfx.py"), args))
        bed = P["bed"]

    # ---------------------------------------------------------------- 9
    args = ["--video", P["sub"], "--out", P["final"], "--work", P["work"],
            "--target", a.target, "--tp", a.tp] + res
    if bed:
        args += ["--bed", bed]
    else:
        args += ["--no-sfx"]
    F.step("BUOC 9 — tron SFX + chuan hoa + mux (-c:v copy)",
           F.py(mine("master.py"), args))

    # ---------------------------------------------------------------- 10
    args = ["--src", src, "--out", P["final"], "--plan", P["subplan"],
            "--ab", P["ab"], "--target", a.target, "--tp", a.tp] + res
    if cards_ok:
        args += ["--cards", P["cards"]]
    if bed:
        args += ["--cues", P["cues"]]
    else:
        args += ["--skip-sfx"]
    F.step("BUOC 10 — verify", F.py(mine("verify_all.py"), args))

    print("")
    print("  " + F.hr())
    print("  XONG. verify_all.py da do 6 thu va bao DAT.")
    print("  " + F.hr())
    print("    video : %s" % os.path.abspath(a.out))
    print("    sub   : %s" % ass_for_burn)
    print("    cue   : %s" % P["cues"])
    print("")
    print("    Trich vai frame de soi:")
    print("        python scripts/frames.py --video \"%s\" --plan \"%s\"%s"
          % (a.out, P["subplan"],
             " --cards \"%s\"" % P["cards"] if cards_ok else ""))
    print("")
    print("    Muon bo het SFX ngoai hook — KHONG phai render lai hinh:")
    print("        python scripts/build_sfx.py --cues \"%s\" --out \"%s\" "
          "--total %.3f --drop-optional" % (P["cues"], P["bed"], total))
    print("        python scripts/master.py --video \"%s\" --bed \"%s\" --out \"%s\""
          % (P["sub"], P["bed"], P["final"]))
    print("")


if __name__ == "__main__":
    C.run_main(main)
