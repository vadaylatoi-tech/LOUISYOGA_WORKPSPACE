# -*- coding: utf-8 -*-
"""verify.py - DO LAI ket qua. Khong bao gio chi in "xong".

Kiem 8 dieu, moi dieu la mot phep DO (5 nhom duoi day, nhom 4 va 5 tach ra
thanh nhieu dong trong bang ket qua):
  1. moi cue sau khi cat co peak > 0            (cue im lang = LOI CUNG)
  2. do to that cua file cuoi (do tren AAC, khong phai WAV trung gian -
     AAC co the vuot true-peak so voi WAV)     -> phai trong +-tol LU
  3. true peak <= tran
  4. luong HINH giong het file vao: cung so frame VA cung md5 goi tin
  5. lop SFX co that trong file ra: bu lai gain roi tru file goc, XONG DOI CHIEU
     phan du voi DUNG doan SFX du kien (loc khop). Xem ghi chu duoi day - phep
     do "nang luong con lai co cao hon san" LA PHEP DO YEU, da bat duoc no cho
     DAT mot file khong he co SFX.

exit 1 neu bat ky phep do nao khong dat.

TAI SAO PHAI LOC KHOP (do that, 25/08):
  Ban dau phep do 5 chi so nang luong phan du trong cua so cue voi SAN =
  median phan du ngoai cue. Da thu bang mot file CHI master, KHONG chen SFX:
  verify bao "15/15 cue noi hon san du" -> DAT. Sai, vi phan du duoi loi noi
  (nhieu AAC + resample) da cao hon median toan file san.
  Cach dung: dung chinh bed SFX du kien lam mau, do
      corr = <phan du, mau> / (|phan du| * |mau|)     va
      proj = <phan du, mau> / <mau, mau>              (bien do, dB)
  Do that: file CO SFX -> corr 0.43..1.00, proj 0.0 dB;
           file KHONG SFX -> corr <= 0.05, proj <= -19 dB. Cach nhau rat xa.
  LUU Y ffmpeg tron stereo -> mono theo (L+R)/sqrt(2), khong phai (L+R)/2.

  python scripts/verify.py --video "<goc>" --out "<ket-qua>" --cues sfx_cues.json
"""
from __future__ import print_function

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_stdout()

RESID_MIN_DB = 3.0   # cue phai noi hon san du cua phep tru it nhat bay nhieu dB
# Nguong loc khop, do that tren may nay (co SFX: corr >= 0.43, proj ~ 0.0 dB;
# khong co SFX: corr <= 0.05, proj <= -19 dB) -> de nguong o giua, lech ve
# phia an toan de khong bao sai cho video/thu vien khac.
# Tieu chi CHINH la BIEN DO (proj): no la uoc luong khong lech cua "SFX nay to
# bang bao nhieu phan so voi ke hoach", nen it bi anh huong khi loi noi che mat
# cue. Do that: co SFX -> 0.0 dB deu tap; khong co SFX -> -19 dB tro xuong;
# tron nho hon ke hoach 20 dB -> -20 dB. Cach nhau 13 dB, rat an toan.
# corr chi dung lam kiem tra phu (nguong long), vi corr cua mot cue nho nam
# duoi doan noi to co the tut xuong that du SFX van co that.
# MIN_PROJ_DB de o -10 dB, KHONG phai -3 dB, vi alimiter cua buoc master CO
# QUYEN keo mot cu danh manh xuong that: do tren video 226s can gain +4.2 dB,
# cue punch @0.13s ra -7.1 dB du no co that trong file. Nguong -10 dB van cach
# truong hop "khong co SFX" (-19 dB tro xuong) va "tron nho hon 20 dB" (-20 dB).
MIN_CORR = 0.10       # tuong quan tung cue (kiem phu, de long co y)
MIN_PROJ_DB = -10.0   # bien do tung cue so voi du kien (0 dB = dung y du kien)
# corr CA LOP chi tinh TRONG vung co SFX. Neu tinh ca timeline thi video cang
# dai corr cang tut (nhieu codec cong don ca file, bed thi chi vai giay) - do
# that: cung mot ban tron tot, video 23s ra 0.887 nhung video 226s ra 0.312.
# Nguong ca lop de THAP (0.15) va co y chi de bat truong hop "khong co gi /
# sai hoan toan cue sheet" (do that: 0.000). Con lai la viec cua phep do tung
# cue. Ly do khong de cao: video can gain lon thi alimiter nen manh, corr ca
# lop tut xuong that (do that tren video 226s: 0.471 du ban tron dung).
MIN_CORR_ALL = 0.15


