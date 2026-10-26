# BỘ CONTEXT DỰ ÁN LOUIS YOGA (louisyoga.vn – Sapo) — BÀN GIAO CHO CHATGPT

> Xuất ngày 11/10/2026, 14:37 (giờ Việt Nam). Gộp từ 3 tài liệu của Claude Project:
> 1. `STATIC_CONTEXT_LOUIS_YOGA.md` — ràng buộc nền, hệ thống thiết kế, quy ước
> 2. `claude/CURRENT_STATUS_2026-10-11.md` — trạng thái mới nhất (11/10)
> 3. `claude/CURRENT_STATUS.md` — nhật ký chi tiết 09–10/10
>
> Nội dung 3 tài liệu được giữ nguyên văn bên dưới. Phần 0 là hướng dẫn đọc dành riêng cho ChatGPT.

---

## PHẦN 0 — HƯỚNG DẪN CHO CHATGPT (đọc trước)

### Vai trò và cách giao tiếp
- Người dùng: **anh Công** (Đào Duy Công), nhà thiết kế đồ họa 2D. Trả lời **tiếng Việt**, tự xưng **em**, gọi **anh**.
- Trực tiếp, không nịnh, phản biện có căn cứ, không bịa. Phân biệt rõ: dữ kiện đã xác minh / suy luận / đề xuất.
- Vấn đề phức tạp: Kết luận → Phân tích → Đề xuất → Bước tiếp theo.

### Thứ tự ưu tiên khi các phần mâu thuẫn
**Yêu cầu mới của anh Công > Phần 2 (11/10) > Phần 3 (09–10/10) > Phần 1 (nền).**
Ví dụ: Phần 1 ghi theme copy là 1151386 — đã lỗi thời. Phần 3 ghi theme chính là 1170160 — đã lỗi thời. **Đúng nhất hiện tại: theme chính (web thật) = `1170134`** (theo Phần 2).

### Khác biệt môi trường quan trọng
- Các phiên trước do Claude làm, có **kết nối trực tiếp Sapo API** (đọc/ghi file theme) và trình duyệt để kiểm tra. **ChatGPT không có các quyền này** trừ khi anh Công cấp công cụ tương đương.
- Vì vậy: khi cần sửa file, **xin anh Công dán nội dung hiện tại của file** (Sapo admin → Giao diện → Sửa code) trước khi đề xuất sửa; không viết lại file từ trí nhớ hay từ mô tả trong tài liệu này.
- Trả kết quả dạng **toàn bộ nội dung file đã sửa** hoặc **đoạn thay thế có chỉ rõ vị trí**, kèm cách hoàn tác.
- Không tuyên bố "đã kiểm tra" khi chưa thật sự kiểm tra; nói rõ phần nào anh cần tự kiểm trên trình duyệt (PC + điện thoại thật).

### Quy tắc an toàn (bắt buộc)
- Theme 1170134 đang là **website thật**: mọi sửa đổi trên nó đều ảnh hưởng khách ngay. Nên đề nghị anh **nhân bản 1170134** để sửa thử, xem trước, rồi mới xuất bản.
- **Xuất bản theme phải làm trong Sapo admin** (xuất bản qua API chỉ đổi cho máy tính, điện thoại vẫn nhận theme cũ). Sau xuất bản luôn kiểm bằng điện thoại.
- Không sửa `templates/product.bwt` toàn bộ (chứa logic chọn phân loại `selectCallback` + `Bizweb.OptionSelectors`).
- Luôn sao lưu file trước khi sửa (quy ước: `snippets/zz-backup-<tên>.bwt`).
- Không rebrand sang Louga, không đổi tên miền/nội dung sản phẩm trong dự án này.

### Việc còn treo (tóm tắt từ các phần dưới, để tiện bắt đầu)
- Video hero: **chưa kiểm trên iPhone thật** (phụ đề CC YouTube có thể vẫn hiện); chưa xác nhận phát 1080p trên Chrome thật. Hướng triệt để: tự host MP4 (anh Công tạm gác).
- Thẻ YOGA MAT trên điện thoại: lưới 2 cột, nút chữ 8px — chưa xử lý.
- Phân khúc/dòng thảm chưa gán: SUN, MINI.
- Danh mục Harmony/Balance/Mastery mới là trang lọc `/collections/all?q=id:(...)`, chưa phải danh mục Sapo thật.
- Cần anh Công sửa trong admin: `policy_title_2` ("7 ngày đổi trả" → chính sách đã chốt 3/10 ngày), trang `/chinh-sach-kiem-hang` còn ghi 7 ngày, "FACIFIC" → "PACIFIC", `social_fb` → https://www.facebook.com/thamlouisyoga, biến thể trùng/0đ của NATURE & LILIUM, mô tả NATURE có `<style>` chưa đóng; hotline 0352 587 836 vs 0888 293 996 chưa chốt.
- Chưa thử luồng Thanh toán tới /checkout; thanh freeship (600.000đ) chưa đối chiếu phí ship thật.
- File rác vô hại chờ duyệt xoá: `assets/ly-logo.svg` (0 byte).

---

## PHẦN 1 — STATIC CONTEXT (nguyên văn `STATIC_CONTEXT_LOUIS_YOGA.md`)

# STATIC CONTEXT — LOUIS YOGA WEBSITE (SAPO)

> Loại tài liệu: Ngữ cảnh nền lâu dài cho Claude Project. Nguồn: bản bàn giao hội thoại ngày 09/10/2026 do người dùng cung cấp. Đây là thông tin được **báo cáo trong phiên trước**, không phải kết quả kiểm tra độc lập hiện tại. Không sử dụng tài liệu này để suy ra tiến độ mới nhất.

## 1. Vai trò và cách cộng tác
- Người dùng là nhà thiết kế đồ họa 2D, làm việc với dự án website Louis Yoga thuộc Phúc Thái Global.
- Giao tiếp bằng **tiếng Việt**, AI xưng **em**, gọi người dùng là **anh**.
- Trả lời trực tiếp, không nịnh; phản biện có căn cứ, không bịa thông tin. Phân biệt dữ kiện, suy luận và đề xuất.
- Với vấn đề phức tạp, ưu tiên: **Kết luận → Phân tích → Đề xuất → Bước tiếp theo**.
- Bám sát yêu cầu gốc; không tự mở rộng phạm vi. Có thể thực hiện giả định nhỏ, có thể đảo ngược và phải nói rõ; hỏi trước khi thay đổi quan trọng hoặc khó hoàn tác.

## 2. Mục tiêu và giới hạn dự án
- Mục tiêu: **chỉnh giao diện website louisyoga.vn theo thiết kế được người dùng cung cấp** trên nền tảng Sapo.
- **Giữ nguyên** logo, thương hiệu **Louis Yoga**, tên miền và nội dung sản phẩm.
- **Không tự triển khai rebrand Louga**, viết lại nội dung hay đổi tên miền trong dự án này.
- Chỉ sửa **theme bản copy**, xem trước và xin duyệt trước khi xuất bản lên website chính.
- Thiết kế tham chiếu được mô tả gồm ba trang: **trang chủ, trang cửa hàng/danh mục, trang chi tiết sản phẩm**. Nếu cần so sánh pixel, phải mở lại file thiết kế gốc; bản tóm tắt không thay thế file thiết kế.

## 3. Môi trường Sapo và quy tắc thao tác
- Website: `https://louisyoga.vn/`.
- Cửa hàng Sapo alias: `hung-yen-sport`.
- Trang quản lý theme: `https://hung-yen-sport.mysapo.net/admin/themes`.
- **Theme chính tại thời điểm bàn giao:** ID `983840`, tên `Louis Yoga 26-12`. **Không sửa** nếu chưa có sự chấp thuận rõ ràng.
- **Theme copy mục tiêu tại thời điểm bàn giao:** ID `1151386`, tên `Louis Yoga 26-12 - Copy`.
- Link preview đã được báo cáo hoạt động trong phiên trước: `https://louisyoga.vn/?previewThemeId=1151386` (cần phiên đăng nhập phù hợp).
- Trước mỗi lần sửa, xác minh theme ID và trạng thái thực tế vì chúng có thể đã thay đổi.
- Luôn đọc nội dung file hiện tại trước khi ghi; ưu tiên sửa nhỏ, bảo toàn logic cũ và có phương án hoàn tác.
- Không tự đăng nhập bằng mật khẩu, không tự thao tác giỏ hàng thật hoặc xuất bản theme. Nếu cần thử giỏ hàng phải xin phép và khôi phục trạng thái ban đầu.
- Khi kiểm tra qua trình duyệt của người dùng, ưu tiên tab riêng, không chiếm dụng tab đang làm việc.

### Connector và API: thông tin lịch sử cần xác minh lại
- Phiên trước dùng connector `Sapo_Louis_Yoga` để đọc asset với `sapo_request` GET `themes/1151386/assets.json`, query `{"key":"<đường dẫn file>"}`.
- Ghi asset qua `put_theme_asset`; công cụ được báo cáo có cơ chế chặn ghi vào theme chính.
- Phiên trước báo lỗi với `get_theme_asset`, API sản phẩm/đơn hàng trả 403 và nội dung file lớn có thể bị cắt. **Không mặc định các hạn chế này còn tồn tại**; kiểm tra quyền và công cụ của phiên hiện tại.

## 4. Hệ thống thiết kế tham chiếu
- Font: **Montserrat** (nhiều độ đậm) và **Inter**.

| Vai trò | Mã màu / quy định |
|---|---|
| Hồng chủ đạo | `#d72182` |
| Đỏ rượu cho chữ/nhãn | `#4a202c` |
| Tấm thảm trong hero tham chiếu | `#a03551` |
| Nền xám | `#f2f2f2` |
| Nền sale | `#fed8e3` |
| Nền dải lợi ích | `#fcefef` |
| Footer tối | `#171516` |
| Giá mới trên thẻ | `#00869e`, dạng `699.000 VNĐ` |
| Giá cũ trên thẻ | `#d72182`, gạch ngang |
| Sao đánh giá | `#d69d31` |
| Nút thêm vào giỏ | chữ `#606060`, viền `#b6b6b6` |
| Thanh lọc giá | `#08392a` trên nền `#cccccc` |
| Chip bộ lọc | nền `#d72182`, chữ trắng |
| Xóa bộ lọc | `#ed1c24` |

- Khối **YOGA MAT** trong thiết kế: vùng 988px; 3 cột thẻ khoảng 184px; khoảng cách ngang 36px, khoảng cách hàng 39px; banner khoảng 330px, tỷ lệ ~1,885:1; tiêu đề cao khoảng 61px, gạch chân 310px, dòng phụ 20px.
- Tỷ lệ chiều rộng nút **Thêm vào giỏ : Mua ngay** trên thẻ khoảng **1,27 : 1**.
- Các số đo là thông tin trích từ bản bàn giao, cần đối chiếu lại file thiết kế khi chỉnh chi tiết.

