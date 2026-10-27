---
name: edit-style-nns
description: "Phong cách edit video talking-head 'AI Prompt Tips' tiếng Việt (kênh tự nhận 'Cường mê AI') — phân tích đo đạc từ 1 video mẫu thực tế (67.6s, 9:16). Đọc khi user đưa file voice-over (mp3/wav) + transcript và muốn nhận về một EDIT BLUEPRINT (timeline theo giây, cut points, prompt B-roll, text overlay script, gợi ý nhạc/SFX/màu, checklist QC) để tự dựng bằng CapCut — KHÔNG build ra file video hay HyperFrames composition. Trigger: '/edit-style-nns', '/edit-style-X' nói chung khi X khớp phong cách này, hoặc câu như 'lên blueprint edit theo phong cách video này', 'phân tích rồi cho tôi timeline dựng CapCut'."
---

# Edit Style — "AI Prompt Tips" Talking-Head (Cường mê AI)

> Nguồn: đo đạc trực tiếp trên 1 video mẫu (`FDown.vn_Tai_video_Facebook_720p (HD)_3817.mp4`,
> 67.59s, 720×1280 @30fps, audio AAC 44.1kHz stereo). Phân tích bằng `ffprobe`/`ffmpeg`
> (scene-detect, silencedetect, volumedetect, ebur128, lấy mẫu pixel màu) + đọc trực tiếp
> khung hình — không phải suy đoán từ trí nhớ chung. Coi đây là **nguồn sự thật duy nhất**
> về phong cách; đọc toàn bộ trước khi tạo blueprint cho video mới.
>
> Đây là skill **tạo blueprint để dựng tay trong CapCut**, khác với các skill HyperFrames
> (`/short-form-video`, `/auto-cut`...) vốn build ra composition/video thật. Không build file
> video ở đây — output cuối là một **văn bản blueprint** theo cấu trúc cố định ở dưới.

---

## 1. Style DNA (rút ra từ video mẫu)

### Cấu trúc tổng thể & timing đo được

| Phần | Thời gian | Tỉ trọng | Đặc điểm |
|---|---|---|---|
| **Hook** | 0.0–8.4s | ~12% | Cắt rất nhanh (6 cut trong 8.4s ≈ mỗi 1.4s). Avatar tròn + icon 💡 + title stack chữ hoa đè lên talking head 2 dòng đầu → B-roll tay gõ laptop chớp nhanh → payoff graphic to bản ("HIỆU SUẤT x10") → stinger số "1" mở tip đầu. |
| **Thân bài (N tip, video mẫu N=3)** | 8.4–63.8s | ~82% | Lặp lại 1 khung "tip-cycle" cho mỗi tip (xem mục 2). Nhịp cắt chậm hơn hook: mỗi cut ~2.9s trung bình, nhưng thực chất là card/screenshot giữ hình 5–7s rồi mới cắt — không cắt đều. |
| **Kết (Outro)** | 63.8–67.6s | ~6% | Chỉ còn talking head, không graphic. Caption CTA nối tiếp ("thử liền đi nha" → "follow mình" → "để không bỏ lỡ" → dòng chốt). |

### Tip-cycle — khung lặp lại của mỗi tip trong thân bài (đây là "nhịp tim" của phong cách)

```
[Talking head, 2–4s]  dẫn/đặt vấn đề
        ↓
[Prompt Card, 5–7s]   thẻ nâu trên nền kem, "Prompt" cam ở trên,
                       chữ prompt build dần kiểu typewriter (con trỏ | nhấp nháy),
                       ăn khớp với VO đọc nguyên câu prompt
        ↓ (đôi khi)
[Sửa từ khoá]          gạch đỏ 1 từ trong câu, chữ mới nối vào ngay sau
                       → dùng khi VO nói kiểu "sửa cụm từ", "gắt hơn thì", "thách thức nhé"
        ↓
[Demo Screenshot, 5–7s] nền gradient cam, khung chat/app ở giữa,
                       mũi tên trắng tay vẽ + label "input"/"output",
                       khoanh ĐỎ đặc (không phải khung viền) lên đoạn kết quả then chốt
        ↓ (đôi khi, 2–4s)
[Payoff / Meme / Credibility]  1 trong 3:
   - Headline Card 2 dòng in hoa (kiểu "TIẾT KIỆM RẤT NHIỀU THỜI GIAN")
   - Sticker mèo phản ứng dán lên góc màn hình (bông đùa)
   - B-roll uy tín: chèn cảnh phỏng vấn/chuyên gia thật khi VO nói "học được từ chuyên gia..."
        ↓
[Talking head, 2–3s]   phản ứng / bắc cầu sang tip kế
        ↓
[Stinger số, 0.3–0.6s] hình "pow" đen 8 cạnh, số to trắng giữa (1/2/3...),
                       kèm SFX bump âm lượng (đo được +2.5–2.8dB so với baseline)
```

Trước outro có thêm 1 nhịp riêng: **Recap Badge** (2–3s) — các viên pill kem "PROMPT ❶/❷/❸..."
xếp dọc, đè lên ảnh stock robot/AI tông cam, đúng lúc VO tóm "kết hợp cả N câu lại".

### Bảng scene — 8 loại cảnh cố định

| # | Scene | Khi dùng | Hold time |
|---|---|---|---|
| 1 | **Talking head** | Nền/mặc định, quay về giữa mọi beat | 2–7s/lần |
| 2 | **Prompt Card** | Mỗi khi VO đọc nguyên văn 1 câu prompt | 5–7s (≈ độ dài câu VO) |
| 3 | **Sửa từ khoá (strike-through edit)** | VO nói về việc sửa/tinh chỉnh prompt | 1–2s |
| 4 | **Demo Screenshot (input/output + khoanh đỏ)** | VO show kết quả AI trả về | 5–7s |
| 5 | **Headline Payoff Card** | Chốt lợi ích ngắn, 1 câu | 1–2s |
| 6 | **Sticker/meme phản ứng** | Bông đùa, giải lao thị giác | 1–2s |
| 7 | **B-roll uy tín (chuyên gia/stock AI)** | Trích dẫn nguồn/chuyên gia, hoặc minh hoạ khái niệm AI trừu tượng | 2–3s |
| 8 | **Stinger số (starburst)** | Chuyển giữa các tip | 0.3–0.6s |
| 9 | **Recap Badge** | Ngay trước outro, tóm tất cả tip | 2–3s |

