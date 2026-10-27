---
name: nns-auto-sub
description: Chèn sub karaoke word-by-word tiếng Việt rồi burn thẳng vào video. Input là 1 video có tiếng nói (--video) + nơi lưu kết quả (--out), tuỳ chọn --resources trỏ tới thư mục có Font/ riêng; output là video đã có chữ cháy sẵn kèm file .ass, .words.json (transcript có mốc từng từ) và .plan.json. Tự nhận dạng lời nói bằng faster-whisper, tự sửa tên riêng bị nghe sai (Cloud→Claude, Hyperframe→HyperFrames), tự chặn độ dài từ bị Whisper phình, tô vàng đúng từ đang được nói, và đo lại bằng pixel để chắc chữ có thật sự hiện. Trigger '/nns-auto-sub', hoặc các câu như 'thêm sub cho video này', 'chèn caption karaoke tiếng Việt', 'làm phụ đề chạy theo từng chữ', 'burn sub vào video giúp tôi', 'video này thiếu chữ, thêm caption vào'.
---

# nns-auto-sub — sub karaoke word-by-word tiếng Việt

## BƯỚC 0 — BẮT BUỘC, LÀM TRƯỚC MỌI THỨ

Ngay khi skill này được gọi, TRƯỚC KHI làm bất cứ việc gì, chạy:

    python <skill>/scripts/preflight.py --video "<video>" [--resources "<thư-mục>"]

Đọc kết quả:

- Preflight in "ĐẦY ĐỦ" -> làm tiếp các bước dưới.
- Preflight in "THIẾU ..." -> DỪNG NGAY. Không cắt, không render, không tạo file gì.
  Đưa NGUYÊN khối hướng dẫn mà preflight in ra cho người dùng, rồi HỎI họ:
  "Thiếu <n> thứ ở trên. Bạn làm theo hướng dẫn rồi báo tôi, hoặc gửi cho tôi
  <thứ còn thiếu> để tôi chạy tiếp?"
  Chờ người dùng trả lời. TUYỆT ĐỐI không tự đoán, không tự thay bằng thứ khác,
  không bỏ qua bước đó để "chạy tạm".

- Nếu người dùng KHÔNG đưa --video: hỏi đường dẫn video thô trước khi làm gì.

## Cần gì để chạy

| Thứ cần | Bắt buộc? | Nếu chưa có thì làm gì (lệnh cụ thể) |
|---|---|---|
| `ffmpeg` + `ffprobe`, có `libass` | Bắt buộc | Windows: tải bản **full** ở https://www.gyan.dev/ffmpeg/builds/ , giải nén ra `C:\ffmpeg`, thêm `C:\ffmpeg\bin` vào PATH. macOS: `brew install ffmpeg`. Linux: `sudo apt install ffmpeg`. Kiểm: `ffmpeg -filters` phải có dòng `subtitles` |
| `python` 3.8+ | Bắt buộc | Tải ở https://www.python.org/downloads/ |
| `numpy` | Bắt buộc | `pip install numpy` |
| `faster-whisper` | Bắt buộc | `pip install faster-whisper` |
| Model Whisper `large-v3` | Bắt buộc, tự tải lần đầu (~1.5 GB) | Lần chạy đầu cần mạng. Máy yếu / không muốn tải nhiều: thêm `--model small` |
| Font có dấu tiếng Việt | Bắt buộc — **ĐÃ KÈM SẴN trong skill** | Đã có `assets/fonts/BeVietnamPro-ExtraBold.ttf`. Muốn font khác: tạo `<thư-mục>/Font/`, bỏ file `.ttf` vào, gọi thêm `--resources "<thư-mục>"` |
| `--resources` | Không bắt buộc | Chỉ cần khi muốn dùng font riêng của bạn. **Đã đưa `--resources` mà trong đó không có font tiếng Việt thì skill DỪNG**, không lặng lẽ tụt về font kèm sẵn — muốn dùng font kèm sẵn thì bỏ hẳn tham số `--resources` |
| GPU NVIDIA | Không bắt buộc | Có thì tự dùng (nhanh hơn ~5 lần). Không có thì tự chạy CPU |