class Checks(object):
    def __init__(self):
        self.rows = []
        self.bad = 0

    def add(self, ok, label, detail, hint=None):
        self.rows.append((bool(ok), label, detail, hint))
        if not ok:
            self.bad += 1

    def report(self):
        w = max([len(r[1]) for r in self.rows] + [10])
        print("")
        for ok, label, detail, _h in self.rows:
            print("  %-8s %-*s  %s" % ("[DAT]" if ok else "[KHONG DAT]", w, label, detail))
        line = "=" * 60
        print("")
        print("  " + line)
        if self.bad == 0:
            print("    TAT CA %d PHEP DO DEU DAT." % len(self.rows))
            print("  " + line)
            print("")
            return 0
        print("    %d/%d PHEP DO KHONG DAT." % (self.bad, len(self.rows)))
        print("  " + line)
        print("")
        for ok, label, detail, hint in self.rows:
            if not ok:
                print("  - %s: %s" % (label, detail))
                if hint:
                    for line2 in hint:
                        print("      " + line2)
                print("")
        return 1


def main():
    ap = argparse.ArgumentParser(description="Do lai ket qua nns-add-sfx")
    C.add_common_args(ap, need_out=True)
    ap.add_argument("--cues", required=True, help="cue sheet JSON da dung khi apply")
    ap.add_argument("--target", type=float, default=None)
    ap.add_argument("--tp", type=float, default=None)
    ap.add_argument("--tol", type=float, default=0.5, help="sai so cho phep, LU")
    ap.add_argument("--skip-residual", action="store_true",
                    help="bo phep do 5 (tru file de tim lop SFX)")
    ap.add_argument("--strict-frames", action="store_true",
                    help="dem frame bang cach GIAI MA het video (cham ~40s/file); "
                         "mac dinh dem goi tin, nhanh hon 400 lan va ra cung so")
    a = ap.parse_args()
    C.require_numpy(a.video)

    import numpy as np

    for p, what in ((a.video, "video goc"), (a.out, "file ket qua"),
                    (a.cues, "cue sheet")):
        if not os.path.isfile(p):
            C.die("khong tim thay %s: %s" % (what, p))

    plan = C.read_json(a.cues)
    cues = plan.get("cues") or []
    if not cues:
        C.die("cue sheet khong co cue nao: %s" % a.cues)
    target = a.target if a.target is not None else float(plan.get("target_lufs", -14.0))
    tp = a.tp if a.tp is not None else float(plan.get("target_tp", -1.5))

    sfx_dir = plan.get("sfx_dir")
    if a.resources:
        d2, _f, _s, _n = C.find_sfx_library(a.resources)
        if d2:
            sfx_dir = d2

    rep = {}
    rep_path = os.path.splitext(a.out)[0] + ".sfxreport.json"
    if os.path.isfile(rep_path):
        try:
            rep = C.read_json(rep_path)
        except Exception:
            rep = {}

    print("")
    print("  nns-add-sfx / VERIFY")
    print("  goc      : %s" % C.disp(a.video))
    print("  ket qua  : %s" % C.disp(a.out))
    print("  cue sheet: %d cue, muc tieu %.1f LUFS +-%.1f LU, TP <= %.1f dBTP"
          % (len(cues), target, a.tol, tp))

    ck = Checks()

    # ---------------------------------------------- 1. moi cue phai co peak > 0
    if not sfx_dir or not os.path.isdir(sfx_dir):
        ck.add(False, "cue peak", "khong tim thay thu muc SFX: %s" % C.disp(sfx_dir),
               ["Goi lai voi --resources \"<thu-muc-chua-sound-effects>\""])
    else:
        cache = {}
        zero = []
        peaks = []
        for i, c in enumerate(cues, 1):
            path = os.path.join(sfx_dir, c["file"].replace("/", os.sep))
            if not os.path.isfile(path):
                zero.append((i, c["file"], c["t"], "khong co file"))
                continue
            if c["file"] not in cache:
                cache[c["file"]] = C.decode_audio(path, channels=2)
            src = cache[c["file"]]
            o = int(round(float(c.get("offset", 0.0)) * C.SR))
            nseg = int(round(float(c.get("dur", 0.0)) * C.SR))
            seg = src[o:o + nseg] if nseg > 0 else src[o:]
            pk = float(np.abs(seg).max()) if len(seg) else 0.0
            g = 10.0 ** (float(c.get("gain_db", 0.0)) / 20.0)
            if pk <= 0.0:
                zero.append((i, c["file"], c["t"], "peak = 0 sau khi cat"))
            else:
                peaks.append((c["t"], c["file"], pk * g))
        if zero:
            ck.add(False, "cue peak",
                   "%d/%d cue co peak = 0 sau khi cat" % (len(zero), len(cues)),
                   ["Cue im lang: " + ", ".join("#%d %s @%.2fs (%s)" % z for z in zero[:8]),
                    "Nguyen nhan gan nhu chac chan: offset dat TRUOC onset cua file.",
                    "Sua bang: python scripts/probe.py --video ... --out sfx_onsets.json",
                    "roi     : python scripts/plan.py  --video ... --onsets sfx_onsets.json"])
        else:
            lo = min(p for _t, _f, p in peaks)
            ck.add(True, "cue peak",
                   "%d/%d cue co peak > 0 (thap nhat %.4f = %.1f dBFS)"
                   % (len(peaks), len(cues), lo, C.db(lo)))

    # ---------------------------------------------- 2 + 3. do to that tren AAC
    vout = C.probe_media(a.out)
    if not vout["has_audio"]:
        ck.add(False, "do to", "file ket qua khong co luong tieng",
               ["apply.py da that bai. Chay lai apply.py va doc thong bao loi."])
    else:
        m = C.measure_loudness(a.out)
        d = abs(m["I"] - target)
        ck.add(d <= a.tol + 1e-9, "do to (I)",
               "I=%.2f LUFS, muc tieu %.2f, lech %.2f LU (cho phep %.2f)"
               % (m["I"], target, m["I"] - target, a.tol),
               ["Chay lai apply.py - vong dieu chinh gain co the da dung som.",
                "Hoac noi rong sai so: --tol 1.0"])
        ck.add(m["TP"] <= tp + 0.05, "true peak",
               "TP=%.2f dBFS, tran %.2f dBTP%s"
               % (m["TP"], tp, "" if m["TP"] <= tp + 0.05 else "  <- VUOT"),
               ["AAC co the vuot true-peak so voi WAV. Ha tran limiter:",
                "    python scripts/apply.py ... --tp %.1f" % (tp - 0.5)])
        lra_in = None
        try:
            lra_in = C.measure_loudness(a.video)["LRA"]
        except SystemExit:
            pass
        if lra_in is not None:
            lost = lra_in - m["LRA"]
            ck.add(lost <= 2.5, "LRA (dai dong)",
                   "%.2f -> %.2f LU (mat %.2f LU)" % (lra_in, m["LRA"], lost),
                   ["Mat qua nhieu LRA = da bi nen dong. Kiem lai apply.py",
                    "co dung loudnorm khong (KHONG DUOC dung), va limit co qua thap khong."])

    # ---------------------------------------------- 4. luong hinh phai y nguyen
    vin = C.probe_media(a.video)
    same_meta = (vin["vcodec"] == vout["vcodec"] and vin["width"] == vout["width"]
                 and vin["height"] == vout["height"]
                 and abs(vin["fps"] - vout["fps"]) < 0.001)
    fin = C.count_frames(a.video, decode=a.strict_frames)
    fout = C.count_frames(a.out, decode=a.strict_frames)
    hin = C.stream_hash(a.video, "v:0")
    hout = C.stream_hash(a.out, "v:0")
    ok_v = same_meta and fin == fout and fin > 0 and hin and hin == hout
    detail = "%s %dx%d %.3ffps, %d frame; md5 %s" % (
        vout["vcodec"], vout["width"], vout["height"], vout["fps"], fout,
        "TRUNG" if (hin and hin == hout) else "KHAC (%s vs %s)"
        % (str(hin)[:8], str(hout)[:8]))
    ck.add(ok_v, "hinh y nguyen", detail,
           ["Luong hinh PHAI duoc copy nguyen: apply.py dung -c:v copy.",
            "Neu khac: co ai ma hoa lai video. Chay lai apply.py.",
            "So frame vao %s, ra %s." % (fin, fout)])

    adur = vout["adur"] or vout["duration"]
    ck.add(abs(adur - vout["duration"]) <= 0.30, "dai tieng == dai hinh",
           "tieng %.3fs, video %.3fs (lech %.3fs)"
           % (adur, vout["duration"], adur - vout["duration"]),
           ["Tieng va hinh lech nhau -> se troi tieng. Chay lai apply.py."])

    # ---------------------------------------------- 5. lop SFX co that khong
    if a.skip_residual:
        print("  (bo qua phep do 5 theo yeu cau --skip-residual)")
    elif not vout["has_audio"]:
        pass
    else:
        gdb = rep.get("gain_db")
        if gdb is None:
            try:
                gdb = C.measure_loudness(a.out)["I"] - C.measure_loudness(a.video)["I"]
            except SystemExit:
                gdb = 0.0
        g = 10.0 ** (float(gdb) / 20.0)
        xin = C.decode_audio(a.video, channels=1).astype(np.float64)
        xout = C.decode_audio(a.out, channels=1).astype(np.float64) / (g if g else 1.0)
        # PHAI chinh lech mau truoc khi tru: ma hoa lai AAC lam tin hieu tre
        # vai tram mau (do that: 239). Khong chinh thi phan du toan la lech pha.
        avoid = []
        for c in cues:
            d = float(c.get("dur", 0.0))
            st = c["t"] - d if c.get("align") == "end" else c["t"]
            avoid.append((st - 0.5, st + d + 0.5))
        lag = C.find_lag(xin, xout, avoid=avoid)
        if lag >= 0:
            xout = xout[lag:]
        else:
            xin = xin[-lag:]
        n = min(len(xin), len(xout))
        xin, xout = xin[:n], xout[:n]
        corr = float(np.corrcoef(xin, xout)[0, 1]) if n > 10 else 0.0
        print("  chinh lech: %+d mau (%.3f ms), tuong quan sau khi chinh %.4f"
              % (lag, lag * 1000.0 / C.SR, corr))
        if corr < 0.90:
            ck.add(False, "khop tin hieu",
                   "tuong quan chi %.3f sau khi chinh lech %+d mau" % (corr, lag),
                   ["File ket qua khong phai ban tron tu chinh video goc nay,",
                    "hoac audio da bi doi toc do / doi cao do.",
                    "Chay lai apply.py voi dung --video goc."])
        else:
            ck.add(True, "khop tin hieu",
                   "tuong quan %.4f sau khi chinh lech %+d mau" % (corr, lag))
        resid = xout - xin
        e = C.env_db(resid, C.HOP_SPEECH)
        ne = len(e)
        mask = np.zeros(ne, dtype=bool)
        for c in cues:
            d = float(c.get("dur", 0.0))
            st = c["t"] - d if c.get("align") == "end" else c["t"]
            i0 = max(0, int(st / C.HOP_SPEECH))
            i1 = min(ne, int((st + d) / C.HOP_SPEECH) + 1)
            if i1 > i0:
                mask[i0:i1] = True
        out_of = e[~mask]
        floor = float(np.median(out_of)) if len(out_of) else -120.0

        # --- dung lai DUNG bed SFX du kien lam mau doi chieu (loc khop) ---
        bed_mono = None
        why_no_bed = None
        missing = []
        if not sfx_dir or not os.path.isdir(sfx_dir):
            why_no_bed = ("khong tim thay thu muc SFX \"%s\" de dung lai doan mau"
                          % C.disp(sfx_dir))
        else:
            for c in cues:
                p = os.path.join(sfx_dir, str(c["file"]).replace("/", os.sep))
                if not os.path.isfile(p):
                    missing.append(str(c["file"]))
            if missing:
                why_no_bed = ("thieu %d file SFX trong %s: %s"
                              % (len(missing), C.disp(sfx_dir),
                                 ", ".join(sorted(set(missing))[:5])))
        if why_no_bed is None:
            try:
                import apply as _apply          # dung dung ham tron cua apply.py
                bed, _rows = _apply.build_bed(cues, sfx_dir, n, verbose=False)
                # ffmpeg tron stereo -> mono theo (L+R)/sqrt(2) (DA DO), khong
                # phai (L+R)/2. Sai cho nay thi bien do lech +3 dB.
                bed_mono = (bed[:, 0].astype(np.float64)
                            + bed[:, 1].astype(np.float64)) / np.sqrt(2.0)
            except SystemExit:
                why_no_bed = "khong dung lai duoc lop SFX du kien (xem loi o tren)"
            except Exception as ex:
                why_no_bed = "khong dung lai duoc lop SFX du kien: %s" % ex

        if bed_mono is None:
            # Khong doi chieu duoc thi KHONG duoc bao DAT. Phep do khong do
            # duoc la phep do that bai, khong phai phep do bo qua.
            ck.add(False, "SFX co trong file ra",
                   "KHONG DO DUOC: %s" % why_no_bed,
                   ["Phep do nay can chinh cac file SFX da dung de doi chieu.",
                    "Goi lai verify voi thu muc thu vien SFX:",
                    "    --resources \"<thu-muc-chua-sound-effects>\"",
                    "Neu ban co y bo phep do nay: them --skip-residual",
                    "(nhung luc do KHONG con bang chung nao la SFX co trong file)."])
        else:
            pad = int(round(0.010 * C.SR))
            # corr ca lop: CHI tinh trong vung bed co tieng, neu khong video dai
            # se tu dong "khong dat" (do that: 0.887 voi 23s, 0.312 voi 226s cho
            # cung mot ban tron dung).
            act = np.abs(bed_mono) > 0.0
            corr_all = 0.0
            if act.any():
                ra, ba = resid[act], bed_mono[act]
                den_all = float(np.linalg.norm(ra) * np.linalg.norm(ba))
                if den_all > 0:
                    corr_all = float(np.dot(ra, ba) / den_all)
            weak = []
            strong = 0
            for c in cues:
                d = float(c.get("dur", 0.0))
                st = c["t"] - d if c.get("align") == "end" else c["t"]
                i0 = max(0, int(round(st * C.SR)) - pad)
                i1 = min(n, int(round((st + d) * C.SR)) + pad)
                s = bed_mono[i0:i1]
                rr = resid[i0:i1]
                den = float(np.dot(s, s))
                if i1 <= i0 or den <= 0.0:
                    weak.append((c["t"], c["file"], 0.0, -120.0))
                    continue
                proj = float(np.dot(rr, s) / den)
                nr = float(np.linalg.norm(rr))
                corr = (float(np.dot(rr, s) / (nr * np.sqrt(den)))
                        if nr > 0 else 0.0)
                proj_db = (20.0 * np.log10(abs(proj))) if proj > 1e-9 else -120.0
                if corr >= MIN_CORR and proj_db >= MIN_PROJ_DB:
                    strong += 1
                else:
                    weak.append((c["t"], c["file"], corr, proj_db))
            ok_all = (not weak) and corr_all >= MIN_CORR_ALL
            detail = ("%d/%d cue khop doan SFX du kien (corr >= %.2f va bien do "
                      ">= %.0f dB); ca lop corr %.3f; san du %.1f dB"
                      % (strong, len(cues), MIN_CORR, MIN_PROJ_DB, corr_all, floor))
            hint = ["Cue KHONG tim thay trong file ra: "
                    + ", ".join("%s @%.2fs (corr %.2f, bien do %.1f dB)"
                                % (f, t, cr, pd) for t, f, cr, pd in weak[:8]),
                    "corr thap = doan tieng do KHONG co trong file ket qua.",
                    "bien do thap = co nhung bi tron nho hon ke hoach nhieu.",
                    "Kiem: file --out co phai ban vua apply.py khong (dung file cu?),",
                    "va cue sheet co dung ban da dung khi apply khong.",
                    "Chay lai: python scripts/apply.py --video ... --cues ... --out ..."]
            if not weak and corr_all < MIN_CORR_ALL:
                hint = ["Ca lop SFX chi tuong quan %.3f voi ke hoach (can >= %.2f)."
                        % (corr_all, MIN_CORR_ALL),
                        "File ket qua co the la ban tron TU MOT CUE SHEET KHAC.",
                        "Chay lai apply.py voi dung cue sheet nay."]
            ck.add(ok_all, "SFX co trong file ra", detail, hint)

    code = ck.report()
    if code == 0:
        print("  Ket qua dung duoc: %s" % C.disp(a.out))
        print("")
    sys.exit(code)


if __name__ == "__main__":
    main()
