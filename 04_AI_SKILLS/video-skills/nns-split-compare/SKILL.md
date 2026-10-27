---
name: nns-split-compare
description: Dựng video SO SÁNH chia đôi màn hình "trước/sau" cho video talking-head — bên trái là bản THÔ, bên phải là bản AI đã cắt, kèm nhãn BẢN GỐC / AI ĐÃ CẮT, badge VS, badge ✦ AI và pill thời lượng đo thật. Hai bên KHÔNG chạy song song mà chạy TUẦN TỰ - pha 1 bên trái chạy (bên phải đứng hình, làm tối), pha 2 bên phải chạy (bên trái đứng hình, làm tối) - nên người xem nghe rõ từng bản và thấy ngay bản AI ngắn hơn bao nhiêu. Chỉ cần truyền 1 file thô (--video), skill tự cắt khoảng lặng bằng nns-cut-silence; đã có sẵn bản cắt thì truyền thêm --right. Output 1080x1920 30fps. Dựng thuần ffmpeg + Pillow, không cần Remotion/HyperFrames/trình duyệt. Trigger '/nns-split-compare', hoặc các câu như 'so sánh video thô với video AI đã cắt', 'làm video chia đôi trước sau', 'video before/after cho reel', 'khoe AI cắt được bao nhiêu giây'.
---

# nns-split-compare — video so sánh chia đôi (thô vs AI đã cắt)

## BƯỚC 0 — BẮT BUỘC, LÀM TRƯỚC MỌI THỨ

Ngay khi skill này được gọi, TRƯỚC KHI làm bất cứ việc gì, chạy:

```
python <skill>/scripts/preflight.py --video "<video-thô>"
```

Đọc kết quả:

- Preflight in "DAY DU" → làm tiếp các bước dưới.
- Preflight in "THIEU ..." → DỪNG NGAY. Không cắt, không vẽ, không render, không tạo file gì.
  Đưa NGUYÊN khối hướng dẫn mà preflight in ra cho người dùng, rồi HỎI họ:
  "Thiếu \<n\> thứ ở trên. Bạn làm theo hướng dẫn rồi báo tôi, hoặc gửi cho tôi
  \<thứ còn thiếu\> để tôi chạy tiếp?"
  Chờ người dùng trả lời. TUYỆT ĐỐI không tự đoán, không tự thay bằng thứ khác,
  không bỏ qua bước đó để "chạy tạm".

- Nếu người dùng KHÔNG đưa `--video`: hỏi đường dẫn video thô trước khi làm gì.

## Skill này dựng ra cái gì

Khung 1080×1920 (9:16), nền đen kèm lưới mờ, **hai khung 9:16 cạnh nhau**:

| | Trái | Phải |
|---|---|---|
| Nội dung | video **thô** bạn đưa vào | bản **AI đã cắt** |
| Nhãn trên | `BẢN GỐC` — trắng | `AI ĐÃ CẮT` — vàng, có glow |
| Badge | — | `✦ AI` góc trên trong khung |
| Pill dưới | `9,8 GIÂY` — nền xám | `7,0 GIÂY` — nền vàng |
| Giữa 2 khung | badge tròn `VS` | |

**Chạy TUẦN TỰ, không song song** (đây là điểm khác với mọi template before/after
thường gặp):

```
Pha 1  0 → 9,8s    TRÁI chạy, có tiếng gốc
                   PHẢI đứng hình ở FRAME ĐẦU của bản AI, tối còn 32%, câm
                   nhãn + pill bên phải mờ còn 45%

Pha 2  9,8 → 16,8s PHẢI chạy, có tiếng bản AI
                   TRÁI đứng hình ở FRAME CUỐI của bản thô, tối còn 32%, câm
                   nhãn + pill bên trái mờ còn 45%
```

Tổng thời lượng = thô + AI. Hai pill thời lượng hiện **từ đầu tới cuối** để
người xem biết trước 9,8 vs 7,0 rồi mới xem.

