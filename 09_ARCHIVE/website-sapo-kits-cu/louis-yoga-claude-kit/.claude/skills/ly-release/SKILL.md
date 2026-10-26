---
name: ly-release
description: Chuẩn bị và xuất bản release theme Sapo Louis Yoga với QA, backup, kiểm tra sau phát hành và phương án rollback.
---

# Phát hành Louis Yoga
Yêu cầu: $ARGUMENTS

Đọc CLAUDE.md, context/STATE.md, context/OPERATIONS.md và context/ACCEPTANCE.md. Mặc định khi không có yêu cầu apply cụ thể: chuẩn bị release reviewable. Skill có thể được khám phá tự động nhưng không tự cấp quyền publish. Nếu người dùng đã chỉ rõ publish đúng release/theme, không hỏi lại cùng một quyền; kiểm tra các điều kiện rồi thực hiện.

1. Xác minh shop, live ID(s), target draft, commit/build hash/settings hash, toàn bộ file upload; chỉ chọn release đã QA. Đọc remote mới ngay trước ghi/switch, xử lý drift. Không “fix thêm cho đẹp” trong bước phát hành.
2. Snapshot live và draft đầy đủ theo OPERATIONS, xác nhận previous live còn nguyên và khả năng khôi phục. Chốt QA: lỗi mua hàng, secrets, Liquid, backup thiếu hoặc write chưa rõ phải chặn publish. Ghi những test chưa chạy.
3. Tạo release record từ templates/release-record.json và báo cáo dễ duyệt: thay đổi, preview, QA, chênh lệch, target/previous ID, manifest, rollback plan. Nếu thiếu quyền live, hỏi duyệt đúng release sau khi đã chuẩn bị xong. Không yêu cầu duyệt lại chỉ vì bắt đầu phiên mới khi đã có bằng chứng cho cùng release còn nguyên.
4. Nếu được yêu cầu publish: dùng phương thức đã xác minh. API chỉ dùng khi quyền và payload phù hợp shop; UI chỉ qua công cụ thực. Ghi thời gian, thao tác, phản hồi đã che bí mật. Timeout thì đọc role lại trước retry.
5. Xác minh role và public website trong phiên sạch không preview, cả PC/mobile. Thử trang chủ, danh mục, variant, cart, đường đến checkout trước tạo đơn; kiểm tra ảnh/font/console/SEO/tracking. Ghi kết quả thực, không lấy 200 của publish làm nghiệm thu.
6. Với lỗi trọng yếu và quyền rollback đã ghi trong lệnh phát hành: áp dụng previous live đã xác minh, kiểm tra lại và báo rõ phát hành thất bại/đã rollback. Nếu không có quyền hoặc target đã thay đổi, trình bày tác động và đề xuất chính xác để người dùng quyết định. Không xóa theme cũ.
7. Cập nhật release record, STATE, báo cáo live và references/release-lessons.md. Chỉ thêm điều đã kiểm chứng; không lưu key, cookie, customer data. Ghi việc theo dõi sau phát hành cho người dùng, không hứa theo dõi nền nếu chưa có công cụ lịch thực.

Hoàn thành chỉ khi xác nhận website public chạy release đúng hoặc đã khôi phục và báo sự cố. Nếu chỉ chuẩn bị, trạng thái là READY_FOR_APPROVAL, không ghi PUBLISHED.
