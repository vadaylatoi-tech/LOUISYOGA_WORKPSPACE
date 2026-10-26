# -*- coding: utf-8 -*-
"""Sinh src/reel/data.ts (caption karaoke + vi tri mat + diem cat) tu clean.words.json + face track.

    python gen_data.py --words work/clean.words.json --face work/face.track.json --out <project>/src/reel/data.ts
                       [--fixes work/fixes.json]

fixes.json (tuy chon):
  {"replace": {"tp": "TPE", "lúm": "lún"},          # sua tu ASR nghe sai (so khop ca tu, bo dau cau)
   "drop": [12, 57],                                 # chi so tu (trong clean.words.json) can bo khoi caption
   "insert": [{"w": "Độ", "start": 8.51, "end": 8.73, "brk_before": true}]}   # tu bi roi o moi cat
Caption: ngat o cuoi cau (dau cau / cuoi segment ho so) va khoang lang > 0.3 s; dong 2-4 tu (toi da 5),
khong bao gio tach tu ghep (COMPOUND: "cơ bản", "định tuyến", "mọi người"...), khong de 1 tu le loi o dau/cuoi dong.
Muon tu ngat tay: them dau "," vao tu trong clean.words.json hoac dung fixes.json "insert" voi brk_before.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

COMPOUND = {tuple(x.split()) for x in (
    "cơ bản", "thường xuyên", "chuyên sâu", "phân khúc", "sản phẩm", "thiết kế", "đầu tư", "cường độ", "hằng ngày", "tập luyện",
    "định tuyến", "đường định", "giáo viên", "hướng dẫn", "trực tiếp", "chỉnh sửa", "căn chỉnh", "động tác", "vị trí", "xác định",
    "thoải mái", "cao su", "su sơ", "sơ dừa", "tự nhiên", "mọi người", "tham khảo", "lựa chọn", "phù hợp", "chất liệu", "đáp ứng",
    "khác nhau", "hoàn toàn", "một chút", "hơn một", "độ bám", "thấm hút", "mồ hôi", "bề mặt", "độ dày", "độ bền", "bong tróc",
    "giỏ hàng", "thương hiệu", "đầy đủ", "tư vấn", "hiện tại", "mức độ", "đường dọc", "dọc thẳng", "chủ yếu", "đôi khi",
    "sử dụng", "mua hàng", "Asana 25", "tần suất", "xen kẽ", "ly rưỡi", "anh chị", "hằng ngày", "mỗi ngày", "ưu tiên", "sức khỏe", "duy trì", "cải thiện", "thể dục", "bắt đầu", "làm quen", "phòng tập",
    "độ êm", "giữ lâu", "nâng cao", "vệ sinh", "bảo quản", "ánh nắng", "mặt trời", "bong tróc", "nhám lì", "sinh thái", "trẻ em", "giá thành", "chất lượng", "luyện tập", "tập trung", "hiệu quả", "an toàn", "ổn định", "chắc chắn", "Louis Yoga", "ví dụ", "như là", "hoặc là", "bởi vì", "nên là", "tại sao", "bao nhiêu", "online ở",
    "ở nhà", "đặt tay", "đặt chân", "quỳ gối", "tì tay", "mới tập", "tập quen", "dòng thảm", "thảm tập", "mẫu thảm")}
WEAK_END = {"là", "các", "cái", "của", "với", "và", "có", "sẽ", "nó", "thì", "những", "một", "mỗi", "rất", "hơi", "đã", "cho",
            "theo", "về", "để", "mà", "nên", "hoặc", "như", "bị", "được", "khi", "nếu", "ở"}
_C2 = {(a.lower(), b.lower()) for a, b in COMPOUND}
NOBREAK = {"ly", "rưỡi", "su", "hơn", "chắn", "nén", "tay", "gối", "cao", "dày", "chọn", "người", "foam", "này", "được", "trạng", "thảm", "định", "quả", "tâm", "mm"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", required=True)
    ap.add_argument("--face", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fixes")
    a = ap.parse_args()
    d = K.read_json(a.words)
    fx = K.read_json(a.fixes) if a.fixes else {}
    rep = fx.get("replace", {})
    drop = set(fx.get("drop", []))
    words = []
    for i, w in enumerate(d["words"]):
        if i in drop:
            continue
        core = re.sub(r"[.,?!…]+$", "", w["w"])
        words.append({"w": rep.get(core, rep.get(core.lower(), core)), "start": w["start"], "end": w["end"], "brk": core != w["w"]})
    for ins in fx.get("insert", []):
        words.append({"w": ins["w"], "start": ins["start"], "end": ins["end"], "brk": False, "brk_before": ins.get("brk_before", False)})
    words.sort(key=lambda w: w["start"])
    for i, w in enumerate(words):
        if w.get("brk_before") and i > 0:
            words[i - 1]["brk"] = True
    def joined(i):  # True if words[i] and words[i+1] must stay on one line
        return i + 1 < len(words) and (words[i]["w"].lower(), words[i + 1]["w"].lower()) in _C2

    # 1) sentences: split at punctuation / long pauses
    sents, cur = [], []
    for j, w in enumerate(words):
        cur.append(w)
        nxt = words[j + 1] if j + 1 < len(words) else None
        if nxt is None or w["brk"] or (nxt["start"] - w["end"]) > 0.3:
            sents.append((cur, j - len(cur) + 1))
            cur = []
    # 2) each sentence -> lines of 2-4 words (max 5), best break = not inside a compound, balanced
    lines = []
    for sent, base in sents:
        i = 0
        while i < len(sent):
            rest = len(sent) - i
            if rest <= 4 or (rest == 5 and not any(joined(base + i + k) for k in (1, 2))):
                lines.append(sent[i:])
                break
            cands = []
            for n in (4, 3, 5, 2):
                if n >= rest - 1:  # never leave a single orphan word
                    continue
                end, nxt_w = sent[i + n - 1]["w"].lower(), sent[i + n]["w"]
                weak = end in WEAK_END and not nxt_w[:1].isdigit()
                score = (10 if joined(base + i + n - 1) else 0) + abs(n - 3.6) + (2 if weak else 0) + (3 if end[:1].isdigit() else 0)
                if sent[i + n]["w"].lower() in NOBREAK:
                    score += 3
                cands.append((score, n))
            n = min(cands)[1] if cands else rest
            lines.append(sent[i: i + n])
            i += n
    cap = [{"start": l[0]["start"], "end": l[-1]["end"], "words": [{"w": x["w"], "s": x["start"], "e": x["end"]} for x in l]} for l in lines]
    for k in range(len(cap) - 1):
        cap[k]["end"] = min(cap[k + 1]["start"], cap[k]["end"] + 0.25)

    tr = K.read_json(a.face)
    sw, sh = d.get("src_size", [tr.get("w", 1080), tr.get("h", 1920)])
    scale = 1080 / sw
    keep = d["keep"]

    def raw2clean(t):
        acc = 0.0
        for s0, e0 in keep:
            if s0 <= t <= e0:
                return acc + t - s0
            acc += e0 - s0
        return None

    face = []
    for s in tr["samples"]:
        c = raw2clean(s["t"])
        if c is None or s.get("fill") or not s.get("box"):
            continue
        b = s["box"]
        face.append([round(c, 2), round((b[0] + b[2]) / 2 * scale), round((b[1] + b[3]) / 2 * scale)])
    ts = "// AUTO-GENERATED by scripts/gen_data.py. Do not edit by hand.\n"
    ts += "export type CapWord={w:string;s:number;e:number};\nexport type CapLine={start:number;end:number;words:CapWord[]};\n"
    ts += "export const CAPTIONS:CapLine[]=" + json.dumps(cap, ensure_ascii=False) + ";\n"
    ts += "// [t, faceCenterX, faceCenterY] in 1080x1920 frame pixels, clean timeline\nexport const FACE:[number,number,number][]=" + json.dumps(face) + ";\n"
    ts += "export const CUTS:number[]=" + json.dumps(d.get("cuts_clean", [])) + ";\n"
    ts += "export const CLEAN_DURATION=" + str(d["duration"]) + ";\n"
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(ts)
    print(f"  {len(cap)} dong caption, {len(face)} moc mat, {len(d.get('cuts_clean', []))} diem cat -> {a.out}")
    print("  " + " | ".join(" ".join(x["w"] for x in c["words"]) for c in cap))


if __name__ == "__main__":
    main()
