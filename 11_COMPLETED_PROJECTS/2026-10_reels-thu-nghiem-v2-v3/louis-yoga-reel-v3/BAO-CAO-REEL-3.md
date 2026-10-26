# Louis Yoga — Reel 3 "Thảm càng dày càng tốt? Chưa chắc!"

Ngày làm: 24/10/2026.
Video gốc: `Video ngắn - thảm yoga/05 - Thảm càng dày càng tốt - chưa chắc.mp4` (65.4s, 1440×2560).
Thành phẩm: `LouisYoga_ThamCangDay_Reel_v1.mp4` (56.2s, 1080×1920 @30fps, −14.0 LUFS, true peak −1.5 dBTP).

## Vì sao chọn video 05

- Hook đi ngược số đông ("càng dày càng tốt? chưa chắc") giữ chân người xem tốt nhất trong 5 video. Đây cũng là cấu trúc "tưởng vậy… nhưng không" của video mẫu.
- Chị diễn giả cầm tấm thảm thật (BASIC xanh dương, cao su 5 mm) suốt từ giây 9 nên làm callout chỉ thẳng vào sản phẩm được.
- Nội dung nối tiếp reel 2 (4,5 ly / 5 ly) nên đăng thành chuỗi được.

## Nội dung và điểm yếu đã xử lý

| Điểm yếu | Cách xử lý |
|---|---|
| Không có hook, câu đầu nói lặp 2 lần | Tiêu đề "THẢM CÀNG DÀY / CÀNG TỐT?" + dấu mộc "CHƯA CHẮC!" ngay giây 0–2. Cắt câu lặp |
| Từ đệm: "ví dụ như là" (2 lần), "các cái", "chẳng hạn", "cái…" kéo dài, "nó sẽ có nhiều loại đó" | Cắt 10 chỗ tại khoảng lặng thật (đo năng lượng từng 10 ms). **65.4s → 54.3s** |
| Máy quay tĩnh, góc rộng, mặt nhỏ | Mỗi đoạn zoom một mức khác nhau (1.10–1.30), xen kẽ chặt/rộng để giấu mối cắt. Punch-in vào từ khoá. Có "zoom blur" ở mỗi mối cắt |
| Chỉ có 1 cảnh suốt 1 phút | 5 cảnh B-roll toàn màn hình từ phim thương hiệu Louis Yoga (bài nâng cao, quỳ gối, tì tay, trồng chuối, thiền), vào/ra bằng whip ngang |
| Khái niệm "độ nén" khó hình dung | Sơ đồ đầu gối ấn xuống: TPE foam lún sâu ("DỄ LÚN!"), cao su 5 ly lún nông ("✓ ỔN ĐỊNH") |
| Đoạn "như thế này này" chỉ có lời | Camera trượt từ mặt xuống tấm thảm đang cầm + callout "Thảm Basic · cao su 5 mm", "Độ nén chắc" |
| Kết thúc nhạt | Checklist 4 lợi ích + màn CTA: logo, "Follow Louis Yoga", polaroid Basic 5 mm và Asana 4,5 mm |

## Theo góp ý của anh: hình tràn khung

- Footage luôn **full khung**, không có tấm nền che toàn màn hình nào.
- Đồ hoạ chỉ nằm ở 2 dải: kệ phía trên đầu (tiêu đề, tag) và vùng khăn/hộp trên bàn phía dưới (bảng so sánh, sơ đồ, checklist). Mặt và tấm thảm luôn lộ rõ.
- Cảnh toàn màn hình duy nhất là B-roll thật của Louis Yoga.

## Tài nguyên đã dùng

- Skill: `nns-auto-sub/transcribe.py` (chép lời word-level), `nns-face-highlight/track.py` (dò mặt để punch-in), cách dựng Remotion theo `edit-nns-v1`.
- B-roll: `Dự án tạo website daft - louis Yoga/Video Hero - Trang chủ.mp4`, đã bỏ các đoạn có chữ/icon in sẵn.
- Ảnh thảm: avatar website (`4. Avatar thảm final`): Basic xanh dương, Asana đen.
- Nhạc: "Inspired" – Kevin MacLeod, CC BY 4.0 (giữ cùng nhạc với reel 2 để chuỗi video nhận diện được). SFX: `shared-sources/sound-effects`.
- Composition: `louis-yoga-remotion/src/reel3/LouisYogaReel3.tsx` (id `LouisYogaReel3`). Dữ liệu caption sinh từ transcript (`src/reel3/data.ts`).

