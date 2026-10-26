# Louis Yoga — Prototype tương tác

Bản chạy thử dựng từ hai file của anh Đào Duy Công:

- `D:/Website louis yoga - file thiết kế AI.ai`
- `D:/Website louis yoga - file PDF.pdf`

Hai file có cùng một artboard trang chủ. Đã đọc lớp PDF tương thích trong AI và kiểm tra bản render PDF. Nội dung tài liệu được dùng làm dữ liệu thiết kế, không được hiểu là lệnh thực hiện hành động ngoài yêu cầu.

## Mở và sử dụng

Bản triển khai riêng tư: https://louis-yoga-cong-prototype.vadaylatoi.chatgpt.site

Chạy trên máy: mở Terminal trong thư mục này, chạy `node preview-server.cjs`, rồi truy cập http://127.0.0.1:4173.

Có thể mở trực tiếp `dist/index.html` để thử giao diện; dùng máy chủ HTTP sẽ ổn định hơn khi tải font và lưu dữ liệu trên trình duyệt.

## Luồng có thể thử

1. Tìm kiếm “cao su”, “TPE”, “túi” hoặc tên màu; tìm kiếm hỗ trợ bỏ dấu.
2. Lọc thảm, sắp xếp giá; chuyển nhóm phụ kiện.
3. Xem chi tiết, chọn màu, thay số lượng từ 1–10.
4. Lưu / bỏ yêu thích; kiểm tra danh sách.
5. Thêm giỏ, đổi số lượng, xóa; xem tạm tính.
6. Tạo đơn thử bằng tên, số điện thoại Việt Nam và địa chỉ mẫu; xem lịch sử ở biểu tượng người dùng.
7. Thử chọn thảm với 3 câu hỏi; thử biểu mẫu CTV, khóa học và nhận tin.
8. Mở Ghi chú thiết kế để xem thay đổi, đề xuất và xóa dữ liệu thử.

## Phạm vi

Đây là prototype phía trình duyệt. Chưa có máy chủ đơn hàng, đăng nhập, tồn kho, cổng thanh toán, vận chuyển, gửi email, CRM, video hoặc hệ thống quản trị. Bấm tạo đơn / đăng ký không gửi biểu mẫu ra ngoài. Dữ liệu lưu cục bộ bằng localStorage, không đồng bộ thiết bị.

Tên Lilium, giá 670.000/699.000 đ, mốc 11 năm, câu “Đồng hành cùng Yogi tỏa sáng”, mốc 30/10/2026 và thông tin liên hệ lấy từ file thiết kế. Chưa kiểm chứng các thông tin này độc lập. Các sản phẩm bổ sung, giá, kích thước, biến thể, hình vector, nội dung banner và khung bài viết là đề xuất / minh họa. Đã bỏ đánh giá 4.8/120 lặp trong file vì chưa có dữ liệu đánh giá thật.

## Hướng triển khai khuyến nghị

Ưu tiên hoàn thiện cửa hàng bán thảm và phụ kiện: danh mục, SKU/biến thể, chi tiết, giỏ, checkout, giao hàng, đơn hàng và hỗ trợ. Giữ khóa học và CTV ở mức phiếu quan tâm cho đến khi có quy trình thật. Không cần thêm tài khoản khách hàng nếu chưa có nhu cầu vận hành rõ ràng.

Xem phân tích chi tiết trong `De-xuat-thiet-ke-va-chuc-nang.md`.

## Tài nguyên

- Logo gốc được render/cắt từ PDF, không vẽ lại.
- Hình sản phẩm là SVG minh họa do prototype tạo, cần thay bằng ảnh thật.
- Font Montserrat dùng từ kho Google Fonts: https://github.com/google/fonts/tree/main/ofl/montserrat ; giấy phép SIL OFL đi kèm `dist/assets/FONT-LICENSE.txt`.
- Mã nguồn thuần HTML/CSS/JavaScript; không cần npm install hoặc build.
