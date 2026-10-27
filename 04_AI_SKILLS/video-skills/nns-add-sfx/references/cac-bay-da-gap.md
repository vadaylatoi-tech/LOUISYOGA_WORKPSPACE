# Các bẫy đã trả giá — kèm cách tránh

Mỗi mục dưới đây là một lỗi **đã xảy ra thật**, không phải lo xa.

## Âm thanh

### 1. Cắt 0.2s từ điểm 0 của file SFX → cue im ru
35/86 file trong thư viện có im lặng ở đầu ≥ 0.15s; `mouse-click.mp3` im **1.02s**.
→ Luôn `probe.py` trước. `apply.py` và `verify.py` **raise lỗi cứng** nếu peak = 0.
Chi tiết: `onset-va-riser.md`.

### 2. Riser lấy cả file → lên đỉnh sớm rồi im trước lúc cần đập
→ Cue riser dùng `align: "end"`; `t` là giây đỉnh phải đập. Cắt ngắn thì **cắt từ
đầu**, giữ đoạn kết.

### 3. Một file "one-shot" hoá ra đánh nhiều lần
`whoosh.wav`: cú ở 0.135–0.410, im, cú nữa ở 1.40, cú nữa ở 2.70 (đỉnh cả file ở
đây). Lấy cả file thì thành 3 cú lệch nhịp.
→ Dùng `burst_end` (chỗ im ≥ 120 ms đầu tiên), không dùng độ dài file.

### 4. `loudnorm` âm thầm nén dải động
Đo thật: LRA 5.5 → 3.2 LU.
→ Dùng `volume=<G>dB` + `alimiter`. `verify.py` kiểm LRA mất ≤ 2.5 LU.

### 5. `alimiter=limit=X` mà quên `level=disabled` → limit vô nghĩa
`level=1` (mặc định) tự kéo biên độ lên lại, **undo** giới hạn.
→ Luôn `alimiter=limit=<L>:level=disabled`. `limit` là tuyến tính, không phải dB.

### 6. Tin true peak đo trên WAV
AAC có thể vượt (~+1 dB ở bitrate thấp).
→ Chừa 0.30 dB (`AAC_GUARD`) và **đo lại trên file AAC cuối**.

### 7. Ghim ngưỡng im lặng cứng (−30 / −35 / −38 dB) để tìm nhịp
Trên giọng thật của creator này, vùng −50…−35 dB là **phụ âm nhẹ và hơi thở**,
chiếm 14.6% thời lượng. Ngưỡng −35 dB đánh dấu sai 69 vùng, tất cả đều có tiếng.
Số thật: sàn ồn (p1 của RMS 10 ms) = **−84 dB**, mức nói (p70) = **−17.6 dB**.
→ Ngưỡng suy ra từ phân bố của **chính file đó**: `p70 − 12 dB`.

### 8. `floor + 8 dB` cao hơn cả đỉnh → không tìm ra onset, crash
Gặp thật với `temple-bell.mp3` (`pk = −6.79`, `p5 = −13.75`).
→ Kẹp `thr = max(pk − 30, min(floor + 8, pk − 6), −70)`.
Và một file không đo được onset phải bị đánh dấu `usable = false` **kèm lý do**,
không được nổ exception phá cả mẻ 86 file.

### 9. **AAC mã hoá lại làm trễ tín hiệu ~239 mẫu** — trừ trực tiếp là vô nghĩa
Đây là bẫy tinh vi nhất trong lần build này, và nó **làm một phép đo trông như
đạt trong khi nó chẳng đo gì cả**.

`verify.py` chứng minh SFX có thật bằng cách bù gain rồi trừ file gốc ra. Bản đầu
trừ thẳng, và:

| | Trừ thẳng | Sau khi chỉnh lệch mẫu |
|---|---|---|
| tương quan giữa 2 file | **0.248** | **0.9995** |
| sàn dư (median) | **−15.5 dB** | **−67.3 dB** |

Sàn dư −15.5 dB là **lệch pha của giọng nói**, không phải SFX — mà giọng thì to
nhất đúng ở chỗ có cue, nên phép kiểm vẫn "đạt". Đạt vì lý do sai hoàn toàn.

