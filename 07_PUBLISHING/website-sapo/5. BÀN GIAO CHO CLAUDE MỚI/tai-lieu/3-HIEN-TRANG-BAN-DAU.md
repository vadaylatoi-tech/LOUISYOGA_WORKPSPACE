# HIỆN TRẠNG WEBSITE LOUISYOGA.VN — THEME NHÁP 1170160 (rà soát 17/10/2026)

> **⚠ CẬP NHẬT CUỐI NGÀY 17/10/2026:** toàn bộ các trang đã được đồng bộ editorial và anh Công đã duyệt. Phiên mới hãy đọc **`BAN-GIAO.md`** rồi **`TIEN-DO.md`** trước. Trong file này, bảng trạng thái §4, mục 1 "Kết luận" và §6 đã CŨ; §0 quy tắc, §2 kiến trúc, §3 token, §7 bẫy kỹ thuật vẫn dùng được. Ghi chú "preview cần đăng nhập admin" ở dưới là SAI — preview `?previewThemeId=1170160` xem được không cần đăng nhập.

> Tài liệu ngữ cảnh cho Claude Code trước khi bắt đầu **đồng bộ thiết kế** toàn site.
> Nguồn: đọc trực tiếp file theme qua Sapo Admin API (17/10/2026, ~14h30 giờ VN) + đọc HTML công khai của bản đang chạy.
> Nhãn độ tin cậy dùng trong file:
> - **[Đã kiểm]** = đọc tận mắt trong code/HTML ở lần rà này.
> - **[Ghi chú code]** = lấy từ comment trong file theme (do phiên trước viết), chưa kiểm lại bằng mắt.
> - **[Suy luận]** = em suy ra từ code, cần xác minh.
> - **[Chưa kiểm]** = chưa xem giao diện thật. **Lần rà này KHÔNG có ảnh chụp/xem trước bằng trình duyệt** (preview cần phiên đăng nhập admin; trình duyệt không được dùng). Mọi nhận xét về hiển thị đều là từ code.
>
> **⚠ Từ 17/10/2026 anh Công KHÔNG dùng "bộ kit" cũ nữa — làm trên phiên mới hoàn toàn.** File này là nguồn ngữ cảnh duy nhất. Mọi nhắc tới `backups/…`, `generated/…`, "bộ kit" trong comment của code theme là dấu vết của phiên cũ: **không còn truy cập được, không dựa vào**.

---

## 0. Quy tắc làm việc (đọc trước khi động vào code)

### Giao tiếp
- Trả lời **tiếng Việt**; xưng **em**, gọi người dùng **anh Công**. Trực tiếp, không nịnh, phản biện có căn cứ.
- Tách bạch **dữ kiện / suy luận / đề xuất**. Không bịa số liệu, tính năng, nội dung.
- Vấn đề phức tạp: **Kết luận → Phân tích → Đề xuất → Bước tiếp theo**.
- Giả định nhỏ, hoàn tác được → làm rồi nêu giả định. Thay đổi lớn/khó hoàn tác → hỏi trước.

### An toàn theme
| Theme ID | Tên | Vai trò (17/10) | Quy tắc |
|---|---|---|---|
| **1170160** | Louis Yoga – Claude build (bản nháp) | unpublished | **Nơi làm việc hiện tại.** Đây là bản thiết kế mới "lyx". |
| **1170134** | Louis Yoga (Bản mới - Edit chỉnh sửa) | **main (web thật)** | **Không ghi** nếu anh Công chưa đồng ý rõ cho từng việc (`allow_live_theme=true`). |
| 1170085 | Louis Yoga 26-12 (Đang sử dụng) | unpublished | Bản lưu cũ. Không sửa. |
| 1151386 | Louis Yoga (Không sửa ở đây) | unpublished | Bản cũ, không sửa. |
| 983840 | Louis Yoga 26-12 | unpublished | Theme gốc trước dự án. Dùng làm tham chiếu khôi phục. |
| 960680 / 878774 | Sudes Beauty / DefaultTheme | unpublished | Không liên quan. |

- **[Đã kiểm]** Web thật `https://louisyoga.vn/` đang phục vụ asset từ `/themes/1170134/` → bản thiết kế "lyx" **chưa lên web thật**.
- Luôn `list_themes` lại trước khi ghi: ID/vai trò có thể đã đổi.
- **Xuất bản theme phải làm trong Sapo admin**, không qua API (API chỉ đổi giao diện máy tính, điện thoại vẫn nhận theme cũ — sự cố 10/10). Sau xuất bản kiểm bằng user-agent điện thoại.
- Không tự đăng nhập bằng mật khẩu, không thao tác giỏ hàng/đơn thật, không xuất bản, không sửa sản phẩm/thương hiệu.
- Giữ nguyên logo, tên **Louis Yoga**, tên miền, nội dung sản phẩm. **Không** áp bộ nhận diện LOUGA lên site này.
- **Bảo toàn `templates/product.bwt`** (40 KB, chứa `selectCallback` + `Bizweb.OptionSelectors`, chọn biến thể, gallery Swiper). Không viết lại cả file.
- Trước khi sửa file: đọc bản hiện tại; sao lưu thành `snippets/zz-backup-<tên>-<ngày>.bwt` (hoặc ghi rõ nguồn hoàn tác); sửa nhỏ nhất có thể.
- **Nguồn hoàn tác (không còn kit):** chỉ còn những gì nằm trên Sapo — các file `snippets/zz-backup-*` trong 1170160, và theme **1170134** (web thật) giữ bản *trước khi* làm lớp lyx của nhiều file (layout, header, collection, ly-home-card, tab_product…) [Suy luận: 1170160 tách từ cùng gốc với 1170134 ngày 10/10, lớp lyx thêm 15–17/10 — đối chiếu nội dung trước khi chép về]. Vì vậy từ nay **mọi lần sửa lớn phải tự tạo zz-backup trên theme trước**.

