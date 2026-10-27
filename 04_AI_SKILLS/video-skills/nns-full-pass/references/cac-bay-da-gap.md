# Các bẫy đã gặp

Mỗi mục dưới đây là một chỗ đã trả giá thật trong project này. Skill đã cài sẵn
cách tránh, nhưng cần biết để không gỡ nhầm.

## 1. Đường dẫn Windows trong chuỗi filter

Filter `subtitles=` của ffmpeg đọc dấu `:` của ổ đĩa Windows (`C:\...`) là dấu
phân cách option. Nhét đường dẫn tuyệt đối vào là lỗi cú pháp, hoặc tệ hơn:
chạy được nhưng không vẽ gì.

**Cách đúng:** copy font + `.ass` vào thư mục tạm rồi chạy ffmpeg với `cwd` ở
đó, filter chỉ dùng **tên file tương đối**.

```python
shutil.copy2(font, os.path.join(tmp, "fonts", name))
shutil.copy2(ass,  os.path.join(tmp, "sub.ass"))
cmd = [..., "-vf", "subtitles=sub.ass:fontsdir=fonts", ...]
subprocess.run(cmd, cwd=tmp)
```

`burn.py` của `nns-auto-sub` đã làm sẵn. Đừng "đơn giản hoá" nó thành đường dẫn
tuyệt đối.

## 2. `-ss` để trích frame

`-ss` nhảy tới **keyframe gần nhất**. Frame lấy ra không phải frame bạn muốn —
lệch tới nửa giây, đủ để kết luận sai về bố cục hoặc bảo "sub không hiện" trong
khi nó hiện ở frame bên cạnh.

**Cách đúng:** `select=eq(n\,N)` + `-vsync 0`.

```bash
ffmpeg -v error -y -i v.mp4 -vf "select=eq(n\,120)" -vsync 0 -frames:v 1 thu.png
```

Lấy nhiều frame một lượt: `select='eq(n\,10)+eq(n\,50)+eq(n\,90)'` — chỉ giải mã
một lần.

## 3. concat demuxer

concat demuxer **tụt fps về 25** và làm lệch mọi mốc giây. Đã dính một lần.

**Cách đúng:** concat **filter** + `-r <fps gốc>`.

## 4. `alimiter` với `level=1`

`level=1` (mặc định) tự kéo biên độ lên sau khi giới hạn — tức là **undo** đúng
phần limiting vừa làm. Luôn dùng `level=disabled`. Xem `loudness.md`.

## 5. `loudnorm` âm thầm chuyển sang `dynamic`

Không có `linear=true` thì `loudnorm` nén dải động mà không báo gì. Đo thật:
LRA **5.5 → 3.2 LU**. Xem `loudness.md`.

## 6. `volumedetect` giấu lỗi clip

Nó clamp giá trị, nên file đã clip vẫn báo `max_volume: 0.0 dB`.

**Cách đúng:** giải mã file mp4 cuối ra f32 rồi lấy đỉnh thật và đếm số mẫu
`> 1.0`.

## 7. File SFX im lặng ở đầu

35/86 file trong thư viện của máy này có ≥ 0.15s im lặng ở đầu, cao nhất
`mouse-click.mp3` **1.02s**. Cắt 0.2s từ điểm 0 → cue im ru. Phải **đo onset
từng file**. Xem `cue-sheet-va-mat-do-sfx.md`.

## 8. Riser lấy cả file

`riser-metallic.mp3` leo tới đỉnh ở 1.77s rồi tắt. Lấy cả file thì nó lên sớm
rồi im trước lúc cần đập. Phải lấy **đoạn giữa** sao cho đỉnh rơi đúng mốc.

## 9. Đo SFX bằng phép trừ `final − source×gain`

**Không dùng cách này.** Nguồn là AAC, bản cuối là AAC khác, cộng thêm
`alimiter` có lookahead ~5ms → phép trừ đó sinh ra dư **rất lớn** (đo thật: nền
dư 0.10, **to hơn cả lớp SFX**). Mọi kết luận rút ra đều vô nghĩa.

**Cách đúng:** chạy **ĐÚNG chuỗi filter hai lần** — một lần với lớp SFX thật,
một lần với lớp SFX **im lặng** — rồi trừ hai bản. Hiệu là đúng phần SFX đóng
góp, không dính một chút nhiễu codec nào.