→ `_common.find_lag()`: tương quan chéo bằng FFT trên một cửa sổ 4 giây **không
có cue**, tìm độ lệch mẫu nguyên, chỉnh rồi mới trừ. Lệch đo được là **+239 mẫu
(4.98 ms)** trên cả 3 video test. `verify.py` in ra cả độ lệch và tương quan sau
khi chỉnh, và KHÔNG ĐẠT nếu tương quan < 0.90.

**Bài học chung: một phép đo "đạt" mà không biết sàn của nó là bao nhiêu thì chưa
phải phép đo.**

### 9-BIS. **"Phần dư cao hơn sàn" vẫn là phép đo YẾU — nó cho ĐẠT một file KHÔNG HỀ CÓ SFX**

Bẫy này bị bắt khi **test lại** chính bản sửa ở mục 9 ở trên, và nó chứng minh
mục 9 mới sửa được một nửa vấn đề.

Bản sau khi chỉnh lệch mẫu đo như sau: sàn = **median** phần dư ngoài các cue,
mỗi cue phải có **max** phần dư cao hơn sàn ≥ 3 dB. Nghe rất hợp lý. Thử nghiệm
đối nghịch: lấy đúng video gốc, chỉ **master** (`volume` + `alimiter`) mà **không
chèn một SFX nào**, rồi verify với cue sheet đầy đủ 15 cue:

```
[DAT]  SFX co trong file ra   15/15 cue noi hon san du >= 3.0 dB (san du -49.8 dB)
TAT CA 8 PHEP DO DEU DAT.          <- SAI. File này không có SFX nào cả.
```

Lý do: sàn là median **của cả file**, còn phần dư **dưới lời nói** (nhiễu AAC +
resample, tỉ lệ theo mức tín hiệu) cao hơn median đó rất nhiều. Đo thật: sàn
median −49.8 dB, nhưng phần dư trong đoạn có giọng là khoảng **−41 dB RMS**. Mà
cue thì được đặt đúng vào chỗ có giọng. Nên mọi cue "nổi hơn sàn" — kể cả khi nó
không tồn tại.

→ Cách đúng: **lọc khớp (matched filter)**. Ta biết chính xác đoạn tiếng đã trộn
(file, offset, dur, gain, fade) nên dựng lại đúng bed đó rồi đo hai số:

| | công thức | file CÓ SFX | file KHÔNG có SFX | trộn nhỏ hơn 20 dB |
|---|---|---|---|---|
| `corr` | `<dư, mẫu> / (\|dư\|·\|mẫu\|)` | 0.43 … 1.00 | ≤ 0.05 | 0.02 … 0.93 |
| `proj` (biên độ) | `<dư, mẫu> / <mẫu, mẫu>` | **0.0 dB** | **≤ −19 dB** | **−20 dB** |

`proj` là tiêu chí chính vì nó là ước lượng "to bằng bao nhiêu phần so với kế
hoạch", không bị lời nói to làm loãng như `corr`. Cột cuối cho thấy vì sao không
được dùng `corr` một mình: `whoosh` trộn nhỏ hơn 20 dB vẫn có `corr` 0.93.

Ba chi tiết phải làm đúng, cả ba đều đo được:

1. **ffmpeg trộn stereo → mono theo `(L+R)/√2`, không phải `(L+R)/2`.**
   Đo tỉ lệ thật: `1.41421353`. Dùng `mean(L,R)` thì mọi cue lệch **+3.0 dB**.
2. **`alimiter` của bước master có quyền kéo một cú đánh mạnh xuống thật.**
   Video 226s cần gain +4.2 dB → cue `punch @0.13s` đo ra **−7.1 dB** dù nó có
   thật trong file. Vì vậy ngưỡng là **−10 dB**, không phải −3 dB.
3. **`corr` cả lớp phải tính TRONG vùng có SFX.** Tính trên cả timeline thì
   video càng dài `corr` càng tụt (cùng một bản trộn đúng: **0.887** với video
   23s nhưng **0.312** với video 226s) → sẽ báo sai. Sau khi chỉ tính vùng có
   tiếng: 0.926 và 0.471.

