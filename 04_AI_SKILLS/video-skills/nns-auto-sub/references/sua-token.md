# Sửa transcript ở mức TOKEN — và tại sao regex cụm từ vô dụng

## 1. Lỗi đắt tiền: regex nhiều từ KHÔNG BAO GIỜ khớp

Sub karaoke vẽ **từng từ**. Một caption token chỉ là `"cloud"`, không bao giờ là
`"dùng cloud để"`. Nên mọi luật viết kiểu này:

```python
re.sub(r"dùng cloud để", "dùng Claude để", text)      # KHÔNG BAO GIỜ KHỚP
re.sub(r"hyper\s*frame", "HyperFrames", text)          # KHÔNG BAO GIỜ KHỚP
```

đều chạy êm, không báo lỗi, và **không sửa được gì** — vì chuỗi đem đi so chỉ dài
đúng một token. Đây là chỗ đã mất thời gian thật.

Cách đúng: luật chạy trên **một token**, và được phép **nhìn token trước / token sau**.
Muốn khớp nhiều token thì phải khai báo là `merge` để chương trình tự trượt cửa sổ.

## 2. Whisper nghe sai tên riêng — ví dụ thật

Chạy `large-v3` trên video thật của kênh này (`video_demo/0817_cut.mp4`):

> "Đây là video có sử dụng AI để edit video, có sử dụng **Cloud** và **Hyperframe**
> để cùng nhau edit một cái video một cách hoàn chỉnh."

Đúng ra là **Claude** và **HyperFrames**. Whisper sai đều tay ở chỗ này, mọi lần chạy
đều sai như vậy — nên phải có luật, không thể sửa tay từng lần.

## 3. Bốn loại luật

File `--fixes` là JSON, chỉ nhận 4 khoá. Khoá lạ là **báo lỗi ngay**, không bỏ qua âm thầm.

```json
{
  "token":   { "cloud": "Claude", "hyperframe": "HyperFrames" },
  "merge":   [ { "words": ["chat", "gpt"], "to": "ChatGPT" } ],
  "context": [ { "token": "cloud", "to": "Claude",
                 "not_next": ["computing", "run"], "not_prev": ["google"] } ],
  "keep":    [ "cloudflare", "icloud" ]
}
```

| Khoá | Làm gì | Mốc thời gian |
|---|---|---|
| `token` | 1 token -> 1 token. So không phân biệt hoa/thường, bỏ dấu câu hai đầu | giữ nguyên |
| `merge` | N token liền nhau -> 1 token | gộp: `start` của token đầu, `end` của token cuối |
| `context` | như `token` nhưng có điều kiện về token lân cận | giữ nguyên |
| `keep` | danh sách cấm — token trong đây **không bao giờ** bị đổi | — |

Điều kiện dùng được trong `context`: `next`, `prev` (bắt buộc phải khớp) và
`not_next`, `not_prev` (khớp là chặn lại).

**Thứ tự ưu tiên:** `keep` > `context` > `merge` > `token`.
`merge` chạy trước tiên (vì nó thay đổi số lượng token), rồi `context`, rồi `token`.
Token nào đã bị `context` xử lý thì `token` không chạm vào nữa.

Dấu câu được giữ lại: `"Cloud,"` -> `"Claude,"`, không phải `"Claude"`.

## 4. Luôn in cả "CÓ Ý KHÔNG SỬA"

Đây là phần quan trọng nhất của bước này. Một luật sai **im lặng** thì rất khó phát
hiện — nên mỗi lần chạy đều in ra cả hai danh sách. Ví dụ thật:

```
  DA SUA CHU (4):
      [  5.40]  "chat gpt"  ->  "ChatGPT"        (merge chat+gpt)
      [  6.30]  "hyper frame"  ->  "HyperFrames" (merge hyper+frame)
      [  7.20]  "cap cut"  ->  "CapCut"          (merge cap+cut)
      [  0.30]  "Cloud"  ->  "Claude"            (context cloud->Claude)

  CO Y KHONG SUA (3) — doc ky, luat sai se lo ra o day:
      [  1.80]  "Cloud"  giu nguyen — luat context cloud->Claude bi chan: tu TRUOC la "Google" (not_prev)
      [  3.30]  "cloud"  giu nguyen — luat context cloud->Claude bi chan: tu SAU la "computing" (not_next)
      [  4.50]  "Cloudflare"  giu nguyen — nam trong danh sach keep
```

