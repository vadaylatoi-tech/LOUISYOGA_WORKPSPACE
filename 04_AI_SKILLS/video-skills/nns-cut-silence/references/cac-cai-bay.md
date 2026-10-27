# Các cái bẫy đã gặp (trả giá thật, không phải lý thuyết)

## 1. concat qua demuxer tụt về 25 fps

**Bẫy:** ghép các đoạn bằng concat demuxer (`-f concat -i list.txt`) thì file ra có thể
tụt xuống **25 fps** dù mọi đoạn vào đều 30 fps. Số frame sai, mọi mốc thời gian sai,
và không có thông báo lỗi nào.

**Cách làm đúng — đang dùng trong `apply.py`:**

```
filter_complex:
  [0:v]trim=start_frame=A:end_frame=B,setpts=PTS-STARTPTS[v0];
  ... (mỗi đoạn một nhánh) ...
  [v0][v1]...concat=n=N:v=1:a=0[vout]
và trên dòng lệnh: -r 30/1
```

Cộng thêm: **luôn đếm lại `nb_frames` sau khi xuất.** `apply.py` đếm ngay và `die()`
nếu lệch. `verify.py` đếm lại lần nữa. Không tin `nb_frames` trong metadata —
đếm packet: `ffprobe -select_streams v:0 -count_packets -show_entries stream=nb_read_packets`.

Đã kiểm thật: 53 đoạn → **đúng 6463 frame** và **215.4333s** audio. Và trong skill này,
8 đoạn → đúng 6402 frame, 213.400s.

## 2. `-ss` seek nhảy sai frame → đừng dùng `-ss` để so frame

**Bẫy:** `ffmpeg -ss 12.5 -i in.mp4 -frames:v 1 x.png` có thể ra frame **không phải**
frame 375. `-ss` trước `-i` seek theo keyframe rồi decode tiếp; `-ss` sau `-i` decode
từ đầu nhưng vẫn làm tròn theo timestamp. Với video có GOP dài, lệch vài frame là bình thường.

Hậu quả cụ thể: dùng `-ss` để chụp ảnh kiểm chứng "vùng này có phải im lặng không"
→ xem đúng nội dung nhưng **sai frame** → kết luận sai về vùng cắt.

**Cách làm đúng:**

```
ffmpeg -i in.mp4 -vf "select=eq(n\,375)" -vsync 0 -frames:v 1 x.png
```

`select=eq(n,N)` đếm frame đã decode, không liên quan timestamp. Chậm hơn (phải decode
từ đầu) nhưng **đúng frame**.

Cùng lý do: `apply.py` cắt hình bằng `trim=start_frame=`/`end_frame=` (chỉ số frame),
**không** bằng `-ss`/`-t` (thời gian). Và cắt tiếng bằng `atrim=start_sample=`/`end_sample=`
(chỉ số mẫu), không bằng `atrim=start=`/`end=` (giây) — chỉ số mẫu tính từ chỉ số frame
bằng `Fraction`, nên không tích luỹ sai số dù có 50 mối nối.

## 3. Đường dẫn trong option của filter làm ffmpeg lỗi vì dấu hai chấm

**Bẫy:** `metadata=print:file=C:/tmp/x.txt` — ffmpeg hiểu `C` là tên option và `/tmp/...`
là giá trị, vì `:` là dấu phân cách option trong filter.

**Cách làm đúng:**
- `metadata=print:file=-` (in ra stdout) — đang dùng cho scene detection.
- Hoặc `cd` vào thư mục rồi dùng đường dẫn tương đối.
- Hoặc escape `\:` — dễ sai trên Windows, tránh.

Trong skill này, **filter graph không chứa đường dẫn nào cả**. Graph được ghi ra file
riêng và nạp bằng `-/filter_complex <file>` (ffmpeg ≥ 7) hoặc `-filter_complex_script <file>`
(ffmpeg < 7). Đường dẫn nằm ở **argument dòng lệnh**, nơi dấu hai chấm vô hại.