Credit cho caption bài đăng:
`Music: "Inspired" – Kevin MacLeod (incompetech.com), CC BY 4.0`

## Bản v2 — `LouisYoga_ThamCangDay_Reel_v2.mp4` (sửa theo góp ý)

### SFX: học từ 2 video tham khảo
Đo trên 2 video anh gửi (Facebook share/v/1ETuvUby7z = HusniXD motion graphic, share/r/1DPJYfCzoA = lewisdang talking-head). Video 2 gần như chỉ có lớp SFX (giữa các tiếng là im lặng tuyệt đối) nên đo được từng tiếng:
- Khoảng 43 tiếng trong 21s, **đa số dài dưới 0,15s**: tick/click ~2 kHz mỗi lần chữ hiện ra; chuỗi 4 tick cách nhau 0,1s khi chữ hiện từng nhịp.
- Whoosh ngắn, dải cao ("air") cho mỗi cú lia/trượt.
- **Bass boom chỉ 2 lần cả video** cho 2 khoảnh khắc lớn nhất.
- Click đôi khi có con trỏ, thud trầm khi thẻ đặt xuống. Không lặp liền cùng 1 tiếng, mức to xen kẽ.

Áp dụng vào reel 3:
- Tách 31 tiếng từ 2 video thành bộ `public/reel3/sfx/`.
- Bỏ swoosh/punch lặp ở mọi mối cắt. Giờ mỗi lần chữ hiện có tick/pop riêng, số liệu dùng chuỗi tick gõ chữ, B-roll dùng 7 kiểu "air" khác nhau.
- Boom chỉ 2 lần: "CHƯA CHẮC!" và "DỄ LÚN!".
- Lưu ý bản quyền: các tiếng này cắt từ video của người khác (họ phát sound pack cho người comment). Nếu chạy quảng cáo thương mại, anh nên lấy bộ sound pack gốc từ tác giả hoặc thay bằng tiếng tương đương có license.

### Âm thanh: giọng rõ nhất, SFX thứ 2, nhạc nhẹ
- **Xử lý giọng:** giọng gốc dồn ở 150–600 Hz, dải trên 5 kHz yếu nên hơi đục. Em đã:
  - Lọc rumble dưới 75 Hz, khử ồn nhẹ.
  - Giữ ấm ở 180 Hz, giảm "tiếng hộp" ở 450 Hz −2,5 dB.
  - Tăng rõ lời ở 3,2 kHz +3 dB và 5,5 kHz +2,5 dB, thêm "air" trên 9 kHz.
  - Nén 2,5:1, khử xì.
- **Mix theo stem:** Remotion xuất riêng hình, SFX và nhạc; mix với giọng đã xử lý bằng `mix_stems.py`. Đo được:
  - Giọng trung bình −18,9 dB.
  - SFX thông thường thấp hơn giọng ~4 dB; tiếng nhấn (boom/hit) có limiter, không vượt giọng quá ~2 dB.
  - Nhạc thấp hơn giọng ~24 dB khi chị nói, tự hạ thêm 5 dB mỗi khi có lời.
  - Master −14 LUFS, đỉnh −1,4 dBTP.

### 2 lỗi trong ảnh anh chụp
1. **Khối tím che số 8/9:** là lỗi. Thanh TPE được lập trình dày dần lên phía trên nên đè vào số. Đã sửa: thanh dày dần xuống dưới, số luôn nằm trọn phía trên.
2. **Sơ đồ quỳ gối:** đã thay cục "đầu gối" vẽ tay bằng **2 ảnh thật**:
   - Bên TPE: ảnh thảm foam cuộn, "Yoga mat.jpg" – Gausanchennai, CC BY-SA 4.0.
   - Bên cao su: khung hình phim Louis Yoga, người tập quỳ gối, tì tay trên thảm cao su xanh.
   - Bên dưới mỗi ảnh có thanh đo độ lún có hoạt ảnh (foam lún sâu, cao su lún ít).

### Ghi chú cho các video sau
- Ưu tiên ảnh/clip thật thay cho hình vẽ: avatar sản phẩm trên web, B-roll phim thương hiệu, ảnh CC trên mạng có ghi nguồn.
- Giữ hình tràn khung; đồ hoạ chỉ đặt ở vùng trống.
- SFX theo "ngôn ngữ" ở trên, mỗi video tối đa ~2 boom.
- Luôn mix theo stem: giọng → SFX → nhạc.

Credit cho caption bài đăng (bản v2):
`Music: "Inspired" – Kevin MacLeod (incompetech.com), CC BY 4.0 · Ảnh thảm foam: Gausanchennai, CC BY-SA 4.0`

