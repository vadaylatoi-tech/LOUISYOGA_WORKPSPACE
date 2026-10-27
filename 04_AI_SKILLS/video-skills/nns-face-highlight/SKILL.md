---
name: nns-face-highlight
description: Zoom/punch-in bám đúng vùng MẶT diễn giả trong video talking-head, và báo SAFE ZONE đo được để skill khác đặt overlay không đè lên mặt. Input là 1 video có người nói (--video) + nơi lưu kết quả (--out); output là video đã có các cú punch-in mượt (ramp vào/giữ/ramp ra), kèm track.json (vị trí mặt theo thời gian) và plan.json (từng đoạn punch, zoom, tâm, khung crop). Vị trí mặt luôn ĐO bằng model det_10g.onnx trên frame thật, không bao giờ giả định mặt ở giữa khung. Trigger '/nns-face-highlight', hoặc các câu như 'zoom vào mặt cho video này', 'thêm punch-in vào mấy chỗ nhấn mạnh', 'video phẳng quá, đẩy máy vào gần mặt', 'cho tôi biết chỗ nào đặt chữ mà không đè lên mặt', 'đo hộp mặt để đặt overlay'.
---

## BƯỚC 0 — BẮT BUỘC, LÀM TRƯỚC MỌI THỨ

Ngay khi skill này được gọi, TRƯỚC KHI làm bất cứ việc gì, chạy:

    python <skill>/scripts/preflight.py --video "<video>" [--resources "<thư-mục>"]

Đọc kết quả:

- Preflight in "ĐẦY ĐỦ" -> làm tiếp các bước dưới.
- Preflight in "THIẾU ..." -> DỪNG NGAY. Không cắt, không render, không tạo file gì.
  Đưa NGUYÊN khối hướng dẫn mà preflight in ra cho người dùng, rồi HỎI họ:
  "Thiếu \<n\> thứ ở trên. Bạn làm theo hướng dẫn rồi bảo tôi, hoặc gửi cho tôi
  \<thứ còn thiếu\> để tôi chạy tiếp?"
  Chờ người dùng trả lời. TUYỆT ĐỐI không tự đoán, không tự thay bằng thứ khác,
  không bỏ qua bước đó để "chạy tạm".

- Nếu người dùng KHÔNG đưa --video: hỏi đường dẫn video thô trước khi làm gì.

Thêm một trường hợp riêng của skill này:

- Preflight in "VIDEO NÀY KHÔNG CÓ MẶT NÀO PHÁT HIỆN ĐƯỢC" -> cũng DỪNG NGAY.
  Đây **không phải lỗi**: video toàn motion-graphic, ảnh đồ hoạ, hay quay cảnh vật
  thì đúng ra phải cho 0 mặt. Skill này chỉ làm một việc là zoom bám **vùng mặt
  đo được**; không có mặt thì không có gì để bám, và chạy tiếp chỉ ra một cú zoom
  vô nghĩa vào giữa khung. Đưa nguyên khối hướng dẫn của preflight cho người dùng
  (nó có sẵn 3 lựa chọn: hạ ngưỡng, dùng ffmpeg zoom cố định, hoặc đưa lại đúng file).

---

## Cần gì để chạy

| Thứ cần | Bắt buộc? | Nếu chưa có thì làm gì (lệnh cụ thể) |
|---|---|---|
| `ffmpeg` + `ffprobe` | **Có** | Windows: `winget install --id Gyan.FFmpeg` · macOS: `brew install ffmpeg` · Linux: `sudo apt install ffmpeg` |
| `python3` | **Có** | Cài Python 3.8+ từ python.org |
| `numpy` | **Có** | `pip install numpy` |
| `onnxruntime` | **Có** | `pip install onnxruntime` (bản CPU là đủ, không cần GPU) |
| Model `det_10g.onnx` (17 MB) | **Có** | **Đã kèm sẵn** trong `assets/det_10g.onnx` -> không cần làm gì. Nếu file bị thiếu khi copy skill: copy lại nguyên thư mục skill kể cả `assets/`. Hoặc đặt file vào `<thư-mục-bạn-chọn>/models/` rồi gọi `--resources <thư-mục-bạn-chọn>`. Hoặc trỏ bằng biến môi trường: PowerShell `$env:FACE_MODEL_ONNX="D:\...\det_10g.onnx"` · CMD `set FACE_MODEL_ONNX=...` · macOS/Linux `export FACE_MODEL_ONNX=...` |
| `--resources` | Không | Skill này **không cần**. Model đã kèm sẵn. Chỉ dùng khi bạn muốn ép dùng file model riêng. Nếu bạn đưa mà trong đó **không có** `det_10g.onnx` thì preflight in `[CANH BAO]` + nói rõ nó đã bỏ qua và dùng bản kèm sẵn (không im lặng). Nếu đường dẫn **không tồn tại** thì preflight coi là THIẾU và dừng. |
| Transcript word-level | Không | Chỉ cần khi dùng `--from-transcript`. Dạng faster-whisper `word_timestamps=True`. Không có thì dùng `--every` hoặc `--at`. |
| Video **có mặt người** | **Có** | Preflight tự đo và báo tỉ lệ bắt được mặt. 0% thì dừng, xem BƯỚC 0. |

