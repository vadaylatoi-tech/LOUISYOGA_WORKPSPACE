# -*- coding: utf-8 -*-
"""nns-cut-silence / remap.py — doi moc thoi gian tu timeline CU sang timeline MOI.

Sau khi cat khoang lang, moi moc gio cua timeline goc deu lech. Script nay
dung file *.timemap.json ma plan.py sinh ra de doi moc cho dung.

Ba kieu dung:

  1) Doi vai moc le:
       python scripts/remap.py --timemap cut.plan.timemap.json --times "3.2,17.8,44.0"

  2) Doi mot file JSON chua danh sach cue (SFX, overlay...). Nhan cac khoa
     time / at / start / end / t0 / t1 o bat ky do sau nao:
       python scripts/remap.py --timemap cut.plan.timemap.json \\
              --json sfx_cue.json --json-out sfx_cue_moi.json

  3) Doi file phu de SRT (cue nao bi xoa het thi bo luon, roi danh so lai):
       python scripts/remap.py --timemap cut.plan.timemap.json \\
              --srt sub.srt --srt-out sub_moi.srt
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

C.setup_io()

TIME_KEYS = ("time", "at", "start", "end", "t0", "t1", "start_sec", "end_sec")


class Mapper(object):
    def __init__(self, tm):
        self.segs = tm["segments"]
        self.dur_out = tm["output_duration"]
        self.dur_in = tm["source_duration"]

    def map(self, t):
        """Tra ve (thoi gian moi, bi_xoa?)."""
        t = float(t)
        if t <= self.segs[0]["old_start"]:
            return self.segs[0]["new_start"], False
        for s in self.segs:
            if s["old_start"] <= t < s["old_end"]:
                return t - s["shift"], False
        # nam trong vung bi xoa hoac vuot cuoi -> gom vao moc gan nhat truoc do
        best = self.segs[-1]["new_end"]
        removed = True
        for s in self.segs:
            if s["old_end"] <= t:
                best = s["new_end"]
        if t >= self.segs[-1]["old_end"]:
            removed = t > self.segs[-1]["old_end"] + 1e-9
        return best, removed


def walk(obj, fn):
    if isinstance(obj, dict):
        return {k: (fn(v) if (k in TIME_KEYS and isinstance(v, (int, float))) else walk(v, fn))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, fn) for v in obj]
    return obj


def srt_time(sec):
    if sec < 0:
        sec = 0.0
    ms = int(round(sec * 1000.0))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def parse_srt_time(txt):
    m = re.match(r"\s*(\d+):(\d+):(\d+)[,.](\d+)\s*", txt)
    if not m:
        return None
    h, mi, s, ms = (int(x) for x in m.groups())
    return h * 3600 + mi * 60 + s + ms / 1000.0


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--timemap", required=True)
    ap.add_argument("--times", default=None)
    ap.add_argument("--json", dest="json_in", default=None)
    ap.add_argument("--json-out", dest="json_out", default=None)
    ap.add_argument("--srt", default=None)
    ap.add_argument("--srt-out", dest="srt_out", default=None)
    a = ap.parse_args()

    if not os.path.isfile(a.timemap):
        C.die("Khong tim thay time map: %s\n       plan.py sinh ra file *.timemap.json." % a.timemap)
    tm = C.read_json(a.timemap)
    if tm.get("skill") != C.SKILL_NAME:
        C.die("File nay khong phai time map cua %s." % C.SKILL_NAME)
    mp = Mapper(tm)

    did = False
    if a.times:
        did = True
        print("")
        print("  cu (goc)      ->  moi (sau cat)")
        for piece in a.times.replace(";", ",").split(","):
            piece = piece.strip()
            if not piece:
                continue
            try:
                t = float(piece)
            except Exception:
                C.die("--times co gia tri khong phai so: %r" % piece)
            nt, removed = mp.map(t)
            print("  %-12s  ->  %-12s%s"
                  % ("%.3f" % t, "%.3f" % nt, "   (nam trong vung DA BI XOA)" if removed else ""))
        print("")

    if a.json_in:
        did = True
        if not a.json_out:
            C.die("--json phai di kem --json-out.")
        obj = C.read_json(a.json_in)
        n = [0]

        def fn(v):
            n[0] += 1
            return mp.map(v)[0]

        C.write_json(a.json_out, walk(obj, fn))
        print("")
        print("  Da doi %d moc thoi gian: %s -> %s" % (n[0], a.json_in, a.json_out))
        print("  (cac khoa duoc doi: %s)" % ", ".join(TIME_KEYS))
        print("")

    if a.srt:
        did = True
        if not a.srt_out:
            C.die("--srt phai di kem --srt-out.")
        with io.open(a.srt, "r", encoding="utf-8-sig") as fh:
            blocks = re.split(r"\r?\n\r?\n", fh.read().strip())
        out = []
        dropped = 0
        for b in blocks:
            lines = [ln for ln in b.splitlines() if ln.strip() != ""]
            if len(lines) < 2:
                continue
            ti = 0 if "-->" in lines[0] else 1
            if ti >= len(lines) or "-->" not in lines[ti]:
                continue
            left, right = lines[ti].split("-->")[0], lines[ti].split("-->")[1]
            t0, t1 = parse_srt_time(left), parse_srt_time(right)
            if t0 is None or t1 is None:
                continue
            n0, _ = mp.map(t0)
            n1, _ = mp.map(t1)
            if n1 - n0 < 0.04:  # ngan hon 1 frame 25fps -> coi nhu bi xoa het
                dropped += 1
                continue
            body = lines[ti + 1:]
            out.append((n0, n1, body))
        with io.open(a.srt_out, "w", encoding="utf-8") as fh:
            for i, (n0, n1, body) in enumerate(out, 1):
                fh.write(u"%d\n%s --> %s\n%s\n\n" % (i, srt_time(n0), srt_time(n1), "\n".join(body)))
        print("")
        print("  Da doi %d cue (%d cue bi xoa het nen bo): %s -> %s"
              % (len(out), dropped, a.srt, a.srt_out))
        print("")

    if not did:
        C.die("Chua chon viec gi. Dung --times, hoac --json/--json-out, hoac --srt/--srt-out.")


if __name__ == "__main__":
    main()