**Bước 1 luôn là chạy preflight. Preflight báo THIẾU thì dừng lại, làm theo hướng
dẫn nó in ra, không được chạy tiếp.**

## Chạy một lệnh là xong

```bash
python scripts/autosub.py --video "video_tho.mp4" --out "video_co_sub.mp4"
```

Lệnh này chạy đủ 6 bước và **chỉ báo xong khi `verify.py` đo lại và báo ĐẠT**:

| Bước | Script | Làm gì | File sinh ra |
|---|---|---|---|
| 0 | `preflight.py` | Kiểm ffmpeg / thư viện / video / font | — |
| 1 | `transcribe.py` | Nhận dạng lời nói, có mốc **từng từ** | `<out>.words.json` |
| 2 | `fix_tokens.py` | Sửa tên riêng nghe sai + chặn độ dài từ bị phình | `<out>.fixed.json` |
| 3 | `build_ass.py` | Gom từ thành cụm, xuất sub karaoke | `<out>.ass`, `<out>.plan.json` |
| 4 | `burn.py` | Vẽ chữ vào video (tiếng giữ nguyên, không mã hoá lại) | `<out>` |
| 5 | `verify.py` | **Đo pixel** để chắc chữ có thật sự hiện | — |

Thêm `--dry-run` để chỉ lập kế hoạch mà **không xuất file nào**:

- Video **chưa từng** nhận dạng: `--dry-run` kiểm input, in ra 5 bước sẽ chạy rồi
  dừng bình thường (exit 0). Chưa có transcript thì chưa thể biết cụm chữ nào,
  nên nó nói rõ điều đó chứ không đoán.
- Muốn xem kế hoạch **chi tiết** (từng cụm, màu, chỗ đặt) mà vẫn chưa vẽ gì vào
  video: chạy `transcribe.py` trước (chỉ ghi 1 file `.words.json`), rồi chạy lại
  với `--dry-run`.

Transcript được **cache** cạnh `--out`. Sửa màu, đổi chỗ đặt, gom cụm lại — chạy lại
từ bước 2, **không phải nhận dạng lại**.

## Đặt sub ở đâu — phần dễ sai nhất

`--y` là toạ độ **ĐÁY** của khối chữ, tính bằng pixel. Mặc định `0.80 × chiều cao`.

Trước khi chốt, hãy **xem frame thật** rồi mới quyết:

```bash
ffmpeg -v error -y -i "video_tho.mp4" -vf "select=eq(n\,120)" -frames:v 1 thu.png
```

Nếu trong video có đoạn bố cục khác (người nói đứng lên, đổi góc, chèn ảnh màn hình),
một chỗ đặt an toàn ở đoạn đầu **sẽ đè lên mặt** ở đoạn sau. Dùng `--safe` để đổi chỗ
theo từng đoạn:

```bash
python scripts/autosub.py --video "v.mp4" --out "v_sub.mp4" \
    --safe "0-12:1100,12-30:1536,30-60:1250"
```

Nghĩa là: giây 0–12 đặt đáy chữ ở y=1100, giây 12–30 ở y=1536, giây 30–60 ở y=1250.

**Luật cứng đã cài sẵn:** không bao giờ để một cụm chữ vắt qua ranh giới `--safe`.
Cụm bị cắt ngắn đúng tại ranh giới, cụm mới bắt đầu ở đoạn sau. Nếu không làm vậy,
cụm sẽ giữ y của đoạn trước và rơi lên mặt người nói. `build_ass.py` in ra rõ cụm nào
bị cắt vì lý do này.

## Sửa tên riêng bị nghe sai

Whisper nghe sai tên riêng rất đều tay. Trên video thật của kênh này nó ra
**"Cloud"** (đúng: Claude) và **"Hyperframe"** (đúng: HyperFrames).

Luật mặc định đã sửa sẵn các tên hay gặp: Claude, ChatGPT, HyperFrames, CapCut,
Gemini, Midjourney, Remotion, AI. Muốn thêm luật riêng:

```json
{
  "token":   { "cờ-lốt": "Claude", "sát-gpt": "ChatGPT" },
  "merge":   [ { "words": ["hai", "pơ", "phêm"], "to": "HyperFrames" } ],
  "context": [ { "token": "veo", "to": "Veo", "next": ["3", "ba"] } ],
  "keep":    [ "cloudflare" ]
}
```

