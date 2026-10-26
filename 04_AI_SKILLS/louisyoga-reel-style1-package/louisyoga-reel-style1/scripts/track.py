# -*- coding: utf-8 -*-
"""track.py - bam vi tri MAT theo thoi gian, ghi ra file track JSON.

Lay mau video moi --step giay, nhan dien mat bang det_10g.onnx, ap LUAT CHON
KHI CO NHIEU MAT (xem references/nhieu-mat-va-drift.md), lam min duong di,
roi bao DO DAT DUOC cua tam mat (drift) de ben goi biet co can bam dong hay
mot tam zoom co dinh la du.

    python track.py --video <video> --out track.json [--step 1.0] [--thr 0.5]
                    [--max-jump-frac 0.08] [--smooth 5] [--resources <dir>]
                    [--dry-run]

Hop mat trong file ra la TOA DO GOC cua video (pixel), khong phai toa do da
thu nho.

MOI mau co HAI hop, dung lan nhau la sai:
    box_det  hop DO DUOC that su o mau nay. None = khong bat duoc mat.
             -> dung cai nay cho moi viec can SU THAT (bao safe zone, verify).
    box      hop dung de dieu khien zoom: da va lo hong (noi suy) va da lam min
             bang trung vi truot. Muot hon, nhung o cho lo hong thi la SUY RA.
             -> dung cai nay de chon tam zoom, va phai kiem co "fill": true khong.
"""
import argparse
import os
import sys

try:
    import numpy as np       # thieu numpy thi KHONG crash o day:
except ImportError:          # F.require_numpy() trong main() se in huong dan
    np = None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facelib as F  # noqa: E402


def fill_and_smooth(samples, win, w, h):
    """Va lo hong (noi suy) roi lam min bang TRUNG VI truot.

    Vi sao trung vi chu khong trung binh: mot mau bat sai (bat vao o anh trong
    contact sheet, hoac hop mat phinh ra vi mo) keo trung binh di ca tram pixel,
    con trung vi thi khong.

    LUU Y QUAN TRONG: trung vi LAM CO hop lai - no cat bo dinh cuc tri. Vi vay
    hop sau khi lam min TUYET DOI khong duoc dung de bao safe zone; bao safe zone
    phai dung box_det. Da co bai hoc that ve viec nay (references/safe-zone-do-that.md).
    """
    n = len(samples)
    idx_ok = [i for i in range(n) if samples[i]["box_det"]]
    if not idx_ok:
        return 0
    filled = 0
    for i in range(n):
        if samples[i]["box_det"]:
            samples[i]["box"] = list(samples[i]["box_det"])
            samples[i]["fill"] = False
            continue
        before = [j for j in idx_ok if j < i]
        after = [j for j in idx_ok if j > i]
        if before and after:
            a, b = before[-1], after[0]
            r = (i - a) / float(b - a)
            box = [samples[a]["box_det"][k] +
                   (samples[b]["box_det"][k] - samples[a]["box_det"][k]) * r
                   for k in range(4)]
        elif before:
            box = list(samples[before[-1]]["box_det"])
        else:
            box = list(samples[after[0]]["box_det"])
        samples[i]["box"] = [round(v, 1) for v in box]
        samples[i]["fill"] = True
        filled += 1
    if win and win > 1:
        arr = np.array([s["box"] for s in samples], float)
        out = arr.copy()
        half = int(win) // 2
        for i in range(n):
            lo, hi = max(0, i - half), min(n, i + half + 1)
            out[i] = np.median(arr[lo:hi], axis=0)
        out[:, 0] = np.clip(out[:, 0], 0, w)
        out[:, 2] = np.clip(out[:, 2], 0, w)
        out[:, 1] = np.clip(out[:, 1], 0, h)
        out[:, 3] = np.clip(out[:, 3], 0, h)
        for i in range(n):
            samples[i]["box"] = [round(float(v), 1) for v in out[i]]
    return filled


