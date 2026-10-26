# 02 — SFX và âm thanh

## Chuẩn đã duyệt (đo thật)
Chủ thương hiệu so 2 video: **reel 2 có SFX "vừa đủ, hợp lý"**, reel 3 bản v3 "quá nhiều". Bản v4 (template này)
lấy đúng chuẩn reel 2:

| chỉ số | reel 2 (chuẩn) | reel 3 v3 (bị chê) | **v4 (đã duyệt)** |
|---|---|---|---|
| cue | 42 / 40.5 s | ~62 / 56 s, chồng 2–3 tiếng | 33 / 56 s, 1 tiếng/nhịp |
| tiếng nghe được / giây | 0.69 | ~1.1 | 0.43 |
| tiếng thường so với giọng | −3.2 dB | ≈ +1 dB | −3.5 dB |
| punch so với giọng | +6.3 dB | +4 dB | +7.1 dB |
| bộ tiếng | 11 tiếng thư viện | 31 tiếng cắt từ video khác | 11 tiếng thư viện |

Mục tiêu cho video mới: **0.45–0.7 tiếng/giây, tiếng thường ≈ −3 dB, punch +6..+8 dB, nhạc ≈ 24 dB dưới giọng.**
Kiểm trước khi render: `scripts/measure_sfx.py`. Sau render: `mix_stems.py` in lại số đo.

## Họ tiếng theo hiệu ứng (lặp được, nhưng phải đúng họ)
| hiệu ứng hình | file (assets/sfx) | volume gợi ý |
|---|---|---|
| chữ slam / dấu mộc / kết luận lớn | punch.mp3 | 0.7–0.95 |
| pill, nhãn, số bật ra | pop-2.mp3 (chính), pop.mp3 (xen kẽ) | 0.4–0.5 |
| số đổi / đếm | digital-counting-1.mp3 | 0.45 |
| B-roll VÀO, mở hook | swoosh.mp3 | 0.35–0.55 |
| panel trượt lên, callout, chuyển ý nhẹ | quick-swoosh.mp3 | 0.4–0.5 |
| ✓ lợi ích, highlight ảnh | quick-ting.mp3 | 0.4–0.45 |
| ✓ cuối / kết luận đúng | correct.mp3 | 0.4–0.45 |
| polaroid sản phẩm | camera-shutter.mp3 | 0.45 |
| dồn vào cú chốt hook | riser-metallic.mp3 (tự cắt đầu cho đỉnh rơi đúng cue) | 0.45 |
| kết thúc CTA | ding.mp3 | 0.35 |

Không đặt SFX: ở mối cắt zoom bình thường, lúc B-roll đi ra, lúc camera trượt (focus), lúc đầu gối/thanh đo nhún.
Chỉ chồng 2 tiếng ở cú chốt hook (riser → punch). `ONSET` (giây lead-in mỗi file) có sẵn trong `kit/sound.tsx`.

## Hook âm thanh (mẫu đã duyệt)
`0.00 swoosh` + `0.05 punch` (tiêu đề) → `0.58 pop-2` (dòng 2) → `riser-metallic` đỉnh tại cú chốt →
`punch 0.95` cùng lúc gạch chữ + dấu mộc + rung 10 khung/18 px + chớp trắng 0.6. Nhạc to hơn (0.2) trong hook, lùi
xuống 0.09 khi bắt đầu giảng, lên 0.26 ở CTA.

## Xử lý giọng (`scripts/process_voice.py`)
Giọng mẫu: năng lượng dồn 150–600 Hz, trên 5 kHz yếu → đục. Chuỗi mặc định:
highpass 75 → afftdn nhẹ → +1.5 dB @180 Hz (ấm) → −2.5 dB @450 Hz (bớt "hộp") → +3 dB @3.2 kHz, +2.5 dB @5.5 kHz
(rõ lời) → treble +2.5 @9 kHz (air) → nén 2.5:1 → deesser → limiter. Chạy `--analyze` để xem dải tần trước/sau;
giọng khác hẳn (nam trầm, mic khác) thì chỉnh `--chain`.

## Mix theo stem (`scripts/render_all.py` → `mix_stems.py`)
Remotion render riêng: SFX (`--props {"stem":"sfx"} --codec=wav`), nhạc (`{"stem":"music"}`), hình (`--muted`).
`mix_stems.py`: giọng → −16 LUFS; SFX giữ đúng volume trong Reel.tsx + `--sfx-rel −2.5 dB`; nhạc đặt 19 dB dưới
giọng rồi duck −5 dB khi có lời (≈24 dB khi nói); master loudnorm −14 LUFS / TP −1.5 (2 pass).
Đừng mix bằng Remotion "all" cho bản giao (giọng chưa xử lý, không duck).

## Nhạc
`assets/music/Inspired_KevinMacLeod_CCBY4.mp3` — điện tử nhẹ tích cực ~117 BPM, giữ chung cho cả series để nhận
diện. Credit bắt buộc: `Music: "Inspired" – Kevin MacLeod (incompetech.com), CC BY 4.0`.
Đổi nhạc: chọn bài CC BY/CC0 tempo 95–120, độ to đều, không lời; ghi credit.

## Bản quyền SFX
11 file trong `assets/sfx` lấy từ thư viện `shared-sources/sound-effects` của bộ skill gốc; `library.json` gốc
không ghi license → nếu chạy quảng cáo thương mại, thay bằng tiếng tương đương có license rõ.
