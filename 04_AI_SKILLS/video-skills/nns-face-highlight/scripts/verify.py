# -*- coding: utf-8 -*-
"""verify.py - DO LAI ket qua tren file da render. Khong bao gio chi in "xong".

    python verify.py --video <video goc> --out <video ket qua> --plan plan.json

Kiem (exit 1 neu co bat ky dong FAIL):
  1. so frame ra == so frame vao, kich thuoc + fps khong doi, con du am thanh
  2. moi doan punch: nhan dien lai mat TRONG FILE RA tai giua doan giu, roi
     - tam mat phai nam trong dai giua (mac dinh 30% giua khung)
     - hop mat phai nam TRON trong khung (khong bi cat mep nao)
     - vi tri do duoc phai khop voi vi tri plan du kien
  3. vai frame NGOAI moi doan punch: mat phai con dung cho cu nhu trong track
     (bat loi zoom nham ca video)

Frame duoc lay bang select=eq(n\\,N), KHONG dung -ss (hop dong muc 6: -ss co
the nhay sai frame).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facelib as F  # noqa: E402

LINE = "=" * 62


def crop_at(zoom, cx, cy, w, h):
    """Khung crop ma zoompan thuc su dung o muc zoom z voi tam (cx,cy).

    zoompan KEP x/y vao [0, iw - iw/zoom] - chinh cho kep nay la ly do mot
    cai mat nam sat vien tren KHONG THE ve giua khung du zoom bao nhieu.
    """
    cw, ch = w / float(zoom), h / float(zoom)
    x0 = min(max(cx - cw / 2.0, 0.0), w - cw)
    y0 = min(max(cy - ch / 2.0, 0.0), h - ch)
    return x0, y0, cw, ch


def ramp_samples(wd):
    """5 moc do hinh dang cu punch: dau - giua ramp vao - giu - giua ramp ra - cuoi.

    CHON GIUA RAMP LA CO Y: o dung giua ramp thi smoothstep va linear cho
    CUNG mot gia tri 0.5, nen khong can biet apply.py chay --ease nao.
    """
    z = wd["zoom"]
    z_mid = 1.0 + (z - 1.0) * 0.5
    f0, f1, f2, f3 = wd["f_start"], wd["f_hold_start"], wd["f_hold_end"], wd["f_end"]
    return [
        (f0, 1.0, "dau (z=1)"),
        ((f0 + f1) // 2, z_mid, "giua ramp vao"),
        (wd["f_hold_mid"], z, "giu"),
        ((f2 + f3) // 2, z_mid, "giua ramp ra"),
        (f3, 1.0, "cuoi (z=1)"),
    ]


def main():
    F.setup_io()
    F.require_numpy()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, help="video GOC")
    ap.add_argument("--out", required=True, help="video KET QUA da render")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--resources", default=None)
    ap.add_argument("--thr", type=float, default=F.DEFAULT_THR)
    ap.add_argument("--tol-pct", type=float, default=12.0,
                    help="sai lech toi da giua vi tri do duoc va vi tri plan du kien, "
                         "tinh theo phan tram canh khung (mac dinh 12)")
    ap.add_argument("--control", type=int, default=3,
                    help="kiem bao nhieu frame NGOAI cac doan punch (mac dinh 3)")
    ap.add_argument("--no-ramp-check", action="store_true",
                    help="bo qua phan do HINH DANG cu zoom (nhanh hon nhung yeu hon)")
    ap.add_argument("--ramp-tol", type=float, default=0.30,
                    help="be rong mat do duoc duoc lech bao nhieu so voi du kien "
                         "o tung moc ramp (0.30 = 30%%)")
    ap.add_argument("--dry-run", action="store_true",
                    help="chi in se kiem gi, khong chay nhan dien")
    a = ap.parse_args()

    if not os.path.isfile(a.plan):
        F.die("khong thay file plan: %s" % a.plan)
    plan = F.read_json(a.plan)
    wins = plan.get("windows") or []
    if not wins:
        F.die("plan khong co window nao -> khong co gi de kiem.")
    if not os.path.isfile(a.out):
        F.die("khong thay file ket qua: %s\n"
              "     Chay apply.py truoc." % a.out)

    fails, warns = [], []
    print("")
    print("  DO LAI KET QUA")
    print("  " + "-" * 58)

    try:
        m_in = F.probe(a.video)
        m_out = F.probe(a.out)
    except Exception as exc:
        F.die(str(exc))

    band = plan["windows"][0].get("center_band", 0.30)
    W, H = m_out["w"], m_out["h"]

    if a.dry_run:
        print("  se kiem %d doan punch + %d frame doi chung tren %s"
              % (len(wins), a.control, os.path.basename(a.out)))
        print("  --dry-run: dung tai day.")
        print("")
        return

    # ---- 1. khung, fps, so frame, am thanh
    if (m_out["w"], m_out["h"]) == (m_in["w"], m_in["h"]):
        print("  [OK]   kich thuoc         %dx%d, khong doi" % (W, H))
    else:
        print("  [FAIL] kich thuoc         %dx%d -> %dx%d, DA DOI"
              % (m_in["w"], m_in["h"], W, H))
        fails.append("kich thuoc khung bi doi")
    if abs(m_out["fps"] - m_in["fps"]) <= 0.01:
        print("  [OK]   fps                %.3f, khong doi" % m_out["fps"])
    else:
        print("  [FAIL] fps                %.3f -> %.3f (bay concat/filter tut fps)"
              % (m_in["fps"], m_out["fps"]))
        fails.append("fps bi doi")
    if m_out["nb_frames"] == m_in["nb_frames"]:
        print("  [OK]   so frame           %d, dung bang vao" % m_out["nb_frames"])
    else:
        print("  [FAIL] so frame           vao %d, ra %d (lech %d)"
              % (m_in["nb_frames"], m_out["nb_frames"],
                 m_out["nb_frames"] - m_in["nb_frames"]))
        fails.append("so frame khong khop")
    if abs(m_out["dur"] - m_in["dur"]) <= 2.0 / max(m_in["fps"], 1.0):
        print("  [OK]   thoi luong         %.3fs (vao %.3fs)" % (m_out["dur"], m_in["dur"]))
    else:
        print("  [FAIL] thoi luong         vao %.3fs, ra %.3fs" % (m_in["dur"], m_out["dur"]))
        fails.append("thoi luong lech")
    a_in, a_out = F.has_audio(a.video), F.has_audio(a.out)
    if a_in and not a_out:
        print("  [FAIL] am thanh           vao co tieng, ra MAT tieng")
        fails.append("mat luong am thanh")
    else:
        print("  [OK]   am thanh           %s"
              % ("con nguyen" if a_out else "vao khong co tieng, ra cung khong"))

    # ---- 2 + 3. nhan dien lai tren FILE RA
    model, source, _t = F.find_model(a.resources)
    if not model:
        F.die("khong tim thay det_10g.onnx -> khong do lai duoc.\n"
              "     Chay: python scripts/preflight.py --video \"%s\"" % a.video)
    det = F.Detector(model, thr=a.thr)
    scale, sw, sh = F.det_scale(W, H)

    track = None
    tp = plan.get("track")
    if tp and os.path.isfile(tp):
        try:
            track = F.read_json(tp)
        except Exception:
            track = None

    idx_win = [wd["f_hold_mid"] for wd in wins]
    idx_ctrl = []
    if track and a.control > 0:
        busy = set()
        for wd in wins:
            for n in range(wd["f_start"] - 2, wd["f_end"] + 3):
                busy.add(n)
        cands = [s for s in track["samples"]
                 if s.get("box_det")
                 and F.frame_of(s["t"], m_in["fps"], m_in["nb_frames"]) not in busy]
        if cands:
            stepi = max(1, len(cands) // a.control)
            for s in cands[::stepi][:a.control]:
                idx_ctrl.append((F.frame_of(s["t"], m_in["fps"], m_in["nb_frames"]),
                                 s["box_det"]))
    elif a.control > 0:
        warns.append("khong doc duoc track -> bo qua %d frame doi chung" % a.control)

    want = sorted(set(idx_win + [i for i, _b in idx_ctrl]))
    frames = dict()
    for n, img in F.frames_at_indices(a.out, want, sw, sh):
        frames[n] = img
    missing = [n for n in want if n not in frames]
    if missing:
        print("  [FAIL] doc frame          khong lay duoc frame %s tu file ra"
              % missing[:5])
        fails.append("khong doc duoc frame can kiem")

    print("")
    print("  TUNG DOAN PUNCH (do tren FILE RA, tai giua doan giu)")
    print("   #  frame   zoom    tam mat do duoc     lech so voi tam khung   ket luan")
    tol = a.tol_pct / 100.0
    for wd in wins:
        n = wd["f_hold_mid"]
        img = frames.get(n)
        if img is None:
            print("  %2d  %5d   -       khong doc duoc frame" % (wd["i"], n))
            continue
        cands = det(img, sw, sh, scale)
        if not cands:
            print("  %2d  %5d   %.3f   KHONG THAY MAT" % (wd["i"], n, wd["zoom"]))
            fails.append("#%d: khong nhan dien duoc mat trong file ra tai frame %d"
                         % (wd["i"], n))
            continue
        pred = wd.get("tam_mat_ra_du_kien") or [W / 2.0, H / 2.0]
        box, score = min(cands, key=lambda d: F.dist(F.box_center(d[0]), pred))
        cx, cy = F.box_center(box)
        dx, dy = abs(cx - W / 2.0), abs(cy - H / 2.0)
        px, py = 100.0 * dx / W, 100.0 * dy / H
        ok_center = (dx <= (band / 2.0) * W) and (dy <= (band / 2.0) * H)
        ok_inside = F.box_inside(box, W, H)
        ok_pred = (abs(cx - pred[0]) <= tol * W and abs(cy - pred[1]) <= tol * H)
        need_center = wd.get("center_ok", True)
        bad = []
        if not ok_inside:
            bad.append("MAT BI CAT")
        if need_center and not ok_center:
            bad.append("LECH GIUA")
        if not ok_pred:
            bad.append("KHAC PLAN")
        print("  %2d  %5d   %.3f   %4.0f,%4.0f (%.2f)   %4.0f px %4.1f%% x %4.0f px %4.1f%%   %s"
              % (wd["i"], n, wd["zoom"], cx, cy, score, dx, px, dy, py,
                 "OK" if not bad else " + ".join(bad)))
        if not ok_inside:
            fails.append("#%d: hop mat %s bi cat o khung %dx%d"
                         % (wd["i"], F.box_round(box), W, H))
        if need_center and not ok_center:
            fails.append("#%d: tam mat lech %.1f%% x %.1f%% (cho phep %.1f%%)"
                         % (wd["i"], px, py, band / 2.0 * 100))
        if not ok_pred:
            fails.append("#%d: tam do duoc (%.0f,%.0f) khac plan du kien (%.0f,%.0f) "
                         "qua %.0f%% canh khung -> phep tinh crop hoac zoompan sai"
                         % (wd["i"], cx, cy, pred[0], pred[1], a.tol_pct))
        if not need_center:
            warns.append("#%d: plan da danh dau khong keo duoc vao giua "
                         "(--allow-offcenter), chi kiem khong bi cat" % wd["i"])

    # ---- 2-BIS. HINH DANG cu zoom: ramp vao -> giu -> ramp ra
    # Bat loi ma phan tren KHONG bat duoc: zoom khong nha ra ma GIAT ve 1 o
    # frame cuoi window (loi that da tung gap), hoac khong co ramp nao ma
    # nhay thang vao muc zoom.
    if not a.no_ramp_check:
        print("")
        print("  HINH DANG CU ZOOM (do be rong mat tren CA hai file, tung moc)")
        print("   #  moc              frame   zoom du kien   rong mat goc -> ra   "
              "ti le do duoc   ket luan")
        need_src, need_out = set(), set()
        for wd in wins:
            for n, _z, _lb in ramp_samples(wd):
                need_src.add(n)
                need_out.add(n)
        src_img = {}
        for n, img in F.frames_at_indices(a.video, sorted(need_src), sw, sh):
            src_img[n] = img
        out_img = dict(frames)
        need_more = sorted(n for n in need_out if n not in out_img)
        if need_more:
            for n, img in F.frames_at_indices(a.out, need_more, sw, sh):
                out_img[n] = img
        for wd in wins:
            ref_src = F.box_center(wd.get("face_mid") or [0, 0, W, H])
            for n, z_t, label in ramp_samples(wd):
                si, oi = src_img.get(n), out_img.get(n)
                if si is None or oi is None:
                    warns.append("#%d moc '%s' frame %d: khong doc duoc frame"
                                 % (wd["i"], label, n))
                    continue
                cs = det(si, sw, sh, scale)
                if not cs:
                    warns.append("#%d moc '%s' frame %d: file GOC khong thay mat "
                                 "-> bo qua moc nay" % (wd["i"], label, n))
                    continue
                bsrc, _s1 = min(cs, key=lambda d: F.dist(F.box_center(d[0]), ref_src))
                wsrc = bsrc[2] - bsrc[0]
                fcx, fcy = F.box_center(bsrc)
                x0, y0, _cw, _ch = crop_at(z_t, wd["cx"], wd["cy"], W, H)
                pred = ((fcx - x0) * z_t, (fcy - y0) * z_t)
                w_pred = wsrc * z_t
                co = det(oi, sw, sh, scale)
                if not co:
                    print("  %2d  %-16s %5d   %.3f          %4.0f -> KHONG THAY MAT"
                          % (wd["i"], label, n, z_t, wsrc))
                    fails.append("#%d moc '%s' frame %d: khong thay mat trong file ra"
                                 % (wd["i"], label, n))
                    continue
                bout, _s2 = min(co, key=lambda d: F.dist(F.box_center(d[0]), pred))
                wout = bout[2] - bout[0]
                ratio = wout / max(w_pred, 1.0)
                ok_w = abs(ratio - 1.0) <= a.ramp_tol
                ocx, ocy = F.box_center(bout)
                ok_c = (abs(ocx - pred[0]) <= tol * W and abs(ocy - pred[1]) <= tol * H)
                print("  %2d  %-16s %5d   %.3f          %4.0f -> %4.0f (du kien %4.0f)"
                      "   %5.2f   %s"
                      % (wd["i"], label, n, z_t, wsrc, wout, w_pred, ratio,
                         "OK" if (ok_w and ok_c) else
                         ("RONG SAI" if not ok_w else "") +
                         (" TAM SAI" if not ok_c else "")))
                if not ok_w:
                    fails.append(
                        "#%d moc '%s' (frame %d): zoom do duoc lech %.0f%% so voi "
                        "du kien (mat rong %.0f px, du kien %.0f px o zoom %.3f) -> "
                        "hinh dang ramp SAI: hoac khong ramp ma giat, hoac zoom "
                        "khong nha ra"
                        % (wd["i"], label, n, (ratio - 1.0) * 100, wout, w_pred, z_t))
                if not ok_c:
                    fails.append(
                        "#%d moc '%s' (frame %d): tam mat do duoc (%.0f,%.0f) khac "
                        "du kien (%.0f,%.0f) qua %.0f%% canh khung"
                        % (wd["i"], label, n, ocx, ocy, pred[0], pred[1], a.tol_pct))

    if idx_ctrl:
        print("")
        print("  FRAME DOI CHUNG (NGOAI cac doan punch - phai giong track goc)")
        for n, bref in idx_ctrl:
            img = frames.get(n)
            if img is None:
                continue
            cands = det(img, sw, sh, scale)
            if not cands:
                print("    frame %5d  khong thay mat (track goc co) -> bo qua" % n)
                warns.append("frame doi chung %d khong nhan dien duoc mat" % n)
                continue
            ref_c = F.box_center(bref)
            box, _s = min(cands, key=lambda d: F.dist(F.box_center(d[0]), ref_c))
            cx, cy = F.box_center(box)
            d = F.dist((cx, cy), ref_c)
            lim = 0.03 * max(W, H)
            print("    frame %5d  do duoc %4.0f,%4.0f  track %4.0f,%4.0f  lech %4.0f px  %s"
                  % (n, cx, cy, ref_c[0], ref_c[1], d, "OK" if d <= lim else "LECH"))
            if d > lim:
                fails.append("frame %d nam NGOAI moi doan punch nhung mat da doi cho "
                             "%.0f px (cho phep %.0f) -> co the ca video bi zoom nham"
                             % (n, d, lim))

    print("")
    for wtxt in warns:
        print("  [luu y] %s" % wtxt)
    if fails:
        print("")
        print(LINE)
        print("  KHONG DAT - %d loi:" % len(fails))
        print(LINE)
        for i, f in enumerate(fails, 1):
            print("  %d) %s" % (i, f))
        print("")
        print("  Viec can lam:")
        print("   - mat bi cat        -> giam --zoom hoac tang --margin o plan.py")
        print("   - lech giua         -> tang --max-zoom, hoac ha --center-band")
        print("   - hinh dang ramp SAI -> apply.py dang render sai: kiem ham ease()")
        print("                          (ramp RA phai goi voi rev=True, neu khong no")
        print("                          tra ve hang so 1 va cu zoom khong nha ra)")
        print("   - khac plan         -> track/plan lap cho video KHAC file dang render;")
        print("                          chay lai track.py roi plan.py cho dung file")
        print("   - so frame khong khop -> them -r <fps> khi render (apply.py da co),")
        print("                          va dung concat qua demuxer")
        print("")
        sys.exit(1)

    n_off = sum(1 for wd in wins if not wd.get("center_ok", True))
    ramp_txt = ("hinh dang cu zoom dung nhu plan" if not a.no_ramp_check
                else "hinh dang cu zoom CHUA kiem (--no-ramp-check)")
    print("")
    print(LINE)
    if n_off:
        # KHONG duoc bao "tam mat trong dai giua" khi co doan da duoc mien kiem
        # dieu do - noi that con so.
        print("  DAT (co dieu kien). %d doan punch: mat khong bi cat, %s."
              % (len(wins), ramp_txt))
        print("  NHUNG %d/%d doan KHONG dua tam mat vao dai"
              % (n_off, len(wins)))
        print("  giua %.0f%% - do chinh ban dua --allow-offcenter, va do la lua chon"
              % (band * 100))
        print("  co y. Neu ban muon dat tieu chi %.0f%% thi bo --allow-offcenter"
              % (band * 100))
        print("  va bo ca --no-recenter de plan.py tu nang zoom.")
    else:
        print("  DAT. %d doan punch deu: mat khong bi cat, tam mat trong dai giua "
              "%.0f%%, %s."
              % (len(wins), band * 100, ramp_txt))
    print(LINE)
    print("")
    sys.exit(0)


if __name__ == "__main__":
    main()