def drift_report(samples, w, h):
    """Do tren box_det (hop DO DUOC), khong tren hop da lam min."""
    rows = [s for s in samples if s.get("box_det")]
    if not rows:
        return None
    a = np.array([s["box_det"] for s in rows], float)
    cx = (a[:, 0] + a[:, 2]) / 2.0
    cy = (a[:, 1] + a[:, 3]) / 2.0
    fw, fh = a[:, 2] - a[:, 0], a[:, 3] - a[:, 1]
    dx, dy = float(cx.max() - cx.min()), float(cy.max() - cy.min())
    return {
        "do_tren": "box_det (hop do duoc, KHONG lam min)",
        "n_do": len(rows),
        "cx_min": round(float(cx.min()), 1), "cx_max": round(float(cx.max()), 1),
        "cy_min": round(float(cy.min()), 1), "cy_max": round(float(cy.max()), 1),
        "drift_x_px": round(dx, 1), "drift_y_px": round(dy, 1),
        "drift_x_pct": round(100.0 * dx / w, 2),
        "drift_y_pct": round(100.0 * dy / h, 2),
        "face_w_min": round(float(fw.min()), 1), "face_w_max": round(float(fw.max()), 1),
        "face_h_min": round(float(fh.min()), 1), "face_h_max": round(float(fh.max()), 1),
        "center_median": [round(float(np.median(cx)), 1), round(float(np.median(cy)), 1)],
        "union_box": F.box_round(F.box_union([s["box_det"] for s in rows])),
        # Nguong 3%: do that tren talking-head 1080x1920 la 138 px ngang trong
        # 135s (12.8% be ngang) -> KHONG dat, phai bam dong tung doan.
        "static_center_du": bool(dx <= 0.03 * w and dy <= 0.03 * h),
    }


def gap_report(samples, step):
    """Cac khoang thoi gian KHONG do duoc mat (vd doan screen-record).

    Ben goi PHAI biet cac khoang nay: dat punch-in vao day la zoom theo hop mat
    SUY RA, tuc doan lai vao cho khong co mat.
    """
    gaps, cur = [], None
    for s in samples:
        if s["box_det"] is None:
            if cur is None:
                cur = [s["t"], s["t"]]
            else:
                cur[1] = s["t"]
        elif cur is not None:
            gaps.append([round(cur[0], 2), round(cur[1] + step, 2)])
            cur = None
    if cur is not None:
        gaps.append([round(cur[0], 2), round(cur[1] + step, 2)])
    return gaps


