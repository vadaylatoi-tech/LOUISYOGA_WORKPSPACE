# Bài học sửa lỗi

Chưa có lỗi được sửa và kiểm chứng bằng bộ kit này. Các dấu hiệu sau đến từ hồ sơ cũ, chỉ là đầu mối chẩn đoán:
- Có lần upload ZIP bị 413; chưa chứng minh hạn mức cố định của nền tảng.
- Có lần read-back text bỏ dòng trắng cuối; phải xác minh lại, không chuẩn hóa rộng để che sai khác.
- Báo cáo cũ đổi tên font thành chữ thường; cần kiểm tra key/case thực tế và CDN khi font lỗi.

## 2026-10-15 — Ghi asset bằng `src` URL làm file rỗng (đã xác minh)
- Điều kiện: `PUT themes/{id}/assets.json` với `{"asset":{"key":…,"src":"https://bizweb.dktcdn.net/…"}}`.
- Bằng chứng: Sapo trả 200, `size: 0`, `value: ""`; CDN trả 0 byte.
- Giải pháp: chỉ ghi bằng `value` (text). Binary: chưa kiểm chứng cách ghi (`attachment` base64 theo tài liệu) — thử trên key probe trước.
- Regression: sau mỗi ghi, so size listing/hash CDN với nguồn.

## 2026-10-15 — Đối chiếu kích thước sau ghi
- Size trong listing Sapo = số byte UTF-8 của nội dung với xuống dòng LF (đã khớp 13/13 file).
- Công cụ Write của Claude cắt khoảng trắng/tab cuối dòng và Bash `awk` thêm newline cuối file → backup lệch vài byte; kiểm tra size trước khi coi là backup chuẩn.

Khi có lỗi mới, thêm: issue/date → điều kiện → bằng chứng nguyên nhân → thay đổi → regression test → checkpoint/commit → giới hạn áp dụng. Không coi các đầu mối trên là lỗi hiện tại.
