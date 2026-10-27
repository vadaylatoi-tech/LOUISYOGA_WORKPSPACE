# -*- coding: utf-8 -*-
"""Nghe lai ban da cat (clean.mp4) va chi ra MEP CAT nao lam MAT chu / SOT tieng — thay cho viec tu so tay.

    python check_cuts.py --work <W>/work [--heard <W>/work/clean_check.words.json]

Doc <W>/work/clean.mp4 + clean.words.json (loi DU KIEN sau cat, kem `keep` / `cuts_clean` do cut_words.py ghi).
Chay transcribe.py (GPU ~30 s) -> clean_check.words.json (hoac dung --heard co san), so tung chu, roi voi moi cho
lech nam gan 1 moi cat (<= 0.7 s) bao: mep goc nao (giay video THO, de sua cuts.json), doi ve huong nao.
Lech xa moi cat = thuong do Whisper nghe khac -> chi liet ke, khong can sua.
Ra: <W>/work/check_cuts.md. Exit 1 neu con loi o moi cat.

Vi sao can: snap_cuts.py keo mep vao cho nang luong thap nhat quanh moc Whisper, nhung moc tu cua Whisper hay lech
(livestream noi lien) -> ~1/5 mep van an vao chu giu hoac sot chu bo (do tren 166 mep cua dot Săn sale 27/10/2026).
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NEAR = 0.7  # s: a mismatch this close to a cut is blamed on the cut


def norm(w: str) -> str:
    return re.sub(r"[^\w]+", "", w.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, help="thu muc work/ co clean.mp4 + clean.words.json")
    ap.add_argument("--heard", help="transcript da co cua clean.mp4 (bo qua buoc chay Whisper)")
    a = ap.parse_args()
    d = K.read_json(os.path.join(a.work, "clean.words.json"))
    heard_path = a.heard or os.path.join(a.work, "clean_check.words.json")
    if not a.heard:
        r = subprocess.run([sys.executable, os.path.join(HERE, "transcribe.py"), "--video", os.path.join(a.work, "clean.mp4"), "--out", heard_path])
        if r.returncode:
            K.die("transcribe.py that bai")
    heard = [w for w in K.read_json(heard_path)["words"] if norm(w["w"])]
    exp = [w for w in d["words"] if norm(w["w"])]
    keep, cuts = d["keep"], d["cuts_clean"]

    def near_cut(t):
        k = min(range(len(cuts)), key=lambda i: abs(cuts[i] - t), default=None)
        return k if k is not None and abs(cuts[k] - t) <= NEAR else None

    sm = difflib.SequenceMatcher(None, [norm(w["w"]) for w in exp], [norm(w["w"]) for w in heard], autojunk=False)
    at_cut, far = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        e_txt = " ".join(w["w"] for w in exp[i1:i2])
        h_txt = " ".join(w["w"] for w in heard[j1:j2])
        t0 = exp[i1]["start"] if i1 < i2 else heard[j1]["start"]
        t1 = exp[i2 - 1]["end"] if i1 < i2 else heard[j2 - 1]["end"]
        k = near_cut(t0) if near_cut(t0) is not None else near_cut(t1)
        if k is None:
            far.append(f"- {t0:6.2f}s du kien \"{e_txt}\" / nghe \"{h_txt}\"")
            continue
        c = cuts[k]
        before = (t0 + t1) / 2 < c  # mismatch sits at the end of keep[k] (cut START edge) or the start of keep[k+1] (cut END edge)
        raw_edge = keep[k][1] if before else keep[k + 1][0]
        edge = "dau doan cat (mep truoc)" if before else "cuoi doan cat (mep sau)"
        if op == "delete" or (op == "replace" and i2 - i1 > j2 - j1):
            fix = "doi VE SAU +0.05..0.15 s" if before else "doi VE TRUOC -0.05..0.15 s"
            what = f"MAT chu \"{e_txt}\"" + (f" (nghe \"{h_txt}\")" if h_txt else "")
            hint = f"; neu chu nay vo tinh chi con tren caption (tieng da bo) thi them chi so cua no vao fixes.json \"drop\""
        elif op == "insert" or (op == "replace" and j2 - j1 > i2 - i1):
            fix = "doi VE TRUOC -0.05..0.15 s" if before else "doi VE SAU +0.05..0.15 s"
            what = f"SOT tieng \"{h_txt}\"" + (f" (du kien \"{e_txt}\")" if e_txt else "")
            hint = "; hoac chu do co that -> them vao fixes.json \"insert\""
        else:
            fix, what, hint = "nghe lai", f"nghe KHAC: du kien \"{e_txt}\" / nghe \"{h_txt}\"", " (thuong la Whisper nghe sai, mep cat co the van dung)"
        at_cut.append(f"- clean {t0:6.2f}s, moi cat #{k + 1} ({c:.2f}s clean) — {what}\n  -> sua cuts.json: {edge} o giay THO {raw_edge:.2f}, {fix}{hint}")

    out = os.path.join(a.work, "check_cuts.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(f"# Kiem moi cat bang tai may ({len(cuts)} moi cat, {len(exp)} chu du kien, {len(heard)} chu nghe duoc)\n\n")
        fh.write(f"## Lech o moi cat ({len(at_cut)}) — can sua\n\n" + ("\n".join(at_cut) or "(khong co)") + "\n\n")
        fh.write(f"## Lech xa moi cat ({len(far)}) — thuong do Whisper, khong can sua\n\n" + ("\n".join(far) or "(khong co)") + "\n")
    print(f"  {len(at_cut)} cho lech o moi cat, {len(far)} cho lech xa moi cat -> {out}")
    for x in at_cut:
        print(x)
    sys.exit(1 if any("MAT" in x or "SOT" in x for x in at_cut) else 0)


if __name__ == "__main__":
    main()
