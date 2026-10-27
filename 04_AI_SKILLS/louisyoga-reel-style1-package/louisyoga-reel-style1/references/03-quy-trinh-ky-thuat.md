# 03 — Quy trình kỹ thuật (lệnh cụ thể)

`<SKILL>` = thư mục skill. `<W>` = thư mục làm việc của video (vd `D:/Video/reel-04/`). Windows dùng được dấu `/`.

```bash
# 0. kiểm máy
python <SKILL>/scripts/preflight.py --video "<raw>.mp4"

# 1. transcript: có hồ sơ thì dùng thẳng "<raw>.hoso.words.json" (KHÔNG chạy transcribe.py); xem khung 1 tấm
python <SKILL>/scripts/contact_sheet.py --video "<raw>.mp4" --out <W>/work/raw_sheet.jpg --every 2

# 2. cắt thô theo mốc từ hồ sơ -> cuts_rough.json [[start,end,"lý do"],...] -> tự kéo mép vào chỗ lặng  -> CỔNG 1
python <SKILL>/scripts/snap_cuts.py --video "<raw>.mp4" --rough <W>/work/cuts_rough.json --out <W>/work/cuts.json --auto-pauses --report <W>/work/cuts_report.md

# 3. cắt (+ khử khối, làm nét nhẹ)
python <SKILL>/scripts/cut_words.py --video "<raw>.mp4" --words "<raw>.hoso.words.json" --cuts <W>/work/cuts.json --out-dir <W>/work
# 3b. tai may nghe lai ban cat: mep nao MAT chu / SOT tieng (giay THO + huong doi) -> sua cuts.json, cat lai, lap toi khi het
python <SKILL>/scripts/check_cuts.py --work <W>/work

# 4. mặt
python <SKILL>/scripts/track.py --video "<raw>.mp4" --out <W>/work/face.track.json --step 0.5

# 5. project + dữ liệu
python <SKILL>/scripts/new_project.py --dest <W>/project --clean <W>/work/clean.mp4 --install
python <SKILL>/scripts/gen_data.py --words <W>/work/clean.words.json --face <W>/work/face.track.json --fixes <W>/work/fixes.json --out <W>/project/src/reel/data.ts
python <SKILL>/scripts/prep_products.py --src "<...>/4. Avatar thảm final" --dest <W>/project/public/img

# 6. dựng: sửa <W>/project/src/reel/Reel.tsx ; kiểm
cd <W>/project && npx tsc --noEmit
python <SKILL>/scripts/stills.py --project <W>/project --out <W>/work/stills_sheet.jpg --times 0.5 1.6 4 9 15 22 30 40

# 7. giọng + đo SFX trước
python <SKILL>/scripts/process_voice.py --in <W>/work/voice_raw.wav --out <W>/work/voice_proc.wav --analyze
python <SKILL>/scripts/measure_sfx.py --reel <W>/project/src/reel/Reel.tsx --voice <W>/work/voice_proc.wav --sfx-dir <W>/project/public/sfx

# 8. render + mix + master
python <SKILL>/scripts/render_all.py --project <W>/project --voice <W>/work/voice_proc.wav --out "<W>/<Ten_Video>_v1.mp4"
# render lai vi ban truoc loi va CHUA giao: them --replace (ban cu -> project/renders/_thay-the/, giu ten chuan); moi render 1 --port rieng
python <SKILL>/scripts/contact_sheet.py --video "<W>/<Ten_Video>_v1.mp4" --out <W>/work/final_sheet.jpg
# (tuỳ chọn, chỉ khi người dùng cho phép chạy Whisper) chép lời bản cuối để chắc không mất chữ
```

## Mốc Whisper nuốt khoảng lặng
Trong hồ sơ, từ đứng trước chỗ ngừng thường bị kéo dài cả khoảng lặng (vd "giáo" 0,9 s) → mốc từ KHÔNG phải ranh giới
âm thật. Luôn cho `snap_cuts.py` kéo mép; mép báo "NGHE LAI" thì nới ra chỗ lặng gần nhất hoặc bỏ cắt đó.

## Cách chọn điểm cắt
- Bỏ: câu nói lặp (giữ lần sau), "ví dụ như là", "chẳng hạn", "các cái", "cái…" kéo dài, ngập ngừng > 0.45 s,
  lặng đầu/cuối. Giữ hơi thở ngắn < 0.3 s.
