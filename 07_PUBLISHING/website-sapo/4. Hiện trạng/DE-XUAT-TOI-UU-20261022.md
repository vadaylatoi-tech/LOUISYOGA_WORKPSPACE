# Đề xuất tối ưu tốc độ & ổn định hiển thị — louisyoga.vn (22/10/2026)

Phạm vi: theme 1170160 (web thật). Mục tiêu: chạy nhanh hơn, hiển thị giống nhau trên mọi điện thoại và máy tính. **Giữ nguyên giao diện, chức năng, nội dung.**
Cách đọc: **[Đo]** = số liệu em đo hôm nay; **[Suy luận]** = nguyên nhân có khả năng cao nhưng chưa kiểm trên iPhone thật; **[Đề xuất]** = việc cần anh duyệt.

---

## 1. Kết luận nhanh

1. **Web chậm vì mỗi trang nạp quá nhiều thứ thừa** [Đo]. Mỗi trang con tải 28–31 file CSS (8 file bị nạp 2 lần), khoảng 590KB CSS và 1MB JS. Trong đó **chỉ 15–27% quy tắc CSS thật sự được dùng** trên trang đó. Đây là hệ quả của 3 lớp giao diện chồng nhau (theme gốc → `ly-*` → `lyx-*`), kèm khoảng 3.900 lệnh `!important` đè qua đè lại.
2. **"Mỗi máy lỗi một kiểu" có 3 nguyên nhân chính:**
   - **Trang tự nhảy bố cục sau khi đã hiện** [Đo]. Ở khổ điện thoại, chỉ số xô lệch (CLS) là **1,79 ở trang sản phẩm** và **1,14 ở trang danh mục**; Google coi tốt là dưới 0,1. Máy nhanh hay chậm thì người dùng bắt gặp ở thời điểm khác nhau, nên thấy "thi thoảng lỗi".
   - **Nút giỏ trên thẻ sản phẩm được đặt bằng một mẹo CSS dễ vỡ trên Safari** [Đo cách đặt + Suy luận nguyên nhân]. Rất có thể đây là lỗi anh thấy trên iPhone 14 Pro Max.
   - **Có dùng tính năng CSS/JS mới** [Đo]: container query (cần iOS 16), `:has()`, `<dialog>`, `dvh` (cần iOS 15.4). iPhone nào chưa cập nhật iOS (hay gặp ở iPhone 11) sẽ hiển thị khác.
3. Hướng xử lý: **sửa lỗi hiển thị trước (nhanh, rủi ro thấp)** → **dọn và chia nhỏ CSS/JS theo từng trang** → **dựng bộ kiểm tự động trên nhiều khổ máy** để lỗi kiểu này không quay lại.

---

## 2. Số liệu đo (22/10, web thật)

### 2.1 Dung lượng mỗi trang
| Trang | HTML | File CSS (lượt nạp) | CSS thô | JS thô | Ảnh | Quy tắc CSS được dùng |
|---|---|---|---|---|---|---|
| Trang chủ | 250KB | 14 (14) | 252KB | 708KB | 57 | — |
| Danh mục `/collections/all` | 393KB | 28 (36) | 570KB | 1.024KB | 59 | **15%** |
| Sản phẩm (LILIUM) | 397KB | 29 (37) | 593KB | 1.047KB | 89 | **27%** |
| FAQ | 211KB | 24 (32) | 510KB | 916KB | 20 | — |