Câu gốc: *"dùng Cloud để edit, Google Cloud Run thì khác, cloud computing nữa,
Cloudflare ok, chat gpt và hyper frame, cap cut"*.

Đúng cả 7 quyết định: sửa cái đáng sửa, giữ `Google Cloud Run`, `cloud computing`,
`Cloudflare` — đây chính là lý do luật phải **nhìn token lân cận** chứ không thể
đổi mù `cloud` -> `Claude`.

## 5. Whisper phình độ dài từ

Whisper kéo `end` của từ để lấp đầy khoảng trống tới từ sau. Số đo thật trên clip
9.43 giây (27 từ, trung vị độ dài từ = **0.280s**):

| Từ | start | end | độ dài |
|---|---|---|---|
| `video` | 0.98 | 1.68 | **0.700s** |
| `và` | 5.18 | 5.78 | **0.600s** |
| `AI` | 2.56 | 2.72 | 0.160s |
| `cái` | 7.86 | 8.00 | 0.140s |

`"và"` — một âm tiết — ra 0.600s, gấp **2.1 lần** trung vị. Không phải người nói kéo
dài, mà là Whisper lấp chỗ trống.

`fix_durations()` chặn lại:

```
cap = max(0.35, trung_vị × 2.0)
nếu token dài hơn 6 ký tự:  cap += 0.06 × (số_ký_tự − 6)
end mới = min(end, start + cap)
và không bao giờ để end tràn qua start của từ sau
```

Kết quả trên clip đó: `"video"` 0.700 -> 0.560s, `"và"` 0.600 -> 0.560s. Chỉ 2/27 từ
bị chạm — đúng ý: chỉ cắt phần phình, không bóp các từ bình thường.

Tắt bằng `--no-dur-fix`. Điều chỉnh bằng `--dur-factor` / `--dur-min-cap`.

**Lưu ý:** việc chặn `end` **không** làm vệt karaoke bị chớp, vì cửa sổ sáng của mỗi
từ bàn giao tại `start` của từ sau chứ không tại `end` (xem `karaoke-ass.md` mục 3).
`end` chỉ quyết định lúc **cụm cuối biến mất** và giúp phát hiện khoảng nghỉ khi gom cụm.

## 6. Luật mặc định có sẵn

`DEFAULT_FIXES` trong `fix_tokens.py`: Claude, ChatGPT, GPT, HyperFrames, CapCut,
Gemini, Midjourney, Remotion, Veo, AI — kèm `merge` cho `chat+gpt`, `hyper+frame`,
`cap+cut`, `mid+journey`, và `context` chặn `cloud` khi nó thật sự là đám mây
(`google cloud`, `cloud computing`, `cloud run`, ...).

Bỏ hết luật mặc định: `--no-default-fixes`. Khi đó chỉ luật trong `--fixes` chạy.
File `--fixes` **cộng thêm** vào luật mặc định (không thay thế), và luật của bạn
ghi đè luật mặc định nếu trùng token.

## 7. Sửa tay một chỗ duy nhất

Không cần viết luật cho lỗi chỉ xảy ra một lần. Sửa thẳng `<out>.words.json` (trường
`w` của token), rồi chạy lại từ bước 3 — **không phải nhận dạng lại**:

```bash
python scripts/build_ass.py --video "v.mp4" --out "v_sub.mp4"
python scripts/burn.py      --video "v.mp4" --out "v_sub.mp4"
python scripts/verify.py    --video "v.mp4" --out "v_sub.mp4"
```

Nếu sửa `.words.json` thì phải chạy lại `fix_tokens.py` trước (nó sinh `.fixed.json`),
hoặc sửa thẳng `.fixed.json` để bỏ qua bước đó.
