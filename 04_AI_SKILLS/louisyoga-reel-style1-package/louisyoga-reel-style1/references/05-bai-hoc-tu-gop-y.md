# 05 — Bài học từ góp ý của chủ thương hiệu (theo thứ tự thời gian, 24/10/2026)

1. **Reel 2 (video có thẻ hồng in cứng)** — làm kiểu tài liệu: khung video phía trên + vùng đồ hoạ tối phía dưới, màu
   xanh chanh như video mẫu. → Duyệt nội dung; yêu cầu **đổi tone hồng** (không cần đúng 100% màu logo), **ảnh minh hoạ
   sát nội dung** (ảnh cao su thật, ảnh thảm đúng mẫu từ dữ liệu web), **nhạc nền hợp nội dung**.
2. **Reel 3 v1 (video 05, không bị che)** — chủ thương hiệu: video mới không bị che nên **hạn chế che toàn khung, ưu tiên
   hình tràn khung**; được tải thêm video Louis Yoga làm B-roll. → Ra phong cách full-bleed + đồ hoạ ở vùng trống.
3. **Reel 3 v2** — "bị lặp hiệu ứng nhiều nên nghe nhàm" → học SFX từ 2 video breakdown; giọng phải **dễ nghe, có độ
   ấm**; thứ tự âm lượng **giọng > SFX > nhạc nhẹ**. Lỗi: khối tím che số (thanh tăng lên phía trên) → sửa. Sơ đồ đầu
   gối hoạt hình → muốn **ảnh thật**.
4. **Reel 3 v3** — "SFX bé quá"; "ít lặp chứ không phải không cho lặp"; **hook còn chìm, cần ấn tượng hơn**; một số
   tiếng không hợp hiệu ứng; ảnh người quỳ "hời hợt" → **dùng ảnh sản phẩm có sẵn trong thư mục dữ liệu**.
5. **Reel 3 v4 (bản chốt)** — so sánh: **bố cục reel 3 tốt, SFX reel 2 vừa đủ và hợp lý hơn** → kết hợp: hình reel 3 +
   bộ tiếng/mật độ/độ to của reel 2. Đây là chuẩn của skill này.

6. **Reel 01 + 02 (26/10/2026, làm bằng skill này)** — hiệu ứng ổn, SFX "vừa đủ không quá nhiều" (0,37–0,51 tiếng/s
   nghe được); chọn ảnh và dòng thảm (Harmony/Balance/Mastery × 4 mẫu) đúng. Chưa ổn: **hình hơi mờ** (đo ra do nguồn
   livestream ~1 Mbps + filter mịn da → thêm khử khối + làm nét, render jpeg 95/crf 14); **edit 1 video quá lâu**
   (→ snap_cuts, build_stems, stills.py, kit/scenes.tsx); **B-roll cận quá, không rõ tư thế** (→ `mode: "fit"` toàn
   khung, được dùng video/ảnh trên mạng không dính logo hãng khác, ưu tiên toàn thân). Chỉ áp dụng cho video sau.

7. **Reel 03 + 04 (27/10/2026)** — "lạm dụng video không phải của Louis": mỗi video dùng 3–4 clip Pexels làm B-roll.
   → Ưu tiên tư liệu Louis (sản phẩm trong video, ảnh sản phẩm/người mẫu trên louisyoga.vn, phim thương hiệu); clip ngoài
   tối đa 1/video và chỉ khi không có cảnh Louis phù hợp. Gợi ý thêm: video trên Facebook Louis Yoga (chưa áp dụng).

Quy tắc rút ra (đã đưa vào SKILL.md): hook mạnh + kết luận rõ; full-bleed; ảnh thật; SFX ~0.5/s, đúng họ tiếng,
tiếng thường −3 dB / punch +7 dB; giọng xử lý rõ ấm; nhạc ~24 dB dưới giọng; không chỉnh màu khi không được yêu cầu;
luôn lưu bản mới với hậu tố phiên bản, không ghi đè.
