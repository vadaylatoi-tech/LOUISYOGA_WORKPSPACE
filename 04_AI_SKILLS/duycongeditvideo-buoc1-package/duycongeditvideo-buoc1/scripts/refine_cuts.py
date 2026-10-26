# -*- coding: utf-8 -*-
"""Buoc 3 — tinh chinh diem cat: tu phuong an (moc uoc luong + cau dau/cau cuoi)
ra moc cat CHINH XAC nam trong khoang lang, khong mat chu dau/cuoi.

    python refine_cuts.py --work "D:/.../du_an"            # doc plan.json, ghi cuts.json + refine_report.md

plan.json (Claude viet o buoc 2):
{
  "videos": [
    {"id": "06", "title": "Dong tham chuyen sau khac gi tham thuong",
     "topic": "1-2 cau tom tat",
     "segments": [
        {"role": "hook", "start": "00:19:58.900", "end": "00:20:06.700",
         "first": "neu nhu ma moi nguoi", "last": "len dong Mastery"},
        ...]}]}

- start/end: moc uoc luong theo video goc (lech 1-3 s van duoc).
- first/last: 2-5 chu DAU va CUOI cua doan, chep tu source.timeline.txt.
- role: hook | body | end (de viet brief); thu tu trong mang = thu tu dung.

Cach tinh: tim chu khop trong source.words.json gan moc uoc luong nhat, roi do
nang luong am thanh 10 ms de dat diem cat vao khoang lang truoc chu dau /
sau chu cuoi. Cho nao noi lien khong co lang -> danh dau TIGHT trong bao cao
de xem lai (thuong nen mo rong sang ranh gioi cau ke ben).
"""
import argparse
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dccommon as C  # noqa: E402

SEARCH = 8.0      # giay quanh moc uoc luong de tim cau khop
PAD_IN = 0.10     # cat truoc chu dau it nhat
PAD_OUT = 0.10    # cat sau khi het tieng
MIN_GAP = 8       # khoang lang phai dai >= 80 ms (chung ngan giua 2 chu khong tinh)


def find_phrase(W, phrase, est, last):
    toks = [C.loose(t) for t in phrase.split() if C.loose(t)]
    if not toks:
        return None, 0
    LW = [C.loose(w["w"]) for w in W]
    best = None
    n = len(toks)
    lo_t, hi_t = est - SEARCH, est + SEARCH
    for i in range(len(W) - n + 1):
        t_ref = W[i + n - 1]["end"] if last else W[i]["start"]
        if not (lo_t <= t_ref <= hi_t):
            continue
        hit = sum(1 for k in range(n) if LW[i + k] == toks[k] or
                  (len(toks[k]) > 2 and (toks[k] in LW[i + k] or LW[i + k] in toks[k])))
        anchor_ok = (LW[i + n - 1] == toks[-1]) if last else (LW[i] == toks[0])
        need = n if n <= 2 else n - 1
        if hit >= need and anchor_ok:
            idx = i + n - 1 if last else i
            score = (n - hit, abs(t_ref - est))
            if best is None or score < best[0]:
                best = (score, idx)
    if best:
        return best[1], best[0][0]
    return None, 0


def nearest_word(W, est, last):
    key = (lambda w: abs(w["end"] - est)) if last else (lambda w: abs(w["start"] - est))
    return min(range(len(W)), key=lambda i: key(W[i]))


class Env(object):
    def __init__(self, video, t):
        self.t0 = max(0.0, t - 4.0)
        x = C.load_pcm(video, self.t0, 8.0)
        db = C.envelope_db(x)
        self.db = np.convolve(db, np.ones(3) / 3, mode="same") if len(db) > 3 else db
        self.floor = float(np.percentile(db, 5)) if len(db) else -60
        self.q = self.floor + 9.0

    def idx(self, t):
        return int(round((t - self.t0) * 100))

    def time(self, k):
        return self.t0 + k / 100.0

    def frames(self, lo, hi):
        return [k for k in range(self.idx(lo), self.idx(hi)) if 0 <= k < len(self.db)]

    def quiet(self, k):
        return self.db[k] < self.q

    def runs(self, frames, min_len=5):
        """Cac khoang lang [k0,k1] dai >= min_len*10ms nam trong (hoac cham) frames."""
        out, k = [], 0
        n = len(self.db)
        lo, hi = (frames[0], frames[-1]) if frames else (0, -1)
        k = lo
        while k <= hi:
            if self.quiet(k):
                k0 = k
                while k0 - 1 >= 0 and self.quiet(k0 - 1):
                    k0 -= 1
                k1 = k
                while k1 + 1 < n and self.quiet(k1 + 1):
                    k1 += 1
                if k1 - k0 + 1 >= min_len:
                    out.append((k0, k1))
                k = k1 + 1
            else:
                k += 1
        return out


def cut_in(video, W, i):
    ws = W[i]["start"]
    pe = W[i - 1]["end"] if i > 0 else ws - 1.0
    env = Env(video, ws)
    fr = env.frames(max(pe - 0.30, ws - 0.8), ws + 0.15)
    rs = [r for r in env.runs(fr, MIN_GAP) if r[0] <= fr[-1]] if fr else []
    if rs:
        k0, k1 = rs[-1]                              # khoang lang gan chu dau nhat
        k1 = min(k1, fr[-1])
        # cat trong khoang lang, va luon truoc chu dau it nhat PAD_IN (chu noi nho van giu)
        t = min(env.time(k1) - 0.03, ws - PAD_IN)
        t = max(t, env.time(k0))
        return round(t, 3), ""
    fr = env.frames(max(pe - 0.05, ws - 0.25), ws + 0.05) or env.frames(ws - 0.25, ws + 0.05)
    k = min(fr, key=lambda k: env.db[k])
    return round(env.time(k), 3), "TIGHT"