**Bước 1 luôn là chạy preflight. Preflight báo THIẾU thì dừng lại, làm theo
hướng dẫn nó in ra, không được chạy tiếp.**

---

## Skill này làm gì (và không làm gì)

Làm:
- Đo vị trí mặt theo thời gian bằng `det_10g.onnx` trên **frame thật**.
- Chọn các đoạn punch-in (theo mốc tay, theo transcript, hay theo nhịp), tính
  zoom + tâm + khung crop sao cho **không bao giờ cắt vào mặt**.
- Render bằng một chuỗi `zoompan` duy nhất, **âm thanh copy nguyên**.
- Đo lại trên file ra và báo đạt/không đạt bằng số.
- Báo **safe zone đo được** để skill khác đặt overlay không đè lên mặt.

Không làm: cắt khoảng lặng, chèn sub, chèn SFX, đổi màu, ghép cảnh.

---

## Quy trình 5 bước

### 1. Preflight (xem BƯỚC 0)

```
python scripts/preflight.py --video "<video>"
```

In bảng trạng thái + tỉ lệ bắt được mặt trên 6 mốc rải đều. Exit 1 nếu thiếu gì
hoặc video không có mặt.

### 2. Bám vị trí mặt -> `track.json`

```
python scripts/track.py --video "<video>" --out track.json --step 0.75
```

| Tham số | Mặc định | Ý nghĩa |
|---|---|---|
| `--step` | 1.0 | lấy mẫu mỗi bao nhiêu giây. **Phải nhỏ hơn `--hold` của plan.py**, nếu không vị trí mặt tại giữa đoạn giữ chỉ là số nội suy |
| `--thr` | 0.5 | ngưỡng điểm tin cậy. Mặt nhỏ/nghịch sáng thì hạ xuống 0.3 |
| `--max-jump-frac` | 0.08 | bán kính chấp nhận, theo cạnh dài khung (154 px với 1080×1920) |
| `--confirm-jump` | 2 | cú nhảy xa cần bao nhiêu mẫu xác nhận thì mới nhận (nhận **hồi tố**, không mất mẫu) |
| `--size-ratio` | 3.0 | mặt mới phải có diện tích trong 1/3..3 lần mặt cũ. Đây là chốt chặn ô ảnh contact sheet |
| `--smooth` | 5 | cửa sổ trung vị trượt |

Đọc gì trong output:
- **tỉ lệ bắt được mặt** — dưới 40% thì cân nhắc hạ `--thr`.
- **KHÔNG CÓ MẶT** — các khoảng không đo được (vd đoạn screen-record). plan.py sẽ
  tránh đặt punch vào đó.
- **hộp mặt gộp** — đây là số dùng cho safe zone.
- **KẾT LUẬN** — nói thẳng là một tâm zoom cố định có đủ hay phải bám từng đoạn.

Chi tiết luật chọn khi có nhiều mặt: `references/nhieu-mat-va-drift.md`.

### 3. Lập kế hoạch -> `plan.json`

Chọn **một** trong ba cách đặt mốc:

```
# a) nhịp đều - đơn giản nhất
python scripts/plan.py --video "<video>" --track track.json --out plan.json --every 20

# b) mốc chỉ định tay
python scripts/plan.py --video "<video>" --track track.json --out plan.json --at "12.5,40,73.2"

# c) bám vào từ nhấn mạnh trong transcript
python scripts/plan.py --video "<video>" --track track.json --out plan.json \
        --from-transcript words.json
```

Hình dạng mỗi cú punch: `--ramp-in 0.5` -> `--hold 1.5` -> `--ramp-out 0.5`,
`--zoom 1.12`.

| Tham số | Mặc định | Ý nghĩa |
|---|---|---|
| `--zoom` | 1.12 | mức zoom **yêu cầu**. Có thể bị nâng lên hoặc hạ xuống, xem dưới |
| `--margin` | 40 | mặt phải cách viền khung kết quả ít nhất bao nhiêu px |
| `--center-band` | 0.30 | tâm mặt phải vào dải giữa này của khung |
| `--center-safety` | 0.75 | nhắm vào **giữa** dải đó (11.2%) chứ không sát viền (15%), để còn dư khi verify đo lại. Đặt 1.0 là nhắm sát viền — đo thật thì gần như trượt |
| `--max-zoom` | 2.5 | trần zoom khi phải nâng để kéo mặt vào giữa |
| `--min-gap` | 3.0 | hai punch cách nhau ít nhất bao nhiêu giây |
| `--max-punch` | dur/25 | tối đa bao nhiêu punch |
| `--pause` | 0.30 | (transcript) nghỉ trước từ, từ đây trở lên tính là nhấn mạnh |
| `--emphasis-file` | `assets/emphasis_words_vi.txt` | danh sách từ/cụm nhấn mạnh |

