# BÀN GIAO — Louis Yoga (cập nhật 22/10/2026 — ĐỌC PHẦN NÀY TRƯỚC)

## 00. Tóm tắt nhanh đến 22/10 (phiên mới đọc mục này + TIEN-DO.md các mục 20/10, 22/10)
- Theme **1170160 = web thật (main)**. Ghi file cần `allow_live_theme:true`; luôn sao lưu `zz-backup-<file>-<ngày>-<việc>` bằng source_key trước khi ghi, đối chiếu CDN sau khi ghi.
- **Có 2–3 phiên Claude làm song song** (máy mới của anh Công + các phiên tách nhánh). Trước khi sửa file nào: đọc bản mới nhất trên Sapo, KHÔNG ghi đè bằng bản cũ trong máy. Tài liệu của phiên máy mới có thể chưa có ở đây.
- File do phiên khác tạo (biết đến 22/10): `assets/lyx-shop.css/.js` + `templates/collection.olb.bwt` (trang danh mục kiểu Olaben, 21/10), bản 21/10 `lyx-card.js` ("ô chọn khớp ảnh"), menu/mega menu 3 cột (phiên tách nhánh 22/10).
- Đã xong 20–22/10: thẻ SP có ô màu (`ly-home-card.bwt`, `lyx-card.css/.js`), khối SP tương tự 8 thẻ (`tab_product.bwt`), lọc theo màu từ trang chủ, sửa tag màu sai 5 SP trong admin, sửa nút màu bộ lọc (`lyx-shop.css`), ảnh mới 7 phụ kiện (ảnh cũ còn giữ).
- **Đang chờ anh Công quyết:** xoá ảnh cũ 7 phụ kiện; tag màu "gần đúng" (AURA Cafe/Hồng Nhạt, Tím Huế ở G220/G320/Vòng gai, Xanh Lá ở SUNFLOWER/Bóng trơn/Túi M2261); G320 biến thể "XANH RÊU" nhưng ảnh xanh ngọc; Vòng gai có ảnh xanh lá chưa có biến thể; thiếu ảnh biến thể (Thảm Du lịch xanh cốm, ASANA 25 ảnh "cafe" là khói); xoá 2 file thử `templates/collection.lyxtest.bwt`, `snippets/lyx-card-test.bwt`.
- Thao tác admin bằng trình duyệt trong app: anh Công tự đăng nhập; API nội bộ `/admin/products/{id}.json` dùng được trong tab admin (kèm X-CSRF-Token). Tải ảnh: xem TIEN-DO.md mục "Ảnh mới cho 7 phụ kiện".


## 0. Cập nhật 20/10 — những gì đã đổi so với bản 17/10 bên dưới
- **Theme 1170160 ĐÃ LÀ WEB THẬT (role `main`) từ 19/10.** 1170134 giờ là unpublished. Mọi sửa trên 1170160 lên web ngay → chỉ sửa khi anh Công yêu cầu rõ; luôn sao lưu bằng `source_key` trước khi ghi; connector cần tham số `allow_live_theme: true` khi ghi.
- Tên sao lưu: `zz-backup-<file>-<yyyymmdd>-<việc>` (thêm hậu tố việc, vì `source_key` ghi đè bản cùng tên mà không báo).
- Cách thử Liquid an toàn trên theme đang chạy: tạo snippet bản sao (vd `snippets/lyx-card-test.bwt`) + template `templates/collection.lyxtest.bwt`, mở `https://louisyoga.vn/<danh-mục>?view=lyxtest`; kiểm xong thì chép sang file thật bằng PUT `{"asset":{"key":"<file thật>","source_key":"<bản thử>"}}`.
- Kiểm khổ 768: phải giả lập cửa sổ thật (resize_window), iframe đặt trong khung 390 bị co nên số đo sai.
- Bản BAN-GIAO 17/10 nguyên vẹn lưu ở `BAN-GIAO.ban-17-10.md`; nội dung cũ vẫn giữ bên dưới (mục 1–8), chỗ nào nói "1170160 là bản nháp / chưa xuất bản" là ĐÃ CŨ.