Ghi chú phiên bản: `-filter_complex_script` bị deprecate ở ffmpeg 7 (chỉ cảnh báo, vẫn chạy),
`-/filter_complex` mới có từ ffmpeg 6.1. `apply.py` đọc major version rồi chọn cờ đúng.

## 4. `drawtext` segfault: "Fontconfig error: Cannot load default config file"

**Bẫy:** filter `drawtext` gọi fontconfig; trên máy không có config mặc định thì
ffmpeg **segfault**, không phải báo lỗi tử tế.

**Cách làm đúng:** không dùng `drawtext`. Dùng ASS + `subtitles=f.ass:fontsdir=<dir>`.
Đã kiểm: chạy tốt, **dấu tiếng Việt không gãy**, không cần cài font hệ thống.
`Style Fontname` phải là **tên FAMILY** của font (ví dụ `Be Vietnam Pro`), và file `.ttf`
phải nằm trong `fontsdir`.

Skill này không burn chữ nên không chạm tới, nhưng bước sau (`nns-auto-sub`) thì có.

## 5. `loudnorm` âm thầm chuyển sang chế độ dynamic và nén LRA

**Bẫy:** `loudnorm` một pass tự chuyển sang dynamic mode, nén tầm động lại.
Đo thật: **LRA 5.5 → 3.2**. Giọng nghe phẳng, mất nhấn nhá.

**Cách làm đúng:** `volume=<G>dB` rồi `alimiter=limit=<L>:level=disabled`.
Đo thật: `G=+4.6, limit=0.74` đưa -17.8 LUFS → **-14.0 LUFS** ở true-peak -2.3 dBFS,
LRA chỉ tụt 5.1 → 4.2.

**`level=1` sẽ undo giới hạn** — bắt buộc `level=disabled`.

Skill này **không** chuẩn hoá loudness (đó là việc của `nns-add-sfx`). Nó chỉ cắt.
Đây là lý do nó xuất WAV PCM: để bước loudness làm việc trên bản gốc.

## 6. AAC vượt true-peak so với WAV

**Bẫy:** encode AAC có thể làm true-peak vượt ~+1 dB so với WAV nguồn (rõ ở bitrate thấp;
256k thì gần như không). Chừa headroom, và **đo lại trên file AAC cuối**, không tin số
đo trên WAV.

Liên quan tới quyết định của skill này: file `.mp4` mang AAC 256k để xem ngay, còn
`.wav` PCM 16-bit đi kèm mới là **bản gốc** cho bước sau. Nguồn thường đã là AAC;
decode → PCM → AAC là **đời nén thứ hai**. Nếu bước sau lại encode AAC nữa thì thành
đời thứ ba: mất cao, true-peak vỡ. Đưa WAV cho bước sau là cắt được một đời nén.
Muốn file chính không tiếng luôn: `--no-mux-audio`.

## 7. Độ dài tiếng không bằng độ dài hình

**Bẫy:** sau khi ghép, tổng số mẫu audio hiếm khi khớp đúng `frames × sr / fps` —
audio nguồn thường ngắn/dài hơn video vài chục ms, và với fps không nguyên
(29.97 = 30000/1001) thì mỗi frame không ứng với số mẫu nguyên.

**Cách làm đúng:** cuối chuỗi audio trong `apply.py` có

```
apad,atrim=end_sample=<số mẫu dự kiến>
```

`apad` đệm im lặng vô hạn, `atrim` cắt đúng con số cần. Kết quả: độ dài tiếng **luôn**
bằng độ dài hình đến từng mẫu. `plan.py` in cảnh báo nếu audio nguồn ngắn hơn video,
để biết là có đệm.

Đo thật sau khi làm vậy: WAV 213.4000s vs hình 213.4000s, lệch **0.0 ms**.

## 8. Pad filter treo lơ lửng làm ffmpeg fail

**Bẫy:** graph có `asplit=2[aout][awav]` mà chỉ `-map [aout]` → ffmpeg báo

```
Error binding filtergraph inputs/outputs: Invalid argument
```

Không nói pad nào, không nói vì sao. Gặp thật khi thêm cờ `--no-mux-audio`: WAV vẫn
được map nhưng `[aout]` thì không, và cả lệnh chết.

