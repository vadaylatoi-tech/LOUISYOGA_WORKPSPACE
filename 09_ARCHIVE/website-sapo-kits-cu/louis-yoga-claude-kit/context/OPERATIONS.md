# Sao lưu, đồng bộ, phát hành và khôi phục

Đây là quy trình dự án được đề xuất. Khả năng endpoint, cách tạo preview và quyền thực tế phải xác minh trên shop. Không có script publish/restore đã chạy sẵn trong bộ này.

## Ngoại lệ hiện tại — chỉ build draft 1170160
Theo STATE gốc ngày 15/10/2026, chủ shop bỏ yêu cầu ZIP toàn theme cho build draft này, nhưng vẫn lưu bản cũ từng file trước ghi. Ngoại lệ chỉ thay baseline toàn theme trong giai đoạn build: bắt buộc đọc đủ key sắp chạm, snapshot nội dung + hash + checkpoint và manifest; key mới phải xác minh chưa tồn tại. Nếu thiếu nội dung/backup thì không ghi. Không miễn guard role, drift, khóa, read-back, QA hoặc snapshot đầy đủ trước release. Không lấy theme main hiện tại làm backup bất biến. Nối phiên không được chép main lên draft hoặc push cây local chưa mirror đủ.

## 1. Baseline và checkpoint
Baseline trước lần build đầu: đọc danh sách theme và role; tải toàn bộ asset của theme nguồn gồm layout, templates, snippets, settings/schema và binary; ghi key đúng case/plural, bytes/hash, time, shop/ID/role. Asset listing chưa phải backup nội dung. Đi hết phân trang nếu có; đối chiếu số lượng, các key thiếu và lỗi tải. Tải asset CDN bằng request riêng không gắn Admin Authorization; xác minh HTTPS/host CDN trước tải.

Snapshot nằm ngoài `theme/`, không bao gồm credentials. Kiểm tra có thể đọc lại từng file và dựng lại cây theme/ZIP trước khi gọi là “khôi phục được”. Thử phục hồi lên một draft khi có quyền/phương án khả thi; nếu chưa thử, ghi “backup đầy đủ, restore rehearsal chưa thử”. Khóa draft đang dùng để tránh hai lần deploy cùng lúc, đọc lại remote ngay trước ghi để phát hiện chỉnh sửa từ quản trị.

Checkpoint trước mỗi đợt sửa chứa commit/branch hoặc snapshot local, diff đang có, untracked files liên quan, remote snapshot các key sắp chạm, settings và manifest. Không dùng `git reset --hard`, `git clean` hay stash mù để dọn công việc của người khác. Không `git add .` khi chưa loại secrets/backup.

Định danh gợi ý: `pre-fix-YYYYMMDD-HHMMSS`, `release-YYYYMMDD-HHMMSS`; ghi timezone. Đây là nhãn gợi ý, phải tạo thật và lưu vị trí. “Bản trước sửa” luôn là checkpoint cụ thể, không đoán theo file gần nhất.

## 2. Upload draft
Tạo allowlist file theme từ build output; loại `.env`, `.git`, `.claude`, docs, source AI/PDF, backup, source maps chứa bí mật. Dry-run liệt kê create/update/delete, bytes và hash. Mặc định không xóa asset remote không liên quan. Sapo docs có sự khác nhau `layout`/`layouts`, `config`/`configs`; giữ key thực tế của listing và xác minh cấu trúc ZIP import, không đổi tên hàng loạt.

Trước mỗi batch: kiểm tra store + target ID + role unpublished, khóa, baseline hash. Upload dependency assets/snippets trước templates tham chiếu; settings phải merge có chủ đích, giữ ID cấu hình cũ khi còn dùng. Ghi log từng key, before/after hash, kết quả read-back và lỗi. Upload nhiều file không nguyên tử: lỗi giữa chừng phải đánh dấu draft chưa hoàn chỉnh, không publish.

