# Louis Yoga — Reels "Ra nhiều mồ hôi, chọn thảm nào?" (phương án v0.1 — ĐÃ DUYỆT 24/10/2026, đã dựng: xem mục 7)

- Ngày: 24/10/2026
- Engine: Remotion 4.0.537, app `louis-yoga-remotion/` (giữ đúng project hiện có, không dùng HyperFrames)
- Quy chuẩn áp dụng: `docs/LOUIS_YOGA_EDIT_GUIDE.md` (màu, font, CTA, vùng an toàn, QC)
- Nguồn: `Tài nguyên video/FDown.vn_Tai_video_Facebook_1080p_748c.mp4` (file gốc không bị sửa; bản chép để dựng: `louis-yoga-remotion/public/reels-chon-tham/source/source-1080p.mp4`)
- Transcript word-level (faster-whisper large-v3): `louis-yoga-remotion/public/reels-chon-tham/data/transcript_raw.json`

Ký hiệu: **[QS]** quan sát/đo trực tiếp · **[DG]** diễn giải · **[ĐX]** đề xuất.

---

## 1. Video tham khảo — https://www.facebook.com/reel/1763428218100789

Truy cập được trong trình duyệt tích hợp mà không cần đăng nhập. Phát ở 540×960.

**Thông tin [QS]:** kênh Finpath, tiêu đề "Liệu ngày tàn của Pháp đã tới? #finpath", 233.6s, ~13.6K lượt thích.

**Cách đo:** tua từng 0.2s đo chênh lệch điểm ảnh (1169 mẫu); ảnh lưới mỗi 2s; đo mức âm (RMS) 0–45s. Em không nghe được tiếng, chỉ đo to/nhỏ.

| Hạng mục | Quan sát [QS] | Ghi chú [DG] |
|---|---|---|
| Thể loại | Video giải thích bằng **đồ hoạ chuyển động + giọng đọc**. Không thấy người nói vào máy ở các khung đã lấy mẫu. | Khác hẳn video gốc (talking-head bán hàng) → chỉ học được *cách trình bày thông tin*, không học được *cách quay*. |
| Nhịp | 0–110s: hình đổi gần như liên tục, mỗi "nhịp" 0.5–2s (bản đồ zoom, ảnh pop, B-roll). 110–233s: chậm hơn, mỗi khối infographic 3–6s, bên trong vẫn có phần tử nhỏ pop vào. | Không có khoảnh khắc nào màn hình đứng yên quá ~2s. |
| Mở đầu | 0–6s: địa cầu zoom vào Pháp → mốc "21/9 ngoại ô Paris" → B-roll thùng rác bị đốt → bản đồ. Tiêu đề "Liệu ngày tàn đế chế Pháp đã tới?" chỉ hiện ở ~42s. | Mở bằng sự kiện cụ thể + con số ("HƠN 6.000"), tiêu đề đến sau. |
| Chữ | Sans đậm IN HOA; trắng + **xanh chanh** làm điểm nhấn, **đỏ** cho con số lớn ("HƠN 6.000", "~90 TỶ €"). Nhãn nhỏ đi kèm số lớn. Chữ nằm ở 10–40% chiều cao, phía trên hình minh hoạ. | Mỗi ý chính = 1 con số/1 từ khoá lớn + 1 nhãn nhỏ giải thích. |
| Hình | Nền tối (bản đồ vệ tinh, giấy than xám), người/vật cắt rời viền trắng kiểu sticker, mặt đất giấy xé, icon line-art xanh chanh, biểu đồ cột/đường, so sánh cân đòn bẩy. | Đồ hoạ minh hoạ trực tiếp từng câu nói. |
| Chuyển cảnh | Zoom/pan bản đồ, phần tử pop/scale, ảnh "ghim" lên bản đồ, một cú whip mờ (~228s). Không thấy glitch. | Chuyển động có chủ đích, gắn với nội dung. |
| Âm thanh | 0–45s: đỉnh mỗi giây −8…−17 dB, đáy −21…−38 dB; không có khoảng lặng dài; nhiều đỉnh ngắn đột ngột. | Nhiều khả năng giọng đọc + nhạc nền + SFX ở các cú pop. **Chưa xác minh** loại nhạc/SFX. |
| Kết | 230–233s: hình người cắt rời + câu chốt chữ xanh/đỏ. | Kết bằng câu chốt, không thấy CTA rõ ở các khung đã lấy mẫu. |

