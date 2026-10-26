# Louis Yoga — TVC Reels v1 (bản không nhạc)

- Ngày dựng: 22/10/2026
- Engine: Remotion 4.0.537, app `05_VIDEO_PROJECTS/louis-yoga-remotion/`, composition `louis-yoga-tvc`
- File cuối: `05_VIDEO_PROJECTS/louis-yoga-remotion/renders/tvc/louis-yoga-tvc-final-v1.mp4`
- Preview (nửa độ phân giải): `renders/tvc/louis-yoga-tvc-preview-v1.mp4`, `-v2`, `-v3`. Bản v3 cùng nội dung với bản cuối.

## 1. Ý tưởng

**"Một khoảng nhỏ cho riêng mình"**

Video không có lời thoại. Mở bằng ánh nắng trên mặt thảm, rồi tới những khoảnh khắc tập chậm rãi trên thảm Louis Yoga, xen các cận hoạ tiết và logo trên thảm. Kết bằng logo động của thương hiệu và CTA "Khám phá Louis Yoga".

- Chỉ dùng hình ảnh thật từ phim thương hiệu của chính Louis Yoga.
- Không có thông số, công dụng hay claim sức khoẻ.
- Không dùng các đoạn người mẫu nói vào máy, vì bản này không có tiếng.

## 2. Kịch bản và timeline (30 fps, tổng 813 frame = 27.1s)

| Thời gian | Cảnh (nguồn trong phim gốc) | Chữ trên màn hình | Chuyển cảnh |
|---|---|---|---|
| 0.0–2.4s | Nắng qua cửa sổ trên góc thảm xanh, tay lật mép thảm (50.6–53.0s) | "Một khoảng nhỏ / cho riêng mình" | Mở thẳng vào hình |
| 2.4–5.2s | Tư thế bồ câu trên thảm xanh (8.0–10.8s) | — | Cắt thẳng |
| 5.2–8.2s | Ngồi thiền trên thảm xanh (13.0–16.0s) | — | Cắt thẳng |
| 8.2–11.0s | Cận tay lướt trên mặt thảm (42.3–45.3s) | "Bắt đầu / từ tấm thảm" | Cắt thẳng |
| 11.0–14.0s | Tư thế đứng bằng đầu, thảm xanh dương (18.0–21.0s) | — | Cắt thẳng |
| 14.0–16.4s | Cận hoạ tiết hoa sen trên thảm xanh dương (46.5–49.0s) | "Chậm lại / một chút" | Cắt thẳng |
| 16.4–19.2s | Tư thế nằm ngửa, thảm xanh hoạ tiết (62.8–65.8s) | — | Cắt thẳng |
| 19.2–22.7s | Ngồi tĩnh, nhắm mắt (71.0–74.5s) | — | Cắt thẳng |
| 22.7–23.9s | Cuộn thảm xanh dương có logo LOUISYOGA (40.5–41.7s) | — | Loé trắng 18 frame |
| 23.9–27.1s | Logo động Louis Yoga (89.0–92.2s) | "Khám phá Louis Yoga" | — |

Cách dựng:
- Mỗi cảnh được cắt về khung dọc 9:16 quanh chủ thể, có push-in chậm 0–5% (cảnh có đầu sát mép trên thì giữ yên).
- Cảnh logo hiển thị rộng hơn, đặt trên nền là chính video đó làm mờ, để chữ LOUISYOGA không bị cắt.
- Chữ Montserrat, màu trắng có bóng mờ, chỉ đặt trên các cảnh cận thảm để không đè lên mặt người.
- CTA màu đỏ rượu `#4a202c`, gạch nhấn hồng `#d72182` (theo hệ màu website trong `LOUIS_YOGA_EDIT_GUIDE.md`).
- Kỹ thuật lấy từ nghiên cứu tham chiếu (bảng B trong guide): hook bằng chuyển động thật ngay frame 0, cắt thẳng, cảnh 2.4–3.5s, chữ ngắn ≤ 3 từ mỗi dòng, end card logo. Không dùng VFX, glitch hay "comment để nhận".

## 3. Asset đã dùng và quyền sử dụng

