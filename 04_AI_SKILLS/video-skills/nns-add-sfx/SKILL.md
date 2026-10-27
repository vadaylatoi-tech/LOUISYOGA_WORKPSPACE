---
name: nns-add-sfx
description: Chèn hiệu ứng âm thanh (SFX) vào video talking-head rồi chuẩn hoá độ to. Input là 1 video CÓ TIẾNG (--video) + nơi lưu kết quả (--out), tuỳ chọn --resources trỏ tới thư mục có sound-effects/ riêng; output là video mới với lớp SFX đã trộn và đã master về -14 LUFS / true peak -1.5 dBTP, luồng HÌNH copy nguyên không mã hoá lại. Mặc định dồn SFX vào HOOK (~20 giây đầu), sau đó chỉ đánh dấu chỗ hình thật sự đổi. Tự đo onset từng file SFX (nhiều file im lặng ở đầu), tự cắt riser để kết thúc đúng đỉnh, và đo lại độ to trên file AAC cuối. Trigger '/nns-add-sfx', hoặc các câu như 'thêm SFX cho video này', 'chèn hiệu ứng âm thanh vào hook', 'video nghe khô quá, thêm whoosh/pop vào', 'chuẩn hoá âm lượng video về -14 LUFS', 'video nhỏ tiếng quá, kéo lên chuẩn TikTok/YouTube'.
---

# nns-add-sfx — chèn SFX + chuẩn hoá loudness

## BƯỚC 0 — BẮT BUỘC, LÀM TRƯỚC MỌI THỨ

Ngay khi skill này được gọi, TRƯỚC KHI làm bất cứ việc gì, chạy:

```
python <skill>/scripts/preflight.py --video "<video>" [--resources "<thư-mục>"]
```

Đọc kết quả:

- Preflight in "ĐẦY ĐỦ" → làm tiếp các bước dưới.
- Preflight in "THIẾU ..." → DỪNG NGAY. Không cắt, không render, không tạo file gì.
  Đưa NGUYÊN khối hướng dẫn mà preflight in ra cho người dùng, rồi HỎI họ:
  "Thiếu \<n\> thứ ở trên. Bạn làm theo hướng dẫn rồi báo tôi, hoặc gửi cho tôi
  \<thứ còn thiếu\> để tôi chạy tiếp?"
  Chờ người dùng trả lời. TUYỆT ĐỐI không tự đoán, không tự thay bằng thứ khác,
  không bỏ qua bước đó để "chạy tạm".

- Nếu người dùng KHÔNG đưa --video: hỏi đường dẫn video thô trước khi làm gì.

## Cần gì để chạy

| Thứ cần | Bắt buộc? | Nếu chưa có thì làm gì (lệnh cụ thể) |
|---|---|---|
| `ffmpeg` + `ffprobe` | Có | `winget install --id Gyan.FFmpeg -e` (macOS: `brew install ffmpeg`; Ubuntu: `sudo apt install ffmpeg`). Phải có **cả hai** file. |
| filter `alimiter`, `ebur128`, `volume` trong ffmpeg | Có | Bản ffmpeg bị cắt bớt bộ lọc → cài bản full (gyan.dev hoặc BtbN). Kiểm: `ffmpeg -filters \| findstr alimiter` |
| `python3` | Có | Tải ở python.org, hoặc dùng miniconda. |
| `numpy` | Có | `pip install numpy` |
| Video đầu vào **có tiếng** | Có | Skill trộn SFX **lên trên** tiếng gốc nên phải có tiếng gốc. Video im lặng: ghép lời nói vào trước bằng `ffmpeg -i silent.mp4 -i voice.wav -c:v copy -c:a aac -b:a 256k -shortest có_tieng.mp4` |
| Thư viện SFX (`.mp3`/`.wav`) | Không | Đã kèm sẵn **9 file** trong `assets/sfx/` → chạy được ngay, **bỏ hẳn `--resources`**. Muốn dùng thư viện riêng: tạo `<thư-mục>/sound-effects/`, copy file `.mp3`/`.wav` vào (tải free ở pixabay.com/sound-effects, freesound.org), rồi gọi `--resources "<thư-mục>"`. |

**Lưu ý về `--resources`:** đưa vào thì phải dùng được. Nếu đường dẫn không tồn
tại, hoặc trong đó không có file `.mp3`/`.wav` nào, thì preflight (và cả
`probe.py` / `plan.py`) **báo THIẾU rồi dừng** — không âm thầm quay về
`assets/sfx/`, vì bạn đã chỉ rõ thư viện muốn dùng. Muốn dùng file kèm sẵn thì
**bỏ hẳn tham số `--resources`**.

