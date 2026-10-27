---
name: edit-nns-v1
description: "Dựng video talking-head tiếng Việt từ FILE RAW CHƯA CẮT bằng Remotion, làm đúng 4 việc: (1) tự cắt khoảng lặng + từ đệm 'ậm ừ' bằng transcript word-level, (2) chèn SFX (dồn vào hook), (3) tự chèn LOGO thương hiệu đúng lúc người nói nhắc tên (Claude, HyperFrames, ChatGPT...) lấy từ shared-sources/brand-logos, (4) chèn CAPTION karaoke word-by-word. Timeline SINH ĐỘNG từ transcript của chính file raw — không ghim mốc giây của video cũ như edit-remotion-nns. KHÔNG dựng tip-cycle/PiP/prompt-card/citation. Trigger: '/edit-nns-v1', 'bỏ file raw này vào cắt ậm ừ rồi thêm caption/SFX/logo', 'edit video thô của tôi'."
---

# edit-nns-v1 — Raw footage → video sạch (cắt ậm ừ + caption + logo + SFX)

> Skill này là bản **tách nhánh** từ `edit-remotion-nns`, KHÁC ở điểm cốt tử:
> `edit-remotion-nns` port 1:1 một video ĐÃ ĐO SẴN (timeline hard-code 50.87s, ~10 mốc
> chuyển cảnh tuyệt đối, tip-cycle 3 tip). Skill này nhận **file raw chưa cắt, chưa biết
> dài bao nhiêu**, và mọi mốc thời gian đều được **tính ra từ transcript của chính file đó**.
> Không bao giờ mượn mốc giây của project cũ. Không dựng card tip/prompt/citation/PiP.

Engine vẫn là Remotion trong `remotion/app/` (đã cài sẵn `@remotion/cli` ^4.0.507).

---

## 1. Đầu vào cần có

| Thứ cần | Ghi chú |
|---|---|
| **File raw** (mp4/mov) — bắt buộc | Talking-head 1 người, chưa cắt. Path do user đưa. |
| Kịch bản gốc (nếu có) | Rất nên có — dùng để hiệu chỉnh ASR (tên riêng, thuật ngữ AI hay bị nghe sai). Không có thì vẫn chạy được. |
| Ngôn ngữ | Mặc định `vi`. |

Không có kịch bản thì KHÔNG tự bịa nội dung — chỉ dựa vào ASR và báo user chỗ nào nghe không rõ.

## 2. Nguồn dùng lại (không tạo mới)

| Thứ cần | Lấy ở đâu |
|---|---|
| Palette + font + hằng số canvas | `remotion/app/src/theme.ts` (cream `#FCF3E1`, brown `#302221`, orange `#FF9248`, red `#C41E20`; 1080×1920 @30fps) |
| Font tiếng Việt **mặc định** | `shared-sources/Font/Be_Vietnam_Pro/*.ttf` — Regular 400 / Bold 700 / ExtraBold 800. **KHÔNG dùng Inter** (subset latin, không có dấu → chữ vỡ, xem §8.1) |
| Component caption để tham chiếu/kế thừa | `remotion/app/src/components/CaptionsV2.tsx` (karaoke word-by-word, viền đen 4 hướng, glow cam) |
| Logo thương hiệu | `shared-sources/brand-logos/` + `library.json` (126 brand, có `claude.svg`, `hyperframes.svg`, `chatgpt.svg`, `googlegemini.svg`...) |
| SFX | `shared-sources/sound-effects/` (~100 file, có `library.json` + `USAGE_GUIDE.md`) |
| Style DNA (nhịp, tinh thần hình ảnh) | `.claude/skills/edit-style-nns/SKILL.md` — đọc để giữ đúng "chất" kênh, KHÔNG copy mốc giây |

Copy asset vào `remotion/app/public/<project>/` bằng **file thật** (không symlink) — Remotion chỉ stage file trong project.

---

## 3. Quy trình 5 bước

### Bước 1 — Đo + bóc lời (không đoán)

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of json "<raw>"
```

Rồi transcribe word-level bằng `faster_whisper` (đã cài trong môi trường này):

```python
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
segs, _ = m.transcribe("<raw>", language="vi", word_timestamps=True,
                       vad_filter=True, condition_on_previous_text=False)
