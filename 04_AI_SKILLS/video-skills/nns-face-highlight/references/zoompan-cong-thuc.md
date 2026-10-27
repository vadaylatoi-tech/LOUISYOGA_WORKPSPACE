# Công thức zoompan, và hình học của việc kéo mặt vào giữa

## 1. Công thức đã kiểm

```
-vf "zoompan=z='<biểu thức theo on>'
             :x='<CX>-(iw/(2*zoom))'
             :y='<CY>-(ih/(2*zoom))'
             :d=1:s=<W>x<H>:fps=<fps>"
```

Vì sao từng phần:

- **`d=1`** — 1 frame ra cho 1 frame vào. Bỏ đi là `zoompan` sinh thêm frame
  (mặc định `d=90`) và số frame ra sai bét.
- **`s=WxH` + `fps=<fps>`** — giữ đúng kích thước và nhịp gốc.
- **`iw/(2*zoom)`** — `zoom` trong biểu thức `x`/`y` là **giá trị z của frame
  hiện tại**, nên viết `CX - iw/(2*zoom)` là "canh giữa vào điểm CX". Đã kiểm
  chạy đúng.
- **`zoompan` tự kẹp `x`/`y` vào vùng hợp lệ**, nên `z=1` cho ra frame nguyên
  gốc, không cần rẽ nhánh riêng.
- **`on`** là chỉ số frame RA. Vì `d=1` và fps không đổi nên `on` == chỉ số
  frame VÀO. Nhờ đó `plan.json` ghim được mốc theo frame chứ không theo giây.

`apply.py` dựng **một** chuỗi filter duy nhất cho cả video: biểu thức `z` là các
`if(between(on, f_start, f_end), <ramp>, <phần còn lại>)` lồng nhau, ngoài mọi
window thì `z=1`.

## 2. Đồ thị filter phải ghi ra FILE

Biểu thức `z`/`x`/`y` cho 9 window dài **2142 ký tự**. Nhét vào dòng lệnh
Windows là con đường ngắn nhất tới lỗi khó hiểu. `apply.py` ghi đồ thị ra file
rồi nạp bằng `-filter_complex_script <file>`, xoá file sau khi xong.

Đây cũng là cách né cái bẫy đã ghi trong hợp đồng: option filter dạng
`file=C:/...` bị hiểu sai vì **dấu hai chấm** là ký tự phân tách option của
ffmpeg. `-filter_complex_script` là tham số dòng lệnh bình thường nên đường dẫn
Windows không sao.

## 3. Ramp: cái bẫy đã mắc

Ramp-in dùng `p = (on - f0) / (f1 - f0)`, ramp-out dùng
`p = (f3 - on) / (f3 - f2)`. Ban đầu code chỉ có một hàm `ease(a, b)` rồi gọi
ramp-out bằng cách **đảo chỗ a/b** — mà hàm có nhánh `if b <= a: return "1"`,
nên ramp-out trả về **hằng số 1**: cú zoom không nhả ra, giữ nguyên độ zoom đến
frame cuối window rồi **giật** về 1. Bắt được lỗi này khi đọc đồ thị in ra ở
`--dry-run`, thấy chuỗi `1.000000+0.120000*1`.

Nay `facelib`-side có tham số `rev` rõ ràng. Kiểm bằng cách đo bề rộng mặt trong
file ra, window frame 165–240 (ramp-in 15 frame, giữ 45, ramp-out 15):

```
frame 164 : 217 px    <- trước window, chưa zoom
frame 168 : 235 px
frame 172 : 283 px
frame 176 : 336 px
frame 180 : 364 px    <- đạt đỉnh, bắt đầu giữ
frame 200 : 361 px
frame 225 : 368 px    <- hết giữ, bắt đầu nhả
frame 230 : 329 px
frame 235 : 253 px
frame 240 : 217 px    <- về đúng gốc
frame 244 : 217 px
```