def cut_out(video, W, j):
    we = W[j]["end"]
    ns = W[j + 1]["start"] if j + 1 < len(W) else we + 1.5
    env = Env(video, we)
    # Khong tin moc chu ke tiep (Whisper hay dat som): tim khoang lang THAT sau chu cuoi.
    fr = env.frames(we - 0.10, we + 0.8)
    # khoang lang phai BAT DAU sau khi chu cuoi ket thuc (khoang chung ngan truoc chu cuoi khong tinh)
    rs = [r for r in env.runs(fr, MIN_GAP) if r[0] >= env.idx(we - 0.03)] if fr else []
    if rs:
        k0, k1 = rs[0]                               # khoang lang dau tien sau chu cuoi
        k0 = max(k0, fr[0])
        t = max(env.time(k0) + PAD_OUT, we + 0.08)
        t = min(t, env.time(k1) - 0.02)
        return round(max(t, env.time(k0)), 3), ""
    fr = env.frames(we - 0.05, min(ns, we + 0.3)) or env.frames(we - 0.05, we + 0.3)
    k = min(fr, key=lambda k: env.db[k])
    return round(env.time(k), 3), "TIGHT"


def ctx(W, i, before=4, after=4):
    return " ".join("%s[%.2f]" % (w["w"], w["start"]) for w in W[max(0, i - before):i + after + 1])


def safe_name(s):
    return re.sub(r'[\\/:*?"<>|]+', "-", s).strip()


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--plan", help="mac dinh <work>/plan.json")
    ap.add_argument("--only", help="chi lam cac id nay, vd 01,02")
    a = ap.parse_args()
    C.need_ffmpeg()
    plan_p = a.plan or os.path.join(a.work, "plan.json")
    src_p = os.path.join(a.work, "source.words.json")
    if not os.path.isfile(src_p):
        C.die("chua co %s — chay transcribe_source.py truoc" % src_p)
    plan = C.read_json(plan_p)
    src = C.read_json(src_p)
    video = plan.get("source") or src["video"]
    W = src["words"]
    only = set(x.strip() for x in a.only.split(",")) if a.only else None
    cuts_p = os.path.join(a.work, "cuts.json")
    old = C.read_json(cuts_p) if os.path.isfile(cuts_p) else {"videos": []}
    keep = {v["id"]: v for v in old.get("videos", [])}
    rep = ["# Bao cao tinh chinh diem cat", "",
           "TIGHT = noi lien khong co khoang lang -> nen nghe lai / mo rong sang ranh gioi cau.",
           "NOMATCH = khong tim thay cau dau/cuoi trong transcript -> dung moc uoc luong, PHAI xem lai.", ""]
    for v in plan["videos"]:
        if only and v["id"] not in only:
            continue
        segs = []
        rep.append("## %s - %s" % (v["id"], v["title"]))
        for n, s in enumerate(v["segments"], 1):
            flags = []
            i, miss_i = find_phrase(W, s.get("first", ""), C.ts2s(s["start"]), last=False)
            if i is None:
                i = nearest_word(W, C.ts2s(s["start"]), last=False)
                flags.append("NOMATCH-dau")
            j, miss_j = find_phrase(W, s.get("last", ""), C.ts2s(s["end"]), last=True)
            if j is None or j < i:
                j = nearest_word(W, C.ts2s(s["end"]), last=True)
                flags.append("NOMATCH-cuoi")
            tin, f1 = cut_in(video, W, i)
            tout, f2 = cut_out(video, W, j)
            if f1:
                flags.append("TIGHT-dau")
            if f2:
                flags.append("TIGHT-cuoi")
            heard = " ".join(w["w"] for w in W[i:j + 1])
            segs.append({"role": s.get("role", "body"), "in": tin, "out": tout,
                         "in_ts": C.s2ts(tin), "out_ts": C.s2ts(tout),
                         "first_heard": " ".join(w["w"] for w in W[i:i + 6]),
                         "last_heard": " ".join(w["w"] for w in W[max(i, j - 5):j + 1]),
                         "flags": flags})
            rep.append("- doan %d (%s) %s -> %s = %.2fs %s" % (n, s.get("role", "body"), C.s2ts(tin), C.s2ts(tout),
                                                         tout - tin, ("**" + ", ".join(flags) + "**") if flags else "OK"))
            rep.append("  - dau: %s" % ctx(W, i))
            rep.append("  - cuoi: %s" % ctx(W, j))
            if len(heard.split()) < 3:
                rep.append("  - **CANH BAO: doan qua ngan, kiem lai first/last**")
        dur = sum(x["out"] - x["in"] for x in segs)
        keep[v["id"]] = {"id": v["id"], "title": v["title"], "topic": v.get("topic", ""),
                         "name": safe_name("%s - %s" % (v["id"], v["title"])),
                         "duration": round(dur, 2), "segments": segs}
        rep.append("- **Tong: %.1f s**" % dur)
        rep.append("")
        print("  %s  %5.1fs  %d doan  %s" % (v["id"], dur, len(segs),
              " ".join(sorted(set(f for x in segs for f in x["flags"]))) or "OK"))
    vids = sorted(keep.values(), key=lambda x: x["id"])
    C.write_json(cuts_p, {"source": video, "videos": vids})
    with open(os.path.join(a.work, "refine_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(rep))
    print("  -> %s\n  -> %s" % (cuts_p, os.path.join(a.work, "refine_report.md")))


if __name__ == "__main__":
    main()