def main():
    F.setup_io()
    F.require_numpy()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True, help="file track JSON ket qua")
    ap.add_argument("--resources", default=None)
    ap.add_argument("--step", type=float, default=1.0, help="lay mau moi bao nhieu giay")
    ap.add_argument("--thr", type=float, default=F.DEFAULT_THR, help="nguong diem tin cay")
    ap.add_argument("--max-jump-frac", type=float, default=0.08,
                    help="ban kinh chap nhan, theo ti le canh dai khung (mac dinh 0.08)")
    ap.add_argument("--max-jump", type=float, default=None,
                    help="ban kinh chap nhan tinh bang PIXEL (ghi de --max-jump-frac)")
    ap.add_argument("--confirm-jump", type=int, default=2,
                    help="mot cu nhay xa can bao nhieu mau lien tiep xac nhan thi "
                         "moi duoc nhan (mac dinh 2; nhan HOI TO, khong mat mau)")
    ap.add_argument("--size-ratio", type=float, default=3.0,
                    help="khi nhay xa, mat moi phai co dien tich trong khoang "
                         "1/N .. N lan mat cu (mac dinh 3; chan o anh contact sheet)")
    ap.add_argument("--smooth", type=int, default=5,
                    help="cua so trung vi truot (so mau, so le; 0 = khong lam min)")
    ap.add_argument("--dry-run", action="store_true",
                    help="chi in ke hoach lay mau, KHONG chay nhan dien, khong ghi file")
    a = ap.parse_args()

    if a.step <= 0:
        F.die("--step phai > 0, dang nhan %s" % a.step)

    try:
        meta = F.probe(a.video)
    except Exception as exc:
        F.die("%s\n     Chay preflight de biet ro:\n"
              "     python scripts/preflight.py --video \"%s\"" % (exc, a.video))

    max_jump = (float(a.max_jump) if a.max_jump is not None
                else a.max_jump_frac * max(meta["w"], meta["h"]))
    n_expect = int(meta["dur"] / a.step) + 1

    print("")
    print("  BAM VI TRI MAT")
    print("  video      %s" % os.path.basename(a.video))
    print("  khung      %dx%d  %.2f fps  %.2fs"
          % (meta["w"], meta["h"], meta["fps"], meta["dur"]))
    print("  lay mau    moi %.2fs  -> khoang %d moc" % (a.step, n_expect))
    print("  nguong     diem tin cay >= %.2f" % a.thr)
    print("  ban kinh   %.0f px (tu choi mat nhay xa hon the giua 2 mau)" % max_jump)
    print("  lam min    trung vi truot cua so %d mau" % a.smooth)

    if a.dry_run:
        print("")
        print("  --dry-run: dung tai day. Khong nhan dien, khong ghi file.")
        print("")
        return

    model, source, _tried = F.find_model(a.resources)
    if not model:
        F.die("khong tim thay det_10g.onnx.\n"
              "     Chay lenh nay, no se chi ro cach lay file model:\n"
              "     python scripts/preflight.py --video \"%s\"" % a.video)
    print("  model      %s (%s)" % (os.path.basename(model), source))
    print("")

    det = F.Detector(model, thr=a.thr)
    scale, sw, sh = F.det_scale(meta["w"], meta["h"])

    # LUOT 1: nhan dien, giu TAT CA ung vien cua tung mau
    all_cands, n_multi, max_faces = [], 0, 0
    shown = False
    for i, img in F.stream_samples(a.video, a.step, sw, sh):
        cands = det(img, sw, sh, scale)
        max_faces = max(max_faces, len(cands))
        if len(cands) > 1:
            n_multi += 1
        all_cands.append(cands)
        if (i + 1) % 25 == 0:
            sys.stdout.write("\r  ... da xu ly %d moc" % (i + 1))
            sys.stdout.flush()
            shown = True
    if shown:
        sys.stdout.write("\r" + " " * 46 + "\r")
        sys.stdout.flush()
    if not all_cands:
        F.die("khong doc duoc mau nao tu video. File co the hong hoac fps la.")

    # LUOT 2: ap luat chon chu the tren toan bo chuoi (co nhan hoi to)
    picks = F.select_track(all_cands, max_jump, confirm=a.confirm_jump,
                           size_ratio=a.size_ratio)
    n_reject = sum(1 for _b, _s, why in picks if why.startswith("tu-choi"))
    samples = []
    for i, ((box, score, why), cands) in enumerate(zip(picks, all_cands)):
        samples.append({
            "t": round(i * a.step, 3),
            "box_det": [round(v, 1) for v in box] if box is not None else None,
            "box": None,
            "fill": None,
            "score": round(score, 3),
            "n": len(cands),
            "pick": why,
            "cands": [[F.box_round(b), round(s, 3)] for b, s in cands[:12]],
        })

    n_det = sum(1 for s in samples if s["box_det"])
    if n_det == 0:
        print("  bat duoc mat   0/%d moc (0%%)" % len(samples))
        F.die("khong moc nao co mat -> khong co gi de bam, khong ghi file.\n"
              "     Video nay khong dung duoc voi skill nay. Chay lenh nay de doc\n"
              "     giai thich va cac lua chon thay the:\n"
              "     python scripts/preflight.py --video \"%s\"" % a.video)

    filled = fill_and_smooth(samples, a.smooth, meta["w"], meta["h"])
    dr = drift_report(samples, meta["w"], meta["h"])
    gaps = gap_report(samples, a.step)

    track = {
        "video": os.path.abspath(a.video),
        "w": meta["w"], "h": meta["h"], "fps": meta["fps"],
        "dur": meta["dur"], "nb_frames": meta["nb_frames"],
        "step": a.step, "thr": a.thr, "max_jump_px": round(max_jump, 1),
        "confirm_jump": a.confirm_jump, "size_ratio": a.size_ratio,
        "smooth_win": a.smooth,
        "model": os.path.basename(model),
        "n_samples": len(samples),
        "n_det": n_det,
        "hit_rate": round(100.0 * n_det / len(samples), 1),
        "n_filled": filled,
        "n_multi_face": n_multi,
        "max_faces_1_frame": max_faces,
        "n_reject_jump": n_reject,
        "gaps_no_face": gaps,
        "drift": dr,
        "samples": samples,
    }

    print("  bat duoc mat   %d/%d moc (%.0f%%)%s"
          % (n_det, len(samples), track["hit_rate"],
             ("  |  %d moc khong co mat -> box da noi suy" % filled) if filled else ""))
    if n_multi:
        print("  NHIEU MAT      %d moc thay >1 mat, nhieu nhat %d mat trong 1 frame"
              % (n_multi, max_faces))
        print("                 da ap luat chon: lon nhat VA cach tam truoc <= %.0f px"
              % max_jump)
    if n_reject:
        print("  tu choi        %d mau: nhay xa hon %.0f px va KHONG duoc %d mau"
              % (n_reject, max_jump, a.confirm_jump))
        print("                 ke tiep xac nhan -> coi la bat lac, bo")
    n_conf = sum(1 for s in samples if s["pick"].startswith("nhay-xa-da-xac-nhan"))
    if n_conf:
        print("  cat canh       %d mau nhay xa DA duoc xac nhan va nhan hoi to"
              % n_conf)
    if gaps:
        print("  KHONG CO MAT   %d khoang: %s" % (len(gaps), ", ".join(
            "%.0f-%.0fs" % (g[0], g[1]) for g in gaps[:6])))
        print("                 plan.py se KHONG dat punch-in vao cac khoang nay")
        print("                 (tru khi ban buoc bang --allow-interpolated)")
    if dr:
        u = dr["union_box"]      # [x1, y1, x2, y2] - de sai thu tu la bao sai truc
        print("  hop mat gop    x %d..%d   y %d..%d   (union cac hop DO DUOC)"
              % (u[0], u[2], u[1], u[3]))
        print("  tam mat        x %.0f..%.0f (bien do %.0f px = %.1f%% be ngang)"
              % (dr["cx_min"], dr["cx_max"], dr["drift_x_px"], dr["drift_x_pct"]))
        print("                 y %.0f..%.0f (bien do %.0f px = %.1f%% chieu cao)"
              % (dr["cy_min"], dr["cy_max"], dr["drift_y_px"], dr["drift_y_pct"]))
        print("  co mat         rong %.0f..%.0f   cao %.0f..%.0f px"
              % (dr["face_w_min"], dr["face_w_max"],
                 dr["face_h_min"], dr["face_h_max"]))
        if dr["static_center_du"]:
            print("  KET LUAN       mat gan nhu khong di chuyen (duoi 3% khung).")
            print("                 MOT tam zoom co dinh (%.0f, %.0f) la du cho ca video."
                  % tuple(dr["center_median"]))
        else:
            print("  KET LUAN       tam mat di chuyen hon 3% khung -> phai bam tam theo")
            print("                 tung doan punch-in. plan.py da lam san viec nay.")

    F.write_json(a.out, track)
    print("")
    print("  -> %s" % os.path.abspath(a.out))
    print("")
    print("  Buoc tiep theo:")
    print("      python scripts/plan.py --video \"%s\" \\" % a.video)
    print("          --track \"%s\" --out plan.json --every 20" % a.out)
    print("")


if __name__ == "__main__":
    main()