### Màu (đo pixel thật từ khung hình, không suy đoán)

| Token | Hex đo được | Dùng cho |
|---|---|---|
| Kem/ivory | `#FCF3E1` | Nền Prompt Card, nền Headline Card |
| Nâu đen | `#302221` | Khối chữ prompt bên trong card |
| Cam chính | `#FF9248` (dải `#FE934A`–`#FF9248`) | Label "Prompt", headline, badge "PROMPT" |
| Đỏ khoanh/gạch | `#C41E20` | Highlight kết quả trong Demo Screenshot, gạch từ bị sửa |
| Gradient nền Demo | `#D89778` → `#D57534` (chéo, sáng→đậm) | Backdrop cho Demo Screenshot |
| Trắng | `#FFFFFF` | Caption, chữ trong box tối |
| Bubble input | `#EEECEA` (gần trắng, hơi xám ấm) | Bong bóng câu hỏi input |

Footage talking head: **không LUT rõ rệt**, tông da tự nhiên, tương phản vừa phải.
**Không có** film grain / vignette / glitch. Đồ hoạ (card, headline, gradient) mới mang bảng
màu ấm nói trên — tách biệt hẳn với tông tự nhiên của cam quay người.

### Chữ (typography)

| Vai trò | Style |
|---|---|
| Caption lời nói (đồng bộ VO) | Bold sans, trắng + viền đen dày, giữa khung theo chiều ngang, y≈78–85% chiều cao. **Cắt theo CỤM/CÂU (2–4 từ), không phải karaoke từng từ** — đây là điểm khác biệt so với style short-form karaoke thông thường. |
| Title hook (2 dòng đầu video) | In hoa, đậm, xếp 2 dòng, trắng, góc trên-trái, đi kèm avatar tròn viền + icon 💡 — chỉ dùng ở giây đầu hook |
| Label "Prompt" | Cam đậm, bold, cỡ lớn, giữa, phía trên card nâu |
| Chữ trong Prompt Card | Trắng bold trên nền nâu. **Karaoke word-highlight** (nâng cấp sau khi so đối thủ vòng 2, thay cho typewriter reveal-từ-vô-hình ban đầu): hiện NGUYÊN CÂU ngay từ đầu ở màu mờ (~opacity 0.4-0.46), mỗi từ SÁNG lên đúng lúc VO đọc đến từ đó (từ trước quay lại mờ). Trong CapCut dùng thẳng preset "Karaoke" có sẵn cho phụ đề. Khi build bằng HyperFrames: bọc theo TỪ (không theo ký tự — xem mục 6) để không bị lỗi xuống dòng giữa từ. |
| Sửa từ khoá | Gạch ngang đỏ trên từ cũ, chữ mới in tiếp ngay sau — không fade, xuất hiện tức thì |
| Headline Payoff | 2 dòng in hoa bold, cam/trắng xen, giữa khung |
| Label input/output | Bold đen/trắng viền, mũi tên vẽ tay cong chỉ vào điểm chính |

### Sound design (đo bằng ebur128/volumedetect, không nghe cảm tính)

- **Không có khoảng lặng thật** (`silencedetect` ở -30dB/0.2s: 0 khoảng lặng trong 67.6s) →
  nhạc nền chạy **liên tục toàn video**, không tắt nhạc khi giọng nói.
- **Loudness tổng**: −14.1 LUFS integrated, **LRA chỉ 3.0 LU** → mix bị nén/limit khá chặt,
  gần như không có đoạn to/nhỏ rõ rệt — nhạc nền bị duck xuống thấp, ổn định dưới giọng nói.
- **SFX tại các stinger số**: đo được mean volume tăng từ −18.7dB (baseline lúc card đang giữ
  hình) lên −16.0dB, max volume tăng từ −4.3dB lên −1.5/−1.8dB tại mọi thời điểm có stinger số
  → xác nhận có **1 SFX impact/whoosh ngắn** đè lên đúng lúc stinger xuất hiện, không phải chỉ
  là hình ảnh.
- Nhạc nền: dựa theo mood video (năng lượng, gọn, không kịch tính) — nhạc điện tử/corporate
  nhẹ, tempo trung-nhanh (~110–130 BPM), không lời, mix ở mức thấp dưới VO.

### Zoom/pan

> **Cập nhật vòng 2** (sau khi user so trực tiếp với đối thủ — nhận định "không zoom/pan" ở bản
> đầu là ĐÁNH GIÁ SAI, đo lại kỹ hơn thấy đối thủ có 2 lớp motion rõ rệt; thay thế hoàn toàn nhận
> định cũ ngay trên):
>
> 1. **Ken Burns liên tục nhẹ** suốt mọi đoạn talking-head đang nói (không phải card tĩnh) —
>    scale ~1.0→1.02-1.04, chậm, mượt, gần như không nhận ra bằng mắt thường nhưng giữ khung
>    hình "sống".
> 2. **Punch-in zoom nhanh** tại điểm nhấn/số liệu/cuối câu (~scale 1.0→1.05 trong 0.1s rồi nhả
>    về, kèm SFX) — không lặp ở mọi câu, chỉ ở beat mạnh.
> 3. **Riêng đoạn hook mở đầu**: vòng tròn spotlight — bên trong sáng/zoom vào mặt diễn giả, bên
>    ngoài tối lại, đúng lúc câu "Mình mới phát hiện ra..." xuất hiện.
>
> Card tĩnh (Prompt/Demo/Headline) vẫn KHÔNG zoom — motion trên card vẫn đến từ chữ/nội dung
> build-in, không phải camera.

### Signature moves (nhận diện phong cách)

