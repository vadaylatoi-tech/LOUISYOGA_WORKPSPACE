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

## 20/10/2026 — Thẻ sản phẩm + khối "Sản phẩm tương tự" (bản thiết kế `1. File thiết kế/2. FIle PDF/Bản thiết kế demo - khối sản phẩm - khối sản phẩm tương tự.pdf`)
Lưu ý: từ 19/10 theme **1170160 là web thật (main)** — sửa trực tiếp, đã sao lưu trước.
- `snippets/ly-home-card.bwt` (thẻ dùng chung: trang chủ, danh mục, tìm kiếm, SP tương tự): thêm hàng ô màu dưới ảnh (mã màu từ cài đặt theme `color_N`/`color_N_c`, thiếu thì JS tô theo tên), màu đang chọn đứng đầu, "+N"; dòng "Màu …". Bấm ô màu → ảnh/giá/nhãn Sale đổi theo màu; bấm giỏ/Mua ngay → hộp chọn phân loại chọn sẵn màu đó.
- **PC + máy tính bảng (≥768)**: ô màu (6) → "Màu …" → tên → sao | giá → nút giỏ + MUA NGAY. **Điện thoại (≤767)**: bản gọn — giỏ có dấu + ở góc ảnh, không có MUA NGAY, 4 ô màu.
- `snippets/tab_product.bwt`: khối SP tương tự 8 thẻ (cùng phân khúc → danh mục của SP → tất cả SP), thẻ bản gọn ở mọi khổ; PC/tablet 4×2, điện thoại 2×3; tiêu đề 1 dòng; "Xem thêm sản phẩm" gạch chân giữa.
- File mới: `assets/lyx-card.css`, `assets/lyx-card.js` (nạp 1 lần từ thẻ đầu tiên). `lyx-home.css` không sửa.
- Sao lưu: `snippets/zz-backup-ly-home-card-20261020-card.bwt`, `snippets/zz-backup-tab_product-20261020-card.bwt`, `assets/zz-backup-lyx-home-20261020-card.css` (chưa dùng tới).
- File thử còn trên theme (chờ anh Công cho xoá): `templates/collection.lyxtest.bwt`, `snippets/lyx-card-test.bwt`.
- Đã kiểm: 390/768/1000/1440 trang chủ, danh mục, tìm kiếm, trang SP — không tràn ngang; chọn biến thể + gallery trang SP còn chạy.

## 22/10/2026 — Lọc theo màu (khối "Tìm màu sắc" trang chủ) — ĐÃ LÊN WEB
- Rà soát trước khi làm: trên Sapo, từ 20/10 chỉ `assets/lyx-card.js` đổi (bản 21/10 của phiên máy mới: "ô chọn khớp ảnh", sao lưu `assets/zz-backup-lyx-card-20261021-mau.js`). `ly-home-card.bwt`, `tab_product.bwt`, `templates/product.bwt`, `ly-pdp-mobile.bwt` và mọi CSS/JS trang SP chưa đổi. Tài liệu của phiên máy mới KHÔNG có trong thư mục này — chép về để gộp.
- Bấm 1 màu ở trang chủ → trang `/collections/all?q=tags:((…))`: mọi thẻ tự chọn ô màu khớp (đúng tên → tên ô chứa tên lọc → tên lọc chứa tên ô, vd "ghi đậm" ⊃ "ghi"), chỉ xét màu có ảnh, ô chọn đưa lên đầu, ảnh đổi ngay. Áp cả khi tick màu ở bộ lọc danh mục và link `?mau=`.
- `snippets/ly-home-card.bwt`: in tối đa 20 ô màu (trước 6); `assets/lyx-card.css`: ẩn ô thứ 7+ (PC); `assets/lyx-card.js`: thêm bước 5 (ghép vào bản 21/10, giữ nguyên bước 4) + sửa lỗi ảnh tải chậm đè ảnh màu đã chọn.
- Sao lưu: `assets/zz-backup-lyx-card-20261022-loc.js/.css`, `snippets/zz-backup-ly-home-card-20261022-loc.bwt`.
- Kiểm 6 nhóm (1300px): Xanh 12/12, Hồng 11/11, Khói 12/12, Xanh lá 11/12, Đen 9/9, Trắng 3/3 thẻ có ảnh khớp ô chọn; 390px: 18/18 ô chọn đứng đầu, không tràn ngang.
- Còn lệch do DỮ LIỆU SẢN PHẨM (sửa trong admin, không phải giao diện): F23 gắn tag Đen/Khói nhưng không có biến thể đen/ghi; Khăn lau mồ hôi — hồng phấn chưa có ảnh biến thể; Thảm Du Lịch — xanh cốm chưa có ảnh; Vòng gai 16cm — đen chưa có ảnh; Đệm kê gối gắn tag Đen nhưng không có màu đen; ASANA 25 — ảnh biến thể "cafe" là file `asana25-mau-khoi`.

### 22/10 — Sửa tag màu sản phẩm trong Sapo admin (anh Công đăng nhập, Claude thao tác trên trình duyệt trong app)
Nguyên nhân: trang lọc màu do Sapo lọc theo TAG; tag màu không có biến thể tương ứng → sản phẩm lọt nhóm màu sai (vd F23 hiện ở nhóm Khói). Quy tắc rà: so 18 tag màu của bộ lọc với màu biến thể có giá (>0đ) của 30 sản phẩm.
Đã XOÁ (đều "Cập nhật sản phẩm thành công"):
| Sản phẩm (id) | Tag cũ | Đã bỏ |
|---|---|---|
| F23 5mm (39620233) | Xanh Rêu, Xanh Coban, Đen, Đỏ, Vàng, Xanh Cốm, Cam, Xanh Đậm, Tím Huế, Ghi Đậm | Đen, Đỏ, Vàng, Xanh Đậm, Tím Huế, Ghi Đậm |
| Đệm kê gối Yoga Pad (36960391) | Xanh Ngọc, Hồng, Đen, Ghi Khói, Tím Đậm, Hồng Nhạt | Xanh Ngọc, Đen, Tím Đậm |
| Túi đa năng M2261 (36960499) | Cam, Đỏ, Xanh Đậm, Xanh Lá, Đen | Đỏ |
| Vòng gai 16cm (36960421) | Đen, Cam, Xanh Coban, Xanh Rêu, Tím Huế, Xanh Ngọc, Vàng, Hồng | Xanh Rêu |
| Gạch G320 (36960317) | Tím Huế, Xanh Đậm, Đỏ | Xanh Đậm |
GIỮ, chờ anh Công quyết (màu gần đúng): AURA tag Cafe (màu thật "nâu") + Hồng Nhạt ("hồng phấn"); G220 + G320 + Vòng gai tag Tím Huế (màu thật "tím"/"tím đậm"); SUNFLOWER, Bóng trơn, Túi M2261 tag Xanh Lá (màu thật xanh rêu/xanh cốm); QUEEN Vàng ("vàng - mã màu q5"); Đệm kê gối Ghi Khói ("ghi"), Hồng ("hồng nhạt"); Khăn lau Hồng ("hồng phấn").
Còn lệch do THIẾU ẢNH biến thể (không phải tag): Vòng gai 16cm màu đen, Khăn lau màu hồng phấn, Thảm Du lịch màu xanh cốm, ASANA 25 ảnh biến thể "cafe" là ảnh khói.

