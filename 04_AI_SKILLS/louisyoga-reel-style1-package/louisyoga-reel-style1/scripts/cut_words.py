# -*- coding: utf-8 -*-
"""Cat cac doan da duyet (tu dem, lap, lang) va dung timeline moi cho moi buoc sau.

    python cut_words.py --video raw.mp4 --words work/src.words.json --cuts work/cuts.json --out-dir work

cuts.json: [[start, end], ...] giay theo FILE GOC (doan BO DI). Doan cuoi co the ghi [65.25, 999] de cat duoi.
Diem cat nen dat vao khoang im lang that (xem analyze_pauses.py). Moi doan giu duoc fade 12 ms
hai dau de khong co tieng 'tach'.

Ra: clean.mov (do phan giai goc, 30fps, PCM), clean.mp4 (h264 -g 10 -bf 0 cho Remotion),
    voice_raw.wav, clean.words.json {keep, words(moc moi), duration, cuts_clean}.

--words nhan ca ho so (<video>.hoso.words.json): cuoi moi segment duoc danh dau ngat cau cho caption.
Hinh: mac dinh khu nhieu nhe + lam net (hqdn3d+cas) vi footage livestream ~1 Mbps bi mo/khoi; --no-sharpen de tat.
Day KHONG phai chinh mau (khong doi mau/sang/tuong phan).
Tu giu lai neu con >= min(0.08 s, 60% do dai) sau khi cat (truoc day xet diem giua -> rot chu o moi cat).
Moc Whisper hay nuot ca khoang lang -> doi khi con 1 tu "ma" (vd "Nên", "Thì") o mep cat: doc caption in ra, bo bang fixes.json "drop".
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402

SHARPEN = "hqdn3d=1.5:1.5:3:3,cas=0.7"  # denoise compression blocks, then contrast-adaptive sharpen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--words", required=True)
    ap.add_argument("--cuts", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--no-sharpen", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    dur = float(K.ffprobe(a.video)["format"]["duration"])
    cuts = sorted(K.read_json(a.cuts))
    keep, t = [], 0.0
    for c0, c1 in cuts:
        if c0 > t:
            keep.append((t, c0))
        t = max(t, c1)
    if t < dur:
        keep.append((t, dur))
    keep = [(round(a0 * 30) / 30, round(min(b0, dur) * 30) / 30) for a0, b0 in keep if b0 - a0 > 0.05]
    fc = []
    for i, (s0, e0) in enumerate(keep):
        d = e0 - s0
        fc.append(f"[0:v]trim=start={s0:.4f}:end={e0:.4f},setpts=PTS-STARTPTS[v{i}]")
        fc.append(f"[0:a]atrim=start={s0:.4f}:end={e0:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.012:.4f}:d=0.012[a{i}]")
    vf = "" if a.no_sharpen else "," + SHARPEN
    fc.append("".join(f"[v{i}][a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=1[vc][a]")
    fc.append(f"[vc]null{vf}[v]")
    mov = os.path.join(a.out_dir, "clean.mov")
    print(f"  giu {len(keep)} doan, cat {len(cuts)} cho ...")
    K.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-r", "30",
           "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", mov], "cat video")
    mp4 = os.path.join(a.out_dir, "clean.mp4")
    info = K.ffprobe(mov)
    v = [s for s in info["streams"] if s["codec_type"] == "video"][0]
    scale = [] if (v["width"], v["height"]) in ((1080, 1920), (1440, 2560), (2160, 3840)) else ["-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"]
    K.run(["ffmpeg", "-v", "error", "-y", "-i", mov, *scale, "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-g", "10", "-bf", "0", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", mp4], "ma hoa clean.mp4")
    K.run(["ffmpeg", "-v", "error", "-y", "-i", mov, "-vn", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le", os.path.join(a.out_dir, "voice_raw.wav")], "tach giong")

    def remap(t0):
        acc = 0.0
        for s0, e0 in keep:
            if t0 < s0:
                return None
            if t0 <= e0:
                return acc + t0 - s0
            acc += e0 - s0
        return None

    src = K.read_json(a.words)
    seg_end = {round(sg["words"][-1]["end"], 3) for sg in src.get("segments", []) if sg.get("words")}

    def kept_part(t0, t1):
        """(start, end) of the longest piece of [t0, t1] that survives, in clean time; None if (almost) all cut."""
        need = min(0.08, 0.6 * (t1 - t0))
        best = None
        for s0, e0 in keep:
            a0, b0 = max(t0, s0), min(t1, e0)
            if b0 - a0 >= need and (best is None or b0 - a0 > best[1] - best[0]):
                best = (a0, b0)
        if best is None:
            return None
        return (remap(best[0]), remap(best[1]))


    words = []
    for w in src["words"]:
        part = kept_part(w["start"], w["end"])
        if part is None:
            continue  # word (almost) entirely inside a cut
        txt = w["w"].strip()
        if round(w["end"], 3) in seg_end and not txt.endswith((".", ",", "?", "!")):
            txt += "."  # sentence end from the hồ sơ -> caption line break
        words.append({"w": txt, "start": round(part[0], 3), "end": round(part[1], 3)})
    acc, cuts_clean = 0.0, []
    for s0, e0 in keep[:-1]:
        acc += e0 - s0
        cuts_clean.append(round(acc, 3))
    for i in range(len(words) - 1):  # the word right before a cut ends a caption line (cuts sit at phrase ends)
        if any(words[i]["start"] < c - 0.03 and words[i]["end"] <= c + 0.03 and words[i + 1]["start"] >= c - 0.03 for c in cuts_clean):
            if not words[i]["w"].endswith((".", ",", "?", "!")):
                words[i]["w"] += ","
    total = sum(e0 - s0 for s0, e0 in keep)
    K.write_json(os.path.join(a.out_dir, "clean.words.json"), {"keep": keep, "words": words, "duration": round(total, 3), "cuts_clean": cuts_clean, "src_size": [v["width"], v["height"]]})
    print(f"  {dur:.1f}s -> {total:.1f}s  ({len(words)} tu)  -> {a.out_dir}")
    print("  KIEM TRA: tu nao bi roi o moi cat (vd 'Độ' bi mat) thi them tay vao clean.words.json truoc buoc gen_data.")


if __name__ == "__main__":
    main()
