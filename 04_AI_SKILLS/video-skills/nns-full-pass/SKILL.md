---
name: nns-full-pass
description: Gộp TOÀN BỘ chuỗi hậu kỳ video talking-head tiếng Việt vào MỘT lệnh. Input là 1 video thô có tiếng (--video) + nơi lưu (--out); output là 1 video đăng được ngay - đã cắt khoảng lặng, có sub karaoke word-by-word, có thẻ chữ nhấn mạnh, có SFX dồn vào hook, và đã chuẩn hoá về -14 LUFS. Tự ĐO bố cục hình (cắt cảnh + hộp mặt + khung màn hình ghi + UI in sẵn) để quyết định chỗ đặt chữ, không phải soi frame gõ --safe bằng tay. Chữ chỉ mã hoá hình ĐÚNG 1 LẦN (sub + thẻ chung 1 file .ass), SFX là bước audio riêng mux -c:v copy. Mặc định DỪNG LẠI sau khi lập kế hoạch để bạn duyệt bảng bố cục / cue sheet / thẻ chữ rồi mới render. Trigger '/nns-full-pass', hoặc các câu như 'làm hết hậu kỳ cho video này', 'từ file thô ra video đăng được', 'cắt lặng + sub + SFX + thẻ chữ một lượt', 'chạy full pass cho video'.
---

# nns-full-pass — cả dây hậu kỳ trong MỘT lệnh

Từ file thô tới file đăng được: cắt khoảng lặng → đo bố cục → nhận dạng → sub
karaoke → thẻ chữ → burn → SFX → master → verify.

## BƯỚC 0 — BẮT BUỘC, LÀM TRƯỚC MỌI THỨ

Ngay khi skill này được gọi, TRƯỚC KHI làm bất cứ việc gì, chạy:

```
python <skill>/scripts/preflight.py --video "<video>" [--resources "<thư-mục>"]
```

Đọc kết quả:

- Preflight in "ĐẦY ĐỦ" → làm tiếp các bước dưới.
- Preflight in "THIẾU ..." → DỪNG NGAY. Không cắt, không render, không tạo file gì.
  Đưa NGUYÊN khối hướng dẫn mà preflight in ra cho người dùng, rồi HỎI họ:
  "Thiếu \<n\> thứ ở trên. Bạn làm theo hướng dẫn rồi báo tôi, hoặc gửi cho tôi
  \<thứ còn thiếu\> để tôi chạy tiếp?"
  Chờ người dùng trả lời. TUYỆT ĐỐI không tự đoán, không tự thay bằng thứ khác,
  không bỏ qua bước đó để "chạy tạm".

- Nếu người dùng KHÔNG đưa `--video`: hỏi đường dẫn video thô trước khi làm gì.

## Cần gì để chạy

| Thứ cần | Bắt buộc? | Nếu chưa có thì làm gì (lệnh cụ thể) |
|---|---|---|
| `ffmpeg` + `ffprobe` bản **full** | Bắt buộc | Windows: `winget install --id Gyan.FFmpeg -e`, hoặc tải bản full ở https://www.gyan.dev/ffmpeg/builds/ , giải nén ra `C:\ffmpeg`, thêm `C:\ffmpeg\bin` vào PATH. macOS: `brew install ffmpeg`. Ubuntu: `sudo apt install ffmpeg` |
| Filter `subtitles`, `alimiter`, `ebur128`, `amix`, `aresample`, `loudnorm` | Bắt buộc | Bản ffmpeg bị cắt bớt bộ lọc thì thiếu. Kiểm: `ffmpeg -filters \| findstr alimiter` |
| `python` 3.8+ | Bắt buộc | https://www.python.org/downloads/ |
| `numpy` | Bắt buộc | `pip install numpy` |
| `Pillow` | Bắt buộc — đo bề rộng chữ thật để auto-fit thẻ | `pip install Pillow` |
| `faster-whisper` | Bắt buộc | `pip install faster-whisper` |
| `onnxruntime` | Bắt buộc cho bước đo bố cục | `pip install onnxruntime`. Không cài được thì chạy thêm `--no-face` (bỏ đo mặt, chỉ dò khung hình) |
| Model Whisper `large-v3` | Tự tải lần đầu (~1.5 GB) | Lần chạy đầu cần mạng. Máy yếu: thêm `--model small` |
| Model mặt `det_10g.onnx` | Bắt buộc | **Đã kèm sẵn** trong `nns-face-highlight/assets/` |
| Font có dấu tiếng Việt | Bắt buộc | **Đã kèm sẵn** `nns-auto-sub/assets/fonts/BeVietnamPro-ExtraBold.ttf`. Muốn font khác: tạo `<thư-mục>/Font/`, bỏ `.ttf` vào, gọi thêm `--resources "<thư-mục>"` |
| Thư viện SFX `.mp3`/`.wav` | Bắt buộc | **Đã kèm sẵn** 9 file trong `nns-add-sfx/assets/sfx/`. Muốn thư viện riêng: `<thư-mục>/sound-effects/` rồi `--resources "<thư-mục>"` |
| Các skill anh em nằm cạnh | Bắt buộc | Skill này **gọi lại** `nns-cut-silence`, `nns-auto-sub`, `nns-face-highlight`, `nns-add-sfx` và `tools/sfx_pass/`. Nó không viết lại từ đầu. Preflight nói rõ thiếu cái nào |
| Video đầu vào **có tiếng** | Bắt buộc | Video im lặng: ghép tiếng vào trước bằng `ffmpeg -i silent.mp4 -i voice.wav -c:v copy -c:a aac -b:a 256k -shortest có_tieng.mp4` |
| GPU NVIDIA | Không bắt buộc | Có thì nhận dạng nhanh hơn ~5 lần |

