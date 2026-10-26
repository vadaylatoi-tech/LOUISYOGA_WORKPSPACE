---
name: louis-yoga-reel-edit-style
description: "User's standing rules for Louis Yoga TikTok/Reels edits (framing, graphics, SFX, audio mix, imagery)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e63febb9-cb00-4627-b38e-c2376eb90a00
  modified: 2026-10-24T10:05:15.397Z
---

Rules the user gave while reviewing Louis Yoga reels (Oct 2026):

- Keep footage full-bleed; covering the whole frame is only OK briefly for an effect. Put graphics in empty bands (shelf above head, table below) so face and product stay visible.
- Colour tone: pink (brand-ish, need not be exact `#d72182`) + gold accents on dark panels; user prefers this over the reference lime.
- Use REAL imagery over cartoon diagrams: Louis Yoga product avatars (`Dự án - Thay đổi giao diện website sapo/3. Tài nguyên hình ảnh/4. Avatar thảm final`), brand film B-roll (`Dự án tạo website daft - louis Yoga/Video Hero - Trang chủ.mp4`), or CC-licensed web photos with credit.
- SFX: "ít lặp" means fewer repeats, NOT zero repeats — each visual effect type gets a matching sound family (slam→impact, stamp→thud/boom, pill→pop, number→tick, whip→air, ✓→click). Mostly short ticks/clicks, ~2 booms per video. The hook must hit hard (impact + riser + boom + shake/flash).
- SFX REFERENCE = reel 2 (`LouisYoga_ChonTham_Reel_v2_hong.mp4`): user judged its SFX "vừa đủ, không lạm dụng" and reel 3 v3 (~1.1 events/s, layered, everyday SFX ≈ voice) "quá nhiều". Target: ~0.45–0.7 sounding events/s, one sound per beat, the 11 shared-sources library sounds (swoosh, quick-swoosh, punch, pop, pop-2, quick-ting, digital-counting-1, ding, correct, camera-shutter, riser-metallic); everyday SFX ≈ −3 dB vs voice, punches on slams/stamps ≈ +6–8 dB. No sound on every zoom cut. Measure with scratchpad `measure_reel_sfx.py`-style rebuild from the CUES list.
- Layout reference = reel 3 (full-bleed footage + graphics in empty bands).
- Audio priority: voice clearest (clean + a little warmth), SFX second, music light (~24 dB under voice).
- Product imagery: use the real product shots in the data folders (e.g. `Dự án tạo website daft - louis Yoga/DSC00985.jpg` rolled rubber mats); user rejected a generic "person kneeling" frame as superficial.

- Feedback 2026-10-26 on reels 01+02 (applies to FUTURE videos only, don't redo done ones): effects and SFX level OK ("vừa đủ"); product line/model picks correct. B-roll must show the FULL pose — brand-film close-ups cropped to 9:16 were "cận quá, không rõ tư thế" → use kit `mode: "fit"`, and web stock video/photos are allowed if they carry no other brand's logo/info (prefer vertical full-body clips). Footage looked blurry → root cause is the ~1 Mbps livestream source; pipeline now denoises+sharpens and renders jpeg 95/crf 14. Editing took too long → use the fast tools (snap_cuts, build_stems, stills.py, kit/scenes.tsx).

- Feedback 2026-10-27 on reels 03+04: "lạm dụng video không phải của Louis" (3–4 Pexels clips per video). PRIORITISE Louis Yoga's own material: product the speaker holds (FOCUS), product/model photos (avatar folders, louisyoga.vn galleries ~230 images incl. spray/towel/bag), brand film (fit). Web stock only if nothing Louis fits: max 1 clip/video, ≤2.5 s, never the main visual. Louis Facebook page videos = suggested future source, not yet.

**Why:** user said the first reel felt monotonous ("lặp hiệu ứng… nghe bị nhàm") and that the content is knowledge-sharing, so the speaker must be easy to listen to.

**How to apply:** start every new Louis Yoga reel from these rules; see [[louis-yoga-reel-pipeline]] for the toolchain. Also follows [[short-video-hook-and-ending]] (hook first, clear conclusion, no colour grade). Source shorts come from [[yoga-mat-shorts-project]].
