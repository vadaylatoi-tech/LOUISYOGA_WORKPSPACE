# Hồ sơ dự án — 15/10/2026

Hồ sơ nền lập lúc khởi tạo; trạng thái triển khai và quyết định mới hơn xem context/STATE.md. Không dùng câu hỏi khởi tạo bên dưới để hỏi lại quyết định đã có.

## Yêu cầu đã xác nhận
Chủ dự án hoàn thiện mô phỏng PC/mobile, ảnh và font, muốn dùng Claude Code triển khai theme Sapo cho https://louisyoga.vn. Đã có API/ứng dụng riêng. Bộ này là prompt, skill và ngữ cảnh chuẩn bị triển khai; chưa thực hiện kết nối API hay xuất bản trong lần bàn giao này.

## Nguồn chính
Thư mục gốc: `D:/Tổng dư liệu - Duy Công/Dự án - Thay đổi giao diện website sapo`.
- `1. File thiết kế`: AI, PDF, SVG; Montserrat OTF; 2 logo SVG.
- `2. Skill thiết kế/frontend-design-codex.zip`: hướng dẫn tham khảo về thiết kế. Không tự cài metadata dành riêng cho Codex vào Claude Code. Bản thiết kế đã duyệt ưu tiên hơn lựa chọn thẩm mỹ chung.
- `3. Tài nguyên hình ảnh`: ảnh avatar thảm, phụ kiện và background.
- `context/source-inventory.csv`: danh sách chính xác, kích thước, hash và kích thước ảnh khi đọc được. Đây là kiểm kê tại ngày bàn giao; chạy lại nếu nguồn thay đổi.
- `context/DESIGN-MAP.md`: trang PDF → chức năng → điều kiện dữ liệu.

Không đưa AI/PDF/SVG mô phỏng nặng lên storefront. Render cục bộ từng trang/vùng cần đối chiếu. PDF có ký tự trích xuất dạng `/uni...`; phải nhìn bản render và kiểm tra tiếng Việt, không dán thẳng text lỗi vào theme.

## Kết quả lịch sử hữu ích, cần kiểm tra lại
Trong workspace cũ có khảo sát ngày 08/10/2026 và báo cáo triển khai preview:
- Admin host: `hung-yen-sport.mysapo.net`.
- Theme main lúc đó: `983840`, Louis Yoga 26-12.
- Theme preview lúc đó: `1151386`, Louis Yoga 26-12 - Copy.
- Preview từng dùng: `https://louisyoga.vn/?previewThemeId=1151386`.
- Wrapper `sapo-connection/sapo.ps1`, khóa `credentials.dpapi`; Basic Authentication; quyền được ghi nhận: đọc/ghi theme và tài nguyên CSS/JS, không có quyền sản phẩm/đơn hàng.
- Báo cáo cũ ghi đã cập nhật 18 tệp trang chủ lên preview và đọc lại; không chứng minh trạng thái ngày hôm nay.
- Có mã thử trước đây tại `outputs/sapo-site/` và `outputs/sapo-preview-deploy/`. Xem như nguồn tham khảo, không mặc định đó là bản chuẩn mới nhất.
- Lần đóng gói trước có lỗi HTTP 413; một ZIP 4,70 MB được tạo để thử lại nhưng ghi nhận lúc đó chưa xác nhận import thành công. Không coi 5 MB là giới hạn chính thức của Sapo.

Đường dẫn workspace cũ nằm trong `project.config.json`. Không mang nguyên `sapo-connection` vào ZIP, Git hay gói theme: chứa khóa và dữ liệu local.

## Nguyên tắc nội dung và kinh doanh
Harmony: Aura, Asana, Moon, Sunflower. Balance: Asana25, Basic, Basiczen, Queen. Mastery: Diamond, F23, Lilium, Nature. Đây là phân nhóm theo thư mục nguồn, chưa phải xác nhận handle/ID của Sapo.

Không tự tạo đánh giá 4.8/174, sale 17%, giá, số lượng, quà tặng, ngưỡng miễn phí vận chuyển hoặc thời gian đếm ngược từ mô phỏng. Map tới nguồn dữ liệu/cấu hình có chủ sở hữu. Thiếu nguồn thì có trạng thái tắt/ẩn phù hợp và ghi rõ trong nghiệm thu.

Giữ URL có giá trị SEO, tracking và tích hợp đang hoạt động; kiểm chứng tránh chèn trùng. Tài khoản CTV, đánh giá Shopee, newsletter, video và wishlist cần xác định hệ thống hiện hữu. Checkout do nền tảng quản lý: chỉ thay phần được Sapo hỗ trợ và đã xác minh.

## Thông tin còn thiếu khi bắt đầu
Claude tự đọc lại phần có thể: role/ID hiện tại, cấu trúc asset, schema, settings, app hooks, baseline code. Chỉ hỏi người dùng phần không thể tự tìm:
1. Cho phép dùng theme preview nào nếu có nhiều bản đang làm song song?
2. Nguồn dữ liệu thật cho đánh giá, newsletter, CTV, video, chiến dịch.
3. Quy tắc “Mua ngay”, wishlist dùng chung và các tính năng chưa có backend.
4. Chốt số hotline khi khác nhau: thiết kế có chỗ 0688.293.996, header/site có 0888.293.996; xác nhận từ cấu hình/chủ shop.
5. Các trang thiếu mẫu desktop/mobile và ngày/giờ phát hành mong muốn.

Không cần hỏi tất cả ngay lập tức. Gộp câu hỏi theo mốc và tiếp tục phần không phụ thuộc.
