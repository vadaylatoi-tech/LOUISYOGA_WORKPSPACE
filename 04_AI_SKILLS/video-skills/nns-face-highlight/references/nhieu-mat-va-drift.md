# Nhiều mặt trong một frame, và mặt trôi bao nhiêu

## 1. Vấn đề: "lấy hộp lớn nhất" là quy tắc MỎNG

Đo thật: một đoạn **screen-record chứa contact sheet ảnh mặt của chính diễn giả**
đã cho tới **11 detection trong một frame**. Khi mặt thật bị che, bị quay đi, hay
mờ vì chuyển động, thì ô ảnh to nhất trong contact sheet **thắng** — và tâm zoom
nhảy sang một ô ảnh. Người xem thấy cú punch-in bổ vào một khung ảnh nhỏ trong
màn hình, không phải vào mặt người nói.

Đã dựng lại tình huống này để kiểm chứ không chỉ viết ra: ghép một video
`talking-head 4s → contact sheet 4×4 (16 ô) 4s → talking-head 4s`.
Detector trả về **16 detection/frame** ở đoạn giữa. Chạy cả hai biến thể:
contact sheet động (16 frame khác nhau) và contact sheet **tĩnh** (16 ô y hệt
nhau — đây mới là ca khó, vì "ô lớn nhất" ổn định qua các mẫu nên rất dễ bị
chốt vào).

## 2. Luật đang dùng (`facelib.select_track`)

Chạy **hai lượt** trên toàn chuỗi mẫu, không phải một lượt online:

1. Mẫu đầu tiên có mặt → lấy hộp **lớn nhất**.
2. Mẫu sau → chỉ xét ứng viên **cách tâm đã nhận trước đó ≤ `max_jump`**, trong
   số đó lấy **lớn nhất**. Mặc định `max_jump = 0.08 × cạnh dài` (154 px với khung
   1080×1920).
3. Không ứng viên nào trong bán kính → **chưa nhận ngay**:
   - lọc trước theo **CỠ**: ứng viên phải có diện tích trong khoảng
     `1/3 .. 3` lần mặt đang bám (`--size-ratio`). Không đạt → từ chối thẳng,
     nhãn `tu-choi-nhay-xa-co-khac-han`.
   - đạt cỡ → giữ làm "chờ xác nhận". Nếu **mẫu kế tiếp** cũng nhảy về gần đúng
     chỗ đó (≤ `max_jump`) thì đây là **cắt cảnh / diễn giả đổi chỗ THẬT** →
     **nhận HỒI TỐ** cả các mẫu đang chờ.
   - không được xác nhận trong `--confirm-jump` mẫu (mặc định 2) → bắt lạc, bỏ.

### Vì sao cả hai chốt đều cần thiết — số đo

| Tình huống | Tỉ lệ diện tích mặt mới / mặt cũ | Kết quả |
|---|---|---|
| Ô ảnh trong contact sheet 4×4 | **0.06** (1/16 tuyến tính ⇒ 1/16 diện tích ô) | ngoài ngưỡng 1/3 → **từ chối**, đúng |
| Cắt cảnh thật (cảnh rộng → cảnh gần) tại t=78.8s | **0.42** | trong ngưỡng → **nhận**, đúng |

Chốt cỡ chặn contact sheet **một cách tất định**, không nhờ may mắn. Trước khi
thêm chốt này, bản chỉ có bán kính vẫn chặn được contact sheet *động* (vì ô "lớn
nhất" nhảy lung tung nên không bao giờ được xác nhận hai lần liền) nhưng với
contact sheet **tĩnh** thì ô lớn nhất ổn định → sẽ bị chốt vào sau 2 mẫu. Đã
kiểm: sau khi thêm chốt cỡ, cả 8 mẫu contact-sheet tĩnh đều bị từ chối, nhãn
`tu-choi-nhay-xa-co-khac-han`.

### Vì sao phải nhận HỒI TỐ

Bản đầu tiên từ chối thẳng cú nhảy rồi "bắt lại" sau 3 mẫu. Hậu quả đo được trên
video thật: mất 2 mẫu ngay sau cắt cảnh, và **hộp mặt gộp tụt từ x = 968 xuống
x = 844** — tức báo safe zone **nhỏ hơn sự thật 124 px**. Đúng loại lỗi đã phải
trả giá (xem `safe-zone-do-that.md`). Nhận hồi tố thì không mất mẫu nào:
hit rate trên video 215s tăng từ 86% → 88%, và khoảng "không có mặt" giả ở
80–84s biến mất.

## 3. Mặt trôi bao nhiêu — số đo thật

Khung 1080×1920, video 215.4s của cùng diễn giả, lấy mẫu mỗi 0.75s
(287 mẫu, 252 mẫu bắt được mặt). **Đo trên `box_det`, không đo trên hộp đã làm mịn.**

| Đoạn | Độ dài | Trôi tâm ngang | Trôi tâm dọc |
|---|---|---|---|
| 0–30s (một khuôn hình) | 30s | 108 px (10.0%) | 95 px (4.9%) |
| 84–140s (một khuôn hình) | 56s | 106 px (9.8%) | 85 px (4.4%) |
| 140–215s (một khuôn hình) | 75s | **55 px (5.1%)** | 62 px (3.2%) |
| cả video (có 2 lần đổi khuôn hình) | 215s | **328 px (30.4%)** | 503 px (26.2%) |

Kết luận rút ra, và `track.py` in đúng kết luận này:

- **Trong một khuôn hình**, mặt talking-head gần như không đi đâu: 55–108 px
  trong 30–75 giây. Khớp với con số tham chiếu đã ghi trước đây (127 px ngang
  trong 136s). Cỡ này thì **một tâm zoom cố định là đủ**.
- **Cả video có đổi khuôn hình** thì trôi 328 px ngang / 503 px dọc — hoàn toàn
  không thể dùng một tâm. Phải bám tâm theo **từng đoạn punch-in**.
- Ngưỡng `track.py` dùng để phán: trôi ≤ **3% khung** cả hai chiều thì in ra
  "một tâm cố định là đủ" kèm toạ độ trung vị; ngược lại in "phải bám tâm từng
  đoạn". Không đoán — in số đo ra để người dùng tự thấy.

## 4. Làm mịn: trung vị, KHÔNG phải trung bình

`--smooth 5` = trung vị trượt cửa sổ 5 mẫu, áp lên từng cạnh hộp.

Trung vị vì: một mẫu bắt sai (bắt vào ô ảnh, hoặc hộp phình ra vì mờ) kéo
**trung bình** đi cả trăm pixel, còn trung vị thì không.

**Nhưng trung vị làm CO hộp** — nó cắt bỏ đỉnh cực trị. Nên:
- hộp đã làm mịn (`box`) → chỉ dùng để **điều khiển tâm zoom**;
- hộp đo được (`box_det`) → dùng cho **mọi việc cần sự thật**: báo safe zone,
  đo drift, verify.

`track.py` giữ cả hai trường trong file JSON, và mẫu nào là nội suy thì có
`"fill": true`. Đừng dùng lẫn.

## 5. Khoảng không đo được mặt

Trên video 215s có một khoảng **32–58s** không mẫu nào có mặt — đó là đoạn
screen-record. `track.py` báo khoảng này ra (`gaps_no_face`), và `plan.py`
**mặc định từ chối** đặt punch-in vào đó, vì hộp mặt ở đấy chỉ là nội suy giữa
hai đầu — zoom theo nó là đoán. Muốn làm thật thì phải gõ `--allow-interpolated`,
và khi đó `verify.py` sẽ báo `KHONG THAY MAT` — đúng như nó phải báo.
