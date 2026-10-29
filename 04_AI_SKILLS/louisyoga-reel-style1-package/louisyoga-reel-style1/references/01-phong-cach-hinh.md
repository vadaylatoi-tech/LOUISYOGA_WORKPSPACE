# 01 — Phong cách hình (Louis Yoga reel style 1)

Nguồn gốc: học từ video explainer kiểu tài liệu (facebook.com/reel/1763428218100789: nền tối, chữ đậm viết hoa,
ảnh polaroid rơi, dấu mộc, whip blur, số liệu thành đồ hoạ), rồi chỉnh theo góp ý của chủ thương hiệu Louis Yoga.

## Khung & bố cục
- 1080×1920, 30 fps. Footage người nói **tràn khung** (không thu nhỏ vào ô, không nền che 40% như bản đầu).
- **SAFE ZONE Facebook Reels + TikTok — nguyên tắc dựng mặc định** (chủ thương hiệu chốt 29/10/2026). Tính ngay lúc
  đặt bố cục, không để tới QC. Vùng ưu tiên cho chữ quan trọng (hook, tiêu đề, caption, logo, CTA, con số, dấu mộc):
  **x 108–886, y 269–1248**. Ngoài vùng này có thể bị che bởi: tai thỏ/Dynamic Island/thanh trạng thái + tab
  "Following/Reels" (trên), avatar-tên-caption bài đăng-thanh điều hướng (dưới), cột Like/Comment/Share (phải).
  - Đo **cả hộp thật** của khối: mọi dòng sau khi ngắt, viền/stroke, shadow, và lúc lớn nhất của animation đang đọc
    (từ đang nói to 108%, slam/pop scale, rung) — không chỉ tâm hay `top`. Vùng an toàn lệch trái (cột nút ở phải):
    khối căn giữa 1080 thì rộng tối đa ~690 px; rộng hơn → dịch tâm về x ≈ 497, xuống dòng, bớt chữ hoặc giảm cỡ.
  - Phải nằm trong vùng suốt lúc người xem cần đọc; đoạn bay vào/ra, whip, chớp được đi ra ngoài.
  - Footage, B-roll, nền, `TopShade`, hiệu ứng trang trí vẫn tràn toàn khung.
  - Là vùng ưu tiên, không phải hình chữ nhật ép cứng: lệch vài chục px vì bố cục đẹp hơn được, miễn chữ không lọt vào
    vùng nút/caption bài đăng. Một bản dùng cho cả hai nền tảng → bố cục hợp cả hai (vùng trên là vùng chung).
- Chia vùng theo footage thật (đo trên 1 khung), các dải đã cắt theo safe zone:
  - **Dải trên** (kệ/tường phía trên đầu, y ≈ 270–420): tiêu đề hook, tag series, nhãn B-roll. Dùng `TopShade` khi cần
    đọc rõ. Hook 2 dòng 136 px cao ~300 px → đỉnh chữ không cao hơn y 270; không đủ chỗ thì giảm cỡ hoặc lấn xuống trán.
  - **Mặt + sản phẩm** (y ≈ 420–1180): KHÔNG đặt chữ/panel. Chỉ được kẻ đường callout chỉ vào sản phẩm.
  - **Caption** ngay dưới sản phẩm/cằm: mép DƯỚI caption (kể cả viền) ≈ 1248 → 1 dòng 62 px thì `CAP_Y` ≈ 1150–1180.
    Dòng dài chạm x > 886 → giảm `--max-chars` hoặc ép `"lines"` trong fixes.json.
  - **Dải dưới** (bàn, khăn, hộp; `G` ≈ 1260–1500): panel so sánh, ảnh thật, checklist. Nằm dưới 1248 nên chỉ để hình/
    panel minh hoạ phụ; con số, chữ chốt, dấu mộc cần đọc thì đặt ở phần trên của panel (≤ ~1300) hoặc đưa lên dải
    trên. x ≤ 886 khi y ≥ 1000 (cột nút); không đặt gì cần đọc ở y > 1500 (avatar, mô tả bài đăng).
- Ví dụ đã duyệt (trước khi có safe zone): CAP_Y = 1196, G = 1330 — video mới kéo lên CAP_Y ≈ 1170, G ≈ 1270.

