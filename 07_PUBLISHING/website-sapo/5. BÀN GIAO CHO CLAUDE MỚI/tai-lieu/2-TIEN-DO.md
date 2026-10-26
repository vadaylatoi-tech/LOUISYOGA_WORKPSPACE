# TIẾN ĐỘ ĐỒNG BỘ GIAO DIỆN — theme nháp 1170160 (cập nhật 17/10/2026)

Đọc `BAN-GIAO.md` trước (kết nối, quy tắc, cách làm, việc còn lại), rồi file này, rồi `CLAUDE.md` cùng thư mục. Mọi sửa chỉ trên theme nháp **1170160**; web thật **1170134** chưa động tới; chưa xuất bản.

## Đã xong (anh Công đã duyệt)
| Trang | File đã sửa | Sao lưu trên Sapo |
|---|---|---|
| Giỏ hàng `/cart` | `templates/cart.bwt`, `assets/ly-cart.css` (khối cuối file) | `snippets/zz-backup-cart-20261017.bwt`, `assets/zz-backup-ly-cart-20261017.css` |
| Trang SP | `assets/lyx-pdp.css`, `assets/lyx-pdp.js` (6 ảnh/trang, ảnh 1024px, bỏ dòng "Dòng thảm – Phân khúc"), `assets/lyx-editorial.css`, `snippets/ly-promos.bwt` (2 thẻ CTA như danh mục), ẩn nút "Xem tất cả trên Shopee" | `zz-backup-lyx-pdp-20261017.js/.css`, `zz-backup-lyx-editorial-20261017.css`, `zz-backup-ly-promos-20261017.bwt` |
| Giỏ trượt | `assets/lyx-cart.css` | `zz-backup-lyx-cart-20261017.css` |
| Danh mục | `snippets/lyx-sale.bwt` (khối sale mobile theo bản thiết kế, có đếm ngược), `assets/lyx-col.css` (bộ lọc PC 260px, màu lọc đỏ rượu, phân trang), `assets/lyx-col.js` (đếm ngược) | `zz-backup-lyx-sale-20261017.bwt`, `zz-backup-lyx-col-20261017.css/.js` |
| Blog / Báo chí / Bài viết | **file mới** `assets/lyx-pages.css`, nạp qua `snippets/ly-favicon.bwt` (mọi trang trừ trang chủ) | `zz-backup-ly-favicon-20261017.bwt` |
| Liên hệ | `templates/page.contact.bwt` (dựng lại bố cục, không ảnh; hotline tách từng số `tel:`), CSS trong `lyx-pages.css` (.lyxct-*) | `snippets/zz-backup-page-contact-20261017.bwt` |

## Kiểm tra toàn site 17/10 (bước cuối giai đoạn 3)
- Tự động 16 trang × 4 khổ (390/768/1024/1440) bằng iframe cùng nguồn trên preview 1170160: trang chủ, /collections/all, /tham-yoga-cao-su, SP MOON, SP Đệm kê gối, /cart, tìm kiếm "thảm", /tin-tuc, bài viết so sánh thảm, báo chí, liên hệ, giới thiệu, đăng nhập, đăng ký, chính sách kiểm hàng, 404 → **64/64 đạt**: không tràn ngang, không ảnh lỗi (ảnh đã tải), đều đúng theme nháp.
- Console: không có lỗi JS (Uncaught/TypeError) ở 16 trang. Chỉ có cảnh báo CSP report-only của khung Google reCAPTCHA (có sẵn, không ảnh hưởng).
- Trang SP: `galleryThumbs` (Swiper) còn sống, bộ chọn biến thể có, `Bizweb.formatMoney()` → "123.400.000₫" (script vá vẫn chạy).
- Xem ảnh: trang chủ + SP ở 768 và 1024 hiển thị đúng bố cục.
- Chưa kiểm được: trang trong tài khoản (cần đăng nhập), thanh toán Sapo Checkout (không thao tác đơn thật).