| Asset | Nguồn | Quyền sử dụng đã xác minh | File trong project |
|---|---|---|---|
| Phim thương hiệu "LOUIS YOGA X HOA HẬU YOGA VIỆT NAM 2024 – NGUYỄN THỊ HUYỀN" | File gốc trên máy: `01_BRAND/video/Video Hero - Trang chủ.mp4` (1920×1080, 59.94fps, 92.6s, 468 MB, creation_time 2024-12-04). Cùng nội dung với https://www.youtube.com/watch?v=AFo_DvpQWf0 | Kênh đăng video là **LOUISYOGA (@louisyoga)**, xác minh qua oEmbed công khai của YouTube. Video đang được dùng làm video nền trang chủ louisyoga.vn. Kết luận: **Louis Yoga là chủ sở hữu nội dung**. Không tải gì từ YouTube. | 10 đoạn trích lại, không tiếng, 30fps: `05_VIDEO_PROJECTS/louis-yoga-remotion/public/tvc/clips/s01–s10.mp4`. File gốc không bị sửa. |
| Logo động Louis Yoga | Nằm ngay trong phim gốc ở trên (89.0–92.2s) | Như trên | `public/tvc/clips/s10.mp4` |
| Font Montserrat (variable) | `Dự án tạo website daft - louis Yoga/louis-yoga/dist/assets/Montserrat.ttf` | SIL Open Font License 1.1 (file license đi kèm) | `public/fonts/Montserrat-Variable.ttf`, `Montserrat-OFL.txt` |
| Nhạc / SFX | **Không dùng** | Kho `shared-sources/sound-effects` không có hồ sơ giấy phép (theo README của kho). Tiếng gốc của phim có lời nói và nhạc chưa rõ quyền dùng lại. | — |

Không dùng: ảnh sản phẩm trong `Dự án tạo ảnh website - Louis Yoga` (không cần cho concept này), video `b8s5AYDkUqI` (chỉ có trên YouTube, không có file gốc), và mọi tư liệu của creator khác.

## 4. Thông số render (ffprobe, file cuối)

| Thông số | Giá trị |
|---|---|
| Container / codec | MP4 / H.264 High |
| Độ phân giải | 1080×1920, khung 9:16 |
| FPS / số frame | 30/1, 813 frame |
| Thời lượng | 27.100s |
| Dung lượng / bitrate | 29.6 MB / ~8.7 Mbps |
| Pixel format | yuvj420p (dải màu đầy đủ; Remotion vẫn ra yuvj dù đã đặt `--pixel-format=yuv420p`) |
| Audio stream | Không có (đúng chủ ý) |

## 5. Checklist QC

| Mục | Kết quả |
|---|---|
| Lint + typecheck | Đạt |
| Đúng 1080×1920, 30fps, H.264, 25–30s | Đạt (27.1s) |
| Giải mã hết file không lỗi | Đạt |
| Không có khung đen (blackdetect) | Đạt, 0 đoạn |
| Không có đoạn đứng hình (freezedetect ≥ 0.5s) | Đạt, không phát hiện |
| Chính tả 4 dòng chữ | Đạt |
| Chữ không đè lên mặt người | Đạt sau khi sửa (preview v1 bị đè, đã chuyển chữ sang cảnh cận thảm) |
| Crop: đầu và chủ thể | Đạt có ghi chú: tư thế bồ câu có 1–2 giây đầu bị cắt đỉnh đầu vì người mẫu ngả ra sau sát mép khung gốc |
| Logo: không cắt, không đổi màu hay hình dạng | Đạt sau khi sửa (preview v2 cắt sát chữ LOUISYOGA) |
| Logo hiển thị đủ đậm ở cảnh cuối | Đạt sau khi sửa (cắt trước frame logo bắt đầu mờ dần) |
| Chữ nằm trong vùng an toàn (x 80–920, chữ từ y 300) | Đạt theo đề xuất trong guide; **chưa đo trên app Facebook thật** |
| Màu sản phẩm giữ nguyên footage gốc (không grade) | Đạt |
| Âm thanh | Không áp dụng, bản không nhạc |
| Xem thử trên điện thoại / đăng thử Reels | **Chưa làm** |

## 6. Còn chưa xác minh

1. **Quyền hình ảnh người mẫu** (Nguyễn Thị Huyền) khi dựng lại thành TVC mới, đăng quảng cáo trên Facebook Reels. Cần xem hợp đồng hoặc xác nhận từ Louis Yoga (anh Công).
2. Trang phục trong phim gốc có logo nhỏ của thương hiệu khác (áo tập). Đây là chi tiết có sẵn trong phim gốc, không chỉnh sửa. Cần xác nhận có chấp nhận khi chạy quảng cáo không.
3. **Nhạc nền**: cần nhạc có giấy phép thương mại (hoặc nhạc gốc của phim nếu hợp đồng cho phép tái sử dụng) trước khi đăng.
4. Màu và font: đang theo hệ thiết kế website, chưa có quy chuẩn video được duyệt chính thức.
5. CTA dẫn về đâu: louisyoga.vn, fanpage hay sản phẩm cụ thể.
6. Pixel format `yuvj420p`: nên kiểm màu sau khi Facebook nén lại.