**Cách làm đúng:** `build_graph()` nhận `want_mux` / `want_wav` và **chỉ sinh đúng
những đầu ra sẽ được `-map`**: cả hai → `asplit=2[aout][awav]`; chỉ mux → `[aout]`;
chỉ WAV → `[awav]`; không cái nào → bỏ hẳn nhánh audio. Không sinh rồi sửa bằng
`str.replace` — cách đó chỉ đúng cho một tổ hợp cờ.

Cùng họ với bẫy này: một input pad (`[0:v]`, `[0:a]`) **được phép** dùng nhiều lần trong
`filter_complex` — ffmpeg tự chèn `split`/`asplit`. Đã kiểm: 8 nhánh `[0:v]trim=...`
trong một graph chạy bình thường. Không cần tự chèn `split`.

## 9. Cross-correlation trên tiếng nói bám vào chu kỳ cao độ

**Bẫy:** dùng tương quan chéo để chứng minh bản đồ thời gian đúng thì đỉnh tương quan
có thể lệch một chu kỳ cao độ (giọng nam ~8ms) thay vì rơi đúng 0.

**Cách làm đúng trong `verify.py`:** cho phép lệch tới **1 frame**, và **bỏ qua** cửa sổ
nào vắt qua một mối cắt (về bản chất không thể khớp — nó là hai đoạn khác nhau ghép lại).
Cũng bỏ qua cửa sổ quá nhỏ tiếng (RMS < -45 dB) vì tương quan trên nhiễu vô nghĩa.

Thực tế đo được trên cả hai file test: **corr = 1.0000, lệch = 0 mẫu** — vì dữ liệu
đầu ra là chính các mẫu đã decode từ đầu vào, không resample.

## 9b. Cửa sổ sát đầu file làm phép đo độ trễ báo sai

**Bẫy:** để đo độ trễ, lấy cửa sổ đầu vào rộng hơn cửa sổ đầu ra `max_lag` mẫu về mỗi
phía, rồi quy `lag = argmax - max_lag`. Nhưng nếu cửa sổ nằm sát đầu file, phần bên trái
bị **kẹp về 0**, cửa sổ ngắn đi, mà công thức vẫn trừ `max_lag`.

Gặp thật khi bật `--trim-edges`: cửa sổ đầu tiên ở 00:00.057 báo **lệch -1911 mẫu
(-1.30 frame)** trong khi `corr = 1.0000` — corr hoàn hảo mà độ trễ khác 0 là dấu hiệu
kinh điển của lỗi hệ quy chiếu, không phải lỗi timing thật.

**Cách làm đúng:** ghi lại số mẫu **thực sự** nằm bên trái (`pad_left = center - s0`
sau khi kẹp) cho từng cửa sổ, rồi `lag = argmax - pad_left`.

## 9c. Cửa sổ trải rời rạc BỎ LỌT nhát cắt bị dịch chỗ

**Bẫy nghiêm trọng nhất trong verify.** Test ngược: lấy plan đúng rồi dịch nhát cắt
đầu tiên **muộn 10 frame**, giữ nguyên độ dài nhát cắt. Kết quả:

- số frame: khớp (401 = 401)
- độ dài tiếng/hình: khớp (lệch 0.0 ms)
- tương quan chéo 8 cửa sổ 0.8s: **corr 1.0000, lệch 0 mẫu — "OK"**
- → verify **thoát mã 0**. Sai mà báo đúng.

Vì sao: dịch nhát cắt trong vùng im lặng, giữ nguyên độ dài, thì mọi thứ **sau** nhát
cắt vẫn map đúng. Chỉ 0.33s nội dung ở ngay chỗ đó là khác. 8 cửa sổ trải trên 13.4s
không cửa sổ nào rơi vào 0.33s đó — mà cửa sổ thứ 4 lại còn bị kẹp ra xa vì nó vắt
qua mối cắt.

