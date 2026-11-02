---
name: louisyoga-reel-style1
description: "Dựng video ngắn talking-head tiếng Việt (TikTok/Reels/Shorts 9:16) theo PHONG CÁCH 1 LOUIS YOGA đã được chủ thương hiệu duyệt: hình người nói TRÀN KHUNG, zoom luân phiên giấu mối cắt, B-roll phim thương hiệu Louis Yoga, đồ hoạ tone hồng + vàng gold chỉ đặt ở vùng trống, caption karaoke, hook đập mạnh (chữ slam + gạch chữ + dấu mộc + rung/chớp), SFX vừa đủ (~0.5 tiếng/giây, 11 tiếng thư viện), giọng xử lý rõ + ấm, mix giọng > SFX > nhạc nhẹ, master −14 LUFS. Input: 1 file video thô có người nói. Output: mp4 1080×1920 đăng được + báo cáo. Dựng bằng Remotion + ffmpeg + faster-whisper. Trigger: '/louisyoga-reel-style1', 'edit video này theo phong cách 1 louis yoga', 'dựng reel louis yoga', 'edit video ngắn thảm yoga như bản đã duyệt'."
---

# Louis Yoga reel — phong cách 1

> Video có phần **giải thích kỹ thuật / so sánh thông số** → dùng **phong cách 2** (`louisyoga-reel-style2`: motion
> graphic toàn khung trên nền footage mờ, hook âm "dồn → lặng → nổ"). Style 2 dùng chung script + kit của skill này.

Bộ skill này đóng gói **đúng quy trình và gu đã được duyệt** qua 3 vòng góp ý trên video
"Thảm càng dày càng tốt? Chưa chắc!" (bản v4). Mọi đường dẫn bên dưới tính từ thư mục skill này
(`<SKILL>` = thư mục chứa file SKILL.md này).

Đọc trước khi làm (bắt buộc, ngắn):
- `references/01-phong-cach-hinh.md` — bố cục, màu, chữ, chuyển động, cái gì CẤM
- `references/02-sfx-va-am-thanh.md` — SFX nào cho hiệu ứng nào, mật độ, mức to, xử lý giọng, mix
- `references/03-quy-trinh-ky-thuat.md` — lệnh từng bước + bẫy đã gặp
- `references/04-checklist-qc.md` — kiểm trước khi giao
- `references/05-bai-hoc-tu-gop-y.md` — lịch sử góp ý của chủ thương hiệu (vì sao làm thế)
- `references/broll-index.md` — mốc giây dùng được trong phim thương hiệu

Ví dụ hoàn chỉnh: `remotion-template/src/reel/Reel.tsx` (chính là bản v4 đã duyệt) + `examples/`.

## Bước 0 — kiểm tra máy (luôn chạy đầu tiên)

```
python <SKILL>/scripts/preflight.py --video "<video thô>"
```
Báo THIẾU → đưa nguyên hướng dẫn cài cho người dùng và DỪNG. Không chạy tạm.
Người dùng không đưa video → hỏi đường dẫn.

## Quy trình (8 bước, có 2 cổng duyệt)

Tạo thư mục làm việc riêng cho mỗi video, ví dụ `<nơi người dùng chọn>/<ten-video>/` gồm `work/`, `project/`, file xuất.
KHÔNG ghi vào thư mục đã có file của người dùng; không ghi đè bản cũ (đặt _v2, _v3).

**NƠI LƯU — BẮT BUỘC (chủ thương hiệu chốt 26/10/2026):**
- **Video FINAL** → Google Drive `LOUGA_WORKSPACE_MEDIA/10_FINAL_DELIVERABLES/<YYYY-MM-DD>_<mã-dự-án>/<NN - tên video>.mp4`.
  Ngày = ngày edit; tên file = đúng tên video trong `cuts/`; bản sửa sau thêm `_v2`, `_v3` cùng thư mục.
  Ví dụ: `10_FINAL_DELIVERABLES/2026-10-26_san-sale/01 - Lau thảm bằng cồn có sao không.mp4`.
  Thư mục này CHỈ chứa video final + ảnh bìa cùng tên (`.jpg`, bước 8) — KHÔNG để video final trong `05_VIDEO_PROJECTS/` hay `11_COMPLETED_PROJECTS/`.
