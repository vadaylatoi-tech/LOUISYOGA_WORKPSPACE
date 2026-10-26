# Góp ý trang chủ của anh Công — 16/10/2026 (việc cần làm phiên sau)

Đã có trên draft 1170160: trang chủ editorial (tag Git `build-2026-10-16-home-editorial`, backup `backups/pre-home-20261016-1000/`). File: `snippets/lyx-home.bwt`, `snippets/lyx-flags.bwt`, `assets/lyx-home.css|js`, `assets/lyx-base.css`. Chưa publish.

## Nguyên tắc chung mới
- **Bản mobile giữ bố cục như bản thiết kế PDF mobile trang 1** (thanh đen YOGA MAT + banner + cột tab trái, danh mục ô nhỏ, sale box…), chỉ áp màu/chữ/nút editorial. PC giữ hướng editorial đã duyệt.
- Không dùng icon trang trí kiểu hoa sen dưới tiêu đề.

## 7 việc
1. **Bỏ icon hoa sen** (`{{ lyx_lotus }}`, `.lyx-lotus`) dưới mọi tiêu đề trên toàn trang.
2. **"Danh mục phổ biến"** (5 ô tròn): ảnh đang là ảnh sản phẩm có logo/chữ, kém sang → thay bằng icon line tinh tế hoặc ảnh lifestyle chuyên nghiệp (được dùng ảnh mạng **không có logo hãng khác**, phải có quyền dùng; ưu tiên Unsplash/Pexels, ghi nguồn vào asset-map).
3. **Sao đánh giá trên thẻ sản phẩm** (`snippets/ly-home-card.bwt`, class `.lyx-card-rate`) hiển thị sai (vd. "(24.1)", "(17.6)", sao xám rỗng). Phải gộp **web (app đánh giá Sapo) + Shopee** (`snippets/ly-shopee-reviews-data.bwt`: lysr_t/lysr_a/lysr_d) giống trang SP (`assets/lyx-pdp.js`): hiện điểm TB 1 chữ số + số lượt. Không đưa điểm Shopee vào schema.
4. **Khối Video**: dùng 7–8 video TikTok + YouTube Shorts thật của Louis Yoga (anh cung cấp link hoặc em tìm kênh chính thức rồi xác nhận với anh); **dưới mỗi video gắn sản phẩm xuất hiện trong video** (ảnh nhỏ + tên + giá + nút) — thiết kế gốc có ô sản phẩm dưới video. Cần bảng map video → handle sản phẩm (anh xác nhận). Tiêu đề video có dấu.
5. **Khối Màu sắc**: bản editorial xấu hơn bản thiết kế → quay về kiểu ô màu bo góc chữ giữa như thiết kế, chọn **các màu bán chạy nhất** (tính từ đơn hàng/tồn: cần anh xác nhận nguồn số liệu hoặc em đọc báo cáo bán hàng Sapo nếu được cấp quyền — chỉ đọc).
6. **Header (thanh đỏ rượu + menu)** đang "cùi" → làm hiệu ứng giống **site live hiện tại** (khảo sát louisyoga.vn bản main 1170134: animation thanh thông báo/ menu/ sticky) rồi áp vào `snippets/lyx-header.bwt` + `lyx-base.css`.
7. **Hero mobile**: video đang hiện nút điều khiển YouTube (pause/prev/next) và bị cắt → mobile dùng **đúng khung thiết kế** (tỉ lệ ảnh `ly-hero-mb.jpg` 875×1451, thấy tổng thể khi vào trang), không lộ điều khiển. Ưu tiên MP4 dọc (anh gửi); nếu còn dùng YouTube phải che/không cho bấm điều khiển (pointer-events, `controls=0` đã có — kiểm tra lại overlay của YouTube).

## Còn treo từ trước
- MP4 hero (ngang 1920×1080 + dọc 1080×1920, không tiếng, <10MB) → điền `lyx_hero_mp4_pc/mb` trong `lyx-flags.bwt`.
- App đánh giá thiếu `jquerymodal` (nút Viết đánh giá); ảnh `lyx-cat-mats/story/about.jpg` chưa lên Sapo; H1 danh mục ẩn ở mobile; popup "Trợ lý chọn thảm" lệch tông.
