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
