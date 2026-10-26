"""Generate src/reels-chon-tham/timeline.gen.ts from the word-level transcript.

Run from louis-yoga-remotion/:  python -X utf8 scripts/reels-chon-tham/build_timeline.py

Everything time-based in the composition comes from here, so no second is typed by hand in the
TSX. Times below are RAW source seconds; this script maps them onto the cut timeline.
Plan + reasoning: docs/LOUIS_YOGA_REELS_CHON_THAM_PLAN.md
"""

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "public/reels-chon-tham/data/transcript_raw.json"
OUT = ROOT / "src/reels-chon-tham/timeline.gen.ts"

FPS = 30
SRC_FRAMES = 1466  # ffprobe: 48.866667s @30fps

# Kept ranges of the source, in source frames [start, end). Cut points sit in measured energy
# dips (RMS < -30 dB): 0-0.5s music-only intro, 21.37-21.93s pause, 33.93-34.90s the repeated
# "rất là đủ rồi".
KEEP = [(15, 641), (658, 1018), (1047, SRC_FRAMES)]

# ASR corrections. Whisper large-v3 output, checked against the audio energy profile.
# "lưu dựa KBN" -> "Louis Yoga" and dropping "xây" are best guesses: FLAGGED for the owner to confirm.
def fix_words(words):
    out = []
    i = 0
    while i < len(words):
        w = dict(words[i])
        t = unicodedata.normalize("NFC", w["w"].strip())
        if t == "4" and i + 1 < len(words) and words[i + 1]["w"].strip() == ",5":
            out.append({"w": "4,5", "start": w["start"], "end": words[i + 1]["end"]})
            i += 2
            continue
        if t == "lưu" and [x["w"].strip() for x in words[i : i + 3]] == ["lưu", "dựa", "KBN"]:
            out.append({"w": "Louis", "start": w["start"], "end": words[i + 1]["start"]})
            out.append({"w": "Yoga", "start": words[i + 1]["start"], "end": words[i + 2]["end"]})
            i += 3
            continue
        if t == "xây":
            i += 1
            continue
        if t == "Thầm":
            t = "Thấm"
        # Energy shows "Mã" at 22.00-22.40 and "2" from 22.80; Whisper put them ~0.5s late.
        if t == "Mã" and abs(w["start"] - 22.54) < 0.05:
            w["start"], w["end"] = 22.00, 22.40
        if t == "2" and abs(w["start"] - 22.90) < 0.05:
            w["start"] = 22.80
        w["w"] = t
        out.append(w)
        i += 1
    return out


def src_to_out(t):
    """Raw source seconds -> output frame, or None if t falls in a cut."""
    f = t * FPS
    acc = 0
    for a, b in KEEP:
        if a <= f < b:
            return round(acc + (f - a))
        acc += b - a
    return None


def load_words():
    segs = json.loads(TRANSCRIPT.read_text(encoding="utf-8"))
    words = fix_words([w for s in segs for w in s["words"]])
    kept = []
    for w in words:
        s, e = src_to_out(w["start"]), src_to_out(max(w["start"], w["end"] - 0.01))
        if s is None:
            continue
        kept.append({"text": w["w"], "start": s, "end": e if e is not None else s + 6, "raw": w["start"]})
    return kept


def find(words, phrase, after=0.0):
    """Raw start time of the first occurrence of `phrase` (lower-case, space separated)."""
    toks = unicodedata.normalize("NFC", phrase).lower().split()
    plain = [re.sub(r"[.,?!]$", "", w["text"].lower()) for w in words]
    for i in range(len(words) - len(toks) + 1):
        if words[i]["raw"] >= after and plain[i : i + len(toks)] == toks:
            return words[i]["raw"]
    raise ValueError(f"phrase not found: {phrase}")


