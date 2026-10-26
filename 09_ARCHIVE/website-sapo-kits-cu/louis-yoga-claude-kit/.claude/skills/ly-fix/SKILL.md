---
name: ly-fix
description: Tái hiện và sửa lỗi theme Louis Yoga trên local hoặc draft, giữ checkpoint trước sửa, kiểm tra hồi quy và cập nhật bài học kỹ năng.
---

# Sửa lỗi có thể khôi phục
Lỗi/phạm vi: $ARGUMENTS

Đọc CLAUDE.md, context/STATE.md, context/OPERATIONS.md và phần ACCEPTANCE liên quan. Nếu thiếu mô tả, kiểm tra URL/ảnh/log người dùng đưa trước, chỉ hỏi phần không thể tái hiện. Không dùng request sửa giao diện để tự publish live.

**Chế độ nhanh (17/10, xem CLAUDE.md):** với draft bỏ bước 2 (backup remote), dry-run/before-hash ở bước 4 và reports/known-issues ở bước 6; chỉ cần: tái hiện → sửa `theme/` → PUT draft → so size → kiểm tra 390/1440 → Git commit → 1 dòng STATE.

1. Ghi URL + theme ID/role + viewport + trình duyệt + bước tái hiện + expected/actual. Kiểm tra console/network và dữ liệu liên quan, phân biệt lỗi template/CSS/JS/data/app/cache. Chỉ báo nguyên nhân sau khi có bằng chứng.
2. Trước sửa tạo checkpoint local và backup remote key dự định chạm; lưu cả diff/untracked thuộc công việc hiện có. Ghi checkpoint ID vào STATE. Nếu không thể backup, vẫn chẩn đoán và tạo patch local, chưa ghi remote.
3. Viết kiểm tra hồi quy có ý nghĩa hoặc kịch bản browser tái hiện. Sửa nguyên nhân với phạm vi nhỏ, không dùng `!important`/timeout/reload như cách che triệu chứng khi chưa hiểu nguyên nhân. Không viết lại theme vì một lỗi cục bộ.
4. Dry-run diff; remote before-hash phải còn khớp. Upload chỉ draft đúng ID, đọc lại từng key. Ghi create/update/delete và before/after để có thể đảo ngược. Kết quả write chưa rõ xử lý read-back trước retry.
5. Chạy lại kịch bản lỗi và luồng lân cận: menu/cart shared cần cả PC/mobile; variant cần giá/stock/cart; header cần route ngoài trang chủ. Chụp trước/sau khi lỗi thị giác. Không gọi đã sửa nếu chưa tái kiểm chứng.
6. Cập nhật reports/fixes/<issue-id>.md và STATE: nguyên nhân, file, checkpoint, bằng chứng, phạm vi chưa test, lệnh/cách restore cụ thể. Tạo commit khi phù hợp và không gom file ngoài phạm vi.

## Học thành skill sau lỗi thực tế
Sau khi fix đã xác minh, thêm một mục ngắn vào references/known-issues.md của skill này: triệu chứng, điều kiện kích hoạt, nguyên nhân đã chứng minh, giải pháp, regression check, giới hạn áp dụng. Không ghi bí mật hoặc biến phỏng đoán thành quy tắc toàn dự án. Nếu có nhiều lỗi cùng cơ chế, hợp nhất mục cũ; chỉ tách skill mới khi workflow độc lập thực sự hữu ích. Skill được tạo sẵn ở đây; cập nhật tri thức thay vì tạo bản trùng tên mỗi lần.