## Cần gì để chạy

| Thứ cần | Bắt buộc? | Nếu chưa có thì làm gì (lệnh cụ thể) |
|---|---|---|
| `ffmpeg` + `ffprobe` | Có | Windows: `winget install Gyan.FFmpeg` · macOS: `brew install ffmpeg` · Linux: `sudo apt install ffmpeg`. Mở lại terminal rồi gõ `ffmpeg -version`. Phải có **cả hai** file. |
| `python` 3.8+ | Có | https://www.python.org/downloads/ |
| `Pillow` | Có | `pip install Pillow` — dùng để vẽ lớp giao diện |
| `numpy` | Có | `pip install numpy` — chỉ `verify.py` cần |
| Font **Be Vietnam Pro** | Có | Đã có sẵn ở `shared-sources/Font/Be_Vietnam_Pro/` (skill tự dò lên các thư mục cha). Nơi khác: tải ở fonts.google.com, giải nén vào `<thư-mục>/Font/Be_Vietnam_Pro/` rồi gọi `--resources "<thư-mục>"`. **Font phải có dấu tiếng Việt** — Arial/Impact không có. |
| Video thô **có tiếng** | Có | Mỗi pha phát tiếng của chính bên đó. Video câm: ghép tiếng vào trước bằng `ffmpeg -i silent.mp4 -i voice.wav -map 0:v -map 1:a -c:v copy -c:a aac co_tieng.mp4` |
| Video thô **fps cố định (CFR)** | Có | File quay điện thoại hay bị VFR → `ffmpeg -i raw.mp4 -c:v libx264 -crf 16 -r 30 -c:a copy cfr.mp4` |
| skill `nns-cut-silence` | Chỉ khi bỏ `--right` | Bỏ `--right` nghĩa là skill này tự cắt khoảng lặng. Không có skill đó thì tự cắt rồi truyền `--right "<file>.mp4"`. |

**Bước 1 luôn là chạy preflight. Preflight báo THIEU thì dừng, làm theo hướng dẫn nó in ra.**

## Chạy

Ngắn nhất — chỉ 1 file thô, skill tự cắt rồi tự dựng (preflight → cắt → plan → chrome → apply → verify):

```
python <skill>/scripts/run.py --video "raw.mp4" --out "SO_SANH.mp4"
```

Đã có sẵn bản AI (ví dụ vừa chạy `/edit-nns-v1`) thì bỏ qua bước cắt:

```
python <skill>/scripts/run.py --video "raw.mp4" --right "ai.mp4" --out "SO_SANH.mp4"
```

Xem kế hoạch mà không tạo file nào:

```
python <skill>/scripts/run.py --video "raw.mp4" --out "SO_SANH.mp4" --dry-run
```

Chạy tay từng bước (khi cần tinh chỉnh giao diện):

```
python <skill>/scripts/plan.py   --left "raw.mp4" --right "ai.mp4" --plan p.json
python <skill>/scripts/chrome.py --plan p.json --outdir work
python <skill>/scripts/apply.py  --plan p.json --chrome work --out "SO_SANH.mp4"
python <skill>/scripts/verify.py --plan p.json --out "SO_SANH.mp4"
```

**Chỉ được báo "xong" khi `verify.py` thoát với mã 0.**

## Tham số

| Cờ | Mặc định | Ý nghĩa |
|---|---|---|
| `--video` (hay `--left`) | — | Video **thô**, hiện bên trái. Bắt buộc. |
| `--out` | — | File kết quả. Bắt buộc. |
| `--right` | — | Bản AI đã cắt. Bỏ đi = skill tự cắt bằng `nns-cut-silence`. |
| `--label-left` | `BẢN GỐC` | Chữ trên khung trái |
| `--label-right` | `AI ĐÃ CẮT` | Chữ trên khung phải |
| `--resources` | — | Thư mục có `Font/Be_Vietnam_Pro/` riêng |
| `--crf` / `--preset` | `18` / `medium` | Chất lượng / tốc độ encode |
| `--keep-work` | tắt | Giữ lại thư mục làm việc (PNG chrome, frame verify) để soi |
| `--dry-run` | tắt | Chỉ in kế hoạch, không tạo file |

