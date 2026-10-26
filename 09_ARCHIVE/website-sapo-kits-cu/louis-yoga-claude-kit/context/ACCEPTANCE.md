# Điều kiện nghiệm thu

Ghi PASS/FAIL/NOT_TESTED/NOT_APPLICABLE cùng URL/theme ID/commit/viewport/thời điểm/bằng chứng. Không đánh dấu PASS vì có code. File QA được tạo ở `reports/`; dùng `templates/qa-results.csv`.

## Hình thức và tương tác
- So sánh ảnh chụp từng trang/vùng với bản thiết kế tương ứng cùng viewport. Giữ tỷ lệ/crop, font weight, chiều cao header, nhịp khoảng cách, cỡ chữ, màu nút; ghi sai khác được chấp nhận. Không đặt tỷ lệ “giống 100%” khi chưa đo.
- 360/390/430/768/1024/1440 px, không tràn ngang; tiếng Việt không mất dấu; chữ dài không vỡ; ảnh không méo; không có banner xám placeholder xuất bản.
- Menu desktop, mobile đóng/mở, accordion, overlay, Escape, focus trap và trả focus; sticky CTA không che nội dung/keyboard; safe-area iPhone.
- Tab Harmony/Balance/Mastery, carousel nếu có, video, link category/color, mọi CTA có đích/hành vi thực.

## Mua hàng
- Product một và nhiều variant, sold out, variant không hợp lệ, giá đổi theo variant, quantity min/max; trạng thái đang gửi/lỗi rõ ràng.
- Product card/quick action chọn đúng variant; “Mua ngay” không bỏ qua lựa chọn bắt buộc. Add-to-cart không nhân đôi khi bấm nhanh/retry.
- Cart empty/filled, quantity/remove, subtotal, badge header, drawer và cart page nhất quán sau reload; lỗi mạng và stock server trả về được xử lý.
- Đi đến checkout với đúng variant/quantity/currency. Chưa tạo đơn thật nếu không có phạm vi thử nghiệm. Phí vận chuyển/discount cuối cùng do checkout quyết định.
- Filter/sort/pagination giữ trạng thái hợp lý, URL/back button; lọc toàn catalog theo cơ chế Sapo, không chỉ lọc sản phẩm của trang hiện tại rồi gọi là hoàn tất.
- Search có dấu/không có kết quả; account/wishlist/CTV/review/newsletter đúng hệ thống thật. Missing integration phải hiện trong báo cáo.

## Nền tảng và nội dung
- Liquid render trên Sapo, không lộ tag template, không lỗi schema/include. Trình render Liquid local không phải bằng chứng tương thích Sapo.
- Kiểm tra hooks nền tảng và app, menu settings, các route hiện có; giá/tồn không hard-code. Bảo toàn chức năng trang chưa thiết kế lại.
- Link, form, hotline, chính sách, video, social, bài báo đúng đích. Không suy luận nội dung pháp lý hoặc số liệu quảng cáo từ hình mẫu.
- Không secret trong HTML/JS/network bundle. Theme ZIP chỉ có file thuộc allowlist.

## Truy cập, SEO và hiệu năng
- HTML semantic, label/alt, focus thấy được, bàn phím, contrast, reduced-motion; test drawer bằng bàn phím.
- Title/meta/canonical đúng route, H1 hợp lý, ảnh có alt, structured data dùng dữ liệu thật; không dựng rating schema từ mẫu. Giữ URL/redirect cũ trong phạm vi; không để noindex dành preview lọt vào live.
- Responsive images srcset/sizes theo CDN đã xác minh, width/height chống nhảy layout; lazy-load dưới màn hình, hero không lazy vô điều kiện; font-display và preload có chọn lọc.
- Đo Lighthouse/mobile với điều kiện ghi rõ; mục tiêu dự án LCP ≤2,5s, CLS ≤0,1; INP mục tiêu ≤200ms cần dữ liệu trường/RUM khi có, không lấy Lighthouse TBT làm INP thực. So sánh baseline và ghi ảnh hưởng app ngoài theme, không bịa điểm.
- Console/network không lỗi cản mua hàng; assets/font trả đúng MIME, không mixed content. Kiểm tra browser đang có; iOS Safari/Android thật ghi NOT_TESTED nếu chưa kiểm tra.

## Cổng phát hành
Blocker: sai giá/variant, không thêm giỏ/checkout, lỗi Liquid, lộ bí mật, sai shop/theme, thiếu backup/restore target, payload chưa xác định kết quả. Lỗi hình thức nghiêm trọng trên mobile phải sửa trước. Các chênh lệch nhỏ ghi cụ thể để duyệt. Báo cáo cuối tách local tests, Sapo preview tests và live tests.