# Caption lines split by meaning (editorial), each must match the transcript word-for-word;
# timing still comes only from the transcript. Text is exactly what is spoken.
CHUNKS = [
    "Thảm loại nào hút mồ hôi tốt",
    "thì tất cả các dòng thảm",
    "ví dụ như là đều là cao su,",
    "chất liệu là cao su tự nhiên",
    "thì nó đều sẽ có",
    "cái độ thấm hút mồ hôi nó tốt.",
    "Khi mình tập luyện",
    "hay mình vận động",
    "mà nó ra nhiều mồ hôi chẳng hạn,",
    "hay là mình tập yoga",
    "theo cái trường phái là hot yoga,",
    "thì mình có thể lựa chọn",
    "các dòng thảm nó có độ dày",
    "tốt hơn một chút cho em.",
    "Thì mình có thể tham khảo",
    "qua cái mã này.",
    "Mã 2 này giúp em",
    "là dành cho anh chị em",
    "mà mình tập luyện thường xuyên.",
    "Mấy chị em nào mà mình mới tập",
    "thì tham khảo qua cái mã này cho em.",
    "Thì nó sẽ có độ dày của thảm",
    "nó sẽ là 4,5 ly.",
    "Là rất là vừa đủ rồi.",
    "Thậm chí nó còn dư rồi",
    "mọi người nhé!",
    "Mọi người tập,",
    "ví dụ như trên bề mặt thảm",
    "nó phải có cái độ êm ái này,",
    "thấm hút mồ hôi tốt này,",
    "hay là bám sàn, bám tay",
    "thì các cái dòng thảm đó",
    "của nhà Louis Yoga",
    "đều có thể đáp ứng được",
    "các cái nhu cầu đó cho mọi người.",
]


def build_captions(words):
    norm = lambda x: re.sub(r"[.,?!]$", "", unicodedata.normalize("NFC", x)).lower()  # noqa: E731
    lines, i = [], 0
    for chunk in CHUNKS:
        toks = chunk.split()
        got = words[i : i + len(toks)]
        if [norm(w["text"]) for w in got] != [norm(t) for t in toks]:
            raise ValueError(f"caption chunk does not match transcript: {chunk!r} vs {[w['text'] for w in got]}")
        lines.append([{"text": t, "start": w["start"], "end": w["end"]} for t, w in zip(toks, got)])
        i += len(toks)
    if i != len(words):
        raise ValueError(f"{len(words) - i} transcript words not covered by CHUNKS")
    out = []
    for k, ln in enumerate(lines):
        nxt_start = lines[k + 1][0]["start"] if k + 1 < len(lines) else ln[-1]["end"] + 12
        out.append(
            {
                "from": ln[0]["start"],
                "to": min(ln[-1]["end"] + 8, nxt_start),
                "words": [{"text": w["text"], "start": w["start"]} for w in ln],
            }
        )
    return out


