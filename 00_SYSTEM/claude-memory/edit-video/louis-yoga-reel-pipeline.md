---
name: louis-yoga-reel-pipeline
description: "Where the Louis Yoga reel projects, assets and render pipeline live, and gotchas hit"
metadata:
  node_type: memory
  type: project
  originSessionId: e63febb9-cb00-4627-b38e-c2376eb90a00
  modified: 2026-10-24T10:38:28.433Z
---

Louis Yoga short-video work (started 2026-10-24) lives in `D:\LOUGA_WORKSPACE` (workspace 12 thư mục):
- Remotion app `05_VIDEO_PROJECTS/louis-yoga-remotion/` — compositions `LouisYogaReel2` (reel 2, chọn thảm hút mồ hôi) and `LouisYogaReel3` (video 05 "Thảm càng dày càng tốt – chưa chắc"); reel3 imports shared graphic atoms exported from `src/reel2/LouisYogaReel2.tsx`.
- Raw shorts to edit next: `11_COMPLETED_PROJECTS/2026-10_reels-chon-tham-dot1/cuts/01–04` (05 done). Outputs go to `11_COMPLETED_PROJECTS/2026-10_reels-chon-tham-dot1/builds/louis-yoga-reel-NN/` (thử nghiệm v2/v3: `11_COMPLETED_PROJECTS/2026-10_reels-thu-nghiem-v2-v3/`).
- Extracted SFX pack (from 2 FB SFX-breakdown reels) in `public/reel3/sfx/*.wav`; music "Inspired" – Kevin MacLeod CC BY 4.0 in `public/reel2/`.
- Pipeline: transcribe (nns-auto-sub transcribe.py, CPU only — no cuBLAS; needs PyAV <16), cut fillers at measured silences, face track (nns-face-highlight), Remotion render video muted + audio stems via `--props '{"stem":"sfx"|"music"}' --codec=wav`, then ffmpeg mix with processed voice and loudnorm -14 LUFS.
- Gotchas: re-encode footage with `-g 10 -bf 0` or Remotion compositor errors "No frame found"; another studio may hold port 3000, so pass `--port=3123`; Windows python prints need UTF-8.

PACKAGED SKILL (2026-10-24, verified end-to-end — reproduces reel 3 v4 exactly): `D:\LOUGA_WORKSPACE\04_AI_SKILLS\louisyoga-reel-style1-package\` (skill dir `louisyoga-reel-style1/`, installers, PROMPT-BAT-DAU.txt, zip 140 MB). For new Louis Yoga reels prefer this skill's scripts + `remotion-template` (kit atoms) over the older ad-hoc reel2/reel3 code.

Related: [[louis-yoga-reel-edit-style]]

PROGRESS 2026-10-24: videos 01 and 02 edited with the skill → `11_COMPLETED_PROJECTS/2026-10_reels-chon-tham-dot1/builds/louis-yoga-reel-01/`, `11_COMPLETED_PROJECTS/2026-10_reels-chon-tham-dot1/builds/louis-yoga-reel-02/` (each has project/, work/, *_v1.mp4, BAO-CAO). Next: 03, 04, 06+. Gotchas: skill `render_all.py` needed `a.project = os.path.abspath(a.project)` (patched in the skill copy under `04_AI_SKILLS/louisyoga-reel-style1-package` (bản sao cũ trong kho edit đã gộp vào đây), NOT in the zip copy); gen_data's 4-word caption split breaks phrases → rebuild captions from hand-written line list; hồ sơ word timings swallow pauses, so snap cuts with a 20 ms energy profile. Product avatars per line: `Dự án - Thay đổi giao diện website sapo/3. Tài nguyên hình ảnh/4. Avatar thảm final/` (Harmony/Balance/Mastery × 4 models).

SPEED/QUALITY UPGRADE 2026-10-26 (skill copies in `04_AI_SKILLS/louisyoga-reel-style1-package` (bản sao cũ trong kho edit đã gộp vào đây) and `D:\LOUGA_WORKSPACE\04_AI_SKILLS\louisyoga-reel-style1-package` kept identical; no zip exists now): new scripts snap_cuts.py (rough cuts from hồ sơ word times → snapped to real silence + auto pause trim), build_stems.py (SFX/music stems in numpy, replaces 2×~3.2 min Remotion wav renders), stills.py (one bundle, ~3 s/frame contact sheet), prep_products.py (avatar crops); cut_words keeps partly-cut words + marks sentence/cut ends + sharpen filter; gen_data breaks captions by sentence + Vietnamese compounds; kit/scenes.tsx (MatCard, RecapRows, NumberRows); kit Broll mode fit/crop/cover + per-item src. Measured: picture render ≈ 2.6 min per 50 s video; concurrency >4 gives nothing. Web B-roll library BUILT 2026-10-26: 17 Pexels vertical full-body clips (user-approved download) in skill `assets/broll/web/` (145 MB, 30fps, logo-checked), indexed with per-second content in `references/broll-index.md`, sources in `assets/broll/web/NGUON.md`. Use `mode: "cover", src: "broll/web/<file>.mp4"`. Pexels pages throw a Cloudflare CAPTCHA after rapid browsing — never solve it; file sizes/downloads work via videos.pexels.com/video-files/<id>/<id>-hd_1080_1920_<fps>fps.mp4.

LOUIS PHOTO LIBRARY 2026-10-27: skill `assets/louis-photos/` (76 curated louisyoga.vn images, 9 MB: tu-the, sinh-hoat, cuon-tham, do-day calipers, be-mat, xit-ve-sinh, khan, tui-dung-tham) indexed in `references/louis-photos-index.md`; new_project copies it; Broll `mode: "photo"`. Reels 03/04 re-rendered as _v2 with Louis-only B-roll. louisyoga.vn product pages scrape fine with curl (Sapo, images on bizweb.dktcdn.net); Windows python writes 
 — strip before shell loops.
