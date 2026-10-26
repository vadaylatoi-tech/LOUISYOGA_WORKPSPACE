# Louis Yoga — Reel "Chọn thảm hút mồ hôi" · bản edit v2

Ngày làm: 24/10/2026.
Video mẫu: facebook.com/reel/1763428218100789 (kênh explainer "Liệu ngày tàn đế chế Pháp", 233.6s, 1080×1920 @30fps).
Video gốc: `Tài nguyên video/FDown.vn_Tai_video_Facebook_1080p_748c.mp4` (48.9s, 1080×1920 @30fps).

Cách đo: dùng ffmpeg để tách khung hình theo giây, dò điểm cắt cảnh (scene > 0.25), đo độ to theo từng 0.1s và dò tiếng "chát" ở dải cao (> 4 kHz) để tìm vị trí SFX. Lời nói chép bằng faster-whisper large-v3, có mốc thời gian từng từ.
Em không nghe trực tiếp âm thanh: nhận xét về nhạc và SFX là suy ra từ số đo.

---

## 1. Phong cách của video mẫu

| Hạng mục | Quan sát (giây) | Áp dụng vào bản mới |
|---|---|---|
| Hook | 0–5s: mở bằng mốc ngày + địa điểm ("21/9 · NGOẠI Ô PARIS") và một hành động cụ thể. Câu thứ 2 đã có con số lớn ("GẦN 500.000 NGƯỜI", "HƠN 6.000") | 0–2.6s: câu hỏi lớn "THẢM NÀO / HÚT MỒ HÔI TỐT NHẤT?" đập vào màn hình, kèm whoosh và punch |
| Nền và màu | Nền than chì tối, bản đồ vệ tinh. Màu nhấn **xanh chanh neon** + trắng, **đỏ** dành cho số liệu xấu hoặc dấu mộc | Nền `#121212` có đường đồng mức mờ (gợi bản đồ). Màu xanh chanh `#C8F53C`, trắng, đỏ `#E8322B` |
| Chữ | Sans rất đậm, VIẾT HOA. Dòng nhỏ giãn chữ ở trên, chữ to ở dưới; từ khoá đổi màu | Montserrat 800–900 viết hoa, cùng kiểu "dòng nhỏ + chữ to" |
| Ảnh minh hoạ | Ảnh polaroid khung trắng rơi xuống hơi xoay, có chú thích dưới ảnh (Versailles, Louvre…). Có sticker (nhiệt kế) và **dấu mộc đỏ "40°C" đập xuống** | Polaroid thảm xanh, thảm đen. Nhiệt kế dâng 28→40°C, dấu mộc đỏ "HOT YOGA", "VỪA ĐỦ" |
| Số liệu | Mỗi con số đều thành đồ hoạ: bộ đếm, thanh, ô lưới, đồ thị | "4,5 LY" đếm từ 0, có thước vạch sáng dần |
| Chuyển cảnh | **Whip dọc có nhoè chuyển động** khoảng 0.3s (ví dụ mốc 19–20s, 23s), zoom bản đồ vào/ra, đẩy chậm vào ảnh | Whip dọc có nhoè ở 10 điểm cắt, kèm swoosh |
| Mép giấy | Giấy xé màu be làm "mặt đất" (120–190s) | Mép giấy xé ngăn khung video với vùng đồ hoạ |
| Sơ đồ | Icon trong vòng tròn viền xanh, nối bằng đường kẻ ("4 BẤT ỔN", ①②③) | Vòng số ①② cho 2 mẫu thảm, danh sách ✓ có đường kẻ nối |
| Âm thanh | Độ to −14.1 LUFS. Không có giây nào dưới −37 dB, tức có **nhạc nền chạy liên tục**. Khoảng **1 SFX mỗi giây** (75 điểm "chát" trong 70s), đúng lúc đồ hoạ xuất hiện | Nhạc nền tự tổng hợp (Am–F–C–G, 100 BPM, không lo bản quyền) ở mức nhỏ dưới giọng. 42 SFX trong 41.7s. Chuẩn hoá −14 LUFS |
| Nhịp | Cứ 1–2s lại đổi hình hoặc có đồ hoạ mới | Đồ hoạ đổi theo từng câu |
| Kết | Câu chốt 2 màu (xanh + đỏ) | CTA "FOLLOW LOUIS YOGA" + nút đỏ "XEM THÊM MẸO CHỌN THẢM", giữ thêm 1.2s |

## 2. Video gốc: nội dung và điểm chưa tốt

**Nội dung:** Thảm cao su tự nhiên đều thấm hút mồ hôi tốt. Ra nhiều mồ hôi hoặc tập hot yoga thì chọn thảm dày hơn. Mẫu 1 (thảm xanh) dành cho người tập thường xuyên. Mẫu 2 (thảm đen) cho người mới tập, dày 4,5 ly là vừa đủ. Bề mặt thảm cần êm ái, thấm hút, bám sàn và bám tay. Thảm Louis Yoga đáp ứng đủ.

