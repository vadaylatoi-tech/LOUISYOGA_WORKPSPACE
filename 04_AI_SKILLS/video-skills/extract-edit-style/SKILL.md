---
name: extract-edit-style
description: "Meta-skill: nhận 1 (hoặc vài) video mẫu của một kênh/phong cách cụ thể, đo đạc thật bằng ffprobe/ffmpeg (không suy đoán từ trí nhớ chung), rồi tạo ra 1 skill `edit-style-<tên>` mới theo đúng khuôn mẫu đã dùng để xây `edit-style-nns`. Dùng khi user gửi video đối thủ/tham khảo và muốn 'học' phong cách đó thành 1 skill dùng lại được nhiều lần cho các video sau, KHÔNG phải khi họ chỉ muốn 1 blueprint dùng 1 lần."
---

# Extract Edit Style — tạo skill phong cách edit mới từ 1 video mẫu

> Meta-skill: input là 1 (hoặc vài) video mẫu của MỘT kênh/phong cách cụ thể, output là 1 skill
> `edit-style-<tên>` mới, đo đạc thật (không suy đoán), theo đúng khuôn mẫu đã dùng để tạo
> `edit-style-nns`. Dùng khi user gửi video đối thủ/tham khảo và muốn "học" phong cách đó
> thành 1 skill dùng lại được nhiều lần.

---

## 1. Khi nào dùng

- User gửi 1 video (thường là đối thủ/kênh tham khảo) + yêu cầu dạng "phân tích phong cách này",
  "tạo skill từ video này", "học theo video này để dùng cho video sau".
- KHÔNG dùng khi user chỉ muốn 1 blueprint edit MỘT LẦN cho video của chính họ (đó là việc của
  skill `edit-style-<tên>` đã có sẵn, không phải việc tạo skill mới) — hỏi lại nếu không chắc ý
  định là "dùng skill có sẵn" hay "tạo skill mới".

**Bước 0 — kiểm tra trùng phong cách TRƯỚC khi đo đạc/tạo skill mới (quan trọng, tránh tạo skill
thừa):** liệt kê các skill `edit-style-*` đã có trong project, đọc nhanh mục 1 (Style DNA) của
từng cái. Xem lướt vài khung hình + cấu trúc tổng thể của video mới (hook/thân/outro, có PiP không,
tông màu, có N-tip lặp không...) rồi so với các skill sẵn có:
- Nếu khớp cơ bản với 1 skill đã có (cùng kiểu cấu trúc, cùng ngôn ngữ hình ảnh, chỉ khác nội dung
  cụ thể) → **BÁO cho user là video này trùng phong cách với `edit-style-<tên có sẵn>`, dùng luôn
  skill đó** (gọi `/edit-style-<tên có sẵn>` để ra blueprint/build), **KHÔNG tạo skill mới trùng
  lặp**. Việc "khác video, khác nội dung" không đồng nghĩa "khác phong cách" — 2 video CÙNG kênh
  hoặc CÙNG công thức edit (dù nội dung khác hẳn) vẫn dùng chung 1 skill.
- Chỉ tiếp tục đo đạc đầy đủ (mục 3) và tạo skill mới khi phong cách THỰC SỰ khác biệt rõ rệt so
  với mọi skill đã có (khác cấu trúc cảnh, khác cách dùng card/PiP, khác tông màu/chữ chủ đạo...).
- Nếu không chắc là "giống" hay "khác" (na ná nhưng có vài điểm lạ) → hỏi lại user, đừng tự quyết.

---

## 2. Input cần có

1. **1 video mẫu** đại diện rõ cho phong cách (đủ dài để thấy hết cấu trúc hook/thân/outro, không
   bị cắt cụt giữa chừng). Có thể nhận nhiều video cùng kênh nếu muốn đối chiếu chéo — khi đó đo cả
   2, ghi rõ số liệu nào đo được ở video nào, và số nào nhất quán giữa các video (đáng tin hơn) vs
   số nào chỉ thấy ở 1 video (có thể là biến thể, không phải quy luật).
2. **Tên/slug cho skill mới** — nếu user không cho tên, tự đặt theo tên kênh/đặc điểm nhận diện
   (watermark, tên trong caption, hoặc mô tả ngắn gọn kiểu nội dung), rồi báo lại tên đã chọn để
   user xác nhận/đổi.

Nếu thiếu video → hỏi lại, không tự bịa đặc điểm phong cách từ trí nhớ chung về "video ngắn thường
có gì".

---