**Nên học:** biến mỗi ý thành 1 phần tử đồ hoạ (số lớn + nhãn nhỏ, icon, so sánh); hình luôn có chuyển động nhỏ mỗi 1.5–3s; số liệu là điểm nhấn thị giác; mở bằng câu hỏi/vấn đề cụ thể.

**Không áp dụng nguyên xi:** nền tối u ám, xanh chanh/đỏ (trái hệ màu Louis Yoga), bản đồ, B-roll tin tức, độ dài 4 phút, cách làm không có người nói. Không lấy nhạc, SFX, hình hay font của video này.

---

## 2. Video gốc

**Thông số [QS]:** 1080×1920, 30fps, H.264 ~1.09 Mbps (đã bị Facebook nén), AAC 48kHz stereo, 48.87s. File 720p cùng thư mục là cùng nội dung, độ phân giải thấp hơn → không dùng.

**Phát hiện quan trọng [QS]:**
1. **Đây là bản đã dựng, không phải file thô.** Nửa dưới khung (khoảng y 1060–1660 trên 1920) có **thẻ hồng Louis Yoga cháy cứng vào hình** (logo hoa sen + chữ "Chọn thảm nào?", "Đều hút mồ hôi", "4,5 ly"…). Không thể gỡ thẻ này ra.
2. **Âm thanh đã có nhạc nền trộn sẵn** và đã chuẩn hoá: −14.1 LUFS, LRA 1.9 LU; trước khi người nói cất lời (0–0.6s) nền vẫn ở −20 dB RMS. Không tách nhạc khỏi giọng được bằng công cụ hiện có.
3. Gần như không có khoảng lặng: chỉ 3 chỗ ngừng ~0.2s và 1 chỗ ngừng 1.5s (20.96–22.54s).
4. Người nói **ra khỏi khung** 2 lần: ~8.3–12s (đi lấy đồ, có crossfade ở ~8s) và ~17.5–19.5s (đi lấy thảm xanh). 15–19s thẻ hồng trống chữ.
5. Hình sáng, đúng màu, phòng trưng bày thảm đẹp; mặt người nói ở khoảng y 250–600.

**Nội dung (theo transcript, chưa sửa):**

| Mốc | Lời nói | Vai trò |
|---|---|---|
| 0.6–7.6 | Thảm loại nào hút mồ hôi tốt thì tất cả các dòng thảm… cao su tự nhiên thì nó đều sẽ có cái độ thấm hút mồ hôi nó tốt. | Hook + ý 1 |
| 7.9–14.0 | Khi mình tập luyện hay vận động mà ra nhiều mồ hôi chẳng hạn, hay tập yoga theo trường phái hot yoga, | Đối tượng |
| 14.9–18.6 | thì mình có thể lựa chọn các dòng thảm có độ dày tốt hơn một chút cho em. | Lời khuyên |
| 19.1–26.1 | Thì mình có thể tham khảo qua cái mã này. **Mã 2 này giúp em**(?) là dành cho anh chị em mà mình tập luyện thường xuyên. | Gợi ý mã 1 |
| 26.2–31.8 | Mấy chị em nào mà mình mới tập thì tham khảo qua cái mã này… độ dày của thảm nó sẽ là 4,5 ly | Gợi ý mã 2 |
| 32.0–36.2 | Là rất là vừa đủ rồi, rất là đủ rồi. Thậm chí nó còn dư rồi mọi người nhé | Nhấn |
| 36.2–42.2 | …trên bề mặt thảm nó phải có cái độ êm ái này, thấm hút mồ hôi tốt này, | Tiêu chí |
| 42.3–48.7 | hay là bám sàn, bám tay thì các dòng thảm đó của **nhà lưu dựa KBN**(?) đều có thể đáp ứng được các cái nhu cầu đó cho mọi người | Kết |

**Cần anh xác nhận (Whisper nghe không rõ):**
- 22.5s: "Mã 2 này giúp em" — đúng là "mã 2", hay tên mã khác? Mã này dày bao nhiêu (anh không nói trong video, em sẽ không tự ghi thông số)?
- 45.4s: "nhà lưu dựa KBN" — em đoán là "nhà Louis Yoga", cần anh xác nhận.
- Tên 2 mẫu thảm (thảm đen hoạ tiết vàng, thảm xanh dương) nếu muốn hiện tên trên màn hình.

