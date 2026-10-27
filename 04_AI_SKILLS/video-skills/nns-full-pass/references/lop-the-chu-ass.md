# Lớp thẻ chữ trong ASS

## Nguyên tắc gốc: MỘT file .ass, MỘT lần mã hoá hình

Sub và thẻ chữ nằm chung **một** file `.ass`, khác `Layer`, khác `Style`:

| Lớp | Layer | Style | Neo |
|---|---|---|---|
| Sub karaoke | 0 | `Sub` | `\an2` |
| Thẻ chữ | 1 | `Cardpunch` / `Cardstat` / `Cardlabel` / `Cardcta` | `\an2` |
| Khung sau thẻ | 0 | `CardPlate` | `\an7` |

Burn 2 lần = mã hoá hình 2 lần: mất chất lượng, mất thời gian, và lần 2 vẽ đè
lên chữ đã bị nén của lần 1.

Thẻ chữ phải dùng **chính font họ đó**. `burn.py` chỉ copy **đúng một** file
font vào thư mục tạm; đổi sang họ khác thì libass fallback sang font hệ thống
và **mất hết dấu tiếng Việt**.

## Dòng `Dialogue` phải có ĐÚNG 8 dấu phẩy trước Text

```
Dialogue: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Text
          ^1    ^2    ^3  ^4    ^5   ^6      ^7      ^8
```

Thừa một dấu phẩy → chữ hiện ra có dấu `,` dính ở đầu. Đã dính lỗi này một lần,
và đã phải viết hẳn `tools/sfx_pass/strip_commas_ass.py` để gỡ.

`selftest.py` kiểm bằng cách tách `line.split(",", 8)` phải ra đúng 9 phần, và
3 trường margin phải là số nguyên.

## Bản vẽ `\p1` phải vẽ từ (0,0) và neo `\an7`

**Đã trả giá một lần:** libass canh bản vẽ `\p1` theo **bounding box của chính
nó**, không theo gốc toạ độ. Vẽ toạ độ âm quanh gốc rồi dùng `\an5` để "căn
giữa" → khung lệch hẳn khỏi chữ.

Cách đúng:

```
{\an7\move(px,py+16,px,py,0,170)\p1 ...}m 20 0 l ... {\p0}
```

- Bản vẽ bắt đầu ở `m <r> 0` — tức từ (0,0), toàn bộ toạ độ dương.
- Neo `\an7` (góc trên-trái).
- Vị trí `px, py` **tính sẵn** bằng Python từ số đo font thật.

## Thẻ có khung thì dùng TRƯỢT + FADE, không pop-scale

Khung neo `\an7` (góc trên-trái), chữ neo `\an2` (đáy-giữa). Scale hai cái bằng
`\t(...\fscx112)` thì chúng **giãn từ hai gốc khác nhau** — nhìn thấy rõ chữ
trượt ra khỏi khung trong 140ms đầu.

- Thẻ **không** khung: pop-in `\fscx60 → 112% → 100%` + fade. Đẹp, an toàn.
- Thẻ **có** khung: `\move` trượt lên 16px trong 170ms + `\fad(70,90)`, áp y hệt
  cho cả khung, bóng và chữ.

## Kiểm glyph TRƯỚC khi burn

Font thiếu ký tự thì libass **vẽ ra khoảng trống và không báo lỗi gì cả**. Exit
0, video ra bình thường, chỉ là chỗ đó trống trơn.

Đo thật trên `BeVietnamPro-ExtraBold.ttf`:

```
'a' -> getmask().size = (78, 65)   có glyph
'→' -> getmask().size = (59,  0)   KHÔNG có glyph, vẫn có bề rộng
'✓' -> (59, 0)   KHÔNG có
'✗' -> (59, 0)   KHÔNG có
```

**Luật đúng: CAO == 0 trong khi ký tự không phải khoảng trắng.**