- Đặt mép cắt vào ký tự `_` hoặc `.` trong hồ sơ âm của `cut_suggestions.md`; nếu cả vùng là `#` thì cắt đúng ranh
  giới từ (fade 12 ms lo việc chống tách).
- Sau cắt luôn đọc caption sinh ra: từ có điểm giữa nằm trong đoạn cắt bị loại khỏi caption dù tiếng còn — thêm lại
  qua `fixes.json` `insert`; từ bị cắt mất một nửa thì nới cuts.

## SEG_ZOOM / PUNCHES / FOCUS
- `SEG_ZOOM` cần ≥ số đoạn (`CUTS.length + 1`); xen kẽ chặt/rộng 1.10–1.30.
- Punch +0.08..+0.14 trên con số/từ khoá; +0.22 ở cú chốt hook.
- `FOCUS [start,end,x,y,zoom]` khi người nói "như thế này này" → trượt camera tới sản phẩm (đo x,y trên khung 1080×1920).

## B-roll
- `assets/broll/louisyoga_brand_film_30fps.mp4` (1920×1080, 92 s, im lặng). Mốc dùng được: `broll-index.md`.
- `cx` = tâm chủ thể theo trục ngang của phim (0–1920); khung dọc lấy 607 px quanh `cx`.
- Ưu tiên cảnh minh hoạ ĐÚNG lời nói; 1.2–3 s mỗi cảnh; 3–5 cảnh/phút.
- Có thể thêm video Louis Yoga khác: đổi sang 30fps `-g 10 -bf 0 -an` rồi để vào `public/broll/`.

## Ảnh
- Ảnh sản phẩm thật của người dùng (avatar web, ảnh chụp sản phẩm) ưu tiên số 1. Assets kèm sẵn ở `assets/brand/`.
- Ảnh web: Wikimedia Commons API (`generator=search` + `extmetadata`) lấy giấy phép + tác giả, ghi credit nhỏ trên ảnh
  và trong báo cáo. Tải vào thư mục riêng, chỉ mở bằng PIL/ffmpeg.

## Bẫy đã gặp
| hiện tượng | cách xử lý |
|---|---|
| Remotion "No frame found at position …" | footage phải mã hoá `-g 10 -bf 0` (cut_words.py đã làm) |
| `remotion still/render` lỗi "not a valid Remotion project" | cổng 3000 đang bị studio khác chiếm → `--port=3123` |
| render_all ghi file vào `<project>/<project>/renders`, mix lỗi IndexError | `--project` tương đối — đã sửa (abspath) |
| 2 render chạy song song cùng cổng | mỗi render một `--port` (3123, 3125…) |
| caption tách "cơ \| bản", "định \| tuyến" | thêm từ ghép vào `COMPOUND` trong gen_data.py |
| faster-whisper `TypeError … metadata_errors` | `pip install "av>=11,<16"` |
| `cublas64_12.dll not found` | không có CUDA libs → transcribe.py tự lùi CPU (chậm hơn ~5×) |
| Python in tiếng Việt lỗi `charmap` | scripts đã ép UTF-8; tự viết script thì `sys.stdout.reconfigure(encoding="utf-8")` |
| caption mất chữ ở mối cắt | thêm qua `fixes.json` `insert` |
| mép snap ăn vào chữ giữ / sót chữ bỏ (mốc Whisper lệch) | `check_cuts.py` chỉ đúng mép + hướng dời; sửa `cuts.json` |
| caption xuống 2 dòng / tách "ảnh \| hưởng" | `gen_data.py` đã giới hạn 21 ký tự + thêm từ ghép; riêng video → fixes `"compound"` / `"lines"` |
| measure_sfx đếm thiếu cue, build_stems "khong biet 'END'" | đã sửa: đọc mọi `const X = <biểu thức số>;` |
| bản render lỗi nằm lại trong 10_FINAL_DELIVERABLES, bản đúng thành `_v2` | `render_all.py --replace` |
| `cublas64_12.dll not found` → Whisper chạy CPU | `transcribe.py` đã tự `add_dll_directory` thư mục nvidia/*/bin |
| ffmpeg 9: `Unrecognized option 'vsync'` | dùng `-fps_mode passthrough` (đã đổi trong mọi script) |
| bar/khối đè lên số | cho thanh dày dần xuống dưới, cố định `marginTop` |
| stamp vàng chìm trên nền sáng | thêm `BottomShade` / `TopShade` |
| lệnh `rm -rf` bị chặn | đừng xoá thư mục; bundle ra thư mục mới |
