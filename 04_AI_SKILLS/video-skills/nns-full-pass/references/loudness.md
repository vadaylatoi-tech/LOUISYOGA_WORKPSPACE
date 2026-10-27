# Loudness

Đích: **−14 LUFS**, true peak **−2.0 dBTP**.

−2.0 chứ không phải −1.0: AAC là codec biến đổi, bản giải mã ra có thể vượt
đỉnh so với trước khi mã hoá. −1.0 không đủ headroom, đo lại trên file mp4 cuối
sẽ thấy vượt trần.

## Hai đường, thử theo thứ tự

### Đường 1 — `loudnorm` 2 pass, `linear=true`

```
pass 1: đo  -> input_i, input_tp, input_lra, input_thresh, target_offset
pass 2: áp  -> loudnorm=...:measured_*=...:linear=true
```

`linear=true` là bắt buộc. Không có nó, `loudnorm` **âm thầm chuyển sang chế độ
`dynamic`** và nén dải động — đo thật trong project này: LRA **5.5 → 3.2 LU**.
Log không báo gì cả, chỉ có một dòng `Normalization Type: dynamic` lẫn trong
summary.

Nhưng `linear=true` chỉ làm được khi còn đủ headroom. `input_tp` cao thì
`loudnorm` không lên nổi mức đích, và nó **cũng không báo lỗi** — nó chỉ trả về
một file thấp hơn đích.

Nên `master.py` **luôn đo lại** sau pass 2. Không đạt thì chuyển đường 2.

### Đường 2 — gain + alimiter

```
volume=<gain>dB,alimiter=limit=<L>:level=disabled
```

**`level=disabled` là bắt buộc.** `level=1` (mặc định) tự kéo biên độ lên sau
khi giới hạn, tức là **undo** đúng phần limiting vừa làm. Dùng `level=1` thì
true peak đo lại vẫn vượt trần, và càng lặp càng không hội tụ.

Vòng lặp:

```
gain  = đích − I đo được
limit = 10^((tp − 0.3) / 20)          0.3 dB dự phòng cho AAC
lặp tối đa 6 vòng:
    mã hoá -> đo lại trên file m4a
    đạt cả I và TP -> xong
    TP vượt -> siết limit
    I thiếu  -> cộng thêm gain
```

Không hội tụ sau 6 vòng thì **dừng và nói rõ**, kèm 2 lựa chọn: nới trần
(`--tp -1.5`) hoặc hạ đích (`--target -13`). Không âm thầm trả về file sai mức.

## Đo lại thế nào cho đúng

**Giải mã file mp4 cuối ra f32 rồi lấy đỉnh thật:**

```bash
ffmpeg -v error -i final.mp4 -f f32le -ar 48000 -ac 2 -
```

rồi đếm số mẫu có `|x| > 1.0`.

**Không dùng `volumedetect`.** Nó clamp giá trị nên nó **giấu lỗi**: file đã
clip vẫn báo `max_volume: 0.0 dB` trông như vừa khít.

`master.py` và `verify_all.py` đều đo theo cách này, và verify **fail nếu có
bất kỳ mẫu nào vượt 1.0**.

Loudness I / LRA / TP đo bằng `ebur128=peak=true`, và đo **trên chính file mp4
cuối** — không phải trên bản trước khi mã hoá AAC.

## Thứ tự các bước — vì sao hình chỉ mã hoá 1 lần

```
bước 7  burn    : libx264 + subtitles(.ass đã gộp), -c:a copy     <- MÃ HOÁ HÌNH
bước 8  sfx     : dựng lớp SFX ra raw f32                          (thuần số)
bước 9  master  : trộn + chuẩn hoá ra m4a, rồi mux -c:v copy       <- KHÔNG mã hoá hình
```

Vì bước 9 mux `-c:v copy`, đổi SFX / đổi mức loudness / bỏ cue optional đều
**không phải render lại hình**. Chạy lại bước 8 + 9 là xong, mất vài giây thay
vì vài phút, và chất lượng hình không suy giảm thêm lần nào.

## Trộn tiếng

```
[0:a]aresample=48000:resampler=soxr[a0];
[1:a]aresample=48000[a1];
[a0][a1]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[am]
```

`normalize=0` là bắt buộc — mặc định `amix` chia biên độ cho số input, tức là
tiếng gốc bị **giảm một nửa** ngay khi có thêm lớp SFX.

`dropout_transition=0` để lớp SFX (phần lớn là im lặng) không làm `amix` tự động
kéo gain của tiếng gốc lên xuống.

## Số đối chiếu

| Đo | Giá trị mong đợi |
|---|---|
| I | −14.0 ± 0.5 LUFS |
| TP | ≤ −2.0 dBFS |
| LRA | mất ≤ 2.5 LU so với bản gốc (mất nhiều hơn = đã bị nén động) |
| Mẫu vượt 1.0 | **0** |
| Độ dài tiếng vs hình | lệch ≤ 1 frame |