| Điểm chưa tốt | Đo được | Cách khắc phục |
|---|---|---|
| Hook yếu: câu hỏi bị lẫn vào câu trả lời | 0–8s là một câu dài | Tách câu hỏi thành tiêu đề đập vào màn hình ở 0–2.6s |
| 0.5s im lặng ở đầu | −42 dB ở giây đầu | Cắt bỏ |
| Từ đệm, nói lặp: "ví dụ như là", "chẳng hạn", "cho em", "giúp em là", "rất là đủ rồi" (lặp), "các cái" | Có mốc từng từ | Cắt 11 chỗ ngay ranh giới từ, có fade 12ms chống tiếng tách. **48.9s → 40.5s (−17%)** |
| Lặng 1.4s giữa câu | raw 21.2–22.5s | Cắt bỏ |
| Người nói đi ra khỏi khung | raw 8–11s, máy dò mặt báo mất mặt ở 8.5–12s | Phủ đồ hoạ "RA NHIỀU MỒ HÔI → nhiệt kế → HOT YOGA" lên đoạn này |
| Thẻ hồng in cứng che 40% khung, nhiều đoạn **thẻ rỗng** | thẻ ở y 1060–1597, rỗng ở khoảng 16–22s và 38s | Chỉ dùng phần hình y 0–1062. Phần dưới thay bằng vùng đồ hoạ mới, không còn thẻ rỗng |
| Người xem không biết "mã này" là mẫu nào | — | Dán nhãn ①/② lên polaroid "Mẫu 1/Mẫu 2" kèm đối tượng |
| Không có nhạc, rất ít SFX | — | Thêm nhạc nền + 42 SFX |
| Kết thúc hụt, tên thương hiệu nói không rõ | ASR nghe thành "lưu dựa KBN" | Hiện logo hoa sen + "LOUIS YOGA" khi tên được nhắc. Thêm màn CTA |

## 3. Đã dùng những gì

- `nns-cut-silence`: kiểm khoảng lặng. File gốc đã khá gọn nên skill không cắt gì, bước verify đạt.
- `nns-auto-sub/transcribe.py`: chép lời word-level (large-v3), để cắt từ đệm và làm caption karaoke.
- `nns-face-highlight/track.py`: dò mặt bằng `det_10g.onnx`, dùng làm tâm cho các cú punch-in.
- Cách làm theo `edit-nns-v1`: dựng bằng Remotion, timeline sinh ra từ transcript (`gen_data.py`), không gõ tay mốc caption.
- SFX lấy từ `shared-sources/sound-effects`. Lead-in của từng file được đo để tiếng đánh trúng khung hình.
- Composition: `louis-yoga-remotion/src/reel2/LouisYogaReel2.tsx`, id `LouisYogaReel2`.

## 3b. Bản v2 (tone hồng) — file `LouisYoga_ChonTham_Reel_v2_hong.mp4`

| Thay đổi | Chi tiết |
|---|---|
| Màu | Màu nhấn hồng `#FF5AAE`, nền pill `#E2318B`, dấu mộc/nút CTA màu vàng gold `#F4C25B` (lấy từ viền vàng của thẻ hồng cũ và logo hoa sen). Nền than ánh tím rượu vang `#16111A` |
| Ảnh "cao su tự nhiên" | Mủ cao su chảy vào chén: "Koh Chang, Thailand, Rubber tapping, Latex" – Vyacheslav Argenberg, Wikimedia Commons, **CC BY 4.0** (đã ghi credit nhỏ trên ảnh) |
| Thảm xanh (người tập thường xuyên) | **BASIC màu xanh dương**, dòng Balance, 5 mm. Đối chiếu hoạ tiết hoa sen trên thảm thật. Ảnh lấy từ `4. Avatar thảm final/2. Balance/2. Basic` |
| Thảm đen 4,5 ly (người mới tập) | **ASANA màu đen**, dòng Harmony, 4.5 mm. Ảnh lấy từ `4. Avatar thảm final/1. Harrmony/3. Asana` |
| Nhạc nền | "Inspired" – Kevin MacLeod (incompetech.com), **CC BY 4.0**, ~117 BPM, điện tử nhẹ tích cực. To hơn ở hook, hạ dưới giọng khi nói, lên lại ở màn CTA |

Credit cần ghi ở caption bài đăng:
`Music: "Inspired" – Kevin MacLeod (incompetech.com), CC BY 4.0 · Ảnh mủ cao su: Vyacheslav Argenberg, CC BY 4.0`

## 4. Cần anh kiểm tra

1. Tên mẫu thảm: em ghi tạm "Mẫu 1 / Mẫu 2" vì trong video chỉ nói "mã này". Có tên/mã thật thì sửa trong `ChoiceScene`.
2. Caption: em sửa "lưu dựa KBN" thành "Louis Yoga bên em", "Thầm" thành "thấm", bỏ "2" trong "Mã 2 này". Anh nghe lại xem đúng ý không.
3. Màu nhấn đang là xanh chanh theo video mẫu. Muốn theo màu thương hiệu thì đổi `C.lime` sang hồng `#d72182` trong file tsx, chỉ cần sửa 1 dòng.
4. Bản quyền SFX: `library.json` không ghi license. Video thương mại nên kiểm tra lại. Nhạc nền do máy tự tổng hợp nên dùng thoải mái. Khi đăng TikTok/FB có thể thay bằng nhạc trend trong app.
