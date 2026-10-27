# Karaoke trong ASS — tại sao KHÔNG dùng `\k`

## 1. Tag `\k` tô ngược ý muốn

Tag karaoke `\k` của ASS chia dòng thành từng đoạn và đổi màu theo thời gian. Nhưng
nó dùng **`SecondaryColour`** cho phần **CHƯA hát tới** và **`PrimaryColour`** cho
phần **ĐÃ hát qua**.

Nghĩa là nếu muốn "từ đang được nói thì nổi bật", `\k` cho ra hiệu ứng **ngược**:
từ đang nói và các từ phía sau giữ một màu, các từ đã nói xong đổi màu.

Chưa kể `\k` còn vài chỗ khó chịu khác:
- Toàn bộ hiệu ứng phải nằm trong **một** dòng `Dialogue`, nên mọi từ trong cụm buộc
  phải dính liền một khối thời gian — không chèn được khoảng nghỉ ở giữa.
- Đơn vị của `\k` là **centisecond**, phải tự cộng dồn; lệch một chút là trôi cả cụm.
- Các biến thể `\kf` / `\ko` render khác nhau giữa các bản libass.

## 2. Cách làm ở đây: một dòng Dialogue cho MỖI TỪ

Với cụm 4 từ, sinh ra **4 dòng** `Dialogue`. Dòng nào cũng chứa **cả cụm**, chỉ khác
ở chỗ từ đang được nói được bọc bằng lệnh đổi màu ghi thẳng:

```
Dialogue: 0,0:00:05.18,0:00:05.78,Sub,,0,0,0,{\an2\pos(540,1536)}{\c&H0000D6FF&}và{\c&H00FFFFFF&} HyperFrames để cùng
Dialogue: 0,0:00:05.78,0:00:06.32,Sub,,0,0,0,{\an2\pos(540,1536)}và {\c&H0000D6FF&}HyperFrames{\c&H00FFFFFF&} để cùng
Dialogue: 0,0:00:06.32,0:00:06.82,Sub,,0,0,0,{\an2\pos(540,1536)}và HyperFrames {\c&H0000D6FF&}để{\c&H00FFFFFF&} cùng
Dialogue: 0,0:00:06.82,0:00:07.20,Sub,,0,0,0,{\an2\pos(540,1536)}và HyperFrames để {\c&H0000D6FF&}cùng{\c&H00FFFFFF&}
```

Ưu điểm:
- Màu **ghi thẳng**, không phụ thuộc `SecondaryColour` hay cách libass hiểu `\k`.
- Mỗi từ có mốc bắt đầu / kết thúc riêng, sai một từ không trôi cả cụm.
- Đọc file `.ass` là thấy ngay từ nào sáng lúc nào — dễ soi lỗi.

Giá phải trả: số dòng `Dialogue` = số từ (không phải số cụm). Video 3,5 phút ra
khoảng 600–900 dòng. libass xử lý thoải mái.

## 3. Cửa sổ thời gian của từng từ — bàn giao ở `start` của từ sau

Trong `karaoke_events()`:

```
cửa sổ của từ thứ i = [ từ_i.start , từ_(i+1).start )
cửa sổ của từ cuối   = [ từ_cuối.start , cụm.end )
```

Cố ý **không** dùng `từ_i.end`. Lý do: Whisper phình `end` của từ để lấp đầy chỗ trống
tới từ sau (xem `sua-token.md`). Nếu lấy `end` thật thì giữa hai từ sẽ có khoảng
**không từ nào sáng** — nhìn như chớp tắt. Bàn giao ngay tại `start` của từ sau thì
vệt sáng chạy liền mạch.

`từ_i.end` vẫn có việc: nó quyết định **cụm kết thúc lúc nào** (từ cuối cùng), và
dùng để phát hiện khoảng nghỉ khi gom cụm.

## 4. Định dạng màu ASS: `&HAABBGGRR`

Đây là chỗ rất dễ sai vì **thứ tự byte ngược với HTML**:

| Màu | HTML | ASS |
|---|---|---|
| Trắng | `#FFFFFF` | `&H00FFFFFF&` |
| Đen | `#000000` | `&H00000000&` |
| Vàng | `#FFD600` | `&H0000D6FF&` |
| Xanh lá | `#00E676` | `&H0076E600&` |

- `AA` = **độ trong suốt ngược**: `00` = đục hoàn toàn, `FF` = trong suốt hoàn toàn.
  Ghi `&HFF...` là chữ **tàng hình** — vẫn exit 0, vẫn không thấy gì.
- `BB GG RR` = xanh dương, xanh lá, đỏ — **đảo ngược** so với `#RRGGBB`.

`build_ass.py` nhận cả hai dạng: `--active-color "#FFD600"` hoặc
`--active-color "&H0000D6FF&"`. Hàm `to_ass_color()` tự đảo byte, nên cứ dùng `#RRGGBB`
cho đỡ sai.

## 5. Ký tự phải escape trong nội dung Dialogue

`{` và `}` là ngoặc mở/đóng khối lệnh của ASS. Chữ trong transcript mà có `{` `}` sẽ
bị libass hiểu là lệnh và **biến mất**. `ass_escape()` đổi `{`→`(`, `}`→`)`,
`\`→`/`, và bỏ ký tự xuống dòng.

## 6. Neo vị trí: `\an2` + `\pos`

`{\an2\pos(x,y)}` — `\an2` neo **đáy, giữa**. Nên `y` chính là **đáy** của khối chữ,
và cụm dài phải xuống 2 dòng thì nó **nở lên trên**, đáy giữ nguyên. Nếu neo kiểu khác
(`\an5` giữa, `\an8` đỉnh) thì cụm 2 dòng sẽ trôi xuống và có thể tràn khỏi khung.

`WrapStyle: 2` = **không tự động ngắt dòng**. Nghĩa là cụm quá rộng sẽ chạy ra ngoài
khung chứ không tự xuống dòng — nên `build_ass.py` phải **đo bề rộng thật** và tự tách
cụm trước. Xem `dat-cho-va-vung-an-toan.md`.