- **8 file CSS nạp 2 lần** trên mọi trang con: `bootstrap`, `main.scss`, `ajaxcart`, `quickviews_popup_cart`, `ly-cart`, `lyx-editorial`, `lyx-pdp`, `jquery-ui`/`picbox`/`style_page`. Lần nạp thứ 2 ở cuối trang được thêm vào ngày 17/10 để "thắng" CSS cũ.
- **CSS nạp ở trang không cần** (tỉ lệ dùng trên trang danh mục): `lyx-pdp.css` **0%**, `lyx-pages.css` 1%, `jquery-ui` 0%, `style_page` 0%, `lyx-home.css` 14%, `ly-design.css` 6%, `main.scss.css` 9% (file 88KB, 270 `!important`), `bpr.min.css` 1% (app đánh giá đã hết hạn).
- **Số `!important` trong các file của Louis Yoga**: `lyx-ui` 420, `lyx-pdp` 360, `lyx-pages` 338, `ly-pages` 219, `lyx-shop` 196, `lyx-editorial` 186, `lyx-cart` 184, `ly-pdp` 170…
- **JS:** khoảng 25 file trên trang con. Có thư viện nạp ở trang không dùng tới, ví dụ `tabletop.js` (đọc Google Sheets) trên trang sản phẩm, `jquery-ui` trên danh mục.
- **109KB JS của Sapo (`Bizweb api`) được chép thẳng vào HTML** trên mọi trang con, nên trình duyệt không lưu đệm được và phải tải lại mỗi lần đổi trang.
- **JS bên thứ ba:** Google Analytics khoảng 527KB (nạp không chặn, giữ nguyên); Zalo SDK 105KB (nạp **chặn**); reCAPTCHA nạp trên mọi trang. Hai thứ sau do Sapo và ứng dụng chèn vào.

### 2.2 Thời gian & độ ổn định
- Thời gian máy chủ trả trang: khoảng 0,15–0,2 giây khi đã có bộ đệm. **Lần đầu (chưa có bộ đệm) danh mục mất 1,6 giây, trang sản phẩm 0,8 giây** do vòng lặp Liquid quét `collections['all']` (250 sản phẩm) [Đo].
- Trên máy em (mạnh, mạng nhanh), mọi trang tải xong trong khoảng 0,5 giây, nên chậm chủ yếu xảy ra trên **điện thoại đời cũ + 4G**: phải tải và xử lý khoảng 600KB CSS cùng 1MB JS [Suy luận].
- **CLS ở khổ điện thoại** [Đo]:

| Nguồn gây nhảy | Mức | Ở đâu |
|---|---|---|
| Khung chat Zalo **tự bật sau 2 giây** (`data-autopopup="2"`), bung cao 675px rồi thu lại | 0,58 + 0,57 | mọi trang con |
| Trang sản phẩm: khối ảnh / thông tin / chính sách bị JS (`ly-pdp.js`, `lyx-pdp.js`) xếp lại sau khi hiện | 0,61 | trang sản phẩm |
| Ảnh nhỏ swiper, dòng sao | nhỏ | trang sản phẩm |

### 2.3 Thẻ sản phẩm — nút giỏ hàng (lỗi iPhone 14 Pro Max)
- Hàng nút `.lyx-card-actions` là `position:absolute; top:0; left:0; right:0;`, **chiều cao chỉ dựa vào `aspect-ratio:1/1`** để nút "rơi" xuống đáy ảnh vuông (`lyx-card.css`) [Đo].
- Trên Chrome nút luôn nằm đúng góc dưới-phải ảnh ở mọi khổ 375–430 [Đo]. Nhưng **WebKit (Safari) từng có lỗi tính `aspect-ratio` cho phần tử absolute bị kéo giãn bởi cả `left` và `right`**, còn iOS cũ thì bỏ qua thuộc tính này. Khi đó hàng nút chỉ cao bằng nút, và nút **nhảy lên góc trên của ảnh** hoặc lệch [Suy luận, cần ảnh chụp máy thật để chốt].
- Ngoài ra nút giỏ ở trang chủ 32px, ở danh mục và trang sản phẩm 40px (không đồng nhất).
- Lớp thẻ cũ có `.ly-card{container-type:inline-size}` + `@container` (iOS 16+) trong `ly-tweaks.css`. Thuộc tính này còn làm đổi cách tính kích thước thẻ trên một số bản Safari.

