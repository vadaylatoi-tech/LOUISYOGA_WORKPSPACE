# B-roll index — `assets/broll/louisyoga_brand_film_30fps.mp4`

Phim thương hiệu Louis Yoga (bản gốc: "Video Hero - Trang chủ.mp4", cũng có trên YouTube @louisyoga, id AFo_DvpQWf0).
1920×1080, 30 fps, im lặng, 92.6 s. `film` = giây bắt đầu, `cx` = tâm chủ thể theo trục ngang (0–1920).

**Chế độ khung (góp ý 26/10/2026):** cắt dọc 9:16 chỉ còn ~607 px quanh `cx` → người tập bị cắt tay chân, "cận quá không
rõ tư thế". Cảnh TƯ THẾ dùng `mode: "fit"` (mặc định: cả khung ngang + nền mờ). Cột "khung" dưới đây ghi chế độ nên dùng.

| film (s) | dài dùng được | nội dung | cx gợi ý | hợp với lời nói | khung |
|---|---|---|---|---|---|
| 7.0–11.5 | 4 s | tư thế bồ câu (gối chạm thảm) trên thảm xanh lá | 860 | quỳ gối, linh hoạt, dẻo | fit |
| 12.0–16.8 | 4 s | ngồi thiền trên thảm xanh lá | 940 | thư giãn, người mới | fit |
| 17.0–19.8 | 2.8 s | chống cẳng tay / dolphin trên thảm xanh dương | 820 | tì tay, bài nâng cao | fit |
| 19.8–22.5 | 2.7 s | trồng chuối chân lên cao | 760 | bài nâng cao, thăng bằng | fit |
| 40.0–41.7 | 1.7 s | ôm thảm cuộn in chữ LOUISYOGA | 960 | thương hiệu, sản phẩm | fit |
| 42.0–45.8 | 3.5 s | tay vuốt bề mặt thảm xanh lá (đường định tuyến) | 1150 | bề mặt, đường định tuyến | crop (cận tay — không dùng minh hoạ tư thế) |
| 46.0–49.8 | 3.5 s | ngón tay lần hoạ tiết in trên thảm xanh ngọc | 1000 | hoạ tiết, in ấn, chất lượng | crop (cận) |
| 50.0–52.0 | 2 s | tay trên thảm xanh lá có nắng | 620 | ánh sáng, cảm giác | crop (cận) |
| 52.5–57.5 | 4.5 s | tay lật mép thảm thấy mặt đen (2 lớp) | 900 | độ dày, cấu tạo, bám sàn | crop (cận) |
| 58.0–59.8 | 1.8 s | quỳ gối + tì tay, trán chạm thảm (thảm xanh dương) | 1000 | quỳ gối, tì tay | fit |
| 60.0–62.8 | 2.8 s | bàn tay ấn trên thảm xanh dương (cận) | 960 | độ nén, độ êm | crop (cận) |
| 63.0–69.8 | 6 s | nằm cầu/vặn mình trên thảm xanh lá | 900 | bài tập lưng, êm ái | fit |
| 70.0–74.8 | 4.5 s | ngồi thiền (thảm xanh dương), cận mặt | 900 | an tâm, tập trung | fit |
| 89.0–92.0 | 3 s | logo Louis Yoga hoa sen | 960 | kết thúc | fit |

TRÁNH: 0–6.8 s (tên người có chữ in), 23–39 s (người nói vào máy + icon ✓ in sẵn ở 27–34 s), 75–88 s (người nói vào máy).


## B-roll từ mạng — CHỈ DÙNG KHI KHÔNG CÓ TƯ LIỆU LOUIS (góp ý 27/10/2026)
Chủ thương hiệu thấy reel 03–04 "lạm dụng video không phải của Louis". Ưu tiên: sản phẩm trong chính video → ảnh sản phẩm /
ảnh người mẫu Louis (louisyoga.vn) → phim thương hiệu (fit) → clip web. Clip web: tối đa 1 clip/video, ≤ 2,5 s, không làm
hình chính, không ghi chữ như thể đó là thảm Louis.

### (cũ) B-roll từ mạng (được phép — chủ thương hiệu 26/10/2026)
Điều kiện: không dính logo / tên / bao bì của hãng khác (soi kỹ thảm, áo, tường), ưu tiên toàn thân, ánh sáng sáng,
thảm trơn hoặc không thấy chữ. Nguồn giấy phép dùng thương mại không cần ghi công: Pexels, Pixabay, Mixkit (ghi nguồn
vào báo cáo vẫn nên làm); Wikimedia Commons theo CC (ghi credit). Hỏi người dùng trước khi tải (tên file, nguồn, dung lượng).
Chuẩn hoá: `ffmpeg -i in.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" -an -c:v libx264
-crf 16 -g 10 -bf 0 public/broll/web/<ten>.mp4` (clip dọc) — clip ngang để nguyên tỉ lệ, dùng `mode: "fit"`.
Ghi từng clip đã duyệt vào bảng dưới để video sau dùng lại.

