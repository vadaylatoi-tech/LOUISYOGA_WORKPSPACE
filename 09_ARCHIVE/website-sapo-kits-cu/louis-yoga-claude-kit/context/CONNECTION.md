# Kết nối Sapo và xử lý lỗi

## Điểm vào khi nối phiên
Đọc STATE trước: phiên 15/10 đã dùng MCP Sapo; legacy wrapper/DPAPI được báo không còn. Phần wrapper bên dưới là tham khảo lịch sử, chỉ dùng lại khi có bằng chứng file tồn tại. Không chạy lại tìm kiếm toàn ổ. Khi gặp lỗi connector, tra đúng mục trong reports/connection-report.md; báo cáo đó có các bước tiếp theo đã lỗi thời, STATE và báo cáo build mới hơn xác định tiến độ. Không ghi file bị cắt, kể cả chuyển sang UI; cần đủ nội dung + backup/hash trước.

## Tái sử dụng kết nối đã có (lịch sử)
`project.config.json` trỏ tới `sapo-connection/sapo.ps1` của workspace cũ. Đã đọc mã wrapper khi soạn bộ này, chưa chạy API. Nó giải mã DPAPI trong tiến trình Windows và gửi Basic header qua HTTPS. Chỉ dùng từ cùng tài khoản Windows có thể giải mã; WSL cần gọi tiến trình PowerShell Windows đúng tài khoản. Không giả định copy file DPAPI sang máy/tài khoản khác sẽ hoạt động.

Wrapper cũ hỗ trợ `Themes`, `Assets`, `Read`, `Write`; tham số `ThemeId`, `Key`, `InputFile`, `OutputFile`. Ví dụ chỉ đọc, sau khi xác nhận đường dẫn và ID:

```powershell
& '<legacy-root>/sapo-connection/sapo.ps1' -Action Themes -OutputFile '<work-root>/reports/themes.local.json'
& '<legacy-root>/sapo-connection/sapo.ps1' -Action Assets -ThemeId <verified-id> -OutputFile '<work-root>/reports/assets.local.json'
& '<legacy-root>/sapo-connection/sapo.ps1' -Action Read -ThemeId <verified-id> -Key '<actual-key>' -OutputFile '<work-root>/reports/asset.local.json'
```

Các `<...>` phải thay bằng giá trị xác minh; không chạy nguyên văn. File output có thể chứa cấu hình nhạy cảm, giữ local và không đưa vào Git/gói bàn giao công khai. Wrapper mặc định ID 1151386: luôn truyền ID, kiểm tra role mới ngay trước thao tác ghi.

### Giới hạn cần xử lý trước khi dùng cho vận hành đầy đủ
- `Write` chỉ xử lý text và đọc tệp cũ trước; không có quy trình create-key chưa tồn tại, binary, xóa, tạo theme hay publish.
- Không có guard role main/mobile, khóa chống hai tiến trình, check thay đổi remote trước ghi, retry hay release transaction.
- So sánh text tuyệt đối có thể báo lệch do Sapo bỏ newline cuối. Cần lưu raw hash lẫn quy tắc chuẩn hóa hẹp, không xóa toàn bộ whitespace/HTML để ép khớp.
- Bản sao mỗi file không thay thế snapshot đầy đủ có manifest, settings và binary.

Claude xây adapter mới trong thư mục làm việc khi cần, dùng cơ chế DPAPI hiện hữu mà không xuất secret ra file tạm. Không sửa wrapper gốc nếu chưa có lý do và backup. Các interface doctor/snapshot/diff/push-draft/verify/publish/restore là **yêu cầu thiết kế**, không phải lệnh sẵn có.

