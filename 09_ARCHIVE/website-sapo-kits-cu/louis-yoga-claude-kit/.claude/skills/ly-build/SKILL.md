---
name: ly-build
description: Xây theme Sapo Louis Yoga theo thiết kế PC và mobile đã duyệt, nối dữ liệu thật và nghiệm thu trên preview.
---

# Xây theme Louis Yoga
Phạm vi bổ sung: $ARGUMENTS

Đọc CLAUDE.md và context/STATE.md; chỉ đọc mục thiết kế/test liên quan trong context/PROJECT.md, context/DESIGN-MAP.md, context/ACCEPTANCE.md. Trước ghi đọc mục 1–2 của context/OPERATIONS.md. Người dùng muốn theme thương mại hoạt động đầy đủ, không chỉ ảnh mô phỏng.

**Chế độ nhanh (17/10, xem CLAUDE.md):** khi ghi draft, bỏ backup remote/MANIFEST/LOCK/hash CDN và báo cáo chi tiết; chỉ cần: sửa `theme/` → PUT draft → so size → kiểm tra 390/1440 → Git commit → 1 dòng STATE. Không đọc OPERATIONS trước mỗi lần ghi draft.

## Khảo sát và chuẩn bị
Khi bắt đầu mới hoặc nguồn đổi mới kiểm kê; khi nối phiên dùng STATE, kiểm tra kết nối tối thiểu và chỉ gọi ly-connect nếu có lỗi/thay môi trường. Không đọc lại toàn inventory. Khi cần thiết kế, đọc/crop thiết kế theo trang, xác định layout/header/footer/product card/states. Không tải SVG/PDF khổng lồ nguyên văn vào context. Liệt kê trang có thiết kế và trang cần giữ/suy diễn. Chốt design tokens theo file, asset map theo inventory, route/data map từ theme và shop. Phân biệt layout mockup với nội dung động và nội dung chờ xác minh.

Đọc remote mới nhất và áp dụng baseline theo OPERATIONS, kể cả ngoại lệ backup từng key đã ghi cho draft hiện tại. Không khởi động lại baseline/main-sync khi nối phiên; không miễn snapshot đầy đủ cho release. Kiểm tra các bản cũ có thay đổi mới trước khi chọn nền; không ghi đè từ outputs cũ. Xác định draft chưa xuất bản và tránh main/mobile đang phục vụ khách. Nếu chưa có draft, chuẩn bị bản sao bằng cơ chế đã xác minh trong phạm vi build; không tự xuất bản. Khởi tạo Git ở workspace build nếu chưa có; tạo checkpoint baseline sau khi đã loại bí mật.

## Thực hiện
1. Khung theme Sapo tương thích cấu trúc thật; hooks header/body, schema/settings, CSS/JS chung và font Montserrat WOFF2 dẫn xuất. Không dùng feature của Shopify mà Sapo chưa chứng minh hỗ trợ.
2. Header/menu PC/mobile, search, footer, product card, drawer và sticky CTA dùng component/snippet thống nhất, selector có namespace để tránh CSS cũ đè lẫn.
3. Trang chủ: hero PC/mobile, danh mục, sale thực, tab 3 phân khúc, phụ kiện, màu, video, story, báo chí. Nội dung/ảnh/link phổ biến chỉnh được qua theme settings phù hợp khả năng Sapo.
4. Collection/filter/sort/pagination, product gallery/variant/stock/quantity/cart. Giữ data contract của cart hiện có; xác minh endpoint/payload thật từ code/tài liệu, không tự bịa đường dẫn. Các request có loading/error/disable chống nhấp lặp.
5. About và các trang phụ: blog/article/search/cart/account/contact/policy/404. Giữ tích hợp CTV/review/newsletter/tracking đã xác minh. Ghi giới hạn checkout và module chưa có dữ liệu.
6. Asset dẫn xuất tối ưu, giữ crop/focal point, responsive images; không sửa nguồn gốc. Không hard-code 12 sản phẩm vào template thay vòng lặp dữ liệu thật.

Làm theo mốc nhỏ nhưng tiếp tục cho đến hoàn tất phạm vi được giao; không dừng ở kế hoạch. Khi cần quyết định thật sự, hỏi ngắn và tiếp tục phần độc lập. Mỗi mốc có checkpoint, diff, test tương ứng, upload draft và đọc lại nếu kết nối cho phép. Nếu remote đổi, so diff và hợp nhất, không cưỡng bức ghi.

## Nghiệm thu và bàn giao
Chạy ACCEPTANCE, chụp ảnh so thiết kế ở kích thước tương ứng. Tách kiểm tra local và Sapo preview; chưa thấy render Sapo thì chưa gọi hoàn tất. Test variant sold-out và cart empty/filled/error. Không gửi form/đơn thật ngoài phạm vi được cho phép. Sửa lỗi phát hiện và kiểm tra lại phần chịu ảnh hưởng.

Đầu ra: theme/, generated/, asset-map, route/data map, reports/design-diff.md, reports/qa-results.csv, build/upload manifest, preview URL, STATE và quyết định. Khi đầy đủ, chuẩn bị release candidate để người dùng xem; không tự apply live nếu chỉ yêu cầu build.
