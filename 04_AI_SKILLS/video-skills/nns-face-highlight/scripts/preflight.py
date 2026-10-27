# -*- coding: utf-8 -*-
"""preflight.py - KIEM INPUT truoc khi lam bat cu viec gi.

In bang PASS/FAIL. Neu thieu thu gi -> in khoi huong dan tung buoc roi exit 1.
Ngoai ra chay THU nhan dien mat tren vai frame de bao ngay ti le bat duoc mat:
video toan motion-graphic se ra 0% - DO KHONG PHAI LOI, nhung skill nay khong
dung duoc cho no, phai noi thang thay vi zoom bua.

    python preflight.py --video <video> [--resources <dir>] [--probe-frames 6]
"""
import argparse
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facelib as F  # noqa: E402

LINE = "=" * 60


def quiet_import(name):
    """import mot thu vien nhung CHAN moi traceback no tu in ra.
    Ly do that: khi numpy hong, chinh onnxruntime tu goi traceback.print_exc()
    -> traceback la cua thu vien, khong phai cua ta, nhung nguoi dung van thay
    va tuong skill bi loi. Ta chi can biet co/khong, roi tu in huong dan."""
    import importlib
    buf = io.StringIO()
    old_err, old_out = sys.stderr, sys.stdout
    sys.stderr, sys.stdout = buf, buf
    try:
        return importlib.import_module(name)
    finally:
        sys.stderr, sys.stdout = old_err, old_out


def row(state, name, detail):
    print("    [%s] %s%s" % (state, name.ljust(22 - len(state)), detail))