---

## 3. Phương án dựng

### 3.1 Ý tưởng
**"Ra nhiều mồ hôi, chọn thảm nào?"** — giữ người tư vấn thật, nói tự nhiên, nhưng **mỗi ý được "vẽ" ra bằng đồ hoạ** như cách Finpath trình bày. Cảm xúc: gần gũi, rõ ràng, đáng tin, như được tư vấn tại cửa hàng.

### 3.2 Bố cục khung 9:16 (giải quyết thẻ hồng cháy cứng)
- **Nửa trên (y 0–~1040): người nói** — hình gốc, punch-in nhẹ ≤ 108% bám mặt ở chỗ nhấn.
- **Nửa dưới (y ~1040–1920): "bảng đồ hoạ" mới, phủ kín thẻ hồng cũ.** Nền `#fcefef` có hoạ tiết nhẹ, viền trên bo cong. Đây là vùng chạy số lớn, icon, so sánh, phụ đề — tương đương các khối infographic của video tham khảo, nhưng bằng màu Louis Yoga.
- Phụ đề karaoke đặt trong bảng dưới (y ~1180–1450), không bao giờ đè mặt. Không đặt chữ quan trọng dưới y 1500 (vùng caption/nút của Reels/TikTok).
- Lý do không crop lấy nửa trên rồi phóng to: nguồn chỉ 1.09 Mbps, phóng 1.8× sẽ vỡ hình.

### 3.3 Timeline dự kiến (mốc theo file gốc; bản dựng ~44–45s)

| Mốc gốc | Giữ / cắt | Nửa trên (người) | Bảng đồ hoạ dưới |
|---|---|---|---|
| 0.0–0.6 | **Cắt** (nhạc nền trước khi nói) | — | — |
| 0.6–2.0 | Giữ | Punch-in nhẹ vào mặt | Câu hỏi hook **"Ra nhiều mồ hôi — chọn thảm nào?"** pop vào ngay frame đầu |
| 2.0–7.6 | Giữ | Bình thường | Icon giọt nước + nhãn **"CAO SU TỰ NHIÊN"** → **"Thấm hút mồ hôi tốt"** |
| 7.9–14.0 | Giữ tiếng | **Lúc người nói ra khỏi khung (~8.3–12s): phủ cả màn bằng thẻ minh hoạ** (giọt mồ hôi + nhiệt kế "HOT YOGA") rồi trả về người nói khi anh quay lại | Nhãn "Ra nhiều mồ hôi / Tập hot yoga" |
| 14.9–18.6 | Giữ | Bình thường; 17.5–18.6 người ra khung → giữ thẻ minh hoạ | Hình thanh độ dày tăng lên + **"Dày hơn một chút"** |
| 19.1–21.0 | Giữ | Cầm thảm | "Tham khảo mẫu này" |
| 21.0–22.5 | **Thu ngắn chỗ ngừng 1.5s → 0.2s** | — | — |
| 22.5–26.1 | Giữ (tuỳ anh xác nhận chữ) | Cầm thảm xanh | Thẻ **"Người tập thường xuyên"** |
| 26.2–31.8 | Giữ | Tay trên thảm đen | Thẻ **"Mới tập"** → số lớn **"4,5 ly"** đếm lên + mặt cắt độ dày thảm |
| 32.0–33.9 | Giữ "Là rất là vừa đủ rồi" | Punch-in | Dấu tích "Vừa đủ" |
| 33.9–34.6 | **Cắt** câu lặp "rất là đủ rồi" | — | — |
| 34.96–36.2 | Giữ "Thậm chí nó còn dư rồi mọi người nhé" | Bình thường | — |
| 36.2–42.2 | Giữ | Bình thường | Checklist 3 tiêu chí pop lần lượt đúng lúc nói: **Êm ái** → **Thấm hút** |
| 42.3–48.7 | Giữ | Bình thường | → **Bám sàn, bám tay** ✓; câu cuối hiện tên thương hiệu (sau khi anh xác nhận) |
| 48.7–48.9 | Kết | End card logo Louis Yoga 1–1.5s *(cần file logo vector — xem mục 7)* | |

