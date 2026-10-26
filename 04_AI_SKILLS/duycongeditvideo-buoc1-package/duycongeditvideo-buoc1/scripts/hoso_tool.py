# -*- coding: utf-8 -*-
"""Cau noi HO SO -> buoc edit (buoc 2 cua quy trinh), de buoc edit KHONG nghe lai video.

  # Xuat transcript cho du an Remotion (dinh dang [{start,end,text,words:[{w,start,end}]}])
  python hoso_tool.py export --video "06 - ....mp4" --to "public/x/data/transcript_raw.json"

  # Video da cat lang bang nns-cut-silence: doi moc ho so theo timemap
  python hoso_tool.py remap --video "06 - ....mp4" --timemap "06.cut.plan.timemap.json" --to "06.cut.hoso.words.json"

  # Va skill nns-auto-sub (va nns-full-pass dung chung) de no tu dung ho so thay vi Whisper
  python hoso_tool.py patch-nns --skills "D:/.../.claude/skills"
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dccommon as C  # noqa: E402


def hoso_path(video):
    return os.path.splitext(os.path.abspath(video))[0] + ".hoso.words.json"


def load(video):
    p = hoso_path(video)
    if not os.path.isfile(p):
        C.die("khong co ho so: %s" % p)
    h = C.read_json(p)
    if os.path.isfile(video) and os.path.getmtime(video) > h.get("video_mtime", 0) + 1:
        C.die("video da bi sua SAU khi tao ho so -> tao lai ho so (finalize.py --only <id>)")
    return h


def remap_words(words, tm):
    out = []
    for w in words:
        mid = (w["start"] + w["end"]) / 2.0
        for s in tm["segments"]:
            if s["old_start"] <= mid < s["old_end"]:
                st = max(w["start"], s["old_start"]) - s["shift"]
                en = min(w["end"], s["old_end"]) - s["shift"]
                out.append(dict(w, start=round(st, 3), end=round(max(en, st + 0.01), 3)))
                break
    return out


PATCH_FUNCS = r'''
def _add_cuda_dll_dirs():
    """Windows: cuBLAS/cuDNN cai bang pip nam trong site-packages/nvidia/*/bin."""
    if os.name != "nt":
        return
    import site
    for sp in site.getsitepackages():
        for sub in ("cublas", "cudnn", "cuda_nvrtc"):
            d = os.path.join(sp, "nvidia", sub, "bin")
            if os.path.isdir(d):
                os.add_dll_directory(d)
                os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")


def _hoso_path(video):
    return os.path.splitext(os.path.abspath(video))[0] + ".hoso.words.json"


def _load_hoso(path, video):
    if not os.path.isfile(path):
        return None
    try:
        data = C.read_json(path)
    except Exception:
        return None
    if data.get("kind") != "nns-hoso" or not data.get("words"):
        return None
    try:
        if os.path.getmtime(video) > data.get("video_mtime", 0) + 1:
            print("  ho so %s CU HON video -> bo qua" % os.path.basename(path))
            return None
    except OSError:
        return None
    return data


def _remap_words(words, timemap):
    out = []
    for w in words:
        mid = (w["start"] + w["end"]) / 2.0
        for s in timemap["segments"]:
            if s["old_start"] <= mid < s["old_end"]:
                st = max(w["start"], s["old_start"]) - s["shift"]
                en = min(w["end"], s["old_end"]) - s["shift"]
                out.append(dict(w, start=round(st, 3), end=round(max(en, st + 0.01), 3)))
                break
    return out


def from_hoso(video):
    """Dung ho so (Duycongeditvideo_Buoc1) thay vi chay Whisper."""
    h = _load_hoso(_hoso_path(video), video)
    if h:
        return {"segments": h["segments"], "words": h["words"], "hoso": _hoso_path(video)}
    tm_path = os.path.splitext(os.path.abspath(video))[0] + ".plan.timemap.json"
    if not os.path.isfile(tm_path):
        return None
    try:
        tm = C.read_json(tm_path)
    except Exception:
        return None
    src = tm.get("source") or ""
    h = _load_hoso(_hoso_path(src), src) if src else None
    if not h:
        return None
    segs = []
    for s in h["segments"]:
        ws = _remap_words(s.get("words", []), tm)
        if ws:
            segs.append({"start": ws[0]["start"], "end": ws[-1]["end"],
                         "text": " ".join(x["w"] for x in ws), "words": ws})
    return {"segments": segs, "words": _remap_words(h["words"], tm),
            "hoso": _hoso_path(src) + " (qua timemap)"}


'''


def patch_nns(skills_dir):
    p = os.path.join(skills_dir, "nns-auto-sub", "scripts", "transcribe.py")
    if not os.path.isfile(p):
        C.die("khong thay %s (may nay chua co skill nns-auto-sub — khong can va)" % p)
    src = open(p, encoding="utf-8").read()
    if "def from_hoso(" in src:
        print("  da va tu truoc: %s" % p)
        return
    anchor = "def transcribe(video, model_name, language, device, compute_type, vad):"
    call = ("    res = transcribe(a.video, a.model, a.language, a.device, a.compute_type,\n"
            "                     not a.no_vad)\n")
    force = '    ap.add_argument("--force", action="store_true", help="nhan dang lai, bo cache")\n'
    if anchor not in src or call not in src or force not in src:
        C.die("transcribe.py khac phien ban da biet — khong va tu dong duoc. "
              "Doc references/noi-buoc-edit.md de va tay.")
    src = src.replace(anchor, PATCH_FUNCS.lstrip("\n") + anchor, 1)
    src = src.replace(call,
                      "    res = None if a.no_hoso else from_hoso(a.video)\n"
                      "    if res:\n"
                      "        print(\"  dung HO SO co san, KHONG chay Whisper: %s\" % res[\"hoso\"])\n"
                      "    else:\n"
                      "        _add_cuda_dll_dirs()\n"
                      "        res = transcribe(a.video, a.model, a.language, a.device, a.compute_type,\n"
                      "                         not a.no_vad)\n", 1)
    src = src.replace(force, force +
                      '    ap.add_argument("--no-hoso", action="store_true",\n'
                      '                    help="bo qua ho so .hoso.words.json, bat buoc chay Whisper")\n', 1)
    bak = p + ".bak"
    if not os.path.isfile(bak):
        open(bak, "w", encoding="utf-8").write(open(p, encoding="utf-8").read())
    open(p, "w", encoding="utf-8").write(src)
    print("  da va: %s  (ban cu: %s)" % (p, bak))


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("--video", required=True)
    e.add_argument("--to", required=True)
    r = sub.add_parser("remap")
    r.add_argument("--video", required=True)
    r.add_argument("--timemap", required=True)
    r.add_argument("--to", required=True)
    pn = sub.add_parser("patch-nns")
    pn.add_argument("--skills", required=True, help="thu muc .claude/skills co nns-auto-sub")
    a = ap.parse_args()
    if a.cmd == "export":
        h = load(a.video)
        segs = [{"start": s["start"], "end": s["end"], "text": s.get("text_fixed") or s["text"],
                 "words": [{"w": w["w"], "start": w["start"], "end": w["end"]} for w in s["words"]]}
                for s in h["segments"]]
        C.write_json(a.to, segs)
        print("  -> %s (%d cau)" % (a.to, len(segs)))
    elif a.cmd == "remap":
        h = load(a.video)
        tm = C.read_json(a.timemap)
        out = dict(h)
        out["words"] = remap_words(h["words"], tm)
        segs = []
        for s in h["segments"]:
            ws = remap_words(s.get("words", []), tm)
            if ws:
                segs.append(dict(s, start=ws[0]["start"], end=ws[-1]["end"], words=ws))
        out["segments"] = segs
        out["note"] = "Da doi moc theo timemap %s" % os.path.basename(a.timemap)
        out.pop("video_mtime", None)
        C.write_json(a.to, out, indent=0)
        print("  -> %s (%d tu)" % (a.to, len(out["words"])))
    else:
        patch_nns(a.skills)


if __name__ == "__main__":
    main()