Kiểm lại bằng 9 tình huống (4 bản trộn thật trên 3 video khác nhau, 3 bản phá
hoại, 1 bản thiếu thư viện, 1 bản verify bằng cue sheet của chính nó): đúng cả 9.
Bản thiếu 3 cue bị chỉ tên đúng 3 cue thiếu.

**Và: phép đo KHÔNG ĐO ĐƯỢC là phép đo KHÔNG ĐẠT.** Nếu không tìm được thư viện
SFX để dựng lại mẫu thì `verify.py` báo `KHONG DO DUOC` + exit 1, chỉ cách đưa
`--resources`, chứ không im lặng cho qua. Muốn bỏ hẳn thì phải nói rõ ý mình
bằng `--skip-residual`.

### 10. Cue quá dài đè lên cue khác
`build-up.mp3` có `rec_dur` **6.66s**. Không chặn thì nó đè lên toàn bộ khúc quanh
đó.
→ `ROLE_MAX_DUR` chặn trên theo vai (riser 2.5s, one-shot 0.7–0.8s).

## ffmpeg

### 11. `drawtext` segfault ("Fontconfig error: Cannot load default config file")
Không dùng `drawtext`. Skill này không cần chữ, nhưng nếu có thì dùng
`subtitles=f.ass:fontsdir=<dir>`.

### 12. `concat` qua demuxer có thể tụt về 25fps
Skill này **không** cắt/nối hình (dùng `-c:v copy`), nên không gặp. Nhưng nếu phải
nối: `filter_complex` `trim`/`concat` + `-r <fps>`, và **kiểm `nb_frames` sau khi
xuất**.

### 13. `-ss` seek có thể nhảy sai frame
Không dùng `-ss` để so sánh frame. Dùng `select=eq(n\,N)`.

### 14. Đường dẫn trong option của filter bị lỗi vì dấu hai chấm
`file=C:/...` trong filter string vỡ vì ffmpeg coi `:` là dấu tách option.
→ Skill này tránh hẳn: filter duy nhất có tham số là
`volume=...,alimiter=...` (không có đường dẫn), và scene detection dùng
`metadata=print:file=-` (ghi ra **stdout**, không phải đường dẫn).

### 15. `nb_frames` trong header không đáng tin
→ `verify.py` **không** đọc header. Nó đếm bằng `ffprobe -count_packets`.

Đo thời gian thật trên video 215s / 6463 frame:

| Cách | Kết quả | Thời gian |
|---|---|---|
| `-count_frames` (giải mã hết) | 6463 | **36.5s** |
| `-count_packets` (chỉ demux) | 6463 | **0.09s** |
| `streamhash md5` | `6fe779d2…` | 0.22s |

Cùng con số, nhanh hơn 400 lần. Với h264 trong mp4 thì 1 gói = 1 frame, và
`streamhash` đã chứng minh **từng bit** của luồng nên đếm gói là đủ. Bản đầu dùng
`-count_frames` làm `verify.py` chạy hơn 2 phút (2 file × 36.5s); giờ 4.4s.
Muốn giải mã thật: `verify.py --strict-frames`.

## Windows / Python

### 16. Console cp1252 crash khi in tiếng Việt có dấu
`UnicodeEncodeError: 'charmap' codec can't encode character '\u1ea1'`.
→ Mọi script gọi `C.setup_stdout()` (reconfigure utf-8) ở đầu, **và** toàn bộ text
in ra là tiếng Việt không dấu (ASCII). File `.md` mới có dấu đầy đủ.
Đọc/ghi file luôn `io.open(..., encoding="utf-8")`.

### 17. Đường dẫn lẫn `\` và `/` trong output nhìn rất khó đọc
→ `C.disp()` đổi hết về `/` khi in.

### 18. File tạm không dọn làm đầy đĩa
→ `apply.py` dùng `tempfile.mkdtemp()` và `shutil.rmtree` trong `finally`.
Muốn giữ lại để xem: `--keep-temp`.

### 19. preflight CHẾT trước khi kịp in hướng dẫn của chính nó (khi thiếu ffmpeg)