```

Lưu ra `transcript_raw.json`: mỗi từ `{w, start, end}`. **`word_timestamps=True` là bắt buộc** —
không có mốc từng từ thì không cắt được ậm ừ, cũng không làm được caption karaoke.

Có kịch bản gốc thì đối chiếu và sửa tay tên riêng/thuật ngữ trước khi qua bước 2 (ASR tiếng Việt
hay nghe "Claude" thành "Cờ-lốt", "HyperFrames" thành "hai pơ phêm").

### Bước 2 — Sinh CUT PLAN (và **dừng lại cho user duyệt**)

Ghép 2 tín hiệu, không dựa 1 cái:

1. **Khoảng lặng thật** — `ffmpeg -i "<raw>" -af silencedetect=n=-32dB:d=0.30 -f null -` (đọc từ stderr).
2. **Từ đệm** — quét transcript theo §4.

Kết quả ghi ra 2 file:
- `cut_plan.json` — danh sách đoạn **GIỮ**: `[{start, end}, ...]` (giây, theo file raw).
- `CUT_PLAN.md` — bảng người đọc được: mỗi dòng cắt gồm `mm:ss.s`, độ dài, lý do (`lặng 0.8s` /
  `từ đệm "ừm"` / `nói lặp`), và **trích 6-8 từ hai bên chỗ cắt** để user hình dung.

**GATE:** đưa `CUT_PLAN.md` cho user xem và chờ OK trước khi cắt. Không tự cắt rồi báo sau —
cắt sai chỗ là hỏng cả bản dựng, mà user đọc bảng này 1 phút là biết ngay.

### Bước 3 — Cắt thật + remap mốc từ

Cắt từng đoạn giữ rồi nối:

```bash
# mỗi đoạn: re-encode (KHÔNG -c copy — copy cắt theo keyframe nên lệch tới cả giây)
ffmpeg -ss <start> -to <end> -i "<raw>" -r 30 -vsync cfr \
  -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 "seg_NN.mp4"
# nối
ffmpeg -f concat -safe 0 -i list.txt -r 30 -c:v libx264 -crf 18 -c:a aac -b:a 192k "clean.mp4"
```

Gotcha đã mắc ở các vòng trước, **bắt buộc phòng**:
- `concat` hay tự tụt về **25fps** → luôn ghim `-r 30` ở CẢ 2 lệnh, xong `ffprobe` lại `r_frame_rate`
  của `clean.mp4` để xác nhận đúng `30/1`.
- Đừng dùng `-c copy` để cắt: cắt theo keyframe → lệch mốc và tiếng bị trượt so với hình.
- `-ar 48000` đồng nhất mọi đoạn, khác sample rate giữa các đoạn là nguồn gốc audio drift khi nối.

Rồi **remap transcript**: mỗi từ còn giữ nhận mốc mới `t_new = t_old - (tổng thời lượng đã cắt trước nó)`.
Ghi ra `transcript_clean.json`. Từ đây trở đi **mọi thứ trong Remotion chỉ dùng mốc mới** —
không bao giờ trộn lẫn mốc raw và mốc clean (đây là bug dễ mắc nhất của cả pipeline).

`durationInFrames` = `Math.round(<duration của clean.mp4> * 30)` — đo bằng ffprobe, không cộng tay
từ cut_plan (sai số làm rớt/đóng băng frame cuối).

### Bước 4 — Dựng composition Remotion

Composition mới trong `remotion/app/src/`, **không sửa file của project cũ**:

```
src/
  NnsV1.tsx                 — AbsoluteFill gốc, lồng các layer theo z-index §5.4
  data/
    timelineV1.ts           — sinh TỰ ĐỘNG từ transcript_clean.json (script, không đánh tay)
    cutPlanV1.ts            — mốc các chỗ cắt (để đặt punch-in/SFX nếu cần)
  components/
    CaptionsV1.tsx          — §6
    BrandLogoV1.tsx         — §7
  layers/
    VideoLayerV1.tsx        — <OffthreadVideo> clean.mp4 + Ken Burns
