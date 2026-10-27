# Ngưỡng im lặng — suy ra từ chính file, không ghim cứng

## Số đo thật (không phải phỏng đoán)

Đo trên một video talking-head tiếng Việt 226s của chính creator này:

| Đại lượng | Giá trị |
|---|---|
| Sàn ồn (p1 của RMS 10ms) | **-84 dB** |
| Mức nói (p70) | **-17.6 dB** |
| Vùng -50..-35 dB | **14.6% thời lượng** |

Vùng -50..-35 dB đó **là phụ âm nhẹ và hơi thở**, không phải im lặng. Đây là điểm
quan trọng nhất của cả skill:

- Ngưỡng **-35 dB** đánh dấu **69 vùng cắt**, và vùng nào **cũng có tiếng nói**.
- Ngưỡng **-50 dB** suy ra từ phân bố cho **52 vùng**, peak xấu nhất **-39.1 dB**
  (21 dB dưới mức nói) → **an toàn**.

Vì vậy: mọi con số ngưỡng ghim cứng (-30, -35, -38 dB) đều sai với file này, và sẽ
sai với file khác theo hướng khác. Ngưỡng **phải** suy ra từ phân bố năng lượng của
chính file đang xử lý.

## Công thức đang dùng

`plan.py` decode audio ra PCM (mono downmix, sample rate gốc), tính RMS theo hop
**10ms**, rồi:

```
floor  = p1                              # sàn ồn
speech = p70                             # mức nói
mid    = floor + 0.5 * (speech - floor)  # điểm giữa, tính theo dB
cand   = min(mid, speech - 30)           # luôn cách mức nói ít nhất 30 dB
cand   = max(cand, floor + 6)            # không sát sàn ồn đến mức vô dụng
NGƯỠNG = min(cand, -45)                  # CHẶN CỨNG: không bao giờ lỏng hơn -45 dB
```

Lý do từng dòng:

- **p1 làm sàn ồn, p70 làm mức nói.** p1 chứ không phải min: một mẫu 0 duy nhất
  (digital silence ở đầu file) sẽ kéo min xuống -inf. p70 chứ không phải trung vị:
  trong talking-head, khoảng 30% thời lượng là khoảng nghỉ/phụ âm, nên p70 rơi đúng
  vào thân âm tiết.
- **Điểm giữa theo dB** cho khoảng cách tương đối, tự co giãn theo độ ồn của phòng.
  Với file đo thật: -84 + 0.5·66.4 = **-50.8 dB** — trùng đúng con số -50 dB đã
  kiểm nghiệm là an toàn.
- **speech - 30 dB** là cái phanh khi phòng ồn. Nếu sàn ồn cao (-47 dB), điểm giữa
  sẽ nhảy lên -32 dB, tức là cắt thẳng vào phụ âm. Dòng này chặn lại.
- **floor + 6 dB** là cái phanh ngược: nếu sàn ồn cực thấp, điểm giữa vẫn hợp lý,
  nhưng dòng này bảo đảm ngưỡng không bao giờ nằm dưới sàn ồn (khi đó không bắt được gì).
- **Chặn cứng -45 dB** là luật cuối. Vùng -50..-35 dB đã đo là phụ âm/hơi thở.
  Ngưỡng lỏng hơn -45 dB là bước vào vùng đó.

## Kiểm trên 4 file thật của máy này

| File | p1 | p70 | Ngưỡng ra | Số khoảng lặng ≥0.35s |
|---|---|---|---|---|
| `video_demo/VIDEO_RAW.mp4` (13.9s) | -69.5 | -20.7 | **-50.7** | 2 |
| `OUT/0822_edit_v4.mp4` (215.4s) | -81.6 | -15.9 | **-48.8** | 7 (min-sil 0.30) |
| `hyperframes/app/assets/input-video.mp4` (50.9s) | -46.8 | -17.9 | **-45.0** (chặn cứng) | **0** |
| `hyperframes/buoc7-ai/assets/input-video.mp4` (62.4s) | -46.9 | -21.1 | **-45.0** (chặn cứng) | **0** |