## File sinh ra

| File | Là gì |
|---|---|
| `SO_SANH.mp4` | Video so sánh, H.264 CRF 18, AAC 256k 48kHz, 1080×1920 @30fps |
| `SO_SANH_ai.mp4` | Bản AI đã cắt (chỉ có khi bỏ `--right`) |
| `SO_SANH.plan.json` | Layout, mốc 2 pha, số frame, chữ trên pill, số giây tiết kiệm |
| `SO_SANH_work/` | PNG lớp giao diện + frame verify (chỉ giữ khi có `--keep-work`) |

## Verify đo những gì

`verify.py` fail (exit 1) nếu bất kỳ mục nào sai — **mọi thứ đều đo lại trên file
ra, không tin plan**:

1. Số frame == thô + AI; fps == 30; kích thước == 1080×1920.
2. Độ dài tiếng == độ dài hình (lệch ≤ 1 frame).
3. **Khung đang chạy đúng nội dung**: crop khung đó ở frame `k` phải khớp frame `k`
   của chính file nguồn, và phải khớp **hơn** các mồi nhử (±8, ±25 frame). So bằng
   chữ ký ảnh xám 64×64 đã chuẩn hoá z-score → chỉ đo *đúng frame hay không*, không
   bị việc làm tối/đổi tone đánh lừa.
4. **Khung đứng hình phải đứng im thật**: 2 frame cách xa nhau trong cùng 1 pha cho
   crop y hệt nhau (lệch < 1/255). Bắt được lỗi "quên freeze, cả 2 cùng chạy".
5. **Khung đang chạy phải có chuyển động**: 2 frame cách xa nhau phải khác nhau
   (> 1/255). Bắt được lỗi ngược lại — dán nhầm ảnh tĩnh vào ô đang chạy.
6. **Tiếng đúng nguồn ở đúng pha**: tương quan đường bao RMS 100 ms giữa pha 1 và
   nguồn TRÁI ≥ 0.90; pha 2 và nguồn PHẢI ≥ 0.90. Bắt được lỗi đảo pha tiếng,
   lỗi lệch pha, và lỗi "cả video chỉ có 1 nguồn tiếng".

## Cách dựng (để sau này sửa cho đúng chỗ)

Toàn bộ giao diện được vẽ sẵn thành **2 file PNG RGBA** (`chrome_p1.png`,
`chrome_p2.png`) bằng Pillow — mỗi pha một file. Lớp PNG chứa **tất cả** trừ pixel
của video đang chạy: nền, lưới, nhãn, VS, pill, badge, viền, glow, **và cả khung
đứng hình đã làm tối**. Chỗ video đang chạy là một **lỗ trong suốt bo góc**.

ffmpeg chỉ còn việc: nền đen → đặt video đang chạy vào đúng toạ độ khung → đè PNG
lên trên. Góc bo của khung đang chạy do chính lớp PNG che, **không cần mask riêng
trong filtergraph**.

Muốn đổi màu / cỡ chữ / vị trí: sửa hằng số ở đầu `scripts/_common.py`, không phải
đi lục filtergraph.

## references/

| File | Nội dung |
|---|---|
| `references/giao-dien.md` | Bảng toạ độ / màu / cỡ chữ, cách đổi layout, vì sao khung 496×882 |
| `references/cac-cai-bay.md` | Các bẫy đã dính thật: lỗ trong suốt xoá mất badge, ImageDraw ghi đè kênh alpha, concat demuxer tụt fps, `-ss` lệch frame, số giây phải lấy từ số frame |