public/<project>/
  footage/clean.mp4   fonts/BeVietnamPro-{400,700,800}.ttf   sfx/*.mp3   logos/*.svg
```

`timelineV1.ts` phải là file **sinh ra bằng script** từ `transcript_clean.json` (caption lines,
brand hits, sfx cues) — không gõ tay mốc giây. Gõ tay là quay lại đúng cái bệnh hard-code của skill cũ.

Đăng ký `<Composition id="NnsV1">` trong `Root.tsx` (thêm vào, không thay thế composition cũ).

### Bước 5 — QC rồi mới render

1. `npx remotion studio` — scrub tới: chỗ cắt đầu tiên, mỗi lần logo hiện, mỗi cue SFX, frame cuối.
2. `npx remotion still src/index.tsx NnsV1 <out.png> --frame=<N>` cho từng phần tử mới thêm —
   kiểm: chữ không wrap ngoài ý muốn, căn giữa đúng, không đè mặt (xem §6.3), logo không tràn khung.
3. Render: `npx remotion render src/index.tsx NnsV1 out/nns-v1-v1.mp4` — đặt tên tăng version,
   **không đè bản trước**.
4. Xoá bundle tạm sau vài lần render — cache Remotion phình rất nhanh, từng làm đầy ổ.

---

## 4. Luật cắt ậm ừ (phần lõi của skill này)

### 4.1 Khoảng lặng

| Loại | Ngưỡng | Xử lý |
|---|---|---|
| Lặng < 0.30s | — | **Giữ nguyên** (nhịp nói tự nhiên, cắt là nghe như robot) |
| Lặng 0.30–0.80s | | Thu về **0.16s** (giữ 1 nhịp thở) |
| Lặng > 0.80s | | Thu về **0.20s** |
| Lặng đầu file / cuối file | | Cắt sạch, chừa 0.10s |

Luôn để **padding 0.06s** hai bên mỗi mối cắt — cắt sát chữ quá sẽ cụt phụ âm đầu/cuối
(tiếng Việt mất dấu cuối nghe rất rõ).

### 4.2 Từ đệm — chỉ cắt khi ĐỨNG MỘT MÌNH

Danh sách ứng viên: `ừ, ờ, ừm, ờm, ậm, ậm ừ, à, ơ, ê, hử, kiểu, kiểu như, tức là, ý là, nói chung là, thì là, cái là, đó, đấy, ok`.

**Luật chặn cắt sai** (bắt buộc, vì phần lớn từ trên cũng là từ nghĩa thật):
- Chỉ cắt khi từ đó **kề một khoảng lặng ≥ 0.25s** ở ít nhất 1 phía → dấu hiệu đang nghĩ, không phải đang nói ý.
- **Không** cắt nếu nó nằm giữa câu liền mạch không có lặng (vd "cái **này** hay đấy", "**đó** là lý do").
- Từ ghép (`kiểu như`, `nói chung là`) chỉ cắt cả cụm, không cắt lẻ 1 nửa.
- Mọi lần cắt từ đệm đều phải xuất hiện trong `CUT_PLAN.md` kèm câu chứa nó → user tự veto.

### 4.3 Nói lặp / nói lại

Phát hiện 2-4 từ giống nhau lặp liền kề (`"tôi... tôi nghĩ là"`) → giữ **lần cuối** (lần cuối
thường trôi chảy nhất), cắt các lần trước. Ghi rõ lý do `nói lặp` trong CUT_PLAN.

### 4.4 Cách xử lý mối cắt về mặt hình ảnh

**Mặc định: jump-cut thẳng** — không transition, không crossfade. Đúng chất TikTok/kênh này,
và mối nối lộ nhẹ là *đặc điểm* của thể loại, không phải lỗi.

Có 2 tinh chỉnh được phép (không đổi nội dung, chỉ giấu mối nối):
- **Micro punch-in**: ở chỗ cắt dài (đoạn bỏ ≥ 1.2s), nhấn scale 1.0→1.04 trong 0.10s rồi thả về
  1.0 trong 0.45s (`back.out`) — mắt bị hút vào chuyển động nên không thấy hình nhảy.
- **SFX cực nhẹ** (`quick-swoosh`, -22dB) ở đúng frame cắt — tai "giải thích" được cú nhảy.

Áp micro punch-in cho **tối đa ~20% số mối cắt** (chọn các chỗ cắt dài nhất). Áp hết mọi mối cắt
sẽ thành video giật liên tục, mệt mắt.

---

## 5. Nguyên tắc chung của composition

### 5.1 Deterministic tuyệt đối
Cấm `Math.random()`, `Date.now()`, `new Date()` trong mọi file composition. Remotion render đa
luồng, mỗi frame tính độc lập — bất kỳ giá trị đổi theo lần gọi sẽ làm frame nhảy loạn.

### 5.2 Animation là hàm thuần của frame
Mọi chuyển động qua `useCurrentFrame()` + `interpolate()`/`spring()`. Không `setTimeout`,
không `.play()`/`.pause()` tay lên media — dùng `<OffthreadVideo>` / `<Audio>` để Remotion tự đồng bộ.

### 5.3 Ken Burns
Layer video full: 1 hàm `interpolate()` **liên tục duy nhất** trải qua toàn timeline (scale ~1.0→1.04),
KHÔNG dựng nhiều đoạn `fromTo` rời — nối nhiều đoạn gây giật scale ở mỗi ranh giới (bug đã biết ở
bản GSAP của 3 project HyperFrames).

### 5.4 Z-index
`video full (0) < logo/badge (10) < caption (30)`. Caption luôn trên cùng — nó là thứ người xem
đọc, không được để logo che.

---

## 6. Caption

### 6.1 Kiểu
Karaoke word-by-word: từ chưa tới màu mờ (`rgba(255,255,255,.55)`), từ đang nói sáng cam
`#FF9248` + glow, ramp 0.16s. Kế thừa thẳng cách làm của `CaptionsV2.tsx` — không phát minh lại.

### 6.2 Ngắt dòng
- **Tối đa 2 dòng, ~5-7 từ / dòng** — dài hơn thì người xem đọc không kịp trong nhịp cắt nhanh.
- Cắt dòng theo **cụm nghĩa** (theo dấu phẩy / mệnh đề), không cắt theo số ký tự.
- Mỗi từ là 1 `<span style={{display:'inline-block'}}>` — **bắt buộc**, xem §8.1.
- Một dòng caption kết thúc khi có lặng ≥ 0.35s hoặc đủ số từ, tính tự động từ transcript.

### 6.3 Vị trí (khung 9:16)
`bottom: 12%`, `left/right: 6%`, `fontSize ~52`, `fontWeight 700`, viền đen 4 hướng
(`-3px/3px` mỗi chiều) để đọc được trên mọi nền. **Không** đặt caption trong vùng y 43–65% —
đó là vùng mặt.

---

## 7. Logo tự chèn khi người nói nhắc tên thương hiệu

### 7.1 Dò tên
Quét `transcript_clean.json` tìm tên brand có trong `shared-sources/brand-logos/library.json`
(so theo `title` + `slug`, không phân biệt hoa/thường, có xét biến thể ASR hay nghe sai:
`Claude / Cờ lốt / Clau`, `HyperFrames / hai pơ phêm / hyper frame`, `ChatGPT / chat gờ pi ti`).

Mỗi lần khớp → 1 "brand hit" `{slug, tStart (mốc từ đầu tiên của tên), tEnd}`.

**Chống spam:** cùng 1 brand nhắc lại trong vòng **8s** thì KHÔNG hiện logo lần nữa. Nhắc tên
15 lần mà hiện logo 15 lần là rối mắt và trông như quảng cáo.

### 7.2 Thời gian hiện
Vào tại `tStart - 0.08s` (hiện hơi sớm nửa nhịp — cảm giác "ăn khớp" tốt hơn là hiện đúng lúc),
giữ **1.4s**, ra trong 0.25s. Vào bằng `spring` (scale 0.6→1, hơi overshoot) + fade; ra fade thuần.
Kèm SFX nhẹ `pop.mp3` hoặc `quick-ting.mp3` tại frame vào (xem §9 để không lạm dụng).

### 7.3 Vị trí — mặc định KHÔNG dán lên ngón tay
Remotion **không có motion tracking**. Có 2 chế độ:

- **`floating` (mặc định)** — badge bo tròn (nền cream `#FCF3E1`, đổ bóng mềm), logo ~150px,
  đặt ở **1/3 trên khung**, lệch về phía đối diện với hướng người nói đang nhìn. An toàn tuyệt đối,
  không bao giờ lệch.
- **`pinned` (chỉ khi user yêu cầu rõ)** — dán gần điểm người nói chỉ tay. Cách làm: trích frame
  tại `tStart` và `tStart+1.2s` (`ffmpeg -ss <t> -frames:v 1`), **xem thật bằng mắt**, đo toạ độ
  đầu ngón tay ở 2-3 frame mốc, rồi `interpolate()` toạ độ giữa chúng. Bắt buộc chụp
  `remotion still` xác nhận sau khi đặt. Nếu tay vung mạnh → báo user rằng `pinned` sẽ trượt và
  đề xuất `floating`; đặt logo **cạnh** ngón tay (như bong bóng đang chỉ vào) an toàn hơn dán đè lên.

### 7.4 File logo dùng bản nào
Ưu tiên **bản mark** (chỉ dấu hiệu): `claude.svg`, `hyperframes.svg`. Bản lockup của HyperFrames
(`hyperframes-lockup-*.svg`) **có kèm chữ "HeyGen"** — chỉ dùng khi VO thật sự nói "HeyGen".
Cần chữ thương hiệu thì dùng mark + tự đánh chữ bằng Be Vietnam Pro của video.

### 7.5 Không có logo thì viết chữ
Brand không có trong `library.json` → thử tải theo README của `brand-logos/` (Simple Icons →
Wikidata → site chính chủ). Vẫn không có → **viết tên bằng CHỮ**. **Tuyệt đối không tự vẽ, tự
chế, tự "vẽ lại cho giống" logo.** Cũng không tự tìm ảnh/video người thật trên mạng (bản quyền +
quyền hình ảnh).

---

## 8. Luật chữ (đã trả giá để biết)

### 8.1 Word-span atomicity + font
Font **Be Vietnam Pro** (`shared-sources/Font/Be_Vietnam_Pro/*.ttf`, khai báo `@font-face` với
`format("truetype")` — TTF chạy tốt trong Remotion, không cần convert woff2). **Không dùng Inter**:
subset latin của nó thiếu dấu tiếng Việt → browser fallback font ngay giữa 1 từ có dấu → coi đó
là điểm ngắt dòng hợp lệ → chữ vỡ kiểu `"nh" / "ất"`. Ngoài ra mọi span từ vẫn phải
`display: inline-block` để cụm ký tự+dấu không thể bị tách dòng.

Nếu `shared-sources/Font/` sau này có font khác (user tự tải), đọc thư mục đó trước khi mặc định
dùng Be Vietnam Pro — đó là kho font dùng chung.

### 8.2 Pill/badge auto-width
Mọi phần tử "co theo 1 dòng chữ ngắn" (badge tên brand, CTA pill) phải có `whiteSpace:'nowrap'` —
shrink-to-fit của browser tính sai khi text trộn font fallback, làm chữ tự xuống dòng và bóp méo
hình pill.

### 8.3 QC bằng ảnh, không bằng niềm tin
Mọi text/card/logo mới thêm phải chụp `remotion still` ở ≥1 frame đại diện trước khi coi là xong.
Kiểm: (a) không wrap ngoài ý muốn, (b) căn giữa/căn lề đúng thiết kế, (c) padding hai bên cân đối,
(d) không đè mặt. Layout auto-size rất dễ lệch theo nội dung thật — chỉ ảnh mới xác nhận được.

---

## 9. SFX — dồn vào hook, đừng rải đều

Bài học đã có: bản rải 53 cue đều cả video bị user cắt xuống còn ~20s đầu. **Mặc định là
hook-weighted**:

| Vùng | Mật độ |
|---|---|
| 0–20s (hook) | Dày — whoosh mỗi chuyển ý, pop/ting ở mỗi nhấn, riser trước câu chốt hook |
| 20s → hết | Thưa — chỉ ở logo pop, và ~20% mối cắt lớn |

Kho: `shared-sources/sound-effects/` (`whoosh.wav`, `quick-swoosh.mp3`, `pop.mp3`, `pop-2.mp3`,
`quick-ting.mp3`, `ding.mp3`, `riser-metallic.mp3`, `ka-ching.mp3`...). Đọc `USAGE_GUIDE.md` trước.

Mức: SFX nền `-20…-24dB` dưới giọng nói; SFX nhấn `-14…-18dB`. Giọng nói luôn là lớp to nhất —
SFX to hơn giọng là lỗi, không phải phong cách.

Gotcha ffmpeg (nếu mix ngoài Remotion): `drawbox` tham số `t` là **độ dày viền, không phải thời
gian**; `alimiter level=1` sẽ tự normalize lại và **triệt tiêu chính cái limit** vừa đặt (dùng
`level=disabled`); `loudnorm` 1 pass chạy chế độ động — muốn ổn định phải 2 pass.

BGM: **không tự thêm** — đang là quyết định mở, hỏi user.

---

## 10. Việc KHÔNG làm

- **Không** mượn mốc giây của `edit-remotion-nns` / `CAPCUT_BLUEPRINT_cuongmeai-tips.md` — timeline
  ở đây sinh từ transcript của file raw mới. Đọc skill cũ để hiểu *chất*, không để copy *số*.
- **Không** dựng tip-cycle / prompt-card / demo-screenshot / citation / PiP — ngoài phạm vi skill này.
  User muốn mấy thứ đó thì dùng `edit-remotion-nns`.
- **Không** sửa `CuongmeaiTips.tsx`, `CuongmeaiTipsV2.tsx`, hay `hyperframes/app/` — thêm composition
  mới, giữ bản cũ nguyên để đối chiếu.
- **Không** cắt trước khi user duyệt `CUT_PLAN.md` (§3 bước 2).
- **Không** tự viết lại nội dung, tự bỏ câu vì thấy "lan man", tự đổi thứ tự ý — chỉ cắt lặng,
  từ đệm, và nói lặp. Muốn cắt nội dung thì phải hỏi.
- **Không** tự vẽ/chế logo, không tự tải ảnh người thật (§7.5).
- **Không** dùng `-c copy` khi cắt, không để concat tụt xuống 25fps (§3 bước 3).
- **Không** trộn mốc thời gian raw và clean sau bước 3.
