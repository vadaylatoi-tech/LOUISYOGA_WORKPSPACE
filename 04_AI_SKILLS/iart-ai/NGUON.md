# Bộ skill IART AI (motion graphics) — bản chép vào repo

Cài 29/10/2026 theo yêu cầu anh. Giấy phép MIT (LICENSE). Nguồn:
- iart-ai/tiktok-video-skills @ 2a77533 2026-06-22
- iart-ai/kinetic-typography-skills @ fccc94b 2026-06-22
- iart-ai/b-roll-skills @ a51e34b 2026-10-17

Đã sửa so với bản gốc: đổi tên skill thêm tiền tố `iart-`, thêm ghi chú đầu description để Claude không chọn nhầm thay skill edit Louis Yoga; chép thư mục `scripts/` dùng chung của gói vào từng skill.

Lưu ý khi chạy trên máy Windows của mình:
- `iart-talking-head-b-roll`: KHÔNG dùng `transcribe.mjs` (cần whisper.cpp hoặc key ElevenLabs) — lấy transcript từ hồ sơ `.hoso.words.json`.
  `render.mjs` cần `npm i playwright-core` + Chrome; nó ghi khung tạm vào thư mục TEMP → đặt `TEMP`/`TMP` sang D: trước khi chạy (không ghi C:).
- Các skill còn lại chủ yếu là hướng dẫn + công thức (markdown), script `.sh` chỉ là tiện ích chụp khung/ghép ảnh.
Cập nhật bản mới: clone lại repo gốc rồi chép đè như trên.

## Cài trên máy mới / sau khi pull
`cd D:/LOUGA_WORKSPACE/04_AI_SKILLS/iart-ai && npm i` (chỉ cài `playwright-core` cho `iart-talking-head-b-roll`; dùng Chrome có sẵn trên máy).
Đặt `npm_config_cache`, `TEMP`, `TMP` = `D:/LOUGA_WORKSPACE/_npm-cache/...` trước khi chạy (không ghi C:).

## Đã thử 29/10/2026 (máy GINART)
20 giây đầu video 11 "Asana hay Asana 25" (bản cut chưa edit): 2 thẻ so sánh ASANA 25 / ASANA hiện đúng lúc nói thông số
+ 1 cảnh phủ "4,5 LY — người mới tập / tập cơ bản ở nhà"; font Be Vietnam Pro, tông hồng–gold. `--check` đạt, render 20 s
mất ~6,5 s. Bài thử: Drive `05_VIDEO_PROJECTS/2026-10_san-sale/edit/_thu-iart-broll/` (page.html, transcript.json lấy từ hồ sơ).
