# Master độ to: `volume` + `alimiter`, không `loudnorm`

## 1. `loudnorm` âm thầm nén dải động

`loudnorm` trông như đúng thứ cần: đưa file về đúng LUFS mục tiêu trong một pass.
Nhưng nó **tự chuyển sang chế độ `dynamic`** khi thấy cần, và khi đó nó nén dải
động. Đo thật trong project này: **LRA 5.5 → 3.2 LU**. Nghe ra là giọng bị "dẹt",
mất chỗ nhấn — đúng cái làm video talking-head nghe như đọc máy.

Cách làm thay thế, **tuyến tính hoàn toàn** trừ đúng những đỉnh cần chặn:

```
volume=<G>dB , alimiter=limit=<L>:level=disabled
```

Kết quả đo trên 3 video test:

| Video | LRA trước | LRA sau | Mất |
|---|---|---|---|
| `0822_edit_v4.mp4` | 4.2 LU | 4.2 LU | 0.0 |
| `footage3/src.mp4` | 5.5 LU | 4.8 LU | 0.7 |
| `clean.mp4` | 1.2 LU | 1.2 LU | 0.0 |

`verify.py` kiểm luôn cái này: mất > 2.5 LU là KHÔNG ĐẠT.

## 2. `alimiter` phải có `level=disabled`

`alimiter` mặc định `level=1` (auto level): sau khi giới hạn xong nó **tự kéo biên
độ lên lại**, tức là **undo** luôn cái giới hạn vừa đặt. Trần true peak trở thành
vô nghĩa.

Luôn viết `alimiter=limit=<L>:level=disabled`.
`limit` là **tuyến tính** (0…1), không phải dB: `limit = 10^(dBTP/20)`.

## 3. AAC có thể vượt true peak so với WAV

Đo trên WAV rồi tin số đó là sai. AAC là biến đổi có mất, dạng sóng sau khi giải
mã **không giống** dạng sóng vào, và đỉnh có thể **cao hơn** (~+1 dB ở bitrate
thấp; ở 256k thì gần như không).

Nên:
- `AAC_GUARD = 0.30 dB`: trần limiter đặt ở `tp − 0.30`, không đặt đúng `tp`.
- **Đo trên file AAC đã mã hoá**, không đo trên WAV trung gian. `apply.py` mã hoá
  audio-only ra `.m4a` rồi đo chính file đó; `verify.py` đo file `.mp4` cuối.
- Mặc định `--abr 256k`.

Kết quả: `--tp -1.5` cho ra TP thật đo được −1.8 và −1.9 dBFS. Có dư, không vượt.

## 4. Vòng dial gain: đo rồi sửa, không tính một lần

Không thể tính `G` bằng một công thức, vì limiter can vào và đổi cả LUFS. Nên:

```
G  = target − I(bản trộn thô)          # điểm xuất phát
L  = 10^((tp − 0.30)/20)
lặp tối đa 6 vòng:
    mã hoá audio-only AAC với (G, L)
    đo I / LRA / TP trên chính file AAC đó
    nếu |I − target| ≤ 0.30  và  TP ≤ tp  ->  xong
    nếu TP > tp  ->  L *= 10^(−(TP − tp + 0.20)/20)
    nếu I lệch   ->  G += (target − I)
```

Thực tế hội tụ nhanh: **1 vòng** khi file đã gần đích, **2 vòng** khi cần
+4.2 dB. Bảng vòng lặp được in ra để đọc lại được.

## 5. Khi trần chặn: phải báo, không được lặp mãi

Có trường hợp **không thể** đạt cả hai mục tiêu. Ví dụ đo thật: `clean.mp4`
(LRA 1.2 LU) với `--target -14 --tp -6.0` — trần −6 dBTP chỉ cho lên tới
khoảng −15 LUFS.

Phát hiện bằng **đo tỷ lệ**, không đoán: nếu TP đã dính trần (`≥ tp − 0.15`) mà
thêm `dG > 0.30 dB` gain chỉ được `dI < 0.5 × dG`, thì limiter đang ăn hết →
dừng và nói rõ:

```
!! LOI: TRAN TRUE PEAK DANG CHAN.
Voi tai lieu nay, tran -6.0 dBTP chi cho phep len toi
khoang -15.00 LUFS, khong the dat -14.00 LUFS.
Chon 1 trong 2:
  - noi tran ra:   --tp -1.5   (hoac -1.0)
  - ha muc tieu:   --target -15.0
```

Không tự nới trần, không tự hạ mục tiêu, không nén động để "cho đạt".

## 6. Hình phải không đổi một bit

`apply.py` mã hoá **chỉ audio**, rồi ghép:

```
ffmpeg -i IN.mp4 -i master_ok.m4a -map 0:v:0 -map 1:a:0 \
       -c:v copy -c:a copy -movflags +faststart OUT.mp4
```

`-c:a copy` nghĩa là audio đã đo chính là audio trong file cuối, bit y hệt.
`-c:v copy` nghĩa là hình không mã hoá lại.

`verify.py` chứng minh bằng cách so **md5 gói tin** luồng video:

```
ffmpeg -i FILE -map 0:v -c copy -f streamhash -hash md5 -
```

Cả 3 video test đều ra md5 **trùng**, và số frame giải mã trùng (6463 / 6787 / 263).

## 7. Đọc số ebur128

```
ffmpeg -i FILE -map 0:a:0 -af ebur128=peak=true:framelog=quiet -f null -
```

In ra khối `Summary:` trên **stderr**, không phải stdout. Parse 3 dòng:
`I: … LUFS`, `LRA: … LU`, `Peak: … dBFS`. Peak này là **true peak** vì có
`peak=true`. Giá trị có thể là `-inf` (file im lặng) → phải xử lý được.
