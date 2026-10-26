# Nối hồ sơ sang bước 2 (edit) — để edit KHÔNG nghe/xem lại video

## Hồ sơ gồm
| File (cạnh mỗi video ngắn) | Nội dung |
|---|---|
| `NN - Tiêu đề.brief.md` | Hook/thân/kết theo giây, lời thoại đã sửa tên riêng, từ khóa nên nhấn. **Phiên edit đọc file này đầu tiên.** |
| `NN - Tiêu đề.hoso.words.json` | `segments[]` (`start`,`end`,`text`,`text_fixed`,`words[]`) + `words[]` phẳng `{w,start,end,p}`, mốc tính từ 0 của video ngắn; `parts[]` ghi đoạn nào lấy từ giây nào của video gốc; `video_mtime` để phát hiện video bị sửa. |

Hồ sơ hết hiệu lực khi file `.mp4` bị render lại → chạy `finalize.py --only <id>`.

## Theo từng công cụ edit
- **nns-auto-sub / nns-full-pass**: `hoso_tool.py patch-nns --skills "<.claude/skills>"` một lần trên mỗi máy. Sau đó `transcribe.py` tự dùng `<video>.hoso.words.json`; nếu video đã qua `nns-cut-silence` thì đọc `<video>.plan.timemap.json`, lấy hồ sơ của video trước khi cắt và dời mốc (đã đo: lệch trung vị 0 s, 90% chữ < 0,02 s so với nghe lại thật). Log in `dung HO SO co san, KHONG chay Whisper`. Ép nghe lại: `--no-hoso`. Có bản sao lưu `transcribe.py.bak`.
  - Muốn skill đó cũng tự dùng GPU: chạy với `--device cuda --compute-type int8_float16`.
- **Remotion (edit-nns-v1, dự án riêng)**: `hoso_tool.py export --video "<mp4>" --to "<.../transcript_raw.json>"`, rồi bỏ qua bước faster-whisper của quy trình đó.
- **Tự cắt lặng bằng công cụ khác**: có timemap định dạng nns-cut-silence → `hoso_tool.py remap`. Không có → dời mốc theo danh sách đoạn giữ lại (t_mới = t_cũ − tổng thời lượng đã cắt trước nó).
- **CapCut/Premiere (dựng tay)**: dùng `.brief.md` làm kịch bản, `text_fixed` làm phụ đề.

## CLAUDE.md cho dự án edit
Chép `assets/CLAUDE.md.mau` vào thư mục gốc của dự án edit thành `CLAUDE.md` và sửa đường dẫn thư mục video. Phiên chat mới mở ở thư mục đó sẽ tự đọc và biết không nghe lại video.

## Câu mở đầu phiên edit (đưa cho người dùng)
> Các video trong thư mục "<thư mục video ngắn>" đã có hồ sơ dựng sẵn: mỗi video có .brief.md và .hoso.words.json. Em chỉ đọc .brief.md của video cần edit, dùng .hoso.words.json làm transcript. KHÔNG chạy Whisper, KHÔNG xem/nghe lại video. Giờ em edit video "<tên>" theo phong cách <tên skill / video mẫu>.
