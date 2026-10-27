# -*- coding: utf-8 -*-
"""Do 2 file that roi xuat plan.json: layout + moc 2 pha + chu tren pill."""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def build_plan(left, right, label_left, label_right, out=None):
    L = C.probe(left)
    R = C.probe(right)
    for name, v in (("trai", L), ("phai", R)):
        if v["nframes"] <= 0:
            C.die("Khong dem duoc frame cua video %s: %s" % (name, v["path"]))

    # Do dai LAY THEO SO FRAME, khong lay metadata duration — metadata hay lech
    # vai ms va lam concat sinh frame thua/thieu.
    d1 = L["nframes"] / C.FPS
    d2 = R["nframes"] / C.FPS

    return {
        "version": C.PLAN_VERSION,
        "canvas": {"w": C.W, "h": C.H, "fps": C.FPS},
        "left": {"path": os.path.abspath(left), "nframes": L["nframes"],
                 "dur": d1, "w": L["w"], "h": L["h"], "has_audio": L["has_audio"],
                 "label": label_left, "pill": C.vn_seconds(d1) + " GIÂY"},
        "right": {"path": os.path.abspath(right), "nframes": R["nframes"],
                  "dur": d2, "w": R["w"], "h": R["h"], "has_audio": R["has_audio"],
                  "label": label_right, "pill": C.vn_seconds(d2) + " GIÂY"},
        "phases": [
            {"n": 1, "active": "left", "start": 0.0, "dur": d1, "frames": L["nframes"]},
            {"n": 2, "active": "right", "start": d1, "dur": d2, "frames": R["nframes"]},
        ],
        "total": {"dur": d1 + d2, "frames": L["nframes"] + R["nframes"]},
        "layout": {
            "panel_w": C.PANEL_W, "panel_h": C.PANEL_H, "panel_y": C.PANEL_Y,
            "left_x": C.LEFT_X, "right_x": C.RIGHT_X, "radius": C.RADIUS,
        },
        "saving": {"sec": d1 - d2, "pct": (d1 - d2) / d1 * 100.0 if d1 else 0.0},
    }


def main():
    C.setup_io()
    ap = argparse.ArgumentParser()
    ap.add_argument("--left", "--video", dest="left", required=True)
    ap.add_argument("--right", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--label-left", dest="ll", default="BẢN GỐC")
    ap.add_argument("--label-right", dest="lr", default="AI ĐÃ CẮT")
    ap.add_argument("--dry-run", dest="dry", action="store_true")
    a = ap.parse_args()

    C.head("PLAN")
    p = build_plan(a.left, a.right, a.ll, a.lr)

    print("  Canvas     : %dx%d @%dfps" % (C.W, C.H, C.FPS))
    print("  Pha 1      : 0.000 -> %.3fs  TRAI chay (%s, %d frame)"
          % (p["phases"][0]["dur"], p["left"]["pill"], p["left"]["nframes"]))
    print("  Pha 2      : %.3f -> %.3fs  PHAI chay (%s, %d frame)"
          % (p["phases"][1]["start"], p["total"]["dur"], p["right"]["pill"],
             p["right"]["nframes"]))
    print("  Tong       : %.3fs, %d frame" % (p["total"]["dur"], p["total"]["frames"]))
    print("  Tiet kiem  : %.2fs (%.1f%%)" % (p["saving"]["sec"], p["saving"]["pct"]))
    print("")

    if a.dry:
        print("  --dry-run: khong ghi file nao.")
        return
    C.save_json(a.plan, p)
    print("  Da ghi plan: %s" % a.plan)
    print("")


if __name__ == "__main__":
    main()