### Kết nối Sapo trên máy mới
- Máy cũ không có lệnh `claude` (chỉ dùng app desktop) → cách gắn: đổi tên `.mcp.json.example` (thư mục dự án) thành `.mcp.json`, anh Công tự thay `<MCP_PATH_TOKEN>` bằng mã thật, mở phiên mới, chấp nhận server `sapo-louisyoga-claude`. Hoặc thêm qua Connectors của app desktop (kiểu http).
- Claude không được tự ghi mã token vào file (bị chặn vì là thông tin đăng nhập) → anh Công tự dán.
- Mã token đã từng dán trong chat ngày 20/10 → nên đổi mã mới trên worker `louisyoga-claude-mcp` khi tiện.
- Kiểm tra: `list_themes` phải thấy **1170160 = main**.

### Việc ĐÃ XONG 20/10 (đang chạy trên web thật)
Bản thiết kế: `1. File thiết kế/2. FIle PDF/Bản thiết kế demo - khối sản phẩm - khối sản phẩm tương tự.pdf` (2 trang; render bằng Windows.Data.Pdf qua PowerShell vì không có pdftoppm).
- Thẻ sản phẩm dùng chung `snippets/ly-home-card.bwt` (trang chủ, danh mục, tìm kiếm, SP tương tự): hàng ô màu dưới ảnh (mã màu từ cài đặt theme `color_1..20` / `color_N_c`, thiếu thì JS tô theo tên), màu đang chọn đứng đầu, "+N", dòng "Màu …"; bấm ô màu → ảnh/giá/nhãn Sale đổi theo màu; bấm giỏ/Mua ngay → hộp chọn phân loại chọn sẵn màu đó.
  - PC + tablet (≥768): ô màu → "Màu …" → tên → sao | giá → nút giỏ + MUA NGAY (anh Công: tablet để giống PC).
  - Điện thoại (≤767): bản gọn — nút giỏ có dấu + ở góc phải dưới ảnh, không có MUA NGAY, 4 ô màu.
- `snippets/tab_product.bwt`: khối "Sản phẩm tương tự" 8 thẻ (cùng phân khúc → các danh mục của SP → tất cả SP), thẻ bản gọn mọi khổ; PC/tablet 4×2, điện thoại 2×3; tiêu đề 1 dòng; "Xem thêm sản phẩm" gạch chân ở giữa.
- File mới: `assets/lyx-card.css`, `assets/lyx-card.js` — nạp 1 lần từ thẻ đầu tiên (cờ Liquid `lyc_assets_done`). `lyx-home.css` KHÔNG sửa.
- Sao lưu: `snippets/zz-backup-ly-home-card-20261020-card.bwt`, `snippets/zz-backup-tab_product-20261020-card.bwt`, `assets/zz-backup-lyx-home-20261020-card.css`.
- File thử còn trên theme (chờ anh Công cho xoá): `templates/collection.lyxtest.bwt`, `snippets/lyx-card-test.bwt` (không có link nào trỏ tới).