Với write timeout: đọc lại key để phân loại chưa ghi/đã ghi/khác nội dung. Không gửi lại mù. Với tạo theme timeout, đọc danh sách và nhận diện theo release marker trước khi tạo lại. Binary kiểm chứng hash tải lại; text dùng raw hash và chỉ chuẩn hóa những khác biệt được chứng minh (ví dụ newline cuối). Không dùng public CDN URL làm bằng chứng backup code template.

## 3. Release
Release record theo `templates/release-record.json`: commit, build hash, theme ID, previous live ID(s), settings hash, manifest, QA, preview, thời điểm, quyền người dùng. Không publish nếu missing critical asset, chưa có backup, kết quả write chưa rõ, draft đang processing, hoặc chưa qua các test mua hàng trọng yếu.

Lưu theme cũ và snapshot trước phát hành. Theme preview thường dùng chung catalog/apps với live; nó không phải sandbox dữ liệu. Không tạo sản phẩm/đơn test hay sửa app setting toàn shop khi chỉ được phép thử draft.

Trước switch đọc lại role và hashes; thay đổi ngoài dự kiến khiến release cũ không còn đúng, phải rà diff và kiểm tra lại phần ảnh hưởng. Nếu đã có lệnh người dùng rõ ràng cho đúng release còn nguyên, tiến hành; nếu chưa, đưa preview + release ID + QA + bản khôi phục để người dùng duyệt một lần.

Xuất bản bằng API hoặc giao diện đã xác minh. Sau switch đọc lại role, rồi mở public URL trong phiên sạch không có preview cookie/query. Kiểm tra cả desktop/mobile và xem có mobile-role riêng che theme mới không. Kiểm tra trang chủ, collection, product, variant, cart, tới checkout trước bước tạo đơn, assets, console, SEO, tracking không nhân đôi. HTTP 200 đơn lẻ không đủ.

Nếu lỗi trọng yếu: dừng rollout; khi lệnh release đã cho phép rollback lỗi trọng yếu thì đưa về previous live đã xác minh và kiểm tra lại. Nếu chưa có phạm vi rollback live, báo lỗi và đề xuất một target cụ thể; không âm thầm thay bằng theme bất kỳ.

## 4. Khôi phục ba lớp
**Local:** khôi phục key/file liên quan từ checkpoint vào nhánh phục hồi, giữ snapshot hiện tại và diff. Ưu tiên commit revert hoặc copy chọn lọc đã hiểu; không xóa toàn repo.

**Draft:** kiểm tra target unpublished; backup hiện tại; dựng manifest đảo ngược. Update key đã đổi, tạo lại key bị xóa; key mới do chính release tạo chỉ xóa khi manifest và phạm vi restore xác nhận. Đọc lại/hash và QA phần liên quan. Không để các key mới còn ảnh hưởng rồi gọi là restore đầy đủ.

**Live:** ưu tiên áp dụng lại theme live cũ còn nguyên. Kiểm tra settings/hash của bản đó; tên “backup” không chứng minh chưa bị sửa. Nếu bản cũ không còn, dựng snapshot thành draft mới, kiểm tra rồi mới apply. Khôi phục code không khôi phục sản phẩm/đơn hàng/app settings hoặc dữ liệu khách hàng.

Nếu không xác định được checkpoint đích hoặc snapshot thiếu, báo rõ và hỏi chọn mốc; vẫn kiểm kê/diff trước. Không bịa rằng checkpoint của Claude Code thay thế được bản sao remote hoặc database.

## 5. Hợp đồng công cụ Claude cần hoàn thiện
Adapter có thao tác read-only doctor/list/read/snapshot/diff; thao tác ghi nhận explicit target, expected role, expected before-hash và manifest; default dry-run. Publish cần release ID và previous-live đã kiểm tra. Restore cần checkpoint + layer. Mọi thao tác lỗi trả mã/nhật ký đã che bí mật. Có mock tests cho 401, 403, 429, timeout sau ghi, stale remote, chặn main, binary roundtrip, snapshot thiếu và rollback đảo file mới. Không dùng production làm môi trường unit test.