## Chính sách / trang nội dung + 404 — ĐÃ DUYỆT 17/10
- `templates/page.bwt` (mọi trang nội dung) dựng lại trong khung `.lyxc`: breadcrumb, đầu trang kem, thanh bên 6 chính sách (chỉ hiện ở 6 trang chính sách footer), nội dung, khối "Cần hỗ trợ" (hotline/Zalo từ cài đặt). `templates/404.bwt` mới (số 404 lớn, ô tìm, 3 link). CSS **`assets/lyx-page.css`** (nạp trong 2 template).
- Nội dung chính sách KHÔNG sửa chữ; CSS đè phông Times/màu dán tay; JS chỉ gắn class tiêu đề cho đoạn đậm bắt đầu "I./II.…" và "1./2.…".
- Sao lưu: `snippets/zz-backup-page-20261017.bwt`, `snippets/zz-backup-404-20261017.bwt`.

## Tài khoản khách hàng — ĐÃ DUYỆT 17/10 (theo bản dựng thử)
- **Chỉ CSS**, không sửa template `customers/*` (JS đăng nhập Firebase/SMS và sổ địa chỉ bám id/class cũ). File mới **`assets/lyx-account.css`**, nạp qua `snippets/ly-favicon.bwt` khi `template contains 'customers'` (sao lưu favicon: `snippets/zz-backup-ly-favicon-v2-20261017.bwt`).
- Đăng nhập / quên mật khẩu / đăng ký: đã xem preview 1440 + 390. Trang tài khoản, đơn hàng, chi tiết đơn, sổ địa chỉ: **chưa xem được** (cần đăng nhập — quy tắc không tự đăng nhập), chỉ tạo kiểu theo mã nguồn; đã dựng thử bằng dữ liệu mẫu chèn vào DOM (thông tin TK, danh sách đơn, sổ địa chỉ) ở 1440 → hiển thị đúng. Anh Công báo "không đăng nhập được": template + customer-firebase-login.js bản nháp giống hệt web thật (chỉ khác CSS) → chưa rõ nguyên nhân, đang hỏi lại hiện tượng.

## Tìm kiếm — ĐÃ DUYỆT 17/10
- `templates/search.bwt` dựng lại trong khung `.lyxc` của trang danh mục (breadcrumb, đầu trang kem, lưới 4/3/2 cột, phân trang tròn) + thẻ SP chung `ly-home-card`; CSS riêng **`assets/lyx-search.css`** (nạp trong template).
- Có 3 trạng thái: chưa nhập từ khoá (ô tìm + chip "Tìm kiếm phổ biến" + 4 SP ưu đãi), có kết quả (đếm, trang x/y), không có kết quả (gợi ý, nút xem tất cả / tư vấn, chip, 4 SP ưu đãi).
- Sao lưu: `snippets/zz-backup-search-20261017.bwt`.

## Giới thiệu — ĐÃ DUYỆT 17/10 (dựng lại toàn bộ)
- `templates/page.about.bwt` giờ chỉ gọi **snippet mới `snippets/lyx-gt.bwt`** + **CSS mới `assets/lyx-gt.css`** (lớp `.lygt-*`). Không nạp `ly-about.css`/`lyx-about.css` nữa; snippet cũ `lyx-about`/`ly-about` vẫn còn trên theme.
- Sao lưu template cũ: `snippets/zz-backup-page-about-20261017.bwt`.
- Bố cục: hero chữ kem + 4 số liệu (2015 · số năm · số giải · Hoa sen) → Về Louis Yoga (ảnh img_video_6) → Nền tảng (content_video) → Giá trị cốt lõi 2×2 → Văn hoá Việt (nền đỏ rượu) → Hoa hậu Nguyễn Thị Huyền (img_bantab1, câu trích từ ảnh có chữ ký) → Giải thưởng (about.png + danh sách) → Báo chí (3 bài, logic link ngoài như trang chủ) → Kêu gọi. Video mở hộp thoại YouTube.
- 17/10 bản 2 (góp ý "typo chưa đẹp, thiếu animation"): hero 2 cột — chữ "LOUIS" đặc + "YOGA" viền đỏ rượu cỡ lớn, ảnh ghép thật (img_video_4 nhóm tập, img_video_2 Hoa hậu), con dấu tròn xoay "LOUIS YOGA • TẬP CHUẨN ĐỀU NHỊP • TỪ 2015". Hiệu ứng: chữ trồi từng dòng, ảnh mở dần, khối hiện khi cuộn, số liệu đếm lên, ảnh trôi nhẹ khi cuộn (PC); tắt khi giảm chuyển động, tự hiện hết sau 2,5s. Bản 1 lưu ở `snippets/zz-backup-lyx-gt-v1-20261017.bwt`.
- Hiển thị "FACIFIC" → "PACIFIC" bằng `replace` trong snippet (dữ liệu admin vẫn sai).
- Bỏ ảnh minh hoạ hồng (giatri.png, video.png) và ảnh bìa YouTube kiểu quảng cáo.