**`--resources` đã đưa vào thì phải dùng được.** Trỏ tới thư mục không có font
tiếng Việt / không có file SFX nào thì skill **DỪNG**, không âm thầm tụt về
assets kèm sẵn. Muốn dùng assets kèm sẵn thì **bỏ hẳn `--resources`**.

## Chạy — hai nhịp, có cổng duyệt ở giữa

```bash
cd <skill>

# NHỊP 1 — lập kế hoạch. Chưa vẽ gì vào video.
python scripts/fullpass.py --video "tho.mp4" --out "xong.mp4"

# ... đọc 3 thứ nó in ra, sửa file JSON nếu cần, rồi:

# NHỊP 2 — render thật
python scripts/fullpass.py --video "tho.mp4" --out "xong.mp4" --go
```

Nhịp 1 in ra 3 thứ để duyệt:

1. **BẢNG BỐ CỤC** — mỗi đoạn đặt chữ ở y nào, vì sao, số đo là gì
2. **CUE SHEET SFX** — `<gốc>.cues.json`
3. **CHỖ ĐẶT THẺ CHỮ** — `<gốc>.cards.json`, trường `text` để **rỗng** cho bạn điền

Thẻ chữ để trống là cố ý: luật cứng của thẻ là "nói thứ mà màn hình và sub CHƯA
nói", máy không tự biết được. Điền xong chạy nhịp 2; `check_cards.py` sẽ đối
chiếu lại với transcript. Thẻ nào không dùng thì **xoá hẳn khỏi file**, đừng để
`text` rỗng. Bỏ hẳn lớp thẻ chữ: thêm `--no-cards`.

Bước nào đã có kết quả thì lần chạy sau **bỏ qua** (nhận dạng có cache, không
làm lại). Muốn làm lại từ đầu: `--force`.

## 11 bước, và file sinh ra

| Bước | Script | Làm gì | File sinh ra |
|---|---|---|---|
| 0 | `preflight.py` | Kiểm ffmpeg / thư viện / font / SFX / video (w×h, fps, CFR, thời lượng, có tiếng) | — |
| 1 | `cut_silence.py` *(nns-cut-silence)* | Cắt khoảng lặng | `<gốc>.cut.mp4` |
| 2 | `layout.py` | **TỰ ĐO bố cục** → chuỗi `--safe` | `<gốc>.layout.json` |
| 3 | `transcribe.py` *(nns-auto-sub)* | faster-whisper large-v3, word-level, có cache | `<gốc>.sub.words.json` |
| 4 | `fix_tokens.py` *(nns-auto-sub)* | Sửa token nghe sai (Cloud→Claude, Hyperframe→HyperFrames) | `<gốc>.sub.fixed.json` |
| 4b | `punct.py` | Thêm dấu chấm cuối câu, bỏ dấu phẩy | *(ghi đè `.fixed.json`)* |
| 5 | `build_ass.py` *(nns-auto-sub)* | Sub karaoke theo `--safe` đo được ở bước 2 | `<gốc>.sub.ass`, `<gốc>.sub.plan.json` |
| 6a | `plan_cues.py` | Đề xuất cue SFX (hook-weighted) + chỗ đặt thẻ | `<gốc>.cues.json`, `<gốc>.cards.json` |
| 6b | `check_cards.py` | Kiểm thẻ chữ — **không đạt thì không được burn** | — |
| 6c | `cards_to_ass.py` *(tools/sfx_pass)* | Gộp thẻ vào **CÙNG** file `.ass` | `<gốc>.merged.ass` |
| 7 | `burn.py` *(nns-auto-sub)* | Vẽ chữ — **mã hoá hình ĐÚNG 1 LẦN**, tiếng copy nguyên | `<gốc>.sub.mp4` |
| 8 | `build_sfx.py` | Dựng lớp SFX từ cue sheet | `<gốc>.sfx.raw` |
| 9 | `master.py` | Trộn + chuẩn hoá + mux `-c:v copy` | `--out`, `<gốc>.ab.json`, `<gốc>.work/` |
| 10 | `verify_all.py` | Đo lại 6 thứ | `<gốc>.report.json` |

