---
name: edit-remotion-nns
description: "Build phong cách 'Cường mê AI' (AI Prompt Tips, 3-tip talking-head) bằng Remotion (React/TypeScript) thay vì HyperFrames, để so sánh trực tiếp 2 hướng build cùng 1 style DNA. Dùng lại đúng voice-over, transcript, blueprint (CAPCUT_BLUEPRINT_cuongmeai-tips.md), palette/typography/font, và cấu trúc tip-cycle đã đo đạc trong edit-style-nns — chỉ đổi engine dựng: HyperFrames data-* timing/GSAP-paused-timeline → Remotion <Sequence>/useCurrentFrame/interpolate. Output là 1 composition Remotion thật trong remotion/app/ + video render, KHÔNG phải blueprint văn bản. Trigger: '/edit-remotion-nns', 'build lại video Cường mê AI bằng Remotion', 'thử Remotion cho video này xem khác HyperFrames chỗ nào'."
---

# Edit Remotion — "Cường mê AI" (Remotion port của edit-style-nns)

> Đây là bản dựng SONG SONG bằng Remotion cho đúng 1 style đã có bản HyperFrames
> (`hyperframes/app/`, render `cuongmeai-tips-v5.mp4`, 1080×1920 @30fps, 50.87s).
> Mục đích: so sánh 2 engine trên cùng 1 nguồn — không phải tạo phong cách mới,
> không phải viết blueprint mới. Style DNA (nhịp cắt, tip-cycle, màu, chữ) đọc từ
> `edit-style-nns/SKILL.md`; timeline/cut points chi tiết đọc từ
> `SON_AI_VIDEO/CAPCUT_BLUEPRINT_cuongmeai-tips.md`. Đọc cả hai trước khi build.

---

## 1. Nguồn dùng lại (không tạo mới, không suy đoán lại)

| Thứ cần | Lấy ở đâu |
|---|---|
| Style DNA (cấu trúc hook/tip-cycle/outro, nhịp cắt, chi tiết hiệu ứng) | `.claude/skills/edit-style-nns/SKILL.md` |
| Timeline giây-theo-giây, cut points, script overlay | `SON_AI_VIDEO/CAPCUT_BLUEPRINT_cuongmeai-tips.md` |
| Transcript word-level (ASR đã hiệu chỉnh tay) | `SON_AI_VIDEO/hyperframes/app/transcript.json` |
| Voice-over / raw footage gốc | `C:\Users\admin\Downloads\0726(2).mp4` (xem CAPCUT_BLUEPRINT để xác nhận path còn đúng) |
| Palette, font, layout THẬT đã approved (nguồn thị giác chính xác nhất — ưu tiên hơn cả style DNA khi có xung đột) | `SON_AI_VIDEO/hyperframes/app/index.html` + `hyperframes/app/assets/` |
| Bản dựng đối chứng để so sánh | `SON_AI_VIDEO/hyperframes/app/renders/cuongmeai-tips-v5.mp4` |
| Logo/brand chung | `SON_AI_VIDEO/shared-sources/` (giữ nguyên vị trí, không copy đè) |

Không đọc lại raw footage/transcript bằng ffprobe/whisper lần nữa — dữ liệu đã đo, dùng lại nguyên.

## 2. Contract dịch: HyperFrames → Remotion

HyperFrames và Remotion cùng nguyên tắc lõi: **animation là hàm thuần của thời điểm, seek-safe, không phụ thuộc wall-clock**. Chỉ khác API:

| Khái niệm HyperFrames | Tương đương Remotion |
|---|---|
| `data-start`, `data-duration` (giây) trên `.clip` | `<Sequence from={Math.round(start*fps)} durationInFrames={Math.round(dur*fps)}>` (frame, không phải giây) |
| GSAP timeline `paused: true`, seek bằng playhead | `useCurrentFrame()` + `interpolate()` / `spring()` — component tự tính trạng thái theo frame hiện tại, không có timeline global phải seek |
| `class="clip"` / tracks song song | Nhiều `<Sequence>`/`<AbsoluteFill>` lồng nhau trong 1 `<Composition>` |
| Framework tự play/pause media theo playhead | `<OffthreadVideo>`, `<Audio>` của Remotion — tự đồng bộ theo frame, không tự gọi `.play()/.pause()` |
| Biến project (`hyperframes.json` variables) | `defaultProps` của `<Composition>` + TypeScript interface |
| Cấm `Math.random()`/`Date.now()` trong composition (đã áp dụng ở HyperFrames) | Y hệt — Remotion render đa luồng, mỗi frame render độc lập, phải deterministic tuyệt đối |
| `npx hyperframes render` | `npx remotion render` (script `render` đã có sẵn trong `remotion/app/package.json`) |

fps/canvas: `<Composition width={1080} height={1920} fps={30} durationInFrames={~1526}>` — khớp đúng số đo ffprobe của bản HyperFrames (50.87s × 30fps), không tự chọn số khác.

## 3. Cấu trúc file trong `remotion/app/`