### 2.4 Tính năng có thể khác nhau theo đời iOS [Đo — có trong code]
| Tính năng | Cần tối thiểu | File |
|---|---|---|
| Container query `@container` | iOS 16 | `ly-tweaks.css` (thẻ SP), `lyx-home.css` (video hero) |
| `:has()` | iOS 15.4 | `ly-design.css`, `ly-pages.css`, `lyx-home.css`, `lyx-pdp.css` |
| `<dialog>.showModal()` | iOS 15.4 | `ly-design.js`, `ly-home.js`, `ly-site.js`, `lyx-home.js` (hộp yêu thích, video, chọn phân loại) |
| `dvh` | iOS 15.4 | `ly-cart.css`, `ly-pdp.css`, `lyx-home.css`, `lyx-shop.css` |
| `overflow:clip` | iOS 16 | `ly-pages.css` |
| `backdrop-filter` thiếu tiền tố `-webkit-` | Safari cần tiền tố | `ly-cart.css` |
| `aspect-ratio` | iOS 15 | nhiều file (thẻ, hero, ảnh) |

→ iPhone chạy **iOS 15.0–15.3 hoặc iOS 14** sẽ: không mở được hộp chọn phân loại/yêu thích/video, thẻ và hero có thể méo. **Cần biết iOS của từng máy anh thử** (Cài đặt → Cài đặt chung → Giới thiệu → Phiên bản iOS).

---

## 3. Phương án đề xuất (theo giai đoạn)

### Nguyên tắc chung
- **Làm trên bản sao theme**: nhân bản 1170160 thành theme nháp, sửa và kiểm qua `?previewThemeId=…`, anh duyệt xong thì **anh xuất bản trong admin**. Web thật không bị ảnh hưởng trong lúc dọn. (Việc tối ưu sẽ đụng nhiều file cùng lúc, không nên sửa thẳng trên web thật.)
- **Mỗi bước đều có ảnh chụp trước/sau** ở 7 khổ (375, 390, 414, 430, 768, 1024, 1440) cho khoảng 16 trang, so khớp để chắc chắn giao diện không đổi.
- **Báo phiên Claude còn lại** (máy mới của anh) tạm dừng sửa theme trong thời gian dọn, tránh ghi đè lẫn nhau.

### Giai đoạn 1 — Sửa lỗi hiển thị theo thiết bị (rủi ro thấp, làm trước, khoảng 1–2 buổi)
1. **Nút giỏ trên thẻ sản phẩm:** đặt nút vào trong khung ảnh với `position:absolute; right; bottom`, bỏ phụ thuộc `aspect-ratio`. Thống nhất cỡ nút giữa các trang. File: `snippets/ly-home-card.bwt`, `assets/lyx-card.css`.
2. **Khung chat Zalo:** tắt chế độ tự bật (hoặc chỉ tự bật trên PC). Chỉnh trong *Tùy chỉnh giao diện → Live chat*, hoặc em sửa mã. Bỏ được hơn một nửa độ xô lệch trên mọi trang con. **Cần anh quyết.**
3. **Bỏ container query** trên thẻ (`ly-tweaks.css`) → thay bằng media query cùng kết quả.
4. **Thêm phương án dự phòng** cho máy cũ: `dvh` → khai `vh` trước; `overflow:clip` → `hidden` trước; thêm `-webkit-backdrop-filter`; `<dialog>` → kiểm `showModal` có tồn tại không, không có thì mở bằng lớp CSS; `:has()` → thêm lớp do JS gắn cho các chỗ quan trọng.
5. **Trang sản phẩm điện thoại:** giữ chỗ sẵn (chiều cao ảnh, khối chính sách) và để CSS xếp đúng ngay từ đầu, hạn chế JS di chuyển khối sau khi tải. Mục tiêu CLS dưới 0,1.

