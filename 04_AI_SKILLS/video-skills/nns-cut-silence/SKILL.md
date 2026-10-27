---
name: nns-cut-silence
description: Cắt khoảng lặng trong video talking-head một cách frame-exact và an toàn (ngưỡng im lặng suy ra từ chính phân bố năng lượng của file, không ghim cứng -30/-38 dB nên không cắt mất phụ âm nhẹ / hơi thở). Input là 1 video có tiếng (--video); output là video đã cắt (--out) + file WAV gốc kèm theo + plan.json + timemap.json để các bước sau (caption, SFX, overlay) re-time theo timeline mới. Trigger '/nns-cut-silence', hoặc các câu như 'cắt khoảng lặng video này', 'bỏ mấy đoạn im im giữa các câu', 'video tôi nói bị ngắt quãng nhiều, cắt gọn lại giúp', 'cắt silence nhưng đừng cắt mất tiếng'.
---

# nns-cut-silence — cắt khoảng lặng trong video (frame-exact, an toàn)

## BƯỚC 0 — BẮT BUỘC, LÀM TRƯỚC MỌI THỨ

Ngay khi skill này được gọi, TRƯỚC KHI làm bất cứ việc gì, chạy:

```
python nns-cut-silence/scripts/preflight.py --video "<video>"
```

Đọc kết quả:

- Preflight in "ĐẦY ĐỦ" (`DAY DU`) -> làm tiếp các bước dưới.
- Preflight in "THIẾU ..." (`THIEU ...`) -> DỪNG NGAY. Không cắt, không render, không tạo file gì.
  Đưa NGUYÊN khối hướng dẫn mà preflight in ra cho người dùng, rồi HỎI họ:
  "Thiếu \<n\> thứ ở trên. Bạn làm theo hướng dẫn rồi báo tôi, hoặc gửi cho tôi
  \<thứ còn thiếu\> để tôi chạy tiếp?"
  Chờ người dùng trả lời. TUYỆT ĐỐI không tự đoán, không tự thay bằng thứ khác,
  không bỏ qua bước đó để "chạy tạm".

- Nếu người dùng KHÔNG đưa `--video`: hỏi đường dẫn video thô trước khi làm gì.

## Cần gì để chạy

| Thứ cần | Bắt buộc? | Nếu chưa có thì làm gì (lệnh cụ thể) |
|---|---|---|
| `ffmpeg` + `ffprobe` | Bắt buộc | Windows: `winget install Gyan.FFmpeg` · macOS: `brew install ffmpeg` · Linux: `sudo apt install ffmpeg`. Mở lại terminal rồi gõ `ffmpeg -version` để kiểm. |
| `python` 3.8+ | Bắt buộc | Tải tại https://www.python.org/downloads/ |
| `numpy` | Bắt buộc | `pip install numpy` (hoặc `python -m pip install numpy`) |
| Video **có stream tiếng** | Bắt buộc | Nếu video không tiếng mà bạn có file voice riêng: `ffmpeg -i silent.mp4 -i voice.wav -map 0:v -map 1:a -c:v copy -c:a aac co_tieng.mp4` rồi dùng `--video co_tieng.mp4` |
| Video fps cố định (CFR) | Bắt buộc | File quay điện thoại / ghi màn hình hay bị VFR. Chuyển trước: `ffmpeg -i raw.mp4 -c:v libx264 -crf 16 -r 30 -c:a copy cfr.mp4` |
| `--resources` | **Không cần** | Skill này không dùng font / SFX / model nào. Bỏ hẳn tham số này. |

**Bước 1 luôn là chạy preflight. Preflight báo THIẾU thì dừng lại, làm theo hướng dẫn
nó in ra, không được chạy tiếp.**

## Skill này làm gì

Cắt các khoảng lặng giữa các câu nói, giữ lại một khe hở nhỏ để câu vẫn có nhịp thở,
mà **không cắt vào tiếng**. Bốn nguyên tắc quyết định toàn bộ thiết kế:

1. **Ngưỡng im lặng suy ra từ chính file đó**, không ghim cứng. Đã đo trên một file
   talking-head tiếng Việt 226s thật: sàn ồn (p1) = **-84 dB**, mức nói (p70) = **-17.6 dB**,
   và vùng **-50..-35 dB chiếm 14.6% thời lượng** — vùng đó là **phụ âm nhẹ và hơi thở**,
   không phải im lặng. Ngưỡng -35 dB đánh dấu sai 69 vùng mà vùng nào cũng có tiếng.
   Ngưỡng -50 dB suy ra từ phân bố cho 52 vùng, peak xấu nhất -39.1 dB → an toàn.
   Chi tiết: `references/nguong-im-lang.md`.
2. **Chỉ cắt PHẦN GIỮA** mỗi khoảng lặng, để lại khe hở `T` (`--keep`, mặc định 0.10s),
   và chừa `GUARD` (`--guard`, mặc định 0.03s) ở hai đầu.
3. **Self-check trước khi cắt**: đo peak thực tế từng mẫu trong mọi vùng sắp cắt.
   Vùng nào peak > -34 dB là có tiếng nói → **báo lỗi và từ chối**, không ghi plan.
4. **Đo lại sau khi cắt**: `verify.py` đếm frame, so độ dài tiếng/hình, tương quan chéo
   để chứng minh bản đồ thời gian đúng, đo bước nhảy tại mỗi mối cắt để chứng minh
   không sinh tiếng "tách", **và so nội dung HÌNH với frame gốc mà time-map chỉ ra**
   (đo tiếng thôi là bỏ lọt trường hợp hình không hề bị cắt — xem mục "Verify đo những gì").

## Chạy

Cách ngắn nhất — một phát cả 4 bước (preflight → plan → apply → verify):

```
python nns-cut-silence/scripts/cut_silence.py --video "raw.mp4" --out "cut.mp4"
```

Muốn xem kế hoạch trước mà không tạo file nào:

```
python nns-cut-silence/scripts/cut_silence.py --video "raw.mp4" --out "cut.mp4" --dry-run
```

Chạy tay từng bước (khi cần tinh chỉnh):

```
python nns-cut-silence/scripts/preflight.py --video "raw.mp4"
python nns-cut-silence/scripts/plan.py     --video "raw.mp4" --plan cut.plan.json
python nns-cut-silence/scripts/apply.py    --video "raw.mp4" --plan cut.plan.json --out cut.mp4
python nns-cut-silence/scripts/verify.py   --video "raw.mp4" --plan cut.plan.json --out cut.mp4
```

**Chỉ được báo "xong" khi `verify.py` thoát với mã 0.**

## File sinh ra

| File | Là gì | Dùng làm gì |
|---|---|---|
| `cut.mp4` | Video đã cắt. Hình re-encode CRF (mặc định 16), tiếng AAC 256k | Xem / duyệt / đưa lên |
| `cut.wav` | Tiếng đã cắt, **PCM 16-bit, sample rate gốc** | BẢN GỐC cho các bước sau (thêm SFX, chuẩn hoá loudness). Dùng file này để tránh nén lossy nhiều đời |
| `cut.plan.json` | Toàn bộ kế hoạch: phân bố năng lượng, ngưỡng, từng nhát cắt kèm peak đo được | Truy vết, tái lập, debug |
| `cut.plan.timemap.json` | **Bản đồ thời gian cũ → mới** | BẮT BUỘC đưa cho bước sau. Không có nó, caption dựng trên timeline gốc sẽ lệch dần |

## Tham số hay dùng