## Bản v3 — `LouisYoga_ThamCangDay_Reel_v3.mp4` (sửa theo góp ý lần 2)

- **SFX to hơn:** tick/pop thông thường giờ ngang giọng (≈ +1 dB so với giọng trung bình, trước đó −4 dB). Tiếng nhấn được vượt giọng tối đa ~3–4 dB nhờ limiter riêng cho lớp SFX. Nhạc vẫn nhẹ, ~24 dB dưới giọng. Master −14 LUFS, đỉnh −1,4 dBTP.
- **Được lặp, nhưng hợp hiệu ứng:** mỗi loại chuyển động có một "họ" tiếng riêng:

  | Hiệu ứng hình | Tiếng |
  |---|---|
  | Chữ đập vào | impact |
  | Dấu mộc | thud (+ boom ở 2 điểm lớn) |
  | Pill bật ra | pop |
  | Số đổi | tick gõ chữ |
  | Panel trượt | swish |
  | B-roll lia vào/ra | air whoosh |
  | Dấu ✓ | click / click đôi, ✓ cuối = ping |
  | Kẻ đường callout | chirp |
  | Camera trượt xuống thảm | riser |
  | Polaroid | tiếng chụp ảnh |

- **Hook ấn tượng hơn (0–2,3s):**
  - "THẢM CÀNG DÀY" đập vào (impact + whoosh, rung khung, chớp trắng).
  - "CÀNG TỐT?" đập vào lần 2.
  - Riser dâng lên, rồi đúng giây 1,45: **gạch chéo vàng lên "CÀNG TỐT?"** + "CHƯA CHẮC!" rơi xuống (boom + rung mạnh + chớp + zoom cận mặt), đặt trên dải tối cho nổi chữ.
  - Nhạc to hơn chút trong hook rồi lùi xuống khi chị bắt đầu giảng.
- **Ảnh phân đoạn quỳ gối:** thay ảnh người quỳ bằng ảnh sản phẩm thật **DSC00985.jpg** (6 cuộn thảm cao su Louis Yoga, thấy rõ mép thảm đặc, chữ LOUISYOGA), lấy trong `Dự án tạo website daft - louis Yoga/`.

## Bản v4 — `LouisYoga_ThamCangDay_Reel_v4.mp4`: bố cục video 2 + SFX kiểu video 1

Anh nhận xét: bố cục video 2 tốt, nhưng SFX của video 1 (reel 2) vừa đủ và hợp lý hơn. Em đo lại lớp SFX của video 1 bằng cách dựng lại từ đúng danh sách cue trong code, rồi áp đúng tỉ lệ đó:

| | Video 1 (chuẩn) | Video 2 bản v3 | **Video 2 bản v4** |
|---|---|---|---|
| Số cue | 42 trong 40,5s | ~62 trong 56s, nhiều chỗ chồng 2–3 tiếng | **33 trong 56s, 1 tiếng/nhịp** |
| Tiếng nghe được / giây | 0,69 | ~1,1 | **0,43** |
| Bộ tiếng | 11 tiếng thư viện quen thuộc | 31 tiếng tách từ video tham khảo | **đúng 11 tiếng của video 1** |
| Tiếng thường ngày so với giọng | −3,2 dB | ≈ +1 dB | **−3,5 dB** |
| Punch (đập chữ/dấu mộc) | +6,3 dB | +4 dB | **+7,1 dB** |

- Hình giữ nguyên bản v3 (hook gạch chữ, rung, zoom; ảnh cuộn thảm Louis Yoga thật; B-roll; panel).
- Mỗi hiệu ứng một tiếng: đập chữ/dấu mộc = punch, pill/nhãn = pop, số = tiếng đếm số, B-roll/panel = swoosh, ✓ = ting, ✓ cuối = correct, polaroid = tiếng chụp ảnh.
- Hook: swoosh + punch → pop → riser dâng vào cú punch "CHƯA CHẮC!" (giống cách video 1 làm ở dấu mộc "HOT YOGA").
- Bỏ tiếng ở các mối cắt zoom và lúc B-roll đi ra, chỉ giữ tiếng lúc B-roll đi vào.

## Cần anh kiểm tra

1. Caption đã sửa: "tp" → TPE, "tp soap" → TPE foam, "lúm thẳng" → lún thảm, "tí tay" → tì tay. Anh nghe lại xem đúng thuật ngữ chưa.
2. Câu "mọi người tập ít nó cũng sẽ an tâm hơn": em bỏ chữ "ít" trong caption vì có vẻ là nói vấp.