## 3. Quy trình đo đạc (phần quan trọng nhất — LUÔN đo thật, không đoán)

Chạy hết các bước dưới trước khi viết bất kỳ dòng nào vào skill mới.

### 3.1 Metadata cơ bản
```bash
ffprobe -v error -show_entries format=duration -show_entries stream=width,height,r_frame_rate,codec_type -of default=noprint_wrappers=1 video.mp4
```
Ghi lại: độ phân giải, tỉ lệ khung (9:16 / 1:1 / 16:9...), fps, thời lượng, codec audio.

### 3.2 Cấu trúc cắt cảnh (hook/thân/outro, mật độ cut)
```bash
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```
Đếm số cut trong đoạn 5-10s đầu (hook thường cắt dày) so với đoạn giữa (thường thưa hơn, gắn với
card/screenshot giữ hình lâu). Nếu ngưỡng 0.3 cho quá nhiều/quá ít cut giả, thử lại 0.2–0.5 rồi đối
chiếu bằng mắt qua vài khung trích ra — đừng tin số một cách máy móc.

### 3.3 Khoảng lặng & loudness (nhạc nền có chạy liên tục không, mix nén chặt hay có to/nhỏ rõ)
```bash
ffmpeg -i video.mp4 -af silencedetect=noise=-30dB:d=0.2 -f null - 2>&1 | grep silence
ffmpeg -i video.mp4 -af volumedetect -f null - 2>&1 | grep -i mean
ffmpeg -i video.mp4 -af ebur128 -f null - 2>&1 | tail -20
```
Ghi lại: có khoảng lặng thật không (→ suy ra nhạc nền chạy liên tục hay tắt lúc thoại), LUFS
integrated, LRA (dải động — số nhỏ nghĩa là mix bị nén/limit chặt, ít đoạn to/nhỏ rõ rệt).

### 3.4 SFX tại các điểm chuyển cảnh/nhấn
So `volumedetect` cắt riêng từng đoạn 0.3-0.6s tại các điểm nghi có SFX (chuyển cảnh, điểm nhấn số
liệu) với baseline đoạn xung quanh — chênh lệch rõ (>2dB) thường xác nhận có SFX đè, không chỉ là
hình ảnh trùng hợp.

### 3.5 Màu — trích khung hình rồi đọc pixel thật, KHÔNG suy đoán "trông giống màu gì"
```bash
ffmpeg -y -ss <t> -i video.mp4 -frames:v 1 -q:v 2 frame.png
```
Trích 5-10 khung ở các beat khác nhau (hook, mỗi loại card/overlay, outro). Đọc pixel bằng Python
(`PIL.Image.open("frame.png").getpixel((x,y))`) tại đúng điểm cần đo (nền card, chữ, badge...) để
ra hex chính xác — không nhìn ảnh rồi đoán "chắc là cam" hay "chắc là be".

### 3.6 Xem trực tiếp khung hình để rút cấu trúc/chữ/motion (cần mắt, không đo bằng số)
Đọc từng khung đã trích (dùng tool đọc ảnh multimodal) để xác định:
- Có bao nhiêu LOẠI cảnh cố định (card gì, dùng khi nào) — lập thành bảng như "Bảng scene" của
  `edit-style-nns` mục 1.
- Cấu trúc lặp: có N mục/tip lặp theo 1 khung cố định không? N là bao nhiêu? Nếu N khác nhau giữa
  các video mẫu, ghi rõ range thay vì chốt cứng 1 số.
- Kiểu chữ: caption cắt theo từ/cụm/câu? Có karaoke word-highlight không? Vị trí trên khung (đo %
  chiều cao, không áng chừng).
- Vùng mặt diễn giả nằm ở đâu (đo % khung, x và y) — để biết vùng an toàn không đặt overlay sau
  này.
- Camera có zoom/pan không (Ken Burns liên tục? punch-in tại điểm nhấn? hay tĩnh tuyệt đối)? Xem
  kỹ nhiều khung liên tiếp, đừng kết luận "không có" chỉ vì không thấy rõ ở lần xem đầu — bài học
  từ chính `edit-style-nns` mục 1 ("Cập nhật vòng 2": kết luận "không zoom/pan" ban đầu ĐÃ
  SAI, đo kỹ lại mới phát hiện 2 lớp motion rõ rệt).
- Có "signature move" nào lặp lại, nhận diện được phong cách không (kiểu chuyển cảnh riêng, hiệu
  ứng số/badge riêng, cách xử lý khi cần hiện thêm nội dung cùng lúc với diễn giả...).

---