| Cờ | Mặc định | Ý nghĩa |
|---|---|---|
| `--keep` | `0.10` | Khe hở còn lại ở mỗi chỗ cắt (giây). Nói nhanh: 0.06–0.08. Muốn giữ nhịp thở: 0.14–0.20 |
| `--min-sil` | `0.35` | Khoảng lặng ngắn hơn mức này thì bỏ qua |
| `--guard` | `0.03` | Chừa ra ở hai đầu khoảng lặng, không bao giờ cắt vào |
| `--protect "a-b,c-d"` | — | Vùng (giây, trên timeline **gốc**) **KHÔNG được cắt**. Xem mục dưới |
| `--protect-cuts` | tắt | Tự tìm các cắt cứng (scene detection) và bảo vệ ±0.25s quanh mỗi cắt |
| `--trim-edges` | tắt | Khoảng lặng ở đầu/cuối video thì bỏ từ phía ngoài vào (thay vì bỏ phần giữa) |
| `--threshold-db` | — | Áp đặt ngưỡng. **Chỉ dùng khi thật cần**; lỏng hơn -45 dB là in cảnh báo |
| `--crf` / `--preset` | `16` / `medium` | Chất lượng / tốc độ encode hình |
| `--no-mux-audio` | tắt | File chính không có tiếng (chỉ WAV mới có) |
| `--no-wav` | tắt | Không xuất WAV kèm theo. Khi đó verify không so được từng mẫu (chỉ CẢNH BÁO) |
| `--allow-no-audio` | tắt | Chỉ cần khi cố tình dùng **cả** `--no-wav` **và** `--no-mux-audio`. Không có cờ này thì `apply.py` **từ chối ngay** (đã thử: tổ hợp đó ra file không có tiếng gì, và verify fail ở cuối sau khi đã encode xong — mất thời gian vô ích) |
| `--no-video-check` | tắt | Bỏ phép kiểm khớp frame hình của verify. Chỉ dùng khi thật cần nhanh — nó là phép kiểm duy nhất bắt được lỗi "hình không bị cắt" |
| `--dry-run` | tắt | Chỉ in kế hoạch, không tạo file |

## `--protect` — khi nào BẮT BUỘC dùng

Có những đoạn mà cắt vào là **lệch hình so với tiếng**, không phải chỉ mất nhịp:

- **Đoạn chèn video khác đang có lời thuyết minh đè lên.** Hình chạy theo timeline của
  clip chèn, tiếng chạy theo timeline của người nói. Cắt bớt frame ở đó là hai luồng
  lệch nhau vĩnh viễn và không sửa được ở bước sau.
- Đoạn có nhạc / SFX đang ngân, hoặc animation đang chạy dở.
- Sát các cắt cứng (transition, jump cut) — dùng `--protect-cuts`.

Cách dùng: `--protect "12.5-19.0,44-50"` (giây, trên timeline **gốc**).
Chi tiết và cách tìm mốc: `references/vung-bao-ve.md`.

## Đưa kết quả sang bước sau

Mọi mốc thời gian của timeline gốc đều đã lệch. Dùng `remap.py`:

```
python nns-cut-silence/scripts/remap.py --timemap cut.plan.timemap.json --times "3.2,17.8"
python nns-cut-silence/scripts/remap.py --timemap cut.plan.timemap.json --srt sub.srt --srt-out sub_moi.srt
python nns-cut-silence/scripts/remap.py --timemap cut.plan.timemap.json --json sfx_cue.json --json-out sfx_cue_moi.json
```

Với `nns-auto-sub`: transcribe **lại trên file đã cắt** thì chuẩn nhất; chỉ remap khi
bạn đã có transcript của bản gốc và không muốn chạy lại. Chi tiết: `references/time-map.md`.

## Verify đo những gì

`verify.py` fail (exit 1) nếu bất kỳ mục nào sai:

1. Số frame đầu ra **đúng bằng** kế hoạch (đếm packet, không tin metadata).
2. Độ dài tiếng == độ dài hình, lệch ≤ 1 frame.
3. Tương quan chéo vài cửa sổ 0.8s giữa tiếng đầu ra và tiếng gốc tại vị trí mà
   time-map nói là tương ứng: corr ≥ 0.85 và lệch ≤ 1 frame. Cửa sổ nào vắt qua
   một mối cắt thì bỏ qua (về bản chất không thể khớp).
4. **Khớp mẫu tuyệt đối tại MỌI biên đoạn giữ**: 0.10s ở đầu và cuối từng đoạn phải
   trùng tiếng gốc **đến từng mẫu** (≤ 2 LSB). Đây là phép kiểm có răng nhất — cửa sổ
   trải rời rạc ở mục 3 có thể bỏ lọt một nhát cắt bị dịch chỗ trong vùng im lặng,
   kiểm từng biên thì không thể bỏ lọt. Cần file WAV (tiếng AAC là lossy nên không so
   tuyệt đối được — khi đó mục này thành CẢNH BÁO).
