# Vì sao mặc định dồn SFX vào hook

## Bằng chứng

Đây không phải sở thích chung chung, mà là **phản hồi cụ thể của creator này**.

Trong một lần làm trước, đã dựng một lớp SFX **53 cue rải đều** cả video 131 giây
(≈ 0.40 cue/giây suốt chiều dài). Creator xem xong và **tự tay cắt bỏ gần hết**,
chỉ giữ lại phần trong khoảng **~20 giây đầu**.

Nên mặc định của skill là:

- **trong hook** (0 → `--hook-len`, mặc định **20s**): dày, `--density` cue/giây
- **sau hook**: **không tự thêm gì cả**, chỉ đặt cue ở chỗ **hình thật sự đổi**

Video ngắn thì cả video **là** hook: nếu thời lượng ≤ 30s, `hook-len` = cả video.
Đối chiếu: video 0822 dài 23.5s, cue sheet tay đã duyệt rải đều ~0.94 cue/giây —
vì cả video là hook.

## Mật độ

`--density 0.8` là mặc định. Đối chiếu với hai cue sheet tay đã được duyệt:

| Video | Cue trong 20s đầu | cue/giây |
|---|---|---|
| 0822 (23.5s, cả video là hook) | 22 cue / 23.5s | 0.94 |
| 111 (131s, hook-weighted) | ~11 cue / 18s | 0.61 |

`--density 0.8` cho ra 14 cue trong hook 20s (0.70 cue/giây) trên cả hai video
đã test — nằm đúng giữa hai con số trên.

Muốn dày hơn: `--density 1.0`. Muốn thưa: `--density 0.5`.
Muốn **chỉ** hook, không cue nào sau đó: `--max-t 20`.

## Nhịp được lấy từ đâu

`plan.py` không đoán nhịp. Nó đo, từ chính file đó:

1. **Cắt cảnh (`cut`)** — `ffmpeg -filter_complex "select='gt(scene,0.35)',metadata=print:file=-"`,
   parse `pts_time`. Cue ở đây **luôn được giữ**, kể cả sau hook, và **luôn là
   whoosh/swoosh** (`Picker.pick_cut()` chỉ quay vòng trong 3 file whoosh/swoosh
   tốt nhất). Đo trên `0822_edit_v4.mp4`: 5 chỗ cắt (32.00, 35.57, 79.00, 100.77,
   121.33).
2. **Đầu câu (`phrase`)** — envelope RMS 10 ms, ngưỡng `p70 − 12 dB` **suy ra từ
   phân bố của chính file** (không ghim cứng), và phải có ≥ 220 ms im trước đó.
3. **Trọng âm (`accent`)** — cực đại địa phương của envelope làm trơn 60 ms, trên
   `p70 − 3 dB`, cách nhau ≥ 450 ms.

Rồi chọn tham lam: ưu tiên `cut` → `phrase` → `accent`, khoảng cách tối thiểu
`1 / density` giây.

**Không ghim ngưỡng dB cố định** là cùng lý do như `nns-cut-silence`: vùng
−50…−35 dB của giọng creator này là **phụ âm nhẹ và hơi thở**, chiếm 14.6% thời
lượng. Giọng ở −17.6 dB, sàn ồn −84 dB. Ngưỡng phải suy ra từ file.

## Vai (role) và mức gain

Gain **không cố định theo file**, mà tính từ peak đã đo:

```
gain_db = ROLE_TARGET_PEAK[role] − seg_peak_dbfs
```

Nhờ vậy đổi sang thư viện SFX khác vẫn ra mức nghe tương đương.

| Vai | Peak đích | `ROLE_MAX_DUR` | Đối chiếu cue sheet tay |
|---|---|---|---|
| `impact` (punch, dun-dun) | −12 dBFS | 0.70s | punch −10 dB trên file peak −2.2 → −12.2 |
| `transition` (whoosh, swoosh) | −21 dBFS | 0.70s | quick-swoosh −16 dB trên peak −8.3 → −24.3 |
| `accent` (ting, pop, click) | −22 dBFS | 0.80s | quick-ting −14…−16 trên peak −7.3 → −21…−23 |
| `riser` | −24 dBFS | 2.50s | riser-metallic −13…−20 trên peak −8.7 → −22…−29 |
| `confirm` (correct, ka-ching) | −20 dBFS | 1.30s | |
| `negative` (error, buzzer) | −19 dBFS | 1.10s | |
| `bed` (keyboard, heartbeat) | −34 dBFS | 4.00s | mechanical-keyboard −28…−34 dB |

Vai suy từ **tên file** (bảng `ROLE_KEYS`), và nếu cạnh thư viện có `library.json`
thì dùng thêm `tags` trong đó. File nào được nhận là riser thì vai luôn là `riser`,
bất kể tên.

`ROLE_MAX_DUR` chặn trên độ dài cue. Không có nó thì `build-up.mp3` vào làm một
cue **6.66 giây** đè lên mọi cue khác quanh đó — đã gặp thật khi chưa chặn.

## Không lặp file

`Picker` quay vòng trong từng vai, và **không dùng lại file nào có trong 3 cue
gần nhất**. Trong mỗi vai, xếp theo: (a) tên quen thuộc trước (`ROLE_PREFER` —
`whoosh` trước `glitch`, `ting` trước `camera-flash`), (b) file ngắn trước.
Nhờ (a) mà cue cắt cảnh ra whoosh/swoosh thật, không ra `weee.mp3`.