## 5. Quyết định thiết kế và hành vi đã chốt

### Trang chủ
- Hero hiển thị **“11 năm”** theo thiết kế (không dùng chữ “15 năm” cũ).
- Có dải **LOUISYOGA**, ba cam kết, khối sale có đồng hồ đếm ngược bốn ô, khối **YOGA MAT**, khu vực banner, phụ kiện, nội dung Yogi, đăng ký nhận tin và footer.
- Không hiển thị chữ giữ chỗ của ảnh cho khách (`.ly-media-label` được ẩn).
- Tiêu đề khối sale đã chọn: **“ƯU ĐÃI LOUIS YOGA / Sản phẩm ưu đãi”**; không dùng dòng chữ mẫu trong thiết kế. Ngày sale là dữ liệu chiến dịch, **không phải ngữ cảnh cố định**.

### Thẻ sản phẩm dùng chung
- Dùng mẫu `ly-home-card` cho trang chủ, danh mục, kết quả lọc/tìm kiếm và sản phẩm tương tự.
- Tên sản phẩm đậm, màu đen; đánh giá thật lấy từ `product.metafields.bpr`; khi chưa có đánh giá, hiển thị năm sao màu xám, không giả làm đánh giá thật.
- Giá cũ màu hồng và gạch ngang; giá mới màu xanh, định dạng VNĐ.
- Có nút **Thêm vào giỏ** và **Mua ngay**.
- Sản phẩm một phân loại: thêm qua AJAX `/cart/add.js`; Mua ngay chuyển `/checkout` sau khi thêm thành công.
- Sản phẩm có nhiều màu/phân loại: mở hộp chọn `.ly-pick` trước khi thực hiện hành động tương ứng.

### Trang danh mục
- Banner **“CỬA HÀNG / LOUIS YOGA”** hoặc tên danh mục phù hợp; dải thương hiệu, ba cam kết, lưới bốn cột trên nền xám và các banner cuối trang.
- Không hiển thị breadcrumb nếu thiết kế tham chiếu không có.
- Thứ tự bộ lọc đã chốt: **Loại sản phẩm → Chọn mức giá → Đánh giá → Màu phổ biến → Độ dày**.
- Thanh giá hai đầu: 0–6.000.000đ, bước 50.000đ theo thiết kế; giới hạn dưới 1đ từng là biện pháp tránh dữ liệu biến thể giá 0, **cần kiểm tra dữ liệu hiện tại trước khi duy trì hoặc bỏ**.
- Có chip **Đang lọc theo**, nút **Xóa bộ lọc**; ẩn khối **Bạn chọn** cũ.
- Lọc đánh giá dựa trên dữ liệu thực và logic làm tròn rating đã mô tả trong bản bàn giao.
- Hai nhóm **Tiêu chí** và **Phân khúc** chưa được chốt trong nguồn, **không tự xem là yêu cầu đã duyệt**.

### Trang chi tiết sản phẩm
- Ẩn breadcrumb; ảnh chính lớn, thumbnail ngang bên dưới; chọn màu theo ô có tên.
- Khung thông số lấy từ `product.summary`, màu hồng; hai nút hành động bo tròn đặt cạnh nhau.
- Ẩn flash sale cũ, sidebar và sản phẩm đã xem.
- Nội dung bên dưới dạng mở/đóng: **Chi tiết sản phẩm / Bảo quản / Vận chuyển và đổi trả**.
- Mục Bảo quản chỉ dành cho thảm, có link bài hướng dẫn; mục vận chuyển/đổi trả lấy nội dung từ trang `chinh-sach-bao-hanh-doi-tra-san-pham`.
- Có khung đánh giá khách hàng qua app Sapo, khu vực bốn sản phẩm tương tự và banner.
- Không tự tạo mục **Chất liệu** từ `product.type` khi trường này không chứa chất liệu thực tế.

## 6. Quy ước mã nguồn và file
- CSS giao diện chính: `assets/ly-design.css`.
- CSS tinh chỉnh: `assets/ly-tweaks.css`, nạp sau CSS chính; ưu tiên dùng cho điều chỉnh nhỏ.
- JS giao diện: `assets/ly-design.js`.
- JS bộ lọc: `assets/ly-filter.js`.
- Layout: `layouts/theme.bwt`.
- Template liên quan: `templates/collection.bwt`, `templates/search.data.bwt`.
- Snippet liên quan: `snippets/ly-home-main.bwt`, `snippets/ly-home-card.bwt`, `snippets/ly-icon.bwt`, `snippets/ly-strip.bwt`, `snippets/ly-promos.bwt`, `snippets/products-grid-item.bwt`, `snippets/tab_product.bwt`, `snippets/aside-filter.bwt`.
- **Bảo toàn `templates/product.bwt`** vì chứa logic chọn phân loại; không viết lại toàn file nếu không có yêu cầu mới và phương án kiểm thử rõ ràng.
- Các tên file trên phản ánh kiến trúc tại thời điểm bàn giao; **kiểm tra sự tồn tại và nội dung thực tế trước khi thao tác**.

## 7. Cách dùng ngữ cảnh này trong phiên mới
1. Xem tài liệu này là **ràng buộc nền**, không phải báo cáo trạng thái hiện tại.
2. Đọc thêm `CURRENT_STATUS.md` hoặc bản Context Handover mới nhất để biết tiến độ, lỗi, thay đổi và việc cần làm.
3. Nếu ngữ cảnh cố định mâu thuẫn với yêu cầu mới rõ ràng của người dùng, **nêu mâu thuẫn và xác nhận** trước khi thực hiện thay đổi quan trọng.
4. Không tuyên bố đã kiểm tra website, quyền API, file theme hoặc trình duyệt nếu chưa thực sự kiểm tra trong phiên hiện tại.
5. Không tự ý xuất bản theme, sửa theme chính, thay đổi sản phẩm hoặc thương hiệu.
6. Khi cần dữ liệu không có trong nguồn, hỏi ngắn gọn đúng phần thiếu; không bịa.

---

## PHẦN 2 — TRẠNG THÁI MỚI NHẤT 11/10 (nguyên văn `claude/CURRENT_STATUS_2026-10-11.md`)

# CURRENT STATUS — bổ sung 11/10/2026 (đọc file này TRƯỚC claude/CURRENT_STATUS.md; mục nào ở đây mâu thuẫn với file cũ thì file này đúng)

⚠ TỪ ~13h 11/10: THEME CHÍNH (web thật) = 1170134 "Louis Yoga (Bản mới - Edit chỉnh sửa)" (anh Công xuất bản trong admin; điện thoại Android cũng nhận 1170134 — đã kiểm 13h40). 1170160 về unpublished (bản 10/10, không có thay đổi 11/10). Ghi 1170134 = sửa web thật: cần allow_live_theme + anh Công đồng ý từng việc (13h35 anh đồng ý sửa thẳng phần hero video). Nên xin anh tạo bản sao 1170134 làm nơi sửa tiếp.

## 11/10/2026 ~12h — Dòng thảm "Thảm Du lịch" + "Thảm TPE" (chỉ theme 1170134, chưa xuất bản)
- Anh Công chốt: thảm Du lịch + OCEAN → "Thảm Du lịch"; TPE9 → "Thảm TPE". SUN, MINI vẫn chưa gán.
- Mã SP (lấy qua `/<alias>.js`): Du lịch 36960223 (`tham-tap-yoga-du-lich`), OCEAN 50892151 (`tham-tap-yoga-du-lich-ocean`), TPE9 36960236 (`tham-tap-yoga-tpe-dinh-tuyen-tpe9`). Túi đựng thảm TPE 36960208 là phụ kiện, KHÔNG gán.
- Thiết kế: tách thành bộ biến riêng `ly_line_*` (handles/names/models/ids/values/urls/all_ids) trong `snippets/ly-segments.bwt`, KHÔNG nhét vào `ly_seg_*` → tab YOGA MAT trang chủ (3 banner), nhãn "Phân khúc X" trang SP và `ly-seg-of.bwt` không đổi.
- Hiện ở: menu Cửa hàng desktop + mobile (nhóm "Dòng thảm" dưới "Phân khúc thảm"), chip danh mục (Tất cả · Harmony · Balance · Mastery · Thảm Du lịch · Thảm TPE · Phụ kiện), bộ lọc nhóm "Dòng thảm" ngay sau "Phân khúc" (chỉ hiện khi danh mục có SP thuộc dòng).
- `assets/ly-segments.js`: tiêu đề tab khi xem dòng có chữ "Thảm" → "Thảm Du lịch – Louis Yoga" (không lặp "Thảm tập Yoga").
- File sửa trên 1170134: snippets/ly-segments.bwt · snippets/ly-home-header.bwt · templates/collection.bwt · snippets/aside-filter.bwt · assets/ly-segments.js. Theme live 1170160 chưa đổi (bản cũ của 5 file này trên 1170160 = bản hoàn tác).
- Đã kiểm preview 1170134: link Thảm Du lịch → đúng 2 SP (OCEAN, Du lịch), H1 "THẢM DU LỊCH / LOUIS YOGA", chip & ô lọc tự đánh dấu; Thảm TPE → đúng 1 SP TPE9; menu desktop 1366×768 cao 528px, không tràn màn hình; không tràn ngang.
- Lưu ý: tích đồng thời 1 phân khúc + 1 dòng thảm (2 nhóm khác nhau cùng trường `id`) có thể ra 0 kết quả do bộ lọc Sapo nối nhóm bằng AND — chưa xử lý vì 2 tập SP không giao nhau.

## 11/10/2026 ~12h30 — Khối Ưu đãi bản điện thoại làm lại (chỉ theme 1170134, chưa xuất bản)
- Vấn đề (đo 390px): khối cao 1.192px — poster dọc 445px chiếm trọn màn đầu, 4 thẻ lưới 2×2 cao 612px, nút thẻ chữ 8px.
- Bố cục mới ≤767px (PC/tablet giữ nguyên, đã đo PC 1280: khối 474px, poster 330×440 như cũ):
  thanh đen tiêu đề (65px) → hàng sản phẩm vuốt ngang scroll-snap, thẻ 56% (187px, hé thẻ kế), nút 34px chữ 10px → chấm vị trí (JS mục 4) → banner ngang 2:1 (334×167).
  Tổng khối còn ~636px. Không tràn ngang.
