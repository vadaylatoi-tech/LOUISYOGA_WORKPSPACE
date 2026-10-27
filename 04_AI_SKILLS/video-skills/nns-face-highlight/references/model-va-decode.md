# Model nhận diện mặt: nằm ở đâu, và giải mã đầu ra thế nào

## 1. File model

Tên: `det_10g.onnx` — 16.9 MB, kiến trúc SCRFD/RetinaFace, thuộc bộ `buffalo_l`
của InsightFace. Chạy bằng `onnxruntime` trên CPU, không cần GPU.

Thứ tự tìm (đúng như `facelib.find_model()`), preflight **luôn in ra nó đang dùng
nguồn nào** để bạn không bị bất ngờ:

| # | Vị trí | Ghi chú |
|---|--------|---------|
| 1 | `<--resources>/models/det_10g.onnx` | ưu tiên cao nhất; nếu không có, tìm đệ quy cả cây `--resources` |
| 2 | `<skill>/assets/det_10g.onnx` | **kèm sẵn trong skill** → copy skill sang máy khác là chạy được ngay, không cần `--resources` |
| 3 | biến môi trường `FACE_MODEL_ONNX` | trỏ thẳng tới file |
| 4 | `~/.insightface/models/buffalo_l/det_10g.onnx` | vị trí InsightFace tự tải về |

Nếu không có chỗ nào: preflight **exit 1** và in ra cả ba cách khắc phục kèm
danh sách mọi đường dẫn đã thử. Đã kiểm thật đường báo thiếu này (chạy trong thư
mục skill không có `assets/`, `USERPROFILE` trỏ vào thư mục rỗng): exit code 1,
in đủ hướng dẫn, không tạo file nào.

## 2. Chữ ký vào/ra của model (đo trên máy này)

- Đầu vào: tên `input.1`, shape `[1, 3, '?', '?']`, NCHW, **RGB**.
  Chuẩn hoá: `(rgb - 127.5) / 128.0`.
- Ảnh được thu nhỏ để **cạnh dài = 640**, rồi *dán vào* khung 640×640 toàn số 0
  (padding ở phải và dưới). Với video dọc 1080×1920: scale 0.3333 → 360×640.
- Đầu ra: **9 tensor** — mỗi stride (8, 16, 32) có 3 tensor:
  - `score` shape `(N, 1)`
  - `bbox`  shape `(N, 4)`
  - `kps`   shape `(N, 10)` — skill này **không dùng** landmark
- Số anchor tại đầu vào 640×640: **12800 / 3200 / 800** (2 anchor mỗi vị trí).
  Con số này **không đổi theo số mặt tìm được** — nó là số anchor dày đặc. Nhờ
  vậy mới phân biệt được tensor của stride nào: sắp xếp theo `shape[0]` giảm dần.

## 3. Cách giải mã (đúng bản đã kiểm 55/55 lần bắt được mặt trên 3 video)

```
anchor_centers = meshgrid(x, y) * stride, lặp lại 2 lần (2 anchor/vị trí)
bbox           = distance2bbox(anchor_centers, preds * stride)
                 tức x1 = cx - d0, y1 = cy - d1, x2 = cx + d2, y2 = cy + d3
lọc            score >= thr (mặc định 0.5)
NMS            IoU <= 0.4
cuối cùng      chia hộp cho `scale` để về TOẠ ĐỘ GỐC của video
```

Bản gốc đã hoạt động: `tools/facetrack/facetrack.py` trong repo của người dùng.
`facelib.Detector` giữ **nguyên** phép giải mã đó, chỉ thêm: trả về *tất cả* hộp
(đã sắp theo diện tích giảm dần) thay vì chỉ hộp lớn nhất, để tầng trên áp được
luật chọn khi có nhiều mặt.

Đã đối chiếu: `track.py` và `facetrack.py` cho **cùng** kết quả trên cùng file
(2/20 mốc trên một clip 20s ít mặt — hai bên khớp nhau, chứng tỏ không sai lệch
khi port).

## 4. Vì sao KHÔNG dùng cách khác

- **`cv2.CascadeClassifier`**: `cv2` 5.0 trên máy này **không còn** class đó.
  `FaceDetectorYN` thì có nhưng **không có file weight YuNet** trên đĩa.
- **Mask màu da**: đã thử và cho kết quả sai — mask bắt cả tay, cả cổ, và cả
  vùng màu be trên đoạn screen-record. Không dùng.
- **Giả định mặt ở giữa khung / ở một dải y cố định**: xem
  `safe-zone-do-that.md`. Đây chính là lỗi đã phải trả giá.

## 5. Giá phải trả về thời gian (đo trên máy này)

Video 1080×1920, 215.4s, lấy mẫu mỗi 2.0s (108 mốc): **~14 giây** cho cả lượt
nhận diện (CPU). Nghĩa là lấy mẫu dày (mỗi 1.0s) cho video vài phút vẫn thoải
mái; không cần tối ưu gì thêm.