- **Hồ sơ làm việc** (work/, BAO-CAO, contact sheet) → Drive `05_VIDEO_PROJECTS/<mã-dự-án>/edit/<NN-ten-video>/`.
- **Project Remotion** → Drive `05_VIDEO_PROJECTS/<mã-dự-án>/edit/<NN-ten-video>/project`; không tạo gì trong `D:/LOUGA_WORKSPACE/05_VIDEO_PROJECTS`.
  `render_all.py`/`stills.py` tự chạy qua cache `LOUGA_CACHE` vì Drive không cài được node_modules; cache xóa được, không chứa gì duy nhất.

1. **Nghiên cứu nội dung**: video đã có hồ sơ (`<video>.brief.md` + `<video>.hoso.words.json` cạnh file) → CHỈ đọc
   brief, dùng `.hoso.words.json` làm transcript (KHÔNG chạy Whisper, KHÔNG xem lại video). Chưa có hồ sơ mới chạy
   `scripts/transcribe.py`. Tìm điểm yếu (hook, lặp, từ đệm, kết thiếu kết luận). Xem khung: `scripts/contact_sheet.py
   --every 2` (1 tấm) để biết vùng trống (kệ trên đầu, bàn dưới). File cắt từ livestream có ô PiP / khung thu nhỏ /
   người rời khung → xử lý theo `references/03` mục "Ô PiP" TRƯỚC khi cắt.
2. **Kế hoạch cắt**: viết `work/cuts_rough.json` lấy thẳng mốc từ của hồ sơ (`[start, end, "lý do"]`), rồi
   `scripts/snap_cuts.py --auto-pauses --report work/cuts_report.md` → `work/cuts.json` (tự kéo mép vào chỗ lặng
   thật, tự rút khoảng ngừng > 0.3 s, đánh dấu mép "NGHE LAI"). KHÔNG ngồi đo năng lượng tay từng mép.
   ▶ **CỔNG 1**: đưa người dùng bảng cắt (giây, lý do, ngữ cảnh) + ý tưởng dựng (hook, các cảnh đồ hoạ,
   B-roll, ảnh sản phẩm định dùng). Chờ OK. Nếu người dùng đã nói "cứ làm" thì ghi vào báo cáo và đi tiếp.
3. **Cắt**: `scripts/cut_words.py --words <video>.hoso.words.json` → clean.mp4 (đã khử nhiễu nhẹ + làm nét, xem
   "Độ nét") + clean.words.json. Chữ còn tiếng sau cắt được giữ tự động; đọc caption `gen_data.py` in ra, chữ "ma"
   ở mép cắt (vd "Nên", "Thì" chỉ còn khoảng lặng) bỏ bằng `fixes.json` → `drop`.
   **Cắt câu lặp có từ phủ định ("đừng", "không") ở gần mép → không cắt** (bài học video 12: suýt mất "đừng" →
   thành "cuộn chặt vào"). Mép "NGHE LAI" không có chỗ lặng thật thì bỏ cắt đó, chỉ rút khoảng lặng.
   **Luôn chạy `scripts/check_cuts.py --work work`** (Whisper GPU ~30 s nghe lại clean.mp4): nó chỉ ra mép nào làm
   MẤT chữ / SÓT tiếng, ở giây THÔ nào trong cuts.json và dời hướng nào → sửa cuts.json, cắt lại, chạy lại tới khi hết.
   (Đo trên 166 mép đợt Săn sale: ~1/5 mép snap vẫn lệch vì mốc từ Whisper lệch — không có quy tắc snap nào tốt hơn.)
   **Bug A "mép cắt lệch chữ" — chủ thương hiệu quyết KHÔNG sửa tiếp (28/10/2026)**: livestream nói liền, 85% chỗ cắt
   không có khoảng lặng; đã thử snap 4 kiểu + căn âm wav2vec2 đều không hơn (xem Drive `00_SYSTEM/SO-BUG.md`).
   Đừng viết lại cách đặt mép; chỉ dùng check_cuts rồi sửa tay chỗ nghe thấy.
   `fixes.json` "replace" áp cho MỌI từ trùng — sửa 1 chữ riêng lẻ thì dùng `drop` + `insert` (vd "làm"→"lắm").