5. Bước nhảy biên độ tại mỗi mối cắt ≤ độ dốc p99.9 của chính tín hiệu → không có click.
6. Không vùng cắt nào có peak > -34 dB (đo **lại** trên file gốc, không tin plan).
7. **HÌNH cũng phải bị cắt đúng chỗ.** Lấy chữ ký ảnh xám (64×64) của 6 frame đầu ra,
   so với frame gốc mà time-map chỉ ra, đặt cạnh các "mồi nhử": shift của đoạn khác
   trong plan, lệch ±1, ±2 và ±8 frame. Frame khớp nhất **phải** là frame plan nói.
   Frame được lấy bằng `select=eq(n\,N)`, **không dùng `-ss`** (fast seek nhảy sai frame).
   Chữ ký được **chuẩn hoá z-score** trước khi so, nên phép đo này chỉ đo *đúng frame hay
   không*, không bị chuyển tone toàn cục làm nhoè.
8. **Dải màu (tone) không được đổi.** Mức sáng trung bình và tỉ lệ độ tương phản của
   frame ra phải bằng frame gốc tương ứng (lệch ≤ 2/255, tỉ lệ trong 1 ± 0.03).
   Có thật: input `yuvj420p` (full range 0–255) bị encode ra `yuv420p` → ffmpeg nén dải
   màu về 16–235, **hình nhạt đi thật** (luma trung bình 29.9 → 41.5, MAE 12.25/255) mà
   mọi phép kiểm khác vẫn OK. Đã sửa trong `apply.py` (giữ nguyên `yuvj*`), sau khi sửa
   luma 29.90 → 29.91, MAE 0.218. Chi tiết: `references/cac-cai-bay.md` mục 14.

Đã thử ngược để chắc verify có răng thật:

- Dịch một nhát cắt đi 10 frame trong vùng im lặng (số frame, độ dài, tương quan chéo
  đều vẫn "OK") → mục 4 bắt được ngay (lệch 639 LSB tại `dau doan 1 @ 00:06.200`), exit 1.
- Ghép file có **tiếng cắt đúng nhưng hình là 677 frame đầu của bản gốc** (tức hình
  không hề bị cắt, lệch tiếng/hình tới 0.93s): mục 1–6 **đều OK** và verify từng báo ĐẠT.
  Đó là lý do mục 7 tồn tại — bây giờ nó báo `4/6 diem do KHONG khop frame goc`, exit 1.
- Dịch **toàn bộ hình đi 1 frame** (33 ms): mục 7 bắt được, exit 1.
  Trong khi đó file đúng vẫn ĐẠT: lệch 0.0026 với frame đúng, frame sai gần nhất 0.126.
- Bản bị nén dải màu full→limited: mục 8 báo `lech muc sang 10.69/255, ti le 0.856`, exit 1;
  bản đã sửa `0.01/255, ti le 1.000`, ĐẠT.

## references/

| File | Nội dung |
|---|---|
| `references/nguong-im-lang.md` | Ngưỡng suy ra thế nào, số đo thật, ví dụ trên 4 file, vì sao chặn cứng -45 dB và tự kiểm -34 dB |
| `references/vung-bao-ve.md` | Luật vùng bảo vệ, vì sao quan trọng, cách tìm mốc, `--protect-cuts` |
| `references/cac-cai-bay.md` | Các cái bẫy đã gặp: concat tụt fps, `-ss` lệch frame, `drawtext` segfault, `loudnorm` nén LRA, AAC vượt true-peak, đường dẫn trong filter, **verify chỉ đo tiếng thì bỏ lọt lỗi hình (mục 12)**, `--no-wav`+`--no-mux-audio` (mục 13), **`yuvj420p` bị nén dải màu (mục 14)** |
| `references/time-map.md` | Định dạng time-map, cách map, cách dùng `remap.py`, những chỗ dễ sai |
