---
name: duycongeditvideo-buoc1
description: "Duycongeditvideo_Buoc1 — BƯỚC 1 của quy trình dựng video: từ MỘT video dài (livestream, buổi tư vấn, podcast tiếng Việt) lọc nội dung thành NHIỀU video ngắn, mỗi video một chủ đề, mở bằng hook và kết trọn vấn đề; cắt ghép frame-exact không mất chữ, rồi tạo HỒ SƠ DỰNG (transcript từng chữ + brief) cạnh mỗi video để bước edit sau KHÔNG phải nghe/xem lại. Dùng khi người dùng gọi '/duycongeditvideo-buoc1', 'Duycongeditvideo_Buoc1', hoặc nói 'lọc video dài này thành nhiều video ngắn', 'cắt ghép livestream thành clip', 'chọn nội dung rồi cắt thành reels/shorts', 'làm hồ sơ để edit hàng loạt'. KHÔNG làm sub/SFX/hiệu ứng — đó là bước 2 (edit)."
---

# Duycongeditvideo_Buoc1 — Lọc nội dung, cắt ghép, làm hồ sơ dựng

Đầu vào: 1 video dài có lời nói tiếng Việt. Đầu ra:
- Thư mục video ngắn `NN - Tiêu đề.mp4` (giữ nguyên độ phân giải, fps, **giữ màu gốc**).
- Cạnh mỗi video: `.hoso.words.json` (transcript từng chữ của chính video ngắn) + `.brief.md` (hook/thân/kết theo giây).
- Thư mục dự án (`--work`): transcript video gốc, phương án dựng, danh sách điểm cắt, báo cáo kiểm tra.

Mọi script nằm trong `scripts/` của skill này (gọi bằng đường dẫn tuyệt đối tới thư mục skill). Chạy được trên Windows/macOS/Linux; tự dùng GPU NVIDIA nếu có, không thì CPU.

## Quy trình (làm đúng thứ tự)

### Bước 0 — Kiểm máy (lần đầu trên máy mới)
```bash
python "<skill>/scripts/preflight.py" --gpu
```
Thiếu gì nó in lệnh cài. Có card NVIDIA mà báo thiếu cuBLAS → `pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"` (nhanh hơn CPU 5–10 lần). Xem `references/cai-dat.md`.

### Bước 1 — Nhận dạng video gốc MỘT lần
```bash
python "<skill>/scripts/transcribe_source.py" --video "<video dài>" --work "<thư mục dự án>"
```
Ra `source.words.json` (từng chữ, dùng cho mọi bước sau) + `source.timeline.txt` (phụ đề có mốc, để đọc). Có cache — chạy lại không nghe lại.
Nếu người dùng đã đưa sẵn file phụ đề có timeline: vẫn chạy bước này (cần mốc **từng chữ** cho bước 3 và 5), nhưng dùng file của họ để đọc nội dung nếu muốn.

### Bước 2 — Lập phương án (Claude làm, KHÔNG có script)
Đọc `source.timeline.txt`, theo **đúng các quy tắc trong `references/quy-tac-noi-dung.md`** (bắt buộc đọc). Viết 2 file vào thư mục dự án:
1. `phuong-an.md` — cho người dùng đọc: danh sách video (tiêu đề, chủ đề, tổng thời lượng ước tính), rồi bảng dựng từng video (đoạn nguồn theo thứ tự dựng, mốc vào–ra, câu đầu/câu cuối, lời thoại, gợi ý chữ trên màn hình, chỗ cần nghe lại).
2. `plan.json` — cho máy: định dạng ở `references/dinh-dang-plan.md` (ví dụ `assets/plan.example.json`).
Kèm `terms.json` (sửa tên riêng Whisper hay nghe sai) — chép `assets/terms.example.json` rồi sửa theo sản phẩm của video.

**Dừng lại, đưa danh sách video cho người dùng duyệt** trước khi cắt — trừ khi họ đã bảo làm luôn.

