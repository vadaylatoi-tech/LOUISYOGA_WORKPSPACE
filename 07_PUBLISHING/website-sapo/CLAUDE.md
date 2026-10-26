# Dự án Louis Yoga — đổi giao diện website Sapo (louisyoga.vn)

Phiên Claude Code mới: **trước khi làm gì, đọc theo thứ tự**
1. `4. Hiện trạng/BAN-GIAO.md` — **mục 00 "Cập nhật 22/10" trước** (trạng thái mới nhất, việc đang chờ, cách thao tác Sapo admin qua trình duyệt), rồi mục 0 (20/10), rồi cách kết nối Sapo, quy tắc, cách làm đã kiểm chứng. Lưu ý: có 2 phiên Claude cùng sửa theme — luôn đọc bản mới nhất trên Sapo trước khi ghi.
2. `4. Hiện trạng/TIEN-DO.md` — tiến độ từng trang, file đã sửa, bản sao lưu.
3. `4. Hiện trạng/CLAUDE.md` — rà soát hiện trạng ban đầu (quy tắc §0, token §3 còn đúng; bảng trạng thái §4, §6 đã cũ).

Quy tắc cốt lõi (chi tiết trong BAN-GIAO.md §3):
- Xưng "em", gọi "anh Công", trả lời tiếng Việt.
- Từ 19/10 theme **1170160 là web thật (main)** — sửa ở đây lên web ngay: chỉ sửa khi anh yêu cầu rõ, sao lưu trước, kiểm sau; ghi cần `allow_live_theme: true`. Không đụng 1170134 (bản cũ). Xuất bản/đổi theme do anh làm trong Sapo admin.
- Không dùng 2 bộ kit cũ (`louis-yoga-claude-kit`, `Louis-Yoga-Claude-Code-Kit`).
- Đọc file mới nhất trên Sapo trước khi ghi; sao lưu bằng `source_key` trước mỗi lần ghi; kiểm tra lại sau khi ghi.
- Không tự đăng nhập, không thao tác giỏ/đơn thật, không tự sáng tác chính sách/đánh giá/khuyến mãi/hotline.

Kết nối Sapo: MCP server `sapo-louisyoga-claude` — mẫu cấu hình ở `.mcp.json.example` (anh Công tự điền mã token, không đưa mã vào tài liệu).

Thư mục: `1. File thiết kế` (PDF bản thiết kế 15/10), `2. Skill thiết kế`, `3. Tài nguyên hình ảnh`, `4. Hiện trạng` (tài liệu bàn giao).