### ✅ ĐÃ XONG 22/10 — lọc theo màu (chi tiết: TIEN-DO.md mục 22/10). Phần dưới giữ để tham khảo
**Yêu cầu anh Công:** ở khối "Tìm màu sắc của bạn" trang chủ, bấm 1 màu (vd Xanh) → sang trang kết quả thì **mọi thẻ sản phẩm hiện ảnh đúng màu đó**.
- Link các ô màu trang chủ: `/collections/all?q=tags:((Xanh Đậm) OR (Xanh Coban) OR (Xanh Ngọc))&page=1&view=grid` (Hồng: Hồng/Hồng Nhạt; Khói: Ghi Khói/Ghi Đậm; Xanh lá: Xanh Lá/Xanh Rêu/Xanh Cốm; Đen; Trắng).
- **3 file đã soạn xong, CHƯA GHI** (connector bị ngắt), nằm ở `4. Hiện trạng/cho-ghi-20261020-loc-mau/`:
  1. `ly-home-card.bwt` → ghi vào `snippets/ly-home-card.bwt`: in tối đa 20 ô màu thay vì 6 (`lyc_swn <= 20`) để ô ẩn vẫn mang ảnh của màu.
  2. `lyx-card.css` → `assets/lyx-card.css`: thêm `.lyx-sw:nth-of-type(n+7){display:none!important}` (PC chỉ hiện 6 ô).
  3. `lyx-card.js` → `assets/lyx-card.js`: hàm `wanted()` đọc màu từ `?q=tags:(...)`, `?mau=` và ô tick đang chọn của bộ lọc (`.filter-item--check-box input:checked`, `data-text`); `applyWanted()` cho mỗi thẻ chọn ô màu khớp (đúng tên trước, chứa tên sau), ô bị ẩn được đưa lên đầu hàng; chạy lúc tải trang + mỗi khi lưới đổi (MutationObserver).
  - (`tab_product.bwt.DA-GHI` chỉ là bản đã ghi lên web, để tham khảo — không cần ghi lại.)
- Đã thử logic JS ngay trên trang thật (chèn bằng trình duyệt): trang "Xanh" 18/18 thẻ đổi ảnh; trang "Khói" 12/18 — 6 thẻ còn lại có màu ghi nằm ngoài 6 ô đầu → sẽ được khi ghi bản thẻ in 20 ô.
- **Các bước:** (1) đọc bản mới nhất 3 file trên Sapo, so với bản trong thư mục (nếu trên Sapo đã khác bản đã ghi 20/10 thì dừng, hỏi anh); (2) sao lưu bằng source_key: `snippets/zz-backup-ly-home-card-20261020-mau.bwt`, `assets/zz-backup-lyx-card-20261020-mau.css`, `assets/zz-backup-lyx-card-20261020-mau.js`; (3) ghi CSS + JS (put_theme_asset, allow_live_theme), đối chiếu CDN `https://bizweb.dktcdn.net/100/466/847/themes/1170160/assets/<file>?v=$RANDOM`; (4) ghi thẻ: tốt nhất ghi vào `snippets/lyx-card-test.bwt`, kiểm `?view=lyxtest`, rồi chép sang `ly-home-card.bwt` bằng source_key; (5) kiểm 6 nhóm màu ở 1440 / 768 / 390, kiểm không tràn ngang, trang SP vẫn chọn biến thể được.

