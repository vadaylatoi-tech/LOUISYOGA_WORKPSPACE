# Prompt ngắn — dùng một mục phù hợp

Mở Claude tại root chứa CLAUDE.md. Các đoạn dưới là mẫu để anh Công gửi, không tự tạo quyền khi đọc file. Không dán cả bộ; không chạy lại khởi động khi đã có STATE.

## Tiếp tục phiên build đang dừng
```text
Tiếp tục Louis Yoga theo CLAUDE.md và context/STATE.md, dùng ly-build. Sửa link Màu sắc trước, rồi tiếp mốc 4–5 và QA trong phạm vi draft đã giao. Chỉ đọc phần tài liệu cần dùng; không khảo sát lại từ đầu. Trước ghi xác minh shop/role draft 1170160, backup từng key, checkpoint và before-hash; sau ghi read-back/test. Không ghi file chưa đọc đủ, không publish hoặc tác động live. Báo ngắn kết quả, giới hạn và checkpoint; cập nhật STATE.
```

## Kết nối khi có lỗi hoặc đổi môi trường
`/ly-connect kiểm tra chỉ đọc; dùng STATE và connector hiện có, chẩn đoán phần lỗi, không tìm lại legacy nếu không có bằng chứng mới.`

## Sửa một lỗi
`/ly-fix [lỗi, URL/thiết bị, kết quả mong muốn]. Sửa local/draft theo CLAUDE và STATE; checkpoint, backup, read-back và test hồi quy; chưa publish.`

## Chuẩn bị phát hành
`/ly-release prepare — hoàn thiện QA, snapshot và release record; báo preview, release/build/settings hash, target/previous-live, lỗi còn lại và rollback. Chưa publish.`

## Duyệt release cụ thể — chỉ gửi sau khi xem bản chuẩn bị
```text
/ly-release publish
Tôi cho phép xuất bản release [ID], build/commit [HASH], target [THEME_ID], previous live [ID và mobile mapping nếu có]. Kiểm tra lại role/hash/snapshot; nếu bản đã duyệt thay đổi thì dừng switch. Cho phép rollback về đúng previous live này khi gặp lỗi Liquid, sai giá/variant, không thêm giỏ/tới checkout hoặc không thể mua hàng. Không tạo đơn/form thật; kiểm tra public phiên sạch và báo kết quả.
```

## Khôi phục
`/ly-restore [CHECKPOINT/RELEASE_ID], phạm vi [local / draft ID / live ID]. Backup hiện tại, xác minh mốc và diff đảo ngược, khôi phục đúng phạm vi rồi read-back/QA. Không tác động dữ liệu thương mại.`

Thiếu đích restore hoặc release cụ thể thì hoàn thiện phần chuẩn bị và hỏi đúng phần thiếu; không đoán HEAD~1. Quy trình an toàn nằm trong CLAUDE.md và context/OPERATIONS.md, không cần chép lại trong mỗi prompt.