def main():
    F.setup_io()
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--video", required=True, help="video dau vao")
    ap.add_argument("--out", default=None, help="khong dung o preflight, nhan cho dong bo")
    ap.add_argument("--resources", default=None, help="thu muc tai nguyen rieng (co the bo)")
    ap.add_argument("--probe-frames", type=int, default=6,
                    help="so frame lay mau de thu nhan dien (mac dinh 6)")
    ap.add_argument("--thr", type=float, default=F.DEFAULT_THR)
    ap.add_argument("--dry-run", action="store_true",
                    help="khong doi hoi gi khac, preflight von khong xuat file")
    a = ap.parse_args()

    missing = []   # (tieu_de, khoi_huong_dan)
    print("")
    print("  KIEM TRA DAU VAO - nns-face-highlight")
    print("  " + "-" * 56)

    # 1) ffmpeg / ffprobe
    ok_ff, v_ff = F.have_tool("ffmpeg")
    ok_fp, v_fp = F.have_tool("ffprobe")
    if ok_ff and ok_fp:
        row("OK", "ffmpeg", "%s (ffprobe %s)" % (v_ff, v_fp))
    else:
        row("THIEU", "ffmpeg", "khong goi duoc ffmpeg/ffprobe tu dong lenh")
        missing.append((
            "Chua co ffmpeg/ffprobe (bo cong cu doc + xuat video)",
            "   Windows - chay lenh nay trong PowerShell:\n"
            "       winget install --id Gyan.FFmpeg\n"
            "   Hoac tai ban full tai https://www.gyan.dev/ffmpeg/builds/ roi\n"
            "   them thu muc bin/ vao bien moi truong PATH.\n"
            "   macOS:  brew install ffmpeg\n"
            "   Linux:  sudo apt install ffmpeg\n"
            "   Kiem lai bang:  ffmpeg -version"))

    # 2) numpy
    try:
        numpy = quiet_import("numpy")
        row("OK", "numpy", numpy.__version__)
    except ImportError:
        row("THIEU", "numpy", "chua cai")
        missing.append((
            "Chua cai thu vien numpy (de tinh toan hop mat)",
            "   Chay lenh nay:\n"
            "       pip install numpy"))

    # 3) onnxruntime
    try:
        onnxruntime = quiet_import("onnxruntime")
        row("OK", "onnxruntime", onnxruntime.__version__)
    except ImportError:
        row("THIEU", "onnxruntime", "chua cai")
        missing.append((
            "Chua cai thu vien onnxruntime (de chay model nhan dien mat)",
            "   Chay lenh nay:\n"
            "       pip install onnxruntime\n"
            "   Ban CPU nay du dung, khong can card do hoa."))

    # 3b) --resources: skill nay KHONG bat buoc co, nhung neu nguoi dung da dua
    # thi phai noi ro no co dung duoc hay khong - khong duoc im lang bo qua.
    res_note = None
    if a.resources is None:
        row("OK", "--resources",
            "khong dua (khong bat buoc) - tim model kem san trong skill, xem dong duoi")
    elif not os.path.isdir(a.resources):
        row("THIEU", "--resources", "thu muc khong ton tai: %s" % a.resources)
        missing.append((
            "Thu muc --resources ban dua khong ton tai",
            "   Duong dan da thu:\n"
            "       %s\n"
            "   Skill nay KHONG can --resources (model nhan dien mat da kem san\n"
            "   trong skill). Chon mot trong hai cach:\n"
            "   Cach A (NGAN NHAT) - bo han tham so --resources:\n"
            "       python scripts/preflight.py --video \"%s\"\n"
            "   Cach B - go dung duong dan thu muc tai nguyen cua ban\n"
            "       (thu muc do can co  models/det_10g.onnx  neu ban muon dung\n"
            "        model rieng), roi goi lai --resources \"<duong-dan-dung>\"."
            % (a.resources, a.video)))
    else:
        m_res, _s_res, _t_res = F.find_model(a.resources)
        if m_res and os.path.abspath(m_res).startswith(
                os.path.abspath(a.resources)):
            row("OK", "--resources", "co model rieng: %s" % m_res)
        else:
            row("CANH BAO", "--resources",
                "khong co det_10g.onnx trong thu muc nay - BO QUA, dung ban kem san")
            res_note = (
                "  LUU Y ve --resources:\n"
                "      Thu muc ban dua khong co file det_10g.onnx nen skill DA BO QUA no\n"
                "      va dung model kem san trong skill (dieu nay hoan toan binh thuong:\n"
                "      skill nay khong can --resources).\n"
                "      Neu ban CO Y muon dung model rieng thi tao:\n"
                "          %s/models/det_10g.onnx\n"
                "      Neu khong, cu bo han tham so --resources cho gon."
                % a.resources.rstrip("/\\"))

    # 4) model det_10g.onnx
    model, source, tried = F.find_model(a.resources)
    if model:
        size_mb = os.path.getsize(model) / 1e6
        row("OK", "model mat", "%s (%.1f MB) - nguon: %s"
            % (os.path.basename(model), size_mb, source))
    else:
        row("THIEU", "model mat", "khong tim thay det_10g.onnx")
        tried_txt = "\n".join("         - %s" % t for t in tried)
        missing.append((
            "Chua co file model nhan dien mat det_10g.onnx (17 MB)",
            "   Cach A (NGAN NHAT) - dung file kem san trong skill:\n"
            "       File le ra phai nam o:\n"
            "           %s\n"
            "       Neu ban copy skill sang may khac ma file 17 MB nay bi thieu,\n"
            "       hay copy lai NGUYEN thu muc skill (ke ca thu muc assets/).\n"
            "   Cach B - dung thu muc tai nguyen rieng cua ban:\n"
            "       - Tao thu muc:   <duong-dan-ban-chon>/models/\n"
            "       - Dat file det_10g.onnx vao do\n"
            "       - Goi lai voi:   --resources <duong-dan-ban-chon>\n"
            "   Cach C - chi tro bang bien moi truong (neu ban da co file o cho khac):\n"
            "       PowerShell:  $env:FACE_MODEL_ONNX=\"D:\\duong\\dan\\det_10g.onnx\"\n"
            "       CMD:         set FACE_MODEL_ONNX=D:\\duong\\dan\\det_10g.onnx\n"
            "       macOS/Linux: export FACE_MODEL_ONNX=/duong/dan/det_10g.onnx\n"
            "   Lay file o dau: det_10g.onnx nam trong bo model 'buffalo_l' cua\n"
            "   InsightFace. Cai 'pip install insightface' roi chay 1 lan\n"
            "   FaceAnalysis(name='buffalo_l') se tu tai ve\n"
            "   ~/.insightface/models/buffalo_l/.\n"
            "   Cac cho da tim:\n%s" % (F.BUNDLED_MODEL, tried_txt)))

    # 5) video
    meta = None
    if not os.path.isfile(a.video):
        row("THIEU", "video", "khong ton tai: %s" % a.video)
        missing.append((
            "Khong tim thay file video dau vao",
            "   Duong dan da thu:\n"
            "       %s\n"
            "   Kiem lai duong dan (nho dat trong dau ngoac kep neu co dau cach),\n"
            "   roi goi lai voi --video \"<duong-dan-dung>\"." % a.video))
    else:
        try:
            meta = F.probe(a.video)
            row("OK", "video", "%dx%d %.0ffps %.2fs %d frame (%s)"
                % (meta["w"], meta["h"], meta["fps"], meta["dur"],
                   meta["nb_frames"], meta["codec"]))
            row("OK", "luong am thanh",
                "co - se copy nguyen, khong ma hoa lai" if F.has_audio(a.video)
                else "khong co - video ra se khong co tieng")
        except Exception as exc:
            row("THIEU", "video", str(exc)[:60])
            missing.append((
                "File video khong doc duoc",
                "   Bao loi: %s\n"
                "   Thu mo file bang trinh phat khac. Neu file hong, xuat lai tu\n"
                "   nguon. Neu dinh dang la .mov/.mkv la, chuyen sang mp4:\n"
                "       ffmpeg -i \"<file-goc>\" -c copy \"<file-moi>.mp4\""
                % str(exc)[:200]))

    # 6) thu nhan dien mat that
    hit, tot, avg_score, max_n = 0, 0, 0.0, 0
    if not missing and meta is not None:
        det = F.Detector(model, thr=a.thr)
        scale, sw, sh = F.det_scale(meta["w"], meta["h"])
        n = max(2, int(a.probe_frames))
        idxs = [int(round(i * (meta["nb_frames"] - 1) / float(n - 1)))
                for i in range(n)]
        scores = []
        for _i, img in F.frames_at_indices(a.video, idxs, sw, sh):
            tot += 1
            faces = det(img, sw, sh, scale)
            max_n = max(max_n, len(faces))
            if faces:
                hit += 1
                scores.append(faces[0][1])
        avg_score = sum(scores) / len(scores) if scores else 0.0
        pct = 100.0 * hit / max(tot, 1)
        if tot == 0:
            row("THIEU", "thu nhan dien", "khong giai ma duoc frame nao")
            missing.append((
                "Khong giai ma duoc frame nao tu video",
                "   ffmpeg mo duoc file nhung khong doc ra frame. Thu chuyen ma:\n"
                "       ffmpeg -i \"%s\" -c:v libx264 -crf 18 -c:a aac \"video_fixed.mp4\"\n"
                "   roi chay lai preflight voi video_fixed.mp4." % a.video))
        elif hit == 0:
            row("FAIL", "thu nhan dien", "0/%d moc co mat (0%%)" % tot)
        else:
            state = "OK" if pct >= 40.0 else "CANH BAO"
            row(state, "thu nhan dien",
                "%d/%d moc co mat (%.0f%%), diem tin cay tb %.2f, nhieu nhat %d mat/frame"
                % (hit, tot, pct, avg_score, max_n))

    print("")

    # ---- ket luan
    if missing:
        print(LINE)
        print("  THIEU %d THU. LAM THEO CAC BUOC SAU ROI CHAY LAI." % len(missing))
        print(LINE)
        print("")
        for i, (title, body) in enumerate(missing, 1):
            print("  %d) %s" % (i, title))
            for ln in body.splitlines():
                print("  " + ln)
            print("")
        print("  Sau khi lam xong, chay lai lenh nay de kiem:")
        print("      python scripts/preflight.py --video \"%s\"%s"
              % (a.video, (" --resources \"%s\"" % a.resources) if a.resources else ""))
        print("")
        sys.exit(1)

    if tot and hit == 0:
        print(LINE)
        print("  VIDEO NAY KHONG CO MAT NAO PHAT HIEN DUOC - DUNG LAI.")
        print(LINE)
        print("")
        print("  Da thu %d moc rai deu ca video, khong moc nao co mat nguoi." % tot)
        print("  DAY KHONG PHAI LOI CUA SKILL: video toan motion-graphic, anh do hoa,")
        print("  quay canh vat, hoac mat qua nho / bi che thi model se ra 0 mat.")
        print("")
        print("  Skill nay chi lam MOT viec: zoom bam VUNG MAT do duoc. Khong co mat")
        print("  thi khong co gi de bam - neu chay tiep thi chi ra mot cu zoom vo nghia")
        print("  vao giua khung. Vi vay khong chay tiep.")
        print("")
        print("  Chon mot trong cac cach sau:")
        print("")
        print("  1) Neu ban CHAC video co mat (mat nho, nguoc sang, doi mu, quay xa):")
        print("     ha nguong tin cay va lay mau day hon:")
        print("         python scripts/preflight.py --video \"%s\" --thr 0.3 --probe-frames 20"
              % a.video)
        print("")
        print("  2) Neu video nay dung la khong co nguoi (motion graphic, screen record):")
        print("     dung skill nay. Muon zoom co dinh vao mot vung tu chon thi")
        print("     dung ffmpeg truc tiep, vi du zoom 1.12 vao giua khung:")
        print("         ffmpeg -i \"<video>\" -vf \"zoompan=z=1.12:d=1:s=%dx%d:fps=%d\" \\"
              % (meta["w"] if meta else 1080, meta["h"] if meta else 1920,
                 int(round(meta["fps"])) if meta else 30))
        print("             %s\"<video-ra>.mp4\""
              % ("-c:a copy " if F.has_audio(a.video) else "-an "))
        print("")
        print("  3) Neu ban dua sai file: goi lai voi dung file quay nguoi noi.")
        print("")
        sys.exit(1)

    if res_note:
        print(res_note)
        print("")

    print("  KET LUAN: DAY DU. Chay tiep duoc.")
    print("")
    print("  Buoc tiep theo:")
    print("      python scripts/track.py --video \"%s\" --out track.json" % a.video)
    print("")
    sys.exit(0)


if __name__ == "__main__":
    main()