```bash
python scripts/autosub.py --video "v.mp4" --out "v_sub.mp4" --fixes luat.json
```

Bước này **luôn in cả hai danh sách**: đã sửa gì, và **cố ý KHÔNG sửa gì**. Đọc phần
"CÓ Ý KHÔNG SỬA" — luật sai sẽ lộ ra ở đó. Chi tiết: `references/sua-token.md`.

## Các tham số hay dùng

```
--y 1536                 đáy khối chữ, pixel (mặc định 0.80 × cao)
--safe "0-12:1100,..."   đổi chỗ đặt theo từng đoạn giây
--max-words 4            mỗi cụm nhiều nhất mấy từ
--max-chars 22           mỗi cụm nhiều nhất mấy ký tự
--gap 0.35               nghỉ bao lâu (giây) thì tách cụm
--font-size 80           mặc định cao_video / 24
--outline 7              độ dày viền, mặc định 0.09 × cỡ chữ
--active-color "#FFD600" màu từ ĐANG được nói
--base-color  "#FFFFFF"  màu các từ còn lại
--model small            model nhẹ hơn large-v3 (máy yếu / không có GPU)
--language vi            đổi ngôn ngữ nếu video không phải tiếng Việt
--fixes luat.json        file luật sửa tên riêng của bạn
--font "D:/x/Font.ttf"   chỉ định thẳng 1 file font
--crf 18                 chất lượng hình (số nhỏ = nét hơn, file to hơn)
--dry-run                chỉ lập kế hoạch, không xuất video
```

## Sau khi chạy — bắt buộc kiểm

`verify.py` đo 5 thứ và **exit khác 0 nếu không đạt**:

1. Số frame file ra **đếm thật** phải bằng file vào.
2. Độ dài tiếng không đổi (tiếng được copy nguyên, đo được MD5 y hệt file vào).
3. File `.ass` khớp `.plan.json`: đúng số dòng Dialogue và đúng mốc cụm cuối.
   Bắt được trường hợp `.ass` bị ghi thiếu / sửa tay mà đo pixel vài mốc thì lọt.
4. **5 mốc đáng lẽ có chữ** — luôn gồm cụm ĐẦU và cụm CUỐI, cộng 3 mốc chia đều:
   so frame ra với frame vào, đếm pixel khác nhau **bên trong dải chữ**. Đo được
   trên máy này: 2.1–5.9% diện tích dải bị đổi, 100% pixel đổi nằm trong dải.
   Ngưỡng đặt ở 0.5%.
5. Một mốc **đáng lẽ KHÔNG có chữ**: phải gần như 0 pixel đổi (đo được: đúng 0).
   Mốc này bắt được cụm sub bị dính lại trên màn hình.

Đây là lý do phải đo pixel chứ không tin log ffmpeg: libass có thể chạy **exit 0 mà
không vẽ chữ nào**, hoặc lặng lẽ vẽ bằng font hệ thống thay vì font của bạn.

## Nếu có vấn đề

| Hiện tượng | Xem file |
|---|---|
| Chữ không hiện, hoặc hiện bằng font lạ | `references/font-tieng-viet.md` |
| Tô màu sai từ, muốn hiểu cách làm karaoke | `references/karaoke-ass.md` |
| Tên riêng vẫn sai, muốn viết luật | `references/sua-token.md` |
| Chữ đè lên mặt, chữ tràn lề | `references/dat-cho-va-vung-an-toan.md` |
| ffmpeg báo lỗi lạ, sai số frame | `references/cac-cai-bay-ffmpeg.md` |

## Ghi chú khi mang skill sang máy khác

Thư mục skill này **tự chứa hoàn toàn**. Copy cả thư mục `nns-auto-sub/` sang
`.claude/skills/` của project khác là chạy được ngay: font đã kèm trong `assets/fonts/`,
mọi script chỉ dùng đường dẫn tương đối. Thứ duy nhất cần cài thêm trên máy mới là
`ffmpeg` và `pip install faster-whisper numpy` — preflight sẽ nói rõ nếu thiếu.