4. **Mặt**: `scripts/track.py --video <thô> --out work/face.track.json --step 0.5` (model kèm sẵn).
5. **Dữ liệu**: `scripts/new_project.py --dest <project> --clean work/clean.mp4 --install` rồi
   `scripts/gen_data.py --words work/clean.words.json --face work/face.track.json --fixes work/fixes.json --out <project>/src/reel/data.ts`.
   `fixes.json` sửa thuật ngữ ASR nghe sai (tp→TPE, lúm thẳng→lún thảm, tí tay→tì tay, lưu dựa→Louis Yoga…).
   Caption tự giữ mỗi dòng ≤ 21 ký tự (`--max-chars`) và không tách từ ghép; từ ghép riêng của video → `"compound"`,
   muốn tự ngắt dòng → `"lines": ["dòng 1", "dòng 2", ...]` trong fixes.json (không cần viết caption_patch riêng).
6. **Dựng**: sửa `<project>/src/reel/Reel.tsx` trong các khối `▼ EDIT ▼` (bands, SEG_ZOOM theo số đoạn,
   PUNCHES, FOCUS, BROLL, IMPACTS, CUES, scenes). Đặt `CAP_Y`, `G` và mọi chữ cần đọc theo **vùng an toàn bậc thang** Reels/TikTok
   (A: y 250–860 · x 90–990; B: y 860–1430 · x 90–800; tính cả hộp chữ thật + animation — `references/01` mục "Khung & bố cục";
   kit đã tự căn/co chữ và thu panel theo vùng). Dùng atoms `src/kit/atoms.tsx` + khối dựng sẵn `src/kit/scenes.tsx`
   (MatCard, RecapRows, NumberRows, DoDont). Ảnh sản phẩm: `scripts/prep_products.py --dest <project>/public/img`.
   Kiểm bố cục: `scripts/stills.py --project <project> --out work/stills_sheet.jpg --times <giây hook, mỗi panel,
   mỗi B-roll, CTA>` (bundle 1 lần, ~3 s/khung → 1 tấm). Soi: chữ không đè mặt/sản phẩm, không cắt mép, không che số,
   không lọt ra ngoài vùng an toàn bậc thang (sửa ngay khi dựng, không thêm lượt render riêng).
7. **Âm thanh**: `scripts/process_voice.py --in work/voice_raw.wav --out work/voice_proc.wav --analyze`;
   `scripts/measure_sfx.py` để chắc mật độ/mức SFX đúng chuẩn TRƯỚC khi render (đọc được cue ghi bằng hằng
   `HOOK_DROP`, `VIDEO_FRAMES / FPS`, hằng tự đặt `const END = ...;` — chỉ cần là biểu thức số học).