### 22/10 — Sửa nút màu trong ngăn "Lọc & Sắp xếp" (bấm màu nào cũng ra Xanh Ngọc, PC + điện thoại)
- Nguyên nhân: `assets/lyx-shop.css` (bản 21/10 của phiên máy mới — trang danh mục kiểu Olaben, `templates/collection.olb.bwt`, `assets/lyx-shop.js`) đặt input màu `position:absolute; inset:0; width/height:100%` nhưng nhãn bị CSS cũ ép `position:static` → 18 input phủ kín cả khung màu, input cuối (Xanh Ngọc) nằm trên cùng nhận mọi cú bấm.
- Sửa: thêm `position:relative!important` cho `.lyxs-drawer .lyx-swatch-list .filter-item label` (1 dòng). Sao lưu `assets/zz-backup-lyx-shop-20261022-mau.css`.
- Đã kiểm bằng chuột thật: 1236px bấm Đen → chọn Đen, "Xem 7 sản phẩm"; 390px mỗi ô nhận đúng màu của nó.
- Lưu ý: trên theme còn file mới của phiên máy mới (`lyx-shop.css/.js`, `collection.olb.bwt`) — tài liệu của phiên đó chưa có ở thư mục này.

### 22/10 — Ảnh mới cho 7 phụ kiện (nguồn: `3. Tài nguyên hình ảnh/4. Avatar thảm final/4.Ảnh avatar phụ kiện JPG/`, 44 ảnh 1200×1200)
- Cách làm (trình duyệt trong app, anh Công đăng nhập admin): máy chủ tạm localhost phục vụ ảnh → chuyển dữ liệu sang trang admin bằng `window.name` (khung trình duyệt chặn fetch localhost & popup) → `POST /admin/products/{id}/images.json` body `{"image":{"base64":…,"filename":…,"variant_ids":[…]}}` (trường `attachment` báo "can't get info") → `PUT …/images/{img}.json {"image":{"position":n}}`.
- Ảnh mới đứng đầu (ảnh đầu = màu của biến thể đầu = ảnh đại diện), gắn vào phân loại màu; ẢNH CŨ GIỮ NGUYÊN phía sau (anh Công chọn — xoá sau khi duyệt). Tên trùng ảnh cũ → thêm hậu tố `-2026`. Đã kiểm: dung lượng ảnh trên Sapo = file gốc, mọi biến thể trỏ ảnh mới, web thật hiện đúng.
- Ghép màu: Bóng gai (36960400) xám→Ghi Đậm, xanh→Xanh Coban, tím→Tím Đậm; Bóng trơn (36960438) xanh→Xanh Coban, xanh lá→Xanh cốm, tím→Tím Đậm, ghi→Ghi Đậm; G220 (36960486) xanh→Xanh Coban, tím→Tím Đậm; G320 (36960317) xanh gray→XANH RÊU (tên biến thể giữ nguyên); Khăn lau (36960300) hồng đậm→ĐỎ, hồng→HỒNG PHẤN, hồng nhạt→Hồng nhạt(0đ), xanh lá→Xanh lá(0đ)+XANH CỐM, xanh→XANH COBAN, ghi (ảnh xanh navy)→GHI ĐẬM, tím→TÍM ĐẬM; Vòng gai (36960421) xanh gray→2 biến thể Xanh Ngọc, xanh→XANH COBAN, ảnh xanh lá chỉ tải lên (chưa có biến thể); Đệm kê gối (36960391) hồng→Hồng Nhạt.
- Còn chờ anh: xoá ảnh cũ; G320 biến thể tên "XANH RÊU" nhưng ảnh màu xanh ngọc/xanh gray (cân nhắc đổi tên + tag); Khăn lau ảnh "ghi" thực tế xanh navy; Vòng gai có ảnh xanh lá nhưng chưa có biến thể.

### 22/10 — Gộp "Phụ kiện yoga" + "Dụng cụ tập yoga" thành 1 (anh Công: trên điện thoại khó tìm xịt thảm, túi, khăn, bình)
- Dữ liệu Sapo (admin, phiên đăng nhập của anh Công): danh mục thủ công `/phu-kien-yoga` (id 3532398) đổi tên "Phụ Kiện Yoga" → **"Phụ Kiện & Dụng Cụ Yoga"** (đường dẫn, SEO giữ nguyên); THÊM 8 SP: G220 36960486, G320 36960317, Bóng trơn 36960438, Bóng gai 36960400, Vòng gai 36960421, Đệm kê gối 36960391, Ghế đa năng 84056302, Túi TPE 9mm 36960208 (collect id 98862050–98862057 — xoá các collect này để hoàn tác). Nay hiện đủ 15 SP không phải thảm. Danh mục `/dung-cu-tap-yoga` giữ nguyên, không xoá.
- `snippets/lyx-header.bwt`: menu PC "Sản phẩm" → nhóm "Phụ kiện & dụng cụ" (Tất cả + 9 lối tắt, 2 cột); menu điện thoại nhóm "Phụ kiện & dụng cụ" (Túi đựng thảm, Khăn lau mồ hôi, Xịt vệ sinh thảm, Bình giữ nhiệt, Gạch, Vòng, Bóng, Đệm kê gối, Ghế, Xem tất cả); chip Xu hướng "Phụ kiện & dụng cụ". Sao lưu `snippets/zz-backup-lyx-header-20261022-phukien.bwt`.
- Đã kiểm: lưới /phu-kien-yoga 15/15, mọi link menu 200, khung menu PC 300×578px, menu điện thoại 390px hiển thị đúng.
- 22/10 (lần 2, anh Công: khung menu PC dài, xấu): menu "Sản phẩm" PC đổi thành **mega menu ngang 3 cột** (Phân khúc thảm | Dòng thảm | Phụ kiện & dụng cụ chia 2 cột nhỏ + "Xem tất cả phụ kiện →"), "Tất cả sản phẩm →" nằm trên cùng. Khung 760×290px (trước 300×578px), lệch trái 150px so với nút để không tràn ở 1024px (đo: 192→952px). CSS nằm trong `<style>` của `lyx-header.bwt`. Sao lưu `snippets/zz-backup-lyx-header-20261022-mega.bwt`. Menu điện thoại không đổi.

