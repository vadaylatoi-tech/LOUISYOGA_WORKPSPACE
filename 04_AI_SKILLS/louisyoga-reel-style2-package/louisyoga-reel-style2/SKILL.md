---
name: louisyoga-reel-style2
description: "Dựng video ngắn talking-head tiếng Việt (TikTok/Reels 9:16) theo PHONG CÁCH 2 LOUIS YOGA — kiểu GIẢI THÍCH KỸ THUẬT + GIỚI THIỆU SẢN PHẨM (chủ thương hiệu duyệt 29/10/2026 trên video 'Mùa đông sàn lạnh' bản v5): mọi chữ trong safe zone Reels/TikTok, phần giải thích chuyển thành MOTION GRAPHIC toàn khung trên nền chính cửa hàng làm mờ (không lưới, không sub, căn giữa), ảnh sản phẩm nằm trọn trong thẻ (không chữ đè ảnh), không nhãn series; âm thanh hook 'dồn → lặng → nổ' với tiếng chói mở đầu, tiếng căng ~7 s/lần, nhạc 'Inspired' nghe rõ (~15,5 dB dưới giọng). Dùng chung script + kit của louisyoga-reel-style1. Trigger: '/louisyoga-reel-style2', 'edit theo phong cách 2 louis yoga', 'dựng reel kiểu motion graphic giải thích', 'làm giống video mùa đông sàn lạnh'."
---

# Louis Yoga reel — phong cách 2 (giải thích + giới thiệu sản phẩm, motion graphic)

Phong cách 2 KHÔNG thay phong cách 1. Chọn style 2 khi video có phần **giải thích cơ chế / so sánh thông số**
(vì sao lạnh, độ dày, chất liệu, cách dùng) mà chữ nhỏ trên mặt người nói không đủ rõ. Video chỉ tư vấn/kể chuyện
→ dùng style 1.

`<S1>` = `~/.claude/skills/louisyoga-reel-style1` (script + kit dùng chung), `<S2>` = thư mục chứa file này.

Đọc trước khi làm (bắt buộc):
- `<S1>/SKILL.md` — quy trình 8 bước, nơi lưu, luật cứng (style 2 giữ nguyên, trừ chỗ ghi khác dưới đây)
- `references/01-phong-cach-2.md` — hình, âm, cái gì CẤM, bài học từ 9 bản thử
- Ví dụ hoàn chỉnh: `remotion-overlay/src/reel/Reel.tsx` (video 03 "Mùa đông sàn lạnh" v5, đã duyệt)

## Quy trình (khác style 1 ở bước 5, 6, 7, 8)

Bước 0–4: y hệt `<S1>/SKILL.md` (preflight, hồ sơ/brief, cuts + check_cuts, cut_words, track).

5. **Project**:
   ```
   python <S1>/scripts/new_project.py --dest <project> --clean work/clean.mp4 --install
   python <S2>/scripts/apply_style2.py --project <project>
   python <S1>/scripts/gen_data.py --words work/clean.words.json --face work/face.track.json --fixes work/fixes.json --out <project>/src/reel/data.ts
   ```
   `apply_style2.py` chép `kit/style2.tsx` (khối dựng sẵn), `kit/sound.tsx` (ONSET của 4 tiếng mới), `kit/media.tsx`
   (nhãn B-roll trong safe zone), 4 tiếng SFX sáng vào `public/sfx`, và Reel mẫu (chỉ khi Reel còn là mẫu style 1).
6. **Dựng** (`references/01` mục Hình):
   - Đọc brief, đánh dấu đoạn **giải thích/so sánh** → mỗi đoạn 1 STAGE (`MgStage` + `MgTitle` + đồ hoạ: `Section`
     mặt cắt, cột so sánh, thẻ ảnh sản phẩm…). Ghi các đoạn vào `MG_WINDOWS` (dùng cho `FrostFootage` làm mờ footage và
     `CaptionsOffMg` tắt sub). Stage dài 5–9 s; giữa các stage phải có mặt người nói (hook, kết, CTA luôn là mặt).
   - Phần còn lại (mặt người nói): chữ trong cột trống cạnh mặt (`ColTitle`, `SafePanel`, `LeftShade`), caption căn
     giữa safe zone.
   - `stills.py` soát: chữ trong x 108–886 / y 269–1248; khối stage căn quanh y ≈ 830 (dịch bằng `dy`); không
     chữ đè ảnh; footage sau stage phải thật sự mờ.
7. **Âm thanh** (`references/01` mục Âm): hook "dồn → lặng → nổ"; tiếng chói ~7 s/lần; cue tính theo lúc tiếng
   CHẠM (ONSET đã có trong kit — riser đặt cue = lúc đỉnh). `measure_sfx.py` như style 1.
8. **Render**: `python <S1>/scripts/render_all.py ... --sfx-rel <bù bug E> --music-under 11` (nhạc ~15,5 dB dưới
   giọng; style 1 mặc định 19 → ~24 dB, nghe như không có nhạc). `mix_stems.py` tự chặn đỉnh nếu AAC đẩy true peak
   > −1,4 dBTP. Ảnh bìa `make_cover.py --t <khung có đủ tiêu đề hook, trước dấu mộc>`, QC theo `<S1>/references/04`.

Báo cáo, nơi lưu final, nhật ký: như style 1.