- Banner điện thoại: `<picture>` nguồn `assets/ly-sale-poster-mb.jpg` (1200×600, anh Công thiết kế — CHƯA CÓ). Chưa có → onerror gỡ <source>, dùng poster dọc cắt phần trên (class `.is-fb`, object-position 50% 12%). Tải file lên là tự hiện, không cần sửa mã.
- File sửa: snippets/ly-home-mid.bwt · assets/ly-home-mid.css · assets/ly-home-mid.js. Hoàn tác: chép 3 file cùng tên từ theme live 1170160 (bản 10/10).
- Chưa làm: thẻ YOGA MAT/Phụ kiện mobile (lưới 2 cột) nút vẫn chữ 8px.

## 11/10/2026 ~13h — Mũi tên + chấm cho hàng vuốt; phân trang phụ kiện kiểu mới (chỉ 1170134)
- Phân trang phụ kiện PC: thay ô số xám ‹ 1 2 3 › bằng mũi tên tròn viền hồng + chấm viên thuốc (trang đang xem dài 28px hồng, còn lại chấm 8px hồng nhạt `--lym-pink-soft` #ecd2de). Đã kiểm 1280px: bấm chấm 2 → trang 2.
- Điện thoại: phụ kiện chuyển từ lưới 2×2 + phân trang dưới cùng sang hàng vuốt ngang giống ưu đãi (thẻ 56%, cả 10 SP, thanh phân trang ẩn). Lý do: nút chuyển nằm ngay trên ảnh/ngay dưới thẻ, khối cao ~373px thay ~900px.
- Hàng vuốt (ưu đãi + phụ kiện): mũi tên tròn trắng 36px hai bên, ở giữa ảnh (`--lym-nav-top` 33% / 27%), tự ẩn ở đầu/cuối; chấm vị trí (ưu đãi: trắng trên nền hồng; phụ kiện: hồng trên nền xám). Nút thẻ 34px chữ 10px.
- Markup: hàng bọc trong `.lym-track[data-lym-carousel]` + `.lym-nav.lym-prev/.lym-next`, chấm `.lym-cdots` ngay sau track.
- Sửa lỗi: banner ưu đãi điện thoại hiện ảnh vỡ khi trang tải ở khổ PC rồi thu nhỏ/xoay màn (trình duyệt không phát lỗi khi đổi <source>) → JS mục 5 kiểm naturalWidth sau load/resize, tự quay về poster dọc. Đã kiểm.
- Thẻ YOGA MAT mobile vẫn lưới 2 cột, nút chữ 8px (chưa đụng).

## 11/10/2026 ~13h40 — Video nền hero PC + mũi tên quay vòng (chỉ 1170134)
- Hero PC (≥768px): YouTube AFo_DvpQWf0 ("LOUIS YOGA X HOA HẬU YOGA VIỆT NAM 2024") chạy 15s → mờ dần về banner ảnh 7s → phát lại từ đầu, lặp. Code trong `snippets/ly-home-main.bwt` (CSS `.lyhb-video`, `<div id="lyhb-yt">`, script cuối khối hero; biến LYHB_VID/LYHB_PLAY/LYHB_IMG).
  - IFrame API tải SAU window.load +1,2s (không chậm ảnh banner), host youtube-nocookie, tắt tiếng, không nút, không bấm được (pointer-events:none → click vẫn đi link banner #ly-mats). Video phủ kín khung (16:9 cắt trên/dưới), không lộ thanh tiêu đề YouTube.
  - Chỉ hiện lớp video khi player báo PLAYING (không khung đen). Không chạy: điện thoại, prefers-reduced-motion, saveData/2G. Tạm dừng khi hero khuất màn hình / tab ẩn. Video lỗi/chặn nhúng → gỡ lớp video, còn banner.
  - Đã kiểm 1280px (giả lập tab hiển thị vì pane ẩn): video hiện ~15s rồi về ảnh, vòng 2 phát lại. Nút "Sản phẩm Louis Yoga" vẫn nổi trên video.
  - Thời gian hiện banner 7s là em tự chọn (anh Công chưa nêu).
- Hàng vuốt mobile (ưu đãi + phụ kiện): mũi tên không bao giờ ẩn/khoá; cuối hàng bấm › → về sản phẩm đầu, đầu hàng bấm ‹ → tới cuối; click chặn lan (stopPropagation). Lý do: anh Công bấm hết sản phẩm, nút ẩn nên bấm trúng thẻ → vào trang sản phẩm. Đã kiểm: ưu đãi 197→394→444→0, phụ kiện …1626→0.

## 11/10/2026 ~14h — Video hero: mờ + to (chỉ 1170134)
- Đo 1440px: YouTube phát hd720 trong khung 1454px (phóng ~2×) → mờ; video dài 93s, có sẵn hd1080. Khung 16:9 cao 802px vs banner 680px → cắt ~15% trên/dưới (cảm giác "to").
- Đã sửa: player dựng 200% rồi scale(.5) (2850×1603 thực) → YouTube chọn hd1080 (đã đo getPlaybackQuality = hd1080); bỏ phóng 102%; chỉ hiện video sau 1,2s đã chạy (LYHB_WARM) để bỏ đoạn đầu chất lượng thấp; gợi ý vq=hd1080 + setPlaybackQuality (YouTube có thể bỏ qua).
- CHƯA xác nhận được phát 1080p trong pane app Claude (visibilityState hidden → kẹt buffering ở giây 0 dù đã tải 18%; bỏ scale cũng kẹt → do môi trường). Cần anh Công xem trên Chrome thật.
- Phần cắt 15% là cố hữu khi nhúng YouTube 16:9 vào banner 2,1:1. Cách triệt để đề xuất: anh Công cắt clip MP4 15s đúng tỉ lệ banner (1920×916), tự host, thay YouTube bằng <video muted loop playsinline>.

## 11/10/2026 ~14h15 — Video hero: bỏ nút pause, bắt đầu từ giây 7 (chỉ 1170134)
- Nút pause tròn giữa video = hiệu ứng YouTube chớp mỗi lần dừng↔phát. Vòng lặp giờ KHÔNG dừng video khi hiện banner (chạy ngầm), chỉ seekTo(LYHB_START) lúc lớp video đang ẩn; chỉ dừng hẳn khi hero khuất màn/tab ẩn. LYHB_WARM 1,5s trước khi hiện.
- LYHB_START = 7 (bỏ đoạn nhân vật nói, anh Công yêu cầu) + playerVars start:7.
- Đã ghi 1 vòng 1280px: hiện ~giây 9→24, banner 7s (video vẫn trạng thái 1), tua về 7 rồi hiện lại; pane ẩn → dừng (2). Chưa chụp được hình vì pane ẩn.

## 11/10/2026 ~14h30 — Video hero theo 2 đoạn anh Công chọn (chỉ 1170134)
- LYHB_SEGS = [[9,21],[41,68]]: đoạn 9s→21s · banner 7s · đoạn 41s→1:08 · banner · lặp. Mỗi đoạn tua tới sớm LYHB_PRE 2,5s, chạy ngầm khi banner đang hiện; hiện/ẩn canh theo getCurrentTime() (poll 150ms), không theo setTimeout.
- Không dừng video giữa các đoạn (chỉ seekTo khi lớp video ẩn) → hiệu ứng nút pause/play của YouTube không lọt ra; chỉ pause khi hero khuất/tab ẩn.
- Đã kiểm 1280px (pane hiển thị thật): SHOW@9,1 → HIDE@20,5 → banner 7,3s → SHOW@41,07 → HIDE@68,0 → banner → SHOW@9,1. Chụp màn lúc đang phát và ngay lúc hiện đoạn 2: KHÔNG có nút pause.
- Nếu anh Công vẫn thấy nút pause: nghi bản cũ trong bộ nhớ trình duyệt → Ctrl+F5; nếu vẫn còn → chuyển sang tự host MP4.

## 11/10/2026 ~13h40 — Hero 2 giai đoạn + nút "Khám phá" (SỬA THẲNG WEB THẬT 1170134, anh Công đồng ý)
- Giai đoạn 1: vào trang banner hiện trước + nút "Sản phẩm Louis Yoga"; YouTube tải ngay khi DOMContentLoaded (không chờ load), player start = 8s, chạy tới 9s thì mờ sang video.
- Giai đoạn 2: hết đoạn → banner 7s (LYHB_IMG) → đoạn kế (9–21s, 41s–1:08) → lặp.
- Nút: hero.is-video (đang hiện video) → ẩn nút "Sản phẩm", hiện nút tròn "KHÁM PHÁ ↓" (50px, viền trắng, nền tối mờ blur, mũi tên nhún) giữa đáy hero; bấm → scrollIntoView phần kế tiếp (dải .ly-ribbon), đã kiểm: dừng ngay dưới header ghim. Banner → nút "Sản phẩm" hiện lại (chạy lại hiệu ứng xuất hiện).
- Bỏ ý tưởng ảnh bìa YouTube làm khung chờ (anh muốn banner trước).
- Điện thoại / giảm chuyển động / 2G: không YouTube, không nút Khám phá (đã kiểm Android UA 375px).
- Chưa kiểm được đoạn chuyển banner→video thật vì pane app bị ẩn (trình duyệt chặn tự phát); logic vòng lặp giữ nguyên bản đã kiểm 12h44. Hoàn tác: nội dung ly-home-main.bwt bản 12h41 (vòng 2 đoạn, chưa có nút Khám phá) hoặc bản 1170160 (chưa có video).

## 11/10/2026 ~13h50 — Dải chữ LOUISYOGA chạy ngang (SỬA THẲNG WEB THẬT 1170134)
- Vị trí có dải: trang chủ (ly-strip), trang danh mục (ly-strip đầu trang + .ly-ribbon-gap cuối trang trong templates/collection.bwt). Trang khác không có (đã dò /, /collections/all, SP, /cart, /gioi-thieu, /tin-tuc, /lien-he, /search, chính sách, đăng nhập).
- `snippets/ly-strip.bwt`: thêm <style> (keyframes ly-ribbon-run, track max-content, gap 0 + span padding-right 60px / mobile 36px để 2 nửa khớp tuyệt đối, 48s / mobile 34s ≈ 65–70px/s; .ly-ribbon-gap chạy ngược; tắt khi prefers-reduced-motion) + 40 chữ (trước 16, đứng yên).
- `templates/collection.bwt`: dải cuối 16 → 40 chữ.
- Đã kiểm 1440px: 2 dải running, nửa = 3360px (khớp ±1px), dịch ~70px/s; 390px: nửa 2150px, không tràn ngang. Trang chủ: 40 chữ + có keyframes.
- Hoàn tác: ly-strip bỏ <style> và đổi (1..40)→(1..16); collection.bwt (1..40)→(1..16).

## 11/10/2026 ~14h — Video hero cho cả điện thoại (SỬA THẲNG WEB THẬT 1170134, ly-home-main.bwt)
- Bỏ điều kiện chỉ PC (min-width:768) trong JS + bỏ CSS ẩn .lyhb-video/.lyhb-down trên ≤767px. Cùng 2 giai đoạn + đổi nút như PC.
- Phủ khung kiểu cover bằng container query (.lyhb-video{container-type:size}): PC width max(200cqw,355.6cqh) scale .5 (1080p); điện thoại width max(100cqw,177.8cqh), không nhân đôi → YouTube chọn hd720 (đã đo). Khung dọc lấy phần giữa video.
- Nút Khám phá mobile 44px, chữ 10px, cách đáy 22px.
- Đã kiểm Android UA 375px: iframe 1106×622 phủ kín hero 375×622, không tràn ngang; video hiện ở giây 9,2, nút Khám phá hiện, nút Sản phẩm ẩn; chụp màn: người mẫu ngồi trên thảm, rõ. PC 1280: player 2530×1423, hiện 1265×712, không đổi.
- Vẫn tắt khi reduced-motion / saveData / 2G; iPhone chế độ nguồn thấp chặn tự phát → giữ banner.
- Ghi chú: dải tiện ích trên header đang chạy chữ "LUÔN CÓ 7 NGÀY ĐỔI TRẢ MIỄN PHÍ" (setting policy_title_2) — vẫn mâu thuẫn chính sách 3/10 ngày, chờ anh sửa trong admin.

## 11/10/2026 ~14h20 — Phụ đề YouTube trên iPhone (SỬA THẲNG WEB THẬT 1170134, ly-home-main.bwt)
- Ảnh anh Công: iPhone hiện phụ đề kiểu CC YouTube (chữ trắng nền đen) — không phải chữ in trong video (đã soi khung gốc đoạn 9–22s: không có chữ). Trên Chrome máy tính của em tracklist trống → phụ đề do cài đặt trợ năng iPhone/tài khoản Google ghi đè cc_load_policy:0.
- Phát hiện thêm: mỗi lần seek YouTube hiện lớp UI ~4s (tiêu đề video, nút pause, More videos, logo) — chỉ thấy khi pointer/không ẩn; với cách tua khi lớp video đang ẩn + pointer-events:none thì không lọt.
- Lớp 1: killCC() = unloadModule('captions'/'cc') + setOption track {} + cc_lang_pref:'zz'; gọi ở onReady, onStateChange (1,3), onApiChange, mỗi lần toVideo.
- Lớp 2 (ccGuard): đọc getOption('captions','track'); có phụ đề → không cho hiện / ẩn tức thì (.is-cut, không mờ dần), gỡ lại mỗi 1,5s; >3 lần → giveUp(): destroy player, gỡ lớp video + nút Khám phá, chỉ còn banner + nút Sản phẩm.
- Đã thử & bỏ: phóng video neo trên để đẩy vùng phụ đề ra ngoài (chỉ hiện 70% trên) → trên điện thoại chỉ còn bức tường, người mẫu bị cắt.
- Đã kiểm bằng giả lập (patch getOption trên player thật, 375px): (a) phụ đề tắt sau 1 lần gỡ → ẩn 0,25s rồi hiện lại 0,76s; (b) phụ đề không tắt → ẩn trong ≤0,5s, gỡ video sau 4,3s, banner + nút Sản phẩm, nút Khám phá bị gỡ.
- CHƯA kiểm trên iPhone thật: nếu iPhone không báo track qua getOption mà unloadModule cũng không ăn → phụ đề vẫn có thể hiện. Giải pháp tuyệt đối còn lại: tự host MP4 (không có phụ đề) — anh Công đã tạm gác.

## 11/10/2026 ~14h15 — Bỏ banner poster ưu đãi trên điện thoại (SỬA THẲNG WEB THẬT 1170134, assets/ly-home-mid.css)
- ≤767px: .lym-poster{display:none!important}; bỏ gap/order cũ. Khối ưu đãi mobile = thanh tiêu đề → hàng vuốt → chấm, cao 450px (trước ~636px). Ảnh poster không bị tải trên điện thoại (loading=lazy + display:none, đã kiểm resource list).
- PC 1280: poster vẫn 330×440, khối 474px. Tablet 768–1023 giữ poster dọc như cũ.
- File ly-sale-poster-mb.jpg không còn cần (markup <picture> vẫn để, vô hại).

## 11/10/2026 ~14h25 — Khối ưu đãi tablet 2 cột như PC (SỬA THẲNG WEB THẬT 1170134, assets/ly-home-mid.css)
- Thêm @media(min-width:768px) and (max-width:1023px) sau khối ≤1023: .lym-sale hàng ngang, poster 36% căn giữa dọc, thanh đen margin-left 6% tràn mép phải (bo trái), hàng sản phẩm vuốt ngang thẻ 44% + mũi tên 38px + chấm trắng; nút thẻ 34px chữ 10px.
- Đo: 768px → khối 705×449, poster 248×331, thẻ 177×275, tiêu đề 1 dòng; 900px → khối 837×486, poster 296×394, thẻ 214×305; 1023px → khối 960×516, poster 340×453, thẻ 249×335. Không tràn ngang. PC (≥1024) và điện thoại (≤767) không đổi.

---

## PHẦN 3 — NHẬT KÝ CHI TIẾT 09–10/10 (nguyên văn `claude/CURRENT_STATUS.md`)

> Lưu ý: các dòng về "theme chính hiện tại" trong phần này đã lỗi thời — xem Phần 2.

# CURRENT STATUS — louisyoga.vn (cập nhật 10/10/2026, ~17h)

## ⭐⭐ 10/10/2026 17:15 — THEME CHÍNH HIỆN TẠI: **1170160 "Louis Yoga (Bản mới"** (anh Công tạo + xuất bản trong admin)
- Lý do: sau khi em xuất bản 1170134 qua API (16:58), máy tính thấy 1170134 nhưng **điện thoại vẫn nhận theme cũ 1151386** (kiểm bằng UA Android, URL chống cache). API không đổi được (`role: mobile` → 422). Anh Công xử lý trong admin → main mới 1170160; 1170134 về unpublished.
- Đã kiểm 17:15: UA Android và UA máy tính đều nhận 1170160 (/, /collections/all, LILIUM, /cart, /gioi-thieu: 200). 252 asset đầu danh sách so với 1170134: cùng tên, cùng dung lượng (danh sách API bị cắt ở ~252 file nên chưa so phần còn lại, nhưng dấu hiệu trang sản phẩm/danh mục/giới thiệu/giỏ đều đủ: ly-pdp, ly-pd-info, nhãn Phân khúc, Google Fonts, favicon, ly-segments, ly-filter, ly-cart, ly-about). Trang chủ mobile 375px: 3 khối mới, 4 ảnh JPG tải đúng, không tràn ngang, hiệu ứng chạy.
- **1170134 giờ unpublished và giống bản live → dùng 1170134 làm bản sửa tiếp** (hoặc theo chỉ định mới của anh Công). Mọi lần ghi 1170160 = sửa web thật.
- Bài học: xuất bản qua API chỉ đổi theme cho máy tính; **xuất bản phải làm trong Sapo admin** để áp dụng cả điện thoại. Sau xuất bản luôn kiểm bằng UA điện thoại.

## ⭐ 10/10/2026 16:58 — ĐÃ XUẤT BẢN theme **1170134 "Louis Yoga (Bản mới - Edit chỉnh sửa)"** = THEME CHÍNH (main) theo yêu cầu anh Công
- Xuất bản qua API `PUT themes/1170134.json {"role":"main"}`; đã kiểm list_themes: 1170134 main, 1151386 "(Không sửa ở đây)" chuyển unpublished.
- Trước khi xuất bản đã kiểm 6 trang trên bản xem trước (/, /collections/all, LILIUM, NATURE, /cart, /gioi-thieu) trả 200; sau xuất bản /, /collections/all, LILIUM, /cart nạp asset theme 1170134, 4 ảnh JPG tải đúng.
- Lần xuất bản này đưa lên web thật mọi thứ trước đó "chờ anh xuất bản" trong 1170134: 3 khối giữa trang chủ + hiệu ứng ưu đãi, phân khúc Harmony/Balance/Mastery (menu, chip, bộ lọc, trang SP), tối ưu ảnh gallery + font Google.
- ⚠ Từ giờ 1170134 LÀ WEBSITE THẬT: ghi file cần `allow_live_theme=true` + anh Công đồng ý từng việc. Nên tạo bản copy mới của 1170134 làm nơi sửa tiếp. Muốn quay lại bản cũ: xuất bản lại 1151386 (giữ nguyên, chưa xoá).
- Thanh "Bạn đang xem thử giao diện" vẫn hiện trên trình duyệt từng mở link preview (cookie phiên) — bấm "Hủy xem thử", khách không thấy.

## 10/10/2026 ~17h — 3 khối giữa trang chủ theo PDF "Bản edit trang chủ" (chỉ theme 1170134, chưa xuất bản)
- File mới: `snippets/ly-home-mid.bwt` (markup + CÀI ĐẶT khối ưu đãi ở đầu file), `assets/ly-home-mid.css` (biến trong :root, chỉ Flexbox, tiền tố `.lym`), `assets/ly-home-mid.js` (đếm ngược, tab, phân trang).
- `snippets/ly-home-main.bwt`: thay 3 section cũ (ly-sale-section, ly-mats, ly-accessories) bằng `{% include 'ly-home-mid' %}`. Bản trước: `snippets/zz-backup-ly-home-main-1010b.bwt` (8683 ký tự, khớp nguyên văn). Hoàn tác = chép backup về ly-home-main.bwt.
- `snippets/ly-segments.bwt`: thêm `ly_seg_descs` (Harmony dành cho người mới tập · Balance … người tập đều · Mastery … người tập chuyên nghiệp).
- Ưu đãi: khung hồng bo góc 1040px; trái poster 3:4 (`assets/ly-sale-poster.jpg`, 1200×1600); phải thanh đen sát mép phải (tiêu đề settings.ly_home_sale_label/title, mặc định "ƯU ĐÃI LOUIS YOGA / Sản phẩm ưu đãi") + 4 thẻ từ settings.section_deal_product, nhãn đỏ trên thẻ = "GIẢM x%" tính từ giá gốc/giá bán thật (LILIUM/NATURE/DIAMOND 17%, QUEEN 19%); có thể ghi đè bằng `lym_vouchers`.
  - Đồng hồ đếm ngược CHỈ hiện khi có settings.ly_home_sale_end (hiện trống → ẩn). Đã bỏ ngày mặc định 01–30/10 cũ (không phải lịch chiến dịch thật).
  - Poster chỉ thành link khi settings.ly_shopee_url có URL chứa "shopee" (hiện chưa có → poster không bấm được). Site hiện không có link Shopee nào.
- Khung xám bo góc chung: YOGA MAT/LOUIS YOGA giữa → banner 4:1 (`assets/ly-seg-{harmony|balance|mastery}.jpg` 1600×400, bấm → trang phân khúc) → tab (mặc định Balance) → mô tả nghiêng → 4 thẻ → kẻ hồng 2px → "PHỤ KIỆN LOUIS YOGA" 1 dòng căn trái + gạch + "Phụ kiện và dụng cụ hỗ trợ tập yoga" → 4 phụ kiện/trang (settings.url_1_all2pro, tối đa 48) → phân trang (hiện 10 SP = 3 trang). Bỏ banner người mẫu dọc, lưới 2×2, link "Xem tất cả".
- Mobile ≤767: 2 thẻ/hàng (phụ kiện 2×2 mỗi trang), poster tối đa 400px giữa; 768–1023: xếp dọc, 4 thẻ/hàng.
- Đã kiểm preview 1440/1188/375px: tab đổi banner+mô tả+SP, phân trang 1/2/3 + ‹ ›, hộp chọn phân loại mở, tim yêu thích bật/tắt, không tràn ngang, không lỗi JS. Không bấm thêm giỏ/mua thật.
- 4 ảnh: Sapo không nhận WebP qua admin → anh Công đổi sang JPG và tải lên 1170134 (poster 384KB, banner 141–189KB). Đã đổi snippet sang .jpg; đã kiểm 4 ảnh tải đúng, poster 330×440 (3:4), banner 879×220 (4:1) ở 1280px, đổi tab đúng ảnh.
- 10/10 ~17h15 — Hiệu ứng khối ưu đãi (anh Công thấy mờ nhạt): nền 6 hàng chữ SALE viền mờ xoay -9°, chạy ngang ngược chiều xen kẽ (48s/56s); tiêu đề thanh đen có ánh sáng hồng lướt (4,5s); dòng phụ "thở" nhẹ (3,2s); vệt sáng quét thanh đen (5s) và nhãn giảm giá (4s, lệch nhịp từng thẻ); đồng hồ lắc khi có đếm ngược. Chỉ chạy khi khối trong màn hình (IntersectionObserver gắn .is-live), tắt hết khi prefers-reduced-motion. Nhãn "GIẢM x%" đổi từ đỏ #ed1c24 (chói trên nền hồng) sang đỏ rượu #4a202c chữ trắng (biến --lym-vch-bg).
- Mẹo kiểm mobile trên trình duyệt tích hợp: preset "mobile" đổi user-agent → Sapo bỏ previewThemeId (hiện theme live). Cách đúng: tải preview ở desktop rồi resize 375 (không tải lại).
- Các file cũ không còn được gọi trên trang chủ nhưng vẫn để: CSS `.ly-sale/.ly-mats/.ly-accessory-track` trong ly-home.css/ly-design.css, JS đếm ngược `.ly-cd` (ly-design.js), carousel/data-tabs (ly-home.js) — tự bỏ qua vì không còn phần tử.

## 10/10/2026 ~14h25 — Favicon (sửa cả theme đang chạy 1151386 theo yêu cầu rõ của anh Công + đồng bộ 1170134)
- Nguyên nhân tab trang chủ hiện quả địa cầu: nhánh `{% if template contains 'index' %}` của `layouts/theme.bwt` không có thẻ favicon; các trang con dùng `favicon.png` (logo cũ có chữ, nền xám) và chỉ khi `settings.favicon_enable`.
- Mới: `snippets/ly-favicon.bwt` — favicon SVG hoa sen (lấy từ logo SVG mới, nền trắng bo góc, data URI ~7,9KB, sha256 đầu 82156a023c1e3de2) + `favicon.png` làm dự phòng (sizes 32x32, cho Safari) + `apple-touch-icon` = favicon.png.
- `layouts/theme.bwt` (cả 2 theme): thêm `{% include 'ly-favicon' %}` vào head trang chủ; ở head trang con thay dòng `{%if settings.favicon_enable%}…favicon.png…{%endif%}` bằng include.
- Đã kiểm: /, /collections/all, trang sản phẩm MOON trên 1151386 và 1170134 trả 200, có 3 thẻ icon, mã băm data URI khớp.
- Hạn chế: Safari (Mac/iPhone) vẫn hiện favicon.png cũ vì không hỗ trợ favicon SVG; muốn đồng bộ cần anh tải lên favicon.png mới (PNG vuông, ≥180×180, chỉ hoa sen) qua Sapo admin (API không ghi được file ảnh).

Lịch sử: **1151386 "Louis Yoga 26-12 - Copy" — ĐÃ ĐƯỢC ANH CÔNG XUẤT BẢN THÀNH THEME CHÍNH (10/10 ~14h)**. Theme cũ 983840 giờ là unpublished; 1170085 "Louis Yoga 26-12 (Đang sử dụng)" unpublished (có thể là bản lưu). ⚠ Mọi lần ghi giờ là sửa trực tiếp website thật: `put_theme_asset` cần `allow_live_theme=true` và phải có anh Công đồng ý rõ ràng cho từng việc (10/10 anh đồng ý cho việc sửa ô tích bộ lọc).

## 10/10/2026 ~14h05 — Ô tích bộ lọc đồng bộ (sửa trên theme đang chạy, anh Công đồng ý)
- `assets/ly-tweaks.css`: mọi `.ly-filters input[type=checkbox]` cùng cỡ 14×14 (box-sizing border-box, viền 1.2px #8a8a8a, hover viền hồng, dấu tích 4×7) giống ô ở mục Đánh giá; bỏ rule riêng `.ly-rate-opt input` 14px. Trước đó ô thường đặt 18px nhưng hiển thị 20×20.
- Đã kiểm louisyoga.vn/collections/all 1280px: tất cả ô 14×14, thẳng hàng. Hoàn tác: đổi lại 14px → 18px ở rule `.ly-filters input[type=checkbox]`.

## 10/10/2026 chiều — Khối Chi tiết / Bảo quản / Vận chuyển và đổi trả (PC + mobile)
- `snippets/tab_product.bwt`: viết lại phần `.ly-pd-info` (thêm class `.lyi`), nạp `assets/ly-pd-info.css` (mới). Giữ `#content`, `.rte.product_getcontent`, phần tự đóng `<style>`, đánh giá, sản phẩm tương tự như cũ.
- Mô tả sản phẩm: chữ Inter 15px/1.75 (mobile 14.5px) màu #3d3739; tiêu đề h2 Montserrat 18px (mobile 16px) đỏ rượu + gạch hồng bên trái; **ghi đè style dán tay trong mô tả** (span `color:#ff00cc`, `font-size:22px`, `text-align:justify`); danh sách chấm hồng; ảnh bo 12px. Mô tả dài tự thu gọn 620px (mobile 460px) + nút "Xem thêm / Thu gọn" (JS nội tuyến cuối section, chỉ hiện khi dài hơn giới hạn +180px).
- Tiêu đề mở/đóng: Montserrat 700 16px đỏ rượu, chữ thường, mũi tên trong vòng tròn hồng nhạt; bỏ kiểu in hoa nhỏ cũ.
- **Vận chuyển và đổi trả**: không chép nguyên trang chính sách nữa → bản tóm tắt viết tay `snippets/ly-pd-policy.bwt`: 4 thẻ (Kiểm tra khi nhận · Lỗi SX/hư hỏng vận chuyển: đổi mới 10 ngày, LY chịu 100% phí · Đổi theo nhu cầu: 3 ngày, chưa dùng, khách chịu phí 2 chiều · Không hỗ trợ), 3 bước đổi trả, ghi chú "mỗi đơn đổi 01 lần", nút gọi CSKH 0352 587 836 + link xem đầy đủ. PC lưới 2 cột (~505px cao), mobile 1 cột.
- Nguồn số liệu: /chinh-sach-bao-hanh-doi-tra-san-pham + /chinh-sach-kiem-hang (đọc 10/10). **Khi chính sách đổi → phải sửa tay ly-pd-policy.bwt.**
- ⚠ Mâu thuẫn dữ liệu trên site (chưa sửa, chờ anh Công chốt): trang bảo hành ghi đổi theo nhu cầu **3 ngày** + khách chịu phí 2 chiều; trang kiểm hàng ghi **7 ngày**; dải cam kết (policy_title_2) ghi "**7 ngày đổi trả miễn phí**". Hotline CSKH trong chính sách 0352 587 836 khác hotline header 0888 293 996.
- Nền 2 màu lệch: `ly-pages.css` cũ đặt cho `.ly-pd-info` dải xám full-width bằng `box-shadow:0 0 0 1280px #f2f2f2` → `.lyi` tắt box-shadow/clip-path, nền trắng liền với khối Đánh giá (PC + mobile).
- Đã kiểm preview: MOON 1280px & 375px, Xem thêm/Thu gọn, không tràn ngang; hàng "Vận chuyển ›" của bản mobile Shopee vẫn mở đúng mục.

## 10/10/2026 chiều — Trang sản phẩm bản mobile kiểu Shopee (≤767px)
- Lý do: anh Công muốn khách thao tác mua quen tay như app Shopee (tham chiếu ảnh chụp Shopee/Welcare; không mở Figma).
- File mới: `snippets/ly-pdp-mobile.bwt` (mẫu HTML trong `<template id="lyp-tpl">` + nạp CSS/JS), `assets/ly-pdp.css`, `assets/ly-pdp.js` (tiền tố `.lyp`). `snippets/tab_product.bwt`: chỉ thêm 1 dòng `{% include 'ly-pdp-mobile' %}` sau dòng đầu. **Không sửa `templates/product.bwt`.**
- Hoàn tác: xoá dòng include trong tab_product.bwt (3 file mới để lại cũng vô hại).
- Bố cục mobile: ảnh tràn viền vuông + bộ đếm "1/N" (ẩn dải ảnh nhỏ) → nhãn "Chính hãng" + tên → giá hồng 22px, giá gốc gạch, nhãn -% → hàng sao + "4,7 · 3 đánh giá" + tim yêu thích + chia sẻ → lưới 2×2 cam kết (policy_title_1..4) → hàng "Phân loại: <màu> · N lựa chọn ›" và "Vận chuyển: Miễn phí vận chuyển đơn từ <free_shipping_price> ›" (bấm mở mục Vận chuyển và đổi trả) → khung thông số → nội dung cũ.
- Thanh cố định đáy 56px: Chat Zalo (settings.social_zl) | Thêm vào giỏ | Mua ngay (1:1:2). Sản phẩm hết hàng: 2 nút mua bị khoá "Tạm hết hàng". Sản phẩm mọi biến thể 0đ: Gọi ngay + "Liên hệ báo giá".
- Bảng chọn trượt từ dưới (bottom sheet): ảnh, giá, nhãn %, tình trạng, ô màu + số lượng **gốc** (được dời vào bảng, vẫn nằm trong form, có mốc comment để trả về chỗ cũ khi màn hình >767px), nút xác nhận gọi `.btn_add_cart` / `.btn-buyNow` gốc → giữ nguyên luồng giỏ trượt & /checkout cũ. Mở từ "Phân loại" = 2 nút; từ thanh đáy = 1 nút tương ứng.
- Nút Zalo/gọi nổi đẩy lên (bottom 70px / 138px), ẩn khi mở bảng chọn.
- Số đánh giá lấy từ `product.metafields.bpr.votes/rating` — **`data-number` của app đánh giá là số sao tối đa (5), không phải số lượt**.
- Sửa kèm lỗi code cũ (mọi kích thước màn hình): biến thể không có giá gốc (vd. NATURE Cafe) vẫn giữ nhãn "-17%" của biến thể trước → JS ẩn nhãn khi giá gốc ẩn.
- Đã kiểm preview 375px: NATURE (chọn Cafe → biến thể 212264285, nhãn % ẩn/hiện đúng), LILIUM (ô hết hàng → 2 nút "Tạm hết hàng"), Bình giữ nhiệt (1 biến thể, ẩn hàng Phân loại), ghế hết hàng (thanh đáy khoá); tim yêu thích bật/tắt; không tràn ngang. Desktop 804px: mọi phần tử trả về chỗ cũ, không hiện thanh/bảng. Không bấm Thêm vào giỏ / Mua ngay thật.
- Còn tồn / cần anh duyệt: nhãn "Chính hãng" là chữ em thêm; dòng miễn phí vận chuyển dựa trên cài đặt theme (600.000đ) chưa đối chiếu phí ship thật; chưa thử trên iPhone thật (safe-area, chia sẻ native); ô Zalo/gọi nổi vẫn chồng một phần nội dung bên phải khi cuộn.

## Đã làm phiên 10/10 — Cân lại menu header
- Menu: chữ 12px→11.5px, giãn 1.6→1.3px, đệm 12→10px; `.lyh-grid` thêm `column-gap:clamp(24px,4vw,64px)`; bậc thu nhỏ mới ≤1360px (11px), ≤1240px, ≤1080px (10.5px).
- Mũi tên "Cửa hàng" vẽ lệch thành "⌐" → ép `fill:none`, nét 2.2 bo tròn, 11px.
- Đo khoảng cách "Liên hệ" → logo: ≥1366px: 78px (ghim 106px); 1280px: 113px; 1100px: 42px (trước ~20px ở 1347px).
- Kích thước banner trang chủ đã đo cho anh Công thiết kế: banner dọc YOGA MAT 376×790 (xuất 752×1580; mobile 343×446 neo trên → đề xuất bản mobile 686×892); 2 banner ngang 548×255 (xuất 1096×510; mobile 166×123 cắt giữa, vùng an toàn ~690px giữa; chừa góc trái dưới ~460×130 cho nút phủ). (Banner dọc YOGA MAT đã bỏ từ 10/10 17h.)

## Đã làm phiên 10/10 — Logo SVG + sửa khoảng cách thanh ghim
- Logo mới từ file SVG anh Công gửi (Illustrator, khung 612×792): cắt viewBox sát hình — bản đầy đủ `172 292 270 206`, bản chỉ hoa sen `174 294 266 158` (bỏ 9 nét chữ class st16).
- Lưu dạng **SVG nhúng** trong `snippets/ly-logo-svg.bwt` (dùng: `assign logo_id` duy nhất + `logo_mark` true/false, rồi include). Class/id trong SVG được đổi tiền tố theo logo_id → không trùng id, không đụng CSS trang. Đã kiểm hash nội dung render = file gốc (full 5f116e79…, mark d2957987…).
- Lý do không dùng file .svg: API theme Sapo coi .svg là nhị phân → `put_theme_asset` (văn bản) tạo file 0 byte. **Còn sót `assets/ly-logo.svg` 0 byte, vô hại, chưa xoá (chờ anh Công đồng ý).**
- Header: bản đầy đủ 64px (mobile 50px); khi ghim chuyển mượt sang bản hoa sen 38px (mobile 30px). Menu mobile: logo đầy đủ 46px. Footer: `.ly-foot-logo` 92px (mobile 76px), nền trong suốt. Không còn trang nào dùng `ly-logo.png`.
- Thanh ghim sát mép trên: nguyên nhân margin-top của `.lyh-bar` bị gộp lề (margin collapse) ra ngoài khung sticky → thêm `display:flow-root` cho `.lyh`; khoảng cách `--lyh-gap` 16px (mobile 10px). Đo desktop: thanh cách mép 16px.
- Sự cố trong phiên: đã ghi đè `templates/page.test.bwt` để thử logo khi chưa sao lưu → đã khôi phục nguyên văn từ theme main 983840 (435 byte, giống bản copy gốc), bản sao ở `snippets/zz-backup-page-test.bwt`. Mẹo: `/<trang>?view=test` gọi template page.test.

## Đã làm phiên 10/10 — Header mới, ghim toàn site
- Mẫu tham chiếu anh Công gửi: Dragonfly Ave (dải tiện ích mảnh, chữ in hoa giãn, logo giữa), Market (hotline, giỏ hàng nổi bật), Solarsphere (thanh điều hướng viên thuốc kính mờ).
- `snippets/ly-home-header.bwt` viết lại (gốc: `zz-backup-ly-home-header.bwt`) + `assets/ly-header.css` (tiền tố `.lyh`, nạp bằng <link> trong snippet). JS nội tuyến trong snippet.
- Bố cục: dải tiện ích đỏ rượu 38px (trái: chạy luân phiên `settings.policy_title_1..4`; phải: Hotline số đầu của `store_phone`, Đăng ký CTV, Bảo hành, Nhận ưu đãi, Zalo/FB/YT) → thanh chính 92px: menu chữ in hoa giãn bên trái, logo hoa sen giữa, tìm kiếm + tài khoản + yêu thích + giỏ bên phải; viền gradient hồng dưới.
- Ghim: wrapper `.lyh` sticky, chiều cao cố định (không giật nội dung); khi qua sentinel → `.is-stuck`: thanh thu thành viên thuốc kính mờ 66px (mobile 56px), logo 46px (mobile 38px). Dải tiện ích cuộn đi.
- Menu Cửa hàng: hover/click/bàn phím, Esc đóng. Mobile ≤991px: hamburger + logo giữa + tìm/yêu thích/giỏ; menu trượt trái có nút Gọi + Chat Zalo; ô tìm kiếm thả xuống.
- Giữ móc JS cũ: data-cart-open/count, data-favorites-open/count (đã kiểm mở giỏ trượt & yêu thích). Không còn `.ly-header`, `.ly-topbar`, `.ly-menu-toggle`, `#ly-nav`.
- Bù chỗ header ghim: `html{scroll-padding-top:112px}` (mobile 84px); khung ảnh trang sản phẩm `top:100px`; khối tóm tắt giỏ hàng `top:100px` (≥992px).
- Đã kiểm preview 1440px & 375px: trang chủ, sản phẩm LILIUM (Swiper còn sống), danh mục, giỏ; không tràn ngang; 39 file theme tải 200.

## Đã làm phiên 10/10 — Footer & nút liên hệ nổi
- Đối chiếu theme main 983840 và copy: nút nổi giống nhau (nút gọi `.addThis_listSharing` tel:0888293996 + widget Zalo OA `.zalo-chat-widget` oaid 1276642695529333922). Không theme nào có chat Messenger/live chat khác. Trên link preview, thanh "Bạn đang xem thử giao diện" (68px) che nửa nút Zalo — chỉ có ở chế độ xem thử.
- Phần thiếu thật: footer mới (`snippets/ly-home-footer.bwt`, gốc: `zz-backup-ly-home-footer.bwt`) không có icon Zalo/Facebook/YouTube và số điện thoại không bấm gọi được → đã thêm (link từ settings.social_zl/fb/you/insta; tách số theo dấu "-" thành từng link tel:).
- Instagram ẩn nếu link không chứa "instagram" (settings.social_insta hiện trỏ nhầm sang Facebook).
- Mobile ≤767px: Zalo `right:14px bottom:18px`, nút gọi `right:22px bottom:88px` → 1 cột, hết chồng nhau (CSS trong <style> của footer).

## Đã làm phiên 10/10 — Thiết kế lại trang Giới thiệu (`/gioi-thieu`)
- `templates/page.about.bwt` viết lại (gốc: `snippets/zz-backup-page-about.bwt`; 4 snippet cũ `about-us/video/giatri/banner` giữ nguyên, không còn được gọi). Hoàn tác = chép nội dung bản backup về page.about.bwt.
- Mới: `snippets/ly-about.bwt` (markup + JS hiện dần & popup video `<dialog>`), `assets/ly-about.css` (mọi selector tiền tố `.lya`).
- Nội dung vẫn lấy từ cài đặt theme như cũ (title_about1/2, content_about, *_faq_about1–4, title/content_video, id_video, title/content_giatri, title_banner, alt_bn/ena_bn, ảnh about/video/giatri/image_bn_*.png).
- Bố cục: Hero (H1 + câu đầu content_about + nút "Khám phá sản phẩm"/"Xem câu chuyện", ảnh about.png, nhãn "2015") → dải số liệu nền đỏ rượu (số năm tính tự động từ 2015, số giải thưởng đếm từ ena_bn) → "Về Louis Yoga" 2 cột → Giá trị cốt lõi lưới 2×2 (trước là accordion ẩn) → Sứ mệnh + video → Văn hoá Việt (trích dẫn) → lưới 4 giải thưởng (trước là slider) → khối kêu gọi nền đỏ rượu.
- Chữ mới do em thêm (UI): nhãn nhỏ "Định hướng phát triển", "Ghi nhận & uy tín", chú thích dải số liệu, khối kêu gọi "Bắt đầu hành trình yoga cùng Louis Yoga" + 1 câu mô tả. Link nút: /collections/all, /lien-he (chưa kiểm /lien-he tồn tại).
- Đã kiểm preview 1440px & 375px: không tràn ngang, video mở đúng id b8s5AYDkUqI, 4 thẻ giá trị + 4 giải thưởng hiển thị.
- Dữ liệu cần anh sửa trong Tuỳ chỉnh giao diện: "Top Brands ASIA FACIFIC" → "PACIFIC" (lỗi chính tả).

## Đã làm phiên 10/10 sáng — Ô chọn màu trùng / màu không bán
### Nguyên nhân (đã xác minh qua `/<alias>.js` công khai, API sản phẩm vẫn 403)
- NATURE (11 biến thể): 4 biến thể **giá 0đ**, không ảnh, không giá gốc — Xanh coban, Tím huế, TÍM HUẾ, TRẮNG; cặp trùng `Xanh Đậm` / `Xanh  Đậm` (2 dấu cách, cả hai có giá & tồn kho 46 / 13).
- LILIUM (8 biến thể): 2 biến thể 0đ — Ghi khói, GHI KHÓI (tồn 18 / 2); Xanh Cốm, Tím Huế, Ghi Đậm hết hàng.
- Mã cũ (`swatch.bwt`, `ly-home-card.bwt`) vẽ mọi biến thể, chỉ loại trùng khi tên giống y hệt; ô hết hàng không có kiểu riêng; tên màu `capitalize` không hạ chữ in hoa.
### Sửa trên theme
- `snippets/swatch.bwt` (gốc: `snippets/zz-backup-swatch.bwt`): ẩn biến thể 0đ khi sản phẩm còn biến thể có giá; gộp tên trùng theo `strip + gộp dấu cách + handle`; trong nhóm trùng ưu tiên biến thể còn hàng; tên hiển thị `downcase` (CSS viết hoa chữ đầu), giá trị gửi đi giữ nguyên; ô hết hàng mờ 45%, viền nét đứt, gạch tên (CSS nội tuyến trong snippet); link cũ `?variant=<id bị ẩn>` tự chuyển về ô đầu tiên còn hàng.
- `snippets/ly-home-card.bwt` (gốc: `snippets/zz-backup-ly-home-card.bwt`): cùng quy tắc cho danh sách hộp chọn nhanh `.ly-pick`; giá thẻ lấy biến thể có giá nếu biến thể mặc định là 0đ; nếu mọi biến thể có giá đều hết → thẻ "Hết hàng".
- Sản phẩm mà **mọi** biến thể đều 0đ (hàng "Liên hệ") giữ hành vi cũ.
### Đã kiểm trên preview
- NATURE: 6 ô (Trắng, Xanh Đậm, Nâu, Xanh Rêu, Đỏ, Cafe); bấm CAFE → đúng biến thể 212264285; `?variant=213040550` (TRẮNG 0đ) tự về "Trắng" có giá, nút mua hiện; `galleryThumbs` còn sống.
- LILIUM: 6 ô, 3 ô hết hàng mờ/gạch; hộp chọn nhanh ở /collections/all đúng 6 lựa chọn, 3 cái khóa "(hết hàng)".
### Còn tồn
- Dòng tiêu đề "Màu sắc: XANH RÊU" vẫn hiện nguyên chữ in hoa của dữ liệu (chưa đổi).
- Biến thể `Xanh  Đậm` (NATURE-M03, tồn 13) không còn chọn được trên web vì bị gộp vào `Xanh Đậm` → cần gộp tồn kho trong admin.
- Ô màu bản mobile: đã xem trong bảng chọn trượt mới (10/10 chiều), hiển thị ổn.

## Cần anh Công sửa trong Sapo admin (API 403)
- Mô tả NATURE: thêm `</style>` cuối hoặc xoá khối `<style>` dán vào.
- NATURE: gộp/xoá biến thể trùng "Trắng"/"TRẮNG", "Tím huế"/"TÍM HUẾ", "Xanh Đậm"/"Xanh  Đậm"; đặt giá hoặc xoá biến thể 0đ (Xanh coban, Tím huế, TÍM HUẾ, TRẮNG).
- LILIUM: "Ghi khói"/"GHI KHÓI" giá 0đ nhưng còn tồn 20 → nếu đang bán thì đặt giá (web sẽ tự hiện lại ô), nếu không thì xoá.
- Thống nhất cách viết hoa tên màu giữa các sản phẩm.

## Đã làm trong phiên 09/10 tối
### Giỏ hàng (làm lại toàn bộ)
- `templates/cart.bwt` viết mới (bản gốc lưu ở `snippets/zz-backup-cart.bwt` + theme 983840).
  - Bố cục 2 cột: danh sách sản phẩm (ảnh, phân loại, bước số lượng, xóa có Hoàn tác) + khối Tóm tắt đơn (thanh freeship theo `settings.free_shipping_price`, tạm tính, giảm giá, tổng).
  - Mục mở/đóng: Thời gian giao hàng (input date + khung giờ từ `settings.delivery_time`), Xuất hóa đơn công ty (kiểm tra MST 10/13 số, email).
  - Thuộc tính đơn giữ đúng tên cũ: "Xuất hóa đơn", "Tên công ty", "Mã số thuế", "Địa chỉ công ty", "Email nhận hóa đơn", "Thời gian giao hàng". Định dạng giờ giao đổi thành `dd/mm/yyyy - <khung giờ>`.
  - Khối "Có thể bạn cần thêm": 4 thẻ `ly-home-card` từ danh mục phụ kiện (`settings.url_1_all2pro`), bỏ sản phẩm đã có trong giỏ.
  - Điện thoại: thứ tự Danh sách → Tóm tắt → Gợi ý; thanh Tổng + Thanh toán cố định đáy; đẩy nút Zalo/gọi lên.
- Giỏ trượt mới `snippets/ly-cart-drawer.bwt` (dùng chung mọi trang). `assets/ly-cart.js` + `assets/ly-cart.css`. `ly-home.js` sửa `drawCart` để giao cho `window.LYCart`.
- Trang chi tiết sản phẩm: nút "Thêm vào giỏ hàng" (code cũ) đóng popup cũ `#popup-cart-mobile` và mở giỏ trượt mới.

### Các trang không có thiết kế — `assets/ly-pages.css`
- Đầu trang `.ly-page-heading` thống nhất (gradient, căn giữa, ẩn breadcrumb), chip Tin tức hồng, ô tìm kiếm bo tròn, bài viết/sidebar nhẹ, thẻ đăng nhập 440px, sửa nút 404.

### Bộ lọc danh mục mượt
- `assets/ly-filter.js` viết lại (bản cũ: `assets/ly-filter-v1.js`): thay `window.doSearch` bằng `lySearch` (fetch + AbortController), không phủ loading toàn trang, giữ min-height, thẻ hiện lần lượt (tự gỡ sau 1s, tắt khi tab ẩn), chỉ cuộn mượt khi lưới đã trôi khỏi màn hình, dải chip mở/đóng mượt, lọc sao tải song song.
- `ly-pages.css` mục 7: chuyển động bộ lọc, hover thẻ, tab trang chủ mờ dần (tôn trọng prefers-reduced-motion).
- Layout: CSS giao diện mới nạp trong `<head>` (hết nháy), vẫn nạp lại lần 2 cuối body để giữ thứ tự ưu tiên sau CSS cũ của footer_script.

### Khung "Đánh giá của khách hàng" theo thiết kế (trang sản phẩm)
- Dữ liệu vẫn từ app đánh giá Sapo (`#sapo-product-reviews`); `assets/ly-reviews.js` (nạp từ `snippets/tab_product.bwt`) sắp xếp lại giao diện bằng MutationObserver.
- Điểm lớn + 5 thanh phân bố sao (bấm để lọc qua input gốc của app) + nút vàng "Viết đánh giá"; tab "Đánh giá (N)"; mỗi đánh giá avatar chữ cái | sao + nội dung; "XEM THÊM" nối trang sau.
- CSS ở `ly-pages.css` mục 8.
- KHÔNG làm (app không có dữ liệu): "Xác thực đã mua hàng", phân khúc/màu khách mua, tab "Đánh giá cửa hàng", sắp xếp, ảnh đại diện thật.

### Sửa trang NATURE (`/tham-tap-yoga-cao-su-cao-cap-nature`)
- **Nguyên nhân:** mô tả sản phẩm kết thúc bằng một thẻ `<style>` (CSS cho `.shorts-wrap`, nhúng YouTube Shorts) **không có `</style>`** → trình duyệt coi toàn bộ phần sau (gồm script của product.bwt) là CSS → không chạy selectCallback/Swiper.
- **Sửa trên theme:** `snippets/tab_product.bwt` tự đếm `<style` / `</style>` trong `product.content` và nối thêm `</style>` nếu thiếu.
- `ly-pages.css` mục 9: ẩn vòng tròn hồng cũ (`label::before/after`) ở swatch màu; khung ảnh sticky `top:24px`.
- Ghi chú product.bwt: `{% if product.price == 0 %}` → `contacts=true` → thêm `d-none` cho `.form-group` phía server khi có biến thể 0đ; chỉ JS selectCallback mới gỡ ra.

## Chưa kiểm/hạn chế
- Chưa bấm "Thanh toán" tới /checkout → luồng thuộc tính hóa đơn mới chỉ kiểm bằng code.
- Thanh freeship dựa trên cài đặt theme (600.000đ); cần đối chiếu phí ship thật trong Sapo.
- Chưa thử trên điện thoại thật; khối đánh giá bản mobile chưa xem bằng mắt.
- Các mục chờ từ trước giữ nguyên (link khóa học, tên/ngày sale, ảnh banner, nhóm lọc Tiêu chí/Phân khúc, lỗi dữ liệu LILIUM/loại sản phẩm).

## Ghi chú kỹ thuật (cho phiên sau)
- **Đọc/ghi file theme:** đọc bằng `sapo_request` GET `themes/<id>/assets.json`, query `{"key":"<đường dẫn>"}` (`get_theme_asset` vẫn lỗi, trả về danh sách file); ghi bằng `put_theme_asset` — **phải gửi toàn bộ nội dung file**. API sản phẩm/đơn hàng trả 403 → đọc dữ liệu sản phẩm qua `https://louisyoga.vn/<alias>.js` (công khai, có đủ biến thể/giá/tồn).
- **Ảnh lớn:** môi trường làm việc của Claude bị chặn mạng tới louisyoga.vn/bizweb CDN; ảnh > ~50KB không gửi base64 được trong 1 lệnh → nhờ anh Công tải lên qua admin.
- **Trình duyệt:** trình duyệt tích hợp của app Claude đã có phiên Sapo, mở được `?previewThemeId=…`.
- **Tab ẩn:** animation bị trình duyệt tạm dừng khi tab ẩn → mọi hiệu ứng vào cảnh phải bỏ qua khi `document.visibilityState==='hidden'` và có hẹn giờ ~1s tự gỡ class.
- **Thứ tự CSS:** CSS cũ (footer_script) nạp cuối body và dùng nhiều `!important` → khối mới ghi đè bằng selector đủ mạnh + `!important`, file ly-* nạp lần 2 cuối body. Theme cũ ép mọi `<button>` về font Montserrat 14px 400 bằng `!important` → nút mới phải khai `font` kèm `!important`.
- **Code cũ cần biết:** trang sản phẩm dùng `selectCallback` + `Bizweb.OptionSelectors`; ô màu đổi `.single-option-selector` theo `value` của radio → ô gộp phải mang đúng giá trị biến thể đại diện. Kiểm nhanh trang sản phẩm còn sống: `typeof galleryThumbs === 'object'`.
- **Mô tả sản phẩm có HTML dán tay** là nguồn lỗi tiềm ẩn: khi trang sản phẩm "hỏng lạ", kiểm `product.content` trước.

## File mới/sửa
- 10/10 ~17h (trang chủ giữa): snippets/ly-home-mid.bwt · assets/ly-home-mid.css · assets/ly-home-mid.js · snippets/ly-home-main.bwt · snippets/ly-segments.bwt · snippets/zz-backup-ly-home-main-1010b.bwt · assets/ly-sale-poster.jpg, ly-seg-harmony.jpg, ly-seg-balance.jpg, ly-seg-mastery.jpg (anh Công tải)
- 10/10 chiều (khối thông tin): snippets/tab_product.bwt · snippets/ly-pd-policy.bwt · assets/ly-pd-info.css
- 10/10 chiều: snippets/ly-pdp-mobile.bwt · assets/ly-pdp.css · assets/ly-pdp.js · snippets/tab_product.bwt (thêm 1 dòng include)
- 10/10: snippets/swatch.bwt · snippets/ly-home-card.bwt · snippets/zz-backup-swatch.bwt · snippets/zz-backup-ly-home-card.bwt
- 09/10: templates/cart.bwt · snippets/ly-cart-drawer.bwt · snippets/zz-backup-cart.bwt · snippets/tab_product.bwt · assets/ly-cart.css · assets/ly-cart.js · assets/ly-pages.css · assets/ly-home.js (drawCart) · assets/ly-filter.js · assets/ly-filter-v1.js (sao lưu) · assets/ly-reviews.js · layouts/theme.bwt

## 10/10/2026 — Hero trang chủ dùng ảnh banner (PC + mobile)
- `snippets/ly-home-main.bwt`: thay khối hero cũ (chữ + khối hình giả) bằng `<picture>`: PC `assets/ly-hero-pc.jpg` (2400×1146), mobile ≤767px `assets/ly-hero-mb.jpg` (875×1451). Ảnh full-width, giữ nguyên tỉ lệ (không cắt). H1 ẩn cho SEO. CSS nội tuyến tiền tố `.lyhb`.
- Nút "Sản phẩm Louis Yoga" phủ lên ảnh: PC tâm x 37,2% / top 71,5% (dưới "TỎA SÁNG"); mobile giữa / top 85,6% (dưới khối thảm, trên dải lụa — đổi từ 40,4% theo góp ý "hơi cao"). Nền chuyển màu hồng hiện khi ảnh chưa tải.
- Sao lưu khối hero cũ: `snippets/zz-backup-ly-home-hero.bwt`.
- Anh Công đã tải 2 file ảnh lên theme copy (đã xác nhận ảnh mobile 875×1451 tải đúng).

## 10/10/2026 — Sản phẩm yêu thích dạng giỏ trượt
- `assets/ly-site.js` (bản gốc: `assets/zz-backup-ly-site.js`, 5561 byte): hộp #ly-favorites được JS gắn class `ly-drawer ly-fav-drawer` → trượt phải giống giỏ hàng (dùng lại CSS ly-cart.css). Không sửa layouts/theme.bwt.
- Mỗi dòng: ảnh, tên, giá (lấy từ `/<alias>.js` khi mở hộp, bỏ biến thể 0đ, ưu tiên biến thể còn hàng), tim đỏ = bỏ lưu. Nút: 1 biến thể còn hàng → "Thêm vào giỏ" (/cart/add.js, rồi phát ly:cart-change); nhiều biến thể → "Chọn mẫu & mua" (link sản phẩm); hết hàng → "Tạm hết hàng" + "Xem sản phẩm".
- Chân: "Mua sắm tiếp" + "Xem giỏ hàng" (mở giỏ trượt). Trạng thái trống có icon tim + nút khám phá. CSS chèn bằng JS, tiền tố `.ly-fav-`.
- Đã kiểm trên preview: hiển thị, bỏ lưu, trạng thái trống, đếm số. Chưa bấm thử "Thêm vào giỏ" (không thao tác giỏ thật).

## 10/10/2026 — Link Facebook
- Trang đúng: https://www.facebook.com/thamlouisyoga (anh Công xác nhận). Cài đặt theme `settings.social_fb` đang là thamtapyogalouis (sai).
- `ly-home-header.bwt` + `ly-home-footer.bwt`: biến `ly_fb` — nếu setting còn chứa "thamtapyogalouis" thì tự thay bằng link đúng. Đã kiểm trang chủ / sản phẩm / liên hệ trên preview.
- Nên sửa gốc trong Sapo admin → Tùy chỉnh giao diện → Mạng xã hội → Facebook (cả theme main và copy). File settings_data.json 204KB nên không ghi qua API.

## 10/10/2026 tối — Chốt chính sách, favicon, tối ưu tốc độ
**Theme làm việc: 1170134 "Louis Yoga (Bản mới - Edit chỉnh sửa)". Theme live 1151386 "(Không sửa ở đây)" — chỉ ghi khi anh Công yêu cầu rõ.**
- Chính sách đã chốt: 3 ngày đổi trả theo nhu cầu (chưa sử dụng, khách chịu ship 2 chiều); 10 ngày đổi do lỗi sản phẩm (Louis Yoga chịu ship). `snippets/ly-pd-policy.bwt` đã đúng. Nhãn "Chính hãng" + dòng miễn ship: anh duyệt giữ.
- Favicon (cả 2 theme): icon hoa sen anh gửi → `assets/ly-favicon-32.png` (32×32) + `assets/favicon.png` (180×180), khai báo trong `snippets/ly-favicon.bwt` (include ở cả 2 nhánh head của `layouts/theme.bwt`). **Upload ảnh qua `sapo_request` PUT `themes/{id}/assets.json` body `{"asset":{"key":...,"base64":...}}` — trường "attachment" tạo file 0 byte.** (Chỉ khả thi với ảnh nhỏ.)
- Tối ưu (chỉ 1170134, chờ anh xuất bản):
  - Ảnh gallery sản phẩm dùng thumb `1024x1024` + srcset `grande`, ảnh thứ 3 trở đi lazy (`templates/product.bwt`); link lightGallery vẫn ảnh gốc. `tab_product.bwt`: ảnh trong mô tả `loading="lazy"`, JS "hâm" 2 slide kế khi vuốt.
  - `ly-pdp.js`: bảng chọn không còn tải ảnh gốc 4000px (dùng currentSrc, chỉ khi mở).
  - Font: bỏ @font-face Montserrat tự host trong `ly-home.css` (5 file ~100KB) và `ly-design.css` (Bold, ExtraBold) → Google Fonts biến thiên `snippets/ly-fonts.bwt` (include trong `ly-favicon.bwt` để không phải sửa layout). Font thực tải ~50–120KB thay ~700KB. Đã so dòng CSS với bản live: chỉ khác dòng @font-face.
  - Đo trang sản phẩm: ảnh ~3,8MB → ~1,1MB tổng trang (ghế tập). Gallery, biến thể, bottom sheet vẫn chạy.
- Chưa làm (rủi ro): reCAPTCHA ~350KB do form đăng ký nhận tin của Sapo chèn — để nguyên.
- Cần anh sửa trong admin: setting `policy_title_2` ("7 ngày đổi trả") → 3/10 ngày; trang `/chinh-sach-kiem-hang` còn ghi 7 ngày; trang Giới thiệu "FACIFIC"→"PACIFIC"; `social_fb` → https://www.facebook.com/thamlouisyoga; NATURE: biến thể trùng + biến thể 0đ + mô tả có `<style>` chưa đóng; LILIUM: "Ghi khói" 0đ (xoá/gộp biến thể là thao tác không hoàn tác — anh tự làm). Hotline 0352 587 836 vs 0888 293 996: chưa chốt.

## 10/10/2026 tối — Phân khúc Harmony / Balance / Mastery (chỉ theme 1170134, chờ anh xuất bản)
- Bảng chốt: Harmony = AURA, MOON, SUNFLOWER, ASANA · Balance = ASANA 25, BASIC, BASIC ZEN, QUEEN · Mastery = LILIUM, NATURE, DIAMOND, F23. Tên dùng "Mastery".
- **Nguồn duy nhất: `snippets/ly-segments.bwt`** — gán theo product.id (không khớp tên): 62337590 36960227 60686622 36960064 | 60763661 36960232 62353814 36960230 | 44128440 37606937 36960218 39620233. Biến thể tự kế thừa. `snippets/ly-seg-of.bwt` tìm phân khúc của `product`.
- Vì API collections/products/linklists trả 403 → **chưa tạo được danh mục Sapo**. Trang phân khúc = `/collections/all?q=id:((…))&page=1&view=grid` (bộ lọc Sapo trường `id` khớp đúng mã; `alias` khớp gần đúng nên KHÔNG dùng). col.js tự tích ô lọc từ URL → chạy cùng sắp xếp/phân trang/lọc khác.
- Sửa: `snippets/ly-home-header.bwt` (menu Cửa hàng desktop + mobile: Tất cả · Phụ kiện · Phân khúc thảm H/B/M kèm tên mẫu; bỏ 3 mục Thảm cao su/TPE/Cao cấp), `templates/collection.bwt` (chip Tất cả·Harmony·Balance·Mastery·Phụ kiện; class chờ `ly-qwait` tránh nháy), `snippets/aside-filter.bwt` (nhóm "Phân khúc" đầu tiên, chỉ hiện khi danh mục có SP phân khúc; "Loại sản phẩm" giữ riêng, ẩn loại không có SP đang bán — vd "Thiết bị hỗ trợ"), `snippets/ly-home-main.bwt` (3 tab YOGA MAT — đã thay bằng ly-home-mid từ 10/10 17h), `snippets/tab_product.bwt` (nhãn "Phân khúc X" trên tên SP, SP tương tự ưu tiên cùng phân khúc), mới `assets/ly-segments.js` (đánh dấu link đang xem, đổi H1 "HARMONY / LOUIS YOGA" khi xem 1 phân khúc).
- Chưa gán phân khúc: SUN, OCEAN, Du lịch, MINI, TPE9 (chờ anh quyết). Danh mục cũ tham-yoga-cao-su / tham-tpe / tham-cao-cap vẫn còn, chỉ không còn trên menu/tab.
- Cần anh làm trong admin (nếu muốn danh mục thật): tạo 3 danh mục Harmony/Balance/Mastery + gán 12 SP → báo em đổi link sang /collections/<handle>.

## 10/10/2026 16:20 — Khối phụ kiện lên trên banner CTV
- Trang chủ (1170134, chưa xuất bản): khối PHỤ KIỆN đã đưa lên TRÊN 2 banner CTV/Khóa học. Yêu cầu "Bản edit trang chủ" (việc dở lúc đó) → ĐÃ LÀM 10/10 ~17h, xem mục đầu file.
