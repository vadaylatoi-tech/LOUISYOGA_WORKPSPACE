# -*- coding: utf-8 -*-
"""Buoc 1 — nhan dang VIDEO DAI mot lan duy nhat (word-level).

    python transcribe_source.py --video "D:/.../video_dai.mp4" --work "D:/.../du_an"

Sinh ra trong --work:
  source.words.json   transcript word-level cua video goc (moi buoc sau dung lai, KHONG nghe lai)
  source.timeline.txt phu de co moc [HH:MM:SS.mmm --> ...] de doc va lap phuong an

Co cache: chay lai thi bo qua neu video khong doi. --force de lam lai.
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dccommon as C  # noqa: E402


def main():
    C.setup_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--work", required=True, help="thu muc du an (luu transcript, phuong an, cuts)")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--language", default="vi")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    C.need_ffmpeg()
    if not os.path.isfile(a.video):
        C.die("khong thay video: %s" % a.video)
    os.makedirs(a.work, exist_ok=True)
    out_json = os.path.join(a.work, "source.words.json")
    out_txt = os.path.join(a.work, "source.timeline.txt")
    mtime = os.path.getmtime(a.video)

    if os.path.isfile(out_json) and not a.force:
        old = C.read_json(out_json)
        if os.path.abspath(old.get("video", "")) == os.path.abspath(a.video) and \
                abs(old.get("video_mtime", 0) - mtime) < 1 and old.get("model") == a.model:
            print("  da co %s — dung lai, khong nhan dang lai (--force de lam lai)" % out_json)
            return

    info = C.probe(a.video)
    print("  video: %s  (%.1f phut, %sx%s)" % (a.video, info["duration"] / 60, info["width"], info["height"]))
    model, desc = C.load_whisper(a.model, a.device)
    print("  nhan dang bang %s tren %s ... (GPU ~1/3 thoi luong, CPU ~1-1.5x thoi luong)" % (a.model, desc))
    t0 = time.time()
    # VAD co dem rong de bo doan im lang dai (cuoi livestream) ma khong mat tu nho
    segs, _ = model.transcribe(a.video, language=a.language, word_timestamps=True, beam_size=5,
                               vad_filter=True,
                               vad_parameters={"min_silence_duration_ms": 1500, "speech_pad_ms": 500},
                               condition_on_previous_text=False)
    S, W = [], []
    last_print = 0
    for s in segs:
        ws = [{"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3),
               "p": round(float(w.probability), 3)} for w in (s.words or []) if w.word.strip()]
        W += ws
        S.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(), "words": ws})
        if s.end - last_print > 300:
            last_print = s.end
            print("    ... da toi %s" % C.s2ts(s.end), flush=True)
    if not W:
        C.die("khong nhan ra loi noi nao")
    C.write_json(out_json, {"kind": "dc-source-words", "video": os.path.abspath(a.video),
                            "video_mtime": mtime, "duration": info["duration"],
                            "model": a.model, "language": a.language,
                            "segments": S, "words": W}, indent=0)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("PHU DE CO TIMELINE — %s\n" % os.path.basename(a.video))
        f.write("Thoi luong video: %s. Loi noi ket thuc khoang %s.\n"
                % (C.s2ts(info["duration"]), C.s2ts(W[-1]["end"])))
        f.write("Moc tinh tu dau video goc. Nhan dang tu dong (%s) — co the sai ten rieng.\n\n" % a.model)
        for s in S:
            f.write("[%s --> %s] %s\n" % (C.s2ts(s["start"]), C.s2ts(s["end"]), s["text"]))
    print("  xong sau %.0fs — %d cau, %d tu" % (time.time() - t0, len(S), len(W)))
    print("  -> %s\n  -> %s" % (out_json, out_txt))


if __name__ == "__main__":
    main()
