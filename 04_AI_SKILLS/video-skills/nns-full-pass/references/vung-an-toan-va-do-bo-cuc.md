# Vùng an toàn & đo bố cục

Đây là bước dễ sai nhất, và là bước trước đây phải làm bằng tay: soi frame rồi
gõ `--safe`. `layout.py` làm thay, nhưng nó **in ra số đo** để bạn kiểm — không
phải hộp đen.

## 4 thứ được đo, không thứ nào được đoán

### 1. Cắt cảnh thật

```
select=gt(scene,0.25)
```

Ngưỡng 0.25 bắt được cả những cú chuyển mềm. Bắt sót thì hạ xuống 0.20; bắt
thừa (mỗi lần người nói vung tay lại thành một cut) thì nâng lên 0.35.

Đoạn ngắn hơn `--min-seg` (mặc định 2.5s) được **gộp vào đoạn trước**. Lý do:
mỗi đoạn có một y riêng, đoạn 0.4 giây nghĩa là chữ nhảy vị trí trong nửa nhịp
thở — nhìn như lỗi render.

### 2. Hộp mặt

Model `det_10g.onnx` (SCRFD) của `nns-face-highlight`, chạy trên **frame thật**,
lấy mẫu `--samples` frame trong mỗi đoạn. Lấy `max(y2)` của mọi mẫu trong đoạn
— tức là chỗ mặt xuống thấp nhất trong đoạn đó, không phải trung bình. Trung
bình sẽ để chữ đè lên cằm ở đúng cái frame người ta gật đầu.

Không bao giờ giả định mặt ở giữa khung.

### 3. Khung chữ nhật (bố cục PiP / quay màn hình)

Đoạn **không thấy mặt** thường là đoạn chèn màn hình ghi hoặc khung video con.
Cách dò: tính **độ lệch chuẩn theo hàng** của frame xám.

- Hàng thuộc về khung nội dung → màu trải dài theo chiều ngang → std cao.
- Hàng thuộc về nền / letterbox / blur → gần như một màu → std thấp.

Lấy **dải liên tục dài nhất** có std > 35% std lớn nhất. Đáy của dải đó là đáy
khung. Khung chiếm trọn chiều cao thì không coi là vật cản (không có chỗ nào để
tránh cả).

Đây là ý "phân bố màu theo hàng" — nó không cần biết khung màu gì, chỉ cần biết
hàng nào có nội dung.

### 4. UI in sẵn trong footage

Ví dụ điển hình: pill thời lượng, watermark, thanh tiến trình đã cháy sẵn trong
file. Cách dò:

- Lấy `--ui-samples` (mặc định 14) frame **rải đều cả video**.
- Hàng nào **có nội dung** (std theo x > 12) nhưng **không bao giờ đổi** (≥97%
  cột có biên độ theo thời gian < 8) → nghi là UI in sẵn.
- **Lọc thêm: chỉ nhận dải HẸP (< 12% chiều cao).**

Cái lọc cuối là bắt buộc. Không có nó thì máy quay cố định + phông nền tĩnh sẽ
làm cả khung bị báo là UI. Đây là heuristic, nên nó được **in ra** để bạn nhìn,
chứ không âm thầm đẩy chữ đi chỗ khác.

## Chọn y

`y` là toạ độ **ĐÁY** của khối chữ (đúng hợp đồng `--safe` của `build_ass.py`).

Chiều cao khối chữ tính từ số đo thật:

```
block_h = font_size × 1.35 × số_dòng + 2 × outline
font_size mặc định = chiều_cao_video / 24      (giống build_ass.py)
outline  mặc định = 0.09 × font_size
```

Thứ tự quyết định:

1. Bắt đầu ở `bottom_safe`.
2. Đụng dải UI in sẵn → **đẩy LÊN** trên dải đó, lặp lại.
3. Còn đủ chỗ dưới vật cản (mặt / khung) → giữ nguyên, in ra thừa bao nhiêu px.
4. Không đủ chỗ ở dưới → **đẩy LÊN TRÊN vật cản**.
5. Đẩy lên cũng không vừa → giữ ở `bottom_safe` và in `CẢNH BÁO` kèm thiếu bao
   nhiêu px.

**Bí quá thì đẩy chữ LÊN, không bao giờ đẩy XUỐNG.** Đẩy xuống là rơi vào vùng
UI nền tảng che — chữ vẫn được vẽ, verify vẫn đạt, nhưng người xem trên điện
thoại không đọc được.

## Vùng an toàn nền tảng

```
PLATFORM_BOTTOM_PX_AT_1920 = 330
bottom_safe = chiều_cao − 330 × chiều_cao / 1920
```

Với khung 1920 → `bottom_safe = 1590`. Tức chữ phải nằm **trên y≈1600**.

Đáy khung ~330px bị UI TikTok/Facebook che: nút tương tác, caption của nền tảng,
tên tài khoản. Con số này đo từ ảnh chụp màn hình thật, không phải ước.

Khung khác 1920 thì tỉ lệ theo chiều cao. Muốn đè: `--bottom-safe <y>`.

## Khoảng cách tối thiểu

| Với | px | Vì sao |
|---|---|---|
| Hộp mặt | 48 | hộp mặt là hộp, cằm và tóc còn tràn ra ngoài hộp một ít |
| Đáy khung màn hình ghi | 36 | mép khung thường có viền/bóng |
| Dải UI in sẵn | 24 | chỉ cần không chồng |
| Mép trên khung | 6% chiều cao | chữ sát mép trên nhìn như lỗi |

## Đọc bảng bố cục

```
đoạn (giây)      y sub  y thẻ  vật cản       lý do / số đo
0-8.40            1590    760  mặt y412..980  dưới mặt, còn thừa 462px
8.40-19.20        1150    360  khung đáy y1010 KHÔNG đủ chỗ dưới khung (thiếu 84px) -> đẩy LÊN
19.20-45.00       1590    760  mặt y380..1002 dưới mặt, còn thừa 440px
```

- `y sub` — đáy khối sub
- `y thẻ` — chỗ đề xuất cho thẻ chữ (trên vật cản)
- Cột lý do luôn có **số**. Không có số nghĩa là có bug, báo lại.

Không đồng ý với kết quả đo thì đè thẳng:

```bash
--safe "0-12:1100,12-30:1536,30-60:1250"
```

## Luật cứng đã cài sẵn ở `build_ass.py`

Không bao giờ để một cụm chữ **vắt qua ranh giới `--safe`**. Cụm bị cắt ngắn
đúng tại ranh giới, cụm mới bắt đầu ở đoạn sau. Không làm vậy thì cụm giữ y của
đoạn trước và rơi lên mặt người nói ở đoạn sau. `build_ass.py` in ra rõ cụm nào
bị cắt vì lý do này.

## Trích frame để tự soi

**Không dùng `-ss`.** `-ss` nhảy tới keyframe gần nhất, frame lấy ra không phải
frame bạn muốn xem — lệch cả nửa giây là đủ để kết luận sai về bố cục.

```bash
ffmpeg -v error -y -i "video.mp4" -vf "select=eq(n\,120)" -fps_mode passthrough -frames:v 1 thu.png
```

Hoặc dùng `scripts/frames.py`, nó trích sẵn ở đầu mỗi đoạn, giữa mỗi thẻ và vài
cụm sub.