Sau khi render, trích sẵn vài frame để soi:

```bash
python scripts/frames.py --video "xong.mp4" --plan "xong.sub.plan.json" --cards "xong.cards.json"
```

## Bước 2 — đo bố cục, phần dễ sai nhất

Trước đây phải soi frame bằng tay rồi gõ `--safe`. Bước này làm thay, và **in ra
bảng cho bạn xem trước khi render**:

- `select=gt(scene,0.25)` tìm cắt cảnh **thật** → chia video thành đoạn
  (đoạn ngắn hơn `--min-seg` được gộp vào đoạn trước, đổi y liên tục thì chữ nhảy nhót).
- Mỗi đoạn chạy face track (`det_10g.onnx`) đo **hộp mặt** trên frame thật.
- Không thấy mặt (bố cục PiP nhỏ / quay màn hình) → dò **hình chữ nhật đang chiếm
  khung** bằng phân bố màu theo hàng, lấy đáy của nó.
- Dò **UI in sẵn trong footage** (ví dụ pill thời lượng): vùng CÓ nội dung nhưng
  KHÔNG BAO GIỜ đổi suốt cả video, và là dải hẹp.
- Chọn y sao cho khối chữ không chạm cả 3, và **không tụt dưới vùng an toàn nền
  tảng** (đáy khung ~330px với khung 1920 → chữ phải trên y≈1600).
- Không đủ chỗ ở dưới thì **đẩy chữ LÊN TRÊN** vật cản, không bao giờ đẩy xuống.

Bảng in ra có cột **lý do** và **số đo** cho từng đoạn. Đoạn nào chật thì nó in
`CẢNH BÁO` kèm thiếu bao nhiêu px. Không đồng ý thì tự đè bằng `--safe "0-12:1100,12-30:1536"`.

Chi tiết: `references/vung-an-toan-va-do-bo-cuc.md`

## Cue sheet SFX — mặc định HOOK-WEIGHTED

| | Mật độ | Neo vào |
|---|---|---|
| Hook (20s đầu) | ~0.60 cue/s | cắt cảnh thật > đầu câu > đầu từ |
| Phần giải thích | ~0.12 cue/s | **chỉ** cắt cảnh thật |
| Video ≤ 30s | rải đều cả video | như hook |

Mọi cue ngoài hook đều mang `"optional": true` thành **một khối**. Bỏ hết bằng
đúng một tham số, và **không phải render lại hình** — lớp SFX là bước audio riêng:

```bash
python scripts/build_sfx.py --cues "xong.cues.json" --out "xong.sfx.raw" --total 79.233 --drop-optional
python scripts/master.py --video "xong.sub.mp4" --bed "xong.sfx.raw" --out "xong.mp4"
```

Chi tiết: `references/cue-sheet-va-mat-do-sfx.md`

## Thẻ chữ — luật cứng

| Luật | Giá trị | Ai chặn |
|---|---|---|
| Tối đa 1 thẻ / 12 giây | `--card-every` | `check_cards.py` |
| Mỗi thẻ ≤ 4 chữ | `--max-words` | `check_cards.py` |
| Mỗi thẻ ≤ 2.5s, ≥ 0.4s | cố định | `check_cards.py` |
| **Không lặp nguyên văn lời thoại** | đối chiếu transcript ±6s | `check_cards.py` |
| **Không in lại con số đang hiện** | đối chiếu transcript ±4s | `check_cards.py` |
| Font phải có đủ glyph | — | `check_cards.py` |
| Không tụt dưới vùng an toàn | từ `layout.json` | `check_cards.py` |
| Vừa bề ngang sau auto-fit | — | `check_cards.py` |

`"plate": true` cho thẻ có khung: nền đen mờ, bo góc, viền vàng, bóng đổ, tự thu
nhỏ / xuống dòng cho vừa.

```json
[
  {"start": 3.20, "end": 5.40, "y": 760, "style": "stat", "plate": true, "text": "3 giây"},
  {"start": 21.0, "end": 23.0, "y": 760, "style": "punch", "text": "sai chỗ này"}
]
```

Chi tiết: `references/lop-the-chu-ass.md`

## Các tham số hay dùng

