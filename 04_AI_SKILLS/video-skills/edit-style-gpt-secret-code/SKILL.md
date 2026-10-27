---
name: edit-style-gpt-secret-code
description: "Phong cách edit video talking-head 'N mã bí mật cho ChatGPT' tiếng Việt — phân tích đo đạc từ 1 video mẫu thực tế (66.7s, 9:16, ffprobe/ffmpeg/faster-whisper). Đọc khi user đưa file voice-over (mp3/wav) + transcript và muốn nhận về một EDIT BLUEPRINT (timeline theo giây, cut points, gợi ý ví dụ ChatGPT cần quay màn hình, text overlay script, gợi ý nhạc/SFX/màu, checklist QC) để tự dựng bằng CapCut — KHÔNG build ra file video hay HyperFrames composition. Trigger: '/edit-style-gpt-secret-code', hoặc câu như 'lên blueprint theo phong cách video ChatGPT secret code này'."
---

# Edit Style — "N mã bí mật cho ChatGPT" (screen-record + PiP tròn mềm)

> Nguồn: đo đạc trực tiếp trên 1 video mẫu (`FDown.vn_Tai_video_Facebook_720p (HD)_13bd.mp4`,
> 66.73s, 720×1280 @30fps, audio AAC). Phân tích bằng `ffprobe`/`ffmpeg` (scene-detect,
> silencedetect, volumedetect, ebur128, lấy mẫu pixel màu) + transcript word-level bằng
> `faster-whisper large-v3` + đọc trực tiếp khung hình — không phải suy đoán từ trí nhớ chung.
> Coi đây là **nguồn sự thật duy nhất** về phong cách; đọc toàn bộ trước khi tạo blueprint.
>
> Đây là skill **tạo blueprint để dựng tay trong CapCut**, khác với các skill HyperFrames vốn
> build ra composition/video thật. Không build file video ở đây — output cuối là 1 **văn bản
> blueprint** theo cấu trúc cố định ở dưới.
>
> Quy ước làm việc chung (gated workflow, trả lời tiếng Việt, xử lý transcript không chắc, review
> đối kháng trước khi render...) — xem `extract-edit-style/references/universal-lessons.md` phần
> B, không lặp lại chi tiết ở đây.
>
> **Xác nhận lại 2026-08-10:** user gửi lại đúng file `FDown.vn_Tai_video_Facebook_720p (HD)_13bd.mp4`
> qua `/extract-edit-style` (tưởng là video đối thủ mới). ffprobe cho ra đúng 66.731293s /
> 720×1280 / 30fps — khớp 100% số liệu đã ghi ở trên, xác nhận đây là CÙNG 1 file, không phải
> video khác. Không tạo skill trùng lặp (đúng "Bước 0" của `extract-edit-style`); số liệu trong
> skill này đã được xác nhận ổn định qua 2 lần đo.

---

## 1. Style DNA (rút ra từ video mẫu)

### Cấu trúc tổng thể & timing đo được

| Phần | Thời gian | Tỉ trọng | Đặc điểm |
|---|---|---|---|
| **Hook** | 0.00–7.7s | ~11.5% | Talking-head ĐẦY KHUNG (không PiP), tiêu đề 2 dòng đè giữa-dưới khung (trắng + xanh ngọc), nêu thẳng số lượng "N mã bí mật" + lời hứa lợi ích ("trả lời chính xác hơn gấp 10 lần"). Kết hook bằng 1 **white-flash wipe** cực nhanh (~0.3-0.5s, đo được ở scene-detect 7.17–7.73s). |
| **Thân bài (N mã, video mẫu N=5)** | 7.7–54.3s | ~70% | Lặp lại 1 khung "code-cycle" cho mỗi mã (xem mục 2). Mỗi mã: VO nêu tên mã bằng tiếng Anh + tác dụng ngắn gọn (7–15s), ĐỒNG THỜI màn hình chuyển sang **screen-recording ChatGPT thật** minh hoạ đúng tác dụng đó (mỗi mã dùng 1 VÍ DỤ CHỦ ĐỀ KHÁC NHAU — không lặp lại chủ đề). Diễn giả thu nhỏ thành **PiP tròn mềm** đè góc màn hình suốt đoạn này (không tách biệt "full ↔ PiP" theo từng card như kiểu khác — ở đây gần như toàn bộ thân bài là chế độ PiP liên tục). |
| **Cầu nối/mồi thêm** | 54.3–59.6s | ~8% | VO chốt "có hàng trăm mã hay nhưng không nói hết được trong video này" — vẫn ở chế độ screen-recording, thấp thoáng 1 danh sách mã được nhóm theo chủ đề (dạng cheatsheet) như minh hoạ "còn nhiều nữa". Kết bằng **white-flash wipe** thứ 2 (~59.4–60.2s). |
| **Outro** | 60.2–66.7s | ~10% | Trở lại talking-head ĐẦY KHUNG. CTA rõ ràng: "follow" + **"comment 1 từ khoá cụ thể"** (đo được: `CMT: "MÃ XỊN"`) để nhận danh sách đầy đủ — mạnh hơn hẳn kiểu CTA chỉ "follow" đơn thuần. |