```
remotion/app/src/
  Root.tsx                 — registerRoot, khai báo <Composition id="CuongmeaiTipsRemotion">
  CuongmeaiTips.tsx         — component gốc, AbsoluteFill lồng theo thứ tự z-index như index.html
  scenes/Hook.tsx           — 0–8.4s
  scenes/TipCycle.tsx       — 1 component tái dùng ×3 (tip 1/2/3), nhận props {index, promptText, ...}
  scenes/Outro.tsx          — 63.8–67.6s (đổi mốc theo timeline thật 50.87s nếu blueprint/video lệch)
  layers/VideoLayer.tsx     — video-wrap + pip-mask, crossfade opacity thuần (giống nguyên tắc HyperFrames: KHÔNG animate scale/x/y của layer video)
  theme.ts                  — hằng số màu/font, copy nguyên giá trị từ :root trong index.html (--cream #FCF3E1, --brown #302221, --orange #CE763A, --red #C41E20)
public/
  fonts/                    — copy nguyên `hyperframes/app/assets/fonts/*.woff2`
  footage/                  — video gốc dùng cho VideoLayer
```

Copy asset bằng file thật (không symlink) để `remotion/app/` độc lập, không phụ thuộc `hyperframes/app/` còn tồn tại.

## 4. Cơ chế BẮT BUỘC — rút từ `index.html` thật, không phải tuỳ chọn

v1 của skill này (bản build đầu) đã bỏ sót toàn bộ mục này vì chỉ đọc lướt `index.html`
thay vì đọc hết. Kết quả là bản Remotion "thô" hơn hẳn bản HyperFrames dù cùng 1 style.
Mọi bản build sau BẮT BUỘC áp dụng đủ các cơ chế dưới — chúng đã đo/đã duyệt, không phải
đề xuất mới.

### 4.1 Video-mode state machine (toPip / toFull / toHidden)

Video luôn ở 1 trong 3 mode, chuyển bằng crossfade opacity 0.45s `sine.inOut` (Remotion:
`interpolate` trên 1 hàm `videoMode(t)` chung, KHÔNG per-segment ad-hoc):

- **full**: video full-bleed hiện (Kiểu A — hook/talking-head/stat/citation).
- **pip**: video full ẩn, thay bằng vòng tròn PiP 460px cố định ở `bottom:260px` (Kiểu B —
  prompt/demo/stinger/recap).
- **hidden**: cả 2 ẩn hoàn toàn (chỉ dùng cho Headline Payoff — card che kín toàn khung).

Mốc chuyển đúng theo `index.html` dòng 397-406 (giây tuyệt đối):
`toPip(6.94) → toFull(7.84) → toPip(9.28) → toHidden(17.32) → toPip(19.84) → toFull(20.74)
→ toPip(23.62) → toFull(32.72) → toPip(34.40) → toFull(47.70)`. Ngoài các mốc này là "full"
(mặc định từ 0). Lưu ý stinger 2 và 3 nằm LỒNG trong 1 khoảng pip liên tục (không tự thêm
cặp toPip/toFull riêng cho từng stinger — sẽ gây nhấp nháy sai).

### 4.2 Z-index / layering — PiP LUÔN nổi trên card

Thứ tự đúng (thấp→cao): video full (0) < card nội dung (1) < **PiP tròn (5)** < caption
(trên cùng). PiP phải có z-index CAO HƠN card, không phải thấp hơn — nếu không sẽ bị card
che kín (đây là nguyên nhân chính khiến v1 bị "nửa dưới trống trơn, không thấy mặt").

### 4.3 Layout Kiểu B — chừa chỗ cho PiP, KHÔNG center nội dung theo full khung

Card Kiểu B (`promptCard`/`demoScreenshot`/`recapBadge`) dồn nội dung lên khu TRÊN, chừa
khoảng trống THẬT ở dưới cho PiP hiện qua — không phải `align-items:center` trên toàn khung
1920px. Copy đúng padding gốc: `padding: 200px <ngang> 780px` (top 200px chứa nội dung,
bottom 780px để trống cho vòng PiP). Stinger cũng KHÔNG center giữa khung — dùng
`padding-top: 200px` (dòng 86-87), vì center-giữa sẽ rơi đúng vùng mặt (y 43–65%) nếu video
full đang hiện.

### 4.4 Hook — spotlight vignette + face-zoom + SFX

3 thứ chạy đồng thời 0–1.75s (dòng 416-422): (a) `spotlight-mask` — radial-gradient vòng
tròn 480px tại 50% 53%, trong suốt ở tâm, tối dần ra ngoài (`rgba(0,0,0,.72)` ở mép), fade
opacity 0→1 trong 0.05–0.35s rồi tắt ở 1.15–1.55s; (b) camera zoom nhẹ vào mặt: scale
1.0→1.15 (0.05–0.40s) rồi về 1.0 (1.10–1.70s), transform-origin 50% 53%; (c) SFX whoosh tại
0.02s.

### 4.5 Punch-in — nhấn camera + SFX ở cao trào/cuối câu

Tại mỗi mốc cao trào (dòng 425-434): scale 1.0→~1.05 rất nhanh (0.10s, ease-in) rồi thả về
1.0 chậm hơn (0.45s, `back.out`). Mốc + SFX đi kèm: 5.05 (pop, "...gấp 10 lần"), 8.85 (không
SFX riêng), 23.35 (pop, "...cực kỳ đỉnh"), 34.05 (không SFX riêng), 48.25 (không SFX riêng),
50.25 (pop, giữ nguyên không thả — beat chốt cuối). Whoosh riêng cho stinger tại 6.94/19.84/
31.82 (trùng mốc toPip).

### 4.6 Ken Burns — camera trôi liên tục suốt video

Áp dụng cho layer video full (không áp dụng lên PiP — PiP tĩnh tuyệt đối). 4 khung tốc độ
(dòng 412-414): `[0,9.28]→1.035`, `[9.28,17.32]→1.025`, `[19.84,34.40]→1.03`,
`[34.40,50.85]→1.04` (scale bắt đầu 1.0 ở mỗi khung, "trôi" dần lên target).

**Khác 1 điểm CÓ CHỦ ĐÍCH so với bản GSAP gốc**: dựng bằng 1 hàm `interpolate()` duy nhất
chạy qua toàn bộ các mốc khung liền nhau (input range nối tiếp `[0,9.28,17.32,19.84,34.40,50.85]`),
KHÔNG dựng 4 `fromTo` riêng từng khung như GSAP. Bản GSAP bị giật scale nhẹ ở mỗi ranh giới
khung (bug đã biết, chưa fix ở cả 3 project HyperFrames — xem memory `project_son_ai_video_buoc7_ai`);
dùng 1 interpolate liên tục tránh được bug này tự nhiên. KHÔNG tự mang cách sửa này quay lại
vá 3 project HyperFrames — đó là quyết định riêng, cần hỏi user trước.

### 4.7 SFX — copy asset, không tự tạo mới

Copy đúng 2 file `hyperframes/app/.media/audio/sfx/sfx_001.mp3` (whoosh) và `sfx_002.mp3`
(pop/ding) vào `remotion/app/public/sfx/`. Trigger bằng `<Audio>` tại đúng giây trong 4.4/4.5
— không tự tìm SFX khác, không tự đổi mốc.

### 4.8 Word-span atomicity — chặn line-break giữa từ

Font Inter chỉ có subset "latin" (không có dấu tiếng Việt) → browser fallback sang font khác
NGAY GIỮA 1 từ có dấu, và coi điểm đổi font là 1 điểm ngắt dòng hợp lệ → chữ bị tách kiểu
"nh" / "ất". Mỗi span từ (karaoke word-by-word) BẮT BUỘC có `display: inline-block` (tương
đương `.w{display:inline-block}` dòng 57) để cả cụm ký tự+dấu không thể bị tách dòng, bất kể
có đổi font ở giữa hay không.

**Font mặc định cho mọi build sau — Be Vietnam Pro (Cập nhật vòng 7):** phát hiện thực tế khi
build cho video mới — Inter (subset latin) khiến chữ có dấu bị "vỡ" (rơi vào đúng lỗi mục 4.8
ở trên, không chỉ lý thuyết). User đã tự tải font hỗ trợ đủ dấu tiếng Việt, để cố định tại
`SON_AI_VIDEO/shared-sources/Font/Be_Vietnam_Pro/*.ttf` — **dùng font này làm mặc định cho MỌI
build Remotion mới từ giờ**, không dùng lại Inter nữa. Copy 2-3 weight cần (Regular 400, Bold
700, có thể thêm ExtraBold 800 cho headline) vào `public/fonts.../` của project, khai báo
`@font-face` với `format("truetype")` (không cần convert sang woff2 — TTF chạy tốt trong
Remotion/Chrome, không đáng công convert). Nếu `shared-sources/Font/` sau này có thêm font
khác (user tự tải), đọc thư mục đó trước khi mặc định dùng Be Vietnam Pro — đây là kho font
dùng chung, không riêng cho 1 project.

### 4.9b Pill/badge auto-width — luôn chặn wrap ngoài ý muốn

Mọi phần tử dạng "pill/badge co theo đúng 1 dòng chữ ngắn cố định" (stat pill, CTA pill —
KHÔNG áp dụng cho chip/box đã thiết kế đa dòng như Recap) phải có `whiteSpace: 'nowrap'`
trên phần tử chứa chữ. Lý do: box auto-width (`left:50%` không kèm `right`, hoặc
`width:'fit-content'`) tin vào phép tính "shrink-to-fit" của trình duyệt — phép tính này có
thể ra sai (co hẹp hơn cần) khi text trộn font fallback (xem §4.8) hoặc gặp edge-case CSS,
khiến chữ tự xuống dòng và bóp méo hình dạng pill đã tính theo 1 dòng (bo tròn không còn
khớp, đệm trên/dưới lệch). `whiteSpace:'nowrap'` loại bỏ khả năng này hoàn toàn, không phụ
thuộc việc đoán đúng nguyên nhân co hẹp. Sau khi thêm, LUÔN chụp `remotion still` tại đúng
frame của phần tử đó để xác nhận bằng mắt — không suy đoán từ code là đủ.

**Quy tắc chung hơn (áp dụng mọi phần tử hiển thị, không chỉ pill):** mọi text/card mới thêm
phải được QC bằng `remotion still` ở ít nhất 1 frame đại diện trước khi coi là xong — kiểm
tra cụ thể: (a) không bị wrap ngoài ý muốn, (b) căn giữa/căn lề đúng như thiết kế (không lệch
trái/phải/trên/dưới so với khung chứa), (c) padding hai bên cân đối. Đừng chỉ tin vào việc
code "nhìn có vẻ đúng" — layout auto-size (`auto`, `fit-content`, flex canh giữa) rất dễ sai
lệch theo nội dung thật, chỉ ảnh chụp mới xác nhận được.

### 4.9 Citation card — không tự tìm ảnh người thật

Mặc định vẫn là thẻ chữ (kicker/badge/tên/chức danh), không kèm ảnh/video. KHÔNG tự tìm/tải
ảnh hoặc video của người được trích dẫn (ví dụ Ethan Mollick) trên mạng — rủi ro bản quyền +
quyền hình ảnh cá nhân, blueprint gốc đã ghi rõ lý do né. Chỉ thêm ảnh/video khi user tự cung
cấp file họ đã có quyền dùng.

## 5. Trình tự build

1. Đọc `edit-style-nns/SKILL.md` + `CAPCUT_BLUEPRINT_cuongmeai-tips.md` — lấy mốc giây từng đoạn.
2. Copy asset cần (font, footage, audio, **SFX** — xem §4.7) vào `remotion/app/public/`.
3. Viết `theme.ts` trước — màu/font là thứ dễ soát nhất, làm nền cho mọi scene.
4. Viết `videoMode(t)` (§4.1) + z-index/layout đúng (§4.2, §4.3) trước khi viết scene — đây là
   bộ khung mọi card khác dựa vào, viết scene trước khi có cái này là nguồn gốc bug v1.
5. Viết từng scene theo đúng thứ tự timeline (Hook → TipCycle×3 → Outro), áp dụng §4.4-4.9 cho
   đúng scene tương ứng. Mỗi scene xong thì `npx remotion studio` xem trực tiếp tại đúng mốc
   giây tương ứng trong blueprint trước khi qua scene kế — không viết hết rồi mới xem lần đầu.
6. Ráp `CuongmeaiTips.tsx` lồng các scene bằng `<Sequence>` theo mốc đã dịch sang frame.
7. QC bằng `npx remotion studio` (xem §6) — đối chiếu TỪNG mục 4.1–4.9 có mặt đủ, không chỉ
   đối chiếu vị trí/màu chữ. So trực tiếp cạnh `cuongmeai-tips-v5.mp4` ở đúng timestamp.
8. Render: `npm run render` (trong `remotion/app/`) → xuất vào `remotion/app/out/`, đặt tên
   version tăng dần (`cuongmeai-tips-remotion-v2.mp4`, ...) — không đè lên bản trước.

## 6. Xem trực tiếp bằng Remotion Studio (không cần render mới đi xem)

`npx remotion studio` (trong `remotion/app/`) mở 1 server local có UI scrub timeline theo
frame, thấy rõ từng `<Sequence>` xếp lớp — minh bạch hơn xem video render xong vì soát được
đúng frame nào đang lỗi, không phải đoán qua playback. Dùng để QC §4.1-4.9 trước khi render
tốn thời gian. Mở qua Browser pane (`preview_start`) khi cần xem cùng user.

## 7. Việc KHÔNG làm

- Không sửa `hyperframes/app/` hay render lại bản HyperFrames trong lúc build bản Remotion — đây là bản đối chứng, giữ nguyên để so sánh công bằng.
- Không tự đổi bố cục/màu/nhịp cắt so với bản đã approved — mục tiêu là port 1:1 engine, không phải "cải tiến" style. Nếu thấy Remotion cho phép làm khác hay hơn, ghi chú lại để hỏi user sau, không tự áp dụng.
- Không thêm BGM ở bản Remotion nếu bản HyperFrames chưa có — giữ cùng điều kiện so sánh (BGM đang là quyết định mở, xem `project_son_ai_video_cuongmeai`/`buoc7_ai`).
- Không tự đổi nhịp/thời gian đã đo (ví dụ kéo dài stinger) trừ khi user xác nhận rõ — xem §4.1 cho mốc đúng.
- Không tự tìm ảnh/video của người có thật trên mạng để làm citation visual — xem §4.9.
- Không gộp việc "nâng cấp demo visuals thành ảnh/video động" vào bản fix-bug này — đó là 1 quyết định DNA riêng, áp dụng cho cả 3 project, cần 1 vòng plan khác (đã thống nhất với user tách riêng).
