# Quy tắc chọn nội dung & dựng video ngắn (đã được người dùng duyệt)

## 1. Chỉ dùng lời có thật
- Mọi câu trong video phải là lời người nói trong video gốc. Không bịa, không viết lại câu nói.
- Phụ đề nhận dạng tự động sai tên riêng/thuật ngữ → đánh dấu **[cần nghe lại]** trong `phuong-an.md`, ghi cách đọc có thể đúng trong `[ngoặc vuông]` (chỉ là gợi ý, không phải lời mới), và đưa vào `terms.json`.
- Không ghép khiến nghĩa câu bị đổi. Đảo thứ tự đoạn được, miễn mỗi đoạn trọn câu và ý không sai.

## 2. Chọn chủ đề
- Mỗi video **một chủ đề**. Ưu tiên: hướng dẫn chọn sản phẩm, so sánh, giải đáp thắc mắc người xem hay hỏi, lỗi thường gặp, mẹo sử dụng/bảo quản, tâm lý người mới.
- Bỏ: lời chào, kêu gọi comment/chốt đơn, chờ đợi, đọc giá/voucher/quà tặng theo phiên, đoạn trục trặc kỹ thuật, nhắc lại không cần thiết.
- **Tránh lặp nội dung giữa các video.** Nếu buộc trùng một ý nhỏ, ghi chú để không đăng 2 video đó liền nhau.
- Đưa **danh sách video có thể làm** trước (bảng: #, tiêu đề, nhóm, tổng giây), rồi mới tới bảng dựng chi tiết.

## 3. Cấu trúc mỗi video: HOOK → THÂN → KẾT
- **HOOK (2–10 s đầu)**: câu gây chú ý nhất về chủ đề — câu hỏi người xem hay hỏi ("Tại sao thảm mua chỉ dùng được vài tháng là hỏng?"), khẳng định gây bất ngờ ("Thảm càng dày càng tốt? Chưa chắc"), lỗi phổ biến ("Rất nhiều chị tập xong cuộn ngược thảm…"), hoặc lời khuyên dứt khoát. Được lấy từ **bất kỳ đâu** trong video gốc đưa lên đầu.
- **THÂN**: giải thích, so sánh, ví dụ — theo trình tự logic.
- **KẾT**: câu **chốt trọn vấn đề** mà hook đặt ra (lời khuyên rõ ràng: "ưu tiên A thì chọn X, cần B thì chọn Y"; hoặc tóm lại các lưu ý). Không kết bằng câu lửng, câu chuyển sang ý khác, hay câu cảm thán rời rạc. Người xem phải hiểu video giải quyết vấn đề gì.
- Tự hỏi trước khi chốt: "Chỉ nghe câu đầu và câu cuối, người xem có hiểu video nói gì và kết luận gì không?"

## 4. Thời lượng
- Mục tiêu 50–90 s, tính **tổng các đoạn đã chọn**, không cộng khoảng bị bỏ.
- Đủ ý quan trọng hơn đúng khung: thiếu/thừa 8–15 s được. Video ngắn quá thì bổ sung đoạn cùng chủ đề; dài quá thì bỏ câu lặp.

## 5. Điểm cắt
- Mốc trong phụ đề là gợi ý; script tính lại theo âm thanh. Không được mất chữ đầu/cuối câu, không mất giọng.
- Người nói nói liền (không có khoảng lặng) → dời sang ranh giới câu gần nhất; chấp nhận chữ nối ở đầu ("Bởi vì là", "Tại vì", "Còn") hơn là cắt giữa chữ. Ghi lại chỗ này để báo người dùng (có thể ẩn bằng phụ đề ở bước edit).

## 6. Mỗi video trong `phuong-an.md` có
Tiêu đề · chủ đề · câu hook (lời gốc) · bảng đoạn nguồn theo thứ tự dựng (#, vào, ra HH:MM:SS.mmm theo video gốc, thời lượng, câu đầu, câu cuối) · lời thoại · tổng thời lượng · gợi ý chữ trên màn hình · chỗ cần nghe lại/tinh chỉnh.

## 7. Màu sắc
Không chỉnh màu trừ khi người dùng yêu cầu (`render.py --grade`).
