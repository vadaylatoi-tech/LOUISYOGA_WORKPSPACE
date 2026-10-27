# Vùng bảo vệ (`--protect`) — luật, và vì sao nó quan trọng

## Luật

Vùng bảo vệ là các đoạn (giây, trên timeline **GỐC**) mà **không một frame nào**
được phép bị cắt.

```
--protect "12.5-19.0,44-50"
```

Cách xử lý trong `plan.py`: sau khi tính xong cửa sổ sắp bỏ của một khoảng lặng,
cửa sổ đó bị **trừ đi** phần giao với mọi vùng bảo vệ. Phần còn lại (0, 1 hoặc 2 mảnh)
mới được frame-align và giữ. Mảnh nào ngắn hơn 0.05s thì bỏ. Nghĩa là:

- Khoảng lặng nằm **hoàn toàn** trong vùng bảo vệ → **không cắt gì**.
- Khoảng lặng **vắt qua** biên vùng bảo vệ → chỉ cắt phần nằm ngoài.
- Bản tóm tắt của `plan.py` in ra số khoảng lặng bị vùng bảo vệ chặn
  (`Bi vung bao ve chan`), để không bao giờ bị bảo vệ âm thầm.

## Vì sao nó quan trọng — trường hợp bắt buộc phải dùng

### 1. Đoạn chèn video khác đang có lời thuyết minh đè lên

Đây là ca nguy hiểm nhất và là lý do tính năng này tồn tại.

Ở đoạn đó có **hai luồng thời gian độc lập**:

- **Hình** chạy theo timeline của clip được chèn (demo màn hình, b-roll, screen record).
- **Tiếng** chạy theo timeline của người nói (voice-over đè lên).

Trong lời thuyết minh có khoảng lặng — người nói ngừng để khán giả kịp nhìn. Máy thấy
đó là khoảng lặng và cắt. Kết quả: **hình mất N frame nhưng nội dung hình không phải là
im lặng**. Con trỏ nhảy, thao tác trên màn hình mất một đoạn, animation giật.
Và tệ hơn: từ điểm đó về sau, hình chèn và lời thuyết minh **lệch nhau vĩnh viễn**.
Không sửa được ở bước sau, vì cả hai đã bị nướng vào cùng một file.

Với hình talking-head thuần thì cắt khoảng lặng là vô hại — mặt người đứng yên,
mất 0.4s không ai thấy. Với hình đang **chuyển động có ý nghĩa** thì không.

### 2. Nhạc / SFX đang ngân

Nếu file đã có nhạc nền hoặc SFX đang tail, khoảng lặng của **lời nói** không phải
khoảng lặng của **bản mix**. Cắt vào là nhạc bị nhảy nhịp. (Nếu chưa mix nhạc thì
cắt trước, mix sau — đó là thứ tự đúng.)

### 3. Animation / text overlay đang chạy

Chữ đang bay vào, lower-third đang mở. Cắt giữa animation là animation giật cục.

### 4. Sát các cắt cứng (transition, jump cut)

Cắt sát một cắt cứng đã có tạo ra hai mối nối cách nhau vài frame — mắt đọc thành
lỗi kỹ thuật. Dùng `--protect-cuts` (tự động, xem dưới).

## Cách tìm mốc để đưa vào `--protect`

**Cách 1 — xem danh sách khoảng lặng mà plan.py tìm được, rồi loại tay:**

```
python scripts/plan.py --video raw.mp4 --plan plan.json --dry-run
```

`plan.json`/bản in có `silence_runs` và `drops` kèm mốc giây. Mở video ở các mốc đó,
xem cái nào là đoạn chèn / animation.

**Cách 2 — xuất ảnh tại từng mốc để xem nhanh, không cần mở video:**

```
python scripts/plan.py --video raw.mp4 --plan plan.json
python -c "import json,io;d=json.load(io.open('plan.json',encoding='utf-8'));print('\n'.join('%.2f'%x['start'] for x in d['drops']))"
```

rồi với từng mốc `T`:

```
ffmpeg -i raw.mp4 -vf "select=eq(n\,<FRAME>)" -vsync 0 -frames:v 1 check_<FRAME>.png
```

Dùng `select=eq(n\,N)` **chứ không dùng `-ss`** — xem `cac-cai-bay.md`.

**Cách 3 — tự động cho các cắt cứng:**

```
--protect-cuts                 # bảo vệ ±0.25s quanh mỗi cắt cứng
--protect-cut-pad 0.4          # nới bán kính bảo vệ
--scene-threshold 0.20         # nhạy hơn (bắt được cả dissolve nhẹ)
```

Cơ chế: `select='gt(scene,TH)',metadata=print:file=-` của ffmpeg, đọc `pts_time`
từ stdout. Chạy thật trên `OUT/0822_edit_v4.mp4` (215s): tìm được **5 cắt cứng**,
sinh 6 vùng bảo vệ tổng 6.50s (đã gộp với `--protect` do người dùng đưa).

Lưu ý về `--scene-threshold`: 0.30 (mặc định) bắt cắt cứng rõ ràng. Hạ xuống 0.15–0.20
sẽ bắt thêm cả dissolve và cả **chuyển động camera mạnh** — với talking-head cầm tay,
ngưỡng quá nhạy sẽ bảo vệ gần hết video và ra 0 nhát cắt. Nếu `--protect-cuts` làm số
nhát cắt tụt hẳn, in ra số cắt cứng phát hiện được và nâng ngưỡng lên.

## Vùng bảo vệ dùng timeline NÀO

**Timeline GỐC** (trước khi cắt) — luôn luôn. `plan.py` chỉ nhìn thấy file gốc.

Nếu bạn đã cắt một lần và muốn cắt tiếp trên bản đã cắt: mốc phải là mốc trên **bản
đã cắt** (vì đó là `--video` mới). Muốn chuyển mốc cũ sang mốc mới thì dùng:

```
python scripts/remap.py --timemap lan1.plan.timemap.json --times "12.5,19.0"
```

## Việc `--protect` KHÔNG làm

- Không bảo vệ khỏi re-encode. Cả file vẫn được encode lại; `--protect` chỉ giữ frame,
  không giữ bitstream. Muốn giữ nguyên bitstream thì không dùng skill này.
- Không tự phát hiện đoạn chèn video. Scene detection tìm **cắt cứng**, không tìm
  "đoạn này là b-roll có voice-over đè". Cái đó phải người xem và chỉ ra.
- Không nới ra sau khi đã ghi plan. Đổi `--protect` là phải chạy lại `plan.py`.