### Code-cycle — khung lặp lại của mỗi "mã" trong thân bài

```
[VO nêu tên mã bằng tiếng Anh, vd "SeekHuman"/"ELI10"/"X10Think"/"KillCritic"/"ALT3"]
        ↓ (đồng thời, không cắt cảnh riêng — chuyển mượt ngay khi tên mã được nói)
[Screen-recording ChatGPT thật, scroll dọc 1 đoạn hội thoại VÍ DỤ]
   — chủ đề ví dụ THAY ĐỔI mỗi mã (đo được: 1 mã minh hoạ bằng bài luận nhân văn, 1 mã minh hoạ
     bằng giải thích lịch sử/khoa học kiểu ELI, 1 mã minh hoạ bằng phân tích sâu...) — chủ đề chọn
     sao cho THỂ HIỆN ĐÚNG tác dụng mã đang nói (vd mã "ELI10" đi kèm ví dụ giải thích cực dễ hiểu)
        ↓ (trong suốt đoạn này)
[Diễn giả co lại thành PiP TRÒN MỀM, góc màn hình] + [caption box bám theo câu nói]
        ↓
[VO giải thích ngắn tác dụng cụ thể của mã đó, 1-2 câu]
```
Không có "stinger số" đếm giữa các mã như kiểu khác — chuyển mã diễn ra MƯỢT trong cùng 1 đoạn
screen-recording liên tục (không cắt cứng giữa mã N và mã N+1 theo quan sát scene-detect — chỉ có
2 cut cứng thật sự trong toàn video là 2 white-flash ở đầu/cuối thân bài).

### Bảng scene

| # | Scene | Khi dùng | Hold time |
|---|---|---|---|
| 1 | **Talking-head đầy khung** | Hook + Outro | 7–8s |
| 2 | **Screen-recording ChatGPT + PiP tròn mềm** | Toàn bộ thân bài (mọi mã) | 7–15s/mã |
| 3 | **White-flash wipe** | Hook→thân, Cầu nối→outro | 0.3–0.5s |
| 4 | **Caption box tương phản thích ứng** | Xuyên suốt (trừ lúc chỉ có tiêu đề hook) | theo câu nói |

### Màu (đo pixel thật từ khung hình)

| Token | Hex đo được | Dùng cho |
|---|---|---|
| Nền tối (UI ChatGPT dark mode) | `#0D0E13` | Nền toàn màn hình lúc screen-recording |
| Xanh ngọc chính (teal, thương hiệu ChatGPT) | `#2FB8A3` (dải `#23A392`–`#3CC5B4`) | Dòng 2 tiêu đề hook, logo ChatGPT lúc mở đầu |
| Caption box TỐI (đè lên nền screen-recording tối) | `#434C53` (bán trong suốt) | Caption trong thân bài |
| Caption box SÁNG (đè lên video người thật) | `~#D8D5D5` (bán trong suốt, be/xám nhạt ấm) | Caption/CTA lúc hook + outro |
| Chữ | Trắng/gần-trắng trên box tối; đen/gần-đen trên box sáng | — |