**Zoom bị đổi là bình thường, và luôn được in ra:**
- dấu `^` = **nâng** zoom, vì zoom yêu cầu quá nhỏ để kéo tâm mặt vào dải giữa.
  Ở zoom 1.12 khung nhìn chỉ dịch được 5.4% bề ngang — một cái mặt nằm ở 78%
  chiều cao khung thì **hình học không cho phép** kéo về giữa. Xem mục 4 của
  `references/zoompan-cong-thuc.md`.
- dấu `!` = **hạ** zoom, để hộp mặt không bị cắt.

**Những mốc bị BỎ, và lý do — đọc phần "DA BO" trong output:**
- không đo được mặt nào trong đoạn đó (đoạn screen-record) -> ép bằng `--allow-interpolated`
- đoạn vắt qua chỗ **đổi cảnh** -> ép bằng `--allow-shot-change`
- không kéo được tâm mặt vào dải giữa -> ép bằng `--allow-offcenter`

Mọi cờ `--allow-*` đều là ép làm việc mà skill biết là sẽ sai. Dùng thì `verify.py`
sẽ báo — đó là đúng ý.

### 4. Render -> file video

```
python scripts/apply.py --video "<video>" --plan plan.json --out ket_qua.mp4
```

Một chuỗi `zoompan` duy nhất cho cả video, `-c:a copy` (âm thanh không mã hoá
lại), `-r <fps>` để không tụt fps. `--dry-run` in đồ thị filter + dòng lệnh mà
không xuất file. `--crf 18 --preset medium` mặc định.

### 5. Đo lại — BẮT BUỘC

```
python scripts/verify.py --video "<video>" --out ket_qua.mp4 --plan plan.json
```

**Chỉ được báo với người dùng là xong khi verify exit 0.** Verify kiểm:
1. số frame ra == số frame vào, kích thước + fps không đổi, còn đủ âm thanh
2. mỗi đoạn punch: **nhận diện lại mặt trong FILE RA** tại giữa đoạn giữ ->
   tâm mặt phải trong dải giữa 30%, hộp mặt phải nằm trọn trong khung, vị trí đo
   được phải khớp vị trí plan dự kiến
3. **HÌNH DẠNG cú zoom** — đo bề rộng mặt trên **cả hai file** tại 5 mốc mỗi
   punch: đầu (z=1) → giữa ramp vào → giữ → giữa ramp ra → cuối (z=1), rồi so
   với bề rộng dự kiến `rộng_gốc × zoom_tại_mốc`. Bắt đúng loại lỗi mà mục 2
   **không** bắt được: zoom giật thẳng vào không có ramp, hoặc zoom không nhả ra
   mà giật về 1 ở frame cuối. Tắt bằng `--no-ramp-check`, nới bằng `--ramp-tol`
   (mặc định 0.30).
4. vài frame **ngoài** mọi đoạn punch: mặt phải còn đúng chỗ như track gốc
   (bắt lỗi zoom nhầm cả video)

Không đạt thì in danh sách lỗi + việc cần làm cho từng loại lỗi.

> Mục 3 không phải cho đẹp: đã render thử một file cố ý bỏ ramp (ease trả về
> hằng số 1 — đúng cái lỗi đã gặp thật). Bỏ mục 3 thì verify **ĐẠT, exit 0** dù
> mắt thường thấy rõ cú zoom giật vào rồi không nhả. Có mục 3: 18 lỗi, exit 1.

---

## Chế độ riêng: báo SAFE ZONE cho skill khác

```
python scripts/plan.py --video "<video>" --track track.json \
        --out zones.json --report-safe-zones --zone-step 5 --pad 24
```

Xuất hộp mặt **đo được** theo từng khoảng thời gian + khoảng trống 4 phía, và
hộp gộp cả video. Đây là input mà skill đặt overlay cần.

Đọc `references/safe-zone-do-that.md` trước khi dùng số này. Tóm lại: đã từng có
overlay đặt ở x 906–1054 vì tin rằng cột x 900–1080 là nền trống; mép phải mặt
**đo được** chạm x 955, nên tấm plate phủ lên tới 3188 px² da mặt. Đo lại trên
máy này với cùng thể loại footage: mép phải mặt tới **x 969**. Hộp giả định
không được chấp nhận.

---