## Màu (tokens trong `src/kit/theme.ts`)
| token | mã | dùng cho |
|---|---|---|
| ink | #16111A | nền panel, chữ trên nền sáng |
| accent | #FF5AAE | từ khoá, từ đang nói trong caption, viền highlight |
| pinkDeep | #E2318B | pill, tag series, vòng ✓ |
| gold | #F4C25B | dấu mộc, gạch chữ hook, nút CTA phụ, "VS" |
| white | #FFFFFF | chữ chính |
| dim | rgba(255,255,255,.55) | kicker phụ |
Hồng không cần đúng #d72182 của logo — chỉ cần cùng tone, đẹp là được (lời chủ thương hiệu).

## Chữ
- Montserrat (variable, đủ dấu tiếng Việt) 800–900, VIẾT HOA, letter-spacing −1; kicker 40 px giãn chữ 4.
- Caption karaoke: 62 px, 4 từ/dòng (cho 6 nếu từ sau là "ly/su/hơn/…"), viền đen 4 hướng, từ đang nói hồng + to 108%.
- Tiêu đề hook 100–136 px, tối đa 2 dòng; dòng 2 màu accent.

## Ngôn ngữ chuyển động (atoms trong `src/kit/`)
| Thành phần | Dùng khi | SFX đi kèm |
|---|---|---|
| `BigText slam` | câu hook, kết luận lớn | punch |
| `Stamp` (dấu mộc vàng) | chốt ý: "CHƯA CHẮC!", "DỄ LÚN!", "CHUẨN 5 LY" | punch (+ rung/chớp nếu là cú lớn) |
| `StrikeLine` | gạch bỏ quan niệm sai ở hook | (đi cùng punch của stamp) |
| `Pill` | nhãn ngắn, ✓ lợi ích | pop / pop-2 |
| `Panel` + số đếm | so sánh số liệu (bar dày dần XUỐNG dưới, không đè số) | quick-swoosh (panel), digital-counting (số) |
| `PhotoCard` | so sánh bằng ẢNH THẬT (sản phẩm, vật liệu) + thanh đo | quick-swoosh |
| `CalloutLine` | chỉ vào sản phẩm người nói cầm | quick-swoosh / pop-2 |
| `CheckGrid` | tổng kết 3–4 lợi ích | quick-ting từng mục, correct mục cuối |
| `Polaroid` | sản phẩm ở CTA | camera-shutter |
| `TalkingHead` | luôn: zoom luân phiên mỗi đoạn (1.10↔1.30), punch-in từ khoá (+0.08..0.22), zoom-blur 4 khung ở mối cắt, `focus` trượt camera xuống sản phẩm | không có SFX ở mối cắt thường |
| `BrollLayer` | minh hoạ lời nói bằng phim thương hiệu, 1.2–3 s/cảnh, whip ngang vào/ra + nhãn | swoosh lúc VÀO, không SFX lúc ra |
| `useImpact` | rung khung + chớp trắng — chỉ 1–3 lần/video | — |

## Cấu trúc video
1. **Hook 0–2.5 s**: quan niệm/ câu hỏi slam 2 nhịp → riser → gạch chữ + dấu mộc + zoom mạnh vào mặt + rung/chớp.
2. **Thân**: mỗi ý một "beat" hình (panel số, B-roll, ảnh thật, callout sản phẩm), đổi hình mỗi 2–5 s.
3. **Kết luận**: tiêu đề slam lời khuyên + checklist lợi ích.
4. **CTA 1.8 s cuối** (freeze + tối nhẹ): logo hoa sen, "FOLLOW LOUIS YOGA", "xem thêm mẹo chọn thảm", polaroid sản phẩm.

## Cấm
- Panel/nền che toàn khung lâu; chữ đè mặt hoặc sản phẩm; hình vẽ hoạt hình thay cho ảnh thật khi có ảnh thật.
- Ảnh người tạo dáng chung chung không liên quan sản phẩm. Bar/khối đè lên con số.
- Chỉnh màu footage khi không được yêu cầu. `Math.random()` trong composition.
