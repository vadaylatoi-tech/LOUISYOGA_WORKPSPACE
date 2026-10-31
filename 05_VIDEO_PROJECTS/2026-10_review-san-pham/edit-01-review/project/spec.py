# -*- coding: utf-8 -*-
"""Sinh src/spec.json + cac clip da chinh mau/lam net cho 3 dang review khong loi."""
import json
import os
import subprocess
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "G:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA/"
V = BASE + "03_MEDIA_LIBRARY/raw-footage/Video Review sản phẩm/snaptikvn_7643468615177768212.mp4"
FILM = "D:/LOUGA_WORKSPACE/04_AI_SKILLS/louisyoga-reel-style1-package/louisyoga-reel-style1/assets/broll/louisyoga_brand_film_30fps.mp4"
FPS = 30
LOOK = {
    1: "eq=contrast=1.1:saturation=1.05:gamma=0.97,colorbalance=rs=.06:bs=-.08:rm=.05:gm=.01:bm=-.06:rh=.04:bh=-.06",
    2: "",  # mau goc (anh chot 31/10)
    3: "eq=contrast=0.94:saturation=0.82:brightness=0.03,colorbalance=rs=.03:bs=.03:rm=.03:gm=-.01:bm=.02",
}
# ten: (nguon, giay, lat, crop x0,y0,x1 | "film cx", toc do)
S = {
    "water": (V, 59.0, 0, None, 2.0), "leg": (V, 47.2, 0, None, 0.9), "edge": (V, 68.5, 0, None, 1), "raise": (V, 35.6, 1, None, 1),
    "flat": (V, 41.6, 0, None, 0.65), "touch": (V, 28.6, 1, (0, 120, 440), 0.7), "bag": (V, 7.2, 1, (110, 505, 400), 1), "unwrap": (V, 22.0, 1, (286, 505, 576), 0.75),
    "dog": (V, 44.3, 0, None, 0.7), "spray": (V, 56.4, 0, None, 1), "lunge": (V, 50.0, 0, None, 0.26),
    "fTouch": (FILM, 42.5, 0, 1150, 0.8), "fPattern": (FILM, 46.3, 0, 1000, 0.8), "fPress": (FILM, 60.2, 0, 960, 0.8), "fMed": (FILM, 12.5, 0, 940, 0.8),
}
B1, B2, B3 = 0.6269, 0.5805, 0.8011
V1 = {  # dinh truoc: canh theo so beat
    "beat": B1, "style": "beat", "trans": 0,
    "music": {"file": "R&B/R01 - Stylish LoFi RnB.mp3", "parts": [[0, 40.12, 12.54], [12.54, 70.21, 17.0]], "fade_in": 0.05},
    "shots": [("water", 4, "5 giây", "nước thấm hết"), ("leg", 4, "Bám chắc", "không trượt chân"), ("edge", 2, "4,5 mm", ""), ("raise", 2, "", ""),
              ("flat", 4, "Một đầu vuông", "một đầu tròn"), ("fTouch", 2, "", ""), ("touch", 2, "Chạm thử", ""),
              ("bag", 4, "Tặng kèm túi", "dày dặn, khá to"), ("unwrap", 2, "", ""), ("fPress", 2, "", ""), ("dog", 6, "", ""), ("lunge", 10, "", "")],
    "sfx": [["unwrap", 0.1, "paper-tear-2.wav", 0.5], ["water", 0.1, "water-drip.mp3", 0.3]],
}
V2 = {
    "beat": B2, "style": "breath", "trans": 12, "framed": 1, "intro": 1, "cta": 967,
    "music": {"file": "Emotional/E04 - Wildflowers.mp3", "parts": [[0, 55.66, 36.4]], "fade_in": 0.25},
    "secs": [("dog", 4.94, "Chiếc thảm này", "có gì đáng thử?", {"ink": 1, "tl": 230, "tr": 50, "td": 22}),
             ("bag", 3.0, "Tặng kèm túi", "", {"tear": 1, "ink": 1, "tl": 640, "tr": 30, "ts": 0.66, "ty": 1120}), ("unwrap", 2.8, "", "", {"tear": 1}),
             ("touch", 3.0, "Chạm thử", "nhìn gần bề mặt thảm", {}), ("raise", 2.6, "", "", {}), ("flat", 3.0, "Một đầu vuông", "một đầu tròn", {}),
             ("spray", 2.0, "", "", {"mist": [0.5, 1.06, 1.7]}), ("water", 2.8, "5 giây", "nước thấm hết", {}), ("leg", 3.2, "Bám chắc", "không trượt chân", {"ink": 1, "tl": 230, "tr": 50}),
             ("edge", 2.0, "4,5 mm", "", {}), ("lunge", 7.06, "", "", {})],
    "sfx": [["bag", 0.0, "paper-tear-1.wav", 0.55], ["unwrap", 0.0, "paper-tear-3.wav", 0.55]],
    "spray": [["spray", 0.5], ["spray", 1.06], ["spray", 1.7]],
    "hits": [[0.72, "mixkit/mixkit-air-woosh-1489.wav", 0.32], [32.3, "mixkit/mixkit-air-woosh-1489.wav", 0.18], [33.4, "quick-ting.mp3", 0.22]],
}
V3 = {
    "beat": B3, "style": "type", "trans": 6,
    "music": {"file": "Dreamy/D03 - Take A Break.mp3", "parts": [[0, 4.0, 34.0]], "fade_in": 0.3},
    "secs": [("bag", 2.4, "Bên trong là gì?", ""), ("unwrap", 2.2, "", ""), ("touch", 2.4, "Chạm thử trước đã", ""), ("fPattern", 2.5, "", ""),
             ("raise", 3.2, "", ""), ("flat", 3.2, "Một đầu vuông", "một đầu tròn"), ("leg", 3.2, "Bám chắc", "không trượt chân"), ("spray", 2.4, "", ""),
             ("water", 3.2, "5 giây", "nước thấm hết"), ("edge", 2.4, "4,5 mm", ""), ("lunge", 5.6, "", "")],
    "sfx": [["unwrap", 0.1, "paper-tear-2.wav", 0.4], ["spray", 1.0, "water-drip.mp3", 0.25]],
}
ALL = {1: V1, 2: V2, 3: V3}


