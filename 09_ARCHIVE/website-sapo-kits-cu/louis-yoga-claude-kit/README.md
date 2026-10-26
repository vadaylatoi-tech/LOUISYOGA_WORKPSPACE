# Louis Yoga — kit làm việc

Mở Claude tại thư mục chứa file này, CLAUDE.md và .claude/skills. Dùng prompt “Tiếp tục phiên build” trong [BO-PROMPT.md](BO-PROMPT.md); không chạy onboarding lại. Kit hiện có công việc draft đang dở, không phải gói khởi tạo trắng.

- [STATE](context/STATE.md): điểm tiếp tục ngắn; dữ kiện remote phải kiểm tra lại trước ghi.
- [Báo cáo build](reports/build-progress-2026-10-15.md): chi tiết đã làm/chưa làm, chỉ đọc mục cần thiết.
- CLAUDE.md: nguyên tắc và cách nạp tài liệu theo việc. 5 skill giữ các bước thực thi.
- project.config.json: đường dẫn nguồn và lần quan sát trước; không là quyền ghi/publish.
- OPERATIONS/ACCEPTANCE: backup, deploy, restore và QA; bắt buộc theo giai đoạn.
- context/archive: lịch sử để truy nguyên, không nạp đầu phiên.

Lệnh hằng ngày: `/ly-build`, `/ly-fix [lỗi]`, `/ly-connect [lỗi kết nối]`, `/ly-release prepare`, `/ly-restore [mốc + phạm vi]`. Publish cần lệnh duyệt release cụ thể. Không gửi API key vào chat.

Chỉnh kit không có nghĩa tiếp tục build, sửa remote hay xuất bản. Các báo cáo cũ giữ ngày/thời điểm của chúng; không coi là test mới. Không mở ZIP kit cũ để ghi đè workspace đang làm. Nếu chuyển máy, giữ nguyên công việc và backup, sửa đường dẫn config phù hợp rồi kiểm tra kết nối.
