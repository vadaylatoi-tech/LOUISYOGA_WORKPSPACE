# Đánh giá và đề xuất cho website Louis Yoga

## Kết luận

Nên triển khai Louis Yoga trước hết như một cửa hàng thảm và phụ kiện yoga. Thiết kế có nhận diện màu nhất quán và thứ tự khối phù hợp, nhưng chưa đủ dữ liệu để mở bán. Prototype giúp xem trực tiếp hành vi trên desktop/điện thoại và kiểm tra luồng mua.

## Dữ kiện từ file thiết kế

- Một artboard desktop dài, cùng bố cục giữa AI và PDF.
- Logo Louis Yoga; màu hồng, hồng nhạt, đỏ rượu; font Montserrat/Inter trong nguồn.
- Header có cửa hàng, về chúng tôi, tin tức, tìm kiếm, yêu thích và giỏ hàng.
- Các khối: hero 11 năm → ưu đãi → thảm → CTV/khóa học → phụ kiện → truyền thông → nhận tin → footer.
- Sản phẩm Lilium được lặp nhiều lần, cùng mức giá và đánh giá. Ô ảnh chủ yếu chưa có nội dung.
- Dòng “Sale gì đó!!!”, bộ đếm “99”, điều kiện freeship còn trống; tên nhóm “Thảm Yoga Sao Su” và “Dũng cụ” có lỗi chính tả.
- Có tên bài báo và khung video, nhưng không có URL/video gốc.

Những điều trên xác minh được từ tài liệu, không phải xác minh tình trạng kinh doanh ngoài thực tế.

## Điểm mạnh, điểm yếu và cách cải thiện

| Hạng mục | Đánh giá | Cách cải thiện trong prototype |
|---|---|---|
| Nhận diện | Màu hồng tạo liên kết rõ giữa các khối; đỏ rượu giúp phân cấp | Giữ bảng màu và logo gốc; dùng hồng chủ yếu cho CTA, nhấn tiêu đề; tăng tương phản chữ nhỏ |
| Hero | Thông điệp chính rõ; ô ảnh trống nên chưa hình dung được sản phẩm | Thêm minh họa thảm; CTA đến danh mục; thêm lối chọn thảm |
| Ưu đãi | Nội dung chưa hoàn chỉnh và đếm ngược không có giá trị thực | Đổi tên khối rõ; bộ đếm đến ngày trong nguồn, xử lý hết hạn; ghi là mốc mẫu |
| Danh mục | Sản phẩm lặp khiến người dùng không so sánh được | Dùng sản phẩm mẫu khác nhau; lọc chất liệu, sắp xếp giá; bỏ đánh giá chưa có bằng chứng |
| Thẻ sản phẩm | Nút nhỏ, thông tin chật, ảnh trống | Phân cấp loại/tên/màu/giá; nút mua thử và thêm giỏ; bỏ thông tin dư |
| Hai banner CTV/khóa học | Có vị trí nhưng thiếu cách chuyển đổi | Biểu mẫu quan tâm đơn giản; chưa tạo lịch học hoặc mức chiết khấu giả |
| Video/báo chí | Có tên nhưng thiếu tư liệu | Mở khung nội dung đề xuất; chờ URL/ảnh/video được phép sử dụng |
| Mobile | Chỉ có bố cục desktop trong file | Menu thu gọn, sản phẩm 2 cột, giỏ dạng drawer, form 1 cột |

## Luồng mua đề xuất

Trang chủ → tìm/lọc → chi tiết → màu/số lượng → giỏ → thông tin nhận hàng → tạo đơn → lịch sử đơn.

Bản thử triển khai đầy đủ chuỗi này ở trình duyệt. Tạm tính chưa bao gồm phí giao hàng; không có thanh toán thật hoặc xác nhận từ máy chủ. Hệ thống thực cần tính lại giá, tồn kho, khuyến mãi và vận chuyển ở máy chủ, không tin tổng tiền phía trình duyệt.

## Hai phương án triển khai

| Phương án | Trọng tâm | Ưu điểm | Rủi ro / dữ liệu cần |
|---|---|---|---|
| A — Cửa hàng tinh gọn (khuyến nghị) | Thảm, phụ kiện, đơn hàng và hỗ trợ; CTV/khóa học là phiếu quan tâm | Bám nội dung chủ đạo trong thiết kế; tập trung nguồn lực hoàn thiện luồng mua | Cần ảnh sản phẩm, SKU, tồn kho, giá được duyệt, thanh toán/vận chuyển và chính sách |
| B — Cửa hàng + cộng đồng/khóa học | Bổ sung lịch lớp, tư liệu video, tài khoản, CTV hoặc nội dung theo người dùng | Phù hợp khi doanh nghiệp có người phụ trách nội dung và đào tạo | Nhiều công quản trị; cần lịch/lớp/giảng viên/học phí, dữ liệu hồ sơ, quy trình CTV và quyền dùng tư liệu |

Chọn A cho giai đoạn đầu. Chỉ mở rộng sang B khi những chức năng đó có chủ sở hữu vận hành và dữ liệu thực, tránh các mục chưa cập nhật làm giảm độ tin cậy.

## Dữ liệu cần trước khi mở bán

1. Ảnh thật mỗi sản phẩm/biến thể và quyền sử dụng ảnh.
2. Danh sách SKU, tên, giá, chất liệu, kích thước, trọng lượng, hướng dẫn và tồn kho đã xác nhận.
3. Điều kiện ưu đãi, mốc chương trình, ngưỡng freeship và cách xử lý hết hạn.
4. Chính sách giao hàng, kiểm hàng, đổi trả, bảo hành, bảo mật và điều khoản được duyệt.
5. Xác nhận tên pháp nhân, địa chỉ, mã số thuế và các kênh liên hệ từ footer.
6. Nguồn bài báo, video, ảnh người tập được phép dùng; không thêm đánh giá giả.
7. Kênh nhận/xử lý đơn, người quản trị, cổng thanh toán và quy trình thông báo trạng thái.

## Các đề xuất đã có trong bản thử

- Công cụ chọn thảm 3 câu hỏi: minh họa cách tư vấn, chưa tư vấn dựa trên thông số thật.
- Tìm kiếm hỗ trợ bỏ dấu; lọc và sắp xếp.
- Yêu thích, giỏ hàng và lịch sử đơn lưu cục bộ.
- Kiểm tra trường bắt buộc và số điện thoại khi đặt hàng thử.
- Phiếu CTV, khóa học và nhận tin chỉ lưu cục bộ.
- Ghi chú thiết kế ngay trong website để phân biệt nguồn / minh họa / đề xuất.
- Hỗ trợ bàn phím, Escape, focus trong giỏ, nhãn nút và chế độ giảm chuyển động.