## Cái bẫy sáng tạo: mặt nhỏ nằm cao trong khung (webcam PiP)

Đo thật trên một video 23.5s kiểu **screen-record + webcam PiP tròn ở góc trên
trái** (mặt rộng ~330 px trong khung 1080, tâm ở x 26% / y 17%):

- Hợp đồng đòi tâm mặt vào dải giữa 15%. Ở vị trí đó, **hình học** buộc zoom lên
  **2.0–2.4**, và ở mức đó cả phần screen-record bị crop gần hết — kết quả là
  một cú close-up rất gắt vào mặt, chữ trên màn hình biến mất.
- Đó không phải lỗi: `zoompan` kẹp khung crop trong khung gốc, nên mặt nằm cách
  viền trên nửa chiều cao crop thì **không thể** về giữa nếu không zoom sâu hơn.
- Nếu ý bạn là "đẩy máy vào nhẹ cho đỡ phẳng", **đừng** để nó nâng zoom:

```
python scripts/plan.py --video "<video>" --track track.json --out plan.json \
        --every 6 --no-recenter --allow-offcenter
```

  Khi đó punch giữ đúng `--zoom 1.12`, verify chỉ kiểm "mặt không bị cắt" và in
  `[luu y]` cho từng đoạn lệch giữa — có chủ ý, không phải lỗi lặng.
- Cách thứ ba: nới dải giữa, ví dụ `--center-band 0.60`, để zoom cần thiết thấp hơn.

`plan.py` khi bỏ mốc luôn nói **đúng nguyên nhân** trong ba nguyên nhân khác nhau
(bị `--no-recenter` chặn / vượt `--max-zoom` / zoom nữa là cắt vào mặt) kèm con số
cần đặt, không nói chung chung.

## Kết quả đo thật (video 1080×1920, 215.4s, cùng diễn giả)

```
track  --step 0.75   : 252/287 mốc bắt được mặt (88%), 2 mẫu đổi cảnh nhận hồi tố
                       hộp mặt gộp x 366..969  y 842..1704
                       trôi tâm 328 px ngang / 503 px dọc  -> phải bám từng đoạn
plan   --every 20    : 8 punch, bỏ 2 mốc (1 chỗ không có mặt, 1 chỗ đổi cảnh)
                       6 punch phải nâng zoom 1.12 -> 1.66..1.93
apply                : 6463 frame vào -> 6463 frame ra, audio copy nguyên
verify               : ĐẠT. lệch tâm đo được 0.2%..6.9% ngang, 2.6%..13.8% dọc
                       (ngưỡng 15%); frame đối chứng lệch 3..43 px
```

## Kết quả đo thật lần 2 (video 1080×1920, 23.5s, webcam PiP góc trên trái)

```
preflight            : ĐẦY ĐỦ, 6/6 mốc bắt được mặt (100%), điểm tin cậy tb 0.82
track  --step 0.5    : 47/47 mốc bắt được mặt (100%)
                       hộp mặt gộp x 65..467  y 83..567
                       tâm mặt trôi 73 px ngang (6.8%) / 105 px dọc (5.5%)
plan   --every 6     : 3 punch, cả 3 phải nâng zoom 1.12 -> 2.01..2.41
apply                : 705 frame vào -> 705 frame ra
                       audio md5 vào == md5 ra (copy nguyên, không mã hoá lại)
verify               : ĐẠT. lệch tâm 1.2%/2.8%/5.6% ngang, 11.8%/12.7%/13.0% dọc
                       ramp: rộng mặt 340 -> 786 px (giữ) -> 297 px (cuối), tỉ lệ
                       so với dự kiến 0.94..1.04 ở cả 15 mốc
PSNR từng frame      : chỉ frame 167-240, 347-420, 527-600 bị đổi (đúng bằng 3
                       window). Ngoài đó PSNR 45-50 dB -> KHÔNG zoom nhầm cả video
```

Ba đường khác cũng đã chạy thật trên video này và verify exit 0: `--at "7,15"`
(chạy từ **bản copy** của skill, cwd khác), `--from-transcript` (transcript
faster-whisper thật, 113 từ, 6 từ nhấn mạnh), và video **không có tiếng**
(apply tự bỏ `-c:a copy`, verify ghi "vào không có tiếng, ra cũng không").

## Đọc thêm

| File | Nội dung |
|---|---|
| `references/model-va-decode.md` | model nằm ở đâu, chữ ký vào/ra, phép giải mã |
| `references/nhieu-mat-va-drift.md` | luật chọn khi 1 frame có 16 mặt, và mặt trôi bao nhiêu |
| `references/safe-zone-do-that.md` | bài học overlay đè lên mặt, cách lấy số đúng |
| `references/zoompan-cong-thuc.md` | công thức zoompan, bẫy ramp, hình học zoom |
