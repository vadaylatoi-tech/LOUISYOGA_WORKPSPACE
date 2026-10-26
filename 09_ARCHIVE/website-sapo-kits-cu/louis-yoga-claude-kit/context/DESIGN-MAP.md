# Bản đồ thiết kế và dữ liệu

Đã trích xuất text và xem bản render tổng quan của 3 trang PDF PC, 11 trang PDF mobile. Đây là bản đồ phạm vi, không phải nghiệm thu pixel của website. Claude cần crop/render vùng chi tiết khi triển khai. Kích thước PDF là đơn vị bản vẽ; không lấy trực tiếp làm CSS px. Hai SVG mô phỏng khoảng 39 MB/file và PDF khoảng 83/95 MB nên đọc theo vùng.

| Màn hình/trạng thái | PDF PC | PDF mobile | Cần triển khai |
|---|---:|---:|---|
| Trang chủ | 1 | 1 | Header, hero PC/mobile, danh mục, sale, tab phân khúc, phụ kiện, màu, video, story, báo chí, footer |
| Danh sách sản phẩm | 2 | 2 | Filter, sort, kết quả, phân trang/xem thêm, CTA CTV/bảo hành |
| Bộ lọc mobile mở | — | 3 | Drawer, chọn/xóa bộ lọc, focus, overlay và đóng |
| Menu mobile mở nhóm | — | 4 | Accordion phân khúc/phụ kiện/tài khoản, search |
| Về chúng tôi | Chưa có trang riêng | 5 | Hero/story, nội dung, video, footer; desktop kế thừa hệ thống thiết kế |
| Chi tiết sản phẩm | 3 | 6 | Gallery, variant, giá/tồn, số lượng, mua hàng, mô tả, review, liên quan |
| Menu mobile thu nhóm | — | 7 | Cùng một menu, trạng thái đóng/mở |
| Product mobile/sticky CTA | — | 8 | Thanh dưới: liên hệ, thêm giỏ, mua ngay, safe-area |
| Home mobile/sticky CTA | — | 9 | Thanh liên hệ/cửa hàng; không chép khung đen mô phỏng thiết bị |
| Giỏ hàng có sản phẩm | Chưa có trang riêng | 10 | Drawer, variant, quantity, remove, gợi ý, subtotal, checkout |
| Giỏ hàng trống | Chưa có trang riêng | 11 | Empty state, tiếp tục mua, tài khoản |

## Hệ thống hình thức
Logo website SVG dùng màu `#d82183` trong file gốc; đây là màu logo, chưa khẳng định mọi nút dùng đúng mã này. Đo màu nút/chữ/nền từ bản thiết kế khi lập token. Font nguồn chủ yếu Montserrat OTF nhiều weight/italic; có một file MontserratAlternates-ThinItalic, không tự áp dụng cho toàn site. Chỉ chuyển những weight cần dùng sang WOFF2, giữ glyph tiếng Việt, kiểm tra quyền sử dụng theo metadata/license nếu có.

Giữ bố cục, thứ tự, tỷ lệ crop, ảnh, typography và mức độ đậm nhạt của thiết kế. Dùng HTML/CSS thật và dữ liệu động. Không phủ một ảnh chụp dài lên trang. Responsive theo nội dung giữa các mốc; không scale nguyên artboard. Mục tiêu kiểm tra 360/390/430/768/1024/1440 px và viewport tương ứng thiết kế sau khi xác định tỷ lệ.

## Tài nguyên đã tìm thấy
- Hero: `ly-hero-pc.jpg`, `ly-hero-mb.jpg`.
- Banner phân khúc: `ly-seg-harmony.jpg`, `ly-seg-balance.jpg`, `ly-seg-mastery.jpg`.
- Background: `Ảnh danh mục - PC.jpg`, hai ảnh về chúng tôi; tên chính xác trong inventory.
- Logo sử dụng trong website và logo đầy đủ là hai SVG khác nhau; chọn theo vị trí thiết kế.
- Avatar theo thư mục từng dòng thảm/phụ kiện. Không lấy tên folder làm product ID; map SKU/handle/variant đã xác minh.

Lập `context/asset-map.csv` khi build với: source_relative_path, output_key, sha256, dimensions, page/component, crop/focal_point, product_id/variant_id nếu có, status. Tránh trùng basename; key dẫn xuất ASCII/chữ thường nhưng giữ tên gốc ở manifest.

## Những chi tiết cần nguồn thật
| Thành phần | Nguồn cần xác minh | Khi chưa có |
|---|---|---|
| Giá, giá cũ, badge giảm | Product/variant Sapo; tính nhất quán | Không hard-code giá trong mockup |
| Swatch màu, độ dày | Variant options/tags/metafields hiện có | Không đoán variant từ vị trí mảng |
| Filter đánh giá | App review hoặc trường được đồng bộ | Tắt filter này nếu không có nguồn; nêu ảnh hưởng |
| Review website/Shopee | App hoặc tích hợp thực, API được cho phép | Không tạo review/sao hoặc nhãn đã mua giả |
| Countdown | Cấu hình chiến dịch với timezone +07:00 | Tắt/hiện hết hạn; không reset mỗi lần load |
| Miễn phí vận chuyển/quà tặng | Quy tắc vận hành và checkout | Không hứa miễn phí chỉ từ subtotal nếu còn điều kiện |
| CTV, bảo hành | URL/app/form hiện có | Dẫn tới trang thật phù hợp; không gửi form giả |
| Video/báo chí | URL, poster, nội dung đã duyệt | Ẩn hoặc đánh dấu thiếu trong preview, không xuất bản nút chết |
| Wishlist | Cơ chế cũ hoặc lựa chọn mới được chốt | Nếu localStorage phải thống nhất giữa header/card/page, không nói đồng bộ tài khoản |
| Newsletter | Dịch vụ/form thực | Test không gửi thật hoặc dùng môi trường test |

## Phạm vi bổ sung để website dùng trọn vẹn
Search có/không kết quả, cart page fallback, blog/article, contact/policies, account routes, 404, các trang CTV/bảo hành đang liên kết. Những trang chưa có mockup giữ chức năng hiện tại và dùng style chung; ghi rõ mức thiết kế suy diễn để chủ shop duyệt. Không bỏ trang cũ chỉ vì PDF không có.

Nguồn mới quyết định hình thức; theme remote mới nhất quyết định hợp đồng dữ liệu. Nếu bản vẽ khác số liệu/copy đang bán hàng, ghi quyết định vào `context/DECISIONS.md` thay vì âm thầm chọn.