`master.py` ghi lại chuỗi filter vào `<gốc>.ab.json` và giữ `voice.raw` /
`bed.raw` trong `<gốc>.work/` chính vì phép đo này. Xoá thư mục `.work/` thì
verify bước 5 không chạy được.

Bản kiểm cũ (so năng lượng phần dư với sàn) đã từng báo **ĐẠT** cho một file chỉ
master mà **không có một SFX nào**.

## 10. Dòng `Dialogue` thừa dấu phẩy

Phải có **đúng 8 dấu phẩy** trước `Text`. Thừa một cái → chữ hiện ra có dấu `,`
dính ở đầu. Xem `lop-the-chu-ass.md`.

## 11. Bản vẽ `\p1` với toạ độ âm + `\an5`

libass canh bản vẽ theo **bounding box của chính nó**, không theo gốc toạ độ.
Khung sẽ lệch hẳn khỏi chữ. Phải vẽ từ (0,0), neo `\an7`, toạ độ tính sẵn.

## 12. Thẻ có khung mà dùng pop-scale

Khung neo `\an7`, chữ neo `\an2` → scale hai cái lệch nhau, nhìn thấy rõ chữ
trượt ra khỏi khung. Thẻ có khung dùng **trượt + fade**.

## 13. Font thiếu glyph — libass không báo lỗi

Nó vẽ ra **khoảng trống**, exit 0. `BeVietnamPro-ExtraBold.ttf` **không có**
`→ ✓ ✗`. Phép kiểm đúng là `getmask(ch).size[1] == 0`, không phải so với
`getmask("")`. Xem `lop-the-chu-ass.md`.

## 14. Thiếu dấu chấm cuối câu

Whisper hay bỏ quên dấu chấm ở từ cuối cùng và ở chỗ nghỉ dài. `build_ass.py`
tách cụm theo `END_PUNCT` nên thiếu nó thì cụm cuối dính vào cụm trước, và
`plan_cues.py` mất hết mốc đầu câu để neo cue.

`punct.py` chạy **trước** khi gom cụm. Và nhớ: **biên câu là biên MỞ** — câu mới
bắt đầu từ từ NGAY SAU dấu chấm.

## 15. Sub hiện dấu phẩy

Sub karaoke chạy từng từ, dấu phẩy lơ lửng giữa khung trông rất bẩn và còn làm
tách dòng sai chỗ. `punct.py` bỏ dấu phẩy mặc định; giữ lại bằng `--keep-commas`.

## 16. Chữ tụt xuống vùng UI nền tảng

Đáy khung ~330px (với khung 1920) bị UI TikTok/Facebook che. Chữ vẫn được vẽ,
verify pixel vẫn đạt, nhưng người xem trên điện thoại không đọc được.

**Bí quá thì đẩy chữ LÊN, đừng bao giờ đẩy xuống.** Xem
`vung-an-toan-va-do-bo-cuc.md`.

## 17. Ước dải thẻ bằng công thức tay

Thẻ 2 dòng bị tính thành 1 dòng (~60px), và khung to hơn khối chữ ~60px mỗi
phía. Phải tính từ **số đo thật**: gọi thẳng `cards_to_ass.fit()` và
`plate_box()`.

## 18. Tin log ffmpeg thay vì đo pixel

libass có thể chạy **exit 0 mà không vẽ chữ nào**, hoặc lặng lẽ vẽ bằng font hệ
thống thay vì font của bạn. Luôn đo pixel: so frame ra với frame vào, đếm pixel
khác nhau **bên trong dải chữ**.

## 19. Sửa vỡ skill cũ

`nns-full-pass` **gọi lại** script của các skill anh em, không copy cũng không
sửa chúng. Chúng vẫn phải chạy độc lập được.

Chỗ nào script cũ chưa đủ thì viết script mới **trong skill này**:

| Thiếu gì ở bản cũ | Script mới trong skill này |
|---|---|
| `build_sfx_json.py` ghim cứng đường dẫn thư viện SFX | `build_sfx.py` — đổi `B.LIB` lúc chạy, không sửa file gốc |
| `cards_to_ass.missing_glyphs` không bắt được glyph thiếu | `check_cards.py` — guard đúng, chạy **trước** ở bước 6b |
| `verify_cards.py` ghim cứng 1080×1920 | `verify_all.py` — nhận w×h thật |
| Không có bước đo bố cục tự động | `layout.py` |
| Không có bước dấu câu | `punct.py` |