## Xác thực theo chứng cứ
Tài liệu ứng dụng riêng Sapo mô tả API key + API secret qua Basic Authentication. Dùng thư viện tạo header trong bộ nhớ; không đặt khóa trong URL hoặc tham số dòng lệnh. [Nguồn](https://support.sapo.vn/ung-dung-rieng-private-apps).

OAuth là nhánh khác: tài liệu mô tả `X-Sapo-Access-Token`, các scope `read_themes`, `write_themes`. Không gửi client secret vào header token, không đổi qua Bearer/Shopify header theo suy đoán. [Nguồn](https://support.sapo.vn/oauth).

Nếu credential cũ không dùng được: hướng dẫn chủ shop nhập trực tiếp vào kho bí mật local bằng input che ký tự. Chỉ hỏi tên/path secret, không xin dán giá trị vào chat. Không tự tạo ứng dụng mới hoặc thay quyền đã cấp khi chỉ đang chẩn đoán.

## Trình tự kiểm tra
1. Phiên bản Claude Code, shell, PowerShell Windows, Git, runtime, công cụ ảnh/browser sẵn có. Không cài CLI tự xưng Sapo từ nguồn không xác minh.
2. Path/config tồn tại; chỉ báo có/thiếu khóa, không đọc plaintext ra output. Kiểm tra quyền giải mã DPAPI trong tiến trình.
3. Host đúng shop; DNS, TLS, proxy và timeout. Website công khai trả 200 không chứng minh Admin API dùng được.
4. GET danh sách theme theo tài liệu áp dụng. Xác nhận JSON/schema, không nhầm HTML trang đăng nhập thành thành công.
5. Đọc asset listing và một template, tìm layout/config/template thực. Phân biệt ID main, mobile riêng nếu có, và unpublished.
6. GET thành công chỉ chứng minh quyền đọc. Ghi nhận quyền ghi là “chưa thử” cho tới phép thử draft được cho phép hoặc lần upload draft đầu tiên được đọc lại đúng.
7. Khi phạm vi cho phép kiểm tra ghi: dùng một key probe độc nhất trên draft, xác nhận key chưa tồn tại, ghi/đọc lại/cleanup bằng API đã xác minh, log cleanup. Không đụng template chính để kiểm tra. Nếu không có cơ chế cleanup, dùng lần ghi cần thiết đầu tiên của build làm bằng chứng, không tạo rác.

## Ma trận xử lý lỗi
| Dấu hiệu | Chẩn đoán và hành động |
|---|---|
| DNS/TCP timeout | Kiểm tra host, DNS, mạng, proxy, thời gian máy; phân biệt timeout kết nối và đọc. Không đổi shop để thử khóa. |
| TLS/certificate | Kiểm tra chuỗi CA, đồng hồ, proxy doanh nghiệp; không tắt TLS verify, không hạ HTTPS xuống HTTP. |
| 301/302 | Không chuyển tiếp Authorization sang host khác. Xác minh canonical Admin host trước request mới. |
| 200 nhưng HTML | Login/WAF/route sai; kiểm tra Content-Type và schema; chưa xác thực thành công. |
| 401 | Kiểm tra loại credential, đúng shop, cặp key/secret và khả năng giải mã; dừng retry credential sai. |
| 403 | Xác định thiếu quyền, WAF hay hạn chế tính năng qua lỗi đã che bí mật. Đọc được product không chứng minh quyền theme. Không tự nâng quyền. |
| 404 | Kiểm tra endpoint thế hệ Sapo, ID đã xóa, key/case/plural; không chuyển sang ghi main để thử. |
| 405/415 | Kiểm tra method, JSON UTF-8, header Content-Type. |
| 400/422 | Kiểm tra envelope, key thực, schema và payload; sửa nguyên nhân, không retry nguyên payload. |
| 409 hoặc remote đổi | Re-read và diff; giữ thay đổi của người khác; cần merge/chọn lại baseline. |
| 413 | Đo kích thước request/ZIP/binary; tối ưu ảnh/font hoặc chia upload khi được hỗ trợ. Không tự giả định giới hạn 5 MB. |
| 429 | Tuân thủ Retry-After; giảm concurrency, backoff có jitter. |
| 5xx/connection reset | GET retry giới hạn; write timeout chuyển sang “kết quả chưa rõ” và GET đối chiếu trước khi gửi lại. |
| CORS trên browser | Admin API phải nằm trong công cụ local/server; không đưa secret vào JavaScript website, không dùng proxy công khai để né CORS. |
| Preview không đổi | Xác nhận theme ID/preview session, key thực và hash remote; sau đó mới xét cache/CDN và phiên duyệt sạch. |

Chính sách retry đề xuất cho adapter: tối đa 3 lần thử/request trong 120 giây, backoff 1/2/4 giây + jitter cho lỗi tạm thời; Retry-After vượt ngân sách thì dừng và hẹn người dùng chạy lại. Đây là quy ước dự án, không phải hạn mức Sapo. Không retry mù POST tạo theme, publish hoặc write có kết quả không rõ.

## Nhật ký và đầu ra
Ghi timestamp UTC + Asia/Ho_Chi_Minh, method/path đã bỏ query bí mật, status, request ID nếu có, thời lượng, số lần thử, capability PASS/FAIL/NOT_TESTED. Không log header Authorization, secret, cookie, response cấu hình nguyên vẹn. Báo cáo nêu nguyên nhân có chứng cứ, điều đã sửa và bước tối thiểu còn cần người dùng.

## Ghi chú 17/10/2026 — đọc một key qua connector MCP
`get_theme_asset` và `sapo_request` với `asset[key]` hiện trả về **cả listing** (bị cắt ~90k), không trả nội dung key. Cách đọc đúng: `sapo_request` GET `themes/<id>/assets.json` với query `{"key": "<key>"}` → trả `asset.value` đầy đủ. File CSS/JS có thể đọc/hash qua CDN `public_url`. Ghi: PUT `themes/<id>/assets.json` body `{"asset":{"key","value"}}`, rồi so sha256 bản CDN với file `after/`.