**Signature move quan trọng nhất — caption box đổi màu tương phản theo nền phía sau** (tối+chữ
sáng trên screen-recording, sáng+chữ tối trên video người thật) — khác hẳn kiểu "1 màu caption cố
định xuyên suốt" của các phong cách khác. Chưa đo được toạ độ Y cố định cho caption box (có vẻ đặt
theo ngữ cảnh/scroll, không neo 1 mốc % như style khác) — cần quan sát thêm nếu build blueprint
cho video cụ thể.

### Chữ (typography)

| Vai trò | Style |
|---|---|
| Tiêu đề hook (2 dòng) | In hoa, đậm, dòng 1 trắng, dòng 2 xanh ngọc, giữa khung theo chiều ngang, đè lên phần ngực diễn giả (không phải góc trên như kiểu khác) |
| Caption lời nói | Bold sans, box bo góc lớn (pill/rounded-rect ôm sát chữ, KHÔNG phải thanh dài full-width), màu box+chữ tương phản thích ứng (xem trên). Cắt theo CỤM ngắn (2-5 từ) |
| CTA cuối | Cùng kiểu box với caption, chữ in hoa đậm hơn (`CMT: "MÃ XỊN"`) |

### Sound design (đo bằng ebur128/volumedetect)

- **Không có khoảng lặng thật** (`silencedetect` -30dB/0.2s: 0 khoảng lặng trong 66.7s) → nhạc nền
  (nếu có) chạy liên tục, hoặc bản thân giọng nói/ambience lấp đầy hoàn toàn.
- **Loudness**: −14.3 LUFS integrated, **LRA chỉ 2.0 LU** — mix nén/limit CHẶT HƠN CẢ style khác đã
  đo (2.0 vs 3.0 LU) — gần như không có đoạn to/nhỏ rõ rệt.
- Chưa đo riêng được SFX tại các white-flash (cần đo `volumedetect` cắt đúng đoạn 7.2–7.7s và
  59.4–60.2s nếu cần chính xác — ước lượng ban đầu là CÓ SFX bump/whoosh đi kèm flash, dựa theo quy
  luật chung của thể loại, nhưng CHƯA XÁC NHẬN bằng số đo).

### Zoom/pan

**Chưa xác nhận rõ** — không đủ dữ liệu để kết luận có Ken Burns/punch-in hay không (khác với
`edit-style-nns`, nơi từng kết luận sai "không có" rồi phải đo lại — ở đây CHỦ ĐỘNG NHẬN LÀ
CHƯA ĐO thay vì đoán). Nếu dùng skill này để build/blueprint 1 video cụ thể, kiểm tra thêm bằng
cách xem liên tiếp nhiều khung ở đoạn hook/outro (lúc talking-head đầy khung, dễ quan sát zoom hơn
lúc đang PiP nhỏ).

### Signature moves (nhận diện phong cách)

1. **PiP tròn MỀM (feathered/soft mask), không phải viền cứng** — khác hẳn kiểu viền kem dày cứng
   của style khác. Vị trí lệch góc (không cố định giữa-dưới), CHE MỘT PHẦN nội dung screen-recording
   phía sau (không né chữ) — khác triết lý "không đè lên nội dung" của style khác.
2. **Video chính hầu như luôn ở chế độ PiP nhỏ trong SUỐT thân bài** — không có nhịp "full ↔ PiP"
   qua lại nhiều lần giữa các mã như kiểu tip-cycle khác; chỉ về FULL đúng 2 lần (hook, outro).
3. **White-flash wipe** đánh dấu 2 ranh giới cấu trúc lớn (hook→thân, thân→outro) — không dùng
   crossfade mờ dần hay stinger số như các phong cách khác.
4. **Mỗi mã minh hoạ bằng 1 VÍ DỤ CHỦ ĐỀ THẬT KHÁC NHAU, không lặp chủ đề** — đây là điểm khác biệt
   LỚN NHẤT so với style dùng card mockup: cần NGUỒN THẬT (ảnh chụp/quay màn hình ChatGPT thật) cho
   mỗi ví dụ, không tự vẽ card giả lập.
