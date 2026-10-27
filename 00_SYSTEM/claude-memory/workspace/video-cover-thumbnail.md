---
name: video-cover-thumbnail
description: "Every final video gets a cover JPG + embedded mp4 cover from the hook frame WITHOUT strike line/stamp (user's choice 2026-10-27)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7e681fd1-276f-4db7-a3f3-f6544d001dfb
  modified: 2026-10-27T13:29:29.672Z
---

Each final video in `10_FINAL_DELIVERABLES/` gets `<NN - tên video>.jpg` next to it and the same image embedded as mp4 cover, made by `louisyoga-reel-style1/scripts/make_cover.py` (default = hook frame with full 2-line title, before the strike line + stamp appear).

**Why:** Frame 0 of these reels has no text, so Drive/Explorer/TikTok showed meaningless thumbnails. User saw a sample with strike line + "SAI LẦM!" stamp and asked for no strike; strike and stamp appear in the same frame, so the stamp goes too.

**How to apply:** After rendering any final ([[final-video-location]]), run make_cover.py on it. Only use `--co-gach` if the user asks for the stamp.
