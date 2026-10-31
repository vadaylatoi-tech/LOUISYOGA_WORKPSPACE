"""Dung video tu edit.json (sua edit.json roi chay lai). Khong ghi gi len C:.

  python build.py sheet  -> anh dau/cuoi moi shot sau crop (work/shots_check.jpg)
  python build.py render [--preview] -> mp4 + edl vao work/
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
MEDIA = Path("G:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA")
WORK = MEDIA / "05_VIDEO_PROJECTS/2026-10_khoang-lang/edit/01-mot-khoang-lang/work"
E = json.loads((HERE / "edit.json").read_text(encoding="utf-8"))
FILM = str(MEDIA / E["film"])
W, H, FPS = E["width"], E["height"], E["fps"]


def ffmpeg(*a):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)


def vf(s, w=W, h=H):
    x, y, cw = s["crop"]
    ch = round(cw * 9 / 16 / 2) * 2
    return f"crop={cw}:{ch}:{x}:{y},scale={w}:{h}:flags=lanczos,setsar=1"


def plate(s):
    return (s["out"] - s["in"]) / s.get("speed", 1)


def sheet():
    # 2 cot moi shot: frame dau / cuoi sau crop, de soi logo in chim, chong hinh, cat tay chan.
    a, f = [], []
    for i, s in enumerate(E["shots"]):
        for j, t in enumerate((s["in"], s["out"] - 0.04)):
            a += ["-ss", t, "-i", FILM]
            f.append(f"[{2*i+j}:v]{vf(s, 480, 270)},trim=end_frame=1[v{2*i+j}]")
    n = 2 * len(E["shots"])
    layout = "|".join(f"{(k%4)*480}_{(k//4)*270}" for k in range(n))
    fc = ";".join(f) + ";" + "".join(f"[v{k}]" for k in range(n)) + f"xstack=inputs={n}:layout={layout}:fill=black"
    ffmpeg(*a, "-filter_complex", fc, "-frames:v", 1, "-q:v", 3, WORK / "shots_check.jpg")


def render(preview):
    shots, card = E["shots"], E["endcard"]
    a, f = [], []
    for i, s in enumerate(shots):
        if "clean" in s:
            a += ["-i", WORK / "plates" / f"{s['clean']['id']}.mkv"]
        else:
            a += ["-ss", s["in"], "-t", s["out"] - s["in"], "-i", FILM]
        chain = f"[{i}:v]{vf(s)},{E['grade']}"
        sp = s.get("speed", 1)
        if sp != 1:
            # Chi 2 shot gan nhu dung yen, toc do khong doi; khong phai speed ramp.
            chain += f",setpts=PTS/{sp},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
        f.append(f"{chain},fps={FPS},format=yuv420p,settb=1/{FPS}[s{i}]")
    # Cut thuong = dissolve 1 frame khong ton; dung concat tung nhom roi xfade o cho co dissolve.
    t = 0.0
    last = None
    groups, cur = [], []
    for i, s in enumerate(shots):
        if s.get("dissolve") and cur:
            groups.append((cur, s["dissolve"]))
            cur = []
        cur.append(i)
    groups.append((cur, None))
    labels = []
    for g, (ids, _) in enumerate(groups):
        f.append("".join(f"[s{i}]" for i in ids) + f"concat=n={len(ids)}:v=1:a=0,settb=1/{FPS}[g{g}]")
        labels.append((f"g{g}", sum(plate(shots[i]) for i in ids)))
    last, t = labels[0]
    for g in range(1, len(labels)):
        d = groups[g - 1][1]
        f.append(f"[{last}][{labels[g][0]}]xfade=transition=fade:duration={d}:offset={t-d:.4f}[x{g}]")
        last, t = f"x{g}", t + labels[g][1] - d
    # Ket: tan vao nen sang cung tong voi can phong, logo nho hien sau.
    n = len(shots)
    d = 1.2
    a += ["-f", "lavfi", "-t", card["duration"], "-i", f"color=c={card['color']}:s={W}x{H}:r={FPS}", "-loop", 1, "-i", str(HERE / "assets/logo.png")]
    f.append(f"[{n+1}:v]format=rgba,scale={card['logo_width']}:-1:flags=lanczos,fade=in:st=0:d={card['logo_fade']}:alpha=1,setpts=PTS+{card['logo_in']}/TB[lg]")
    f.append(f"[{n}:v]format=gbrp[bg];[bg][lg]overlay=(W-w)/2:(H-h)/2:shortest=1:format=gbrp,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,settb=1/{FPS}[card]")
    f.append(f"[{last}][card]xfade=transition=fade:duration={d}:offset={t-d:.4f}[v]")
    total = t - d + card["duration"]
    m = E["music"]
    dur = m["out"] - m["in"]
    a += ["-ss", m["in"], "-t", dur, "-i", str(MEDIA / m["file"])]
    gain = m["gain_db"]
    delay = int(m["at"] * 1000)
    f.append(
        f"[{n+2}:a]afade=t=in:d={m['fade_in']}:curve=hsin,afade=t=out:st={dur-m['fade_out']}:d={m['fade_out']}:curve=hsin,"
        f"{m['comp']},volume={gain}dB,adelay={delay}:all=1,apad,atrim=end={total:.4f},aresample=48000[a]"
    )
    out = WORK / ("preview.mp4" if preview else "master.mp4")
    enc = ["-preset", "veryfast", "-crf", 24] if preview else ["-preset", "slow", "-crf", 15]
    ffmpeg(*a, "-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", *enc, "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", "-t", f"{total:.4f}", out)
    edl(total)
    print(out, f"{total:.2f}s")


def tc(sec):
    fr = round(sec * FPS)
    return f"{fr//108000:02d}:{fr//1800%60:02d}:{fr//30%60:02d}:{fr%30:02d}"


def edl(total):
    # EDL CMX3600 de nap vao Premiere/Resolve: thu tu + mot vao/ra tren phim goc.
    L = [f"TITLE: {E['title']}", "FCM: NON-DROP FRAME", ""]
    t = 0.0
    for i, s in enumerate(E["shots"], 1):
        d = plate(s)
        if s.get("dissolve"):
            t -= s["dissolve"]
        L.append(f"{i:03d}  FILM V C {tc(s['in'])} {tc(s['out'])} {tc(t)} {tc(t+d)}")
        L.append(f"* FROM CLIP NAME: louisyoga_brand_film_30fps.mp4 | {s['name']} | crop {s['crop']} | speed {s.get('speed',1)}")
        t += d
    (WORK / "dung.edl").write_text("\n".join(L) + "\n", encoding="utf-8")


if sys.argv[1] == "sheet":
    sheet()
else:
    render("--preview" in sys.argv)
