# Shared Sources — kho tài nguyên dùng chung cho mọi skill dựng video

Thư mục này (`SON_AI_VIDEO/shared-sources/`) là kho tài nguyên **dùng chung giữa
mọi project và mọi skill edit** (`edit-style-*`, `script-writer` mục demo, và bất
kỳ `edit-style-<tên>` nào tạo ra sau này qua `extract-edit-style`). Khác với
`assets/` bên trong từng project HyperFrames (chỉ dùng riêng cho project đó), file
ở đây được phép tái sử dụng qua nhiều video/nhiều project.

**Quy tắc dùng chung:**
- User tự thêm file vào đây bất cứ lúc nào (video mẫu, ảnh chụp màn hình, sticker,
  nhạc nền, SFX riêng, B-roll đã quay sẵn...) — mỗi lần thêm, ghi 1 dòng vào bảng
  manifest bên dưới để skill biết file đó dùng cho việc gì.
- Mọi skill edit khi cần 1 loại tài nguyên (demo screenshot, B-roll, sticker...)
  **luôn đọc bảng manifest này trước** để tìm file có sẵn, trước khi tự tạo mới
  (vd tự thao tác Chrome quay demo) hoặc trước khi báo "thiếu, cần hỏi user".
- Khi 1 skill tự tạo ra tài nguyên mới (vd demo screenshot tự chụp qua Chrome, đã
  được user đồng ý), lưu file vào đây (không chỉ vào `assets/` riêng của 1
  project) và tự thêm 1 dòng manifest, ghi rõ project/ngày nào đã tạo ra nó — để
  video sau tái dùng được nếu hợp.
- Skill KHÔNG được tự ý xoá hoặc ghi đè file đã có trong manifest — nếu cần thay,
  hỏi user trước (đây là kho tài nguyên lâu dài, không phải thư mục tạm).

## Manifest

| Thư mục/File | Loại | Dùng cho / mô tả | Người/skill thêm | Ngày thêm |
|---|---|---|---|---|
| `sound-effects/` | SFX (~90 file, mp3/wav) | Thư viện SFX dùng chung — **tự có index riêng** (`sound-effects/library.json` + tags + `README.md`), KHÔNG liệt kê từng file ở đây. Đọc mục "Thư viện SFX" bên dưới trước khi dùng — có cảnh báo bản quyền cần lưu ý. | User | 2026-08-09 |
| `brand-logos/` | Logo SVG (~120 file, Simple Icons/Wikidata) | Logo thương hiệu (Claude, OpenAI, Gemini, DeepSeek, Qwen, Mistral, HuggingFace, Perplexity, LangChain, Ollama, và nhiều brand ngoài AI) để chèn khi kịch bản/VO nhắc tới tên 1 công cụ/thương hiệu cụ thể. **Tự có index riêng** (`brand-logos/library.json` + `README.md`) — đọc mục "Thư viện Brand Logos" bên dưới trước khi dùng, có lưu ý về nhãn hiệu (trademark) cần biết. | User | 2026-08-09 |
| `Font/Be_Vietnam_Pro/` | Font TTF (đủ dấu tiếng Việt, 18 weight/style) | **Font mặc định cho mọi build Remotion mới** — thay Inter (chỉ có subset latin, gây vỡ chữ có dấu, xem `edit-remotion-nns` §4.8 "Cập nhật vòng 7"). Copy weight cần (400/700/800) vào `public/fonts.../` của project, `@font-face format("truetype")`. | User | 2026-08-15 |
| `demo-screens/5-ma-bi-mat-chatgpt-2026-08-10.md` | Link chat ChatGPT thật (5 đoạn, không phải ảnh tĩnh) | 5 ví dụ thật cho blueprint `CAPCUT_BLUEPRINT_5-ma-bi-mat-gpt-secret-code-style.md` — 1 link/mã (SeekHuman/ELI10/X10Think/KillCritic/ALT3), kèm prompt đã dùng + kết quả nổi bật. Mở link + tự screen-record khi dựng. | Claude (qua Chrome thật của user) | 2026-08-10 |
| `../video_demo/demo1_clarifying_questions_2026-08-15.gif` | GIF quay màn hình thật (Claude.ai, 14 frame) | Demo cho `edit-remotion-nns`/`edit-style-nns` tip 1 (0726.mp4 mới) — prompt: "...hãy đặt cho tôi những câu hỏi làm rõ vấn đề cho đến khi bạn tự tin 95%...". Ghi lại Claude đặt 3 câu hỏi làm rõ trước khi lên kế hoạch. **CHỜ USER DUYỆT** trước khi coi là chính thức dùng trong build. | Claude (qua Chrome thật của user, claude.ai) | 2026-08-15 |
| `../video_demo/demo2_top1percent_reframe_2026-08-15.gif` | GIF quay màn hình thật (Claude.ai, 6 frame) | Demo cho tip 2 (Ethan Mollick/top 1%) — prompt: "...người thuộc top 1% xuất sắc nhất trong lĩnh vực này sẽ nghĩ gì về điều này". Ghi lại Claude reframe câu hỏi nghỉ việc khởi nghiệp kiểu top 1%. **CHỜ USER DUYỆT**. | Claude (qua Chrome thật của user, claude.ai) | 2026-08-15 |
| `../video_demo/demo3_challenge_perspective_2026-08-15.gif` | GIF quay màn hình thật (Claude.ai, 9 frame) | Demo cho tip 3 (thách thức góc nhìn) — prompt: "...hãy trình bày lại vấn đề này theo cách làm thách thức hoàn toàn góc nhìn của tôi...". Ghi lại Claude phản biện quan điểm "tuần làm việc 4 ngày". **CHỜ USER DUYỆT**. | Claude (qua Chrome thật của user, claude.ai) | 2026-08-15 |