5. **Caption box tương phản thích ứng theo nền** (xem mục màu ở trên).
6. **CTA cuối là "comment 1 từ khoá cụ thể"**, không chỉ "follow" suông — bẫy tương tác rõ ràng hơn.
7. **An toàn vùng mặt**: CHƯA đo % chính xác cho style này (khác `edit-style-nns` đã có số đo
   x38-62%/y43-65%) — vì ở đây diễn giả hiếm khi ở cỡ đầy khung TRONG LÚC có overlay khác (chỉ đầy
   khung ở hook/outro, lúc đó chỉ có tiêu đề/caption, không có overlay khác chồng lên). Nếu style
   mới cần thêm overlay khác đè lên lúc đầy khung, đo lại vùng mặt trước.

---

## 2. Input yêu cầu

Khi user gọi skill này, cần:

1. **File voice-over** (`.mp3`/`.wav`) — bắt buộc.
2. **Transcript** — bắt buộc (word-level ưu tiên, xem `edit-style-nns` mục 2 cho quy tắc ước
   lượng nếu chỉ có transcript câu).
3. **Riêng style này — THÊM 1 input đặc thù**: với MỖI "mã/tip" trong video mới, cần **1 ví dụ
   ChatGPT (hoặc công cụ AI liên quan) THẬT** để screen-record minh hoạ đúng tác dụng của mã đó —
   khác với style dùng card mockup (không cần ảnh/video thật, tự vẽ card). **Trước khi hỏi user**,
   kiểm tra `SON_AI_VIDEO/shared-sources/SOURCES.md` xem đã có sẵn ví dụ/ảnh khớp chủ đề mã đó chưa
   (mục 7). Nếu vẫn thiếu, HỎI LẠI user xem họ muốn: (a) tự chuẩn bị/quay màn hình trước rồi gửi, (b)
   cho phép tự thao tác lấy qua Chrome thật của họ (mục 7), hay (c) blueprint chỉ mô tả GỢI Ý chủ đề
   ví dụ nên dùng (để họ tự tạo), KHÔNG tự bịa nội dung "kết quả ChatGPT trả lời" giả rồi trình bày
   như thật.

Nếu thiếu audio/transcript → hỏi lại, không tự bịa nội dung lời.

---

## 3. Thuật toán tạo blueprint (map transcript → scene)

1. **Tách hook**: đến hết câu nêu số lượng mã + lời hứa lợi ích (thường 1 câu dài, ~10-12% thời
   lượng), kết bằng 1 nhịp chuyển nhanh (white-flash).
2. **Tìm số mã (N) và tên từng mã**: quét transcript tìm các từ khoá tiếng Anh viết liền/viết hoa
   xen giữa câu tiếng Việt (dấu hiệu: "mã X", "code X", đọc như 1 từ riêng biệt) + marker thứ tự
   ("đầu tiên", "thứ 2", "thứ 3", "tiếp theo", "cuối cùng"/"đó là"). N quyết định số vòng code-cycle.
3. **Với mỗi mã, xác định**:
   - Tên mã (giữ nguyên tiếng Anh/không dấu như VO đọc).
   - Tác dụng ngắn gọn (1 câu, lấy từ VO ngay sau tên mã).
   - **Gợi ý chủ đề ví dụ minh hoạ** — chọn 1 chủ đề THỂ HIỆN RÕ tác dụng đó (vd mã "giải thích dễ
     hiểu" → gợi ý chủ đề có thể gây khó hiểu nếu giải thích thường (khoa học/lịch sử phức tạp); mã
     "tư duy sâu hơn" → gợi ý 1 câu hỏi cần phân tích nhiều lớp). Ghi RÕ đây là GỢI Ý, không phải
     nội dung ChatGPT thật đã tạo ra — user cần tự chạy thử để lấy screen-recording thật.
4. **Cầu nối cuối thân bài** (nếu VO có câu kiểu "còn nhiều mã khác nhưng không nói hết được") →
   đánh dấu là 1 beat riêng trước outro, không gộp vào mã cuối.
