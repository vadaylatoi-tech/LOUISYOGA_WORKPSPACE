---
name: ly-connect
description: Kiểm tra kết nối ứng dụng riêng Sapo của Louis Yoga, chẩn đoán lỗi xác thực, mạng và quyền theme. Dùng trước build hoặc khi API lỗi.
---

# Kiểm tra kết nối
Yêu cầu bổ sung: $ARGUMENTS

Đọc CLAUDE.md, context/STATE.md, project.config.json; chỉ đọc phần lỗi liên quan trong context/CONNECTION.md từ root dự án. Nếu được gọi từ thư mục khác, tìm root chứa các file này trước. Mặc định chỉ đọc, không publish hoặc thử ghi để chứng minh kết nối.

1. Ưu tiên connector thực có trong STATE. Chỉ kiểm tra lại runtime/legacy khi môi trường đổi hoặc có chứng cứ mới; không tìm toàn ổ hay đọc wrapper đã ghi là không tồn tại. Khi cần xác minh giao thức, tra tài liệu chính thức trong context/SOURCES.md; nếu wrapper có thật, đọc mã và xác định credential provider/quyền. Khóa DPAPI chỉ được giải mã trong tiến trình cần dùng; không xuất ra công cụ đọc file/chat/log.
2. Dùng host ứng viên từ config, xác nhận shop đúng với louisyoga.vn và hồ sơ. Kiểm tra DNS/TLS/HTTPS, request không tự chuyển Authorization sang host khác. Tái sử dụng Basic đúng ứng dụng riêng; chỉ dùng token nếu bằng chứng cho thấy đó là OAuth.
3. Đọc theme listing, role, asset listing và template/config mẫu. Lưu dữ liệu nhạy cảm vào reports/*.local.json đã ignore. Ghi riêng bản báo cáo đã lược bỏ bí mật.
4. Lập capability matrix: auth, list themes, list/read assets, snapshot text/binary, write draft, create key, delete probe, preview, publish/restore. Đánh dấu bằng chứng và NOT_TESTED cho thao tác chưa chạy; không suy từ quyền khai báo thành đã thử thành công.
5. Nếu lỗi, phân loại theo CONNECTION.md; sửa cấu hình/tool local khi có chứng cứ rồi thử lại có giới hạn. 401/403 không retry mù; timeout sau write phải read-back; DPAPI khác tài khoản thì hướng dẫn nhập credential che ký tự vào kho local. Không xin khóa plaintext.
6. Không đủ API thì tiếp tục khảo sát/build local, chuẩn bị gói đúng cấu trúc và hướng dẫn thao tác quản trị từ UI thực. Chỉ gọi browser/MCP nếu thực có. Không giả lập đã upload.

Kết quả: reports/connection-report.md (ngày giờ, shop, method, capability, lỗi, cách sửa, việc còn thiếu), cập nhật STATE.md và giá trị **đã xác minh** trong config. Không thay ID lịch sử thành hiện tại nếu chưa đọc remote. Với nhiệm vụ chỉ kiểm tra kết nối, dừng sau báo cáo; với nhiệm vụ build đi tiếp phần đã sẵn sàng.