### 22/10 — Ảnh nhỏ theo màu cạnh ô màu, trang SP (PC + tablet) — ĐÃ LÊN WEB
- Vấn đề (anh Công, ảnh LILIUM): PC ảnh chính là lưới 2 cột cố định → chọn màu không thấy ảnh màu đó. Anh vẽ demo: ô ảnh nhỏ bên trái hàng ô màu, bấm để xem to.
- `assets/lyx-pdp.js`: khối mới chèn trước mục "4. Bảng thông số" — nút `.lyxp-vimg` đặt đầu `.select-swatch` (thêm lớp `.lyxp-vwrap`); ảnh = `featured_image` của biến thể đọc từ `/<alias>.js` (biến `product` trên trang không dùng được), khớp theo `option1` = giá trị ô màu đang tick; đổi khi ô màu đổi (jQuery `change`, bắt cả `.trigger`). Bấm → `click()` vào ảnh cùng đường dẫn trong `#lightgallery` (mở lightGallery có sẵn, kể cả ảnh đang ẩn ở trang lưới khác); không tìm thấy thì mở ảnh ở tab mới. Biến thể không có ảnh / SP nhiều tuỳ chọn không khớp → ẩn ô.
- `assets/lyx-pdp.css` (cuối file): ô 132×132px, viền `--lyx-line`, bo 6px, hover viền `--lyx-cta`, `cursor:zoom-in`; chỉ ≥768px, điện thoại ẩn (lớp mobile ly-pdp.js không đổi).
- Sao lưu: `assets/zz-backup-lyx-pdp-20261022-anhmau.js`, `assets/zz-backup-lyx-pdp-20261022-anhmau.css` (bản 17/10, trước khi sửa).
- Đã kiểm trên web thật: LILIUM đổi 4 màu → ảnh đúng màu; bấm chuột thật → mở ảnh to đúng màu; 1440/1024/768 hiện ô, 390 ẩn, không tràn ngang; G220, BASIC có ảnh đúng; Bình giữ nhiệt (không ô màu) không có ô; combo AURA (biến thể không có ảnh) ô tự ẩn.
- 22/10 (lần 2, anh Công: trang combo thì ảnh đổi theo màu phải là thảm): biến thể combo không gắn ảnh → lấy ảnh cùng tên màu (so không phân biệt hoa/thường) của SP thảm cùng dòng. Dòng thảm đọc từ tên "Combo thảm yoga X, …" và bảng `COMBO_MAT` trong `lyx-pdp.js`: AURA → `tham-tap-yoga-cao-su-xo-dua-aura`, ASANA → `tham-tap-yoga-cao-su-asana`. **Thêm combo dòng thảm khác thì thêm 1 dòng vào bảng này.** Ảnh thảm không có trong bộ ảnh combo → bấm mở lightGallery tạm (dynamic), đóng thì gỡ. Sao lưu trước lần 2: `assets/zz-backup-lyx-pdp-20261022-combo.js`. Đã kiểm web thật: combo AURA, combo ASANA, LILIUM, G220 — đổi 4 màu đều đúng ảnh, bấm mở ảnh to được.