def clip(ver, name):
    os.makedirs(f"{HERE}/public/clips", exist_ok=True)
    out = f"{HERE}/public/clips/v{ver}_{name}.mp4"
    if os.path.exists(out):
        return f"clips/v{ver}_{name}.mp4"
    src, ss, fl, cr, sp = S[name]
    vf = []
    if src == FILM:
        vf.append(f"crop=607:1080:{cr - 303}:0")
    else:
        if fl:
            vf.append("hflip")
        if cr:
            x0, y0, x1 = cr
            w = x1 - x0
            vf.append(f"crop={w}:{int(w * 16 / 9) // 2 * 2}:{x0}:{y0}")
        vf.append("hqdn3d=2:2:4:4")
    vf += [f"setpts=PTS/{sp}", f"minterpolate=fps={FPS}:mi_mode=blend" if sp < 0.5 else f"fps={FPS}", "scale=1080:1920:flags=lanczos", ("cas=0.45" if ver == 2 else "cas=0.8") if src == V else "cas=0.4"] + ([LOOK[ver]] if LOOK[ver] else [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(9 * sp), "-i", src, "-an", "-vf", ",".join(vf), "-t", "9",
                    "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-g", "10", "-bf", "0", "-pix_fmt", "yuv420p", out], check=True)
    return f"clips/v{ver}_{name}.mp4"


TF = 2.2  # so frame cho moi ky tu, khop TF trong Review.tsx


def keys(at, text):
    return [round((at + i * TF) / FPS, 3) for i, ch in enumerate(unicodedata.normalize("NFC", text)) if ch != " "]


spec = {}
for ver, c in ALL.items():
    shots, t, ticks = [], 0.0, []
    if c.get("cta"):
        ticks += keys(c["cta"] + 12, "Thảm Aura") + keys(c["cta"] + 44, "louisyoga.vn")
    items = [(n, k * c["beat"], a, b) for n, k, a, b in c["shots"]] if "shots" in c else c["secs"]
    for it in items:
        n, d, a, b = it[:4]
        fx = it[4] if len(it) > 4 else {}
        fr, to = round(t * FPS), round((t + d) * FPS)
        shots.append({"name": n, "clip": clip(ver, n), "from": fr, "dur": to - fr, "a": a, "b": b, **fx})
        if c.get("framed") and a:
            at = fr + round(c["trans"] / 2) + fx.get("td", 4)
            ticks += keys(at, a)
            if b:
                ticks += keys(at + len(a) * TF + 6, b)
        t += d
    spec[str(ver)] = {"style": c["style"], "trans": c["trans"], "beat": c["beat"], "total": round(t * FPS), "shots": shots, "music": c["music"], "sfx": c["sfx"], "spray": c.get("spray", []), "framed": c.get("framed", 0), "intro": c.get("intro", 0), "cta": c.get("cta", 0), "ticks": ticks, "hits": c.get("hits", [])}
json.dump(spec, open(f"{HERE}/src/spec.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v["total"] / FPS for k, v in spec.items()})