Vào mượt, nhả mượt, về đúng bằng lúc chưa zoom. Hàm ease mặc định là
smoothstep `p*p*(3-2*p)` (đổi bằng `--ease linear`).

### 3-BIS. `verify.py` nay TỰ đo hình dạng ramp — và đây là bằng chứng nó cần

Bản verify đầu tiên chỉ đo **giữa đoạn giữ** + vài frame **ngoài** window. Đã
render thử một file cố ý sai (`ease` trả về hằng số 1 — tái tạo đúng lỗi trên):

```
verify --no-ramp-check  ->  DAT, exit 0     (bỏ sót hoàn toàn)
verify (mặc định)       ->  18 lỗi, exit 1
```

Lý do bỏ sót: giữa đoạn giữ thì zoom **đúng** bằng plan, còn frame đối chứng thì
nằm ngoài window nên zoom đã về 1. Cú giật nằm đúng ở hai đầu window — chỗ mà
không phép kiểm nào chạm tới.

Cách đo (mục 3 của verify): 5 mốc mỗi punch — `f_start`, giữa ramp vào,
`f_hold_mid`, giữa ramp ra, `f_end` — nhận diện mặt trên **cả file gốc và file
ra** tại cùng chỉ số frame, rồi so `rộng_ra` với `rộng_gốc × zoom_tại_mốc`.
Khung crop dự kiến tính bằng `crop_at()`, có kẹp đúng như `zoompan`.

**Chọn GIỮA ramp là có chủ ý**: tại `p = 0.5` thì smoothstep và linear cho cùng
một giá trị `0.5`, nên phép kiểm không cần biết `apply.py` chạy `--ease` nào.

Số đo thật (video 23.5s, 3 punch, zoom nâng lên 2.01–2.41), tỉ lệ
`rộng_đo / rộng_dự_kiến`:

```
đầu (z=1)      1.00  1.00  1.00
giữa ramp vào  0.94  0.98  0.99
giữ            1.00  0.99  1.02
giữa ramp ra   1.03  1.03  1.04
cuối (z=1)     1.00  1.00  1.00
```

Ngưỡng `--ramp-tol 0.30`. File cố ý sai cho 1.36–2.47 ở các mốc đó.

## 4. HÌNH HỌC: vì sao zoom 1.12 KHÔNG kéo được mặt vào giữa

Đây là chỗ dễ hiểu sai nhất cả skill.

Ở mức zoom `z`, khung crop rộng `W/z` và chỉ trượt được trong `[0, W - W/z]`.
Nghĩa là **tâm nhìn chỉ dịch được tối đa `(1 - 1/z)/2` bề ngang khung**:

| zoom | dịch được tối đa |
|---|---|
| 1.12 | **5.4%** |
| 1.50 | 16.7% |
| 1.70 | 20.6% |
| 2.00 | 25.0% |

Video dọc 9:16 rất thường để người ngồi **thấp** trong khung (chừa chỗ cho
caption / screen-record ở trên). Đo thật trên video này: từ giây 84 trở đi tâm
mặt nằm ở **y ≈ 1500 / 1920 = 78% chiều cao**. Muốn kéo về dải giữa 30% thì cần
dịch ~28% chiều cao — **zoom 1.12 không thể**, và đó không phải lỗi code.

Công thức tối thiểu (`facelib.zoom_to_center`): gọi `d` = khoảng cách từ tâm mặt
tới **viền gần nhất**, `b` = nửa bề rộng dải giữa cho phép, thì

```
z >= (cạnh/2 - b) / d
```

`plan.py` tính số này cho từng window và **tự nâng zoom** lên mức tối thiểu đủ
dùng (trần `--max-zoom`, mặc định 2.5), rồi in dấu `^` ở dòng đó. Kết quả thật
trên video 215s, yêu cầu `--zoom 1.12`:

```
 #  giây            zoom     lệch tâm dự kiến
 0   19.50- 22.00   1.120    6.2% x  2.0%     <- mặt đã gần giữa, giữ nguyên 1.12
 1   59.50- 62.00   1.120    0.0% x  4.5%
 2   99.50-102.00   1.707^   5.0% x 13.5%     <- phải nâng
 3  119.50-122.00   1.662^   5.6% x 13.5%
 4  139.50-142.00   1.931^   0.0% x 13.5%
 ...
```

Nếu không nâng thì `verify.py` sẽ báo `LECH GIUA` và exit 1 — đúng như nó phải
báo. Muốn giữ nguyên zoom đã yêu cầu thì `--no-recenter`; muốn giữ cả window
không kéo được vào giữa thì thêm `--allow-offcenter` (khi đó verify chỉ kiểm
"mặt không bị cắt").

### 4-BIS. NHẮM SÁT VIỀN DẢI GIỮA LÀ SAI — phải để dư (`--center-safety`)

Bản đầu nhân dải giữa với **0.9**, tức nhắm lệch tâm dự kiến **13.5%** so với
ngưỡng đạt **15%**. Đo lại trên file render thật thì máy nhận diện lệch thêm
**1–2 điểm %** (hộp mặt ở frame verify chọn không giống hộp lúc plan lấy mẫu):

```
plan nhắm 13.5%  ->  verify đo được 13.9% / 14.7% / 14.3%   (ngưỡng 15%)
```

Đạt, nhưng dư chỉ 0.3–1.1 điểm — một video khác là trượt. Nay hệ số mặc định là
`--center-safety 0.75` (nhắm **11.2%**):

```
plan nhắm 11.2%  ->  verify đo được 11.8% / 12.7% / 13.0%
```

Giá phải trả: zoom cần cao hơn một chút (2.27 → 2.41 ở window đầu). Đó là đánh
đổi đúng: thà zoom sâu hơn 6% còn hơn render xong mới biết trượt tiêu chí.

## 5. Không bao giờ cắt vào mặt

`facelib.solve_window` giới hạn zoom theo hộp mặt trước khi làm gì khác:

```
cần W/z >= bề ngang mặt + 2*margin   ->   z <= W / (fw + 2*margin)
tương tự cho chiều cao
```

Rồi kẹp `crop_x` vào đoạn `[max(0, fx2+m - W/z), min(W - W/z, fx1-m)]` để hộp
mặt nằm trọn trong khung. Nếu mặt sát viền thì `margin` bị ép nhỏ lại theo viền
thật, chứ không bịa ra khoảng trống không có.

Đã kiểm: yêu cầu `--zoom 6` trên mặt 233×311 px với `--margin 40` bị **hạ xuống
3.448** và đánh dấu `!`. Hộp mặt om trọn.

Một điểm quan trọng: hộp dùng để kiểm "om trọn" là **hộp GỘP cả đoạn punch**
(`face_fit`), không phải hộp của một frame. Lấy hộp một frame thì đầu/cuối đoạn
mặt có thể lồi ra khỏi khung đã crop.

## 6. Những cái phải kiểm sau khi render

- **`-r <fps>`**: qua filter/concat ffmpeg từng tụt về 25fps. `apply.py` luôn
  truyền `-r` và `verify.py` **so lại `nb_frames`**. Đo thật: vào 6463 frame,
  ra 6463 frame; vào 900, ra 900.
- **`-c:a copy`**: âm thanh không mã hoá lại, nên không lệch loudness, không
  suy giảm. `verify.py` kiểm luồng audio còn không.
- **Frame đối chứng**: `verify.py` lấy vài frame **ngoài** mọi window và so vị
  trí mặt với track gốc (cho phép lệch 3% cạnh dài). Đây là cái bắt được lỗi
  "zoom nhầm cả video". Đo thật: lệch 3–43 px, đạt.
- **Lấy frame bằng `select=eq(n\,N)`**, không dùng `-ss`: `-ss` có thể nhảy sai
  frame. `verify.py` gộp mọi frame cần vào **một** biểu thức select nên chỉ giải
  mã một lượt.
