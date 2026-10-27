# Đặt chỗ cho sub — và luật không vắt qua ranh vùng an toàn

## 1. `--y` là ĐÁY của khối chữ

Sub được neo bằng `{\an2\pos(rộng/2, y)}` — `\an2` là neo **đáy, giữa**. Nên `--y`
chính là toạ độ đáy của khối chữ, tính từ **trên xuống** (y=0 là mép trên).

Mặc định: `y = 0.80 × chiều cao`. Với video 1080x1920 -> `y = 1536`.

Chọn neo đáy là có lý: cụm dài phải xuống 2 dòng thì khối chữ **nở lên trên**, đáy
giữ nguyên. Neo đỉnh hay neo giữa thì cụm 2 dòng sẽ trôi xuống và có thể tràn ra
ngoài khung.

## 2. Bài học trả giá: một chỗ an toàn ở đoạn này đè lên mặt ở đoạn khác

Đây là lỗi đã gặp thật. Đặt `--y 820` cho toàn bộ video: ở đoạn người nói ngồi xa thì
đẹp, nhưng ở đoạn họ ngồi gần / nhìn lên thì chữ **đè thẳng lên mặt**.

Không có con số y nào an toàn cho cả video nếu bố cục đổi. Phải **xem frame thật** rồi
mới chốt:

```bash
ffmpeg -v error -y -i "video.mp4" -vf "select=eq(n\,120)" -frames:v 1 thu.png
```

(Dùng `select=eq(n\,N)` chứ đừng dùng `-ss` — xem `cac-cai-bay-ffmpeg.md`.)

## 3. `--safe` — đổi chỗ theo từng đoạn giây

```bash
--safe "0-12:1100,12-30:1536,30-60:1250"
```

Đọc là: giây 0–12 đặt đáy chữ ở y=1100, giây 12–30 ở y=1536, giây 30–60 ở y=1250.
Giây nào không nằm trong đoạn nào thì dùng `--y` (hoặc mặc định).

Kiểm tra đầu vào rất chặt, sai là **báo lỗi và dừng**, không đoán:
- sai cú pháp -> in đúng dạng cần viết
- `end <= start` -> báo lỗi
- y nằm ngoài khung -> báo lỗi
- hai đoạn chồng nhau -> báo lỗi

## 4. LUẬT CỨNG: không bao giờ để một cụm vắt qua ranh vùng

Nếu một cụm bắt đầu ở đoạn A và kết thúc ở đoạn B, nó sẽ giữ **y của đoạn A** cho tới
lúc biến mất — tức là tràn sang đoạn B với vị trí sai, và rơi lên mặt. Đây đúng là lỗi
đã phải sửa.

`chunk_words()` xử lý ba chiều:

1. **Cắt cụm tại ranh giới.** Đang gom cụm, gặp từ thuộc đoạn có y khác -> đóng cụm
   ngay, từ đó mở cụm mới.
2. **Cắt ngắn thời gian hiển thị.** Từ cuối của cụm vẫn có thể `end` tràn qua ranh
   giới (do Whisper phình). Nên `end` của cụm bị **kẹp về đúng mốc ranh giới**.
3. **Cụm quá ngắn thì đổi vùng thay vì cắt.** Nếu cụm chỉ còn dưới `0.15s` trước ranh
   giới (`MIN_CHUNK_DUR`), cắt nó xuống 4–5 frame sẽ thành cái **nhấp nháy**. Trường
   hợp đó cụm được cho luôn **y của đoạn SAU** và giữ nguyên độ dài — sớm 0.1 giây ở
   chỗ đúng vẫn tốt hơn muộn nửa giây ở chỗ sai.

Số đo thật, `--safe "0-5.3:900,5.3-10:1536"`:

```
  [  4.22-  5.18] y=900   có sử dụng Claude    (tách vì: đủ 4 từ)
  [  5.18-  5.74] y=1536  và                   (tách vì: ranh vùng an toàn (y 900 -> 1536))
  [  5.78-  7.20] y=1536  HyperFrames để cùng  (tách vì: đủ 22 ký tự)

  co 1 cum qua ngan o cuoi vung nen duoc doi sang y cua vung sau:
      [  5.18-  5.74] y=1536  và
```