Nguyên tắc cắt: chỉ cắt khoảng ngừng và câu lặp nguyên văn. Không bỏ ý, không đổi thứ tự, không viết lại lời.

### 3.4 Lời nói, phụ đề, từ khoá, âm thanh
- **Phụ đề:** karaoke từng từ, tối đa 2 dòng × 5–7 từ, chữ đỏ rượu `#4a202c` trên nền bảng sáng, từ đang nói tô hồng `#d72182`. Font Montserrat (đã có trong project, có dấu tiếng Việt). Phụ đề viết đúng lời nói, chỉ sửa chính tả/dấu câu và lỗi nhận dạng ("thầm hút" → "thấm hút").
- **Từ khoá nhấn:** chỉ những từ đã có trong lời nói: *mồ hôi, cao su tự nhiên, hot yoga, độ dày, thường xuyên, mới tập, 4,5 ly, êm ái, thấm hút, bám sàn, bám tay*.
- **Nhạc nền:** giữ nhạc đã trộn sẵn trong nguồn (không tách được). **Không thêm nhạc mới** để tránh 2 lớp nhạc chồng nhau.
- **SFX:** đề xuất 4–6 tiếng "pop" mềm trong 15s đầu, sau đó chỉ ở checklist 3 tiêu chí, −20 dB dưới giọng. **Chưa chèn được**: kho `shared-sources/sound-effects` không có hồ sơ giấy phép (README của kho khuyến cáo không dùng cho video thương mại). Cần anh chọn: gửi SFX có bản quyền, cho phép em tải SFX miễn phí bản quyền (Pixabay/Mixkit), hoặc dựng không SFX.
- **Âm lượng:** nguồn đã ở −14.1 LUFS. Sau khi cắt sẽ đo lại, chuẩn hoá −14 LUFS, true peak ≤ −1.5 dBTP. Không giảm nhiễu (giọng đang sạch; khử nhiễu sẽ làm méo nhạc nền trộn sẵn).

### 3.5 Áp dụng phong cách tham khảo
| Từ Finpath | Áp dụng cho Louis Yoga |
|---|---|
| Số lớn + nhãn nhỏ | "4,5 ly" cỡ lớn, nhãn "MỚI TẬP" nhỏ phía trên |
| Icon line-art pop theo lời | Giọt nước, nhiệt kế, lớp thảm, bàn tay, tích ✓ — vẽ bằng SVG đơn giản, màu hồng/đỏ rượu |
| Không đứng hình quá 2–3s | Mỗi 1.5–3s có 1 phần tử mới vào bảng dưới hoặc 1 punch-in |
| Thẻ minh hoạ phủ cảnh "chết" | Phủ cả 2 đoạn người nói ra khỏi khung |
| Mở bằng vấn đề cụ thể | Câu hỏi "Ra nhiều mồ hôi — chọn thảm nào?" ngay frame 0 |
| *Không dùng* | Nền tối, xanh chanh/đỏ, bản đồ, glitch, whip mờ, nhạc/SFX của họ |

Motion theo guide: fade/slide/scale 6–10 frame, easing mềm, không nảy mạnh, không rung.

### 3.6 Điểm yếu của nguồn → cách khắc phục
| Điểm yếu | Khắc phục |
|---|---|
| Thẻ hồng cũ cháy cứng, chữ cũ lặp lại lời nói | Phủ bằng bảng đồ hoạ mới |
| Người nói ra khỏi khung 2 lần | Thẻ minh hoạ toàn màn ở đúng các đoạn đó |
| Chỗ ngừng 1.5s, câu lặp | Cắt |
| Nguồn nén thấp (1.09 Mbps) | Không phóng to quá 108%; xuất bitrate cao để không nén chồng thêm |
| Nhạc nền trộn sẵn | Giữ nguyên, không thêm nhạc |
| Không có tên mẫu thảm, độ dày mẫu "thường xuyên" | Không tự ghi; chờ anh cung cấp |

---

## 4. Tài nguyên

