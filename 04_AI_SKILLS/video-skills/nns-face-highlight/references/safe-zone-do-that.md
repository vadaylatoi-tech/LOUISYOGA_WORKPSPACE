# Safe zone: hộp ĐO ĐƯỢC, không phải hộp GIẢ ĐỊNH

Đây là bài học đã phải trả giá, và là lý do skill này tồn tại chứ không phải chỉ
là một cú `zoompan`.

## 1. Chuyện đã xảy ra

Một overlay được đặt ở **x 906–1054**, trên cơ sở tin rằng **cột x 900–1080 là
nền trống** ở video dọc 1080×1920.

Đo lại trên frame thật: **mép phải hộp mặt chạm tới x = 955**.

Kết quả: tấm plate phủ lên tới **3188 px² vùng da mặt được chiếu sáng**.
Vùng chồng lấn là x 906–955, rộng 49 px.

Con số 900–1080 không đến từ phép đo nào. Nó đến từ việc **nhìn một frame rồi
tưởng**. Frame đó có thể đúng là trống ở cột phải — nhưng ở giây khác thì không.

## 2. Đo lại trên máy này, cùng thể loại footage

Video 1080×1920, 215.4s, cùng diễn giả, lấy mẫu mỗi 0.75s, 252 mẫu bắt được mặt:

```
HỘP MẶT GỘP CẢ VIDEO   x 366..969   y 842..1704
```

**Mép phải mặt đo được là x = 969** — còn xa hơn con số 955 của lần trước.
Nghĩa là "cột x 900–1080 trống" sai **69 px**, và cột trống thật chỉ còn
**111 px** (x 969 → 1080), chưa trừ pad.

Chia theo từng khoảng 20 giây thì thấy rõ hơn vì sao một frame không nói được gì:

| khoảng | hộp mặt đo được | trống bên phải (pad 24) |
|---|---|---|
| 0–20s | x 416..827 | 229 px |
| 20–40s | x 476..828 | 228 px |
| **60–80s** | **x 368..968** | **88 px** |
| **80–100s** | **x 685..968** | **88 px** |
| 120–140s | x 634..961 | 95 px |
| 140–160s | x 641..854 | 202 px |
| 200–215s | x 625..848 | 208 px |

Nếu bạn chỉ nhìn frame ở giây 10 rồi kết luận "bên phải trống 250 px", thì tới
giây 80 overlay của bạn nằm đè lên má người nói.

## 3. Cách lấy số đúng

```
python scripts/track.py --video "<video>" --out track.json --step 0.75
python scripts/plan.py  --video "<video>" --track track.json \
        --out zones.json --report-safe-zones --zone-step 5 --pad 24
```

`zones.json` chứa:

| khoá | nghĩa |
|---|---|
| `union_do_duoc` | hộp mặt gộp toàn video, **đo trên frame thật** |
| `union_cong_pad` | như trên, nới thêm `--pad` px mỗi phía |
| `cot_an_toan_trai` / `cot_an_toan_phai` | dải x đặt overlay được |
| `hang_an_toan_tren` / `hang_an_toan_duoi` | dải y đặt overlay được |
| `windows[]` | hộp mặt **theo từng khoảng thời gian** + khoảng trống 4 phía |
| `khoang_khong_do_duoc` | các khoảng không đo được mặt — ở đây skill **không biết gì**, đừng coi là "trống" |
| `union_moi_ung_vien` | gộp **mọi** hộp model trả về, kể cả hộp bị luật chọn loại (ảnh mặt trong màn hình, người phụ). Biên phòng xa nhất. |

**Nguồn số:** chỉ `box_det` — hộp đo được. **Không** dùng hộp đã làm mịn, vì
trung vị trượt cắt bỏ đỉnh cực trị, tức nó **báo nhỏ hơn sự thật**. Báo nhỏ hơn
sự thật đúng bằng cái lỗi ở mục 1.

## 4. Ba cái bẫy còn lại

1. **`khoang_khong_do_duoc` không phải "trống"**. Ở đoạn screen-record 32–58s
   của video này, skill không đo được mặt nào. Điều đó nghĩa là *không có dữ
   liệu*, chứ không phải *không có mặt*. Đừng đặt overlay dựa vào khoảng đó.
2. **Số safe zone là toạ độ KHUNG GỐC.** Nếu bạn cũng áp punch-in, thì trong
   mỗi đoạn punch vùng nhìn bị thu lại theo `crop` của window đó trong
   `plan.json`. Overlay phải tính lại theo `crop` + `zoom`, không dùng thẳng số
   khung gốc. `plan.json` có sẵn `face_out_du_kien` = hộp mặt trong khung kết
   quả, dùng làm mốc.
3. **Vùng an toàn ≠ dải trống.** Kể cả khi cột bên phải trống 208 px, đặt plate
   sát mặt vẫn xấu. Số này cho biết *chỗ nào chắc chắn không đè lên mặt*, chưa
   phải *chỗ nào đẹp*.

## 5. Quy tắc một dòng

> Không có phép đo thì không có safe zone. Hộp giả định không được chấp nhận;
> hộp đo được thì được.
