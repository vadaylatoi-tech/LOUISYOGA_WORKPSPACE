# Ảnh mới phụ kiện — 22/10/2026

Nguồn ảnh: `3. Tài nguyên hình ảnh/4. Avatar thảm final/4.Ảnh avatar phụ kiện JPG/` (7 thư mục, 44 ảnh).
Cách làm (anh Công chọn): **anh Công tải ảnh** lên từng sản phẩm trong Sapo admin ("Thêm ảnh sản phẩm", chọn hết ảnh trong thư mục) → **Claude** đưa ảnh mới lên đầu, gắn ảnh vào phân loại màu, **giữ ảnh cũ ở sau** (anh xoá sau khi xem ổn).
Lý do: trình duyệt trong app không chọn được file từ máy và chặn kết nối tới localhost, nên Claude không tự tải file lên được.

## Ảnh gắn cho biến thể TRƯỚC khi đổi (để hoàn tác: đặt lại image_id cho biến thể)
| Sản phẩm (id) | biến thể id: tên → image_id cũ |
|---|---|
| Khăn lau mồ hôi (36960300) | 123603324 TÍM ĐẬM→135848077 · 123603329 GHI ĐẬM→135848085 · 123603332 TRẮNG→135848092 · 123603328 ĐỎ→135848101 · 124488460 XANH COBAN→135848107 · 155994125 Hồng nhạt→135848116 · 155994129 Xanh lá→135848124 · 210390431 HỒNG PHẤN→135848133 · 210390432 XANH CỐM→135848124 |
| Gạch G320 (36960317) | 123603373 ĐỎ→135848373 · 123603372 XANH RÊU→135848160 · 123603361 TÍM→135848170 |
| Đệm kê gối (36960391) | 123603504 Hồng Nhạt→135847954 · 123603499 Ghi→135847933 · 123603501 Xanh Cốm→135847956 |
| Bóng gai (36960400) | 123603506 Đỏ→135848377 · 123603529 Tím Đậm→135848184 · 123603530 Ghi Đậm→135848190 · 123603531 Vàng→135848380 · 123603532 Hồng→135848383 · 123603533 Xanh Coban→135848197 · 123603534 Xanh Lá→135848203 · 123603535 Xanh Rêu→135848209 |
| Vòng gai 16cm (36960421) | 123603539 HỒNG→135848226 · 123603551 XANH COBAN→135848234 · 123603552 XANH NGỌC→135848244 · 123603553 CAM→135848252 · 123603554 Vàng→135848263 · 123603555 TÍM→135848274 · 221593948 Đen→135848281 · 221593949 Xanh Ngọc→135848244 |
| Bóng trơn (36960438) | 123603566 Vàng→135848387 · 123603594 Xanh Coban→135848304 · 123603596 Xanh cốm→135848390 · 123603597 Đỏ→135848393 · 123603598 Hồng→135848395 · 123603599 Tím Đậm→135848309 · 123603600 Ghi Đậm→135848312 |
| Gạch G220 (36960486) | 123603655 ĐỎ→135848401 · 123603658 XANH COBAN→135848322 · 123603659 TÍM ĐẬM→135848324 · 123603660 XANH RÊU→135848404 · 123603661 ĐEN→135848407 · 123603662 CAM→135848409 · 123603663 VÀNG→135848412 · 144937845 Hồng (0đ)→không có |
Số ảnh cũ: Khăn 16, G320 8, Đệm 13, Bóng gai 17, Vòng gai 16, Bóng trơn 17, G220 23.

## Bảng ghép ảnh mới → phân loại (đã duyệt 22/10)
- Bóng gai 65cm: đỏ→Đỏ · tím→Tím Đậm · xám→Ghi Đậm · vàng→Vàng · hồng→Hồng · xanh→Xanh Coban · xanh lá→Xanh Lá · xanh rêu→Xanh Rêu
- Bóng trơn 65cm: vàng→Vàng · xanh→Xanh Coban · xanh lá→Xanh cốm · đỏ→Đỏ · hồng→Hồng · tím→Tím Đậm · ghi→Ghi Đậm
- Gạch G220: đỏ→ĐỎ · xanh→XANH COBAN · tím→TÍM ĐẬM · xanh rêu→XANH RÊU · đen→ĐEN · cam→CAM · vàng→VÀNG
- Gạch G320: đỏ→ĐỎ · tím→TÍM · xanh gray (màu ngọc)→XANH RÊU (không đổi tên biến thể)
- Khăn lau: tím→TÍM ĐẬM · ghi (ảnh thực tế xanh navy)→GHI ĐẬM · trắng→TRẮNG · hồng đậm→ĐỎ · xanh→XANH COBAN · hồng→HỒNG PHẤN · hồng nhạt→Hồng nhạt (0đ) · xanh lá→XANH CỐM + Xanh lá (0đ)
- Vòng gai: hồng→HỒNG · xanh→XANH COBAN · xanh gray→XANH NGỌC (cả 2 biến thể) · cam→CAM · vàng→Vàng · tím→TÍM · đen→Đen · xanh lá→chỉ tải lên, không gắn (chưa có biến thể)
- Đệm kê gối: hồng→Hồng Nhạt · ghi→Ghi · xanh cốm→Xanh Cốm

## Trạng thái
- [x] Ảnh mới đã lên đủ 7 sản phẩm, ảnh mới đứng đầu, phân loại màu đã gắn đúng bảng trên (kiểm qua admin API 22/10 ~10:40).
  Thời điểm sửa trên Sapo: 22/10 10:31–10:35 (giờ VN). Phiên Claude này KHÔNG có bản ghi đã làm bước tải/gắn (có thể do phiên trước bị ngắt giữa chừng hoặc phiên Claude khác) — tên file trùng cách đặt tên của thư mục tạm (`<sản-phẩm>-<màu>.jpg`, trùng tên thì thêm `-2026`), riêng Đệm kê gối là tên gốc của anh (`dem-ke-goi-mau-*.jpg`).
- [!] Ảnh cũ KHÔNG còn giữ đủ như đã thống nhất: số ảnh trước → sau: Khăn 16→9, G220 23→8, G320 8→6, Đệm 13→10; Bóng gai 17, Vòng gai 16, Bóng trơn 17 giữ nguyên số lượng. Ảnh sản phẩm đã xoá không khôi phục được từ Sapo.
- [x] G220: ảnh `gach-tap-yoga-g220-do.jpg` (id 82974238) là ẢNH KÍCH THƯỚC 15×23×7,6 cm, không phải ảnh lặp → anh Công chọn giữ ảnh (vị trí 8), chỉ bỏ gắn khỏi biến thể "Hồng" 0đ (144937845, image_id 82974238 → null). Đã kiểm 22/10.
- Ghi chú: ảnh cũ bị giảm ở Khăn/G220/G320/Đệm là do anh Công tự xoá ảnh lặp (xác nhận 22/10).