1. Stinger số 8-cạnh đen + SFX bump để đánh dấu chuyển tip — lặp lại mỗi lần sang tip mới.
   **Cập nhật vòng 3**: stinger dùng kiểu **PiP** (xem mục 7 dưới) — số/hình nổ nằm ở khu nội dung
   phía trên nền gradient ấm, diễn giả là 1 khối PiP nhỏ phía dưới, không đè lên nhau. (Vòng 2 từng
   thử "nền burst bán trong suốt để mặt lấp ló qua" — **đã bỏ**, vì số vẫn nằm đúng vị trí mặt.)
   **Cập nhật vòng 4** — lỗi dựng thực tế: số và hình nổ PHẢI lồng vào nhau (số là con của hình
   nổ, hình nổ tự căn giữa số bên trong) — nếu để 2 phần tử tách riêng, mỗi phần tử tự tính vị trí
   riêng và số sẽ bị lệch/lẹm lên mép hình nổ, không nằm giữa.
2. Prompt Card với karaoke word-highlight, đúng khớp giây với VO đọc nguyên văn (xem mục Chữ).
3. Gạch đỏ 1 từ + chữ mới nối ngay sau, dùng riêng cho beat "sửa/tinh chỉnh prompt".
4. Demo Screenshot luôn có mũi tên tay vẽ + label input/output + 1 khối tô ĐỎ ĐẶC (không phải khung viền) lên đúng đoạn kết quả quan trọng nhất — tạo hiệu ứng "được bật mí".
5. Recap Badge — số lượng mục = số tip trong video, và mỗi mục phải có NỘI DUNG TÓM TẮT thật của
   tip đó (không chỉ nhãn "PROMPT 1/2/3" trống).
6. Có Ken Burns liên tục + punch-in zoom tại điểm nhấn (xem mục Zoom/pan) — không còn "camera tĩnh tuyệt đối".
7. **2 kiểu xử lý khi cần hiện thêm nội dung cùng lúc với diễn giả** (cập nhật vòng 3 — thay hẳn
   khái niệm "split-card băng trên/băng dưới theo %" của vòng 2, vì cách chia % mù dễ lẹm vào đầu
   diễn giả và bỏ trống nội dung khi ước lượng sai):
   - **Kiểu A — Headroom accent**: dùng khi nội dung NHẸ (kicker/tên/chức danh 1 dòng, icon nhỏ,
     title hook...). Diễn giả giữ NGUYÊN cỡ đầy khung, không thu nhỏ. Nội dung chỉ đặt trong
     vùng đầu trống phía trên đầu diễn giả (y từ 0 đến ~40% khung — mặt đo mẫu bắt đầu ở y≈43%,
     luôn còn khoảng trống này phía trên). Ví dụ: B-roll uy tín/trích dẫn chuyên gia (tên+chức
     danh) dùng kiểu này thay vì chia nửa màn hình.
   - **Kiểu B — PiP**: dùng khi nội dung NẶNG hơn mức headroom chứa được (Prompt Card, Demo
     Screenshot, Recap, Stinger). Nội dung chiếm phần lớn khung trên nền gradient ấm; diễn giả
     hiện trong **1 khung PiP hình TRÒN, kích thước/vị trí cố định**, đặt gọn vào phần trống còn
     lại (thường ở dưới). **Cập nhật vòng 4**: PiP là **video riêng, crop/zoom TÙY CHỌN** (không
     cần giữ y nguyên góc quay/tỉ lệ khung gốc như vòng 3 từng làm — vòng 3 giữ tỉ lệ gốc 9:16 ra
     hình chữ nhật dọc, to, bị chê "khó chịu") — chỉ cần lấy gọn phần ĐẦU diễn giả (không cần cả
     tay/cả ngực), zoom riêng vào đúng vùng mặt. Chuyển cảnh giữa Kiểu A ↔ Kiểu B là **crossfade
     mờ dần** (không phải "thu nhỏ" morph) — xem chi tiết kỹ thuật ở mục 6.
8. **An toàn vùng mặt — không có ngoại lệ**: không overlay/text/graphic NÀO được chạm vào vùng mặt
   diễn giả (đo mẫu khung 1080×1920: x 38–62%, y 43–65%) khi diễn giả đang hiện ở cỡ đầy khung —
   áp dụng cho MỌI graphic kể cả số stinger/hình nổ. Nếu nội dung cần nhiều chỗ hơn vùng đầu trống
   cho phép → chuyển sang Kiểu B (thu nhỏ diễn giả) trước, không cố nhồi đè lên mặt.

---

## 2. Input yêu cầu

Khi user gọi skill này, cần:

1. **File voice-over** (`.mp3`/`.wav`) — bắt buộc.
2. **Transcript** — bắt buộc. Chấp nhận 2 dạng:
   - Có timestamp theo câu/từ (json/srt/vtt) → dùng thẳng, chính xác nhất.
   - Chỉ có text thuần → tự ước lượng thời điểm bằng cách chia đều theo
     `ffprobe` duration của file audio và tốc độ đọc tiếng Việt trung bình
     (~2.2–2.8 âm tiết/giây cho voice tự nhiên, chậm hơn ở các câu prompt được đọc chậm/nhấn).
     Luôn nói rõ trong blueprint là mốc giờ ở dạng **ước lượng**, không phải đo thật.

Nếu thiếu 1 trong 2 (không có audio, hoặc không có transcript) → hỏi lại user, không tự đoán nội dung lời.

Trước khi lên blueprint, đo `ffprobe -show_entries format=duration` trên file audio để có tổng thời lượng chính xác — đây là khung để chia hook/thân/outro theo đúng tỉ lệ ở mục 1 (12% / 82% / 6%, có thể lệch nếu số tip khác 3).

---

## 3. Thuật toán tạo blueprint (map transcript → scene)

