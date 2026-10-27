# Quy trình edit nhanh — DÙNG HỒ SƠ, KHÔNG NGHE LẠI VIDEO

## Video đã có hồ sơ thì KHÔNG chạy Whisper, KHÔNG xem lại toàn bộ video

Cạnh mỗi video đã cắt trong `11_COMPLETED_PROJECTS/2026-10_reels-chon-tham-dot1/cuts/` (17 video, đợt 1) và `05_VIDEO_PROJECTS/2026-10_san-sale/cuts/` (12 video, buổi live "Săn sale cùng Louis Yoga"; dự án/cuts ở `05_VIDEO_PROJECTS/2026-10_san-sale/plan/`) có 2 file hồ sơ, làm sẵn một lần:

| File | Nội dung | Dùng để |
|---|---|---|
| `NN - tên.brief.md` | Tóm tắt: hook / thân / kết theo giây, toàn văn lời thoại đã sửa tên riêng, từ khóa nên nhấn | **Đọc file này đầu tiên** — đủ để hiểu video, không cần xem/nghe lại |
| `NN - tên.hoso.words.json` | Transcript word-level (faster-whisper large-v3) của **chính video ngắn**, mốc tính từ 0 | Sub karaoke, cắt từ đệm, đặt SFX/thẻ chữ/logo theo từ |

Định dạng `hoso.words.json`: `segments[]` (mỗi câu có `start`, `end`, `text`, `text_fixed`, `words[]`) và `words[]` phẳng, mỗi từ `{w, start, end, p}`. Ngoài ra có `parts[]` (đoạn nào ghép từ giây nào của video gốc) và `video_mtime`.

### Cách dùng theo từng skill

- **nns-auto-sub / nns-full-pass**: cứ chạy bình thường. `transcribe.py` đã được sửa để tự tìm `<video>.hoso.words.json`; nếu video đã qua `nns-cut-silence` thì nó tự đổi mốc theo `<video>.cut.plan.timemap.json`. Log sẽ in `dung HO SO co san, KHONG chay Whisper`. Muốn ép nghe lại: `--no-hoso`.
- **edit-nns-v1 / louis-yoga-remotion (Remotion)**: KHÔNG chạy đoạn faster-whisper trong skill. Ghi `segments` của hồ sơ ra làm `transcript_raw.json` (cùng định dạng `[{..., "words": [{w,start,end}]}]`), rồi đi tiếp các bước cắt từ đệm / remap / timeline như bình thường. Nếu tự cắt thêm khoảng lặng thì remap mốc theo timemap, không nhận dạng lại.
- Chỉ đo thêm thứ hồ sơ không có (ví dụ vị trí mặt, khung hình để đặt chữ) — trích vài frame, không xem hết video.

### Khi nào hồ sơ KHÔNG còn dùng được
- Video `.mp4` bị sửa/render lại sau khi làm hồ sơ (`video_mtime` không khớp) → script tự bỏ qua hồ sơ. Tạo lại hồ sơ cho riêng video đó.
- Video mới chưa có hồ sơ → chạy Whisper như thường (đã bật GPU, xem dưới).

## Whisper trên máy này
- GPU GTX 1660 Super chạy được sau khi cài `nvidia-cublas-cu12` + `nvidia-cudnn-cu12` (pip). Trên Windows phải thêm `site-packages/nvidia/{cublas,cudnn,cuda_nvrtc}/bin` vào đường tìm DLL (`os.add_dll_directory`) trước khi nạp model — `transcribe.py` đã tự làm.
- Dùng `device="cuda", compute_type="int8_float16"` (nhanh hơn `float16` ~2 lần trên card này). ~30 giây cho 1 video 60–90 giây.

## Quy tắc nội dung video ngắn (người dùng đã duyệt)
- Mở bằng **hook**, kết bằng **câu chốt trọn vấn đề**; không để mất chữ đầu/cuối câu.
- Không chỉnh màu nếu không được yêu cầu.
- Tên riêng hay bị nhận sai: Asana (Asena/Ascena), Moon (mút), Queen (Quin), Basic Gen (Basic Den/Gem/Gel), TPE (TP/tê bê), Mastery, thảm (thạm/tạm/hạm), bong tróc (bong chóc), giỏ hàng (dọa hàng), thương hiệu Louis Yoga (Lushoga/Louis Soga/Richoga).

