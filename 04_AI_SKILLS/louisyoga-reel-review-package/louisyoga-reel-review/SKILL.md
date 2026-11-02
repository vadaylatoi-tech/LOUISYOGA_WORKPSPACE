---
name: louisyoga-reel-review
description: "Dựng video REVIEW / UNBOX SẢN PHẨM Louis Yoga dạng KHÔNG LỜI 9:16 (PHONG CÁCH 3): tắt tiếng gốc, video nằm trong khung bo góc trên nền mờ của chính cảnh quay, logo Louis Yoga trên đầu, tên + ảnh sản phẩm góc dưới phải, chữ gõ từng ký tự kèm tiếng phím thật, mở đầu thu vào khung đúng nhịp nhạc, cắt và chuyển cảnh mềm theo nhạc, âm thanh cận cảnh, kết bằng CTA ảnh sản phẩm bay vào giữa. Input: video review/unbox có sẵn. Output: mp4 1080×1920 + ảnh bìa + báo cáo. Mẫu duyệt: video thảm Aura. Trigger: '/louisyoga-reel-review', 'edit video review thảm', 'dựng video review sản phẩm', 'làm video unbox không lời', 'làm giống video review thảm Aura', 'phong cách 3 louis yoga'. KHÔNG dùng cho video có người nói tư vấn (style 1) hay giải thích kỹ thuật bằng lời (style 2)."
---

# Louis Yoga reel — phong cách 3 (review sản phẩm không lời)

Chọn phong cách này khi video gốc là cảnh **dùng thử sản phẩm** và thông tin có thể kể bằng hình + vài chữ ngắn.
Người nói tư vấn → style 1. Giải thích cơ chế, so thông số bằng lời → style 2.

`<S>` = thư mục chứa file này. `<S1>` = `~/.claude/skills/louisyoga-reel-style1` (dùng lại `make_cover.py`, `remotion_local.py`).

Đọc trước khi làm: `references/01-phong-cach-3.md` (bố cục, âm, điều cấm, bài học từ 7 bản). Mẫu đầy đủ: `examples/aura.review.json`.

## Nơi lưu
- Project: Drive `05_VIDEO_PROJECTS/<dự án>/edit/<NN-ten>/project`, hồ sơ ở `edit/<NN-ten>/`.
- Final + ảnh bìa: Drive `10_FINAL_DELIVERABLES/<YYYY-MM-DD>_<dự án>/<NN - tên video>.mp4`. Bản sửa sau thêm `_v2`, không ghi đè.
- Không ghi lên C:. Sau khi ghi nhiều lên G:, chờ Drive đồng bộ xong rồi mới test.

## Quy trình

1. **Xem nguồn**: `<S1>/scripts/contact_sheet.py --every 2`. Ghi lại cảnh dùng được (giây), cảnh có mặt đang nói, chữ cháy sẵn, logo bị ngược (cảnh selfie cần `flip`). Hỏi quyền đăng lại nếu video là của người khác.
2. **Chọn nhạc**: `03_MEDIA_LIBRARY/MUSIC_LIBRARY/CATALOG.md`. Tìm nhịp đậm đầu tiên của đoạn nhạc rồi đặt điểm bắt đầu = nhịp đó − 0,9 s; khi bài dâng nên rơi vào cảnh test cao trào. Ghi credit bài nhạc.
3. **Phân cảnh** vào `review.json`, 30–40 s:
   mở bằng cảnh đẹp nhất + câu hỏi → quà/đóng gói → chạm bề mặt → thiết kế → test thật (xịt nước, độ bám) → thông số → cảnh tập → CTA.
   ▶ **CỔNG 1**: đưa bảng phân cảnh, nhạc, chữ. Chờ anh OK, trừ khi anh đã nói "cứ làm".
4. **Tạo project + clip**:
   ```bash
   python <S>/scripts/new_review.py --dest <project> --anh-san-pham <anh.jpg> --config <review.json>
   python <S>/scripts/build_review.py --project <project>
   ```
   Sửa `ss`, `crop`, `speed` của một clip thì xóa `public/footage/<ten>.mp4` hoặc thêm `--lam-lai`.
5. **Soát bố cục** trước khi render: chạy ở giây mở đầu, mỗi cảnh có chữ, cảnh xịt, CTA.
   ```bash
   python <S>/scripts/render_review.py --project <project> --chi-still 0.3 3.6 12 22 34 --sheet <work>/stills.jpg
   ```
   Chữ phải đọc được, không đè tay/sản phẩm, không chạm thẻ ảnh góc phải. Cảnh xịt: đo lại `nozzle` trên khung 1080×1920.
6. **Render + mix + ảnh bìa**:
   ```bash
   python <S>/scripts/render_review.py --project <project> --out "<final>.mp4"
   ```
   Tự ra −14 LUFS, đỉnh khoảng −2 dBTP, gắn bìa ở giây `--bia` (mặc định 3,6, lúc tiêu đề đã hiện đủ).
7. **QC**: contact sheet bản cuối, đối chiếu số đo. Em không nghe được âm thật nên luôn ghi "chưa nghe thật" và nhờ anh nghe.
   ▶ **CỔNG 2**: giao file + báo cáo ngắn: nguồn, nhạc + credit, số đo, chỗ cần anh nghe, quyền đăng lại.

## review.json

| Khóa | Ý nghĩa |
|---|---|
| `source` | video gốc; một clip có `source` riêng thì dùng của clip |
| `product` | `label`, `name` (góc dưới), `title`, `site`, `button` (CTA) |
| `cta` | frame bắt đầu CTA, cần ít nhất 3 s tới cuối |
| `trans` | frame chuyển cảnh, mặc định 12 |
| `music` | `file` trong MUSIC_LIBRARY, `parts` `[giây video, giây nguồn, độ dài]`, `fade_in` |
| `clips.<ten>` | `ss` giây nguồn, `flip`, `crop` `[x0,y0,x1]` theo 9:16, `speed` |
| `shots[]` | `clip`, `dur` (giây), `a` dòng chính, `b` dòng phụ |
| chữ của cảnh | `ink` chữ tối trên nền sáng, `tl`/`tr` lề, `ty` đỉnh chữ, `ts` tỉ lệ cỡ, `td` frame trễ |
| hiệu ứng | `tear` chuyển cảnh xé giấy, `mist` các giây xịt (có cả tiếng), `nozzle` `[x,y]` vòi xịt |
| `sfx` | `[cảnh, giây trong cảnh, file, âm lượng]`, file trong `shared-sources/sound-effects` |
| `hits` | `[giây tuyệt đối, file, âm lượng]`, canh theo đỉnh tiếng |

Mở đầu, khung, nền mờ, logo, thẻ sản phẩm, CTA nằm trong `remotion-template/src/Review.tsx`. Chỉ sửa file này khi cần đổi cả phong cách.

## Luật cứng
- Tắt hẳn tiếng gốc. Không dùng cảnh đang nói vào máy, trừ khi crop bỏ miệng.
- Chữ chỉ dùng ý có trong video gốc; thông số phải khớp web hoặc được anh xác nhận.
- Không chỉnh màu; chỉ làm nét nhẹ (`build_review.py` đã có).
- Chỉ dùng cảnh quay đúng sản phẩm đang review. Không trám phim thương hiệu của thảm khác.
- Không gọi đây là quảng cáo công dụng: không viết chữ vượt nội dung video.
- Credit nhạc CC-BY là bắt buộc.