| Cần | Đã có | Còn thiếu |
|---|---|---|
| Video nguồn | Có (1080p) | File quay gốc chưa chèn thẻ (nếu còn) — sẽ cho chất lượng tốt hơn nhiều |
| Font | Montserrat Variable (OFL) trong `public/fonts/` | — |
| Màu thương hiệu | Từ `LOUIS_YOGA_EDIT_GUIDE.md` | — |
| Logo Louis Yoga | Chỉ có bản PNG 130×112 trong bản website nháp (quá nhỏ) | **Logo vector (SVG/AI)** cho end card |
| Icon minh hoạ | Em tự vẽ SVG đơn giản (giọt nước, nhiệt kế, lớp thảm, tích) | — |
| SFX | Kho chung không rõ giấy phép | SFX có bản quyền hoặc cho phép tải nguồn miễn phí |
| Nhạc | Giữ nhạc trong nguồn | — |
| Xác nhận lời nói | — | 2 chỗ nghe không rõ (mục 2) |

## 5. Thông số đầu ra
- 1080×1920, 9:16, 30fps (theo nguồn), MP4 H.264 + AAC 48kHz, −14 LUFS.
- Composition mới `louis-yoga-reels-chon-tham` trong `louis-yoga-remotion/src/reels-chon-tham/` (không sửa composition TVC cũ).
- Asset: `louis-yoga-remotion/public/reels-chon-tham/`
- Xuất: `louis-yoga-remotion/renders/reels-chon-tham/` — preview `…-preview-v1.mp4`, bản hoàn chỉnh `…-final-v1.mp4`, tăng version, không ghi đè.
- Tên đề xuất: **"Ra nhiều mồ hôi, chọn thảm nào?"** (phụ: "Tập hot yoga nên chọn thảm dày bao nhiêu?")

## 6. Đề xuất cần anh duyệt (chưa đưa vào video)
- CTA cuối: video gốc có "Theo dõi Louis Yoga". Đề xuất giữ đúng 1 CTA đó ở 2s cuối, hoặc đổi thành "Nhắn shop để chọn thảm" — anh chọn.
- Tên mẫu thảm / mã sản phẩm trên màn hình.

---

## 7. Bản dựng v1 (24/10/2026)

### File
| Loại | Đường dẫn |
|---|---|
| **Bản hoàn chỉnh** | `louis-yoga-remotion/renders/reels-chon-tham/louis-yoga-reels-chon-tham-final-v2.mp4` |
| Bản trước (thay bằng v2: v2 hiện câu hook ngay frame 0) | `…/louis-yoga-reels-chon-tham-final-v1.mp4` |
| Preview đầu tiên (trước khi sửa số "?", checklist, thẻ đứng yên) | `…/louis-yoga-reels-chon-tham-preview-v1.mp4` |
| Ảnh QC | `…/stills/qc-v1/`, ảnh nháp bố cục `…/stills/layout-draft-*.png` |
| Composition | `louis-yoga-remotion/src/reels-chon-tham/ReelsChonTham.tsx` (id `louis-yoga-reels-chon-tham`) |
| Dữ liệu timeline (sinh tự động) | `src/reels-chon-tham/timeline.gen.ts` ← `scripts/reels-chon-tham/build_timeline.py` |
| Transcript | `public/reels-chon-tham/data/transcript_raw.json` |

Sửa chữ phụ đề: sửa `CHUNKS` / `fix_words` trong `build_timeline.py` → chạy `python -X utf8 scripts/reels-chon-tham/build_timeline.py` → render lại (tăng version).

Lệnh render (cổng 3000 đang bị Studio của phiên khác chiếm nên dùng cổng khác):
`npx remotion render src/index.ts louis-yoga-reels-chon-tham renders/reels-chon-tham/louis-yoga-reels-chon-tham-final-v3.mp4 --port=3177 --codec=h264 --crf=16 --pixel-format=yuv420p --audio-codec=aac --audio-bitrate=256k`