### Ghi chú nhỏ
- Điện thoại: tên màu dài bị cắt ("Màu xanh r…") vì cùng dòng với sao + số lượt — có thể bỏ "(10)" ở bản điện thoại nếu anh muốn.
- Console trang danh mục có `colId is not defined` — lỗi có sẵn của template danh mục, không do thẻ.
- Quy tắc 20/10 của sếp anh Công: không dùng mảng/nút màu ĐEN trên toàn site (dùng đỏ rượu #4a1f2b / #5a2333).

---

# BÀN GIAO CHO PHIÊN CLAUDE CODE MỚI — Louis Yoga (cập nhật 17/10/2026, cuối ngày)

Anh Công đổi máy + đổi tài khoản Claude. Bộ nhớ của Claude trên máy cũ **không đi theo**, nên mọi thứ cần biết nằm trong thư mục `4. Hiện trạng/`:

| Thứ tự đọc | File | Nội dung |
|---|---|---|
| 1 | `BAN-GIAO.md` (file này) | Cách kết nối, cách làm việc đã kiểm chứng, bẫy kỹ thuật, việc còn lại |
| 2 | `TIEN-DO.md` | Từng trang đã làm: file nào, sao lưu ở đâu, trạng thái duyệt |
| 3 | `CLAUDE.md` | Rà soát hiện trạng ban đầu (sáng 17/10) — quy tắc §0, token màu §3, kiến trúc §2, bẫy §7 vẫn đúng; **bảng trạng thái §4 và §6 đã CŨ** (xem TIEN-DO.md) |
| — | `HIEN_TRANG_LOUISYOGA_1170160_2026-10-17.md` | Bản gần giống CLAUDE.md, chỉ để tham khảo |

---

## 1. Tóm tắt dự án (đọc trong 30 giây)

- Website **louisyoga.vn** (Sapo/Bizweb). Đồng bộ toàn site theo phong cách **"Editorial sang trọng"**: nền trắng/kem `#f8f5f0`, nút hành động đỏ rượu `#5a2333`, chữ Montserrat, tiêu đề in hoa giãn chữ, nút bo tròn, đường kẻ mảnh `#e7e2dc`.
- Làm **chỉ trên theme nháp `1170160`** ("Louis Yoga – Claude build (bản nháp)"). Web thật là theme **`1170134`** (main) — **chưa động tới, chưa xuất bản**.
- **Tất cả các trang đã làm xong và anh Công đã duyệt** (trang chủ, danh mục, SP, giỏ trượt, /cart, blog/báo chí/bài viết, liên hệ, giới thiệu, tìm kiếm, tài khoản, chính sách, 404). Đã kiểm toàn site 16 trang × 4 khổ 390/768/1024/1440: đạt hết.
- Ngày 17/10 cuối ngày: sửa các câu chính sách sai trong theme nháp (anh đã duyệt). Còn 2 chỗ anh tự sửa trong admin + vài quyết định chờ anh (mục 7).
- **Bước tiếp theo**: chờ anh Công sửa admin + quyết các mục chờ → anh **tự xuất bản trong Sapo admin** → Claude kiểm lại web thật bằng user-agent điện thoại.

## 2. Kết nối Sapo trên máy/tài khoản mới

Công cụ cần có trong phiên: `sapo_request`, `put_theme_asset`, `list_themes`, `list_theme_assets` (tiền tố MCP `sapo-louisyoga-claude`).

- Máy chủ MCP là Cloudflare worker **`louisyoga-claude-mcp`** (tài khoản Cloudflare của anh, tên miền `vadaylatoi.workers.dev`), nối với app riêng trên Sapo **"Claude - Sapo connector Louis Yoga" (id 14806)** của cửa hàng `hung-yen-sport.mysapo.net`.
- **KHÔNG dùng / KHÔNG sửa** worker cũ `sapo-louisyoga` và app "ChatGPT - Chỉnh giao diện Louis Yoga" (của người khác).
- Đường dẫn MCP: `https://louisyoga-claude-mcp.vadaylatoi.workers.dev/mcp/<MCP_PATH_TOKEN>` — kiểu `http`.
  - Mã `<MCP_PATH_TOKEN>` nằm ở máy cũ: `C:\Users\ADMIN\Documents\louisyoga-mcp-token.txt` (hoặc trong `~/.claude.json` máy cũ). **Anh tự chép mã sang máy mới, không dán vào tài liệu/chat công khai.**
- Cách gắn trên máy mới (một trong hai):
  1. Trong thư mục dự án có file mẫu `.mcp.json.example` → đổi tên thành `.mcp.json`, thay `<MCP_PATH_TOKEN>` bằng mã thật, mở lại Claude Code, chấp nhận server.
  2. Hoặc chạy lệnh: `claude mcp add --transport http sapo-louisyoga-claude https://louisyoga-claude-mcp.vadaylatoi.workers.dev/mcp/<MCP_PATH_TOKEN>`
  - Hoặc thêm qua giao diện kết nối (Connectors) của Claude desktop nếu dùng bản desktop.
- Kiểm tra kết nối: gọi `list_themes` → phải thấy `1170134` role `main` và `1170160` unpublished. Nếu ID/vai trò khác → dừng, hỏi anh Công.
- Nếu công cụ chưa hiện: vẫn gọi được worker bằng JSON-RPC (POST `tools/list`, `tools/call`) tới đúng URL trên.

## 3. Quy tắc bắt buộc (anh Công đặt)

- Xưng **em**, gọi **anh Công**, trả lời tiếng Việt, ngắn gọn, phân biệt dữ kiện / suy luận / đề xuất.
- **Không ghi, không xuất bản theme 1170134** nếu anh chưa đồng ý rõ cho từng việc. Xuất bản do anh làm **trong Sapo admin** (API chỉ đổi giao diện máy tính, điện thoại vẫn nhận theme cũ — sự cố 10/10).
- **Không dùng 2 bộ kit cũ** (`louis-yoga-claude-kit`, `Louis-Yoga-Claude-Code-Kit`) — không đọc, không tìm, không hỏi.
- Không tự đăng nhập, không thao tác giỏ hàng/đơn thật, không đổi logic Sapo Checkout, không đổi dữ liệu sản phẩm, không xoá file/sao lưu khi chưa được duyệt.
- Không tự sáng tác chính sách, cam kết, đánh giá, khuyến mãi, hotline. Chỉ dùng nội dung/ảnh có sẵn. Đánh giá chỉ dùng dữ liệu thật.
- Giữ nguyên: `selectCallback`, `Bizweb.OptionSelectors`, gallery Swiper (`templates/product.bwt` — không viết lại), script vá `Bizweb.formatMoney` trong `layouts/theme.bwt`, mọi `data-*` móc JS, id/class form tài khoản (JS Firebase/SMS).
- Tiết kiệm token nhưng **không được bỏ**: xác minh theme, đọc file mới nhất trước khi ghi, sao lưu, kiểm tra chức năng.
- Làm từng trang → cho anh xem → anh duyệt ("Duyệt trang X. Làm tiếp Y") rồi mới sang trang khác. Anh hay góp ý bằng ảnh chụp màn hình.

## 4. Cách làm đã kiểm chứng

**Đọc 1 file theme**: `sapo_request` GET `themes/1170160/assets.json`, query `{"key":"templates/search.bwt"}` → `asset.value`. (`get_theme_asset` bị lỗi: trả cả danh sách.) Thư mục layout là `layouts/` (không phải `layout/`). Danh sách asset bị cắt ở ~247 mục → không liệt kê được `templates/…`; đọc thẳng theo key.

**Sao lưu trước khi ghi (không tốn token)**: `sapo_request` PUT `themes/1170160/assets.json` body `{"asset":{"key":"snippets/zz-backup-<tên>-<yyyymmdd>.bwt","source_key":"<file gốc>"}}` (CSS/JS: `assets/zz-backup-….css`). Nếu đã có bản cùng tên thì thêm `-v2`.

**Ghi**: `put_theme_asset` (theme_id 1170160) — **gửi toàn bộ nội dung file** (ghi đè). Sửa nhỏ cũng phải gửi lại cả file → soạn file ở thư mục tạm, sửa, rồi gửi.

**Đối chiếu sau khi ghi (CSS/JS)**: `curl https://bizweb.dktcdn.net/100/466/847/themes/1170160/assets/<file>?v=$RANDOM | tr -d '\r'` rồi `diff` với bản cục bộ (chỉ được lệch dòng trống cuối file).

**Xem trước**: `https://louisyoga.vn/<đường dẫn>?previewThemeId=1170160` — **không cần đăng nhập**. Dùng trình duyệt trong app:
- Tải trang ở khổ máy tính **rồi mới** thu về 390px (tải lại ở khổ điện thoại = user-agent điện thoại → Sapo trả theme live).
- Ảnh chụp màn hình hay bị trễ 1 nhịp sau khi cuộn → cuộn, chờ 1s, chụp 2 lần; kiểm số đo bằng JS (`getComputedStyle`) chắc hơn ảnh.
- Muốn xem giỏ có hàng / trang trong tài khoản: **chèn DOM mẫu** bằng JS, không thêm hàng thật, không đăng nhập.
- Tab xem trước có thể bị người dùng bấm chuyển trang → chạy kiểm tra dài trong **tab riêng** (`tabs_create`).

**Kiểm tra toàn site tự động** (đã dùng 17/10): trong tab riêng, tạo iframe cùng nguồn rộng `W+15px` (trừ thanh cuộn) cho từng trang × khổ, đo `documentElement.scrollWidth` > `clientWidth` (tràn ngang), ảnh `naturalWidth==0` (ảnh lỗi), có link asset `1170160` (đúng theme nháp). Lệnh JS bị giới hạn 45 giây → chạy nền, ghi kết quả dần vào `localStorage`, gọi lại để đọc.

**Máy cũ không có python/node** — dùng bash/PowerShell; ảnh ghép xem nhanh bằng System.Drawing (PowerShell).

## 5. Kiến trúc lớp giao diện mới (theme 1170160)

Thứ tự CSS (§2.2 CLAUDE.md): gốc Sapo < `ly-*` (09–13/10) < `lyx-*` < `lyx-editorial.css`. CSS cũ của theme nạp **cuối trang** với nhiều `!important` → file mới nạp trong `<head>` phải dùng tiền tố mạnh (`html body .lớp…`) + `!important`.

| Trang | Template / snippet | CSS / JS riêng | Nạp ở đâu |
|---|---|---|---|
| Trang chủ | `snippets/lyx-home.bwt` | `lyx-home.css/.js` | layout |
| Header / footer | `snippets/lyx-header.bwt`, `lyx-footer.bwt` | `lyx-base.css` | layout |
| Danh mục | `templates/collection.bwt`, `snippets/lyx-sale.bwt` | `lyx-col.css/.js` | layout |
| Sản phẩm | `templates/product.bwt` (gốc) + `tab_product.bwt`, `ly-promos.bwt` | `lyx-pdp.css/.js`, `lyx-editorial.css` | layout |
| Giỏ trượt | `snippets/ly-cart-drawer.bwt` | `lyx-cart.css/.js` | snippet |
| /cart | `templates/cart.bwt` | cuối `ly-cart.css` | layout |
| Blog / báo chí / bài viết / liên hệ | `templates/blog*.bwt`, `article.bwt`, `page.contact.bwt` | **`lyx-pages.css`** | `snippets/ly-favicon.bwt` (mọi trang trừ trang chủ) |
| Giới thiệu | `templates/page.about.bwt` → **`snippets/lyx-gt.bwt`** | **`lyx-gt.css`** (hiệu ứng JS nằm trong snippet) | template |
| Tìm kiếm | `templates/search.bwt` | **`lyx-search.css`** | template |
| Tài khoản (đăng nhập, đăng ký, TK, đơn, địa chỉ) | `templates/customers/*` **giữ nguyên** | **`lyx-account.css`** (chỉ CSS) | `ly-favicon.bwt` khi `template contains 'customers'` |
| Chính sách / trang nội dung, 404 | `templates/page.bwt`, `templates/404.bwt` | **`lyx-page.css`** | template |

Các trang mới dùng chung khung `.lyxc` của danh mục (breadcrumb `.lyxc-crumb`, đầu trang kem `.lyxc-hero`, lưới `.ly-grid.ly-collection-grid`, phân trang tròn) và thẻ SP chung `snippets/ly-home-card.bwt`.

Dữ liệu cấu hình: phân khúc `snippets/ly-segments.bwt`; cờ trang chủ/video/màu `snippets/lyx-flags.bwt`; thông tin liên hệ lấy từ cài đặt theme (`settings.store_phone`, `store_phone1`, `store_email`, `social_*`).

## 6. Bẫy kỹ thuật gặp trong các phiên 17/10

- Thân trang có class `ly-template-{{template}}`; trang tài khoản ra `ly-template-customers/login` (có dấu `/`) → chọn bằng `body[class*="ly-template-customers"]`.
- Trong CSS grid, `position:sticky` bị giới hạn theo cả `.row` → không dùng sticky cho khối thông tin trang SP.
- **Chữ viền (`-webkit-text-stroke`) với Montserrat bản biến thiên lộ nét chồng bên trong** → không dùng chữ viền, dùng chữ đặc nét mảnh.
- CSS cũ ép `h1/h2/p/button` (font, căn trái) → luôn khai `font`, `text-align` kèm `!important` ở trang mới.
- Hiệu ứng vào cảnh: chỉ bật khi JS thêm class (vd. `.lygt-anim`), tắt khi `prefers-reduced-motion`/tab ẩn, luôn tự hiện hết sau 2,5s (tránh kẹt nội dung ẩn).
- Liquid Sapo: tránh tag Liquid trong comment HTML; số "4,8" bị đọc thành 48 (đã xử lý trong `ly-home-card`).
- Sed trong bash dễ phá chuỗi `\u00a0`, `\s` → sửa file bằng công cụ Edit thay vì sed với biểu thức có dấu `\`.
- Nội dung trang chính sách soạn trong admin có style dán tay (Times New Roman, màu) → `lyx-page.css` đè bằng `!important`, không sửa chữ; JS trong `page.bwt` chỉ gắn class tiêu đề cho đoạn đậm bắt đầu "I./II.…" và "1./2.…".
- Console luôn có cảnh báo CSP report-only của khung Google reCAPTCHA — có sẵn, bỏ qua.

## 7. Việc còn lại

**Anh Công tự làm trong admin** (chi tiết ở TIEN-DO.md mục "Câu chính sách"):
1. Tùy chỉnh giao diện → chính sách trang SP: `policy_title_2` "Luôn có 7 ngày đổi trả miễn phí" → "Đổi mới trong 10 ngày nếu sản phẩm lỗi"; `policy_title_4` "Chính sách 1 đổi 1 nếu không hài lòng" → "Đổi theo nhu cầu trong 3 ngày" (làm ở cả theme nháp và theme đang chạy).
2. Trang nội dung "Chính sách kiểm hàng": câu "đổi trả … trong vòng 7 ngày" → "Sản phẩm lỗi do nhà sản xuất được đổi mới trong vòng 10 ngày; đổi theo nhu cầu trong vòng 03 ngày kể từ ngày nhận hàng (sản phẩm chưa sử dụng)."

**Chờ anh quyết (không tự sửa):**
- "Giao nhanh trong 24h" (dải thông báo + trang SP): áp dụng mọi khu vực hay chỉ nội thành?
- Hotline thống nhất: 0888.293.996 (header, liên hệ) hay CSKH 0352 587 836 (trang chính sách)?
- Đếm ngược "tới cuối tháng" ở khối sale (`lyx_sale_cd='month'` trong `lyx-flags.bwt`) — nên đặt ngày thật ở cài đặt `ly_home_sale_end` khi có chương trình.
- Chữ cứng "Săn sale mùa thu đông" (`lyx-home.bwt`, `lyx-sale.bwt`).
- Dữ liệu admin "Top Brands ASIA FACIFIC" (trang Giới thiệu đang tự hiển thị "PACIFIC" bằng `replace`).
- Ảnh tạm Unsplash ở 2 thẻ danh mục trang chủ (`lyx_cat_img_1/2`), MP4 cho hero trang chủ (`lyx_hero_mp4_*` đang trống).

**Khi anh xuất bản xong** (anh làm trong admin): Claude kiểm web thật (theme main mới) ở 390/768/1024/1440, kiểm bằng user-agent điện thoại, kiểm `galleryThumbs`, chọn biến thể, giỏ trượt mở được, console sạch. Không thao tác đơn thật.

**Chưa kiểm được**: trang trong tài khoản với dữ liệu thật (cần đăng nhập — đã dựng thử bằng DOM mẫu, hiển thị đúng); Sapo Checkout.

## 8. Khôi phục nếu cần

Mỗi file đã sửa có bản `zz-backup-…` trên chính theme 1170160 (danh sách đầy đủ trong TIEN-DO.md). Khôi phục = PUT với `source_key` = file sao lưu, `key` = file gốc (hỏi anh Công trước). Theme 1170134 (web thật) và 983840 (gốc) là nguồn đối chiếu bản cũ.
