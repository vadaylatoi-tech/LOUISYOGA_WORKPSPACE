---
name: ly-restore
description: Khôi phục theme Louis Yoga về checkpoint trước sửa ở local, draft hoặc live, bảo toàn trạng thái hiện tại và kiểm chứng kết quả.
---

# Khôi phục trước sửa
Đích/phạm vi: $ARGUMENTS

Đọc CLAUDE.md, context/STATE.md, context/OPERATIONS.md và release/fix record liên quan. Xác định lớp local/draft/live và checkpoint thật. “Quay lại bản trước sửa” chỉ đủ rõ khi STATE có duy nhất mốc của đợt sửa đang nói tới; nếu có nhiều khả năng, trình bày các mốc và hỏi chọn. Không dùng mặc định `HEAD~1`.

1. Inventory trạng thái hiện tại, diff, uncommitted/untracked liên quan và remote role/hash. Tạo checkpoint cứu hộ trước khôi phục. Không ghi đè công việc chưa lưu của người dùng.
2. Xác minh snapshot có đủ key/content/settings/binary, đúng shop/theme, hash hợp lệ và mốc phù hợp; tạo kế hoạch đảo create/update/delete. Không coi asset listing là snapshot đầy đủ.
3. Local: áp dụng file/commit phù hợp trên nhánh phục hồi; giữ công việc ngoài phạm vi. Draft: chỉ ghi target chưa xuất bản đã xác minh, read-back/hash và thử lại. Live: ưu tiên switch về previous live còn nguyên; nếu phải rebuild snapshot, dựng draft và QA trước.
4. Lệnh restore local/draft không bao hàm live. Nếu người dùng đã yêu cầu restore live tới mốc cụ thể, tiến hành trong quyền đó; không hỏi lại. Nếu đích live còn mơ hồ, hoàn thành diff/snapshot trước rồi xin chọn target cụ thể.
5. Kiểm chứng key/hash, settings, trạng thái role và public URL/preview tương ứng. Chạy test liên quan và cart/variant khi khôi phục layout/shared JS. Không đặt đơn thật nếu chưa được phép.
6. Lưu reports/restores/<id>.md: từ mốc nào đến mốc nào, lớp khôi phục, file thêm/sửa/xóa, checkpoint cứu hộ, kết quả QA, giới hạn. Cập nhật STATE. Nêu rõ sản phẩm/đơn hàng/app settings không được khôi phục bằng theme rollback.

Nếu mất backup hoặc chưa từng chụp trạng thái trước sửa, báo không thể bảo đảm khôi phục chính xác; khảo sát version history/theme cũ/Git có thật và đưa phương án có bằng chứng. Không xóa thư mục hoặc ghi main để thử tìm lại phiên bản.