8. **Render + mix**: `scripts/render_all.py --project <project> --voice work/voice_proc.wav --out "<Drive>/10_FINAL_DELIVERABLES/<YYYY-MM-DD>_<mã-dự-án>/<NN - tên video>.mp4"`
   (`--music-under N`: nhạc thấp hơn giọng N dB trước duck, mặc định 19 → ~24 dB khi nói; true peak AAC vượt −1,4 thì mix tự chặn đỉnh)
   (stem SFX + nhạc dựng bằng numpy `build_stems.py` vài giây; hình không tiếng jpeg 95/crf 14 ~3 phút/phút video;
   mix giọng > SFX > nhạc → −14 LUFS, TP −1.5). Nhiều video: render chạy nền, dựng video sau trong lúc chờ
   (mỗi render một `--port` riêng: 3123, 3131, 3141…).
   Render lại vì bản trước còn lỗi và **chưa giao** → thêm `--replace`: bản cũ chuyển ra
   `<project>/renders/_thay-the/…_KHONG-GIAO.mp4`, bản mới giữ đúng tên chuẩn. Không có `--replace` → `_v2` (chỉ dùng
   cho bản sửa SAU KHI đã giao). Mix lỗi giữa chừng không để lại file hỏng trong thư mục final.
   **Ảnh bìa (thumbnail)**: `scripts/make_cover.py "<file final>.mp4"` → tự chọn khung hook đủ tiêu đề, KHÔNG gạch
   chữ/dấu mộc (kiểu chủ thương hiệu duyệt 27/10/2026; `--co-gach` nếu muốn khung có dấu mộc), lưu `<tên video>.jpg`
   cạnh video và gắn làm ảnh bìa trong mp4 (copy luồng, kiểm md5 hình/tiếng, giữ mtime; chạy lại thì thay bìa cũ).
   Khung đầu video luôn trống chữ nên thiếu bước này thì Drive/Explorer/nền tảng hiện ảnh vô nghĩa.
   SOÁT ảnh JPG: hook nằm giữa khung trên B-roll hoặc panel/caption hiện ngay sau tiêu đề → chọn tay `--t <giây>`
   (đợt 27/10: 5/29 video phải chọn tay).
   Rồi QC theo `references/04-checklist-qc.md` (contact sheet bản cuối, chép lời lại bản cuối, số đo âm).
   ▶ **CỔNG 2**: giao file + báo cáo ngắn (đã làm gì, số đo, credit cần ghi, chỗ cần người dùng nghe/duyệt).

## Tốc độ (góp ý 26/10/2026: "edit 1 video quá lâu")
Mục tiêu ≤ 25–30 phút/video khi đã có hồ sơ. Chỗ từng tốn thời gian và cách đã xử lý:
| Chỗ chậm | Trước | Bây giờ |
|---|---|---|
| Stem SFX + nhạc | 2 lần render Remotion ~3,2 phút/lần | `build_stems.py` ~2 s (lệch < 1,5 ms) |
| Chọn mép cắt | đo năng lượng tay từng mép, 3–4 lượt | `snap_cuts.py` 1 s + `check_cuts.py` ~30 s chỉ đúng mép hỏng |
| Caption | tự viết lại từng dòng vì ngắt "cơ \| bản" | `gen_data.py` ngắt theo câu + từ ghép + ≤ 21 ký tự |
| Chữ rơi ở mối cắt | thêm tay qua `insert` | `cut_words.py` tự giữ chữ còn tiếng |
| Still soát bố cục | mỗi khung bundle lại | `stills.py` bundle 1 lần, 1 tấm sheet |
| Viết cảnh đồ hoạ | viết mới mỗi video | `kit/scenes.tsx` + `prep_products.py` |
Không lặp vòng soát quá 2 lần cho 1 cảnh; render video trước chạy nền khi dựng video sau.

## Độ nét (góp ý 26/10/2026: "hình hơi mờ")
Đo thật: mờ chủ yếu do NGUỒN — file livestream gốc `Video lọc nội dung.mp4` chỉ ~1 Mbps cho 1440×2560 + filter làm mịn
da của app live; chuỗi dựng chỉ làm mờ thêm chút (JPEG 80 của Remotion, mã hoá 3 lần). Đã xử lý: `cut_words.py`
khử khối nhẹ + làm nét `hqdn3d=1.5:1.5:3:3,cas=0.7` (không phải chỉnh màu; `--no-sharpen` để tắt), render
`--jpeg-quality=95 --crf=14`. Zoom giữ ≤ 1.30 (nguồn 1440 px → 1080 px không phải phóng ảnh). Muốn nét hẳn: quay/lưu
bản gốc từ máy/điện thoại (không qua livestream) — báo người dùng khi nguồn < 4 Mbps.

## Luật cứng (vi phạm = làm lại)

