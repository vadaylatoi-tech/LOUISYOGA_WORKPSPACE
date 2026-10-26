# Kết quả kiểm tra prototype

Đã kiểm tra bằng trình duyệt Codex trên bản mã nguồn cuối, ngày 06/10/2026 (Asia/Bangkok).

| Kiểm tra | Kết quả quan sát |
|---|---|
| Desktop 1366 × 900 | Không tràn ngang, mọi ảnh tải được; đã lưu ảnh trang chủ và toàn trang |
| Mobile 390 × 844 | Menu hoạt động, thẻ 2 cột, giỏ và form phù hợp màn hình; không tràn ngang |
| Mobile 320 × 740 | Chiều rộng tài liệu không vượt viewport; bộ lọc/sắp xếp tự xuống dòng |
| Tìm kiếm “cao su” | Hiển thị 3 sản phẩm mẫu tương ứng |
| Lọc TPE | Hiển thị 2 sản phẩm TPE |
| Sắp xếp giá tăng dần | 420.000 → 420.000 → 670.000 → 670.000 → 670.000 → 890.000 đ |
| Chọn Lilium màu Xanh sage, số lượng 2 | Giỏ giữ đúng màu và số lượng; tạm tính 1.340.000 đ |
| Tăng lên 3, giảm về 2 | Tạm tính 2.010.000 đ rồi 1.340.000 đ |
| Số điện thoại không hợp lệ | Hiển thị lỗi, chưa tạo đơn |
| Đặt hàng với dữ liệu giả hợp lệ | Tạo đơn LY-DEMO, xóa giỏ đã mua; lịch sử hiển thị tạm tính đúng |
| Yêu thích | Sản phẩm xuất hiện trong danh sách; còn sau khi tải lại |
| Giỏ sau tải lại | Lilium số lượng 1 còn trong giỏ, tạm tính 670.000 đ |
| Chọn thảm qua 3 câu hỏi | Hoàn tất và mở gợi ý theo khoảng giá/màu trong dữ liệu mẫu |
| Chuyển nhóm phụ kiện | Hiển thị nhóm vòng, con lăn, bóng và túi phụ kiện |
| Biểu mẫu CTV | Lưu phiếu thử và hiển thị xác nhận cục bộ |
| Nhận tin | Lưu email mẫu cục bộ và thông báo chưa đăng ký vào hệ thống thật |
| Bàn phím ở nhóm chất liệu | ArrowRight chuyển từ Tất cả sang Cao su, hiển thị 3 sản phẩm |
| Console trình duyệt | Không có lỗi hoặc cảnh báo trong các phiên được kiểm tra |
| Tài nguyên cuối | Không có ảnh lỗi trên bản cuối |

Kiểm thử dùng phiên `?qa=1` với khóa lưu trữ riêng, tách khỏi dữ liệu anh đang thử. Các ảnh trong `screenshots/` là minh chứng kiểm tra. Không có giao dịch, gửi email hoặc đăng ký thật.

Giới hạn: chưa thử trên thiết bị iOS/Android vật lý và chưa có hệ thống thương mại phía máy chủ để kiểm tra thanh toán, tồn kho, giao hàng hoặc bảo mật của một cửa hàng thật.
