# Nguồn và độ chắc chắn — tra ngày 15/10/2026

## Tài liệu chính thức
| Nguồn | Dùng để xác minh |
|---|---|
| [Claude Code Skills](https://code.claude.com/docs/en/skills) | Cấu trúc .claude/skills/name/SKILL.md, YAML name/description, gọi /name, $ARGUMENTS. Kit dùng field cơ bản, không cấp allowed-tools rộng. |
| [Claude Code memory](https://code.claude.com/docs/en/memory) | CLAUDE.md làm ngữ cảnh dự án; nội dung dài tách ra tài liệu theo nhu cầu. |
| [Sapo Private Apps](https://support.sapo.vn/ung-dung-rieng-private-apps) | Cặp API key/secret, Basic auth và phân quyền ứng dụng riêng. |
| [Sapo OAuth](https://support.sapo.vn/oauth) | Nhánh OAuth, X-Sapo-Access-Token và scope theme; không trộn với Basic. |
| [Sapo Theme API](https://support.sapo.vn/theme) | GET /admin/themes.json, GET/PUT /admin/themes/{id}.json, role main/unpublished và trạng thái xử lý. Publish cần xác minh đúng thế hệ/quyền shop. |
| [Sapo Asset API](https://support.sapo.vn/asset) | Asset listing, đọc theo key, cập nhật text qua value và binary qua base64; kiểm tra tên field/key trên shop thật. |
| [Sapo Liquid templates](https://support.sapo.vn/gioi-thieu-ve-template-liquid) | Tổ chức theme và template theo trang; không suy rằng toàn bộ Liquid Shopify được hỗ trợ. |
| [Sapo theme.bwt](https://support.sapo.vn/theme-bwt) | Hooks content_for_header và khối ContentPlaceHolder bắt buộc theo tài liệu này; đối chiếu theme thực trước sửa layout. |
| [Sapo thiết lập giao diện](https://support.sapo.vn/chinh-sua-giao-dien) | Nối settings ID với Liquid, nội dung quản lý qua tùy chỉnh. |
| [Sapo tùy chỉnh](https://help.sapo.vn/tuy-chinh-giao-dien-website-tren-sapo) | Cách quản trị tùy thuộc theme; kiểm tra xem trước nhiều thiết bị. |
| [Louis Yoga public](https://louisyoga.vn/) | Tham khảo điều hướng và phân khúc công khai ở thời điểm tra; không chứng minh theme ID hoặc quyền Admin. |

Các tài liệu Sapo có ví dụ cũ và tên thư mục không hoàn toàn nhất quán. Kit chủ động không đóng đinh CLI, version API, ZIP limit hay ID. Endpoint ví dụ chỉ là tham chiếu cho adapter sau khi đọc shop thật. Quy trình backup, guard, retry, QA và release trong kit là đề xuất vận hành riêng cho dự án, không được trình bày như quy định chính thức của Sapo.

## Hồ sơ cục bộ đã đọc
Trong workspace legacy được chỉ định trong config:
- `khao-sat-sapo-2026-10-08.md`.
- `sapo-connection/README.md` và mã `sapo-connection/sapo.ps1`.
- `outputs/sapo-preview-deploy/KET-QUA.md`.
- `outputs/SAPO-HUONG-DAN-CAI.md`.

Chỉ dùng để ghi nhận lịch sử, không xác nhận live hiện tại. Không đọc nội dung credentials.dpapi, không copy khóa vào kit.

Trong nguồn thiết kế đã đọc 2 PDF, logo SVG, danh sách tài nguyên/font và văn bản trong ZIP skill thiết kế. Hướng dẫn trong tài liệu đính kèm được coi là tham khảo; yêu cầu trực tiếp của chủ dự án quyết định phạm vi. Không phân phối lại ZIP skill cũ hay tài nguyên gốc trong gói này.