### Bước 3 — Tính điểm cắt chính xác
```bash
python "<skill>/scripts/refine_cuts.py" --work "<thư mục dự án>"
```
Tìm câu đầu/cuối trong transcript từng chữ, đo năng lượng âm thanh 10 ms để đặt điểm cắt vào khoảng lặng. Ra `cuts.json` + `refine_report.md`. **Đọc báo cáo**:
- `NOMATCH` → `first`/`last` trong plan chép sai; sửa theo ngữ cảnh in trong báo cáo rồi chạy lại.
- `TIGHT` → người nói nói liền, không có chỗ lặng. Ưu tiên dời điểm vào/ra sang **ranh giới câu kế bên** (chấp nhận thêm vài chữ nối như "Bởi vì là", "Tại vì", "Đây là") hơn là cắt giữa dòng chữ. Sửa `first`/`last` + mốc rồi chạy lại `--only <id>`.
- Với livestream dài, transcript gốc hay **lệch mốc vài giây quanh chỗ ngừng** (chữ "Vệ" ở 38:25 trong khi câu nói ở 38:36…), nên báo cáo có thể nhiều cờ. Cách nhanh nhất: nghe lại đúng khung bị cờ bằng
  `python "<skill>/scripts/listen.py" --video "<video gốc>" --at 1094.4-1095.9 --at ...` rồi sửa thẳng `in`/`out` (giây) trong `cuts.json`, cập nhật `first_heard`/`last_heard` theo chữ thật của đoạn (để bước 5 so đúng). Cặp đoạn liền nhau trong video gốc thì gộp thành 1.

### Bước 4 — Cắt ghép
```bash
python "<skill>/scripts/render.py" --work "<thư mục dự án>" --out "<thư mục video ngắn>"
```
Mặc định **không chỉnh màu**. Chỉ thêm `--grade` khi người dùng yêu cầu chỉnh màu. `--only 06,07` để làm lại vài video.

### Bước 5 — Nghe lại + tạo hồ sơ dựng (1 lần cho cả 2 việc)
```bash
python "<skill>/scripts/finalize.py" --work "<thư mục dự án>" --out "<thư mục video ngắn>"
```
Ra `.hoso.words.json` + `.brief.md` cạnh mỗi video, và `verify_report.md`. Có `CANH BAO` → mở báo cáo xem chữ nghe được ở ranh giới; mất chữ thì lùi/tiến điểm cắt trong `cuts.json` (hoặc sửa plan → bước 3), render lại `--only`, chạy lại finalize `--only` (báo cáo các video khác được giữ nguyên).
Nhiều CANH BAO là **báo nhầm**: Whisper nghe khung 4 s hay sai chữ ("Dòng"→"Rồi") hoặc bịa câu ("Hãy subscribe cho kênh…"). Trước khi sửa, kiểm lại bằng `listen.py` trên **video ngắn** ở giây đó; chỉ sửa khi chữ thật sự mất (ví dụ đã gặp: thiếu "sao" trong "Bởi vì sao?" vì Whisper đặt chữ cuối sớm 0,4 s).

### Bước 6 — Bàn giao cho bước edit
- Chép `assets/CLAUDE.md.mau` thành `CLAUDE.md` ở thư mục gốc dự án edit (sửa đường dẫn), để phiên chat mới tự biết dùng hồ sơ, không nghe lại.
- Máy có skill `nns-auto-sub`/`nns-full-pass`: `python "<skill>/scripts/hoso_tool.py" patch-nns --skills "<.claude/skills>"` — sau đó các skill đó tự dùng hồ sơ (kể cả sau khi cắt lặng, qua timemap).
- Dự án Remotion: `hoso_tool.py export --video <mp4> --to <transcript_raw.json>`.
- Báo người dùng: danh sách video + thời lượng, chỗ nào chưa gọn (chữ nối đầu câu, video dài hơn dự kiến), nơi lưu. Chi tiết: `references/noi-buoc-edit.md`.

## Những lỗi đã gặp — đừng lặp lại
- **Mốc trong phụ đề dòng ~6 s chỉ là gợi ý**; luôn để `refine_cuts.py` tính trên transcript từng chữ của large-v3. Model `small` nghe sai nhiều, không dùng để định vị.
- **Chữ nói nhỏ ở đầu đoạn bị coi là im lặng** (từng mất chữ "Queen"). `first` trong plan phải là đúng chữ đầu tiên muốn giữ; verify sẽ bắt lỗi này.
- Mở đầu/kết thúc video phải **trọn ý**: hook là câu gây chú ý nhất (có thể lấy từ cuối video gốc đưa lên đầu), câu cuối phải trả lời vấn đề đặt ra — không kết bằng câu lửng hay chuyển ý.
- Không cộng khoảng bị bỏ giữa các đoạn vào thời lượng. Thời lượng mục tiêu 50–90 s nhưng **đủ ý quan trọng hơn** — dài/ngắn hơn chút được.
- Không đưa giá, voucher, % giảm, quà tặng theo phiên live vào video (hết hạn nhanh) trừ khi người dùng muốn.
- Console Windows: scripts tự ép UTF-8; nếu tự viết python thêm thì set `PYTHONIOENCODING=utf-8` và mở file với `encoding="utf-8"`.
- Chạy nhận dạng dài nên chạy nền và lưu kết quả từng phần; đừng để lỗi ở bước ghi file làm mất cả lượt chạy.