**Cách làm đúng:** thêm phép **khớp mẫu tuyệt đối tại từng biên đoạn giữ**.
`apply.py` chỉ COPY mẫu (không resample, không đổi sample rate), nên tiếng đầu ra phải
**trùng từng mẫu** với tiếng gốc — so hiệu số trực tiếp, không dùng tương quan.
Lấy 0.10s ở đầu và cuối mỗi đoạn giữ, yêu cầu `max |diff| <= 2 LSB`.

Với ca test trên, phép này bắt ngay: **lệch 639 LSB tại `dau doan 1 @ 00:06.200`**,
verify thoát mã 1.

Hai điều kiện để phép này dùng được:
- phải có **WAV pcm** (tiếng AAC là lossy, không so tuyệt đối được → hạ xuống CẢNH BÁO).
- offset của đoạn `i` trong đầu ra phải tính bằng **tổng số mẫu các đoạn trước**, chứ
  không phải `round(new_start_frame * sr / fps)`. Hai cách này chỉ trùng nhau khi
  `sr/fps` là số nguyên (44100/30 = 1470, 48000/30 = 1600 thì trùng; 29.97 fps thì không).

Bài học tổng quát: **verify phải được thử ngược.** Một verify chỉ chạy trên file đúng
thì không biết nó có răng hay không.

## 10. Console Windows cp1252 crash khi in tiếng Việt

**Bẫy:** `print("Đã xong")` trên console cp1252 → `UnicodeEncodeError`, script chết
ở đúng dòng thông báo, người dùng không biết gì.

**Cách làm đúng:** mọi script gọi `C.setup_io()` ở đầu (reconfigure stdout/stderr sang
utf-8), và mọi lần đọc/ghi file dùng `io.open(..., encoding='utf-8')`.

## 11. VFR làm mọi phép tính frame sai

**Bẫy:** file quay điện thoại / ghi màn hình hay là VFR. Khi đó `frame × 1/fps` không
phải thời gian thật của frame đó, và cắt theo frame sẽ lệch tiếng dần.

**Cách làm đúng:** `preflight.py` so `r_frame_rate` với `avg_frame_rate`; lệch > 0.5%
thì báo THIẾU và chỉ cách chuyển sang CFR. `plan.py` từ chối chạy trừ khi có `--allow-vfr`.

```
ffmpeg -i raw.mp4 -c:v libx264 -crf 16 -r 30 -c:a copy cfr.mp4
```

## 12. Verify chỉ đo TIẾNG thì bỏ lọt hoàn toàn lỗi HÌNH không bị cắt

**Bẫy (đã dựng thật rồi đo, không phải suy đoán):** ghép một file trong đó **tiếng đã
cắt đúng** nhưng **hình là 677 frame đầu của bản gốc** — tức hình không hề bị cắt, nên
từ giây 11.77 trở đi hình lệch tiếng, đến cuối lệch 0.93s. File đó:

- đúng số frame (677 = kế hoạch), đúng fps 30/1
- độ dài tiếng == độ dài hình (lệch 0.0 ms)
- tương quan chéo 8 cửa sổ: corr 1.0000, lệch 0 mẫu
- khớp mẫu tuyệt đối 7 biên: 0.0 LSB
- peak vùng cắt: -43.4 dB

→ **verify thoát mã 0 và báo "ĐẠT"** trên một file lệch tiếng/hình gần 1 giây.
Lý do: mọi phép kiểm đều so tiếng-với-tiếng, còn hình thì chỉ **đếm** frame.

**Cách làm đúng:** verify phải so **nội dung hình** với frame gốc mà time-map chỉ ra.
Cách rẻ và nhạy: lấy chữ ký ảnh xám 64×64 của vài frame đầu ra (một lần decode duy nhất,
`select='eq(n\,A)+eq(n\,B)+...'` + `-frames:v k` để ffmpeg dừng sớm), rồi so MAE với
frame gốc `N + shift` và với các mồi nhử `N + shift_khác`, `N + shift ± 1, ± 2, ± 8`.
Frame khớp nhất phải là frame plan nói.

Số đo thật trên 0822.mp4 (1080x1920, 30fps): frame đúng MAE **0.10**, frame lệch 8 frame
MAE **6–44**, tức cách biệt 60–400 lần. Bắt được cả trường hợp lệch **1 frame** (MAE
2.8–9.9 so với 0.10). Toàn bộ phép kiểm này tốn **~1.4s** cho video 23.5s.

