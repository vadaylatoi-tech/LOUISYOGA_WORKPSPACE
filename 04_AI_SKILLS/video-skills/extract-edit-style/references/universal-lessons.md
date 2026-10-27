# Bài học dùng chung cho MỌI skill `edit-style-*` build bằng HyperFrames

> Đúc rút từ thực tế build nhiều video/phong cách khác nhau (bắt đầu từ `edit-style-nns`).
> Khi `extract-edit-style` tạo 1 skill `edit-style-<tên>` mới, LUÔN chép nguyên phần A vào mục 6
> ("Ghi chú khi build trực tiếp bằng HyperFrames") của skill mới ngay từ đầu — đây là kỹ thuật NỀN
> TẢNG áp dụng bất kể phong cách hình ảnh cụ thể ra sao, không phải thứ phải chờ build thử mới biết
> như các kỹ thuật ĐẶC THÙ cho từng phong cách. Phần B là quy ước làm việc — thêm 1 đoạn ngắn trỏ
> tới file này ở đầu skill mới (ngay dưới blockquote giới thiệu), không cần copy hết chi tiết.

---

## A. Kỹ thuật HyperFrames nền tảng (copy vào mục 6 của mọi skill mới)

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
opacity đơn giản (~0.4–0.5s, ease `sine.inOut`/`power1`, KHÔNG dùng ease giật như `back`/`power2` ở
đây — những ease đó dành cho hiệu ứng bounce-vào-khung, không phải crossfade lớp).

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
   Nếu `box_low` ra ÂM (hairline nằm trên biên cover-crop tự nhiên — video quay rất cận) → KẸP về
   0, origin trở thành top-anchored (`transform-origin: 50% 0%`) thay vì origin nằm giữa khung.
5. Crop thử bằng ffmpeg (`crop=<w>:<w>:<x>:<y>` suy từ bước 4, rồi `scale=460:460`) và XEM LẠI BẰNG
   MẮT trước khi đưa vào code.
6. Số này KHÔNG copy sang video/project khác — lặp lại bước 1–5 cho mỗi video mới.

**Canh giữa nội dung Kiểu B (không neo cứng lên trên):**
```css
.xxx-root { justify-content: center; padding: 200px <trái/phải> <bottom>px; }
```
`<bottom>` = khoảng cách từ đáy khung tới mép trên `#pip-mask` + biên thở ~40-60px, để nội dung tự
canh giữa trong phần khung CÒN LẠI phía trên PiP thay vì dồn lên đỉnh và để trống 1 khoảng lớn ở
giữa. Tính lại `<bottom>` nếu đổi kích thước/vị trí PiP (số này KHÔNG phụ thuộc video/góc quay, chỉ
phụ thuộc hình học khung + layout PiP — khác với bước hiệu chỉnh PiP ở trên).

**An toàn vùng trên cho Facebook Reels/TikTok:** không đặt nội dung nào cao hơn **200px** tính từ
mép trên khung (trên khung 1080×1920, tỉ lệ tương ứng nếu khung khác) — thanh tìm kiếm/icon UI của
app che mất phần này. Áp dụng cho MỌI root có nội dung neo trên; dùng chung 1 hằng số cho cả bài.

**Caption đáy KHÔNG chạy song song với card full-bleed (Kiểu B) đang hiện.** Card Kiểu B (nền phủ
toàn khung) tự nó đã là "caption" lúc đó. Chạy thêm caption đè lên vừa dư thừa, vừa dễ FAIL contrast
check thật (chữ trắng viền mỏng trên nền sáng). Chỉ bật caption lúc talking-head thuần hoặc Kiểu A
(nền trong suốt, video chính vẫn hiện phía sau).

**Ken Burns nhiều đoạn = 1 chuỗi LIÊN TỤC, dùng `tl.to()` không dùng `tl.fromTo(scale:1.0→target)`
lặp lại từng đoạn** — `fromTo` ép giá trị nhảy về đúng 1.0 ở đầu MỖI đoạn bất kể đoạn trước đã zoom
tới đâu, tạo giật ngược đúng tại ranh giới 2 đoạn. `to()` kế thừa giá trị hiện tại, chuỗi mượt.

**Mọi `.root` xếp nội dung theo chiều DỌC phải khai báo rõ `flex-direction: column`** — base class
`display:flex` không có `flex-direction` mặc định (tức `row`). Quên khai báo ở 1 class con khiến
nội dung (badge + nhiều dòng chữ...) dính liền thành 1 dòng ngang thay vì xếp dọc. Lint KHÔNG bắt
được lỗi này (lỗi bố cục thẩm mỹ) — luôn tự kiểm bằng snapshot khung hình đầu tiên của MỖI loại
card mới, không chỉ tin lint 0 lỗi.

