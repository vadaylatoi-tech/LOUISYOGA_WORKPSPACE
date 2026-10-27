# Các cái bẫy ffmpeg đã gặp thật

## 1. `drawtext` segfault — đừng dùng

`drawtext` chết với `Fontconfig error: Cannot load default config file`.
Dùng `subtitles=file.ass:fontsdir=<dir>` thay thế: chạy tốt, dấu tiếng Việt không gãy,
không cần cài font vào hệ thống.

## 2. Đường dẫn tuyệt đối trong filter làm ffmpeg lỗi vì dấu hai chấm

```bash
# LỖI: ffmpeg thấy 'C:' rồi tưởng ':' là dấu phân cách option
-vf "subtitles=C:/duong/dan/sub.ass:fontsdir=C:/font"
```

Cách làm ở đây (`burn.py`, `render_ink`): copy `.ass` và font vào một **thư mục tạm**,
chạy ffmpeg với `cwd` là thư mục đó, filter chỉ dùng **tên tương đối**:

```bash
# cwd = thư mục tạm; fonts/ chứa .ttf; sub.ass nằm ngoài fonts/
-vf "subtitles=sub.ass:fontsdir=fonts"
```

`-i` và file ra vẫn dùng đường dẫn tuyệt đối bình thường — chỉ **trong filter** mới
kẹt dấu hai chấm.

## 3. `-ss` có thể nhảy sai frame — dùng `select=eq(n\,N)`

Muốn lấy đúng frame số N để so sánh thì đừng dùng `-ss`:

```bash
ffmpeg -v error -i v.mp4 -vf "select=eq(n\,165)" -fps_mode passthrough -frames:v 1 f.png
```

Đổi lại: ffmpeg phải decode tuần tự từ đầu, nên frame càng xa càng lâu. Với video
215 giây thì lấy frame cuối mất vài giây — chấp nhận được, vì đúng frame quan trọng
hơn nhanh. `verify.py` chỉ lấy 4 frame nên tổng thời gian vẫn nhỏ.

## 4. Phải ĐẾM lại số frame, không tin `nb_frames`

`nb_frames` trong container có thể thiếu hoặc sai. `count_frames()` dùng:

```bash
ffprobe -v error -select_streams v:0 -count_frames \
        -show_entries stream=nb_read_frames -of default=nw=1:nk=1 v.mp4
```

`verify.py` **đếm cả hai file** rồi mới so. Đo thật: vào 283 frame, ra 283 frame.

## 5. Ghim `-r <fps>` khi mã hoá lại

`concat` qua demuxer từng tụt về 25 fps. Ở skill này chỉ filter hình nên ít gặp, nhưng
`burn.py` vẫn ghim `-r <fps nguồn>` cho chắc, và `verify.py` so lại fps. Sai fps thì
số frame lệch và toàn bộ mốc sub trôi.

## 6. Tiếng: copy nguyên, đừng mã hoá lại

`burn.py` dùng `-c:a copy`. Chỉ vẽ chữ lên hình, không có lý gì mã hoá lại tiếng —
mã hoá lại là mất chất lượng và làm lệch độ dài. Nếu copy thất bại (codec không vào
được container), script tự thử lại bằng `aac 192k` và **nói rõ** là đã đổi.

`verify.py` so độ dài tiếng vào/ra, sai quá 0.05s là báo lỗi.

## 7. libass có thể exit 0 mà không vẽ gì

Đây là lý do `verify.py` phải đo pixel. Các trường hợp ffmpeg trả về 0 nhưng chữ
không có (hoặc sai):

| Nguyên nhân | Biểu hiện |
|---|---|
| `Style Fontname` sai tên họ | chữ vẫn hiện nhưng bằng **font hệ thống**, không phải font bạn chọn |
| Màu ghi `&HFF...` | chữ **trong suốt hoàn toàn**, không thấy gì |
| Nội dung Dialogue chứa `{` `}` | phần chữ đó **biến mất** |
| `PlayResX/Y` khác kích thước video | cỡ chữ và viền **sai tỉ lệ** |
| `--y` ngoài khung | chữ vẽ **ngoài** vùng nhìn thấy |

Cách đo: so frame ra với frame vào, đếm pixel lệch quá 60 mức xám **bên trong dải chữ**.
Số đo thật (1080x1920, cỡ chữ 80):

| Loại frame | pixel đổi trong dải | % diện tích dải | % pixel đổi nằm trong dải |
|---|---|---|---|
| có chữ, t=2.56s | 6868 | 3.79% | 100.0% |
| có chữ, t=6.19s | 12501 | 6.89% | 100.0% |
| có chữ, t=8.51s | 9697 | 5.34% | 100.0% |
| **không** chữ, t=4.08s | **0** | **0.0000%** | — |

Phân tách rất sạch, nên ngưỡng đặt ở 0.5% diện tích dải là thừa an toàn. Nhiễu nén
x264 nằm dưới mức 60 nên không lọt vào phép đếm.

## 8. Đọc bảng `name` / `cmap` của TTF bằng tay

Không phụ thuộc `fontTools` (không có trong danh sách phụ thuộc được phép). `nnscommon`
tự đọc sfnt:

- header 12 byte, rồi mỗi bảng 16 byte: tag, checksum, offset, length
- `ttcf` (TrueType Collection) -> lấy font đầu tiên tại offset ghi ở byte 12
- bảng `name`: ưu tiên bản platformID 3 (Windows, UTF-16BE), fallback platformID 1
  (mac-roman)
- bảng `cmap`: ưu tiên (3,10) format 12, rồi (3,1) format 4. Tra từng codepoint chứ
  không liệt kê hết — format 12 có thể có dải rất lớn
- bảng `OS/2`: `usWeightClass` ở offset 4

Font symbol (Webdings, Wingdings, Symbol, Marlett) **không có cmap unicode** -> bị loại
ngay ở bước này.

## 9. Console Windows mặc định cp1252

In tiếng Việt ra là crash `UnicodeEncodeError`. Mọi script gọi `C.setup_stdout()` ngay
đầu (`sys.stdout.reconfigure(encoding="utf-8")`), và mọi file mở bằng
`io.open(..., encoding="utf-8")`.

## 10. Thứ tự output khi gọi tiến trình con

`autosub.py` in tiêu đề rồi gọi script con bằng `subprocess.call`. Không `flush()`
trước thì chữ của tiến trình con **in ra trước** tiêu đề (stdout của cha bị đệm, con
ghi thẳng). Phải `sys.stdout.flush()` ngay trước mỗi lần gọi.
