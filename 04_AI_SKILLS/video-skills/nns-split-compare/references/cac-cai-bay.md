# Các cái bẫy — đã dính thật khi xây skill này

Không phải danh sách lý thuyết. Mỗi mục dưới đây đều là lỗi đã xảy ra trong lúc
dựng, kèm cách phát hiện và cách sửa.

## 1. Lỗ trong suốt xoá mất badge `✦ AI`

**Triệu chứng:** pha 1 badge AI hiện bình thường, pha 2 badge biến mất sạch.

**Nguyên nhân:** badge nằm **bên trong** khung phải (`rx+20, py+20`). Ở pha 2 khung
phải là khung đang chạy nên bị đục lỗ trong suốt — mà lỗ được đục **sau** khi vẽ
badge, nên nó xoá luôn badge.

**Sửa:** đục lỗ **trước**, vẽ badge **sau cùng**. Thứ tự trong `build()` bây giờ là:
… pill → **đục lỗ** → badge AI → save. Bất cứ thứ gì nằm đè lên khung đang chạy
đều phải vẽ sau bước đục lỗ.

## 2. `ImageDraw` mặc định GHI ĐÈ cả kênh alpha

**Triệu chứng:** nhãn và pill của bên đang mờ (alpha 45%) tự đục thủng lớp chrome —
chỗ đáng lẽ là nền đen lại lộ ra video/nền phía dưới.

**Nguyên nhân:** `ImageDraw.Draw(img)` trên ảnh RGBA **thay thế** pixel, không trộn.
Vẽ chữ màu `(255,255,255,114)` lên vùng nền đục sẽ biến vùng đó thành alpha 114.

**Sửa:** dùng `ImageDraw.Draw(base, "RGBA")` — chế độ này trộn alpha đúng nghĩa.
Riêng cú **đục lỗ** thì lại cần ghi đè, nên nó dùng `ImageDraw.Draw(base)` thường:

```python
d = ImageDraw.Draw(base, "RGBA")            # moi thu ve binh thuong
ImageDraw.Draw(base).rounded_rectangle(...)  # RIENG cu duc lo
```

Lưu ý: mỗi lần `Image.alpha_composite()` sinh ảnh **mới**, phải tạo lại đối tượng
`Draw` trỏ vào ảnh mới — nếu không mọi nét vẽ sau đó rơi vào ảnh cũ đã bị vứt.

## 3. Số giây phải tính từ SỐ FRAME, không lấy `format.duration`

`ffprobe` báo duration lệch vài ms so với `nframes / fps`. Nếu lấy duration để đặt
`d=` cho `color` source, phần nền sẽ dài/ngắn hơn video vài frame và `concat` sinh
frame thừa hoặc cụt.

`plan.py` luôn tính `dur = nframes / FPS`, và `nframes` **đếm packet**
(`-count_packets`), không đọc metadata `nb_frames` — metadata hay sai trên file đã
qua nhiều đời encode.

Kiểm được ngay: `apply.py` tự đếm frame file ra và **die** nếu lệch kế hoạch.

## 4. concat demuxer tụt fps về 25

Dùng `-f concat -safe 0 -i list.txt` trên vài build ffmpeg cho ra file 25fps dù cả
2 nguồn đều 30fps. Skill này dùng **filter** `concat=n=2:v=1:a=1` trong cùng một
filtergraph, và ép thêm `-r 30` ở output. `verify.py` đo lại fps trên file ra.

## 5. `-ss` nhảy sai frame khi trích ảnh

`ffmpeg -ss 3.2 -i in.mp4 -frames:v 1` có thể ra frame lệch vài đơn vị trên file có
B-frame. Mọi chỗ trích frame trong skill này (`chrome.py`, `verify.py`) đều dùng:

```
-vf "select=eq(n\,N)" -fps_mode passthrough -frames:v 1
```

Đây cũng chính là lý do phép kiểm mục 3 của `verify.py` tin được: nếu trích sai
frame thì "mồi nhử ±8" sẽ thắng frame đúng và verify fail.

## 6. Đường dẫn Windows KHÔNG được nhét vào chuỗi filter

`C:\...\thô.mp4` có dấu `:` và `\` — cả hai đều là ký tự cú pháp của filtergraph.
Nhét vào là vỡ graph với lỗi khó hiểu. Mọi file trong skill này đều đi qua `-i`,
và filtergraph chỉ nói chuyện bằng nhãn `[0:v] [1:a] [p1] …`.

## 7. Chỉ đo tiếng thì bỏ lọt lỗi hình, và ngược lại

Bản nháp đầu chỉ kiểm số frame + độ dài tiếng. Cả hai vẫn "OK" trong khi:

- Quên freeze → hai khung cùng chạy (mục 4 của verify bắt: khung đứng hình lệch
  16.8/255 giữa 2 frame, phải < 1.0).
- Dán nhầm ảnh tĩnh vào khung đang chạy (mục 5 bắt: phải > 1.0).
- Đảo tiếng 2 pha (mục 6 bắt: tương quan đường bao tụt xuống ~0.1).

Nên verify có đủ **cả 3 chiều**: đúng frame, đúng trạng thái tĩnh/động, đúng nguồn
tiếng theo pha.

## 8. So ảnh phải chuẩn hoá z-score

Khung đứng hình bị làm tối còn 32% và giảm bão hoà. So pixel thô với frame nguồn
sẽ lệch rất lớn dù **đúng frame**. `sig()` trừ trung bình rồi chia độ lệch chuẩn,
nên phép đo chỉ còn trả lời "đúng frame hay không", miễn nhiễm với chuyển tone
toàn cục.

## 9. Khung mờ 0.40 vẫn còn quá sáng

Thử `DIM_BRIGHT = 0.40`: trên preview desktop thì phân biệt được, nhưng thu nhỏ về
kích thước điện thoại thì hai bên nhìn sáng gần bằng nhau, mất hẳn tín hiệu "bên
nào đang chạy". Hạ xuống **0.32** mới đọc rõ ở mọi cỡ.
