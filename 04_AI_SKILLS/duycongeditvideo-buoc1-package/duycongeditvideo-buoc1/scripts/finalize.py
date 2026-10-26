# -*- coding: utf-8 -*-
"""Buoc 5 — nghe lai video da cat (1 lan) de: (a) KIEM mat chu o dau/cuoi/moi noi,
(b) tao HO SO DUNG cho buoc edit sau khoi phai nghe lai.

    python finalize.py --work "D:/.../du_an" --out "D:/.../Video ngan" [--only 06,07] [--terms terms.json]

Sinh canh moi video:
  <ten>.hoso.words.json  transcript word-level cua CHINH video ngan (moc tu 0)
  <ten>.brief.md         hook/than/ket theo giay, loi thoai da sua ten rieng, tu khoa
Va <work>/verify_report.md: so chu nghe duoc o moi ranh gioi voi chu mong doi.
"""
import argparse
import difflib
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dccommon as C  # noqa: E402

ROLE_VI = {"hook": "HOOK", "body": "THÂN", "end": "KẾT"}


def fmt(t):
    return "%02d:%05.2f" % (int(t // 60), t % 60)


def similar(a, b):
    a, b = C.loose(a), C.loose(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(a=a, b=b).ratio()


def window_text(model, video, t0, dur):
    x = C.load_pcm(video, t0, dur)
    segs, _ = model.transcribe(x, language="vi", beam_size=5, vad_filter=False,
                               condition_on_previous_text=False)
    return " ".join(s.text.strip() for s in segs)


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only")
    ap.add_argument("--terms", help="file sua ten rieng (mac dinh <work>/terms.json neu co)")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    a = ap.parse_args()
    C.need_ffmpeg()
    cuts = C.read_json(os.path.join(a.work, "cuts.json"))
    plan_p = os.path.join(a.work, "plan.json")
    plan = {v["id"]: v for v in C.read_json(plan_p)["videos"]} if os.path.isfile(plan_p) else {}
    terms = C.load_terms(a.terms or os.path.join(a.work, "terms.json"))
    only = set(x.strip() for x in a.only.split(",")) if a.only else None
    model, desc = C.load_whisper(a.model, a.device)
    print("  Whisper tren %s" % desc)
    rep_p = os.path.join(a.work, "verify_report.md")
    rep = ["# Kiem tra mat chu (nghe lai video da cat)", "",
           "Moi ranh gioi: `...6 chu cuoi doan truoc || 6 chu dau doan sau`. "
           "CANH BAO = chu nghe duoc o dau/cuoi doan khac han chu mong doi -> co the mat chu, nghe lai.", ""]
    bad_total = 0
    for v in cuts["videos"]:
        if only and v["id"] not in only:
            continue
        f = os.path.join(a.out, v["name"] + ".mp4")
        if not os.path.isfile(f):
            print("  bo qua %s (chua render)" % v["id"])
            continue
        t = time.time()
        S, W = C.words_of(model, f)
        parts, acc = [], 0.0
        for k, s in enumerate(v["segments"]):
            d = s["out"] - s["in"]
            parts.append({"idx": k + 1, "role": s.get("role", "body"), "short_start": round(acc, 3),
                          "short_end": round(acc + d, 3), "src_start": s["in"], "src_end": s["out"],
                          "expect_first": s.get("first_heard", ""), "expect_last": s.get("last_heard", "")})
            acc += d
        for s in S:
            s["text_fixed"] = C.fix_text(s["text"], terms)
        C.write_json(os.path.join(a.out, v["name"] + ".hoso.words.json"), {
            "kind": "nns-hoso", "hoso_version": 1, "video": os.path.abspath(f),
            "video_mtime": os.path.getmtime(f), "model": a.model, "language": "vi",
            "source_video": cuts["source"], "parts": parts,
            "note": "Transcript word-level cua CHINH video ngan (moc tu 0). 'w' la chu Whisper goc; 'text_fixed' da sua ten rieng.",
            "segments": S, "words": W}, indent=0)

        # ---- kiem mat chu: nghe RIENG 4 s dau / cuoi moi doan (nghe ca file hay nuot chu o ranh gioi)
        rep.append("## %s" % v["name"])
        bad = []
        for p in parts:
            ws = [w for w in W if p["short_start"] <= (w["start"] + w["end"]) / 2 < p["short_end"]]
            d = min(4.0, p["short_end"] - p["short_start"])
            head = window_text(model, f, p["short_start"], d)
            tail = window_text(model, f, p["short_end"] - d, d)
            p["_head"], p["_tail"] = head, tail
            got_first = " ".join(head.split()[:3])
            got_last = " ".join(tail.split()[-3:])
            # bo chu dau/cuoi cua chuoi mong doi: no hay dinh chu doan ke ben (gay bao nham)
            ef, el = p["expect_first"].split(), p["expect_last"].split()
            exp_first = " ".join(ef[1:3] if len(ef) > 3 else ef[:2])
            exp_last = " ".join(el[-3:-1] if len(el) > 3 else el[-2:])
            sf = max(similar(" ".join(head.split()[k:k + 2]), exp_first) for k in range(0, 5))
            sl = max(similar(" ".join(tail.split()[-k - 2:len(tail.split()) - k]), exp_last) for k in range(0, 5))
            p["_text"] = C.fix_text(" ".join(w["w"] for w in ws), terms)
            flag = []
            if exp_first and sf < 0.7:
                flag.append("dau: nghe '%s' / mong '%s'" % (got_first, exp_first))
            if exp_last and sl < 0.7:
                flag.append("cuoi: nghe '%s' / mong '%s'" % (got_last, exp_last))
            if flag:
                bad.append(p["idx"])
            rep.append("- doan %d %s→%s %s" % (p["idx"], fmt(p["short_start"]), fmt(p["short_end"]),
                                               ("**CANH BAO** " + "; ".join(flag)) if flag else "OK"))
        rep.append("  - mo dau video: %s…" % parts[0]["_head"][:70])
        for k in range(1, len(parts)):
            rep.append("  - noi @%s: …%s || %s…" % (fmt(parts[k]["short_start"]),
                                                     parts[k - 1]["_tail"][-60:], parts[k]["_head"][:60]))
        rep.append("  - ket video: …%s" % parts[-1]["_tail"][-70:])
        rep.append("")
        bad_total += len(bad)

        # ---- brief
        pv = plan.get(v["id"], {})
        L = ["# %s" % v["title"], "",
             "- File: `%s.mp4` — dài %.1f s, %d từ" % (v["name"], parts[-1]["short_end"], len(W)),
             "- Nội dung: %s" % (v.get("topic") or pv.get("topic", "")),
             "- Transcript word-level: `%s.hoso.words.json` (mốc tính từ 0 của video này). "
             "KHÔNG chạy lại Whisper, KHÔNG xem lại video." % v["name"], "",
             "## Các đoạn (mốc trong video ngắn)", ""]
        for p in parts:
            L += ["### %d. %s — %s → %s  (gốc %.2f–%.2fs)" % (p["idx"], ROLE_VI.get(p["role"], p["role"].upper()),
                                                            fmt(p["short_start"]), fmt(p["short_end"]),
                                                            p["src_start"], p["src_end"]), "",
                  "> " + p.pop("_text"), ""]
        kws = pv.get("keywords", [])
        if kws:
            L += ["## Từ khóa nên nhấn (lần nói đầu tiên)", ""]
            found = []
            for kw in kws:
                n = len(kw.split())
                for i in range(len(W) - n + 1):
                    if C.loose(C.fix_text(" ".join(w["w"] for w in W[i:i + n]), terms)) == C.loose(kw):
                        found.append((W[i]["start"], kw))
                        break
            L += ["- %s — **%s**" % (fmt(t0), kw) for t0, kw in sorted(found)] + [""]
        with open(os.path.join(a.out, v["name"] + ".brief.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(L))
        for p in parts:
            for key in ("_text", "_head", "_tail"):
                p.pop(key, None)
        print("  %s  %d tu, %.0fs  %s" % (v["id"], len(W), time.time() - t,
                                          ("CANH BAO doan " + ",".join(map(str, bad))) if bad else "OK"), flush=True)
    if only and os.path.isfile(rep_p):
        # chay --only: giu bao cao cua cac video khac, chi thay phan vua kiem
        old = open(rep_p, encoding="utf-8").read().split("\n## ")
        keep = [b for b in old[1:] if b.split(" - ")[0].strip() not in only]
        rep = rep[:5] + ["## " + b for b in keep] + rep[5:]
    with open(rep_p, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rep))
    print("  -> %s  (%s)" % (rep_p, "%d doan can xem lai" % bad_total if bad_total else "khong co canh bao"))


if __name__ == "__main__":
    main()