**Hai cái bẫy con bên trong phép kiểm này:**

1. Hai frame liền kề trong vùng im lặng gần như giống nhau (MAE 0.13 vs 0.28), nên
   **không** dùng cách biệt ±1 frame để kết luận "đo được". Chỉ tính "kết luận được"
   trên các mồi nhử XA (shift của đoạn khác, ±8 frame); ±1/±2 chỉ dùng để BẮT LỖI khi
   nó khớp hơn hẳn (> 0.30 MAE).
2. Video gần như tĩnh (slide, màn hình không đổi) thì mọi frame giống nhau → phải báo
   **CẢNH BÁO "không kết luận được"**, không được báo ĐẠT giả.

## 13. `--no-wav` + `--no-mux-audio` cùng lúc = file không có tiếng, phát hiện quá muộn

**Bẫy:** hai cờ đó cộng lại tạo ra mp4 **không có stream tiếng nào**. Bản đầu chỉ in
`CANH BAO ... Chac chan chua?` rồi chạy tiếp: encode xong toàn bộ video (chậm), rồi
verify mới báo SAI 2 mục ở cuối. Người dùng mất công chờ để nhận một file vô dụng.

**Cách làm đúng:** `apply.py` **từ chối ngay từ đầu** (exit 1) và in 3 lựa chọn kèm lệnh
copy-paste được. Ai thật sự muốn video im lặng thì thêm `--allow-no-audio`; khi đó
verify hạ các phép kiểm tiếng xuống CẢNH BÁO và vẫn kiểm hình bình thường.

## 14. `yuvj420p` (full range) bị encode ra `yuv420p` → hình NHẠT đi mà không ai báo

**Bẫy (đo thật, không suy đoán):** file CapCut / điện thoại xuất ra thường là
`pix_fmt=yuvj420p`, `color_range=pc` — tức **full range 0–255**. Bản đầu của `apply.py`
có danh sách `SAFE_PIX` không chứa `yuvj*`, nên nó ép `-pix_fmt yuv420p`. ffmpeg **nén
dải màu 0–255 → 16–235**, rồi vẫn gắn thẻ `-color_range pc` (sai gấp đôi). Kết quả:

| Đo trên `OUT/0822_edit_v4.mp4` (215s, yuvj420p/pc) | Số |
|---|---|
| luma trung bình frame gốc 3874 | **29.90** |
| luma trung bình frame ra 3820 (đúng frame tương ứng) | **41.50** |
| MAE toàn frame (0–255) | **12.25** |
| MAE sau khi bù công thức `out = src*(219/255)+16` | **0.498** |

Tức hình ra **nhạt đi thật**, đen 0 thành 16. Mọi phép kiểm khác (số frame, độ dài,
tương quan chéo, khớp mẫu, peak vùng cắt) đều báo OK.

**Cách làm đúng:** thêm `yuvj420p / yuvj422p / yuvj444p` vào `SAFE_PIX` để giữ nguyên
pix_fmt của nguồn (libx264 nhận yuvj và tự bật cờ full range). Sau khi sửa: luma
29.90 → **29.91**, MAE **0.218** (chỉ còn nhiễu re-encode).

**Và verify phải bắt được:** mục 6b so **mức sáng trung bình + tỉ lệ độ tương phản**
của frame ra với frame gốc tương ứng. Ngưỡng: lệch mức sáng ≤ 2/255, tỉ lệ tương phản
trong 1 ± 0.03. Bản bị nén cho `lech 10.69/255, ti le 0.856` → SAI ngay.

**Hệ quả thứ hai:** phép so khớp frame (mục 6) **phải chuẩn hoá z-score** trước khi so.
Nếu so MAE thô, chuyển tone toàn cục đẩy MAE của **mọi** ứng viên lên ~10–16 và cách
biệt giữa frame đúng và frame sai tụt còn 0.39 — gần như mù. Sau khi z-score: frame đúng
lệch **0.001–0.01**, frame sai lệch **0.02–0.80**.
