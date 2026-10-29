# 01 — Phong cách 2: hình, âm, bài học

Nguồn: video 03 đợt Săn thảm 24/10 "Mùa đông sàn lạnh – thảm dày có cần lót thêm không?", 9 bản (v1–v9) ngày
29/10/2026; chủ thương hiệu chốt **v5** (hình v4 + SFX v5 + nhạc "Inspired"). Báo cáo đầy đủ từng vòng:
Drive `05_VIDEO_PROJECTS/2026-10_san-tham-2410/edit/03-mua-dong-san-lanh/BAO-CAO-MuaDongSanLanh_v1.md`.

## Hình

**Safe zone** (giữ từ style 1): chữ/logo/CTA cần đọc trong x 108–886, y 269–1248 (tính cả hộp chữ thật, viền, bóng,
animation). Hằng `SAFE_L/SAFE_R/SAFE_CX/CAP_Y` ở `kit/style2.tsx`.

**Motion graphic stage** (`MgStage`) cho mọi đoạn giải thích kỹ thuật / so sánh:
- Nền = **chính footage làm mờ** (`FrostFootage`: blur 38 px, tối 35 %, phóng 8 %) + phủ tím than 50 % + ánh hồng nhẹ.
  CẤM nền lưới ô vuông (anh: "quá nhiều video có rồi, bị AI"). KHÔNG dùng CSS `backdrop-filter` — Remotion render
  không ăn, footage vẫn rõ phía sau (đã thử v4).
- Mở bằng vòng tròn loang (9 frame), tắt mờ 6 frame. SFX vào stage: `glitch.mp3` hoặc quick-swoosh.
- **Không sub trong stage** (`CaptionsOffMg`) — đồ hoạ đã mang ý.
- **Căn giữa khung**: dựng nội dung từ `MG_TOP` (290) rồi đẩy cả khối xuống bằng `dy` để tâm khối ≈ y 820–840 (mẫu: dy 150–210).
  Bản đầu để sát trên (y 290–960) bị chê "bố cục bị đẩy lên".
- Đồ hoạ khoa học, đơn giản: `Section` = mặt cắt NGƯỜI TẬP / THẢM / SÀN LẠNH, hơi lạnh xuyên qua thảm mỏng (người
  chuyển màu lạnh) hoặc bị chặn dưới thảm dày (viền vàng); tách đôi so sánh mỏng ✗ / dày ✓; cột độ dày tỉ lệ
  thật (4,5 vs 6,5 ly) có số đếm; viên "Nặng hơn 4 kg".
- Chỉ dùng số liệu người nói nói ra hoặc dữ liệu sản phẩm thật — không thêm nhiệt độ, % … tự bịa.

**Ảnh sản phẩm**: nằm TRỌN trong khung, trong thẻ trắng bo góc, tên dưới ảnh; **không chữ/pill nào đè lên ảnh**.
(v1 polaroid lệch ra mép trái x −14 + pill đè ảnh → anh chê "lia ra ngoài khung, chữ đè không phù hợp".)

**Không nhãn series** ("Mẹo chọn thảm"…): góc trên đã có tiêu đề/panel, thêm nhãn là rối (anh bỏ ở v3).

**Phần mặt người nói**: chữ dồn vào cột trống cạnh mặt (mặt ở giữa-phải → cột trái x 108–450), `LeftShade` làm tối
mép trái; caption căn giữa safe zone (tâm 497, thu 94 %), mép dưới ≈ 1245.

## Âm

Bài học Quạ HD ("Cách chèn Sound Effects để vừa đúng kĩ thuật, lại vừa có gu", tóm tắt + transcript ở
Drive `…/03-mua-dong-san-lanh/work/tham-khao-quahd/`):
- **Mở video bằng tiếng chói, tần số cao** (rắc/keng) — não tò mò với âm cao, người xem "ngoái lại". Khung 0: `glitch.mp3` + punch.
- **Tiếng căng/chói ~7 s một lần**, không dồn (dồn = nhức đầu). Mẫu: 0 · 1,85 · 7 · 13,3 · 22,3 · 40,5 · 49,6 s.
- Các SFX khác dùng như style 1; tiếng chỉ cần hợp nhịp, không cần giống thật.

**Hook "dồn → lặng → nổ"** (`MUSIC_CURVE` + CUES mẫu):
- Riser kim loại: **cue = lúc ĐỈNH** (ONSET 1,81 s) → đặt `[HOOK_DROP, "riser-metallic.mp3", …]` thì riser vang từ ~0 s và
  lên đỉnh đúng cú chốt. (v4 đặt cue ở 0 s → bị cắt gần hết, gần như không kêu.)
- Nhạc vào to ngay, cắt còn 0,03 trong 0,3 s trước cú chốt, nổ lại cùng punch + "keng" (`glasses-cheers-2.wav`) + rung/chớp.
- `HOOK_DROP` đặt ngay sau cụm từ chốt của câu mở (mẫu 1,85 s sau "miền Bắc").

**4 tiếng mới** (`assets/sfx`, nguồn `03_MEDIA_LIBRARY/shared-sources/sound-effects`; ONSET đã có trong kit + build_stems):
`glitch.mp3` (rắc, vào stage), `glasses-cheers-2.wav` (keng, cú chốt/câu trả lời), `ting.wav` (dấu mộc kết luận),
`new-item.wav` (lấp lánh khi hiện ưu điểm sản phẩm). Cue ghi đúng lúc tiếng CHẠM.

**Nhạc**: "Inspired" – Kevin MacLeod (CC BY 4.0, có sẵn trong asset style 1) — anh thử 5 bài khác (Easy Lemon, Driving
Ambition nguyên bài/cắt ghép, Tears of Joy) rồi quay lại bài này. Mức: `render_all.py --music-under 11` → ~15,5 dB dưới
giọng khi nói (style 1 ~24 dB: anh nghe như "video không có nhạc nền").
Muốn đổi nhạc: chỉ dùng bài có giấy phép THƯƠNG MẠI cho Facebook/TikTok (CC BY, Mixkit…). Bài "No Copyright" trên
YouTube thường là CC BY-NC hoặc chỉ cho YouTube — không dùng cho video quảng cáo.

**Master**: −14 LUFS, true peak ≤ −1,4 dBTP (`mix_stems.py` tự chặn đỉnh nếu AAC đẩy vượt). SFX ~0,43–0,5 tiếng/s.

## Checklist thêm (ngoài `<S1>/references/04-checklist-qc.md`)
- [ ] Mỗi đoạn giải thích kỹ thuật là 1 stage; giữa các stage có mặt người nói; hook + kết + CTA là mặt.
- [ ] Nền stage là footage mờ thật (soi still), không lưới; không sub trong stage; khối căn quanh giữa khung.
- [ ] Ảnh sản phẩm trọn trong khung, không chữ đè ảnh; không nhãn series.
- [ ] Khung 0 có tiếng chói; riser lên đỉnh đúng cú chốt; tiếng căng cách nhau ≥ ~6 s.
- [ ] Nhạc dưới giọng 14–17 dB khi nói.