**Bước 1 luôn là chạy preflight. Preflight báo THIẾU thì dừng lại, làm theo hướng dẫn
nó in ra, không được chạy tiếp.**

## Chạy 4 bước

Tất cả script nhận `--video`, `--out`, `--resources`, `--dry-run` theo cùng một hợp đồng.
`--resources` là **tuỳ chọn**: bỏ đi thì dùng `assets/sfx/` kèm sẵn trong skill.

```bash
cd <skill>

# 1) Kiểm input + đo độ to hiện tại
python scripts/preflight.py --video "IN.mp4"

# 2) ĐO onset từng file SFX (bắt buộc, có cache — lần 2 gần như tức thì)
python scripts/probe.py --video "IN.mp4" --out sfx_onsets.json

# 3) Lập cue sheet (mặc định dồn vào hook)
python scripts/plan.py  --video "IN.mp4" --out sfx_cues.json --onsets sfx_onsets.json

# 4) Trộn + master (hình được copy nguyên)
python scripts/apply.py --video "IN.mp4" --out OUT.mp4 --cues sfx_cues.json

# 5) ĐO LẠI. Chỉ được báo xong khi bước này exit 0.
python scripts/verify.py --video "IN.mp4" --out OUT.mp4 --cues sfx_cues.json
```

### Cờ hay dùng

| Cờ | Script | Ý nghĩa |
|---|---|---|
| `--hook-len 20` | plan | Độ dài hook. Mặc định: cả video nếu video ≤ 30s, còn lại 20s. |
| `--density 0.8` | plan | Số cue mỗi giây **trong hook**. 0.8 ≈ nhịp đã được duyệt. |
| `--max-t 20` | plan, apply | Chỉ giữ cue trong N giây đầu. Cách nhanh nhất để "chỉ SFX phần hook". |
| `--risers 2` | plan | Số riser đặt trong hook. |
| `--scene 0.35` | plan | Ngưỡng phát hiện cắt cảnh. Hạ xuống 0.25 nếu bỏ sót cut. |
| `--cues my.json` | plan | Cue do bạn tự cho (xem mẫu dưới). Ghi đè toàn bộ phần tự động. |
| `--target -14` | apply, verify | Độ to đích, LUFS. |
| `--tp -1.5` | apply, verify | Trần true peak, dBTP. |
| `--dry-run` | plan, apply | In kế hoạch, kiểm hết cue, **không xuất file**. |
| `--tol 0.5` | verify | Sai số độ to cho phép, LU. |
| `--strict-frames` | verify | Đếm frame bằng cách giải mã hết video (~40s/file). Mặc định đếm gói tin: cùng con số, nhanh hơn 400 lần. |
| `--keep-temp` | apply | Giữ file tạm để xem xét. |

### Tự cho cue chính xác

`plan.py --cues file.json` nhận mảng JSON. Chỉ `t` là bắt buộc; những trường
khác lấy từ bảng onset đã đo (`offset`, `dur`, `align`, `gain_db`, fade).

```json
[
 {"t": 0.00,  "file": "punch.mp3",        "gain_db": -10, "why": "hook mở đầu"},
 {"t": 1.43,  "file": "money.mp3",        "gain_db": -15, "dur": 1.20, "fade_out": 0.40},
 {"t": 17.84, "file": "riser-metallic.mp3", "gain_db": -15, "align": "end"},
 {"t": 19.71, "file": "wrong-answer-buzzer.mp3", "gain_db": -12}
]
```

`align: "end"` nghĩa là **đoạn tiếng kết thúc đúng giây `t`** — dùng cho riser, để
đỉnh của nó đập đúng vào nhịp. `align: "start"` (mặc định) thì tiếng bắt đầu ở `t`.

Bỏ `file` đi thì skill tự chọn theo `role` (`impact`, `transition`, `accent`,
`riser`, `confirm`, `negative`, `bed`).

## 4 quyết định thiết kế, và lý do đo được

1. **Mặc định dồn vào hook.** Creator này đã xem một bản 53 cue rải đều cả video
   rồi tự tay cắt lại chỉ còn ~20 giây đầu. Nên: dày trong hook, sau hook **chỉ**
   đánh dấu chỗ hình thật sự đổi (phát hiện bằng scene detection).
   → `references/hook-weighting.md`