**Hiệu ứng camera (`#cam-punch`, Ken Burns trên `#cam`) chỉ hiển thị khi `#video-wrap` đang HIỆN
(opacity ~1).** Nếu điểm nhấn rơi đúng lúc đang PIP, punch trên `#cam-punch` vô hình — không thể
chuyển sang `#pip-cam` (luật PiP cấm animate kích thước). Đối chiếu lịch `toPip`/`toFull` trước khi
thêm punch tại 1 mốc giờ; nếu lúc đó đang PIP, bỏ punch đó (giữ SFX một mình vẫn ổn).

**Nếu style có stinger số:** số PHẢI là con của hình nổ (`display:flex;align-items:center;
justify-content:center` trên hình nổ để tự căn giữa) — 2 phần tử `position:absolute` tách riêng sẽ
lệch tâm.

**Nếu style có karaoke word-highlight:** bọc theo TỪ (`<span class="w">từ</span>` với khoảng trắng
THẬT giữa các span), không bọc theo ký tự — bọc ký tự khiến trình duyệt được phép ngắt dòng giữa 2
ký tự bất kỳ.

**Nhạc nền (BGM):** trước khi coi 1 bản build là "xong", tự hỏi đã có `<audio>` nhạc nền chưa (dễ
quên nếu chỉ lo phần SFX). Thêm BGM cần hỏi ý user trước — không tự ý chọn cách lấy nhạc (HeyGen
cần đăng nhập, generate cục bộ cần API key hoặc tải model nặng) — xem `media-use/audio/references/
bgm.md` mục Preflight.

**Trước khi render, luôn:** `npx hyperframes check` (0 lỗi) + snapshot vài khoảnh khắc chính rồi
XEM BẰNG MẮT — lint sạch không đồng nghĩa hình đẹp/đúng bố cục.

---

## B. Quy ước làm việc (thêm 1 đoạn ngắn trỏ tới mục này ở đầu skill mới, không copy hết)

- **Gated workflow khi user feedback trên bản build đã render:** plan (chỉ text, không sửa file)
  → chờ user OK → update skill (`edit-style-<tên>/SKILL.md`) → chờ user OK lần nữa → mới build/
  render lại. Không skip gate dù fix có vẻ nhỏ/hiển nhiên.
- **Trả lời user bằng tiếng Việt** (trừ khi họ đổi ngôn ngữ).
- **Video không khớp cấu trúc N-tip mẫu:** báo rõ cho user, thích ứng khung sườn linh động (vd.
  listicle N bước nhanh, CTA đơn không có tip) thay vì ép khuôn giả — nhưng luôn ghi chú rõ trong
  blueprint/skill chỗ nào là thích ứng và vì sao.
- **Transcript/ASR nghe không chắc** (tên riêng, thuật ngữ): đánh dấu rõ ràng (⚠ hoặc placeholder
  an toàn), KHÔNG đoán liều rồi trình bày như sự thật — hỏi lại user xác nhận trước khi chốt.
- **Video lạ chưa rõ nội dung:** xem qua vài khung hình để xác nhận nội dung hợp lệ/an toàn trước
  khi transcribe/xử lý tiếp, đặc biệt nếu tên file không rõ nguồn gốc.
- **Trước khi render 1 bản quan trọng/nhiều thay đổi:** cân nhắc chạy 1 vòng review đối kháng (vài
  góc nhìn độc lập kiểm tra: khớp blueprint, tuân thủ quy tắc skill, QA hình ảnh bằng snapshot thật)
  thay vì chỉ tự kiểm 1 lần — tự kiểm một mình dễ bỏ sót lỗi hiển nhiên (đã xảy ra thật).
- **Kho tài nguyên dùng chung `SON_AI_VIDEO/shared-sources/`** (manifest tại `shared-sources/
  SOURCES.md`) — MỌI skill edit đọc/ghi được thư mục này, khác `assets/` riêng của từng project.
  Trước khi tự tạo 1 tài nguyên mới (demo screenshot, B-roll...), LUÔN đọc `SOURCES.md` xem đã có
  sẵn chưa. Nếu thiếu và cần tự thao tác lấy (vd quay demo giao diện thật qua Chrome của user) —
  BÁO cho user đang thiếu gì cụ thể và hỏi trước khi tự làm, không tự động chạy song song lúc đang
  lên blueprint. Sau khi tạo xong, lưu file vào `shared-sources/` (thư mục con phù hợp, tạo mới nếu
  cần) và tự thêm 1 dòng vào manifest — để video sau tái dùng được. Không tự xoá/ghi đè file đã có
  trong manifest.