Hai file cuối đáng chú ý: sàn ồn của chúng là **-47 dB** (file đã qua xử lý /
noise gate làm nền dâng lên). Với hai file đó, công thức trả về 0 vùng cắt —
**đó là câu trả lời đúng**, không phải lỗi. Không có khoảng lặng nào an toàn để cắt.
Nếu ép cắt (`--threshold-db -40`) là cắt vào phụ âm.

## Self-check: -34 dB, và vì sao nó cứu

Sau khi đã lập xong danh sách vùng cắt, `plan.py` decode lại lần thứ hai và đo
**peak thực tế từng mẫu** (max |sample| trên mọi kênh) trong **đúng** cửa sổ sắp bị bỏ.
Vùng nào peak > **-34 dB** → **từ chối cả kế hoạch**, không ghi file plan.

-34 dB đến từ: mức nói -17.6 dB trừ ~16 dB. Một mẫu vượt -34 dB trong vùng được cho
là "im lặng" chỉ có thể là thân âm tiết.

Đây không phải lý thuyết. Chạy thật với ngưỡng ép -22 dB trên `VIDEO_RAW.mp4`:

```
════════════════════════════════════════════════════════════
  TU CHOI CAT — 6 vung co TIENG NOI (peak > -34.0 dB)
════════════════════════════════════════════════════════════
    #0   00:00.733 -> 00:01.067  (frame 22..32)   peak = -25.6 dB
    #2   00:03.100 -> 00:04.433  (frame 93..133)  peak = -11.6 dB
    ...
[LOI] Ke hoach khong an toan — khong ghi file plan.
```

Peak -11.6 dB là **to hơn cả mức nói trung bình**. Không có self-check thì 1.3 giây
giữa câu đó đã bị xoá.

`verify.py` đo lại đúng phép đo này trên file gốc một lần nữa sau khi cắt — không tin
con số đã ghi trong plan.

## Vì sao 10ms, vì sao RMS mono, vì sao peak đa kênh

- **Hop 10ms**: đủ mịn để bắt khoảng lặng 0.2s (20 hop), đủ thô để không bị nhiễu
  từng mẫu. Cũng là hop đã dùng khi đo các con số ở đầu tài liệu này, nên số so được.
- **RMS trên bản downmix mono** để phát hiện: tai nghe năng lượng, không nghe mẫu lẻ.
- **Peak trên từng kênh** (không downmix) để self-check: nếu tiếng nói chỉ có ở một
  kênh, downmix sẽ hạ nó 6 dB và self-check có thể bỏ lọt.

## Hình học một nhát cắt

```
khoảng lặng phát hiện được:  [====================================]
                             rs                                 re
GUARD (0.03s)                [--]                           [--]
vùng bị bỏ (phần GIỮA):           [====================]
còn lại sau khi cắt:         [--]                      [--]   = --keep (0.10s)
```

- Lượng bỏ = `(re - rs) - keep`, chặn trên bởi `(re - rs) - 2*guard`.
- Căn giữa khoảng lặng, rồi **frame-align làm tròn VÀO TRONG**
  (`f0 = ceil(t0*fps)`, `f1 = floor(t1*fps)`) — thà cắt ít hơn kế hoạch một frame
  còn hơn nhiều hơn một frame.
- Nhát ngắn hơn `MIN_DROP_SEC = 0.05s` thì bỏ, vì vô nghĩa mà lại thêm một mối nối.
- `--trim-edges` (mặc định tắt): khoảng lặng chạm frame 0 hoặc frame cuối thì bỏ từ
  phía ngoài vào, vì phía ngoài không có câu nào cần nhịp thở.

## Khi nào chỉnh tay

| Triệu chứng | Chỉnh |
|---|---|
| Nghe bị "cụt", chữ đầu câu sau dính chữ cuối câu trước | tăng `--keep` lên 0.14–0.20 |
| Vẫn còn nhiều khoảng nghỉ | giảm `--min-sil` xuống 0.25 |
| plan.py từ chối vì peak > -34 dB | hạ ngưỡng (`--threshold-db` số âm hơn) hoặc `--protect` đoạn đó |
| Phòng ồn, ra 0 nhát cắt | **đừng ép**. Xử lý ồn trước (`ffmpeg -af afftdn`) rồi cắt trên file đã xử lý |
| Cắt xong nghe khô, mất nhịp | tăng cả `--keep` và `--min-sil`; hoặc `--protect` các đoạn cần nhịp |