### Kết nối của phiên mới
- Phiên cũ đọc/ghi theme qua connector `Sapo_Louis_Yoga` (công cụ `sapo_request`, `put_theme_asset`, `list_themes`, `list_theme_assets`). **Phiên Claude Code mới phải kiểm có công cụ này hay không trước tiên.** Không có → chỉ đọc được HTML công khai của web thật (theme 1170134), **không** đọc/ghi được 1170160; khi đó báo anh Công thay vì đoán nội dung file.
- Không có bản sao code theme trên máy: nguồn sự thật là file trên Sapo. Nếu tải về làm việc cục bộ, luôn đọc lại bản trên Sapo ngay trước khi ghi đè.

### Cách đọc/ghi theme (connector `Sapo_Louis_Yoga`)
- Đọc: `sapo_request` GET `themes/<id>/assets.json`, query `{"key":"<đường dẫn>"}` (ổn định hơn `get_theme_asset`).
- Ghi file văn bản: `put_theme_asset` — **gửi toàn bộ nội dung file** (ghi đè, không vá từng phần).
- Ghi ảnh nhỏ: `sapo_request` PUT `themes/<id>/assets.json` body `{"asset":{"key":"assets/x.png","base64":"..."}}`. Trường `attachment` tạo file 0 byte. Ảnh lớn (> ~50 KB) và **.svg** → nhờ anh Công tải qua admin (API coi .svg là nhị phân → file 0 byte; vì vậy logo SVG được nhúng vào snippet).
- API sản phẩm / danh mục / menu / blog / bài viết trả **403**. Dữ liệu sản phẩm công khai đọc qua `https://louisyoga.vn/<alias>.js`.
- `configs/settings_data.json` 204 KB — không ghi qua API; sửa cài đặt trong admin (Tùy chỉnh giao diện).
- Xem trước: `https://louisyoga.vn/<đường dẫn>?previewThemeId=1170160` — cần phiên đăng nhập admin; **user-agent điện thoại làm Sapo bỏ qua previewThemeId** (hiện theme live). Muốn xem khổ điện thoại: tải ở khổ máy tính rồi thu cửa sổ về 375–390px, không đổi UA.

---

## 1. Kết luận hiện trạng (tóm tắt)