Lưu ý: `tools/sfx_pass/cards_to_ass.py` có hàm `missing_glyphs` riêng, nhưng nó
so với `getmask("")` = `(0,0)` — mà ký tự thiếu trả về `(59, 0)`, nên phép so
**không bao giờ khớp** và guard đó im lặng cho qua. Vì vậy guard thật của skill
này nằm ở `check_cards.py`, và nó chạy ở bước 6b — **trước** `cards_to_ass.py`
ở bước 6c. `selftest.py` kiểm cả hai hành vi này.

Nói ngắn: font này **không** có `→ ✓ ✗`. Đừng dùng chúng trong thẻ chữ.

## Auto-fit

`cards_to_ass.fit()`:

1. Vừa bề ngang (`rộng − 120`) → giữ nguyên.
2. Không vừa → thu nhỏ dần 2px một, xuống tối đa 72% cỡ gốc.
3. Vẫn không vừa → **xuống 2 dòng** tại chỗ chia làm bề rộng nhỏ nhất, rồi thu
   nhỏ lại.

Bề rộng đo bằng **chính file font sẽ dùng để burn** (PIL `getlength`), không
ước bằng số ký tự × cỡ chữ.

## Luật nội dung — thứ máy không tự biết

**Thẻ phải nói thứ mà màn hình và sub CHƯA nói.**

| Sai | Vì sao |
|---|---|
| Lời thoại: "cái này nhanh gấp ba" → thẻ "nhanh gấp ba" | lặp nguyên văn, sub đã nói rồi |
| Lời thoại: "mất bốn mươi bảy giây" → thẻ "47 giây" | in lại con số đang được nói |
| Màn hình đang hiện `12.4s` → thẻ "12.4s" | in lại con số đang hiện |
| Lời thoại: "cái này nhanh gấp ba" → thẻ "chỗ tôi từng sai" | ĐÚNG — thêm thông tin mới |

`check_cards.py` chặn 2 trường hợp đầu bằng cách đối chiếu transcript (±6s cho
lặp nguyên văn, ±4s cho con số). Trường hợp "con số đang hiện trên màn hình"
thì máy không đọc được — **đó là việc của người duyệt**.

## Giới hạn

| Luật | Giá trị |
|---|---|
| Tối đa 1 thẻ / 12 giây | `--card-every` |
| ≤ 4 chữ | `--max-words` |
| ≤ 2.5s, ≥ 0.4s | cố định |
| Không chồng thời gian | cố định |
| Không tụt dưới vùng an toàn | lấy từ `layout.json` |

## Dạng `cards.json`

```json
[
  {"start": 3.20, "end": 5.40, "y": 760, "style": "stat", "plate": true, "text": "3 giây"},
  {"start": 21.0, "end": 23.0, "y": 760, "style": "punch", "text": "sai chỗ này"}
]
```

| Style | Cỡ | Màu | Dùng cho |
|---|---|---|---|
| `punch` | 118 | trắng | câu nhấn |
| `stat` | 124 | vàng | con số |
| `label` | 104 | vàng | nhãn ngắn |
| `cta` | 110 | vàng | kêu gọi |

`plate: true` → khung nền đen mờ (alpha 0x26), bo góc 20px, viền vàng `#F5C426`
dày 5px, bóng đổ lệch (5, 9), padding 44×22.

## Verify dải thẻ

Dải pixel của thẻ phải tính từ **số đo THẬT**, không ước bằng công thức tay:

- cỡ chữ **sau auto-fit** (không phải cỡ gốc)
- **số dòng** sau khi xuống hàng (thẻ 2 dòng bị tính thành 1 dòng là sai ~60px)
- nếu có khung: cộng cả `padding + viền + bóng đổ` (khung to hơn khối chữ ~60px
  mỗi phía)
- cộng `RISE_PX` vì thẻ trượt lên 16px khi hiện ra

`verify_all.card_band()` gọi thẳng `cards_to_ass.fit()` và `plate_box()` để lấy
đúng các con số này.