## 4. Viết skill mới — dùng khuôn `edit-style-nns` làm template

Copy cấu trúc file `edit-style-nns/SKILL.md` mục 1–5 (Style DNA / Input yêu cầu / Thuật toán
tạo blueprint / Output cố định / Checklist QC) — thay số liệu bằng số liệu ĐÃ ĐO ở mục 3, giữ
nguyên khung sườn trừ khi phong cách mới thực sự khác về bản chất (vd. không phải dạng N-tip mà là
dạng khác hẳn — khi đó điều chỉnh thuật toán map ở mục 3 cho khớp và ghi rõ lý do khác biệt).

**Mục 6 ("Ghi chú khi build trực tiếp bằng HyperFrames") của skill mới KHÔNG để rỗng hoàn toàn** —
LUÔN chép nguyên phần A của `references/universal-lessons.md` (cùng thư mục với skill này) vào làm
nội dung khởi điểm của mục 6: đây là kỹ thuật NỀN TẢNG áp dụng cho MỌI skill `edit-style-*` build
bằng HyperFrames bất kể phong cách hình ảnh cụ thể (luật allowlist GSAP, PiP hình tròn 2-lớp video,
công thức hiệu chỉnh PiP, canh giữa nội dung phía trên PiP, an toàn vùng trên nền tảng, caption
không đè card full-bleed, Ken Burns liên tục, `flex-direction`, punch chỉ hiện khi video chính đang
hiện, BGM...) — không phải thứ phải chờ build thử mới biết, khác với kỹ thuật ĐẶC THÙ cho phong
cách/video cụ thể (chỉ thêm SAU khi thực sự build qua ít nhất 1 lần, không bịa trước).

Ngoài ra, thêm 1 đoạn ngắn ngay dưới blockquote giới thiệu ở đầu skill mới, trỏ tới phần B của
`references/universal-lessons.md` (quy ước làm việc: gated workflow, trả lời tiếng Việt, xử lý
transcript không chắc, thích ứng linh động khi nội dung khác cấu trúc mẫu, review đối kháng trước
khi render...) — không cần copy hết chi tiết phần B, chỉ cần 1 câu trỏ tới file để không lặp lại
đoạn dài giống nhau ở mọi skill.

**Luôn ghi rõ nguồn đo** ở đầu file (đúng pattern đã có): tên file video mẫu, độ phân giải/fps/thời
lượng, các lệnh đã dùng để đo — để lần sau (kể cả ở phiên làm việc khác, không còn nhớ hội thoại
này) biết đây là số liệu đo thật và biết đo lại bằng gì nếu cần cập nhật.

**Đặt tên & vị trí:** `.claude/skills/edit-style-<slug>/SKILL.md` trong project hiện tại (slug viết
thường, không dấu, nối gạch ngang — vd tên kênh hoặc đặc điểm ngắn gọn). Frontmatter `description`
viết theo đúng giọng văn của `edit-style-nns`, nêu rõ trigger (`/edit-style-<slug>`, hoặc câu
kiểu "lên blueprint theo phong cách [tên kênh]").

---

## 5. Sau khi tạo xong

- Báo cho user: đã tạo skill nào, đo được gì đáng chú ý — đặc biệt nếu phong cách mới KHÁC hẳn
  `edit-style-nns` ở điểm nào (N-tip hay không, có PiP không, tông màu gì, có karaoke không).
- Hỏi user có muốn thử ngay skill mới trên 1 audio/transcript cụ thể để ra blueprint đầu tiên
  không — đây là cách tốt nhất để phát hiện chỗ đo chưa chuẩn trước khi dùng nhiều lần về sau.
- KHÔNG tự động build HyperFrames composition từ skill mới ngay. Mục 6 lúc này mới chỉ có phần
  NỀN TẢNG dùng chung (từ `references/universal-lessons.md`) — phần kỹ thuật ĐẶC THÙ cho phong
  cách/video cụ thể vẫn cần build thử ít nhất 1 lần thật mới rút ra được, đúng như cách phần đặc
  thù trong mục 6 của `edit-style-nns` được viết dần qua nhiều vòng build thực tế (vòng 2 →
  vòng 5), không phải viết sẵn từ đầu.

---

*Meta-skill này không thay thế `skill-creator` (dùng cho việc tạo skill nói chung) — đây là quy
trình CHUYÊN BIỆT cho đúng 1 việc: biến 1 video mẫu thành 1 skill phong cách edit, đo đạc thật theo
đúng phương pháp đã dùng để tạo `edit-style-nns`.*