2. **Phải đo onset từng file SFX.** Trên thư viện 86 file của máy này, **35 file**
   có im lặng ở đầu ≥ 0.15s: `mouse-click.mp3` im **1.02s**, `buzzer.mp3` 0.66s,
   `digital-counting-2.mp3` 0.66s, `new-item.wav` 0.65s, `funny.mp3` 0.52s,
   `pop.mp3` 0.23s. Cắt 0.2s từ điểm 0 → **cue im ru**.
   → `references/onset-va-riser.md`
3. **Riser phải cắt để KẾT THÚC đúng đỉnh.** `riser-metallic.mp3` leo tới đỉnh ở
   1.77s rồi tắt. Lấy cả file thì nó lên sớm rồi im trước lúc cần đập.
   → `references/onset-va-riser.md`
4. **Master bằng `volume` + `alimiter`, KHÔNG dùng `loudnorm`.** `loudnorm` âm thầm
   chuyển sang chế độ `dynamic` và nén dải động (đo thật trong project này:
   LRA 5.5 → 3.2 LU). Và `alimiter` bắt buộc `level=disabled`, vì `level=1`
   (mặc định) tự kéo biên độ lên và **undo** giới hạn.
   → `references/loudness-master.md`

## verify.py đo 8 thứ

| Phép đo | Đạt khi |
|---|---|
| cue peak | **mọi** cue có peak > 0 sau khi cắt (peak = 0 là **lỗi cứng**) |
| độ to (I) | trong ±`--tol` (mặc định 0.5) LU so với `--target`, **đo trên file AAC cuối** |
| true peak | ≤ `--tp` |
| LRA | mất ≤ 2.5 LU so với file gốc (mất nhiều = đã bị nén động) |
| hình y nguyên | cùng codec/kích thước/fps, **cùng số frame giải mã**, **cùng md5 gói tin** luồng video |
| dài tiếng == dài hình | lệch ≤ 0.30s |
| khớp tín hiệu | tương quan ≥ 0.90 sau khi chỉnh lệch mẫu (AAC mã hoá lại làm trễ ~239 mẫu) |
| SFX có trong file ra | **lọc khớp**: dựng lại đúng bed SFX đã lên kế hoạch rồi đối chiếu với phần dư. **Mọi** cue phải có biên độ ≥ −10 dB so với kế hoạch và tương quan ≥ 0.10 |

Phép đo cuối được viết lại sau khi **bắt được nó báo sai**: bản cũ chỉ so năng
lượng phần dư với sàn, và nó cho **ĐẠT** một file chỉ master mà **không có một SFX
nào**. Lý do và số đo: `references/cac-bay-da-gap.md` mục 9-BIS. Nếu không tìm
được thư viện SFX để dựng lại mẫu, verify báo `KHONG DO DUOC` + exit 1 (đưa
`--resources` để đo được, hoặc `--skip-residual` nếu **cố ý** bỏ phép đo này).

Chỉ được báo với người dùng là xong khi `verify.py` **exit 0**.

## Số đo thật trên máy này (để đối chiếu)

| Video | Trước | Sau | Vòng dial | Hình |
|---|---|---|---|---|
| `0822_edit_v4.mp4` 215.4s | -14.0 LUFS, LRA 4.2, TP -2.3 | -14.00 LUFS, LRA 4.2, TP -1.8 | 1 | md5 trùng, 6463 frame |
| `footage3/src.mp4` 226.3s (thô) | -17.8 LUFS, LRA 5.5, TP -0.4 | -14.20 LUFS, LRA 4.8, TP -1.9 | 2 | md5 trùng, 6787 frame |
| `clean.mp4` 8.8s | -17.1 LUFS, LRA 1.2 | -14.20 LUFS, LRA 1.2, TP -1.8 | 1 | md5 trùng, 263 frame |

LRA chỉ mất 0.0–0.7 LU. Đó là điểm khác `loudnorm`.

## Đọc thêm

- `references/onset-va-riser.md` — luật đo onset kèm số thật, luật riser, cách bắt file đánh 2 lần
- `references/hook-weighting.md` — vì sao dồn vào hook, cách chọn nhịp, bảng gain theo vai
- `references/loudness-master.md` — `loudnorm` vs `volume`+`alimiter`, AAC vượt true peak, vòng dial gain
- `references/cac-bay-da-gap.md` — mọi cái bẫy đã trả giá, kèm cách tránh