5. **Outro**: map câu CTA — tách rõ phần "follow" và phần "comment từ khoá gì" (nếu có) thành 2
   dòng text riêng, vì đây là 2 hành động khác nhau cần cả 2 đều rõ ràng trên màn hình.
6. Nếu transcript KHÔNG có cấu trúc N-mã rõ ràng → báo cho user, hỏi có muốn ép cấu trúc này hay xử
   lý theo hướng khác (skill này thiết kế riêng cho dạng "liệt kê N từ khoá/mã ngắn kèm ví dụ thật",
   không phải mọi video ChatGPT-content đều hợp cấu trúc này).

---

## 4. Output — cấu trúc cố định (như `edit-style-nns` mục 4, đủ 6 phần A–F)

Theo đúng khuôn A (Timeline) / B (Cut points) / C (Nguồn ví dụ cần chuẩn bị — THAY vì "Prompt
B-roll", ở đây là danh sách ví dụ ChatGPT cần tự quay màn hình, kèm gợi ý chủ đề cho từng mã) / D
(Text overlay script) / E (Nhạc+SFX+màu) / F (Checklist QC) — xem cấu trúc chi tiết từng phần ở
`edit-style-nns` mục 4, chỉ đổi tên phần C cho khớp bản chất input khác biệt của style này.

---

## 5. Checklist QC (chạy trước khi giao blueprint cho user)

```
[ ] 1. Tổng thời lượng timeline khớp đúng duration thật của file audio (ffprobe)
[ ] 2. Hook ~10-12% tổng thời lượng, có tiêu đề 2 dòng + kết bằng 1 nhịp chuyển nhanh
[ ] 3. Mỗi mã đều có: tên mã (tiếng Anh) + tác dụng ngắn gọn + gợi ý chủ đề ví dụ minh hoạ rõ ràng
[ ] 4. Số ví dụ cần chuẩn bị (Part C) == số mã (N) đã tách ở bước 2 thuật toán
[ ] 5. Không tự bịa "nội dung ChatGPT trả lời" trình bày như thật — chỉ ghi GỢI Ý chủ đề
[ ] 6. Mọi timestamp trong Part A và Part B khớp nhau
[ ] 7. Text overlay không thiếu/cắt chữ so với transcript gốc
[ ] 8. Màu/hex đúng bảng mục 1, có ghi rõ 2 biến thể caption box (tối/sáng) theo đúng ngữ cảnh nền
[ ] 9. Outro có ĐỦ 2 phần CTA tách biệt: "follow" và "comment từ khoá" (nếu VO có cả 2)
[ ] 10. Nếu transcript không khớp cấu trúc N-mã → đã hỏi/ghi rõ cách xử lý, không tự bỏ qua
[ ] 11. Có ghi chú rõ: style này diễn giả PiP liên tục suốt thân bài (không phải full↔PiP xen kẽ)
```

---

## 6. Ghi chú khi build trực tiếp bằng HyperFrames

Chưa build thực tế lần nào bằng style này — phần dưới đây là kỹ thuật NỀN TẢNG dùng chung cho MỌI
skill `edit-style-*` (chép từ `extract-edit-style/references/universal-lessons.md` phần A), áp
dụng được ngay cả khi chưa build qua. Kỹ thuật ĐẶC THÙ cho style này (cách dựng PiP tròn MỀM/feathered
thay vì viền cứng, cách đổi màu caption box tự động theo nền, cách chèn screen-recording thật vào
timeline HyperFrames...) sẽ bổ sung SAU khi build thử ít nhất 1 lần thật — không bịa trước khi chưa
kiểm chứng.

**Kiến trúc camera — lồng 2 lớp trong `#video-wrap`:**
```
#video-wrap (opacity toggle ẩn/hiện)
  └ #cam (Ken Burns liên tục, scale chậm, origin 50%/50%)
      └ #cam-punch (punch-in nhanh tại điểm nhấn)
          └ <video>
```
Tách 2 lớp để không bao giờ có 2 tween `scale` chồng nhau trên CÙNG 1 phần tử ở CÙNG 1 lúc.

**Luật allowlist GSAP — KHÔNG BAO GIỜ vi phạm** (lint `gsap_non_transform_motion`): chỉ tween
`opacity, x, y, scale, rotation, color, backgroundColor, borderRadius`. Tuyệt đối không tween
`width/height/top/left` để "thu nhỏ/PiP" — đây là pattern sai/lỗi thời.

**PiP hình tròn — video RIÊNG, 2 lớp độc lập, không morph:**
```html
<div id="pip-mask">  <!-- khung TRÒN cố định: width=height=border-radius:50%, KHÔNG BAO GIỜ animate kích thước/vị trí -->
  <div id="pip-cam">  <!-- 1 scale TĨNH duy nhất, không animate -->
    <video id="pip-video" src="..." muted playsinline data-start="0" data-duration="…" data-track-index="2"></video>
  </div>
</div>
```
`#video-wrap` (video chính) và `#pip-mask` (PiP) là 2 lớp ĐỘC LẬP, chuyển cảnh giữa chúng = crossfade
opacity đơn giản (~0.4–0.5s, ease `sine.inOut`/`power1`). **Lưu ý riêng cho style này**: video mẫu
dùng white-flash wipe thay vì crossfade ở 2 ranh giới lớn — nếu build thật, cân nhắc mô phỏng
white-flash bằng 1 lớp trắng phủ toàn khung, `opacity` 0→1→0 cực nhanh (~0.15-0.2s mỗi chiều), thay
vì dùng crossfade `toPip`/`toFull` tiêu chuẩn — đây là khác biệt CHƯA kiểm chứng thực tế.

**Công thức + quy trình hiệu chỉnh scale/transform-origin cho PiP — ĐO LẠI CHO MỖI VIDEO MỚI, không
hardcode:**
1. Trích 1-2 khung hình đại diện lúc diễn giả nói bình thường (`ffmpeg -ss <t> -frames:v 1`).
2. Đo % chiều cao khung của **đỉnh tóc** và **đáy cằm** (lưới % qua `drawgrid` hoặc mắt).
3. Cộng biên thở: trên đỉnh tóc trừ ~3–5%, dưới cằm cộng ~8–12% (chừa cổ/vai) → khoảng hiển thị
   mục tiêu `[top%, bottom%]`.
4. Áp công thức (tổng quát theo tỉ lệ `W/H` thật của video nguồn):
   ```
   band = W / H;  band_start = 0.5 − band/2
   box_low = (top% − band_start) / band;  box_high = (bottom% − band_start) / band
   scale = 1 / (box_high − box_low)
   transform-origin(%) = box_low × scale / (scale − 1)
   ```
   Nếu `box_low` ra ÂM (hairline nằm trên biên cover-crop tự nhiên) → KẸP về 0, origin trở thành
   top-anchored (`transform-origin: 50% 0%`).
5. Crop thử bằng ffmpeg và XEM LẠI BẰNG MẮT trước khi đưa vào code.
6. Số này KHÔNG copy sang video/project khác — lặp lại bước 1–5 cho mỗi video mới.

**Canh giữa nội dung phía trên PiP:**
```css
.xxx-root { justify-content: center; padding: 200px <trái/phải> <bottom>px; }
```
`<bottom>` = khoảng cách từ đáy khung tới mép trên `#pip-mask` + biên thở ~40-60px. **Lưu ý riêng
cho style này**: vì PiP ở đây lệch GÓC (không phải giữa-dưới) và ĐÈ LÊN nội dung thay vì né ra, quy
tắc "canh giữa phía trên PiP" của style card-mockup có thể KHÔNG áp dụng nguyên xi — cần xem lại
khi build thật, vì bản chất layout (screen-recording toàn khung + PiP đè góc) khác hẳn layout
"card nền màu + PiP né sang 1 bên" của style khác.

**An toàn vùng trên cho Facebook Reels/TikTok:** không đặt nội dung nào cao hơn **200px** tính từ
mép trên khung. Áp dụng cho tiêu đề hook và mọi overlay neo trên.

**Caption đáy KHÔNG chạy song song với card full-bleed (Kiểu B) đang hiện** — quy tắc này có thể
cần điều chỉnh cho style này vì bản thân "card Kiểu B" ở đây CHÍNH LÀ screen-recording (không phải
nền màu đơn sắc), nên caption CÓ THỂ vẫn cần thiết trong lúc screen-recording (khác 2 style khác,
nơi card tự nó đã là "caption"). Xem lại khi build thật.

**Ken Burns nhiều đoạn = 1 chuỗi LIÊN TỤC, dùng `tl.to()` không dùng `tl.fromTo(scale:1.0→target)`
lặp lại từng đoạn** — `fromTo` ép giá trị nhảy về đúng 1.0 ở đầu MỖI đoạn, tạo giật ngược tại ranh
giới. `to()` kế thừa giá trị hiện tại, chuỗi mượt.

**Mọi `.root` xếp nội dung theo chiều DỌC phải khai báo rõ `flex-direction: column`** — base class
`display:flex` không có `flex-direction` mặc định (tức `row`). Lint KHÔNG bắt được lỗi này — luôn
tự kiểm bằng snapshot khung hình đầu tiên của MỖI loại card mới.

**Hiệu ứng camera (`#cam-punch`, Ken Burns trên `#cam`) chỉ hiển thị khi `#video-wrap` đang HIỆN
(opacity ~1).** Đối chiếu lịch `toPip`/`toFull` trước khi thêm punch tại 1 mốc giờ — với style này,
`#video-wrap` gần như LUÔN ẩn trong thân bài (PiP liên tục), nên punch-in trên video chính chỉ có ý
nghĩa ở hook/outro.

**Nhạc nền (BGM):** trước khi coi 1 bản build là "xong", tự hỏi đã có `<audio>` nhạc nền chưa. Thêm
BGM cần hỏi ý user trước — xem `media-use/audio/references/bgm.md` mục Preflight.

**Trước khi render, luôn:** `npx hyperframes check` (0 lỗi) + snapshot vài khoảnh khắc chính rồi
XEM BẰNG MẮT.

---

## 7. Lấy ví dụ ChatGPT THẬT khi thiếu (screen-recording)

Style này CẦN nguồn thật cho mỗi mã (mục 2 điểm 3) — ưu tiên dùng kho chung trước
khi tự thao tác:

0. Đọc `SON_AI_VIDEO/shared-sources/SOURCES.md` — nếu đã có ảnh/luồng khớp đúng
   chủ đề ví dụ cần cho mã đang xử lý, dùng lại luôn.
1. Nếu thiếu — báo cho user đang thiếu ví dụ cho mã nào/chủ đề gì cụ thể, hỏi có
   cho phép tự thao tác lấy không. Không tự chạy song song lúc đang lên blueprint.
2. Nếu user đồng ý: dùng **Claude/ChatGPT trong Chrome thật của user**, thao tác
   ĐÚNG theo chủ đề ví dụ đã chốt cho mã đó (không tự đổi chủ đề, không tự ý mở
   tab/đoạn chat khác ngoài phạm vi cần).
3. Chụp/ghi lại đủ đoạn hội thoại cần scroll qua (đúng bản chất "screen-recording
   ChatGPT thật" của style này, không chỉ 1 ảnh tĩnh).
4. Lưu vào `SON_AI_VIDEO/shared-sources/demo-screens/` và thêm 1 dòng vào
   `SOURCES.md` (chủ đề, mã nào dùng, ngày, project nào tạo ra).

Nếu user không muốn dùng Chrome thật, quay lại cách (c) ở mục 2: blueprint chỉ
ghi GỢI Ý chủ đề, không tự bịa nội dung ChatGPT trả lời.

---

*Nguồn duy nhất của phong cách này: 1 video mẫu đo đạc trực tiếp bằng ffprobe/ffmpeg/faster-whisper
(scene score, silencedetect, volumedetect, ebur128, lấy mẫu pixel, transcript word-level). Khi có
thêm video mẫu cùng kênh/phong cách, cập nhật lại bảng ở mục 1 thay vì tạo skill mới.*