### Thay đổi so với phương án
- Cắt làm ngay trong Remotion (3 đoạn `trimBefore/trimAfter`, khớp từng frame) thay vì xuất `clean.mp4` bằng ffmpeg: nguồn đã nén 1.09 Mbps, tránh nén thêm 1 lần. Mỗi mối cắt có ramp âm lượng 3 frame (đo: không có tiếng click).
- Điểm cắt đặt theo đo năng lượng âm thanh: bỏ 0–0.5s (chỉ có nhạc), 21.37–21.93s (khoảng ngừng; chữ "Mã" thật sự bắt đầu ở 22.0s chứ không phải 22.54s như Whisper báo), 33.93–34.90s (câu lặp "rất là đủ rồi").
- End card: dùng **logo động của chính Louis Yoga** (`public/tvc/clips/s10.mp4`, trích từ phim thương hiệu, đã xác minh quyền trong `LOUIS_YOGA_TVC_V1.md`) + CTA lấy đúng chữ từ thẻ cuối của video gốc: "Muốn chọn đúng thảm? · Theo dõi Louis Yoga · để xem thêm mẹo chọn thảm". Không vẽ lại logo.
- Không thêm nhạc: giữ nhạc trộn sẵn trong nguồn. Nhạc nguồn tắt hẳn ở cuối, nên 2.5s end card chỉ có tiếng chime (−31.6 dB RMS).

### Nguồn đã dùng
| Asset | Nguồn | Quyền |
|---|---|---|
| Video người nói | `Tài nguyên video/FDown.vn_Tai_video_Facebook_1080p_748c.mp4` (bản chép trong `public/reels-chon-tham/source/`) | Video của Louis Yoga do anh cung cấp |
| Logo động | `public/tvc/clips/s10.mp4` (phim thương hiệu Louis Yoga) | Louis Yoga sở hữu |
| Font | Montserrat Variable, `public/fonts/` | SIL OFL 1.1 |
| 6 SFX | Mixkit, lưu tại `shared-sources/sound-effects/mixkit/` (+ `SOURCES.md`), chép vào `public/reels-chon-tham/sfx/` | Mixkit Sound Effects Free License (dùng thương mại/mạng xã hội, không cần ghi công) |
| Icon (giọt nước, nhiệt kế, cuộn thảm, người, dấu tích, mũi tên) | Vẽ SVG trong code | Tự tạo |

### Thông số (ffprobe / ebur128 trên file final-v2)
| Mục | Giá trị |
|---|---|
| Khung / FPS | 1080×1920 (9:16), 30/1, 1480 frame |
| Thời lượng | 49.37s (46.83s lời nói + 2.5s end card) |
| Video | H.264 High, CRF 16, ~4.2 Mbps; pixel format yuvj420p (Remotion vẫn ra yuvj dù đặt yuv420p, giống bản TVC) |
| Audio | AAC-LC 48 kHz stereo 256 kbps |
| Loudness | −14.1 LUFS, true peak −2.5 dBTP |
| Dung lượng | 25.9 MB |

### QC đã làm
- Lint + typecheck cho thư mục `reels-chon-tham`: đạt.
- Giải mã hết file không lỗi; blackdetect 0 đoạn; freezedetect (≥ 0.6s): 0 đoạn (bản preview có 2 đoạn thẻ đứng yên → đã thêm push chậm ≤ 4%).
- Không có tiếng click ở 3 mối cắt (chênh lệch mẫu lớn nhất quanh mối cắt 0.007, ngưỡng p99.9 của cả bài 0.126).
- Soi ảnh ở 0.25s/1s/khung chính và ở cỡ điện thoại (360px rộng): chữ không đè mặt, dấu tiếng Việt đủ, không xuống dòng lỗi; nội dung chữ nằm trong x 90–910, y ≤ ~1500.
- **Chưa làm được:** nghe bằng loa (em không nghe được âm thanh) và kiểm thật trên app Reels/TikTok. SFX được đặt mức theo số đo (đỉnh pop ≈ −12 dBFS, giọng ≈ −3 dBFS).

### Còn chờ anh duyệt
1. **Phụ đề 2 chỗ Whisper nghe chưa chắc:** "Mã 2 này giúp em" (~20.9s trong bản dựng) và "của nhà Louis Yoga" (~43.1s, Whisper nghe "nhà lưu dựa KBN"). Ngoài ra em bỏ 1 từ Whisper nghe là "xây" trước "cho mọi người" (~46s), coi như lỗi nhận dạng.
2. Bảng chữ "LOUIS YOGA · Đều đáp ứng được" ở ~42–46.8s dựa trên chỗ (1); nếu sai thì sửa cùng lúc.
3. Mức SFX khi nghe bằng loa thật.
