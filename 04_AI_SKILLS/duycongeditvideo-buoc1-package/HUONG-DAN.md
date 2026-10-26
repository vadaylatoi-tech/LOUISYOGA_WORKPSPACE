# Duycongeditvideo_Buoc1 — Hướng dẫn cài & dùng

**Bước 1 của quy trình dựng video:** từ 1 video dài, bộ skill lọc nội dung thành nhiều video ngắn. Mỗi video mở bằng hook và kết trọn vấn đề, được cắt ghép không mất chữ. Bộ skill cũng làm sẵn **hồ sơ dựng** cạnh mỗi video, để bước edit sau không phải nghe hay xem lại video.

## Trong thư mục này có gì
| Mục | Là gì |
|---|---|
| `duycongeditvideo-buoc1/` | Bộ skill: `SKILL.md`, `scripts/`, `references/`, `assets/` |
| `CAI-DAT-WINDOWS.bat` | Nháy đúp để cài trên Windows |
| `cai-dat-mac-linux.sh` | Chạy `sh cai-dat-mac-linux.sh` để cài trên macOS/Linux |
| `Duycongeditvideo_Buoc1.zip` | Bản nén của cả thư mục, để mang sang máy khác |

## Cài trên máy mới hoặc tài khoản mới
1. Chép file `Duycongeditvideo_Buoc1.zip` sang máy kia (USB, Google Drive…) rồi giải nén.
2. Windows: nháy đúp `CAI-DAT-WINDOWS.bat`. macOS/Linux: chạy `sh cai-dat-mac-linux.sh`.
   - Script chép skill vào `~/.claude/skills/duycongeditvideo-buoc1`, nên **mọi dự án** trên máy đó đều dùng được.
   - Script tự cài `faster-whisper` và `numpy`, sau đó kiểm tra máy.
3. Nếu máy báo thiếu thì cài theo gợi ý:
   - ffmpeg: Windows `winget install Gyan.FFmpeg`, macOS `brew install ffmpeg`.
   - Có card NVIDIA thì cài thêm: `pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"`.
4. Lần đầu chạy, máy sẽ tự tải model Whisper large-v3 (khoảng 3 GB), nên cần có mạng.
5. Mở lại Claude Code. Gõ `/` sẽ thấy skill `duycongeditvideo-buoc1`.

Muốn chỉ dùng cho một dự án thì chép thư mục `duycongeditvideo-buoc1` vào `<dự án>/.claude/skills/` thay vì chạy file cài.

Trên Claude.ai (web/app), vào **Settings → Capabilities → Skills**, tải lên file zip chỉ chứa thư mục `duycongeditvideo-buoc1`. Lưu ý trên web không có GPU và ffmpeg của máy anh, nên quy trình cắt ghép đầy đủ nên chạy bằng Claude Code trên máy.

## Prompt bắt đầu (dán vào phiên chat mới)

**Làm trọn bộ từ video dài:**
```text
/duycongeditvideo-buoc1
Video dài: "D:\...\ten_video.mp4"
Thư mục dự án (lưu transcript, phương án): "D:\...\Du an ABC"
Thư mục xuất video ngắn: "D:\...\Du an ABC\Video ngan"
Chủ đề/sản phẩm: <vd: thảm và phụ kiện yoga Louis Yoga>
Yêu cầu: lọc thành nhiều video ngắn, mỗi video 1 chủ đề, mở bằng hook, kết trọn vấn đề, khoảng 50–90 giây (đủ ý quan trọng hơn). Ưu tiên hướng dẫn chọn sản phẩm, so sánh, giải đáp thắc mắc, lỗi thường gặp. Không đưa giá/voucher. Không chỉnh màu.
Trước tiên đưa anh danh sách video để duyệt, anh duyệt xong mới cắt.
```

**Đã có file phụ đề sẵn:** thêm dòng
```text
Phụ đề có timeline: "D:\...\phu_de.txt" (dùng để đọc nội dung; vẫn chạy nhận dạng từng chữ để cắt chính xác)
```

**Đã duyệt danh sách, cho cắt luôn:**
```text
Oke anh duyệt. Em cắt ghép tất cả theo plan, kiểm tra không mất chữ, rồi làm hồ sơ dựng cho từng video.
```

**Chỉ làm lại vài video:**
```text
/duycongeditvideo-buoc1 — dự án "D:\...\Du an ABC": sửa video 03 và 07 (lý do: ...), cắt lại và cập nhật hồ sơ cho 2 video này.
```

**Sang bước edit (phiên chat khác):**
```text
Các video trong thư mục "D:\...\Video ngan" đã có hồ sơ dựng sẵn: mỗi video có .brief.md và .hoso.words.json. Em chỉ đọc .brief.md của video cần edit, dùng .hoso.words.json làm transcript. KHÔNG chạy Whisper, KHÔNG xem/nghe lại video. Giờ em edit video "<tên>" theo phong cách <tên skill / video mẫu>.
```

## Quy trình skill tự chạy
0. `preflight.py`: kiểm tra máy.
1. `transcribe_source.py`: nghe video dài **1 lần**, ra transcript từng chữ và phụ đề có timeline.
2. Claude lập phương án theo `references/quy-tac-noi-dung.md`, ra `phuong-an.md` (anh đọc và duyệt) và `plan.json`.
3. `refine_cuts.py`: tính điểm cắt rơi vào khoảng lặng, báo những chỗ người nói nói liền không có chỗ ngắt.
4. `render.py`: cắt ghép, giữ màu gốc (chỉ chỉnh màu khi anh yêu cầu, dùng `--grade`).
5. `finalize.py`: nghe lại đầu, cuối và mối nối để bắt mất chữ, đồng thời tạo `.hoso.words.json` và `.brief.md`.
6. Bàn giao: `CLAUDE.md` cho dự án edit, `hoso_tool.py` (patch-nns / export / remap).