### 22/10 — Trang "Câu hỏi thường gặp" + khối FAQ cuối trang chủ — BẢN THỬ, CHỜ ANH CÔNG DUYỆT
- Tham khảo: olaben.com/vi/pages/faq (bố cục: cột hỏi–đáp gọn, nhóm in hoa, dấu +, ô tìm kiếm), dotapyogatot.com/cau-hoi-thuong-gap-faq (loại câu hỏi). Nét riêng Louis Yoga: số nhóm 01–06 đỏ rượu, chữ "FAQ" chìm nền kem, mục lục ghim bên trái (điện thoại: hàng chip ghim dưới header), vạch đỏ rượu khi mở câu, thẻ liên hệ đỏ rượu bo góc cuối trang; trang chủ: chữ "Q&A" lớn + 6 câu.
- File MỚI trên theme 1170160 (chưa gắn vào trang thật nào): `templates/page.faq.bwt`, `snippets/lyx-faq-items.bwt` (nội dung 21 câu, 6 nhóm — một nguồn cho cả trang và trang chủ; `lyx_faq_home = true` → 6 câu), `snippets/lyx-home-faq.bwt`, `assets/lyx-faq.css`, `assets/lyx-faq.js` (tìm kiếm không dấu + tô từ khoá, mục lục theo nhóm đang xem, mở câu theo #id, JSON-LD FAQPage), `templates/index.lyxtest.bwt` (bản thử trang chủ). Bản sao trong `faq-20261022/`.
- Tiền tố CSS là `.lyxq-` — KHÔNG dùng `.lyxf-` (footer `lyx-footer` đã dùng `lyxf-hero/grid/in…`, lần đầu đặt trùng làm chữ FAQ lọt xuống footer, đã sửa). Thẻ `<header>` bị CSS cũ ghim `position:fixed` → dùng `<div>`. Bộ lọc `money` của shop lỗi định dạng → số tiền miễn ship tự định dạng trong Liquid (`floor`).
- Xem thử: trang FAQ `https://louisyoga.vn/dieu-khoan-quy-dinh?view=faq`; trang chủ có khối FAQ `https://louisyoga.vn/?view=lyxtest`. Đã kiểm 1440/1024/768/390 không tràn ngang; 21 câu, tìm kiếm, ô trống, schema 21 câu.
- Nội dung chỉ lấy từ: chính sách bảo hành–đổi trả, kiểm hàng, CTV, đại lý, bài "So sánh các dòng thảm…", "Hướng dẫn sử dụng & bảo quản thảm", cài đặt giao diện (miễn ship 600.000đ, hotline, bảo hành, Zalo), trường "Xuất hóa đơn"/"Thời gian giao hàng" ở /cart.
- CHỜ ANH CÔNG: (1) duyệt giao diện + câu chữ; (2) xác nhận các câu chưa có nguồn chắc: hình thức thanh toán (đang viết chung "hiển thị ở bước Thanh toán"), "giao nhanh trong 24h" áp dụng khu vực nào, số gọi đổi trả (trang chính sách ghi CSKH 0352 587 836, footer ghi bảo hành 0973.168.389 — FAQ đang lấy số bảo hành từ cài đặt `store_phone1`), quyền lợi tài khoản/điểm tích lũy; (3) tạo trang trong admin: Website → Trang nội dung → "Câu hỏi thường gặp", đường dẫn `cau-hoi-thuong-gap`, giao diện `page.faq` (khối trang chủ trỏ tới đường dẫn này); nên thêm link vào menu/footer.
- Khi duyệt trang chủ: sao lưu `snippets/lyx-home.bwt` (zz-backup-lyx-home-20261022-faq.bwt), chèn `{%- include 'lyx-home-faq' -%}` ngay sau `{%- include 'lyx-news' -%}` (trước `</main>`), rồi xoá `templates/index.lyxtest.bwt`.
- 22/10 (anh Công duyệt giao diện) — ĐÃ GẮN KHỐI FAQ VÀO TRANG CHỦ THẬT: `snippets/lyx-home.bwt` thêm `{%- include 'lyx-home-faq' -%}` ngay sau `lyx-news` (mục 10). Sao lưu `snippets/zz-backup-lyx-home-20261022-faq.bwt` (đã đối chiếu khớp bản gốc). Đã kiểm web thật 1440/1024/768/390: 6 câu, mở được, không tràn ngang, footer không ảnh hưởng; UA điện thoại cũng có khối.
- Anh Công tự tạo trang `/cau-hoi-thuong-gap` (giao diện `page.faq`) — trước khi tạo, nút "Xem tất cả câu hỏi" ở trang chủ sẽ ra trang 404. Còn chờ anh xác nhận 4 câu (thanh toán, phạm vi giao 24h, số đổi trả, quyền lợi tài khoản).
- `templates/index.lyxtest.bwt` (bản thử) còn trên theme, chưa xoá — chờ anh cho phép (cùng 2 file thử cũ).
- 22/10 (anh Công đăng nhập admin, "triển khai luôn") — TRANG FAQ ĐÃ LÊN WEB:
  - Tạo trang qua admin (POST `/admin/pages.json`, phiên của anh): id **3473876**, "Câu hỏi thường gặp", alias `cau-hoi-thuong-gap`, giao diện `page.faq`, meta title "Câu hỏi thường gặp – Louis Yoga", meta description có sẵn; đã bật hiển thị (published_on). https://louisyoga.vn/cau-hoi-thuong-gap — 21 câu, index,follow.
  - Shop đã có trang CŨ `/faqs` (id 2545510, 2024, kiểu dotapyogatot): còn email hungyenthethao@gmail.com, địa chỉ "Số 2 A6 Ngõ 51", phí ship 30K, nhắc logo Bộ Công Thương → GIỮ NGUYÊN, chưa sửa/ẩn/chuyển hướng (chờ anh quyết).
  - Cập nhật 2 câu theo nguồn của shop: thanh toán (COD, chuyển khoản, trực tuyến — từ trang /faqs cũ) và "Tích điểm và hạng thành viên" (id `tich-diem-thanh-vien`, từ trang /chinh-sach-khach-hang-than-thiet: 100.000đ = 1 điểm, 1 điểm = 1.000đ, hạn 6 tháng, hạng Member/Silver/Gold/Diamond giảm 5–15%, sinh nhật 10–20%). Còn chờ anh: phạm vi "giao nhanh 24h", số gọi đổi trả (0352 587 836 hay 0973.168.389).
  - Link: `snippets/lyx-header.bwt` — thanh tiện ích PC thêm "Hỏi đáp" sau "Bảo hành" (aria-current khi template page.faq), menu điện thoại thêm "Câu hỏi thường gặp" sau "Liên hệ"; `snippets/lyx-footer.bwt` — cột "Về chúng tôi" thêm "Câu hỏi thường gặp". Menu chính PC không đổi (5 mục). Sao lưu `snippets/zz-backup-lyx-header-20261022-faq.bwt`, `snippets/zz-backup-lyx-footer-20261022-faq.bwt`.
  - Đã kiểm trang chủ, trang FAQ, trang SP LILIUM ở 1440/1024/768/390: không tràn ngang, thanh tiện ích không tràn ở 1024, link có ở menu điện thoại + footer.

### 22/10 — Nút Messenger nổi (anh Công) — ĐÃ LÊN WEB
- `snippets/support.bwt` (nút nổi góc phải, mọi trang trừ trang chủ — layout nhánh trang con `{% include 'support' %}`): thêm nút Messenger phía trên nút gọi, link `https://m.me/thamlouisyoga` (fanpage từ `settings.social_fb`, cùng logic lyx-header; m.me đã kiểm chuyển đúng trang id 107564394384565). Cùng kiểu tròn đỏ rượu của `assets/lyx-tab.css` (icon Messenger SVG nét hồng nhạt); `<style>` trong snippet cho khung `.addThis_listSharing` tự cao + cách 12px (lyx-tab.css đặt cao cố định 48px).
- Sao lưu: `snippets/zz-backup-support-20261022-mess.bwt`.
- Đã kiểm trang SP + FAQ ở 1440/1024/768/390: Messenger – Gọi – Zalo xếp dọc, không chồng nhau. Trang chủ không có cụm nút này (trang chủ có thanh Zalo dưới đáy trên điện thoại) — chưa thêm Messenger ở trang chủ.
- Trang FAQ cũ để anh xem: https://louisyoga.vn/faqs

### 22/10 (chiều) — Thống nhất 1 số điện thoại 0888.293.996 (mua hàng + bảo hành), bỏ 0973.168.389 / 0352 587 836 / 0386.988.979
- Cài đặt giao diện (`configs/settings_data.json`, ghi qua phiên admin trong trình duyệt — chỉ thay đúng chuỗi): `store_phone` "0888.293.996 - 0386.988.979" → "0888.293.996"; `store_phone1` "0973.168.389" → "0888.293.996". Sao lưu `assets/zz-backup-settings_data-20261022-sdt.json`.
- `snippets/lyx-footer.bwt` (bản mới nhất của phiên khác, 22/10 07:43) + `templates/page.contact.bwt`: khi store_phone1 trùng hotline → 1 dòng/ô "Hotline mua hàng & bảo hành", ẩn "Bảo hành - khiếu nại"/ô "Bảo hành". `snippets/ly-pd-policy.bwt`: "CSKH 0352 587 836" → "Hotline {số đầu của store_phone}". Sao lưu `*-20261022-sdt.bwt`.
- Trang nội dung (admin → Trang): Chính sách bảo mật (0973 → 0888), Chính sách bảo hành – đổi trả (2 × 0352 587 836 → 0888.293.996), Câu hỏi thường gặp (câu "shop còn sử dụng hotline 0386.988.979" → "shop không dùng số nào khác — 0888.293.996 là số duy nhất cho cả mua hàng và bảo hành."). Sao lưu nội dung cũ: `snippets/zz-backup-trang-<alias>-20261022-sdt.bwt`.
- Đã quét: 554 sản phẩm + 200 bài viết không có số cũ; 234 file theme chỉ còn số cũ trong comment / bộ lọc chặn 0386; web thật (curl, không cookie) 64 trang không còn số cũ.
- ⚠ Theme **1173918 "Bản tối ưu code"** (bản nháp do phiên khác tạo trước khi sửa) VẪN mang số cũ + cài đặt cũ → nếu xuất bản theme đó phải áp lại các sửa trên. Trình duyệt trong app có thể bị dính cookie xem trước 1173918 — kiểm web thật bằng curl.

## 22/10/2026 — TỐI ƯU, GIAI ĐOẠN 1 (sửa lỗi hiển thị theo thiết bị) — trên BẢN SAO theme 1173918, CHỜ ANH DUYỆT
Đề xuất đầy đủ: `DE-XUAT-TOI-UU-20261022.md`. Bản sao: **1173918** "Louis Yoga – Claude build (bản nháp) - Bản tối ưu code" (anh Công tạo 22/10, unpublished; lúc kiểm giống hệt 1170160 ở 14 file chính). Xem: mở `https://louisyoga.vn/?previewThemeId=1173918` (đặt cookie, các trang sau đều theo bản sao; chỉ với UA máy tính — UA điện thoại Sapo trả web thật → xem khổ điện thoại bằng iframe rộng 430 trong trang khổ PC).
- 8 file đã sửa trên 1173918 (bản sao lưu `zz-backup-<file>-20261022-opt.*` trên chính 1173918; bản đã ghi ở `toi-uu-gd1-20261022/`):
  1. `assets/lyx-card.css` — nút giỏ trên ảnh (điện thoại + "SP tương tự"): bỏ `aspect-ratio:1/1` trên hàng nút absolute → khung vuông `height:0;padding-top:100%`, nút `absolute; right:10px; bottom:10px`. Đo: mọi thẻ, khổ 375/414/430, trang chủ/danh mục/SP: nút cách góc ảnh 10px, kích thước như cũ (32px trang chủ, 40px nơi khác).
  2. `assets/ly-tweaks.css` — bỏ `.ly-card{container-type:inline-size}` + 2 khối `@container` (iOS 16+, lớp cũ không còn dùng).
  3. `assets/ly-pages.css` — `#ly-page-main{overflow-x:clip}` thêm `@supports not (overflow:clip){… overflow-x:hidden}` (iOS < 16 mất chốt chống tràn ngang).
  4. `assets/ly-cart.css` (`100dvh`), `assets/ly-pdp.css` (`84dvh`), `assets/lyx-shop.css` (`88dvh`), `assets/lyx-home.css` (`88svh`) — khai `vh` trước làm dự phòng; `ly-cart.css` thêm `-webkit-backdrop-filter`.
  5. `snippets/ly-favicon.bwt` (trong `<head>` mọi trang): (a) giả lập `<dialog>.showModal/close` cho iOS < 15.4 (thử bằng cách gỡ showModal: mở/Esc/close/sự kiện close đúng; máy mới bỏ qua); (b) trang SP: bật sẵn lớp `lyp-on` trên `<html>` khi ≤767px (ly-pdp.js gắn lên body sau tải → trước đây trang hiện kiểu PC rồi nhảy).
- Kết quả đo (bản sao): CLS trang SP điện thoại (không tính Zalo) **0,62 → 0,001** (390) / **0,59 → 0,009** (430); danh mục/trang chủ không đổi (0 / 0,027). Bộ đo vị trí 15 trang × 7 khổ: không tràn ngang; khác biệt còn lại = dời khối 28px do nội dung động + footer khác (xem dưới), vị trí tương đối trong thẻ giữ nguyên.
- Còn CLS do **khung chat Zalo tự bật** (`data-autopopup="2"`, cài đặt Live chat): 1,1–1,2 điện thoại, 0,2 PC — CHỜ ANH QUYẾT tắt tự bật.
- ⚠ Cài đặt giao diện của web thật đã đổi SAU khi tạo bản sao (footer web thật: "Hotline mua hàng & bảo hành"; bản sao còn "Bảo hành - khiếu nại 0973.168.389"). → KHÔNG xuất bản thẳng bản sao; đề xuất: duyệt xong thì chép 8 file sang 1170160 (sao lưu trước), giữ nguyên cài đặt web thật.
- Bộ đo (JS chạy trong tab riêng trang 404): `__fp(tag)` ghi `localStorage.fp_<tag>` vị trí ~25 loại khối; đo CLS cần tab đang hiển thị (tab ẩn không ghi layout-shift); iframe đo trang /lien-he từng điều hướng cả tab → chạy trong tab riêng.
- 22/10 (anh Công: "chọn phương án tốt nhất, không ảnh hưởng giao diện") — **Khung chat Zalo** trên bản sao 1173918: `snippets/livechat.bwt` (sao lưu `snippets/zz-backup-livechat-20261022-opt.bwt` trên 1173918). Mã Live chat trong cài đặt giữ nguyên, chỉ đổi cách nạp: điện thoại `data-autopopup="0"` (không tự bung che màn hình), PC giữ tự bật; điện thoại ẩn khung (visibility) tới khi SDK đã ở dạng nút 60px (vì SDK luôn dựng khung 675px rồi thu lại — đó mới là nguồn nhảy chính, autopopup=0 một mình không hết); Zalo SDK nạp sau `load` (trước là script chặn). Đã kiểm: điện thoại nút Zalo hiện lại sau ~1–4 giây dạng 60px, PC không đổi. **Chưa đo lại CLS** vì khung trình duyệt của app bị ẩn (tab ẩn không ghi layout-shift) — đo lại khi mở khung.
- 22/10 — **Đo lại CLS (khung trình duyệt mở, cùng điều kiện, bộ đệm đã nóng)**: bản sao — điện thoại mọi trang ≤ 0,028 (trang SP 0,001, danh mục 0, FAQ 0); PC danh mục 0,206 = khung Zalo tự bật (giữ theo lựa chọn). Web thật đo cùng lúc cũng ~0 trên điện thoại → khi JS/Zalo SDK đã nằm trong bộ đệm thì cả hai đều không nhảy; mức 1,1–1,8 đo buổi sáng là **lần tải đầu (bộ đệm lạnh)** — đúng tình huống khách mới / mạng yếu / máy chậm.
- **Phép đo không phụ thuộc bộ đệm** (mô phỏng mạng chậm: dựng trang bằng HTML đã bỏ các `<script src>`, giữ script nội tuyến, so với bố cục cuối; tổng px dịch chuyển của các khối trong màn hình đầu): trang SP 390 — web thật **1.235px** (ảnh, tên, giá, khối chính sách nhảy) → bản sao **48px** (chỉ khối chính sách, dưới màn hình đầu); 430 — 1.152 → 48. Danh mục 390: 0 cả hai. Hàm đo `__fv2(theme, path, width)` (tab trang 404).
- 22/10 — **GIAI ĐOẠN 1 ĐÃ LÊN WEB THẬT (anh Công duyệt)**: 9 file chép từ bản sao sang **1170160** (trước khi ghi đã đọc bản web thật — cả 9 file chưa ai sửa từ lúc tạo bản sao, nên ghi đè an toàn). Sao lưu trên 1170160: `assets/zz-backup-{ly-cart,ly-pages,ly-pdp,ly-tweaks,lyx-card,lyx-home,lyx-shop}-20261022-opt.css`, `snippets/zz-backup-{ly-favicon,livechat}-20261022-opt.bwt` (+ `zz-backup-livechat-20261022-opt2.bwt` trước lần chỉnh thời gian chờ). Đối chiếu: 7 CSS khớp CDN, 2 snippet khớp (chỉ lệch dòng trống cuối), HTML điện thoại có mã mới, không còn `<script src=…zalo…sdk.js>` chặn trang.
- Kiểm web thật: không tràn ngang (SP 390/1440, danh mục 430, trang chủ 390, FAQ 390); nút giỏ cách góc ảnh 10px; trang SP 390 có `lyp-on` trên html+body; Zalo điện thoại autopopup 0 → ẩn tới khi thành nút 60px rồi hiện, PC autopopup 2 như cũ. Chỉnh thêm: điều kiện hiện nút Zalo "đứng yên 3 giây" → 1,5 giây (môi trường đo hãm bộ đếm ~4 lần, đo được 9–10 giây là quá lâu); đã ghi cả 1170160 và 1173918.
- Lưu ý: đợt đổi số điện thoại (phiên khác, cùng ngày) sửa cài đặt + footer + trang Liên hệ + `ly-pd-policy.bwt` + 3 trang admin — các thay đổi đó KHÔNG có trên bản sao 1173918. Bản sao giờ chỉ dùng làm nơi thử; mọi sửa trên bản sao phải chép từng file sang 1170160, không xuất bản bản sao.

## 22/10/2026 — TỐI ƯU GIAI ĐOẠN 2, ĐỢT 1 (CSS theo loại trang) — trên BẢN SAO 1173918, CHỜ ANH DUYỆT
- Phương pháp chứng minh "giao diện không đổi": bộ so `toi-uu-gd2-dot1-20261022/bo-so-kieu-hien-thi.js` — trong iframe, tắt animation/transition, chụp ~49 thuộc tính computed style + ::before/::after + toạ độ của TỪNG phần tử (500–2.500 phần tử/trang), gỡ thẻ <link> CSS ngay trên trang, chụp lại, so. Đối chứng: gỡ lyx-col.css ở danh mục → 702 phần tử đổi (bộ so bắt được); không gỡ gì → 0. Nhiễu đã biết (bỏ qua): dòng chữ chạy `.lyx-tick`, margin `.lyx-util-row`, ảnh thanh toán `.lyx-pay` tải muộn, số đếm ngược `.is-tick`, Zalo, hiệu ứng reveal `lym-up`, số đếm trang Giới thiệu, băng chuyền SP.
- Ma trận 168 lần (15 file ứng viên × 13 loại trang × 390/1440): GIỮ (có khác biệt thật): ly-home.css, ly-design.css, ly-site.css ở trang con; lyx-col.css ở SP/FAQ/trang nội dung; lyx-home.css ở SP/danh mục/giỏ; 3 file nạp lại cuối trang ở SP + giỏ; ly-home/ly-design/lyx-editorial ở trang chủ.
- Đã sửa trên 1173918 (sao lưu `zz-backup-<file>-20261022-gd2.*` trên 1173918; bản ghi ở `toi-uu-gd2-dot1-20261022/`):
  1. `layouts/theme.bwt`: trang chủ bỏ `ly-tweaks.css`, `ly-pages.css`; trang con: `appcombo.css` + `lyx-pdp.css` (cả lượt nạp lại cuối) chỉ khi template chứa 'product'; `lyx-home.css` bỏ khi template = page / page.faq / page.about / blog* / article* / customers*; 3 file nạp lại cuối trang (ly-cart, lyx-pdp, lyx-editorial) chỉ trang SP + giỏ.
  2. `snippets/ly-favicon.bwt`: `lyx-pages.css` không nạp ở product/collection/search/cart.
  3. `snippets/header_style.bwt`: `style_page.scss.css` gộp 2 dòng (trang nội dung từng nạp 2 lần).
  4. `snippets/footer_script.bwt`: bỏ `jquery-ui-min.scss.css` ở danh mục (JS jquery-ui giữ).
- Kiểm cuối (trên web thật, gỡ đúng tổ hợp file của bản sửa, 13 loại trang × 390/1440): 0 khác biệt ngoài nhiễu. Các trang trên bản sao không lỗi Liquid.
- Kết quả CSS/trang (web thật → bản sao): danh mục 32 file/657KB → 25/492KB; FAQ 29/596 → 22/437; trang nội dung 29/592 → 22/433; giới thiệu 29/602 → 22/443; blog 28/583 → 22/437; tài khoản 28/606 → 22/460; tìm kiếm 31/614 → 25/478; giỏ 28/597 → 24/507; trang chủ 15/251 → 13/222; SP 33/666 → 32/640.
- Khi chép sang 1170160: layouts/theme.bwt, header_style, footer_script, ly-favicon — đọc bản web thật trước (ly-favicon trên web thật đã có bản GĐ1, giống bản sao), nếu khác bản gốc của bản sao thì ghép lại, không ghi đè.
- Ghi chú cho đợt sau: trang SP tải Google Sheets (danh sách cửa hàng, `tabletop.js` + Papa.parse) mỗi lần mở trang; swiper.js (94KB, nạp chặn ở <head>) chỉ trang SP dùng; jquery-ui + touch-punch (cdnjs) + search_filter.js nạp chặn ở danh mục; placeholdertypewriter.js nạp chặn mọi trang con.
- 22/10 — **GĐ2 ĐỢT 1 ĐÃ LÊN WEB THẬT (anh duyệt)**: 4 file (layouts/theme.bwt, header_style, footer_script, ly-favicon) — web thật trước khi ghi giống hệt bản gốc của bản sao → ghi đè an toàn. Sao lưu trên 1170160: `layouts/zz-backup-theme-20261022-gd2.bwt`, `snippets/zz-backup-{header_style,footer_script,ly-favicon}-20261022-gd2.bwt`. Kiểm: 13 trang × UA máy tính/iPhone đều 200, không lỗi Liquid, số CSS đúng (trang chủ 12, SP 31, danh mục/tìm kiếm 24, giỏ 23, liên hệ 22, còn lại 21); 6 trang × 390/1440 không tràn ngang.

## 22/10/2026 — TỐI ƯU GĐ2, ĐỢT 2 (JS) — trên BẢN SAO 1173918, CHỜ ANH DUYỆT
- Rà soát (trên trang thật): Swiper chỉ trang SP dùng (3 khung); main.js chỉ dùng Swiper trong hộp "xem nhanh"; ly-design.js có kiểm `window.Swiper`; nút `.quick-view` hiển thị = 0 ở danh mục/tìm kiếm/yêu thích/SP (SP có 7 nút trong khối cũ đã ẩn); `main.js` LUÔN gọi `$('.search-auto').placeholderTypewriter(...)` (không có .search-auto ở trang nào, nhưng thiếu plugin sẽ ném lỗi) → giữ plugin; hộp chọn cửa hàng (`product-hethong`, bật bằng `settings.product_store_enable`) không có nút `.btn-hethong` nào trên trang nhưng vẫn tải tabletop.js (PapaParse) + bảng Google Sheets mỗi lần xem SP.
- Đã sửa trên 1173918 (sao lưu `zz-backup-<file>-20261022-js.*` trên 1173918; bản ghi ở `toi-uu-gd2-dot2-20261022/`):
  1. `layouts/theme.bwt`: `swiper.js` (94KB, nạp chặn ở <head>) chỉ khi template chứa 'product'.
  2. `snippets/footer_script.bwt`: bỏ `quickview-template` + `quickview.js`; `placeholdertypewriter.js` đổi sang `defer`, đặt trước `main.js` (giữ thứ tự chạy).
  3. `snippets/product-hethong.bwt`: tabletop.js + Papa.parse(bảng Google) chỉ chạy khi bấm `.btn-hethong` lần đầu (`$(document).one`), nút cũ vẫn mở hộp như trước.
- Kiểm trên bản sao: SP — Swiper chạy (16 ảnh), đổi màu + ô ảnh nhỏ, mở giỏ trượt; danh mục (390) — không Swiper vẫn chạy, ngăn "Lọc & Sắp xếp" mở, ô màu thẻ đổi ảnh; hộp cửa hàng: gắn tạm nút .btn-hethong → bấm → PapaParse tải, hộp hiện, danh sách tỉnh nạp. Lỗi JS sau tải (bắt bằng listener) SP/danh mục/FAQ/tìm kiếm: giống hệt web thật (danh mục có 1 "Script error" của script ngoài — có sẵn ở web thật).
- Kết quả JS của theme (web thật → bản sao): FAQ 14 file/275KB (chặn 4/189KB) → 13/181KB (chặn 2/93KB); blog, giỏ tương tự; danh mục 21/380 (chặn 7/227) → 19/267 (chặn 5/131); SP 20/403 (chặn 6/262) → 18/367 (chặn 4/242) + không tải bảng Google Sheets.
- Khi chép sang 1170160: đọc bản web thật trước (theme.bwt + footer_script web thật hiện = bản GĐ2 đợt 1, giống bản sao trước đợt 2), sao lưu `-js`.
- 22/10 — **GĐ2 ĐỢT 2 (JS) ĐÃ LÊN WEB THẬT (anh duyệt)**: 3 file (layouts/theme.bwt, snippets/footer_script.bwt, snippets/product-hethong.bwt) — web thật trước khi ghi giống hệt bản gốc của bản sao → ghi đè an toàn. Sao lưu trên 1170160: `layouts/zz-backup-theme-20261022-js.bwt`, `snippets/zz-backup-{footer_script,product-hethong}-20261022-js.bwt`. Kiểm: 12 trang × UA máy tính/iPhone đều 200, không lỗi Liquid; swiper.js chỉ ở 2 trang SP thử; không còn quickview.js/tabletop.js. Chức năng (web thật): SP 1440 — galleryTop 16 ảnh, đổi màu, giỏ trượt mở (`<dialog open>`), PapaParse không tải, 0 lỗi JS; danh mục 390 — ngăn "Lọc & Sắp xếp" mở, ô màu thẻ đổi ảnh (1 "Script error" của script ngoài, có sẵn); FAQ 390 — mở câu được, 0 lỗi.

## 24/10/2026 — Ô "Danh mục phổ biến" trang chủ: "Vòng tập yoga" → "Combo" — ĐÃ LÊN WEB
- Yêu cầu anh Công: đổi ô thứ 5 thành Combo, icon tự tạo, bấm ra các SP combo.
- Shop CHƯA có danh mục combo (20 custom collection, 0 smart collection — đọc qua connector `custom_collections.json`); trang tìm kiếm `/search?type=product&q=combo` trả đúng 5 combo (BASIC, AURA, ASANA, QUEEN, F23) — chính là hình anh gửi → ô dẫn tới đây; combo mới đặt tên "Combo …" tự hiện.
- `snippets/lyx-home.bwt`: chuỗi `lyx_tiles` mục 5 `vong-tap-yoga~Vòng tập yoga~wheel` → `search?type=product&q=combo~Combo~combo`; thêm `{%- when 'combo' -%}` icon nét mảnh phối cảnh 3/4: hộp mở nắp + cuộn thảm dựng đứng + gạch (viewBox 64, cùng stroke CSS `.lyxh-tile-img svg`). Icon vòng (`else`) giữ trong mã. Sao lưu `snippets/zz-backup-lyx-home-20261024-combo.bwt` (web thật trước khi ghi = bản 22/10, không ai sửa thêm).
- Đã kiểm web thật: 5 ô đúng thứ tự, không lỗi Liquid, 390 không tràn ngang; bấm "Combo" → /search?type=product&q=combo, 5 thẻ combo.
- Gợi ý chưa làm: tạo danh mục "Combo" trong admin (có trang danh mục riêng, tiêu đề/mô tả SEO) rồi đổi link ô sang danh mục đó.

## 24/10/2026 — PHÂN KHÚC Harmony / Balance / Mastery CHUYỂN SANG TAG — ĐÃ LÊN WEB
- Vấn đề (anh Công): thêm tag "Harmony" cho combo nhưng bộ lọc không ra. Nguyên nhân: phân khúc lấy từ DÃY MÃ SẢN PHẨM viết cứng trong `snippets/ly-segments.bwt`; ô lọc "Phân khúc" khai `data-field="id"` → link `?q=tags:(...)` không có ô tích tương ứng nên bộ lọc (col.js) không chạy; 12 thảm chưa có tag phân khúc (chỉ 5 combo có).
- Dữ liệu (admin, phiên anh Công): thêm tag cho 12 thảm — Harmony: AURA 62337590, MOON 36960227, SUNFLOWER 60686622, ASANA 36960064; Balance: ASANA 25 60763661, BASIC 36960232, BASIC ZEN 62353814, QUEEN 36960230; Mastery: LILIUM 44128440, NATURE 37606937, DIAMOND 36960218, F23 39620233. Chỉ thêm, không mất tag cũ; biến thể/ảnh/mô tả không đổi (đã kiểm). Tag cũ lưu ở `tag-phan-khuc-20261024/tag-cu-truoc-khi-them-phan-khuc.json`.
- Theme (sao lưu `zz-backup-<file>-20261024-tag.*` trên 1170160; bản ghi ở `tag-phan-khuc-20261024/`): `ly-segments.bwt` (thêm `ly_seg_tags`; `ly_seg_values` = "(Harmony)"…, `ly_seg_urls` = `/collections/all?q=tags:((Harmony))…`; dãy mã giữ làm dự phòng + thứ tự), `ly-seg-of.bwt` (tag trước, mã sau, không phân biệt hoa thường), `aside-filter.bwt` (ô Phân khúc `data-field="tags"`, nhóm hiện khi danh mục có SP mang tag), `lyx-home.bwt` (tab trang chủ: SP theo mã trước, thiếu chỗ mới thêm SP có tag — hiện vẫn 4 thảm/tab như cũ), `tab_product.bwt` (SP tương tự: theo mã → SP cùng tag → danh mục), `assets/ly-segments.js` (nhận `tags:` khi đánh dấu menu). Header + trang tìm kiếm tự đổi link theo `ly_seg_urls`.
- Thử trên bản sao 1173918 trước rồi lên web thật. Kiểm web thật: bộ lọc Harmony 6 SP (4 thảm + combo AURA, ASANA), Balance 6 (+ combo BASIC, QUEEN), Mastery 5 (+ combo F23); tích ô "Mastery" trong ngăn lọc điện thoại → 5 SP; tab trang chủ 4/4/4 y như cũ; nhãn "Phân khúc" trang SP đúng (LILIUM Mastery, ASANA 25 Balance, combo BASIC Balance); không lỗi Liquid (máy tính + iPhone). Tiêu đề trang khi lọc vẫn "Tất cả sản phẩm" (web thật trước đây cũng vậy).
- CÁCH DÙNG (anh Công): thêm SP vào phân khúc = thêm tag đúng chữ `Harmony` / `Balance` / `Mastery` trong admin (Sản phẩm → Tag). Bỏ khỏi phân khúc = xoá tag (riêng 12 thảm gốc còn nằm trong dãy mã dự phòng — muốn bỏ hẳn phải sửa `ly_seg_ids`). "Dòng thảm" (Du lịch/TPE) vẫn theo mã sản phẩm như cũ.