### Giai đoạn 2 — Giảm tải CSS/JS (giữ nguyên giao diện, khoảng 3–5 buổi, làm dần từng trang)
1. **Mỗi trang chỉ nạp CSS của trang đó**: `lyx-pdp.css` chỉ trang sản phẩm, `lyx-col.css`/`lyx-shop.css` chỉ danh mục, `lyx-pages.css` chỉ blog/trang nội dung, `lyx-home.css` chỉ trang chủ (phần thẻ dùng chung tách ra file chung).
2. **Bỏ 8 lượt nạp CSS lần 2** bằng cách viết selector đủ mạnh, thay cho việc nạp lại file.
3. **Gộp và dọn quy tắc chết**: hợp các lớp `ly-*` + `lyx-*` thành 1 bộ "lõi" + file theo trang, xoá quy tắc không còn phần tử nào dùng (đang khoảng 75–85%), giảm `!important`. Dự kiến CSS mỗi trang còn khoảng 200–250KB (từ khoảng 590KB) [ước tính].
4. **JS:** bỏ thư viện không dùng ở trang đó (`tabletop.js`, `jquery-ui`, `placeholdertypewriter` nếu tắt…), chuyển script của theme sang `defer`, nạp Zalo SDK sau khi trang đã hiện. Thử chuyển 109KB `Bizweb api` chép trong HTML thành file ngoài để trình duyệt lưu đệm (nếu Sapo cho phép).
5. **Ảnh & video:** hero YouTube dùng "ảnh bìa, bấm mới tải video" (giảm khoảng 1MB JS lúc đầu); ảnh đầu trang được tải trước (preload), ảnh dưới màn hình tải chậm (đa phần đã làm).
6. **Liquid:** giảm vòng lặp `collections['all']` 250 sản phẩm ở khối "Sản phẩm tương tự" và trang chủ, rút thời gian trả trang lần đầu từ 0,8–1,6 giây.
7. **App đánh giá Sapo đã hết hạn** nhưng `bpr.min.css` (66KB) và `productReviews.min.css` (41KB) vẫn nạp → nếu anh xác nhận không dùng lại thì tắt.

### Giai đoạn 3 — Giữ ổn định lâu dài
1. **Bộ kiểm tự động** (em dựng, chạy sau mỗi lần sửa): khoảng 16 trang × 7 khổ — tràn ngang, CLS, vị trí nút giỏ / ô màu / nút mua, ảnh lỗi, lỗi console, thời gian tải. Lưu kết quả để so sánh.
2. **Quy tắc viết mã** (ghi vào BAN-GIAO): không dùng tính năng chỉ chạy từ iOS 16 trở lên mà không có dự phòng; không dùng mẹo `aspect-ratio` + `absolute`; không di chuyển khối sau khi tải; mỗi thành phần chỉ một nguồn CSS; hạn chế `!important`.
3. **Kiểm trên máy thật** trước mỗi lần xuất bản: iPhone 11, 12, 14 Pro Max (ghi rõ iOS), 1 máy Android, Safari trên Mac. Nếu cần kiểm nhiều máy hơn có thể dùng dịch vụ máy ảo như BrowserStack (trả phí).

### Kết quả mong đợi [ước tính, sẽ đo lại sau mỗi giai đoạn]
| Chỉ số | Hiện tại (trang con) | Mục tiêu |
|---|---|---|
| CLS điện thoại | 1,1–1,8 | < 0,1 |
| File CSS mỗi trang | 28–31 (36–37 lượt) | khoảng 10–12, không nạp trùng |
| CSS thô | khoảng 590KB | khoảng 200–250KB |
| JS của theme | khoảng 25 file | bỏ file không dùng, toàn bộ `defer` |
| Lỗi theo đời iPhone | có | không còn tính năng thiếu dự phòng |

---

## 4. Cần anh Công quyết / cung cấp
1. **Đồng ý làm trên bản sao theme** rồi anh xuất bản? (em khuyên nên làm vậy)
2. **Tắt chế độ tự bật khung chat Zalo** (trên điện thoại / tất cả)?
3. **Phiên bản iOS** của iPhone 11, 12, 14 Pro Max đang thử, kèm **ảnh chụp lỗi nút giỏ trên 14 Pro Max** (trang nào).
4. **Thứ tự**: làm Giai đoạn 1 ngay, Giai đoạn 2 làm dần từng trang và mỗi trang anh duyệt?
5. App "Đánh giá sản phẩm" Sapo đã hết hạn: có gia hạn lại không? Nếu không thì em bỏ CSS của app.
6. Báo phiên Claude máy mới tạm dừng sửa theme trong thời gian tối ưu.