- Hình người nói **tràn khung**; chỉ che toàn khung trong chớp nhoáng để tạo hiệu ứng. Đồ hoạ ở vùng trống.
- Chữ/logo/CTA cần đọc nằm trong **vùng an toàn bậc thang** Reels/TikTok (A: y 250–860 · x 90–990; B: y 860–1430 · x 90–800)
  suốt lúc đọc; nền/footage/ảnh tràn khung.
- **Ảnh thật** thay vì hình vẽ: ảnh sản phẩm trong thư mục dữ liệu của người dùng, avatar web, B-roll phim
  thương hiệu, ảnh CC trên mạng (ghi credit). Không dùng ảnh "hời hợt" (người tạo dáng chung chung).
- **Tư liệu LOUIS YOGA trước tiên** (góp ý 27/10/2026: "đang lạm dụng video không phải của Louis"). Thứ tự ưu tiên khi
  cần hình minh hoạ: (1) sản phẩm người nói đang cầm/bày trong chính video (`FOCUS` zoom vào); (2) ảnh sản phẩm thật
  (avatar, ảnh trải phẳng đủ màu, kho `assets/louis-photos/` 76 ảnh người mẫu/cuộn thảm/đo độ dày/xịt/túi từ louisyoga.vn —
  tra `references/louis-photos-index.md`, dùng `mode: "photo"`); (3) phim thương
  hiệu Louis (`mode: "fit"` cho cảnh tư thế để thấy toàn thân, `crop` chỉ cho cận tay/bề mặt); (4) **chỉ khi 3 nguồn trên
  không có cảnh phù hợp** mới dùng clip web (Pexels…, không logo hãng khác): tối đa 1 clip/video, ≤ 2,5 s, không bao giờ
  làm hình chính, không ghi chữ như thể đó là thảm Louis. Ghi rõ trong báo cáo chỗ nào dùng clip ngoài và vì sao.
  Gợi ý nguồn thêm (chưa áp dụng): video trên trang Facebook Louis Yoga.
- **B-roll minh hoạ tư thế phải thấy TOÀN THÂN** (góp ý 26/10/2026: "cận cảnh quá, không rõ tư thế"): phim thương hiệu
  16:9 dùng `mode: "fit"` (mặc định — cả khung ngang trên nền mờ), `mode: "crop"` chỉ cho cận cảnh tay/bề mặt/logo.
- SFX theo `references/02`: mỗi loại hiệu ứng một họ tiếng; **lặp được** nhưng ít; 0.45–0.7 tiếng/giây;
  không SFX ở mối cắt zoom thường; chỉ 1–3 cú "nặng" (punch + rung) cho khoảnh khắc lớn.
- Mix: giọng rõ nhất → SFX (thường −3 dB, punch +6..+8 dB so với giọng) → nhạc nhẹ (~24 dB dưới giọng).
- Hook trong 2 s đầu phải "đập" (chữ slam + chốt ý bất ngờ); kết có kết luận rõ + CTA "Follow Louis Yoga".
- Không chỉnh màu (color grade) nếu không được yêu cầu. Không bịa thông số sản phẩm — lấy từ dữ liệu web
  hoặc hỏi người dùng (vd độ dày: ASANA/MOON 4.5 mm, BASIC/QUEEN/DIAMOND 5 mm).
- Credit bắt buộc khi dùng: nhạc "Inspired" – Kevin MacLeod (incompetech.com) CC BY 4.0; ảnh CC theo nguồn.

## Báo cáo giao kèm

Ghi `BAO-CAO-<ten>.md` trong thư mục hồ sơ `05_VIDEO_PROJECTS/<mã-dự-án>/edit/<NN-ten-video>/` (không để trong 10_FINAL_DELIVERABLES): video gốc, lý do chọn, điểm yếu → cách xử lý, bảng cắt, B-roll/ảnh đã
dùng (nguồn + giấy phép), số đo âm (SFX/giây, dB so với giọng, nhạc dưới giọng, LUFS/TP), credit cho caption bài
đăng, những chỗ cần người dùng nghe/kiểm.
