# Giao diện — toạ độ, màu, cỡ chữ

Mọi con số dưới đây nằm ở đầu `scripts/_common.py`. Sửa ở đó, chạy lại `chrome.py`
+ `apply.py`, **không** phải đụng vào filtergraph.

## Canvas

| Hằng | Giá trị | Ghi chú |
|---|---|---|
| `W`, `H` | 1080 × 1920 | 9:16, chuẩn Reels/TikTok/Shorts |
| `FPS` | 30 | Cả 2 nguồn đều bị `fps=30` ép về đây trước khi ghép |
| `BG` | `#0A0B0D` | Gần đen, không đen tuyệt đối — để lưới và glow còn đọc được |
| `GRID` | `#16191E`, bước 60px | Lưới mờ, chỉ để nền đỡ chết |

## Hai khung video

| Hằng | Giá trị |
|---|---|
| `PANEL_W` × `PANEL_H` | 496 × 882 |
| `LEFT_X` | 24 |
| `RIGHT_X` | 560 |
| `PANEL_Y` | 540 |
| `RADIUS` | 28 |

Kiểm cộng ngang: `24 + 496 + 40 + 496 + 24 = 1080`. Khe giữa 2 khung = 40px.

**Vì sao 496 chứ không to hơn:** khung phải giữ đúng 9:16 để không phải crop mặt
người nói. 496 × 1920/1080 = 881,8 → 882. Muốn to hơn thì phải thu hẹp lề hoặc
khe giữa — mà khe giữa còn phải chứa badge `VS` (bán kính 46, tức 92px) nên nó
đã tràn nhẹ lên hai khung, đúng như ảnh mẫu.

Chiều cao bị **giới hạn bởi chiều ngang**, không phải bởi canvas: hai khung 9:16
cạnh nhau thì cao nhất chỉ tới 882px, còn dư ~430px trên và ~390px dưới. Khoảng
trống đó là chỗ của nhãn và pill. Muốn khung to nữa thì phải bỏ bố cục cạnh nhau.

## Chữ và badge

| Thành phần | Hằng | Giá trị | Font |
|---|---|---|---|
| Nhãn `BẢN GỐC` / `AI ĐÃ CẮT` | `LABEL_SIZE`, `LABEL_CY` | 78px, tâm y = 450 | Be Vietnam Pro **Black** |
| Pill thời lượng | `PILL_TEXT`, `PILL_Y`, `PILL_H` | 34px, y = 1452, cao 62 | **Bold** |
| Badge `VS` | `VS_R`, `VS_TEXT` | bán kính 46, chữ 34px | **Black** |
| Badge `✦ AI` | `AI_BADGE_H`, `AI_TEXT` | cao 48, chữ 28px | **Bold** |

Ngôi sao `✦` được **vẽ tay** bằng polygon 4 cánh (`_star()` trong `chrome.py`),
không dùng glyph U+2726 — nhiều font Việt không có glyph đó và sẽ ra ô vuông.

## Màu

| Hằng | Mã | Dùng ở đâu |
|---|---|---|
| `YELLOW` | `#F5A623` | Nhãn phải, viền + glow khung đang chạy, pill phải, badge AI |
| `WHITE` | `#FFFFFF` | Nhãn trái, chữ VS |
| `PILL_GREY_BG` / `PILL_GREY_FG` | `#24262B` / `#B9BEC7` | Pill trái |
| `PILL_YEL_FG` | `#101112` | Chữ trên nền vàng |
| `DIM_BORDER` | `#2E3138` | Viền khung đang đứng hình |
| `VS_BG` / `VS_BORDER` | `#26282E` / `#3A3D45` | Badge VS |

## Trạng thái "đang chạy" vs "đứng hình"

| Hằng | Giá trị | Tác dụng |
|---|---|---|
| `DIM_BRIGHT` | 0.32 | Độ sáng của khung đứng hình |
| `DIM_SAT` | 0.35 | Độ bão hoà màu của khung đứng hình |
| `DIM_UI_ALPHA` | 0.45 | Nhãn + pill của bên không chạy mờ còn 45% |

Ba con số này là **toàn bộ tín hiệu** cho người xem biết đang xem bên nào. Đừng
để `DIM_BRIGHT` lên quá 0.45 — thử ở 0.40 thì trên màn điện thoại hai bên nhìn
gần như sáng bằng nhau, mất hẳn ý nghĩa.

Khung đang chạy còn có **glow vàng**: 3 vòng `rounded_rectangle` nở dần
(16 / 8 / 2 px, alpha 70 / 110 / 160) vẽ trên lớp riêng rồi `GaussianBlur(11)`.
Vẽ thẳng lên nền sẽ ra viền cứng, không ra quầng sáng.

## Đổi nhãn

`--label-left` và `--label-right` nhận chữ tuỳ ý. Nhãn dài hơn ~11 ký tự ở cỡ
78px sẽ tràn khung 496px — hạ `LABEL_SIZE` xuống 64 hoặc rút ngắn chữ. Hiện
`chrome.py` **không** tự thu nhỏ chữ cho vừa.
