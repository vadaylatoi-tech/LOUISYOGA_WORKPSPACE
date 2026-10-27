# Luật đo onset và luật riser

Đây là phần dễ làm sai nhất, và sai thì **không nghe ra ngay** — cue chỉ đơn giản
là không có tiếng, hoặc có tiếng nhưng lệch nhịp. Nên nó là phép đo bắt buộc,
không phải tuỳ chọn.

## 1. Vì sao phải đo onset: số thật

Rất nhiều file trong thư viện SFX **có im lặng ở đầu**. Đo trên thư viện 86 file
`shared-sources/sound-effects/` của máy này: **35 file** có onset ≥ 0.15s.

| File | Onset đo được | Nếu cắt `[0.0 .. 0.2]` thì được gì |
|---|---|---|
| `opening-bottle.wav` | 1.055s | im hoàn toàn |
| `mouse-click.mp3` | **1.020s** | im hoàn toàn |
| `ting.wav` | 0.965s | im hoàn toàn |
| `buzzer.mp3` | 0.660s | im hoàn toàn |
| `digital-counting-2.mp3` | 0.660s | im hoàn toàn |
| `new-item.wav` | 0.650s | im hoàn toàn |
| `funny.mp3` | 0.520s | im hoàn toàn |
| `pop.mp3` | 0.225s | im hoàn toàn |
| `punch.mp3` | 0.050s | được, may |

Kết luận: **không được đoán offset**. `probe.py` đo và cache lại; `plan.py` chỉ
đọc bảng đó. `apply.py` và `verify.py` đều raise lỗi cứng nếu một cue ra peak = 0.

## 2. Thuật toán onset (đúng thuật toán trong `_common.analyse_sfx`)

1. Giải mã ra mono float 48 kHz.
2. Envelope RMS **5 ms** một khung, đổi ra dB.
3. `pk = max(envelope)`, `floor = percentile(envelope, 5)`.
4. Ngưỡng:
   ```
   thr = max( pk - 30 ,  min(floor + 8, pk - 6) ,  -70 )
   ```
   Chú ý cái `min(..., pk - 6)`: **bắt buộc**. File đã nén rất mạnh thì
   `floor + 8` có thể **cao hơn cả đỉnh** → không frame nào vượt ngưỡng → crash.
   Đã gặp thật với `temple-bell.mp3`: `pk = -6.79 dB`, `p5 = -13.75 dB`, nên
   `floor + 8 = -5.75 > pk`. Với cái kẹp `pk - 6` thì `thr = -12.79` và onset ra
   0.010s (đúng — quả chuông vang ngay từ đầu).
5. Lấy khung đầu tiên vượt `thr`, rồi **lùi lại** trong khi còn vượt
   `back = max(thr - 12, min(floor + 3, thr - 3))` — để không cắt mất phần tấn công.

Đối chiếu: thuật toán này cho ra đúng những con số đã đo bằng tay ở trên
(mouse-click 1.020 vs 1.00; pop 0.225 vs 0.20; new-item 0.650 vs 0.60;
funny 0.520 vs 0.50; digital-counting-2 0.660 vs 0.60; buzzer 0.660 vs 0.60).

## 3. `burst_end` — bắt file đánh 2 lần

`whoosh.wav` đánh một cú ở **0.135 → 0.410**, rồi **im**, rồi đánh lại ở 1.40, và
còn một cú nữa ở 2.70 (chỗ này mới là đỉnh của cả file). Nếu lấy cả file thì một
cú whoosh biến thành ba cú lệch nhịp.

`burst_end` = chỗ **im ≥ 120 ms** đầu tiên sau onset (im = envelope < `thr - 6`).
Với whoosh.wav ra 0.410 — đúng bằng cú đầu.

Nên `rec_dur` mặc định của cue one-shot = `burst_end - onset` (chặn trên 2.5s).

## 4. Luật riser: cắt để KẾT THÚC đúng đỉnh

Riser là file **leo dần rồi tắt**. `riser-metallic.mp3`: onset 0.210, đỉnh
**1.770**, rồi chết. Nếu đặt cue ở giây `T` và lấy cả file thì riser lên đỉnh ở
`T + 1.56` rồi im — trong khi cái nhịp cần nó đập lại ở chỗ khác.

Cách làm đúng: cue riser có `align = "end"`, và `t` là **giây mà đỉnh phải đập**.
`apply.py` tính `start = t - dur`. Đối chiếu với cue sheet tay đã được duyệt của
video 0822: cue ở 16.64 dài 1.20 → climax rơi vào 17.84, đúng chỗ câu
"có làm thì mới có ăn" bắt đầu.

Cắt ngắn một riser thì **cắt từ đầu**, giữ đoạn kết:
`offset = onset + (rec_dur - dur)`. Cắt từ đuôi là mất luôn cái đỉnh.

### Nhận diện riser (không đoán theo tên file)

Điều kiện, đo trên envelope:

| Tiêu chí | Ngưỡng | Vì sao |
|---|---|---|
| `span = burst_end - onset` | ≥ 1.00s | dưới 1s là one-shot, không phải riser |
| `frac = (climax - onset) / span` | ≥ 0.65 | đỉnh phải ở **cuối** vùng có tiếng |
| `rise` = `pk` − trung bình 20% đầu | ≥ 8 dB | phải thật sự **leo lên** |
| `decay` = `pk` − trung bình 400 ms sau đỉnh | ≥ 5 dB | phải **tắt** sau đỉnh |
| `corr(index, envelope)` trên `[onset..climax]` | ≥ 0.45 | leo **đều**, không phải chuỗi cú đập rời |
| `onset < climax < burst_end` | | đỉnh phải nằm trong cú đầu, không phải cú thứ hai |

Chạy trên cả 86 file, bộ luật này chọn ra đúng 2 file: `build-up.mp3`
(onset 0.535 → đỉnh 7.145) và `riser-metallic.mp3` (0.210 → 1.770).

Từng thử ngưỡng lỏng hơn và bị **dương tính giả**, ghi lại để đừng lặp lại:

- `span ≥ 0.35`: kéo vào `camera-flash-1..3.wav`, `camera-shutter-2/3.wav`,
  `digital-counting-1.mp3`, `paper-handle-foley.mp3` — đều là one-shot 0.4–0.9s.
  → sửa bằng `span ≥ 1.00`.
- không có điều kiện `corr`: kéo vào `iphone-typing.mp3` (chuỗi cú gõ rời, tình cờ
  cú to nhất nằm ở 2.03s). → sửa bằng `corr ≥ 0.45`.
- `frac ≥ 0.60`: kéo vào `money-counter.mp3` (frac 0.61). → sửa bằng `frac ≥ 0.65`.
- Điều kiện `climax < burst_end` là cái loại `whoosh.wav` (đỉnh ở 2.70 nhưng
  `burst_end` 0.41 → đỉnh thuộc cú **khác**) và `meme-laugh.mp3` (đỉnh ở 20.0s
  của file 30s).

## 5. Cache

`probe.py` ghi `sfx_onsets.json`, khoá theo `(size, mtime, CACHE_VERSION)` của
từng file. Đo mới 86 file mất ~3.5s; lần sau gần như tức thì. **Đổi thuật toán
thì phải tăng `CACHE_VERSION`**, nếu không sẽ đọc lại số cũ.