## Thư viện SFX (`sound-effects/`)

Thư mục này tự quản lý bằng `library.json` (mỗi file có `tags`, `description`,
`durationMs`, `source`, `license`) — đọc `sound-effects/README.md` trước khi dùng
hoặc thêm file mới, đừng thêm dòng thủ công vào bảng Manifest ở trên cho từng SFX
lẻ. Điểm quan trọng cần nhớ khi 1 skill edit muốn dùng SFX từ đây:

- **Cảnh báo bản quyền**: phần lớn file trong này KHÔNG có giấy phép rõ ràng —
  README của thư viện nói thẳng "không khuyến khích dùng cho video thương mại".
  Nếu video sắp làm là nội dung thương mại/kiếm tiền, hỏi user trước khi lấy SFX
  từ đây, hoặc ưu tiên file có `license` sạch (`CC0-1.0`, `Pixabay`...) ghi rõ
  trong `library.json` — không mặc định coi cả thư viện là an toàn dùng thoải mái.
  Tuyệt đối không dùng các file nhận ra ngay là trích đoạn phim/game/nhãn hiệu
  (jingle nổi tiếng...) — README liệt kê rõ loại này.
- **Cách tìm SFX**: đọc `sound-effects/USAGE_GUIDE.md` trước — đã xếp theo TÌNH
  HUỐNG DỰNG VIDEO thật (chuyển tip, nhấn mạnh, reveal payoff, sai/lỗi, hài,
  gõ phím demo, đếm số, hồi hộp, tiền/CTA...), khớp đúng các beat trong
  `edit-style-cuongmeai`/`edit-style-gpt-secret-code`. Chỉ cần tra `library.json`
  trực tiếp khi muốn lọc theo `tags` cho nhu cầu ngoài các tình huống đã liệt kê.
  File này cũng đã xác nhận thật (mở/ffprobe) 18 entry trong `library.json` bị
  thiếu file trên đĩa (đoạn nhận diện bên thứ 3, bị `.gitignore`) — đừng tham
  chiếu tới chúng.
- **Khi dùng cho 1 video cụ thể**: copy file cần vào `assets/` riêng của project
  đó (không trỏ thẳng vào `shared-sources/` từ composition) — đúng quy ước "mỗi
  project tự chứa đủ asset của nó" đã ghi trong `sound-effects/README.md`.

## Thư viện Brand Logos (`brand-logos/`)

Logo SVG các thương hiệu (chủ yếu công nghệ/AI — sẵn `claude.svg`, `openai.svg`,
`googlegemini.svg`, `deepseek.svg`, `qwen.svg`, `mistralai.svg`,
`huggingface.svg`, `perplexity.svg`, `langchain.svg`, `ollama.svg`,
`anthropic.svg`... rất hợp cho series "30 ngày tìm hiểu bạn AI" của
`script-writer` mỗi khi cần Tool Card nêu tên công cụ) — cùng nhiều brand khác
(mạng xã hội, ngân hàng, hãng công nghệ...). Tự quản lý bằng `library.json`
(`slug`, `title`, `color`, `file`, `source`, `license`) — đọc
`brand-logos/README.md` trước khi dùng hoặc thêm mới. Điểm quan trọng:

- **Đây là NHÃN HIỆU của chủ thương hiệu, không phải asset tự do** — dùng để
  NHẮC TỚI 1 thương hiệu (nêu tên công cụ, so sánh) là bình thường, nhưng không
  được dùng theo cách khiến người xem tưởng thương hiệu đó tài trợ/xác nhận nội
  dung video. Không tự chỉnh sửa/tái tạo logo theo cách sai khác bản gốc.
- **Nếu thiếu 1 brand cần dùng**: kiểm tra `library.json` trước; nếu chưa có,
  server dự án có thể tự tải qua Simple Icons/Wikidata (xem lệnh trong README) —
  nếu không tự tải được, viết tên thương hiệu bằng CHỮ, **tuyệt đối không tự vẽ
  hay tự chế logo** thay thế.
- **HyperFrames (thêm 2026-08-17)**: Simple Icons/Wikidata KHÔNG có brand này —
  file tải trực tiếp từ site chính chủ `hyperframes.dev` (dự án open-source của
  HeyGen). 3 file: `hyperframes.svg` (chỉ dấu hiệu, gradient cyan→green, đặt được
  trên mọi nền — **mặc định dùng file này**), `hyperframes-lockup-dark.svg` (lockup
  "HeyGen HyperFrames" mực đen, cho nền sáng/cream), `hyperframes-lockup-light.svg`
  (mực trắng, cho nền tối). Lưu ý: bản lockup có kèm chữ "HeyGen" — nếu VO chỉ nói
  "HyperFrames" thì dùng file mark rồi tự đánh chữ theo font của video.
- **Khi dùng cho 1 video cụ thể**: copy file cần vào `assets/` riêng của project
  đó trước khi tham chiếu trong composition — không trỏ thẳng vào
  `shared-sources/` (cùng quy ước với `sound-effects/`).

## Cấu trúc thư mục con gợi ý (tạo khi cần, không bắt buộc từ đầu)

- `demo-screens/` — ảnh/luồng chụp giao diện Claude/ChatGPT thật (theo mục 7 của
  `edit-style-cuongmeai`).
- `broll/` — video/ảnh B-roll dùng lại được nhiều video (stock, minh hoạ...).
- `sound-effects/` — đã có, xem mục riêng ở trên.
- `brand-logos/` — đã có, xem mục riêng ở trên.
- `stickers/` — sticker/meme phản ứng hay dùng lặp lại.