1. **Theme 1170160 là một bản thiết kế lại lớn** (15–17/10/2026), phong cách **"Editorial sang trọng"**: nền trắng/kem, **đỏ rượu làm màu hành động**, hồng logo chỉ làm điểm nhấn, tiêu đề in hoa giãn chữ, nút viên thuốc viền mảnh. Mã mới dùng tiền tố **`.lyx*`** chồng lên lớp cũ **`.ly*`** (09–13/10) và lớp gốc của theme Sapo (Bootstrap 4 + scss cũ).
2. **Đã chuyển sang lyx:** header, footer, trang chủ (viết mới toàn bộ), trang danh mục, trang sản phẩm (phủ lên khung cũ), giỏ trượt, đầu trang Giới thiệu.
3. **Chưa đồng bộ:** trang giỏ hàng `/cart`, blog/bài viết, liên hệ, tìm kiếm, tài khoản, 404, trang chính sách — vẫn mang phong cách `ly-*` (hồng #d72182 / đỏ rượu #4a202c) hoặc kiểu theme gốc.
4. **Hệ màu đang song song 3 lớp** (gốc Sapo → ly-* → lyx-*) với nhiều `!important`; nút giỏ trượt dùng **đen**, trang chủ dùng **đỏ rượu**, trang danh mục điện thoại còn khối sale kiểu PDF cũ. Đây là việc chính của "đồng bộ thiết kế".
5. Nhiều nội dung đang **chờ tài nguyên/quyết định** (ảnh dẫn xuất, MP4 hero, gán sản phẩm cho video, ảnh Unsplash tạm, thông điệp chính sách 7 ngày trái với chính sách đã chốt 3/10 ngày).

---

## 2. Kiến trúc theme 1170160

### 2.1 Layout `layouts/theme.bwt` — hai nhánh  [Đã kiểm]
**Nhánh trang chủ** (`template contains 'index'`): HTML gọn, **không nạp CSS/JS cũ của theme gốc** (không footer_script, không bootstrap).
- Head: jQuery → script vá `Bizweb.formatMoney` (17/10, xem §7) → `content_for_header` → CSS: `ly-home.css`, `ly-design.css`, `ly-tweaks.css`, `ly-cart.css`, `ly-pages.css`, `lyx-base.css`, `lyx-home.css`, `lyx-editorial.css` → JS defer: `ly-cart.js`, `ly-home.js`, `ly-site.js`, `ly-design.js`.
- Body `class="ly-home-page lyx-page"`: `lyx-header` → `content_for_layout` (`templates/index.bwt` = `{% include 'lyx-home' %}`) → `lyx-footer` → `ly-cart-drawer` → dialog yêu thích `#ly-favorites`, dialog video `#ly-video`, toast `#ly-toast`.

**Nhánh các trang khác**: giữ khung theme gốc (jQuery, Swiper, lazy.js, `header_style`, `notify`, `appcombo.css`, `footer_script` nạp CSS/JS cũ cuối body…).
- Head CSS theo thứ tự: `appcombo.css`, `ly-home.css`, `ly-site.css`, `ly-design.css`, `ly-tweaks.css`, `ly-cart.css`, `ly-pages.css`, `lyx-base.css`, `lyx-home.css`, `lyx-col.css`, `lyx-pdp.css`, `lyx-editorial.css`.
- Body `class="ly-home-page ly-inner-page lyx-page ly-template-{{template}}"` (vd. `ly-template-product`, `ly-template-collection`).
- Cuối body **nạp lại** `ly-cart.css`, `lyx-pdp.css`, `lyx-editorial.css` để thắng CSS cũ nạp giữa trang (comment 17/10: đã giảm từ 10 file xuống 3, kiểm computed style không đổi ở 1440/390).
- Vẫn include: `footer_script`, `popup_sale` (theo setting), `support`, `popup-sapo`, `livechat`, `loyalty`, `ly-cart-drawer`.
- `louis-quiz` (Trợ lý chọn thảm) **đã bỏ** 17/10 theo anh Công; snippet còn trên theme.

### 2.2 Thứ tự ưu tiên CSS (quy tắc thực tế)
gốc Sapo (`main.scss`, `index.scss`, `product_style.scss`… nhiều `!important`, ép mọi `<button>` về Montserrat 14px/400) **<** `ly-*.css` (09–13/10) **<** `lyx-base/home/col/pdp.css` (15–16/10) **<** `lyx-editorial.css` (17/10, lớp phủ cuối cùng).
→ Sửa giao diện mới: ưu tiên **sửa/viết vào lyx-***; tránh thêm vào ly-* (đang là lớp sẽ bị thay). Nút mới phải khai `font` kèm `!important` nếu nằm ở trang không phải trang chủ.

### 2.3 Breakpoint
- Điện thoại **≤767px**, tablet **768–1023px**, PC **≥1024px**. Header chuyển sang bố cục điện thoại ở **≤1023px**. PC hẹp 1024–1240px có bậc thu nhỏ menu/ô tìm kiếm.

---

## 3. Hệ thiết kế đang áp dụng — "Editorial sang trọng" (`assets/lyx-base.css`)  [Đã kiểm]

```css
--lyx-wine:#4a1f2b;      /* thanh tiện ích trên cùng, nền khối kêu gọi */
--lyx-brand:#d82183;     /* hồng logo – chỉ điểm nhấn (badge, viền focus, gradient header) */
--lyx-cta:#5a2333;       /* MÀU HÀNH ĐỘNG CHÍNH (nút, giá trang SP, link hover) */
--lyx-cta-dark:#3f1824;
--lyx-ink:#141414;  --lyx-text:#2b2b2b;  --lyx-muted:#7a7470;
--lyx-line:#e7e2dc; --lyx-soft:#f4f1ed;  --lyx-cream:#f8f5f0;
--lyx-star:#c9973f; --lyx-mastery:#5c3317;
--lyx-w:1280px;  --lyx-font:Montserrat,Arial,sans-serif;
--lyx-head-h:80px (≤1023: 60px);  --lyx-sec-y:clamp(52px,6.5vw,96px);
--lyx-ease:cubic-bezier(.2,.7,.2,1);
```
- Font: **Montserrat** (Google Fonts biến thiên qua `snippets/ly-fonts.bwt`, include trong `ly-favicon.bwt`). Inter có file woff2 trên theme nhưng lớp lyx chỉ dùng Montserrat [Suy luận từ token].
- Kiểu chữ: eyebrow 11px/600, giãn .3em, in hoa, màu `--lyx-cta`; H2 `clamp(24px,2.7vw,38px)`/500, in hoa, giãn .06em.
- Nút `.lyx-btn`: cao 46px (mobile 44), bo 999px, chữ 11.5px/600 giãn .2em in hoa. Biến thể: `-out` (viền), `-wine`/`-cta` (đỏ rượu), `-light`, `-ghost-light`. Link `.lyx-link`: gạch chân + mũi tên.
- Khung: `.lyx-wrap` max 1280px, lề `clamp(16px,3vw,40px)`; khối `.lyx-sec` padding dọc `--lyx-sec-y`.
- Biến riêng khác tồn tại song song: `--lyxp-*` trong `lyx-pdp.css` (vd. `--lyxp-cta`, chưa đọc chi tiết), `--lyxc-*` trong `lyx-cart.css` (`--lyxc-ink:#111`, `--lyxc-gold:#d9a030`), fallback `var(--lyx-cta,#be3a63)` (màu nút "MUA NGAY" đo từ PDF 15/10 — **khác** giá trị token hiện tại #5a2333).

### 3.1 Hệ cũ còn sống (`ly-*`, 09–13/10) — cần thay dần
Hồng `#d72182`, đỏ rượu `#4a202c`, giá mới xanh `#00869e`, nền xám `#f2f2f2`, sale `#fed8e3`, footer `#171516`, sao `#d69d31`… (theo STATIC_CONTEXT). Còn hiện ở `/cart`, trang phụ (`ly-pages.css`), khối mô tả SP (`ly-pd-info.css`), bộ lọc (`ly-tweaks.css`), chip phân khúc trang SP (CSS nội tuyến `#d72182`).

### 3.2 Tham chiếu thiết kế được nhắc trong code [Ghi chú code]
- "Bản thiết kế PC/mobile 15/10/2026" (PDF, nhiều trang: mobile trang 1 = trang chủ, trang 5 = giới thiệu, trang 10–11 = giỏ trượt). Claude Code cần **mở lại file thiết kế gốc** khi so pixel — file này không thay thế bản vẽ.
- Comment code nhắc tới bộ "kit" (`backups/pre-home-*`, `generated/`) — **đã ngừng dùng từ 17/10**. Hệ quả: 3 ảnh dẫn xuất chuẩn bị trong `generated/` (`lyx-cat-mats.jpg` 640×328, `lyx-story.jpg` 640×488, `lyx-about.jpg` 600×868) **không còn** → phải làm lại hoặc anh Công cung cấp ảnh mới, tải lên Assets rồi bật cờ trong `lyx-flags.bwt`. Bản PDF thiết kế 15/10: hỏi anh Công gửi lại nếu cần so pixel.
- Tham chiếu phong cách: "olaben" (thẻ bộ sưu tập, chữ hero căn giữa).

---

## 4. Trạng thái từng khu vực

| Khu vực | File chính | Mức đồng bộ editorial | Ghi chú |
|---|---|---|---|
| Header | `snippets/lyx-header.bwt` + `lyx-base.css` | ✅ Xong | Xem §4.1 |
| Footer | `snippets/lyx-footer.bwt` + `lyx-base.css` + `lyx-editorial.css` | ✅ Xong | Nền kem, cột in hoa |
| Trang chủ | `snippets/lyx-home.bwt`, `lyx-home.css`, `lyx-home.js`, `lyx-flags.bwt` | ✅ Xong (chờ tài nguyên) | Xem §4.2 |
| Danh mục | `templates/collection.bwt`, `lyx-col.css/js`, `lyx-editorial.css`, `aside-filter.bwt`, `ly-filter.js`, `col.js` | 🟡 Phần lớn | Điện thoại `/collections/all` còn chèn `lyx-sale.bwt` (kiểu PDF 15/10, nút đen, "!!") |
| Trang SP (PC) | `templates/product.bwt` (gốc) + `tab_product.bwt` + `lyx-pdp.css/js` + `lyx-editorial.css` | 🟡 Phủ lên khung cũ | Chip phân khúc còn hồng #d72182; khối mô tả từ `ly-pd-info.css` |
| Trang SP (mobile) | `ly-pdp-mobile.bwt`, `ly-pdp.css/js` (kiểu Shopee) + phủ editorial | 🟡 | Đã đổi hồng → đỏ rượu bằng lớp phủ |
| Giỏ trượt | `ly-cart-drawer.bwt`, `lyx-cart.css/js`, `ly-cart.js` | 🟠 Theo PDF 15/10, **không** theo editorial | Nút thanh toán **đen #000**, thanh freeship **vàng** |
| Trang `/cart` | `templates/cart.bwt` + `ly-cart.css` | ❌ Chưa | Comment lyx-cart.css: "trang /cart giữ nguyên" |
| Giới thiệu | `page.about.bwt` → `lyx-about.bwt` + `ly-about.bwt`, `lyx-about.css`, `ly-about.css` | 🟡 | Đầu trang mới; các khối dưới là ly-about được phủ màu |
| Blog / bài viết / báo chí | `blog.bwt`, `blog.baochi.bwt`, `article.bwt`, `ly-pages.css` | ❌ Chưa | Logic link báo chí ngoài (12/10) cần giữ |
| Liên hệ, tìm kiếm, tài khoản, 404, chính sách, hệ thống cửa hàng, guide | templates tương ứng + `ly-pages.css` | ❌ Chưa | |

### 4.1 Header  [Đã kiểm]
- Thanh tiện ích đỏ rượu 36px: **4 thông điệp viết cứng** chạy luân phiên 4,2s — "Luôn có 7 ngày đổi trả miễn phí", "Nhận điểm tích lũy cho mỗi lần mua", "Giao nhanh trong 24h", "Chính sách 1 đổi 1 nếu không hài lòng" (bản live lấy từ `settings.policy_title_1..4`). Bên phải: Hotline (số đầu của `settings.store_phone`), Đăng ký CTV, Bảo hành, Nhận ưu đãi (#lyx-news), Zalo/FB/YT.
- Thanh chính: PC = logo trái (146px) · menu giữa (Trang chủ · Sản phẩm ▾ · Blog ▾ · Về chúng tôi · Liên hệ) · tìm kiếm + yêu thích + giỏ + tài khoản. Điện thoại = burger + tìm kiếm | logo giữa | yêu thích + giỏ.
- Ghim: sentinel + IntersectionObserver → `.is-stuck` thu thành viên thuốc kính mờ (PC 64px, mobile 52px).
- Bảng "Sản phẩm": Tất cả · Phân khúc (Harmony/Balance/Mastery kèm tên mẫu) · Dòng thảm (Du lịch, TPE) · Phụ kiện (`/phu-kien-yoga`). Bảng "Blog": `/tin-tuc`, `/bao-chi-noi-ve-louis-yoga`, `/suc-khoe-moi-ngay`, `/truyen-thong-louis-yoga`.
- Menu điện thoại (ngăn kéo `#lyx-menu`, bẫy focus, Esc): ô tìm kiếm, chip "Xu hướng", nhóm Thảm yoga / Phụ kiện yoga (vòng, ghế, đệm kê gối, gạch, bóng) / Tài khoản.
- Móc JS dùng chung **phải giữ**: `data-cart-open`, `data-cart-count`, `data-favorites-open`, `data-favorite-count`, `window.LYXDrawer`.
- Logo: `snippets/lyx-logo.bwt` (SVG nhúng). Bỏ icon hoa sen theo góp ý 16/10.

### 4.2 Trang chủ (`snippets/lyx-home.bwt`, 32 KB)  [Đã kiểm]
Thứ tự khối:
1. **Hero video** toàn khung: ảnh nền `ly-hero-pc.jpg`; video ưu tiên MP4 (`lyx_hero_mp4_pc/_mb`, đang **trống**) → tạm dùng YouTube `ZoOMtbkA-8A` tắt tiếng. Chữ: eyebrow "Louis Yoga", H1 "Vững vàng / trong từng chuyển động", nút "Khám phá ngay" (#lyxh-mats) + "Xem câu chuyện" (mở modal video). PC: chữ căn giữa, hiện dần khi video chạy. Điện thoại: khung 5:4, cắt hai mép ảnh ngang.
2. **Danh mục sản phẩm**: 2 thẻ bộ sưu tập (Thảm yoga cao su → `/tham-yoga-cao-su`; Phụ kiện → `/phu-kien-yoga`) dùng **ảnh Unsplash** (`lyx_cat_img_1/2`) + "Danh mục phổ biến" 5 ô icon nét mảnh (cao su, TPE, du lịch, gạch, vòng → `/tham-yoga-cao-su`, `/tham-tpe`, `/tham-yoga-du-lich`, `/gach-tap-yoga`, `/vong-tap-yoga`).
3. **Săn sale**: "Săn sale mùa thu đông", "Giảm tới X%" (X = % giảm lớn nhất tính từ giá thật trong danh mục `settings.section_deal_product`, mặc định `san-pham-khuyen-mai`), đồng hồ đếm ngược: có `settings.ly_home_sale_end` thì đếm tới đó, không thì `lyx_sale_cd='month'` → **đếm tới 23:59 cuối tháng hiện tại** (anh Công chọn 16/10). Hàng thẻ cuộn ngang 12 SP.
4. **Yoga mat Louisyoga**: 3 tab Harmony/Balance/Mastery (+ "Người mới / thường xuyên / chuyên nghiệp"), banner `ly-seg-{h}.jpg` 1600×400, 4 thẻ/tab lấy theo `ly_seg_ids`.
5. **Phụ kiện**: hàng cuộn 16 SP từ `settings.url_1_all2pro` (mặc định `phu-kien-yoga`).
6. **Video**: 7 video YouTube từ `lyx_vid_list` (lyx-flags), mỗi video kèm ô sản phẩm (BASIC/ASANA) hoặc ô "Khám phá thảm" khi chưa gán.
7. **Tìm màu sắc của bạn**: 6 ô màu (`lyx_colors`) → `/collections/all?q=tags:(...)`.
8. **Câu chuyện**: "Sự chân thành", ảnh `img_video_6.jpg` (chờ `lyx-story.jpg`).
9. **Louis News**: video Hoa hậu (ảnh `img_bantab1.jpg`, trích dẫn) + 3 bài báo từ blog `settings.section_baochi_blog` (link thẳng ra báo nếu Tóm tắt là URL; có dòng thay link Thương hiệu & Cuộc sống .vn → .info).
- Thanh nổi đáy điện thoại `.lyx-sticky`: Zalo | "Thảm tập yoga" (→ `/tham-tap-yoga`). Đẩy nút Zalo/gọi nổi lên 72px.
- Tối ưu 17/10: quét `collections['all']` (≤250 SP) **một lượt** để dựng thẻ phân khúc & ô SP video (trước đó TTFB 0,7–1,4s) [Ghi chú code].
- Trang chủ cũ (`ly-home-main.bwt`, `ly-home-mid.bwt`, `ly-home-yogi.bwt`, `ly-home-header/footer.bwt`) **vẫn còn trên theme** nhưng không được gọi.

### 4.3 Thẻ sản phẩm dùng chung `snippets/ly-home-card.bwt` (lớp `.lyx-card`)  [Đã kiểm]
- Dùng ở: trang chủ, danh mục (`products-grid-item`), SP tương tự, gợi ý giỏ.
- Ảnh `large` 480px, nhãn "Sale X%" / "Hết hàng", tim yêu thích, tên, **sao gộp web (`product.metafields.bpr`) + Shopee (`ly-shopee-reviews-data`) theo trọng số lượt**, giá (cũ gạch + mới, đơn vị "đ"), 2 nút "Thêm vào giỏ" / "Mua ngay".
- Logic giữ từ 10/10: ẩn biến thể 0đ khi có biến thể có giá; gộp phân loại trùng tên (khác hoa/thường, 2 dấu cách); mọi biến thể 0đ → "Xem chi tiết" + "Liên hệ" (tel:).
- Móc JS: `.ly-card`, `data-add`, `data-buy`, `data-pick`, `.ly-variant-list`, `data-wish` (ly-design.js / ly-site.js).
- Bẫy Liquid Sapo: số "4,8"/"4.8" bị đọc thành 48 → điểm sao tính bằng số nguyên ×100 rồi chia (đừng "đơn giản hoá").

### 4.4 Danh mục (`templates/collection.bwt`)  [Đã kiểm]
- Breadcrumb (có — khác quyết định cũ "không breadcrumb"; đây là theo bản thiết kế 15/10) → khối đầu trang kem: eyebrow, H1, mô tả danh mục (hoặc đoạn mặc định) → (chỉ `/collections/all`, điện thoại) khối `lyx-sale` → "Cửa hàng / Toàn bộ sản phẩm" (điện thoại) → thanh Bộ lọc/Sắp xếp (điện thoại) + sidebar lọc `#lyxc-side` + lưới → 2 thẻ CTA (CTV, Bảo hành "Lỗi 1 đổi 1") → đoạn outro.
- **Giữ khung cho col.js + ly-filter.js**: `.dqdt-sidebar`, `.opacity_sidebar`, `#open-filters`, `.category-products`, `collection-sortby`, `products-grid-item`, biến `colName/colId/selectedViewData`.
- Bộ lọc (aside-filter, live đọc được): Phân khúc → Dòng thảm → Loại SP → Chọn mức giá (0–6.000.000đ) → Đánh giá → Màu phổ biến (lyx-col.js thêm ô màu) → Độ dày.
- Link phân khúc = `/collections/all?q=id:((...))` → class chờ `html.ly-qwait` tránh nháy.

### 4.5 Trang sản phẩm  [Đã kiểm code, chưa xem hình]
- Khung `templates/product.bwt` (gốc, đừng viết lại) → `snippets/tab_product.bwt`: chip "Phân khúc X" (CSS hồng nội tuyến) · lớp mobile `ly-pdp-mobile` · khối Chi tiết / Bảo quản (chỉ thảm) / Vận chuyển & đổi trả (`ly-pd-policy.bwt`, viết tay) · Đánh giá (Shopee `ly-shopee-reviews.bwt` + app Sapo nếu bật) · SP tương tự (ưu tiên cùng phân khúc, 5 thẻ) · `ly-promos`.
- `lyx-pdp.js` (PC): nhãn "Chính hãng" + chip phân khúc, dòng sao gộp, tim + chia sẻ cạnh giá, bảng thông số "Nhãn: giá trị" 2 cột, dòng miễn ship, **ảnh lưới 2×2 có chấm phân trang**, khối đánh giá gộp với 2 tab "Đánh giá (n)" / "Đánh giá shopee (n)".
- Tự đóng `<style>` hở trong mô tả (lỗi NATURE) — giữ.
- App "Đánh giá sản phẩm" Sapo **đã hết hạn** (13/10); khối Shopee là nguồn chính. Không đưa điểm Shopee vào schema `aggregateRating`.

### 4.6 Giỏ trượt / trang giỏ  [Đã kiểm]
- Giỏ trượt `#ly-cart.lyx-cart`: tiêu đề in hoa, thanh freeship vàng, dòng SP viền mảnh, "Sản phẩm thường được mua cùng" (3 cột, từ danh mục phụ kiện), nút **THANH TOÁN nền đen** + "Xem giỏ hàng". Hành vi (số lượng, xoá, hoàn tác, freeship) do `ly-cart.js`.
- Trang `/cart`: bố cục 2 cột 09/10 (ly-*), thuộc tính đơn giữ đúng tên ("Xuất hóa đơn", "Tên công ty", "Mã số thuế", "Địa chỉ công ty", "Email nhận hóa đơn", "Thời gian giao hàng"). **Chưa** áp editorial.

### 4.7 Giới thiệu  [Đã kiểm]
- `lyx-about.bwt`: hero (ảnh `lyx-about.jpg` nếu cờ bật, chưa có → nền gradient + chữ "LOUISYOGA Tập CHUẨN ĐỀU Nhịp"), "Sự chân thành", "Về Louis Yoga" + video `settings.id_video`. Sau đó `ly-about.bwt` (giá trị cốt lõi, văn hoá, giải thưởng, kêu gọi) được `lyx-editorial.css` phủ màu.

---

## 5. Nguồn dữ liệu & cấu hình trong code

| Nội dung | Nơi cấu hình | Ghi chú |
|---|---|---|
| Phân khúc Harmony/Balance/Mastery + Dòng thảm Du lịch/TPE | `snippets/ly-segments.bwt` (**nguồn duy nhất**) | Gán theo product.id. Harmony: AURA 62337590, MOON 36960227, SUNFLOWER 60686622, ASANA 36960064 · Balance: ASANA 25 60763661, BASIC 36960232, BASIC ZEN 62353814, QUEEN 36960230 · Mastery: LILIUM 44128440, NATURE 37606937, DIAMOND 36960218, F23 39620233 · Du lịch 36960223, OCEAN 50892151 · TPE9 36960236. Chưa gán: SUN, MINI. |
| Cờ trang chủ, video, màu, ảnh | `snippets/lyx-flags.bwt` | `lyx_has_cat_mats/story/about=false`, `lyx_hero_mp4_pc/mb=''`, `lyx_hero_yt='ZoOMtbkA-8A'`, `lyx_sale_cd='month'`, `lyx_vid_list` (7 video), `lyx_colors` (6 màu), `lyx_cat_img_1/2` (Unsplash) |
| Đánh giá Shopee | `snippets/ly-shopee-reviews-data.bwt` + `assets/lysr-1..4.js` | 203 đánh giá / 18 SP, lọc từ 2 shop chính hãng. Chỉ dùng đánh giá thật. |
| Chính sách đổi trả (tóm tắt) | `snippets/ly-pd-policy.bwt` | Đã chốt: 3 ngày đổi theo nhu cầu (khách chịu ship 2 chiều), 10 ngày đổi do lỗi (Louis Yoga chịu ship). Sửa tay khi chính sách đổi. |
| Cài đặt theme dùng nhiều | settings_data | `section_deal_product`, `url_1_all2pro`, `ly_home_sale_end/start`, `store_phone` ("0888.293.996 - 0386.988.979"), `store_phone1` (bảo hành 0973.168.389), `store_email`, `store_address`, `social_fb/zl/you/insta`, `free_shipping_enable/price` (600.000đ), `section_baochi_blog`, `id_video`, `content_about`, `policy_title_1..4`, `use_cart_vat`, `delivery_time` |
| Link Facebook đúng | code tự thay | Nếu `social_fb` chứa "thamtapyogalouis"/"sapoweb" → `https://www.facebook.com/thamlouisyoga` |

Danh mục đã xác nhận tồn tại trên web (live, 17/10) [Đã kiểm]: `/phu-kien-yoga` (7 SP), `/tham-yoga-cao-su` (2 trang), `/tham-tap-yoga` (2 trang), `/san-pham-khuyen-mai` (6 SP: LILIUM, NATURE, DIAMOND, QUEEN, F23, ASANA 25). **Chưa kiểm**: `/tham-tpe`, `/tham-yoga-du-lich`, `/gach-tap-yoga`, `/vong-tap-yoga`, `/ghe-tap-yoga`, `/bong-tap-yoga`, `/suc-khoe-moi-ngay`. Lưu ý: bản live trỏ "Phụ kiện" về `/collections/dung-cu-tap-yoga`, bản nháp trỏ `/phu-kien-yoga` (hai danh mục khác nhau, nên thống nhất).

---

## 6. Vấn đề tồn đọng & rủi ro (ưu tiên giảm dần)

### Ảnh hưởng nội dung / pháp lý
1. **Thông điệp chính sách sai**: header viết cứng "Luôn có 7 ngày đổi trả miễn phí" và "Chính sách 1 đổi 1 nếu không hài lòng"; danh mục/giỏ ghi "Lỗi 1 đổi 1". Chính sách đã chốt là **3 ngày (theo nhu cầu, khách chịu ship) / 10 ngày (lỗi)**. [Đã kiểm code] → cần anh Công duyệt câu chữ thay thế; `policy_title_2` và trang `/chinh-sach-kiem-hang` cũng còn "7 ngày" (sửa trong admin).
2. **Ảnh Unsplash** ở 2 thẻ danh mục trang chủ: ảnh tồn kho, không phải sản phẩm Louis Yoga → nên thay bằng ảnh thật (`lyx-cat-mats.jpg` 640×328 hoặc lớn hơn, ngang ~16:10).
3. **Đếm ngược "tới cuối tháng"** không gắn với chiến dịch thật → có thể bị xem là tạo khan hiếm giả. Nên đặt ngày thật ở `ly_home_sale_end` hoặc ẩn (`lyx_sale_cd=''`). Cần anh Công quyết.
4. "Săn sale **mùa thu đông**" là chữ cứng trong 2 file (`lyx-home.bwt`, `lyx-sale.bwt`); "Thời gian và số lượng có hạn.!!" (dấu câu lỗi) trong `lyx-sale.bwt`.
5. Hotline: header/sticky dùng 0888.293.996; chính sách đổi trả ghi CSKH 0352 587 836 — chưa chốt số nào cho CSKH.

### Thiết kế chưa đồng bộ
6. Ba hệ màu song song; CTA giỏ trượt đen vs đỏ rượu; fallback `#be3a63` trong lyx-cart; chip phân khúc trang SP hồng #d72182; bảng màu swatch bộ lọc (`lyx-col.js`, `COLORS`) khác bảng `lyx_colors` trang chủ.
7. `/cart`, blog, bài viết, liên hệ, tìm kiếm, tài khoản, 404, chính sách: chưa editorial.
8. Khối `lyx-sale` trên danh mục điện thoại khác hẳn khối sale trang chủ (nút đen, bố cục PDF cũ).

### Kỹ thuật
9. Nợ CSS: nhiều tầng + `!important` dày đặc; file cũ không còn dùng vẫn nạp (`ly-home.css`, `ly-design.css` trên trang chủ có selector `.ly-sale/.ly-mats` thừa) [Suy luận về mức thừa, chưa đo].
10. File rác/lưu: `assets/ly-logo.svg` 0 byte, nhiều `snippets/zz-backup-*`, `ly-filter-v1.js`, `zz-backup-ly-site.js`, snippet trang chủ cũ, `louis-quiz.bwt`. Không xoá khi chưa được anh Công đồng ý.
11. Vòng lặp `collections['all'] limit:250` ở trang chủ và SP tương tự (`tab_product.bwt` vẫn lặp 250 × số ID) → chi phí render; trang SP chưa được tối ưu như trang chủ.
12. Hero YouTube: rủi ro phụ đề CC trên iPhone, chặn tự phát chế độ nguồn thấp (đã gặp trên bản live 11/10). Hướng triệt để: MP4 tự host (`lyx_hero_mp4_*`).
13. Shopee reviews: dữ liệu tĩnh tại 13/10 — không tự cập nhật.

### Dữ liệu cần sửa trong admin (ngoài theme, API 403)
NATURE (biến thể trùng, biến thể 0đ, `<style>` hở trong mô tả), LILIUM ("Ghi khói" 0đ còn tồn), `policy_title_2`, "FACIFIC" → "PACIFIC", `social_fb`, ghép "Vòng gai 16cm" ↔ Shopee "VÒNG GAI 1.6kg" (chờ xác nhận).

---

## 7. Bẫy kỹ thuật đã biết

- **formatMoney (17/10)**: định dạng tiền của shop là "$" thiếu `{{amount}}` → `Bizweb.formatMoney()` ném lỗi "reading '1'" (giỏ, app). Layout có script bọc `Bizweb.formatMoney` luôn dùng `{{amount_no_decimals_with_comma_separator}}₫`. **Giữ script này ở cả 2 nhánh**, đặt trước `content_for_header`.
- Theme cũ ép `<button>` về Montserrat 14px/400 bằng `!important` (trang không phải trang chủ).
- Animation bị dừng khi tab ẩn → hiệu ứng vào cảnh phải bỏ qua khi `document.visibilityState==='hidden'` + hẹn giờ tự gỡ class.
- Mọi hiệu ứng có nhánh `prefers-reduced-motion:reduce`.
- Kiểm nhanh trang SP còn sống: `typeof galleryThumbs === 'object'`; ô màu đổi `.single-option-selector` theo `value` radio.
- `data-number` của app đánh giá = số sao tối đa (5), không phải số lượt.
- `.json` trong assets không được CDN Sapo phục vụ → dữ liệu tĩnh để dạng `.js` (`window.LYSR`).
- Bộ lọc Sapo nối các nhóm bằng AND: chọn đồng thời 1 phân khúc + 1 dòng thảm (cùng trường `id`) có thể ra 0 kết quả.
- Mô tả sản phẩm có HTML dán tay → nguồn lỗi; khi trang SP "hỏng lạ", kiểm `product.content` trước.
- `put_theme_asset` ghi đè toàn file — đọc bản mới nhất ngay trước khi ghi để không đè thay đổi của phiên khác.

---

## 8. Đề xuất lộ trình đồng bộ (ĐỀ XUẤT — chưa được anh Công duyệt)

1. **Chốt token một nguồn**: giữ `lyx-base.css :root` làm chuẩn; quy đổi `--lyxp-*`, `--lyxc-*`, fallback `#be3a63`, hồng chip phân khúc về token chung. Quyết định: nút thanh toán giỏ trượt đen hay đỏ rượu.
2. **Sửa nội dung sai trước khi làm đẹp**: thông điệp chính sách header/CTA, đếm ngược, "mùa thu đông", "!!".
3. **Đồng bộ trang còn thiếu** theo thứ tự ảnh hưởng doanh thu: `/cart` → trang SP (khối mô tả, chip, SP tương tự) → khối sale danh mục mobile → blog/bài viết/báo chí → liên hệ, tìm kiếm, tài khoản, 404, chính sách.
4. Gom CSS trang phụ thành một file `lyx-pages.css` (thay `ly-pages.css` dần), tránh thêm lớp phủ mới.
5. Thay ảnh tạm (Unsplash, img_video_6) bằng ảnh thật; bật cờ trong `lyx-flags.bwt`.
6. Kiểm 1440 / 1024 / 768 / 390px cho từng trang trên preview 1170160 trước khi đề nghị xuất bản; xuất bản do anh Công làm trong admin.

---

## 9. Bản đồ file chính (theme 1170160)

```
layouts/theme.bwt                 2 nhánh head/body, thứ tự nạp CSS/JS (17/10)
templates/index.bwt               → snippets/lyx-home.bwt
templates/collection.bwt          danh mục lyx (giữ khung col.js / ly-filter.js)
templates/product.bwt             KHUNG GỐC – không viết lại
templates/cart.bwt                giỏ 09/10 (ly-*) – chưa editorial
templates/page.about.bwt          lyx-about + ly-about
templates/blog.bwt, blog.baochi.bwt, article.bwt, page.contact.bwt, search.bwt, 404.bwt, customers/*  – chưa editorial
snippets/lyx-header.bwt | lyx-footer.bwt | lyx-logo.bwt | lyx-home.bwt | lyx-flags.bwt | lyx-sale.bwt | lyx-about.bwt
snippets/ly-home-card.bwt         thẻ SP dùng chung (.lyx-card)
snippets/ly-segments.bwt | ly-seg-of.bwt   phân khúc / dòng thảm
snippets/tab_product.bwt          phần dưới trang SP + nạp lyx-pdp.js
snippets/ly-pdp-mobile.bwt        lớp mobile kiểu Shopee
snippets/ly-pd-policy.bwt         tóm tắt chính sách đổi trả
snippets/ly-shopee-reviews.bwt | ly-shopee-reviews-data.bwt
snippets/ly-cart-drawer.bwt       giỏ trượt (nạp lyx-cart.css/js)
snippets/aside-filter.bwt | swatch.bwt | ly-favicon.bwt | ly-fonts.bwt
assets/lyx-base.css   token + nút + header + footer + menu mobile
assets/lyx-home.css/.js   trang chủ
assets/lyx-col.css/.js    danh mục
assets/lyx-pdp.css/.js    trang SP
assets/lyx-cart.css/.js   giỏ trượt
assets/lyx-about.css      giới thiệu
assets/lyx-editorial.css  LỚP PHỦ CUỐI 17/10 (danh mục, SP, giới thiệu, footer, thẻ danh mục trang chủ)
assets/ly-*.css/js        lớp 09–13/10 (cart, filter, site, design, pages, pd-info, pdp, reviews, segments)
assets/lysr-1..4.js       dữ liệu đánh giá Shopee
```

---

## 10. Giới hạn của lần rà soát này
- Chưa xem giao diện bằng trình duyệt (không có ảnh chụp, không đo px, không kiểm lỗi console). Claude Code nên bắt đầu bằng một vòng chụp/so sánh trên preview 1170160 ở 1440/1024/768/390px.
- Chưa đọc đầy đủ `lyx-home.css` (36 KB), `lyx-pdp.css` (28 KB), `lyx-col.css`, `lyx-about.css`, `lyx-home.js`, `ly-*.css`; mô tả các file này dựa trên comment đầu file và nơi chúng được gọi.
- Danh sách asset API có thể bị cắt ở ~250 file (đã gặp 10/10); lần này trả về đủ đến các file lyx mới nhất nhưng không có xác nhận tổng số.
- Không có tài liệu trạng thái cho phiên 15–17/10 trong Project; lịch sử giai đoạn này lấy từ comment trong code. Phiên đó dùng bộ kit đã ngừng dùng — những gì kit lưu ngoài Sapo (sao lưu, ảnh, ghi chú) coi như không còn.