Từ `"và"` có `start=5.18`, `end=5.74` — vắt qua mốc 5.30, và chỉ còn 0.12s trước mốc
đó. Nên nó được tách thành cụm riêng rồi **chuyển sang y=1536** của đoạn sau.

`build_ass.py` **in ra** mọi cụm bị cắt ngắn và mọi cụm bị đổi vùng, để không có gì
xảy ra âm thầm.

## 5. Đo bề rộng thật, không đoán

`WrapStyle: 2` = libass **không tự ngắt dòng**. Cụm quá rộng sẽ chạy ra ngoài khung
chứ không tự xuống dòng. Nên phải biết trước cụm rộng bao nhiêu pixel.

Cách làm (2 lớp, không đoán):

1. **Hiệu chuẩn một lần.** Render chuỗi mẫu tiếng Việt 54 ký tự qua đúng ffmpeg+libass
   với đúng font và đúng cỡ chữ, đo khung bao, chia ra px/ký tự.
   Đo được: cỡ chữ 80 px, Be Vietnam Pro ExtraBold -> **28.0 px/ký tự**.
2. **Đo thật 3 cụm dài nhất.** Sau khi gom cụm xong, render thật 3 cụm dài nhất và
   in số pixel. Nếu tràn lề thì **dừng lại** và chỉ rõ nên giảm tham số nào.

```
  do be rong THAT cua 3 cum dai nhat:
      "và HyperFrames để cùng"  = 661 px  (OK)
      "video một cách hoàn"     = 556 px  (OK)
      "có sử dụng Claude"       = 484 px  (OK)
```

Bề rộng dùng được = `rộng − 2 × --margin`. Mặc định `margin = 0.06 × rộng`, nên video
1080 px có **950 px** dùng được.

Tắt phần đo bằng `--no-measure` (nhanh hơn vài giây, nhưng mất đảm bảo).

## 6. Gom cụm — thứ tự các lý do tách

Đang gom cụm, gặp từ mới thì tách nếu (theo đúng thứ tự ưu tiên này):

| # | Lý do | Tham số |
|---|---|---|
| 1 | ranh vùng an toàn (y đổi) | `--safe` — **luật cứng, không tắt được** |
| 2 | khoảng nghỉ ≥ ngưỡng | `--gap` (mặc định 0.35s) |
| 3 | đủ số từ | `--max-words` (mặc định 4) |
| 4 | đủ số ký tự | `--max-chars` (mặc định 22) |
| 5 | ước bề rộng vượt lề | tự tính từ hiệu chuẩn |
| 6 | hết câu (`. ! ? … : ;`) | `--no-break-punct` để tắt |
| 7 | dấu phẩy, khi cụm đã có ≥ 2 từ | `--no-break-punct` để tắt |

`build_ass.py` in lý do tách của từng cụm, nên soi lại rất nhanh.

## 7. Gợi ý con số cho 9:16 (1080x1920)

| Kiểu | Tham số |
|---|---|
| Mặc định, an toàn | `--y 1536 --max-words 4 --font-size 80` |
| Chữ to kiểu TikTok | `--max-words 3 --font-size 96 --outline 9` |
| Người nói ngồi gần, mặt chiếm giữa khung | `--y 1620` (đẩy xuống thấp) |
| Có chèn ảnh màn hình ở nửa dưới | `--safe "0-8:1536,8-20:620"` (đẩy lên trên) |

Nhớ chừa chỗ cho UI của TikTok / Reels ở đáy (khoảng 300–400 px cuối) và bên phải.

## 8. Video nguồn đã có sub cháy sẵn

Nếu `--video` là một file **đã dựng xong và đã cháy sub** (chứ không phải footage thô),
sub mới sẽ nằm đè lên sub cũ — hai dòng chữ chồng nhau. Đã gặp khi thử trên
`OUT/0822_edit_v4.mp4`.

Skill không tự phát hiện được chuyện này (nó không biết chữ trên hình là chữ ai vẽ).
Cách xử lý:
- Tốt nhất: dùng **footage thô**, chưa cháy sub.
- Nếu buộc phải dùng file đã cháy sub: xem frame thật, rồi đặt `--y` vào chỗ trống
  khác (thường là cao hơn), hoặc dùng `--safe` để tránh dải có sub cũ.
