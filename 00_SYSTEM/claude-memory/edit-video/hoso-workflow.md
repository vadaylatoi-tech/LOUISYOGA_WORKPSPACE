---
name: hoso-workflow
description: Pre-built word-level "hồ sơ" next to each short video lets edit sessions skip Whisper; GPU Whisper setup on this machine
metadata:
  type: project
---

Since 2026-10-24 each video in `Video ngắn - thảm yoga/` has `<name>.hoso.words.json` (word-level large-v3 transcript of the short itself) and `<name>.brief.md` (hook/body/ending with text). `.claude/skills/nns-auto-sub/scripts/transcribe.py` was patched to use the hồ sơ directly or remapped via `<video>.plan.timemap.json` from nns-cut-silence (tested: median 0 s, p90 0.02 s vs real Whisper); `--no-hoso` forces Whisper. Project `CLAUDE.md` documents this. GPU: pip `nvidia-cublas-cu12` + `nvidia-cudnn-cu12`, add `site-packages/nvidia/*/bin` via os.add_dll_directory, use `int8_float16` (~25 s per 70 s video). Likely edit style project: `louis-yoga-remotion` (reads `transcript_raw.json` = hồ sơ `segments`). Related: [[yoga-mat-shorts-project]].
