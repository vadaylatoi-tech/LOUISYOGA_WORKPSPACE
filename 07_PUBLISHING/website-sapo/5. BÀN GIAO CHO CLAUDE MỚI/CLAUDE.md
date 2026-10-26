# Dự án Louis Yoga — đổi giao diện website Sapo (louisyoga.vn) — GÓI BÀN GIAO 17/10/2026

Phiên Claude Code mới mở trong thư mục này: **trước khi làm gì, đọc theo thứ tự**
1. `tai-lieu/1-BAN-GIAO.md` — cách kết nối Sapo, quy tắc, cách làm đã kiểm chứng, việc còn lại.
2. `tai-lieu/2-TIEN-DO.md` — tiến độ từng trang, file đã sửa, bản sao lưu trên Sapo.
3. `tai-lieu/3-HIEN-TRANG-BAN-DAU.md` — rà soát ban đầu sáng 17/10 (quy tắc §0, token màu §3 còn đúng; bảng trạng thái §4, §6 đã cũ).

(Trong các tài liệu, chỗ ghi `4. Hiện trạng/BAN-GIAO.md`, `TIEN-DO.md`, `CLAUDE.md` chính là 3 file trên — tên đã được đánh số trong gói này.)

Quy tắc cốt lõi (chi tiết trong 1-BAN-GIAO.md §3):
- Xưng "em", gọi "anh Công", trả lời tiếng Việt, ngắn gọn.
- Chỉ sửa theme nháp **1170160**. Không ghi / không xuất bản theme đang chạy **1170134** khi anh chưa đồng ý rõ. Xuất bản do anh làm trong Sapo admin.
- Không dùng 2 bộ kit cũ (`louis-yoga-claude-kit`, `Louis-Yoga-Claude-Code-Kit`).
- Đọc file mới nhất trên Sapo trước khi ghi; sao lưu bằng `source_key` trước mỗi lần ghi; kiểm tra lại sau khi ghi.
- Không tự đăng nhập, không thao tác giỏ/đơn thật, không tự sáng tác chính sách/đánh giá/khuyến mãi/hotline.

Kết nối Sapo: MCP server `sapo-louisyoga-claude` — mẫu cấu hình `ket-noi-sapo-MAU.mcp.json` (anh Công đổi tên thành `.mcp.json` và tự điền mã token).

Việc đầu tiên của phiên mới: gọi `list_themes` kiểm tra kết nối (phải thấy 1170134 = main, 1170160 = bản nháp), rồi hỏi anh Công đã sửa 2 chỗ chính sách trong admin và quyết các mục chờ (1-BAN-GIAO.md §7) chưa.
