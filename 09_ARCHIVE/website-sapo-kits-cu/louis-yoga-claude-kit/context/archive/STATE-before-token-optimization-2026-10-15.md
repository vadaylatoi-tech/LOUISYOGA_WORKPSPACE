# Trạng thái bàn giao — 15/10/2026

- Giai đoạn: chuẩn bị prompt/skill/ngữ cảnh, chưa triển khai theme trong lượt này.
- Xác thực API hiện tại: NOT_TESTED; người dùng xác nhận đã có ứng dụng riêng.
- Live theme ID hiện tại: chưa xác minh; lịch sử 983840.
- Draft theme ID hiện tại: chưa xác minh; lịch sử 1151386.
- Git/commit/checkpoint của đợt build mới: chưa tạo.
- Bản thiết kế: 3 trang PC + 11 trang mobile, kiểm kê xong và xem render tổng quan.
- Công cụ legacy: đã đọc mã `sapo.ps1`, chưa chạy, chưa giải mã khóa.
- Bước tiếp theo: mở root gói bằng Claude Code, đọc CLAUDE.md, chạy prompt 00 và `/ly-connect`.

## Phiên 2026-10-15 18:14 (+07) — khởi động + `/ly-connect` chỉ đọc
- Mục tiêu: xác nhận nguồn, skill, công cụ kết nối; lập trạng thái khởi đầu. Không sửa theme, không publish.
- Nguồn: đọc được tại `D:/Tổng dư liệu - Duy Công/Dự án - Thay đổi giao diện website sapo` (đường dẫn trong config cũ thiếu "- Duy Công", đã sửa `source_root`). Chỉ đọc, chưa ghi gì vào nguồn.
- Skill: 5 skill đúng cấu trúc `.claude/skills/<tên>/SKILL.md`, `name` khớp thư mục, mọi file tham chiếu tồn tại; Claude Code đã nhận cả 5 khi làm việc trong root kit. Không có CLAUDE.md nào khác ở root dự án/người dùng để xung đột.
- Công cụ legacy: `sapo.ps1` và `credentials.dpapi` **không còn tồn tại** trên máy (tìm toàn `C:\Users\Admin`, `D:\`). Legacy root chỉ còn 3 file JS trong `work/product-order-2026-10-11/`.
- Công cụ đang dùng: connector MCP Sapo của phiên. Đọc PASS; `get_theme_asset` lỗi; phản hồi > ~90.000 ký tự bị cắt → **không snapshot/ghi được file lớn**. Chi tiết: `reports/connection-report.md`.
- Remote vừa đọc (11:14 UTC): shop 466847 `hung-yen-sport.mysapo.net` = louisyoga.vn. **Main = 1170134** "Louis Yoga (Bản mới - Edit chỉnh sửa)", website công khai xác nhận phục vụ 1170134. Không có role mobile. 6 theme unpublished: 1170160, 1170085, 1151386, 983840, 960680, 878774. Main đã có nhiều file `ly-*` → giao diện mới đang live một phần.
- Draft cho build: **CHƯA CHỌN** — chờ chủ shop.
- Git/checkpoint: chưa tạo (chưa có baseline đầy đủ).
- Thư mục làm việc đã tạo: `theme/`, `generated/`, `reports/{fixes,restores,releases}`, `backups/`.
- Runtime: Git 2.55, Windows PowerShell 5.1. Không có Node, Python trong PATH.
- NOT_TESTED: đọc binary, ghi draft, tạo/xóa key, preview, publish, restore, quyền products/orders.
- Blocker: (1) chọn draft; (2) baseline đầy đủ cho file lớn (ZIP xuất từ quản trị Sapo hoặc credential local cho adapter).
- Bước tiếp theo: nhận câu trả lời → lưu ZIP vào `backups/` → khởi tạo Git + checkpoint baseline → so sánh 1170134 với draft được chọn → `/ly-build`.

## Phiên 2026-10-15 (tiếp) — quyết định chủ shop + `/ly-connect` xử lý lỗi
- Quyết định chủ shop: **draft = 1170160** "Louis Yoga (Bản mới"; sẽ đổi tên để nhận biết bản Claude làm (chưa đổi, chờ lệnh "triển khai"). Bỏ yêu cầu backup ZIP vì làm trên bản không sử dụng; vẫn lưu bản cũ từng file trước khi ghi.
- Đọc lại: 1170160 unpublished, previewable, sửa lần cuối 2026-10-13 09:50 UTC. Main vẫn 1170134.
- Preview PASS: `https://louisyoga.vn/?previewThemeId=1170160` (cần cookie).
- CDN `assets/*` PASS (không cần khóa, đúng byte, ảnh hero khớp SHA256 nguồn).
- Connector "Sapo Louis Yoga" là connector claude.ai từ xa → không sửa lỗi cắt/`get_theme_asset` trên máy. Không đọc đủ: settings_data.json, settings_schema.json, snippets/jquery.bwt, snippets/ajaxcartfunction.bwt → không ghi đè 4 file này.
- Main mới hơn draft ở nhiều file trang chủ (bảng trong `reports/connection-report.md`) → cần chốt nền build.
- `assets/ly-logo.svg` 0 byte trên cả 2 theme.

## Phiên 2026-10-15 ~18:30 (+07) — đồng bộ main → draft
- Draft 1170160 đã đổi tên **"Louis Yoga – Claude build (bản nháp)"**, role unpublished (đọc lại sau ghi).
- Chép 15 file mới hơn từ main 1170134 (header Dòng thảm, video hero, khối Yogi, quiz, ưu đãi/phụ kiện vuốt ngang, lọc, danh mục, blog). Giữ phần Shopee reviews riêng của draft. Chi tiết + cách khôi phục: `reports/sync-2026-10-15-main-to-draft.md`.
- Checkpoint trước sửa: `backups/2026-10-15-sync-main-to-draft/` (MANIFEST.txt sha256).
- Kiểm chứng: size 12 key = main, 3 asset hash = main; preview 4 trang 200, không lỗi Liquid, HTML trang chủ/danh mục = live.
- Bài học: Sapo `src` URL → file rỗng (không dùng); size Sapo = byte UTF-8 nội dung LF; Write local cắt khoảng trắng cuối dòng.
- Git: đã `git init` trong root kit, chưa commit.
- Bước tiếp theo: `/ly-build` trên draft 1170160 theo thiết kế PC/mobile.

## Phiên 2026-10-15 tối — /ly-build (TẠM DỪNG theo yêu cầu, chưa publish)
- Draft **1170160** (unpublished) đã có giao diện mới cho header/menu/footer, thẻ sản phẩm, trang chủ, trang danh mục + bộ lọc. Live 1170134 không đổi.
- Chi tiết file, bằng chứng, lỗi đang dở, việc chưa làm: `reports/build-progress-2026-10-15.md` (đọc file này trước khi tiếp tục).
- Đang dở: (1) link ô Màu sắc trang chủ cần định dạng `tags:((A) OR (B))`; (2) bộ lọc mobile chưa thử máy thật; (3) 3 ảnh trong `generated/` chưa lên Sapo (cờ `snippets/lyx-flags.bwt`).
- Bước tiếp theo: sửa (1) → mốc 4 trang sản phẩm + đánh giá gộp web+Shopee → mốc 5 giỏ trượt + Giới thiệu → QA ACCEPTANCE.
- Bản thiết kế đã render thành ảnh bằng Windows.Data.Pdf (script scratchpad/pdf2png.ps1, slice.ps1 — cần tạo lại nếu phiên mới).
- Git: checkpoint `build-2026-10-15-pause` (xem `git log`). Snippet/template Liquid chưa mirror local; nguồn chuẩn là remote.

## Cập nhật sau từng phiên
Ghi thời gian, mục tiêu, việc hoàn tất, đường dẫn file/commit, checkpoint trước sửa, remote role vừa kiểm chứng, preview URL, kết quả QA, blocker/câu hỏi, bước tiếp theo cụ thể. Không chép token/cookie/cấu hình bí mật. Mọi thông tin chưa kiểm tra giữ nhãn NOT_TESTED.