def main():
    words = load_words()
    total_speech = sum(b - a for a, b in KEEP)
    o = lambda t: src_to_out(t)  # noqa: E731

    # Graphic beats on the lower panel, anchored to the words that trigger them.
    beats = [
        # Starts before frame 0 so the hook question is already fully on screen in the first frame.
        {"kind": "title", "from": -14, "label": "TẬP RA NHIỀU MỒ HÔI", "title": "Chọn thảm nào?"},
        {"kind": "material", "from": o(find(words, "chất liệu")), "pop": o(find(words, "thấm hút"))},
        {"kind": "hotyoga", "from": o(11.85), "pop": o(find(words, "hot yoga"))},
        {"kind": "title", "from": o(find(words, "thì mình có thể lựa chọn")), "label": "NÊN CHỌN", "title": "Thảm dày hơn một chút"},
        {"kind": "pointer", "from": o(19.5), "label": "THAM KHẢO", "title": "Mẫu thảm này"},
        {"kind": "audience", "from": o(find(words, "dành cho")), "label": "DÀNH CHO", "title": "Người tập thường xuyên"},
        {"kind": "audience", "from": o(find(words, "mấy chị em")), "pop": o(find(words, "mới tập")), "label": "NẾU BẠN", "title": "Mới tập"},
        {
            "kind": "stat",
            "from": o(find(words, "thì nó sẽ có độ dày")),
            "pop": o(find(words, "4,5 ly")),
            "enough": o(find(words, "vừa đủ")),
            "extra": o(find(words, "còn dư")),
        },
        {
            "kind": "checklist",
            "from": o(find(words, "bề mặt")),
            "items": [
                {"text": "Êm ái", "at": o(find(words, "êm ái"))},
                {"text": "Thấm hút mồ hôi", "at": o(find(words, "thấm hút", after=40))},
                {"text": "Bám sàn, bám tay", "at": o(find(words, "bám sàn"))},
            ],
        },
        {"kind": "brand", "from": o(find(words, "các cái dòng thảm")), "pop": o(find(words, "đáp ứng"))},
    ]
    for i, b in enumerate(beats):
        b["to"] = beats[i + 1]["from"] if i + 1 < len(beats) else total_speech

    # Full-screen illustration cards over the two stretches where the speaker walks out of frame
    # (measured on frames: raw ~8.3-12.0s and ~18.2-19.5s).
    cards = [
        {"kind": "sweat", "from": o(7.95), "to": o(11.85), "pop": o(find(words, "ra nhiều mồ hôi"))},
        {"kind": "thickness", "from": o(17.3), "to": o(19.5)},
    ]

    # Punch-ins on the speaker (scale about the measured face point, source pixels).
    punches = [
        {"from": o(0.5), "to": o(2.4), "x": 340, "y": 700},
        {"from": o(find(words, "4,5 ly")) - 3, "to": o(33.9), "x": 340, "y": 320},
        {"from": o(find(words, "bám sàn")) - 3, "to": o(44.4), "x": 350, "y": 340},
    ]

    sfx = [
        {"file": "mixkit-explainer-light-pop-whoosh-3005.wav", "at": 0, "volume": 0.35},
    ]
    pop = "mixkit-bubble-pop-up-2357.wav"
    for b in beats[1:7]:
        sfx.append({"file": pop, "at": b.get("pop", b["from"]), "volume": 0.3})
    for c in cards:
        sfx.append({"file": "mixkit-air-woosh-1489.wav", "at": max(0, c["from"] - 3), "volume": 0.18})
    sfx.append({"file": "mixkit-long-pop-2358.wav", "at": beats[7]["pop"], "volume": 0.3})
    for it in beats[8]["items"]:
        sfx.append({"file": "mixkit-interface-click-tone-2568.wav", "at": it["at"], "volume": 0.35})
    sfx.append({"file": "mixkit-page-forward-chime-1107.wav", "at": total_speech, "volume": 0.3})

    data = {
        "fps": FPS,
        "keep": [{"srcFrom": a, "srcTo": b} for a, b in KEEP],
        "speechFrames": total_speech,
        "captions": build_captions(words),
        "beats": beats,
        "cards": cards,
        "punches": punches,
        "sfx": sorted(sfx, key=lambda s: s["at"]),
    }
    OUT.write_text(
        "// GENERATED by scripts/reels-chon-tham/build_timeline.py — do not edit by hand.\n"
        "// All values are output frames @30fps (source frames for `keep`).\n"
        f"export const TIMELINE = {json.dumps(data, ensure_ascii=False, indent=1)} as const;\n",
        encoding="utf-8",
    )
    print(f"speech frames {total_speech} ({total_speech / FPS:.2f}s), captions {len(data['captions'])}")
    for c in data["captions"]:
        print(f"{c['from'] / FPS:6.2f}-{c['to'] / FPS:6.2f}  " + " ".join(w["text"] for w in c["words"]))
    for b in beats:
        print("beat", b["kind"], b["from"], b["to"], b.get("title", ""))


if __name__ == "__main__":
    main()
