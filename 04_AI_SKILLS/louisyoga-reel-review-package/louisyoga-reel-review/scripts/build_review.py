# -*- coding: utf-8 -*-
"""review.json -> public/footage/<ten>.mp4 + src/spec.json. Clip da co thi giu, --lam-lai de cat lai."""
import argparse
import json
import math
import os
import subprocess
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
FPS = 30
TF = 2.2  # so frame cho moi ky tu, khop TF trong Review.tsx


def clip(project, name, c, source, min_len, lam_lai):
    out = f"{project}/public/footage/{name}.mp4"
    if os.path.exists(out) and not lam_lai:
        return f"footage/{name}.mp4"
    sp = c.get("speed", 1)
    vf = []
    if c.get("flip"):
        vf.append("hflip")
    if c.get("crop"):
        x0, y0, x1 = c["crop"]
        w = x1 - x0
        vf.append(f"crop={w}:{int(w * 16 / 9) // 2 * 2}:{x0}:{y0}")
    vf.append("hqdn3d=2:2:4:4")
    vf += [f"setpts=PTS/{sp}", f"minterpolate=fps={FPS}:mi_mode=blend" if sp < 0.5 else f"fps={FPS}", "scale=1080:1920:flags=lanczos", "cas=0.45"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["ss"]), "-t", str(min_len * sp), "-i", c.get("source", source), "-an", "-vf", ",".join(vf), "-t", str(min_len),
                    "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-g", "10", "-bf", "0", "-pix_fmt", "yuv420p", out], check=True)
    return f"footage/{name}.mp4"


def keys(at, text):
    return [round((at + i * TF) / FPS, 3) for i, ch in enumerate(unicodedata.normalize("NFC", text)) if ch != " "]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--lam-lai", action="store_true", help="cat lai moi clip")
    a = ap.parse_args()
    c = json.load(open(f"{a.project}/review.json", encoding="utf-8"))
    os.makedirs(f"{a.project}/public/footage", exist_ok=True)
    trans = c.get("trans", 12)
    cta = c["cta"]
    p = c["product"]
    ticks = keys(cta + 12, p["title"]) + keys(cta + 44, p["site"])
    shots, spray, t = [], [], 0.0
    for s in c["shots"]:
        n, d = s["clip"], s["dur"]
        fr, to = round(t * FPS), round((t + d) * FPS)
        x = {k: v for k, v in s.items() if k not in ("clip", "dur")}
        x.setdefault("a", "")
        x.setdefault("b", "")
        src = clip(a.project, n, c["clips"][n], c["source"], max(9, math.ceil(d + trans / FPS + 1)), a.lam_lai)
        shots.append({"name": n, "clip": src, "from": fr, "dur": to - fr, **x})
        spray += [[n, m] for m in s.get("mist", [])]
        if x["a"]:
            at = fr + round(trans / 2) + x.get("td", 4)
            ticks += keys(at, x["a"])
            if x["b"]:
                ticks += keys(at + len(x["a"]) * TF + 6, x["b"])
        t += d
    spec = {"trans": trans, "total": round(t * FPS), "cta": cta, "product": p, "shots": shots, "music": c["music"], "sfx": c.get("sfx", []), "spray": spray, "ticks": ticks, "hits": c.get("hits", [])}
    json.dump(spec, open(f"{a.project}/src/spec.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Thoi luong", round(t, 2), "s,", len(shots), "canh, CTA luc", round(cta / FPS, 2), "s")
    if not 0 < cta < spec["total"] - 90:
        print("[CANH BAO] CTA phai bat dau truoc diem ket it nhat 3 s")


if __name__ == "__main__":
    main()
