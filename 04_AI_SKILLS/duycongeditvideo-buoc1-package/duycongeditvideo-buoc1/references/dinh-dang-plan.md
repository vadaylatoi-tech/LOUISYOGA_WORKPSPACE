# Định dạng plan.json (bước 2 → bước 3)

```json
{
  "source": "D:/du_an/video_dai.mp4",
  "videos": [
    {
      "id": "06",
      "title": "Dòng thảm chuyên sâu khác gì thảm thường",
      "topic": "Mastery: bề mặt PU nhám lì, bám chắc; tập thường thì dòng 5 ly là đủ.",
      "keywords": ["Mastery", "PU", "độ bám", "thấm hút", "5 ly"],
      "segments": [
        {"role": "hook", "start": "00:19:58.900", "end": "00:20:06.700",
         "first": "nếu như mà mọi người", "last": "lên dòng Mastery"},
        {"role": "body", "start": "00:19:26.500", "end": "00:19:58.900",
         "first": "thì cái dòng Mastery", "last": "mọi người nhá"},
        {"role": "end",  "start": "00:20:08.520", "end": "00:20:24.080",
         "first": "nếu mà mọi người tập", "last": "mọi người nhé"}
      ]
    }
  ]
}
```

| Khóa | Bắt buộc | Ý nghĩa |
|---|---|---|
| `source` | không | đường dẫn video gốc; bỏ trống thì lấy từ `source.words.json` |
| `id` | có | 2 chữ số, quyết định tên file `NN - Tiêu đề.mp4` |
| `title` | có | tiêu đề (ký tự `\/:*?"<>|` tự đổi thành `-`) |
| `topic` | nên có | 1–2 câu, đưa vào brief |
| `keywords` | không | từ nên nhấn ở bước edit; brief ghi lần nói đầu tiên |
| `segments` | có | **thứ tự trong mảng = thứ tự dựng** |
| `role` | nên có | `hook` / `body` / `end` |
| `start`, `end` | có | mốc ước lượng theo video gốc (`HH:MM:SS.mmm`, `MM:SS` hoặc số giây); lệch 1–3 s vẫn được (tìm trong ±8 s) |
| `first`, `last` | có | 2–5 chữ đầu / cuối của đoạn, chép từ `source.timeline.txt` (dấu, hoa thường không quan trọng). Chọn cụm đặc trưng, tránh chỉ "mọi người" |

Mẹo:
- Đoạn nằm giữa một dòng phụ đề dài: ước lượng mốc theo tỉ lệ số chữ, script sẽ tự tìm đúng chữ.
- Hai đoạn liền nhau trong video gốc và liền nhau trong video ngắn → gộp thành 1 đoạn (không cắt vô ích).
- `cuts.json` (bước 3 sinh ra) có thể sửa tay `in`/`out` (giây) rồi render lại `--only`.