## Còn lại
- Toàn bộ trang đã đồng bộ + kiểm xong. Trước khi xuất bản: anh Công quyết các mục "Chờ anh Công quyết" bên dưới, rồi tự xuất bản trong Sapo admin (không qua API) và kiểm lại bằng điện thoại thật.
Trang phụ mới: thêm CSS vào `assets/lyx-pages.css` (selector `html body.ly-template-…` + `!important` vì CSS cũ nạp sau).

## Cách làm đã kiểm chứng
- Đọc file: `sapo_request` GET `themes/1170160/assets.json` query `{"key":"..."}` (`get_theme_asset` lỗi, trả cả danh sách).
- Sao lưu nhanh không tốn token: PUT `themes/1170160/assets.json` body `{"asset":{"key":"…zz-backup…","source_key":"<file gốc>"}}`.
- Xem trước: trình duyệt trong app, `louisyoga.vn/<đường dẫn>?previewThemeId=1170160` (không cần đăng nhập). Tải ở khổ máy tính rồi mới thu về 390px (user-agent điện thoại làm Sapo trả theme live). Muốn xem giỏ có hàng: chèn DOM mẫu, không thêm hàng thật.
- Đối chiếu sau khi ghi: tải CSS/JS từ CDN `bizweb.dktcdn.net/100/466/847/themes/1170160/assets/<file>` rồi `diff`.

## Câu chính sách — anh Công duyệt 17/10, ĐÃ SỬA trong theme nháp
Căn cứ trang /chinh-sach-bao-hanh-doi-tra-san-pham: lỗi NSX đổi mới trong 10 ngày (Louis Yoga chịu ship); đổi theo nhu cầu trong 03 ngày (chưa dùng, khách chịu ship 2 chiều).
- `snippets/lyx-header.bwt` dải thông báo: "Luôn có 7 ngày đổi trả miễn phí" → "Đổi mới trong 10 ngày nếu sản phẩm lỗi"; "Chính sách 1 đổi 1 nếu không hài lòng" → "Đổi theo nhu cầu trong 3 ngày". Sao lưu `zz-backup-lyx-header-20261017.bwt`.
- `templates/collection.bwt` + `snippets/ly-promos.bwt` thẻ Bảo hành: "Lỗi 1 đổi 1 giao hàng tiện lợi" → "Lỗi nhà sản xuất đổi mới trong 10 ngày". Sao lưu `zz-backup-collection-20261017.bwt`, `zz-backup-ly-promos-v2-20261017.bwt`.
- `templates/cart.bwt`: "Bảo hành sản phẩm — chính sách 1 đổi 1" → "— đổi mới trong 10 ngày nếu lỗi nhà sản xuất". Sao lưu `zz-backup-cart-v2-20261017.bwt`.
- CÒN TRONG ADMIN (anh Công tự sửa): Tùy chỉnh giao diện → chính sách trang SP `policy_title_2` ("Luôn có 7 ngày đổi trả miễn phí") và `policy_title_4` ("Chính sách 1 đổi 1 nếu không hài lòng") — dùng chung cho web thật; Trang nội dung "Chính sách kiểm hàng" mục THỜI GIAN ĐỔI TRẢ ghi "7 ngày".

## Chờ anh Công quyết (không tự sửa)
- "Giao nhanh trong 24h" (dải thông báo + trang SP) — không có trong trang chính sách, cần xác nhận phạm vi.
- Hotline: header/liên hệ dùng 0888.293.996; trang chính sách ghi CSKH 0352 587 836.
- Đếm ngược "tới cuối tháng" (`lyx_sale_cd='month'`) — anh đã yêu cầu hiện trên danh mục; nên đặt ngày thật ở `ly_home_sale_end` khi có chương trình.
- "Top Brands ASIA FACIFIC" (sai chính tả, trong dữ liệu trang Giới thiệu).
- Tiêu đề khối sale "Săn sale mùa thu đông" viết cứng.