Mỗi clip: 1080×1920, 30 fps, im lặng, đã soi khung từng 2 s không thấy logo/chữ hãng khác (26/10/2026).
Dùng: `{ start, end, film: <giây trong clip>, src: "broll/web/<file>.mp4", mode: "cover", label: "…" }`.
Thảm trong clip là thảm KHÁC hãng → chỉ minh hoạ tư thế/hoạt động, không nói/ghi như sản phẩm Louis Yoga.

| file (`assets/broll/web/`, .mp4) | dài (s) | nội dung theo giây | hợp với lời nói |
|---|---|---|---|
| tu-the-em-be-meo-bo_6696224 | 10.0 | 0–6 tư thế em bé trên thảm xanh · 6–10 chống 4 điểm (mèo-bò); phòng ấm, thảm trơn | thư giãn, người mới, tập tại nhà |
| cho-up-mat-tap-online-laptop_6767726 | 9.8 | chó úp mặt trước laptop (logo laptop bị miếng dán che), thảm in hoạ tiết hoa không chữ | **tập online**, tự tập ở nhà |
| kiem-tra-tham-dien-thoai-tap-online_7690290 | 3.0 | ngồi xổm chỉnh thảm, điện thoại trên tripod (không lộ logo) | **tập online**, chuẩn bị buổi tập |
| chien-binh-tap-tai-nha_6696211 | 10.0 | 0–4 chiến binh, giơ tay · 4–10 gập người chân rộng; phòng khách nắng | tập tại nhà, thăng bằng |
| tam-giac-chien-binh_6437979 | 10.0 | 0–4 tam giác · 4–8 dang tay · 8–10 tam giác; thảm xanh, sofa | đặt chân, thăng bằng, căn chỉnh |
| bird-dog-tren-tham_6297114 | 10.0 | 0–8 bird-dog (chống tay + duỗi chân) · 8–10 quỳ; thảm xanh | vị trí đặt tay/chân, căn chỉnh, tì tay |
| quy-goi-len-plank_7589753 | 13.8 | 0–2 quỳ gối · 2–14 plank cẳng tay; thảm xám, rèm trắng | **quỳ gối, tì tay**, độ êm, chống trượt |
| plank-cang-tay-tham-xam_7589746 | 10.6 | 0–8 plank cẳng tay · 8–10 plank thẳng tay; thảm xám | tì tay, độ bám |
| plank-cang-tay-tham-xanh_6302985 | 10.0 | plank cẳng tay nhìn thẳng máy, thảm xanh, phòng gạch | tì tay, sức bền |
| plank-nghieng-san-go_6437916 | 10.0 | 0–6 plank cẳng tay · 6–10 plank nghiêng; sàn gỗ, KHÔNG có thảm | bài nâng cao (không dùng khi nói về thảm) |
| ran-ho-mang-cobra_6437925 | 10.0 | rắn hổ mang trên thảm xanh, phòng rất sáng | giãn lưng, tư thế cơ bản |
| cho-up-mat-sang-ran-ho-mang_7663063 | 21.4 | 0–6 chó úp mặt · 6–8 chuyển · 8–21 chó ngửa mặt; thảm xanh đậm, phòng gỗ ấm | chuỗi tư thế, độ bám tay chân |
| lunge-cho-up-mat-chong-day_6019799 | 30.0 | 0–2 lunge · 2–12 gập → chó úp mặt · 12–16 plank → chống đẩy; nền xám, KHÔNG thảm | tư thế khó, linh hoạt |
| ngoi-thuyen-giu-thang-bang_4535119 | 7.8 | tư thế thuyền (ngồi nâng chân); phòng cửa sổ trắng, thảm mỏng | cơ bụng, thăng bằng |
| trai-tham-ra-san_7590819 | 5.6 | quỳ trải thảm xám ra sàn | bắt đầu buổi tập, mở thảm mới |
| cuon-tham-quy-goi_7589754 | 14.1 | 0–12 quỳ cuộn thảm xám · 12–14 dựng thảm đã cuộn | **cuộn/bảo quản thảm** |
| nam-cuon-tham_6297120 | 10.0 | nam quỳ cuộn thảm xanh, phòng gạch | cuộn thảm, kết buổi tập |

Nguồn: Pexels (pexels.com/video/<mã số cuối tên file>/), giấy phép Pexels — dùng miễn phí cả thương mại, không bắt buộc
ghi công; KHÔNG bán lại nguyên clip, KHÔNG làm như người trong clip đang giới thiệu sản phẩm. Danh sách gốc: `assets/broll/web/NGUON.md`.
