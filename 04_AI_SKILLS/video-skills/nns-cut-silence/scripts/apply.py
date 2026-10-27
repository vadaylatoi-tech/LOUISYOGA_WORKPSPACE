# -*- coding: utf-8 -*-
"""nns-cut-silence / apply.py — THUC HIEN CAT theo plan.json.

Cach lam (da kiem thuc te, xem references/cac-cai-bay.md):
  * Hinh va tieng duoc cat RIENG nhung tu CUNG mot danh sach frame:
      hinh   : trim=start_frame=A:end_frame=B  (frame-exact, KHONG dung -ss)
      tieng  : atrim=start_sample=S0:end_sample=S1 (sample-exact)
    S0/S1 tinh tu chi so frame bang Fraction nen khong tich luy sai so.
  * Noi lai bang filter_complex concat (KHONG dung concat demuxer — no tut ve 25fps).
  * Luon ep fps dau ra bang -r <fps> va PHAI kiem lai nb_frames (verify.py lam).
  * Cuoi chuoi audio co apad + atrim=end_sample=<du kien> nen do dai tieng LUON
    bang do dai hinh dung den mau.

TIENG DAU RA — quyet dinh va ly do:
  * File chinh (--out) mang tieng AAC 256k: de xem/nghe ngay, ai cung mo duoc.
  * KEM THEO mot file WAV pcm_s16le ben canh (<out>.wav, doi --wav de doi cho).
    Day moi la BAN GOC de cac buoc sau (them SFX, chuan hoa loudness) dung,
    tranh nen lossy nhieu doi (AAC -> AAC -> AAC lam mat cao va vo true-peak).
    Muon file chinh khong co tieng luon thi dung --no-mux-audio.

Vi du:
    python scripts/apply.py --video raw.mp4 --plan plan.json --out cut.mp4
    python scripts/apply.py --video raw.mp4 --plan plan.json --out cut.mp4 --crf 14 --preset slow
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_io()

SAFE_PIX = ("yuv420p", "yuv422p", "yuv444p", "yuv420p10le", "yuv422p10le", "yuv444p10le",
            # yuvj* = FULL RANGE (0-255). PHAI giu nguyen, khong duoc doi sang yuv420p:
            # da do that tren file CapCut xuat ra (yuvj420p, color_range=pc) — doi sang
            # yuv420p lam ffmpeg nen dai mau 0-255 -> 16-235, anh nhat di, do luma
            # trung binh nhay 29.9 -> 41.5 va MAE toan frame 12.3/255. Xem
            # references/cac-cai-bay.md muc 14.
            "yuvj420p", "yuvj422p", "yuvj444p")


def ffmpeg_major():
    exe = C.need_tool("ffmpeg")
    try:
        out = subprocess.run([exe, "-version"], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL
                             ).stdout.decode("utf-8", "replace")
        m = re.search(r"version\s+n?(\d+)", out)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def build_graph(plan, want_mux, want_wav):
    """Sinh noi dung filter_complex. Khong chua duong dan nao (tranh bay dau hai cham).

    QUAN TRONG: chi sinh dung nhung dau ra se duoc -map. Mot pad treo lo lung
    (vd asplit ra [awav] ma khong ai map) lam ffmpeg bao
    "Error binding filtergraph inputs/outputs" — xem references/cac-cai-bay.md.
    """
    keeps = plan["keeps"]
    n = len(keeps)
    if n == 0:
        C.die("Plan khong co doan nao de giu.")
    lines = []
    for i, k in enumerate(keeps):
        lines.append("[0:v]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[v%d];"
                     % (k["old_start_frame"], k["old_end_frame"], i))
    if n == 1:
        lines.append("[v0]null[vout];")
    else:
        lines.append("".join("[v%d]" % i for i in range(n))
                     + "concat=n=%d:v=1:a=0[vout];" % n)

    if not (want_mux or want_wav):
        return "\n".join(lines).rstrip(";")

    for i, k in enumerate(keeps):
        lines.append("[0:a]atrim=start_sample=%d:end_sample=%d,asetpts=PTS-STARTPTS[a%d];"
                     % (k["start_sample"], k["end_sample"], i))
    if n == 1:
        lines.append("[a0]anull[acat];")
    else:
        lines.append("".join("[a%d]" % i for i in range(n))
                     + "concat=n=%d:v=0:a=1[acat];" % n)

    # apad + atrim => do dai tieng dung bang du kien, den tung mau.
    tail = "[acat]apad,atrim=end_sample=%d,asetpts=PTS-STARTPTS" \
           % plan["expected"]["audio_samples"]
    if want_mux and want_wav:
        tail += ",asplit=2[aout][awav]"
    elif want_mux:
        tail += "[aout]"
    else:
        tail += "[awav]"
    lines.append(tail)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--wav", default=None, help="duong dan WAV goc kem theo (mac dinh <out>.wav)")
    ap.add_argument("--no-wav", dest="no_wav", action="store_true", help="khong xuat WAV kem theo")
    ap.add_argument("--no-mux-audio", dest="no_mux_audio", action="store_true",
                    help="file chinh khong co tieng (chi WAV moi co)")
    ap.add_argument("--allow-no-audio", dest="allow_no_audio", action="store_true",
                    help="cho phep --no-wav + --no-mux-audio (ket qua IM LANG hoan toan)")
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--vcodec", default="libx264")
    ap.add_argument("--pix-fmt", dest="pix_fmt", default="auto")
    ap.add_argument("--audio-bitrate", dest="abr", default="256k")
    ap.add_argument("--dry-run", dest="dry_run", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(a.plan):
        C.die("Khong tim thay plan: %s\n       Chay plan.py truoc." % a.plan)
    plan = C.read_json(a.plan)
    if plan.get("skill") != C.SKILL_NAME:
        C.die("File plan khong phai cua %s (skill=%r)." % (C.SKILL_NAME, plan.get("skill")))
    if plan.get("plan_version") != C.PLAN_VERSION:
        C.die("Plan phien ban %r khong khop scripts (%r). Chay lai plan.py."
              % (plan.get("plan_version"), C.PLAN_VERSION))

    info = C.probe(a.video)
    pv = plan["video"]
    if info["nb_frames"] != pv["nb_frames"] or info["fps_text"] != pv["fps"]:
        C.die("Video khong khop plan.\n"
              "       plan : %d frame, %s fps\n"
              "       file : %d frame, %s fps\n"
              "       Chay lai plan.py cho dung file nay."
              % (pv["nb_frames"], pv["fps"], info["nb_frames"], info["fps_text"]))

    fps = info["fps"]

    pix = a.pix_fmt
    if pix == "auto":
        pix = info["pix_fmt"] if info["pix_fmt"] in SAFE_PIX else "yuv420p"

    out_dir = os.path.dirname(os.path.abspath(a.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    wav_path = None
    if not a.no_wav:
        wav_path = a.wav or (os.path.splitext(a.out)[0] + ".wav")
    if a.no_wav and a.no_mux_audio and not a.allow_no_audio:
        # DUNG NGAY: da thu that, to hop nay tao ra file KHONG CO TIENG, sau do
        # verify.py bao SAI o cuoi (sau khi da encode xong ca video) — vua mat
        # thoi gian vua kho hieu. Tu choi som, va noi ro phai lam gi.
        C.die(
            "--no-wav + --no-mux-audio cung luc => file ket qua KHONG CO TIENG gi ca,\n"
            "       ma skill nay ton tai la de cat tieng cho khop hinh. Chon 1 trong 3:\n"
            "\n"
            "       1) Bo ca 2 co (khuyen dung): ra mp4 co tieng AAC + WAV pcm kem theo\n"
            "            python scripts/apply.py --video \"%s\" --plan \"%s\" --out \"%s\"\n"
            "\n"
            "       2) Chi can WAV, mp4 khong can tieng: bo rieng --no-wav\n"
            "            python scripts/apply.py --video \"%s\" --plan \"%s\" --out \"%s\" --no-mux-audio\n"
            "\n"
            "       3) That su muon video IM LANG hoan toan: them co --allow-no-audio\n"
            "          (khi do verify.py se khong doi chieu duoc tieng, chi kiem hinh)\n"
            % (a.video, a.plan, a.out, a.video, a.plan, a.out)
        )

    graph = build_graph(plan, want_mux=not a.no_mux_audio, want_wav=bool(wav_path))

    ffmpeg = C.need_tool("ffmpeg")
    gfd, gpath = tempfile.mkstemp(prefix="nns_cut_", suffix=".ffgraph", text=True)
    os.close(gfd)
    with open(gpath, "w", encoding="utf-8") as fh:
        fh.write(graph + "\n")

    graph_opt = ["-/filter_complex", gpath] if ffmpeg_major() >= 7 else \
                ["-filter_complex_script", gpath]

    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-y", "-i", a.video]
    cmd += graph_opt
    cmd += ["-map", "[vout]"]
    if not a.no_mux_audio:
        cmd += ["-map", "[aout]"]
    cmd += ["-map_chapters", "-1",
            "-c:v", a.vcodec, "-crf", str(a.crf), "-preset", a.preset,
            "-pix_fmt", pix, "-r", "%d/%d" % (fps.numerator, fps.denominator)]
    for opt, key in (("-color_range", "color_range"), ("-colorspace", "color_space"),
                     ("-color_primaries", "color_primaries"), ("-color_trc", "color_transfer")):
        val = info.get(key)
        if val and val not in ("unknown", "unspecified"):
            cmd += [opt, val]
    if not a.no_mux_audio:
        cmd += ["-c:a", "aac", "-b:a", a.abr]
    if os.path.splitext(a.out)[1].lower() in (".mp4", ".m4v", ".mov"):
        cmd += ["-movflags", "+faststart"]
    cmd += ["-stats", a.out]
    if wav_path:
        cmd += ["-map", "[awav]", "-c:a", "pcm_s16le", wav_path]

    print("")
    print("  nns-cut-silence — APPLY")
    print("  " + "-" * 58)
    print("  Vao        : %s" % a.video)
    print("  Ra (hinh)  : %s  (%s crf %d preset %s pix %s)"
          % (a.out, a.vcodec, a.crf, a.preset, pix))
    print("  Ra (tieng) : %s" % (wav_path or "(khong xuat WAV)"))
    print("  Doan giu   : %d   Nhat cat: %d" % (len(plan["keeps"]), plan["expected"]["cuts"]))
    print("  Du kien    : %d frame, %.3fs, %d sample audio"
          % (plan["expected"]["frames"], plan["expected"]["duration"],
             plan["expected"]["audio_samples"]))
    print("")

    if a.dry_run:
        print("  --dry-run: KHONG chay ffmpeg. Filter graph:")
        print("")
        for line in graph.splitlines():
            print("    " + line)
        print("")
        print("  Lenh:")
        print("    " + " ".join('"%s"' % c if " " in c else c for c in cmd))
        print("")
        os.unlink(gpath)
        return

    rc = subprocess.call(cmd, stdin=subprocess.DEVNULL)
    try:
        os.unlink(gpath)
    except Exception:
        pass
    if rc != 0:
        C.die("ffmpeg that bai (ma %d). Xem thong bao ffmpeg o tren." % rc)

    got = C.count_video_packets(a.out)
    print("")
    print("  Xong. So frame dau ra: %s (du kien %d)"
          % (got, plan["expected"]["frames"]))
    if got != plan["expected"]["frames"]:
        C.die("SO FRAME KHONG DUNG KE HOACH (%s != %d).\n"
              "       Day dung la cai bay concat/fps. Xem references/cac-cai-bay.md.\n"
              "       Dung file nay, bao loi len."
              % (got, plan["expected"]["frames"]))
    print("")
    print("  Buoc tiep theo (BAT BUOC):")
    print("      python scripts/verify.py --video \"%s\" --plan \"%s\" --out \"%s\""
          % (a.video, a.plan, a.out))
    print("")


if __name__ == "__main__":
    main()