1. **Tách hook**: ~8–12% thời lượng đầu, hoặc đến câu đầu tiên đọc xong ý mở bài (dạng "mình mới
   phát hiện/mình học được...").
2. **Tìm số tip**: quét transcript tìm marker liệt kê — số thứ tự ("câu 1/2/3", "đầu tiên/tiếp
   theo/cuối cùng"), hoặc ranh giới ý rõ ràng nếu không có marker. Số tip quyết định số vòng
   tip-cycle và số pill trong Recap Badge.
3. **Với mỗi tip, map câu nói → scene** theo mục 2 (bảng dưới):

   | Câu VO chứa | → Scene |
   |---|---|
   | Trích nguyên văn 1 câu lệnh/prompt (thường có dấu ngoặc kép hoặc "hãy...") | Prompt Card, typewriter khớp đúng khoảng VO đọc câu đó |
   | "sửa từ", "đổi thành", "gắt hơn", "thách thức nhé" | Sửa từ khoá (gạch đỏ + nối chữ mới), chèn ngay sau Prompt Card liên quan |
   | "kết quả ra...", "AI trả lời...", "nó sẽ..." | Demo Screenshot, input/output + khoanh đỏ đúng câu được nhắc |
   | Câu chốt lợi ích ngắn (1 câu, giọng nhấn) | Headline Payoff Card |
   | Nhắc tên/trích dẫn người khác, "chuyên gia", "mình học được từ..." | B-roll uy tín (stock/interview) |
   | Đùa, ví von hài | Sticker/meme |
   | "kết hợp cả...", "một lúc luôn", tóm N tip | Recap Badge, N pill |
   | Cuối bài: "follow", "theo dõi", "để không bỏ lỡ" | Outro — chỉ talking head, không graphic thêm |

4. **Chuyển tip → chèn stinger số** đúng ranh giới, độ dài 0.3–0.6s, kèm ghi chú SFX bump.
5. **Không chèn cut nào ngắn hơn ~1s trong thân bài** trừ hook và stinger — style này không giật
   liên tục, card/screenshot cần đủ thời gian cho VO đọc hết.
6. Nếu transcript KHÔNG có nhịp 3-tip rõ ràng (vd. video kể chuyện, không phải dạng "N mẹo") —
   báo cho user rằng style này thiết kế cho nội dung dạng liệt kê N-tip, và hỏi có muốn ép cấu
   trúc hook/thân/outro không kèm tip-cycle lặp, hay dùng nguyên khối 1 tip-cycle duy nhất cho
   toàn thân bài.

---

## 4. Output — cấu trúc cố định (luôn xuất đủ 6 phần, đúng thứ tự)

### A. Timeline chi tiết theo giây

Bảng, mỗi dòng là 1 beat (không phải mỗi giây, mỗi BEAT — nhiều giây/beat khi card đang giữ hình):

`| Bắt đầu–Kết thúc | Scene | Lời VO (câu/cụm) | Text overlay | Ghi chú nhạc/SFX |`

### B. Danh sách cut points

`| Giây | Loại cut (hard cut / stinger số / vào-ra card) | Từ scene → scene |` — liệt kê đủ, kể cả
cut trong hook (dày) và cut trong thân (thưa hơn, gắn với card/screenshot).

### C. Prompt B-roll cần tìm/generate

Với mỗi B-roll uy tín / stock AI / meme cần trong timeline: câu prompt cụ thể để tìm trên
stock site hoặc để generate ảnh AI (mô tả nội dung, tông màu cam/kem, tỉ lệ 9:16), gắn kèm
timestamp sẽ dùng.

### D. Text overlay script

Với mỗi overlay (Prompt Card, Headline, label input/output, caption...): nội dung chữ chính xác,
thời điểm bắt đầu/kết thúc, và style-token áp dụng (tham chiếu bảng màu/chữ ở mục 1 — không lặp
lại toàn bộ spec, chỉ ghi tên token, vd. "nền `#FCF3E1`, label cam `#FF9248`").

- **Karaoke cho Prompt Card**: ghi rõ nguyên câu + timestamp bắt đầu MỖI TỪ (lấy từ transcript
  word-level nếu có; nếu chỉ có transcript câu, ước lượng đều theo số âm tiết) — không chỉ ghi
  timestamp bắt đầu/kết thúc cả câu.
- **Chọn Kiểu A hay Kiểu B** cho mỗi overlay xuất hiện lúc diễn giả đang hiện (xem mục "Signature
  moves" #7): nội dung nhẹ ghi rõ "Kiểu A — headroom, không thu nhỏ diễn giả"; nội dung nặng ghi
  rõ "Kiểu B — PiP hình tròn, chỉ lấy phần đầu, đặt ở góc/dưới". Không còn phương án "để trống nửa
  còn lại" hay "chia % mù" — luôn chọn 1 trong 2 kiểu trên, không có lựa chọn thứ 3.

### E. Gợi ý nhạc + SFX + màu

- Nhạc: thể loại/tempo/mood đề xuất (dựa theo mood transcript), mốc giờ nên bắt đầu/kết
  (thường là 0s → hết video, không tắt).
- SFX: bảng cue theo timestamp — **whoosh** tại: hook (đúng lúc spotlight zoom vào mặt) + mỗi
  lần stinger số xuất hiện; **pop/ding** tại: 4-5 điểm nhấn mạnh nhất trong bài (số liệu, câu
  kết, câu chốt mạnh) — không cần SFX ở MỌI punch-in zoom, chỉ những điểm mạnh nhất, tránh ồn.
  Nếu dựng tay CapCut: dùng preset "Zoom" (phần Nhấn/Emphasis) kèm SFX có sẵn trong thư viện app
  cho đúng 2 loại cue trên.
- Màu: nhắc lại đúng các hex ở mục 1 áp cho video mới, cảnh báo nếu transcript gợi ý màu thương
  hiệu khác (khi đó hỏi user có muốn giữ palette gốc hay đổi theo brand riêng).

### F. Checklist QC cuối

Chạy checklist ở mục 5 và in kết quả (đạt/chưa đạt từng mục) kèm blueprint.

---

## 5. Checklist QC (chạy trước khi giao blueprint cho user)

```
[ ] 1. Tổng thời lượng timeline (A) khớp đúng duration thật của file audio (ffprobe)
[ ] 2. Hook chiếm ~10–15% tổng thời lượng, có avatar/title stack + stinger "1" ở cuối hook
[ ] 3. Mỗi tip đều có đủ: dẫn (talking head) → Prompt Card → (sửa từ khoá nếu VO có) →
       Demo Screenshot → payoff/meme/uy tín → talking head bắc cầu → stinger số
[ ] 4. Số pill trong Recap Badge == số tip đã tách ở bước 2 thuật toán
[ ] 5. Không có Prompt Card nào giữ hình ngắn hơn thời gian VO đọc hết câu prompt tương ứng
[ ] 6. Mọi timestamp trong (A) và (B) khớp nhau (không lệch giây giữa 2 bảng)
[ ] 7. Text overlay script (D) không có nội dung chữ nào bị cắt/thiếu so với transcript gốc
[ ] 8. Màu/hex dùng trong (E) đúng bảng gốc ở mục 1, trừ khi user đã yêu cầu đổi palette
[ ] 9. Outro chỉ có talking head, không chèn thêm card/graphic nào (áp dụng cho blueprint CapCut
       theo đúng video mẫu; khi BUILD bằng HyperFrames, user có thể yêu cầu thêm 1 badge CTA follow
       nhẹ — xem "build note" riêng ở mục 6, không tính là vi phạm mục này)
[ ] 10. Nếu transcript không khớp cấu trúc N-tip → đã hỏi/ghi rõ cách xử lý, không tự bỏ qua
[ ] 11. Không overlay/text/graphic nào (kể cả số stinger) nằm trên vùng mặt diễn giả (x38–62%, y43–65%) khi diễn giả đang hiện đầy khung — không ngoại lệ
[ ] 12. Card nội dung nhẹ dùng Kiểu A (headroom accent, giữ nguyên cỡ diễn giả); card nội dung nặng (Prompt/Demo/Recap/Stinger) dùng Kiểu B (PiP hình tròn) — không còn full-takeover che hết khung, và không dùng cách chia % mù kiểu vòng 2
[ ] 13. PiP (Kiểu B) là hình TRÒN, kích thước/vị trí cố định, chỉ lấy gọn phần đầu diễn giả (không cần cả tay/ngực, không cần giữ y nguyên tỉ lệ khung gốc) — không phải hình chữ nhật dọc to
[ ] 14. Số/hình nổ ở Stinger phải LỒNG vào nhau (số là con của hình nổ) — không để 2 phần tử tách riêng, dễ lệch tâm
[ ] 15. Chuyển cảnh giữa Kiểu A ↔ Kiểu B là crossfade mờ dần, ≥0.4s, không giật — không phải "thu nhỏ/phóng to" morph nhanh
```

---

## 6. Ghi chú khi build trực tiếp bằng HyperFrames

Áp dụng khi skill này được dùng để BUILD composition thật (không chỉ xuất blueprint CapCut) —
tóm tắt các kỹ thuật đã kiểm chứng qua thực tế dựng + so sánh đối thủ vòng 2, để lần build sau
không lặp lại đúng các lỗi đã gặp.

**Kiến trúc camera — lồng 2 lớp trong `#video-wrap`:**
```
#video-wrap (opacity toggle ẩn/hiện — giữ nguyên vai trò cũ)
  └ #cam (Ken Burns liên tục, scale chậm, origin 50%/50%)
      └ #cam-punch (punch-in nhanh tại điểm nhấn; origin đổi tạm 50%/53% ở hook để zoom vào mặt)
          └ <video>
```
Tách 2 lớp để không bao giờ có 2 tween `scale` chồng nhau trên CÙNG 1 phần tử ở CÙNG 1 lúc (Ken
Burns liên tục + punch nhanh chạy đồng thời nhưng trên 2 phần tử khác nhau).

**Luật allowlist — KHÔNG BAO GIỜ vi phạm** (lint `gsap_non_transform_motion`): chỉ tween
`opacity, x, y, scale, rotation, color, backgroundColor, borderRadius`. **Tuyệt đối không tween
`width/height/top/left`** để "thu nhỏ/PiP" — dù tài liệu mẫu của skill `talking-head-recut` có
làm vậy, đây là pattern sai/lỗi thời theo phần còn lại của hệ skill HyperFrames.

**Kiểu A — Headroom accent (nội dung nhẹ, không thu nhỏ diễn giả):** `#video-wrap` giữ nguyên
opacity:1/scale:1 bình thường (như lúc thuần talking-head). Card overlay chỉ có `background:
transparent` trên toàn bộ `.root`, nội dung đặt bằng `padding-top`/`align-items:flex-start` để
nằm gọn trong y 0–~40% (dùng đúng logic đã áp cho `hook-title`/`stat-x10` từ vòng 1). KHÔNG dùng
cho nội dung dài hơn ~350-400px cao — vượt mức đó phải chuyển sang Kiểu B.

**Kiểu B — PiP (nội dung nặng)** — đã đổi kiến trúc 2 lần:
- Vòng 2: "split-card chia % băng trên/dưới" → bỏ (lẹm đầu, cách chia mù).
- Vòng 3: "morph `#video-wrap` (scale+x+y+borderRadius) giữ nguyên tỉ lệ gốc" → bỏ (user chê PiP
  ra hình chữ nhật dọc "to, khó chịu"; chuyển cảnh morph nhiều thuộc tính cùng lúc cũng bị giật).
- **Vòng 4 (hiện tại) — video PiP RIÊNG, khung tròn cố định, crossfade:**

```html
<div id="pip-mask">           <!-- khung TRÒN cố định — width=height=border-radius:50%, KHÔNG bao giờ animate kích thước/vị trí -->
  <div id="pip-cam">          <!-- zoom/pan riêng, canh vào vùng mặt — không cần khớp góc quay gốc -->
    <video id="pip-video" src="assets/input-video.mp4" muted playsinline data-start="0" data-duration="…" data-track-index="2"></video>
  </div>
</div>
```
```css
#pip-mask{position:absolute;left:50%;bottom:260px;width:460px;height:460px;margin-left:-230px;
  border-radius:50%;overflow:hidden;opacity:0;z-index:5; /* z-index TĨNH, không cần đổi động nữa */
  box-shadow:0 24px 60px rgba(0,0,0,.4),0 0 0 12px #FCF3E1;}
#pip-cam{position:absolute;inset:0;}
#pip-cam video{width:100%;height:100%;object-fit:cover;}
```
`#pip-cam` chỉ cần 1 `scale` tĩnh (không animate) để crop gọn vùng đầu (bỏ tay/ngực) —
**không cần giữ đúng góc/tỉ lệ khung quay gốc**, vì đây là video độc lập, được phép crop khác
miễn lấy đúng mặt. Vì `#pip-mask` là khung VUÔNG cố định + `border-radius:50%`, luôn ra hình
TRÒN thật — khác vòng 3 (scale nguyên khung 1080×1920 portrait → dù bo góc vẫn ra chữ nhật/
oval, không thể ra tròn thật nếu không tách video riêng như thế này).

**Số `scale`/`transform-origin` chính xác KHÔNG được hardcode — phải đo lại cho MỖI video mới
(Cập nhật vòng 5):** mỗi video quay ở khoảng cách/góc/chiều cao khung khác nhau sẽ cho vị trí đầu
khác nhau trong ảnh, nên một cặp số cố định (vd. scale 1.9, origin 50%/40%) chỉ đúng cho ĐÚNG cái
video đã đo ra nó — dùng lại y nguyên cho video khác dễ ra kết quả "trống phía trên đầu, cằm/cổ
sát viền" hoặc ngược lại. Quy trình hiệu chỉnh (chạy lại mỗi khi có video nguồn mới):

1. Trích 1–2 khung hình đại diện lúc diễn giả đang nói bình thường từ video nguồn (`ffmpeg -ss <t>
   -i input.mp4 -frames:v 1 ... frame.png`) — chỉ đọc, không sửa gì.
2. Đo trên khung hình GỐC (lưới % qua `ffmpeg -vf drawgrid=w=iw:h=ih/20` hoặc ước lượng mắt) 2 mốc:
   **đỉnh tóc** (hairline) và **đáy cằm** (chin), tính theo % chiều cao khung hình gốc.
3. Cộng biên thở: phía trên đỉnh tóc trừ thêm ~3–5%, phía dưới cằm cộng thêm ~8–12% (chừa cổ/vai)
   → ra khoảng hiển thị mong muốn `[top%, bottom%]` (tính theo % chiều cao khung gốc).
4. Áp công thức (tổng quát theo tỉ lệ `W/H` thật của video nguồn — không riêng gì 1080×1920, vì
   `object-fit:cover` vào khung PiP vuông luôn cắt theo đúng logic này bất kể độ phân giải):
   ```
   band            = W / H                     // vd video dọc 1080×1920 → band = 0.5625
   band_bắt_đầu    = 0.5 − band / 2
   box_low         = (top%    − band_bắt_đầu) / band
   box_high        = (bottom% − band_bắt_đầu) / band
   scale           = 1 / (box_high − box_low)
   transform-origin(%) = box_low × scale / (scale − 1)
   ```
5. **Crop thử bằng ffmpeg** đúng hình vuông tương ứng (`crop=<w>:<w>:<x>:<y>` suy từ scale/origin ở
   bước 4, rồi `scale=460:460` để xem đúng kích cỡ PiP thật) và XEM LẠI BẰNG MẮT trước khi đưa số
   vào code — không tin công thức một cách máy móc, chỉnh tay thêm nếu khung nhìn chưa cân.
6. Gán `scale` và `transform-origin` (theo `%` trục Y, trục X giữ `50%`) vào `#pip-cam` của
   video đó trong `index.html`. Số này KHÔNG copy sang project/video khác — lặp lại bước 1–5.

*Ví dụ đã tính cho video hiện tại của project này* (nguồn 1080×1920, hairline đo được ~40%, chin
~59–60%, cộng biên → khoảng hiển thị mục tiêu ~37%–69%): `scale: 1.76; transform-origin: 50% 62%;`
— đây là KẾT QUẢ của quy trình trên cho một video cụ thể, không phải giá trị mặc định.

**Chuyển cảnh Kiểu A ↔ Kiểu B = crossfade đơn giản, không phải morph:**
```js
function toPip(t, d) { // d ~0.45s, ease êm (sine/power1), KHÔNG dùng ease giật (power2/back) ở đây
  tl.to("#video-wrap", { opacity: 0, duration: d, ease: "sine.inOut" }, t);
  tl.to("#pip-mask",   { opacity: 1, duration: d, ease: "sine.inOut" }, t);
}
function toFull(t, d) {
  tl.to("#video-wrap", { opacity: 1, duration: d, ease: "sine.inOut" }, t);
  tl.to("#pip-mask",   { opacity: 0, duration: d, ease: "sine.inOut" }, t);
}
```
Vì `#pip-mask` không đổi kích thước/vị trí bao giờ (chỉ đổi `opacity`), chuyển cảnh luôn êm — không
còn hiện tượng "nhảy" kích thước như cách morph 1 phần tử ở vòng 3. `#video-wrap` (video chính,
đầy khung) quay lại đơn giản: chỉ toggle `opacity`, không cần `scale/x/y/borderRadius` gì nữa.

Stinger dùng Kiểu B giống các card khác: số/hình nổ ở khu nội dung phía trên (nền gradient ấm),
PiP tròn diễn giả ở dưới. **Số PHẢI là con của hình nổ** (hình nổ `display:flex;align-items:
center;justify-content:center` để tự căn giữa số bên trong) — để 2 phần tử `position:absolute`
tách riêng sẽ khiến "vị trí tĩnh" của mỗi phần tử tính độc lập, số dễ bị lệch/lẹm lên mép hình nổ.

**Canh giữa nội dung Kiểu B — không neo cứng lên trên (Cập nhật vòng 5):** lỗi thực tế gặp phải —
`.prompt-root`/`.demo-root`/`.recap-root` dùng `padding-top` cố định + `justify-content:
flex-start`, nội dung dồn hết lên sát trên trong khi PiP neo cố định ở dưới → khoảng trống lớn ở
giữa khung, nhìn mất cân đối bất kể nội dung dài ngắn. Sửa: đổi cả 3 sang `justify-content:
center` và dùng padding để CHỪA vùng PiP ra khỏi phép canh giữa, thay vì chừa bằng padding-top:
```css
.prompt-root, .demo-root, .recap-root {
  justify-content: center;         /* thay flex-start */
  padding: 200px <trái/phải như cũ> 780px;  /* 780px ≈ khoảng cách từ đáy khung tới mép trên
                                                #pip-mask (bottom:260px + height:460px) + biên thở
                                                ~60px — nội dung tự canh giữa trong phần khung
                                                CÒN LẠI phía trên PiP, không tràn xuống đè PiP */
}
```
(`.demo-root` gộp luôn padding-top của `.demo-top` cũ vào đây, `.demo-top` chỉ giữ padding ngang.)
780px này đi cùng với kích thước/vị trí `#pip-mask` (460px, bottom:260px) ở trên — nếu đổi kích
thước/vị trí PiP thì phải tính lại padding-bottom tương ứng (khác với mục crop PiP ở trên, số
780px này là hình học khung 1080×1920 + layout PiP cố định của kênh, không phụ thuộc video/góc
quay, nên KHÔNG cần đo lại mỗi video — chỉ đổi nếu tự thay đổi kích thước/vị trí PiP).

**An toàn vùng trên cho Facebook Reels/TikTok (Cập nhật vòng 5):** khi đăng lên các nền tảng này,
thanh tìm kiếm/icon UI của app che mất phần trên cùng màn hình — không đặt nội dung nào cao hơn
**200px** tính từ mép trên khung (trên khung 1080×1920). Áp dụng `padding-top: 200px` (hoặc
tương đương) cho MỌI root có nội dung neo trên: `.hook-root`, `.cite-root`, `.stinger-root`, và
giá trị 200px ở khối canh-giữa phía trên cũng chính là mốc an toàn này — dùng chung 1 hằng số
cho cả bài để dễ nhớ, không cần tính riêng từng card.

**CTA follow ở outro — build note riêng cho video, KHÔNG phải Style DNA gốc (Cập nhật vòng 5):**
video mẫu gốc đo ở mục 1 có outro chỉ thuần talking-head, không graphic (checklist mục 5 #9 vẫn
đúng cho blueprint CapCut chuẩn phong cách). Nhưng khi user tự yêu cầu thêm hiệu ứng cho câu CTA
follow của VIDEO CỦA HỌ, đây là lựa chọn build-cụ-thể được phép thêm, không sửa lại số đo gốc ở
mục 1: 1 badge nhỏ **Kiểu A** (headroom, không thu nhỏ diễn giả) — pill nền cam `var(--orange)`
giống `.stat-pill` đã dùng ở hook (tái dùng ngôn ngữ hình ảnh sẵn có, không bịa màu/hình mới), có
icon (chuông/"+follow") + chữ ngắn (vd "THEO DÕI NGAY"), `padding-top` theo mốc an toàn 200px ở
trên (dùng ~220px như `.stat-root` cho cùng nhịp thị giác). Timing: xuất hiện đúng lúc VO nói tới
câu follow trong outro, giữ đến hết video. Vào khung bằng bounce `back.out` giống `.stat-pill`,
sau đó lặp 1 nhịp phập phồng nhẹ (`scale` 1↔1.04, `sine.inOut`, lặp) trong lúc giữ hình — tránh
"đứng hình" nếu card giữ quá 1–2s (đối chiếu quy tắc `sweep_static` của `hyperframes check`: một
card giữ nguyên trạng thái tĩnh nhiều giây liền có thể bị lint coi là composition không có motion).
Chỉ thêm card này khi transcript video CÓ câu CTA follow rõ ràng — không tự ý thêm nếu outro mẫu
gốc không có, và không áp dụng ngược lại vào checklist mục 5 (blueprint CapCut vẫn theo đúng #9).

**Karaoke word-span (sửa luôn lỗi xuống dòng giữa từ)**: KHÔNG bọc từng KÝ TỰ (`<span class="char">`
không có khoảng trắng giữa 2 span khiến trình duyệt được phép ngắt dòng giữa 2 ký tự bất kỳ — đây
là nguyên nhân lỗi "chữ xuống dòng sai cú pháp giữa từ"). Bọc từng TỪ (`<span class="w">từ</span>`)
với khoảng trắng THẬT (text node) giữa các span — từ luôn nguyên khối, không thể vỡ giữa dòng.
Toàn câu hiện mờ từ đầu; tại đúng thời điểm mỗi từ theo transcript, `tl.set()` (không cần tween)
đổi class từ đó sang trạng thái sáng, đồng thời trả từ trước về trạng thái mờ — O(n) theo số từ,
không lặp N² lần.

**SFX**: dùng thư viện local có sẵn của skill `media-use` (`resolve --type sfx --intent "whoosh"`
/ `"pop"`) — hoàn toàn offline, không cần mạng/tài khoản/xin phép tải, khác với `resolve --type
video` (có phí, cần xác nhận từng lần). File `<audio>` resolve xong PHẢI có `id` riêng (lint
`media_missing_id` — thiếu id thì audio render ra SILENT, không lỗi rõ ràng nào khác báo trước).

**Nhạc nền (BGM) — đừng quên** (phát hiện qua 1 vòng review đối kháng: cả 3 project dựng theo
skill này đến giờ đều THIẾU nhạc nền dù mục 1/mục E yêu cầu nhạc chạy liên tục toàn video): trước
khi coi 1 bản build là "xong", tự hỏi đã có `<audio>` cho nhạc nền chưa. Thêm nhạc cần hỏi ý user
trước khi làm (không tự ý chọn) vì cả 2 cách đều cần quyết định của họ — xem `media-use/audio/
references/bgm.md` mục Preflight: lấy từ thư viện HeyGen (cần đăng nhập) hoặc generate cục bộ
(cần `GEMINI_API_KEY`/`GOOGLE_API_KEY` cho Lyria, hoặc tải model MusicGen ~300MB). Không tự ý chọn
1 trong 2 cách rồi làm luôn.

**Bốn bài học kỹ thuật rút ra khi build thực tế nhiều video khác nhau cùng skill này (Cập nhật
vòng 6)** — áp dụng cho MỌI video dùng skill này, không riêng video nào:

1. **Caption đáy KHÔNG được chạy song song với 1 card Kiểu B (full-bleed) đang hiện.** Card Kiểu B
   (nền kem/gradient phủ toàn khung) tự nó đã đóng vai trò "caption" lúc đó — chạy thêm caption
   đáy đè lên vừa dư thừa thị giác, vừa có nguy cơ FAIL contrast check thật (chữ trắng viền đen
   mỏng trên nền kem sáng dễ dưới 3:1 ở 1 số khung hình cụ thể, khác hẳn khi caption nằm trên nền
   video tự nhiên). Chỉ bật caption đáy lúc: talking-head thuần (không card), hoặc Kiểu A (nền
   trong suốt, video chính vẫn hiện phía sau). Tắt hẳn caption trong toàn bộ khoảng active của bất
   kỳ card Kiểu B nào.
2. **Ken Burns nhiều đoạn phải là 1 CHUỖI LIÊN TỤC — dùng `tl.to()`, không dùng `tl.fromTo(scale:
   1.0 → target)` lặp lại cho từng đoạn.** Nếu chia Ken Burns thành nhiều "cửa sổ" thời gian (đổi
   tốc độ zoom theo từng đoạn nội dung), mỗi đoạn phải kế thừa giá trị hiện tại bằng `tl.to(el,
   {scale: target, duration, ease}, t)` — dùng `fromTo` sẽ ép scale nhảy về đúng 1.0 ở đầu MỖI
   đoạn bất kể đoạn trước đã zoom tới đâu, tạo 1 khung giật ngược đúng tại ranh giới 2 đoạn.
3. **Mọi `.root` xếp nội dung theo chiều DỌC phải khai báo rõ `flex-direction: column`.** Base
   class `.card .root { display:flex; }` KHÔNG có `flex-direction` mặc định (tức mặc định `row`).
   Quên khai báo ở 1 class con (`.hook-root`, `.tool-root`, `.step-root`...) khiến nội dung (badge
   + nhiều dòng chữ, label + box...) xếp NGANG dính liền thay vì xếp dọc — lỗi này ĐÃ xảy ra thật
   ở nhiều project khác nhau dùng skill này (kể cả 1 video đã render và gửi cho user mà không ai
   phát hiện ra vì chỉ hiện 1 giây ở đầu hook) — `hyperframes check` KHÔNG bắt được lỗi này (đây là
   lỗi bố cục thẩm mỹ, không phải lỗi kỹ thuật). Luôn tự kiểm bằng snapshot đúng khung hình đầu
   tiên của MỖI loại card mới trước khi coi là xong, không chỉ tin lint báo 0 lỗi.
4. **Hiệu ứng camera (`#cam-punch` punch-in, Ken Burns trên `#cam`) chỉ hiển thị khi `#video-wrap`
   đang ở trạng thái HIỆN (opacity ~1).** Nếu 1 điểm nhấn (số liệu, câu chốt) rơi đúng lúc đang ở
   chế độ PIP (`#video-wrap` opacity 0), hiệu ứng trên `#cam-punch` sẽ hoàn toàn vô hình vì chạy
   trên phần tử đang ẩn — và không thể "sửa" bằng cách chuyển hiệu ứng sang `#pip-cam` vì luật PiP
   không bao giờ animate kích thước. Trước khi thêm 1 `punch()` tại mốc giờ nào, luôn đối chiếu với
   lịch `toPip`/`toFull` — nếu lúc đó đang PIP, bỏ punch đó (SFX một mình vẫn ổn, không bắt buộc
   mọi SFX phải có hiệu ứng hình kèm theo) hoặc dời điểm nhấn sang lúc video chính đang hiện.

---

## 7. Lấy demo giao diện THẬT khi kịch bản/nội dung có đoạn thao tác trên Claude

Khi transcript (hoặc kịch bản gốc từ skill `script-writer`) có đoạn dạng "gõ câu
này vào Claude, nó trả lời/hỏi lại thế này" — Demo Screenshot nên dùng ảnh THẬT
thay vì dựng giả, vì đây là nội dung cụ thể viewer có thể tự làm theo. Quy trình:

0. **Kiểm tra kho chung trước** — đọc `SON_AI_VIDEO/shared-sources/SOURCES.md`
   (manifest dùng chung cho mọi skill edit) xem đã có sẵn ảnh/asset khớp đúng
   prompt/tình huống cần demo chưa. Nếu có, dùng lại luôn, không cần thao tác
   Chrome lại từ đầu.
1. Nếu THIẾU (không có sẵn trong kho chung) — **báo cho user biết đang thiếu gì
   cụ thể và hỏi có cho phép tự thao tác lấy không**, không tự động chạy song
   song lúc đang lên blueprint. Chỉ khi user đồng ý mới dùng **Claude trong
   Chrome thật của user** (không phải browser rời trong app) để demo đúng giao
   diện/tài khoản thật họ dùng.
2. Thao tác ĐÚNG theo prompt đã có trong transcript/kịch bản — không tự ý đổi
   câu hỏi hay thử thêm nội dung ngoài phạm vi đã chốt, vì mục đích là tái tạo
   đúng cảnh sẽ lên video, không phải khám phá tự do trên tài khoản thật của họ.
   Không tự ý mở/đọc các tab hay đoạn chat khác ngoài phạm vi demo đang cần.
3. Chụp lại đủ các mốc cần cho Demo Screenshot (mục 1 bảng scene #4): trước khi
   gõ, sau khi gõ, lúc AI đang trả lời, lúc trả lời xong — đủ để chọn 1 khung
   dùng input/output + khoanh đỏ đúng đoạn kết quả then chốt.
4. **Lưu ảnh vào `SON_AI_VIDEO/shared-sources/demo-screens/`** (không chỉ vào
   `assets/` riêng của 1 project) và **tự thêm 1 dòng vào manifest
   `SOURCES.md`** (loại, dùng cho gì, ngày, skill/project nào tạo ra) — để video
   sau tái dùng được nếu hợp, không phải quay lại từ đầu mỗi lần.

Nếu user không muốn dùng Chrome thật (dữ liệu/tài khoản nhạy cảm), quay lại cách
cũ: mô tả demo bằng dựng đồ hoạ (không phải ảnh thật) như các Demo Screenshot
trước đây trong style này.

---

*Nguồn duy nhất của phong cách này: 1 video mẫu đo đạc trực tiếp bằng ffprobe/ffmpeg (scene
score, silencedetect, volumedetect, ebur128, lấy mẫu pixel). Khi có thêm video mẫu cùng kênh,
cập nhật lại bảng ở mục 1 thay vì tạo skill mới.*