Đây là trạng thái **dễ gặp nhất** khi copy skill sang máy khác, và bản đầu xử lý
sai. `preflight.py` ghi nhận `[THIEU] ffmpeg` vào bảng, nhưng ngay sau đó vẫn gọi
`probe_media()` để đo video — mà hàm đó cần `ffprobe`:

```
  nns-add-sfx / PREFLIGHT
  [..]     dang do do to cua video, cho vai giay...
!! LOI: khong chay duoc 'ffprobe' ([WinError 2] The system cannot find the file
        specified). ffprobe khong doc duoc file nay, co the khong phai video.
```

Người dùng nhận được một dòng WinError, **không** nhận được bảng trạng thái và
**không** nhận được khối hướng dẫn cài ffmpeg — dù khối hướng dẫn đó đã viết sẵn
trong code. Một preflight không in nổi hướng dẫn của mình thì vô dụng.

→ Kiểm công cụ TRƯỚC, lưu `have["ffmpeg"] / have["ffprobe"]`, rồi **bỏ qua** mọi
phép đo cần công cụ đó (probe video, giải mã SFX, đo loudness) và đánh dấu là
`[LUU Y] chua kiem duoc vi thieu ffprobe`. Kết quả đúng: bảng đầy đủ + 2 khối
hướng dẫn cài ffmpeg + exit 1.

**Luật:** thứ tự kiểm phải theo thứ tự phụ thuộc. Cái nào là nền của cái khác thì
kiểm trước, và thiếu nó thì các phép đo phía sau **không được chạy**.

### 20. `--resources` trỏ vào thư mục rỗng → âm thầm dùng assets kèm sẵn

Bản đầu coi đây là chuyện nhỏ: in `[LUU Y]` rồi quay về `assets/sfx/`, exit 0.
Nhưng người dùng **đã chỉ rõ** thư viện họ muốn dùng. Chạy tiếp bằng thư viện
khác là đúng cái "tự thay thế" mà hợp đồng cấm — và họ sẽ chỉ phát hiện ra khi
nghe video xong thấy toàn tiếng lạ.

→ Nếu `--resources` được đưa mà không dùng được (không phải thư mục, hoặc không
có `.mp3/.wav` nào), thì **THIẾU + exit 1**, kèm 2 cách rất cụ thể:
Cách A bỏ hẳn `--resources` (nói rõ trong skill có sẵn mấy file),
Cách B tạo `<đường-dẫn>/sound-effects/` và tải file ở đâu.
`probe.py` và `plan.py` cũng chặn y như vậy (`_common.resources_problem()`), để
ai gọi thẳng script giữa pipeline cũng không bị đổi thư viện sau lưng.

### 21. Thiếu thư viện Python thì các bước sau in traceback

`preflight.py` bắt `ImportError` của `numpy` rất tử tế, nhưng nếu người dùng (hay
agent) gọi thẳng `probe.py` thì `numpy` được import **sâu trong** `_common.analyse_sfx()`
→ đổ ra 12 dòng traceback với đường dẫn nội bộ. Người dùng không đọc được traceback.

→ `_common.require_numpy(video)` gọi ngay sau `parse_args()` trong cả 4 script làm
việc (`probe`, `plan`, `apply`, `verify`): in khối hướng dẫn + `pip install numpy`
+ `python -m pip install numpy` (cho máy nhiều bản Python) rồi exit 1.
Kiểm bằng cách chặn thật: một `sitecustomize.py` raise `ImportError` cho `numpy`,
đặt vào `PYTHONPATH`. Cả 4 script đều ra hướng dẫn, không script nào ra traceback.

## Nguyên tắc chung

- **Đo, đừng tin giả định.** Onset, riser, nhịp, độ to, số frame — tất cả đều đo
  trên chính file đang xử lý.
- **Phép đo phải tự chứng minh nó phân biệt được đúng/sai.** Cách duy nhất biết
  điều đó: tạo một bản SAI cố ý (file không có SFX, thiếu cue, trộn nhỏ 20 dB)
  rồi xem phép đo có bắt được không. Xem mục 9-BIS.
- **Thiếu gì thì báo rõ + chỉ cách làm, rồi dừng.** Không đoán, không tự thay thế,
  không "chạy tạm".
- **Chỉ báo xong khi `verify.py` exit 0.**