```
--go                     render thật (mặc định chỉ lập kế hoạch rồi dừng)
--force                  làm lại mọi bước, bỏ cache
--dry-run                chỉ in kế hoạch các bước, không đụng tới file nào
--no-cut                 không cắt khoảng lặng, dùng thẳng video vào
--no-cards               bỏ hẳn lớp thẻ chữ
--no-sfx                 bỏ hẳn lớp SFX, chỉ chuẩn hoá
--drop-optional          bỏ mọi cue SFX ngoài hook
--safe "0-12:1100,..."   tự đặt chỗ chữ, bỏ qua kết quả đo tự động
--scene 0.25             ngưỡng cắt cảnh
--min-seg 2.5            đoạn ngắn hơn thì gộp vào đoạn trước
--no-face                bỏ đo mặt (không có onnxruntime)
--hook-len 20            độ dài hook
--density 0.60           cue/giây trong hook
--tail-density 0.12      cue/giây ngoài hook
--card-every 12          tối đa 1 thẻ / bao nhiêu giây
--max-words 4            mỗi cụm sub nhiều nhất mấy từ
--font-size 80           mặc định cao_video / 24
--active-color "#FFD600" màu từ ĐANG được nói
--keep-commas            giữ dấu phẩy trong sub (mặc định bỏ)
--target -14 --tp -2.0   loudness đích / trần true peak
--model small            model nhẹ hơn large-v3
--crf 18 --preset medium chất lượng hình
```

## verify đo những gì

`verify_all.py` **exit khác 0 nếu không đạt**. Chỉ được báo với người dùng là
xong khi nó exit 0.

| # | Phép đo | Đạt khi |
|---|---|---|
| 1 | Số frame / fps / kích thước | frame ra **đếm thật** == frame vào, fps và w×h không đổi |
| 2 | Đồng bộ tiếng–hình | lệch ≤ **1 frame** |
| 3 | Sub có thật sự hiện | đo pixel đổi trong dải chữ tại ≥3 mốc, > 600 px mỗi mốc |
| 4 | Thẻ chữ hiện, không tràn | > 600 px trong dải thẻ, và ≤ 10% pixel đổi nằm **ngoài** dải thẻ + dải sub. Dải thẻ tính từ số đo **THẬT**: auto-fit, số dòng, padding + viền + bóng của khung |
| 5 | SFX vào đúng chỗ | render **2 lần cùng chuỗi filter** — một lần lớp SFX thật, một lần lớp SFX im lặng — rồi trừ. Mọi cue phải nghe thấy, tương quan ≥ 0.90, lệch ≤ 2 × 10ms |
| 6 | Loudness | đo trên **chính file mp4 cuối**: I trong ±0.5 LU, TP ≤ trần, và **0 mẫu vượt 1.0** sau khi giải mã ra f32 |

Vì sao phải đo pixel chứ không tin log ffmpeg: libass có thể chạy **exit 0 mà
không vẽ chữ nào**, hoặc lặng lẽ vẽ bằng font hệ thống thay vì font của bạn.

Vì sao phép 5 không dùng `final − source×gain`: nguồn AAC + đích AAC + alimiter
lookahead làm nền dư **to hơn cả lớp SFX**, mọi kết luận rút ra đều vô nghĩa.

## Tự kiểm khi chưa có video

```bash
python scripts/selftest.py
```

59 phép kiểm thuần dữ liệu, không cần video: `--help` của mọi script, preflight
báo đúng khi thiếu, `--dry-run` in đủ kế hoạch, thẻ chữ → `.ass` (đếm dấu phẩy
dòng `Dialogue`, glyph thiếu bị chặn, thẻ dài tự xuống dòng), cue sheet → lớp
SFX (đúng số mẫu, không clip, tiếng vào đúng mốc).

## Nếu có vấn đề

| Hiện tượng | Xem file |
|---|---|
| Chữ đè lên mặt / bị UI nền tảng che / bảng bố cục sai | `references/vung-an-toan-va-do-bo-cuc.md` |
| SFX quá dày, quá thưa, muốn đổi mật độ | `references/cue-sheet-va-mat-do-sfx.md` |
| Thẻ chữ lệch khung, chữ mất dấu, khung không khớp chữ | `references/lop-the-chu-ass.md` |
| Video nhỏ tiếng / nghe méo / không đạt −14 LUFS | `references/loudness.md` |
| ffmpeg báo lỗi lạ, sai số frame, đường dẫn Windows | `references/cac-bay-da-gap.md` |

## Cách làm việc với người dùng

1. Chạy preflight. Thiếu gì thì đưa nguyên khối hướng dẫn rồi **dừng, hỏi**.
2. Chạy nhịp 1 (không `--go`). **In ra cho người dùng**: bảng vùng an toàn, cue
   sheet SFX, danh sách thẻ chữ.
3. Điền `text` cho thẻ chữ theo luật "nói thứ sub chưa nói". Hỏi người dùng duyệt.
4. Người dùng OK thì mới chạy `--go`.
5. Render xong: chạy `frames.py` trích sẵn vài frame ở các mốc quan trọng cho họ soi.
6. **Chỉ báo xong khi `verify_all.py` exit 0.**
