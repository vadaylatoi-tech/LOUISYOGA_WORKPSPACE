# -*- coding: utf-8 -*-
"""apply.py - render cac doan punch-in bang zoompan (MOT chuoi filter duy nhat).

    python apply.py --video <video> --plan plan.json --out ket_qua.mp4 [--dry-run]

Cong thuc zoompan da kiem tren may nay (xem references/zoompan-cong-thuc.md):
    zoompan=z='<bieu thuc theo on>':x='<CX>-(iw/(2*zoom))':y='<CY>-(ih/(2*zoom))'
            :d=1:s=<W>x<H>:fps=<fps>
- d=1  -> 1 frame ra cho 1 frame vao, khong sinh them frame.
- zoompan tu KEP x/y vao vung hop le, nen z=1 cho ra frame nguyen goc.
- 'on' la chi so frame RA; vi d=1 va fps khong doi nen on == chi so frame VAO.

Am thanh: -c:a copy, KHONG ma hoa lai (khong lam suy giam, khong lech loudness).
Ca do thi filter duoc ghi ra FILE va nap bang -filter_complex_script: bieu thuc
z/x/y co the dai vai nghin ky tu, nhet vao dong lenh Windows la de vo.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facelib as F  # noqa: E402


def ease(var, a, b, mode, rev=False):
    """Bieu thuc ffmpeg cho tien do 0..1 giua frame a va frame b.

    rev=False: 0 tai a  -> 1 tai b   (ramp VAO)
    rev=True : 1 tai a  -> 0 tai b   (ramp RA)

    CAI BAY: neu ramp ra ma van dung dang thuan roi doi cho a/b thi ham tra ve
    hang so 1 -> cu zoom khong nha ra, den frame cuoi window moi giat ve 1.
    Da mac dung loi nay mot lan; do la ly do co tham so rev.
    """
    if b <= a:
        return "0" if rev else "1"
    p = ("((%d-%s)/%d)" % (b, var, b - a) if rev
         else "((%s-%d)/%d)" % (var, a, b - a))
    if mode == "linear":
        return p
    # smoothstep: vao/ra mem, khong giat o dau va cuoi cu day may
    return "(%s*%s*(3-2*%s))" % (p, p, p)


def zoom_expr(windows, mode):
    """Bieu thuc z theo 'on'. Long nhau tung window, ngoai window thi z=1."""
    expr = "1"
    for wd in reversed(windows):
        f0, f1 = wd["f_start"], wd["f_hold_start"]
        f2, f3 = wd["f_hold_end"], wd["f_end"]
        z = wd["zoom"]
        ein = "1+%.6f*%s" % (z - 1.0, ease("on", f0, f1, mode))
        eout = "1+%.6f*%s" % (z - 1.0, ease("on", f2, f3, mode, rev=True))
        inner = ("if(lt(on,%d),%s,if(lte(on,%d),%.6f,%s))"
                 % (f1, ein, f2, z, eout))
        expr = "if(between(on,%d,%d),%s,%s)" % (f0, f3, inner, expr)
    return expr


def center_expr(windows, key, default_expr):
    expr = default_expr
    for wd in reversed(windows):
        expr = "if(between(on,%d,%d),%.3f,%s)" % (
            wd["f_start"], wd["f_end"], wd[key], expr)
    return expr


def build_graph(plan, mode):
    w, h, fps = plan["w"], plan["h"], plan["fps"]
    wins = plan["windows"]
    z = zoom_expr(wins, mode)
    cx = center_expr(wins, "cx", "iw/2")
    cy = center_expr(wins, "cy", "ih/2")
    return ("[0:v]zoompan=z='%s'"
            ":x='(%s)-(iw/(2*zoom))'"
            ":y='(%s)-(ih/(2*zoom))'"
            ":d=1:s=%dx%d:fps=%.6f[v]" % (z, cx, cy, w, h, fps))


def main():
    F.setup_io()
    F.require_numpy()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--plan", required=True, help="file plan JSON tu plan.py")
    ap.add_argument("--out", required=True, help="file video ket qua")
    ap.add_argument("--resources", default=None)
    ap.add_argument("--ease", choices=["smooth", "linear"], default="smooth",
                   help="kieu vao/ra cua cu zoom (mac dinh smooth)")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--dry-run", action="store_true",
                    help="in do thi filter + dong lenh ffmpeg, KHONG xuat file")
    a = ap.parse_args()

    if not os.path.isfile(a.plan):
        F.die("khong thay file plan: %s\n"
              "     Chay truoc: python scripts/plan.py --video \"%s\" --track track.json "
              "--out plan.json --every 20" % (a.plan, a.video))
    plan = F.read_json(a.plan)
    if plan.get("che_do") == "report-safe-zones":
        F.die("file nay la bao cao safe zone, khong phai ke hoach punch-in.\n"
              "     Chay lai plan.py KHONG co --report-safe-zones de co plan.")
    wins = plan.get("windows") or []
    if not wins:
        F.die("plan khong co window nao -> khong co gi de render.")

    try:
        meta = F.probe(a.video)
    except Exception as exc:
        F.die(str(exc))
    if (meta["w"], meta["h"]) != (plan["w"], plan["h"]):
        F.die("video hien tai %dx%d khac video luc lap plan %dx%d.\n"
              "     Toa do zoom se sai. Chay lai track.py + plan.py cho video nay."
              % (meta["w"], meta["h"], plan["w"], plan["h"]))
    if abs(meta["fps"] - plan["fps"]) > 0.01:
        F.die("fps hien tai %.3f khac fps luc lap plan %.3f.\n"
              "     Moc frame se lech. Chay lai track.py + plan.py cho video nay."
              % (meta["fps"], plan["fps"]))
    for wd in wins:
        if wd["f_end"] >= meta["nb_frames"]:
            F.die("window #%d ket thuc o frame %d nhung video chi co %d frame.\n"
                  "     Lap lai plan cho dung video." % (wd["i"], wd["f_end"], meta["nb_frames"]))

    graph = build_graph(plan, a.ease)
    audio = F.has_audio(a.video)

    print("")
    print("  RENDER PUNCH-IN")
    print("  vao        %s  (%dx%d %.2ffps %d frame)"
          % (os.path.basename(a.video), meta["w"], meta["h"], meta["fps"], meta["nb_frames"]))
    print("  ra         %s" % a.out)
    print("  punch      %d doan, ease %s" % (len(wins), a.ease))
    for wd in wins:
        print("             #%d frame %d-%d  zoom -> %.3f  tam (%.0f,%.0f)"
              % (wd["i"], wd["f_start"], wd["f_end"], wd["zoom"], wd["cx"], wd["cy"]))
    print("  am thanh   %s" % ("copy nguyen (-c:a copy)" if audio else "video khong co tieng"))
    print("  video      libx264 crf %d preset %s, giu dung %.3f fps"
          % (a.crf, a.preset, meta["fps"]))
    print("  do thi     %d ky tu" % len(graph))

    out_dir = os.path.dirname(os.path.abspath(a.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    gpath = os.path.join(out_dir or ".",
                         os.path.basename(a.out) + ".filter.txt")

    cmd = ["ffmpeg", "-y", "-v", "error", "-stats", "-i", a.video,
           "-filter_complex_script", gpath,
           "-map", "[v]"]
    if audio:
        cmd += ["-map", "0:a:0", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", str(a.crf), "-preset", a.preset,
            "-pix_fmt", "yuv420p",
            # -r bat buoc: qua filter/concat ffmpeg tung tu tut ve 25fps
            "-r", "%.6f" % meta["fps"],
            "-movflags", "+faststart", a.out]

    if a.dry_run:
        print("")
        print("  DO THI FILTER:")
        print("  " + graph)
        print("")
        print("  DONG LENH:")
        print("  " + " ".join('"%s"' % c if " " in c else c for c in cmd))
        print("")
        print("  --dry-run: khong ghi file nao.")
        print("")
        return

    with open(gpath, "w", encoding="utf-8") as f:
        f.write(graph)
    print("")
    p = subprocess.run(cmd)
    if p.returncode != 0:
        F.die("ffmpeg that bai (ma loi %d).\n"
              "     Do thi filter da luu o: %s\n"
              "     Chay lai bang tay voi -v info de xem loi day du." % (p.returncode, gpath))
    if not os.path.isfile(a.out):
        F.die("ffmpeg bao thanh cong nhung khong co file ra: %s" % a.out)

    try:
        m2 = F.probe(a.out)
    except Exception as exc:
        F.die("file ra khong doc duoc: %s" % exc)
    print("")
    print("  -> %s  (%dx%d %.2ffps %d frame, %.2fs)"
          % (a.out, m2["w"], m2["h"], m2["fps"], m2["nb_frames"], m2["dur"]))
    if m2["nb_frames"] != meta["nb_frames"]:
        print("  CANH BAO: so frame ra (%d) khac vao (%d). verify.py se bao that bai."
              % (m2["nb_frames"], meta["nb_frames"]))
    try:
        os.remove(gpath)
    except OSError:
        pass
    print("")
    print("  Buoc cuoi - BAT BUOC, phai do lai ket qua:")
    print("      python scripts/verify.py --video \"%s\" \\" % a.video)
    print("          --out \"%s\" --plan \"%s\"" % (a.out, a.plan))
    print("")


if __name__ == "__main__":
    main()
