# Font tiếng Việt + libass — cái bẫy đắt nhất của skill này

## 1. Công thức vẽ chữ (đã kiểm, chạy tốt)

```bash
ffmpeg -i vao.mp4 -vf "subtitles=sub.ass:fontsdir=fonts" -c:a copy ra.mp4
```

- **KHÔNG dùng `drawtext`.** Nó segfault với thông báo
  `Fontconfig error: Cannot load default config file`.
  `subtitles=` + file `.ass` thì chạy tốt, dấu tiếng Việt không gãy, và **không cần
  cài font vào hệ thống**.
- `fontsdir` là **thư mục chứa file .ttf**, không phải file .ttf.
- File `.ass` phải nằm **NGOÀI** `fontsdir`. libass thử nạp mọi file trong `fontsdir`
  như font, nên nếu để `.ass` chung thư mục nó in
  `Error opening memory font 'probe.ass'`. Không chết, nhưng làm log rác.
- Header `.ass` phải có `PlayResX`/`PlayResY` **đúng bằng** kích thước video, và
  `ScaledBorderAndShadow: yes`. Nếu PlayRes khác kích thước frame, libass co giãn
  cỡ chữ và viền theo tỉ lệ `frame_h / PlayResY` — cỡ chữ ghi 80 sẽ không ra 80 px.

## 2. LUẬT VÀNG: `Style Fontname` phải là **nameID 1**, không phải nameID 16

libass khớp font theo **tên họ**, không theo tên file. Nhưng "tên họ" có tới hai loại
trong bảng `name` của file TTF:

| nameID | Tên gọi | Với BeVietnamPro-ExtraBold.ttf |
|---|---|---|
| 1 | tên họ "RIBBI" (legacy) | `Be Vietnam Pro ExtraBold` |
| 16 | tên họ kiểu chữ (typographic) | `Be Vietnam Pro` |

**libass dùng nameID 1.** Đặt nameID 16 vào `Style Fontname` thì libass **lặng lẽ bỏ**
file `.ttf` trong `fontsdir` và vẽ bằng font hệ thống.

Nguy hiểm ở chỗ: chữ vẫn hiện, **vẫn có dấu đầy đủ, vẫn đẹp**, nên rất dễ tưởng là
đã chạy đúng font mình chọn. Thực ra không.

### Số đo thật trên máy này

Render `"Cắt khoảng lặng ậm ừ"` cỡ 90 px, đếm pixel có mực:

| fontsdir | Style Fontname | Bold | Kết quả | Kết luận |
|---|---|---|---|---|
| (rỗng) | `ZzzNnsNoSuchFamily991` | 0 | **15249** px | ← chữ ký fallback |
| (rỗng) | `ZzzNnsNoSuchFamily991` | 1 | **20987** px | ← chữ ký fallback (đậm) |
| ExtraBold.ttf | `Be Vietnam Pro` (nameID 16) | 0 | 15249 px | **BỊ FALLBACK** |
| ExtraBold.ttf | `Be Vietnam Pro` (nameID 16) | 1 | 20987 px | **BỊ FALLBACK** |
| ExtraBold.ttf | `Be Vietnam Pro ExtraBold` (nameID 1) | 0 | 14560 px | dùng đúng font |
| ExtraBold.ttf | `Be Vietnam Pro ExtraBold` (nameID 1) | 1 | 14560 px | dùng đúng font |
| Black.ttf | `Be Vietnam Pro` (nameID 16) | 1 | 20987 px | **BỊ FALLBACK** |
| Regular.ttf | `Be Vietnam Pro` (nameID 1 = nameID 16) | 0 | 9481 px | dùng đúng font |
| Bold.ttf | `Be Vietnam Pro` (nameID 1) | 0 | 13414 px | dùng đúng font |

Lý do các mặt Regular / Bold / Italic / BoldItalic "may mắn" chạy đúng: với 4 mặt đó
nameID 1 **trùng** tên họ gốc. Mọi độ dày khác (Thin, Light, Medium, SemiBold,
ExtraBold, Black) có nameID 1 = `"<Họ> <Độ dày>"` và nameID 16 = `"<Họ>"` — đây chính
là chỗ sập.

`nnscommon.font_names()` trả về `ass_family` = **nameID 1**. Đừng sửa thành nameID 16.

## 3. `Style Bold` phải khớp độ dày của file font

`ass_bold_for(usWeightClass)`: weight ≥ 600 -> `Bold=0`, còn lại -> `Bold=1`.

- Font đã dày (ExtraBold, weight 800) mà để `Bold=0` thì libass lấy đúng mặt chữ dày đó.
- Đặt `Bold=1` lên font đã dày: nếu trong `fontsdir` không có mặt Bold cùng họ, libass
  **làm đậm giả** hoặc tuột về font hệ thống. Đo được: Regular.ttf + `Bold=1` ra
  11041 px (đậm giả) so với 9481 px (`Bold=0`).

## 4. Kiểm font bằng 3 lớp độc lập (`check_font_vietnamese`)

Không tin tên file. Không tin log ffmpeg. `preflight.py` kiểm 3 lớp:

**Lớp 1 — CMAP (chắc chắn nhất).** Đọc thẳng bảng `cmap` trong file font, tra 19
codepoint tiếng Việt khó: U+0102/0103, U+0110/0111, U+01A0/01A1, U+01AF/01B0,
U+1EA1, U+1EA3, U+1EA5, U+1EAD, U+1EAF, U+1EB7, U+1EC7, U+1ED1, U+1EEB, U+1EF9.
Thiếu một cái là loại ngay. Đọc bằng tay bảng `cmap` format 4 và format 12, không cần
`fontTools`.

**Lớp 2 — CHỮ KÝ FALLBACK (bắt lỗi im lặng).** Render bằng font này, rồi render lại
với `fontsdir` **rỗng** + tên họ bịa. Nếu hai bản **giống nhau từng pixel và cùng khung
bao** thì libass không hề dùng file font của ta. Đây là lớp duy nhất bắt được lỗi
"tên họ sai" ở mục 2.

**Lớp 3 — DẤU CÓ ĐƯỢC VẼ.** So `"Cắt khoảng lặng ậm ừ"` với bản ASCII cùng số ký tự
`"Cat khoang lang am u"`. Font bỏ dấu cho tỉ lệ ≈ 1.00; font vẽ ô vuông tofu cho tỉ lệ
rất cao.

Đo trên cả 9 độ dày của Be Vietnam Pro:

| File | weight | mực có dấu / không dấu | cao có dấu / không dấu |
|---|---|---|---|
| Thin | 100 | 1.050 | 1.136 |
| ExtraLight | 200 | 1.075 | 1.153 |
| Light | 300 | 1.086 | 1.169 |
| Regular | 400 | 1.092 | 1.203 |
| Medium | 500 | 1.088 | 1.203 |
| SemiBold | 600 | 1.082 | 1.241 |
| Bold | 700 | 1.084 | 1.241 |
| **ExtraBold** | **800** | **1.085** | **1.259** |
| Black | 900 | 1.095 | 1.259 |

Dải đo được rất chặt: mực 1.050–1.095, cao 1.136–1.259. Ngưỡng đang dùng:

```python
INK_RATIO_MIN   = 1.02    # dưới đây = dấu bị bỏ
INK_RATIO_MAX   = 1.45    # trên đây = vẽ ô vuông tofu
HEIGHT_RATIO_MIN = 1.08   # chữ có dấu BẮT BUỘC cao hơn chữ không dấu
```

## 5. Vì sao lớp 3 một mình là KHÔNG đủ

Thử với 4 font Windows chắc chắn không có glyph tiếng Việt:

| Font | mực có dấu / không dấu | lớp 3 nói gì | lớp 1 nói gì |
|---|---|---|---|
| Webdings | 1.143 | **lọt** (nằm trong dải) | loại — không có cmap unicode |
| Symbol | 1.340 | **lọt** | loại — không có cmap unicode |
| Marlett | 1.204 | **lọt** | loại — không có cmap unicode |
| Wingdings | 1.010 | loại | loại — không có cmap unicode |

3 trong 4 font rác **lọt qua** phép đo tỉ lệ mực, vì libass đã lặng lẽ fallback sang
font hệ thống và cái ta đo là font hệ thống, không phải font rác. Nên **lớp 1 (cmap)
mới là lớp quyết định**, lớp 3 chỉ là kiểm tra bổ sung.

## 6. Nếu người dùng chỉ `--font` mà font đó không đạt

Không được tự đổi sang font khác. `resolve_font()` trả về `explicit_failed` và
preflight in rõ: font nào, lý do gì, rồi để người dùng chọn. Tự thay font là vi phạm
luật "không đoán, không tự thay thế".

## 6-BIS. Nếu người dùng đưa `--resources` mà trong đó không có font tiếng Việt

Cũng **không được tự tụt về font kèm sẵn rồi chạy tiếp**. Người dùng đưa
`--resources` là đang nói "dùng thư viện của tôi"; lặng lẽ vẽ bằng font khác là
đoán. `resolve_font()` trả về `resources_unused=True` và:

- `preflight.py` in `[THIEU] font tieng Viet` + khối hướng dẫn 2 cách
  (Cách A: bỏ hẳn `--resources`; Cách B: tạo `<resources>/Font/` rồi bỏ file
  `.ttf` vào, kèm link Google Fonts), rồi exit 1.
- `build_ass.py` và `burn.py` cũng dừng với đúng khối hướng dẫn đó, để chạy lẻ
  từng script cũng không lọt.

Đã test: `--resources` trỏ vào thư mục rỗng → exit 1; `--resources` có
`Font/symbol.ttf` + `Font/webdings.ttf` → exit 1, in ra từng font bị loại kèm lý do.
Bỏ hẳn `--resources` → chạy bình thường, preflight in
`khong co --resources -> dung font kem san trong skill`.

## 7. Font tải ở đâu

- Be Vietnam Pro (đang kèm sẵn): https://fonts.google.com/specimen/Be+Vietnam+Pro
- Inter, Roboto, Noto Sans — đều đủ dấu tiếng Việt, đều có trên Google Fonts.
- Arial / Times của Windows cũng đủ dấu (cmap có hết), chỉ là nhìn không đẹp bằng.