## Đường dẫn trong LOUGA WORKSPACE (thêm khi chuyển máy, 2026-10-26)
- Thư viện dùng chung: `03_MEDIA_LIBRARY/shared-sources/`. Skill `nns-*` không còn tự tìm thấy thư mục này (nó không còn là thư mục cha) → luôn truyền `--resources "<workspace>/03_MEDIA_LIBRARY/shared-sources"`.
- Media (mp4, ảnh, work/, cả `cuts/` + hồ sơ) ĐỌC THẲNG từ Google Drive `G:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA/<cùng đường dẫn>` (Drive đã bật offline nên file có sẵn trên máy). KHÔNG chép media về D: — bản chép sẽ lệch khi Drive được sửa. D: chỉ giữ repo, asset skill (dong_bo.py tự đồng bộ) và project Remotion có node_modules.
- Đường dẫn cũ còn trong memory/báo cáo cũ: tra `00_SYSTEM/claude-memory/PATH_MAP.md`.

## NƠI LƯU VIDEO FINAL — BẮT BUỘC (chủ thương hiệu chốt 26/10/2026)
- Video final (bản giao, mọi skill edit) → Google Drive `LOUGA_WORKSPACE_MEDIA/10_FINAL_DELIVERABLES/<YYYY-MM-DD>_<mã-dự-án>/<NN - tên video>.mp4`.
  - Ngày = ngày edit (vd hôm nay edit thì là ngày hôm nay); `<mã-dự-án>` = phần sau tháng của thư mục dự án (vd `2026-10_san-sale` → `san-sale`).
  - Tên file = đúng tên video trong `cuts/`; bản sửa sau → `_v2`, `_v3` cùng thư mục, không ghi đè.
  - Ví dụ: `10_FINAL_DELIVERABLES/2026-10-26_san-sale/01 - Lau thảm bằng cồn có sao không.mp4`, `10_FINAL_DELIVERABLES/2026-10-26_reels-chon-tham-17/`.
  - Thư mục này CHỈ chứa video final. KHÔNG để video final trong `05_VIDEO_PROJECTS/` hay `11_COMPLETED_PROJECTS/`.
- Hồ sơ làm việc (work/, BAO-CAO, contact sheet) → Drive `05_VIDEO_PROJECTS/<dự án>/edit/<NN-ten-video>/`.
- Project Remotion (node_modules) → ổ máy `D:/LOUGA_WORKSPACE/05_VIDEO_PROJECTS/<dự án>/edit-<NN-ten-video>/project` (Drive không cài được node_modules).

## ĐỒNG BỘ GIỮA CÁC MÁY + NHẬT KÝ — BẮT BUỘC (từ 26/10/2026)
- GitHub giữ code/skill/quy tắc; Google Drive giữ media, asset skill và **nhật ký làm việc** `LOUGA_WORKSPACE_MEDIA/00_SYSTEM/NHAT-KY-LAM-VIEC.md`.
- Đầu phiên: hook SessionStart tự chạy `00_SYSTEM/sync/dong_bo.py session-start` (git pull, đồng bộ asset skill với Drive, in 3 mục nhật ký cuối). Không thấy khối "DONG BO WORKSPACE" ở đầu phiên → chạy tay lệnh đó, rồi đọc nhật ký trước khi làm.
- Skill `louisyoga-reel-style1`, `duycongeditvideo-buoc1` trong `~/.claude/skills/` là LIÊN KẾT tới `04_AI_SKILLS/...` của repo — sửa skill là sửa trong repo. Asset nặng (mp3/mp4/onnx/ảnh) không lên git, nằm ở Drive cùng đường dẫn `04_AI_SKILLS/...`; thêm asset mới → script tự đẩy lên Drive ở phiên sau.
- Xong việc (trước khi báo hoàn thành): ghi nhật ký
  `python D:/LOUGA_WORKSPACE/00_SYSTEM/sync/dong_bo.py ghi-nhat-ky --viec "..." --file "<đường dẫn final/hồ sơ>" --con-lai "..."`
- Có sửa skill/quy tắc/script trong repo → commit + push lên GitHub ngay trong phiên (máy chưa cấu hình git user thì dùng tác giả của commit trước, `git -c user.name=... -c user.email=...`).
- Máy mới: cài Google Drive for desktop + Git + Python, `git clone https://github.com/vadaylatoi-tech/LOUISYOGA_WORKPSPACE D:/LOUGA_WORKSPACE`, chạy `00_SYSTEM/setup/CAI-DONG-BO.bat`, mở lại Claude Code.
