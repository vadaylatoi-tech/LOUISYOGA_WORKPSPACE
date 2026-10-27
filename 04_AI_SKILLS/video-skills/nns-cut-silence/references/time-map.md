# Time map — bản đồ thời gian cũ → mới

## Vì sao bắt buộc phải có

Cắt khoảng lặng làm **mọi mốc thời gian của timeline gốc lệch đi**, và lệch **không đều**:
mỗi nhát cắt cộng thêm một lượng dịch. Một caption dựng trên timeline gốc sẽ đúng ở
câu đầu, lệch 0.3s ở câu thứ ba, lệch 2s ở cuối video. Cùng chuyện đó với SFX cue,
overlay, logo, punch-in.

Vì vậy `plan.py` luôn xuất `<plan>.timemap.json` cùng lúc với plan. Không có nó thì bước
sau **không thể** đặt đúng chỗ.

## Định dạng

```json
{
  "skill": "nns-cut-silence",
  "plan_version": 1,
  "fps": "30/1",
  "fps_float": 30.0,
  "source": "...\\VIDEO_RAW.mp4",
  "source_duration": 13.9,
  "output_duration": 13.366666666666667,
  "how_to_use": "Tim segment co old_start <= t < old_end, roi new_t = t - shift. ...",
  "segments": [
    {
      "old_start": 0.0,   "old_end": 6.2,
      "new_start": 0.0,   "new_end": 6.2,
      "shift": 0.0,
      "old_start_frame": 0, "old_end_frame": 186,
      "new_start_frame": 0, "new_end_frame": 186
    },
    {
      "old_start": 6.466666666666667, "old_end": 10.833333333333334,
      "new_start": 6.2,               "new_end": 10.566666666666666,
      "shift": 0.26666666666666666,
      "old_start_frame": 194, "old_end_frame": 325,
      "new_start_frame": 186, "new_end_frame": 317
    }
  ],
  "removed": [
    { "old_start": 6.2, "old_end": 6.466666666666667, "collapsed_to": 6.2 }
  ]
}
```

- `segments` là các đoạn **được giữ**, theo thứ tự, phủ kín timeline mới không chồng lấn.
- `shift` là lượng dịch **không đổi trong cả đoạn** — nên phép map là dịch thuần, không
  co giãn, không resample. Tốc độ nói không đổi.
- `removed` là các đoạn đã bị xoá; `collapsed_to` là mốc trên timeline mới mà cả đoạn
  đó co về.

## Cách map

```
new_t = t - shift   với segment thoả  old_start <= t < old_end
```

Nếu `t` không nằm trong segment nào (nó ở trong một `removed`) thì điểm đó **đã bị xoá**.
Quy ước: dùng `new_end` của segment ngay trước đó, tức mốc mà cả vùng bị xoá co về.
Ranh giới `old_end` chính là đầu vùng xoá nên tự động rơi đúng vào quy ước này.

Frame thì dùng cặp `*_frame`, vẫn là phép trừ nguyên — không có làm tròn nào để mà sai.

## Dùng `remap.py`

**Vài mốc lẻ:**

```
python scripts/remap.py --timemap cut.plan.timemap.json --times "3.2,17.8,44.0"
```

```
  cu (goc)      ->  moi (sau cat)
  3.200         ->  3.200
  6.300         ->  6.200          (nam trong vung DA BI XOA)
  11.050        ->  10.567         (nam trong vung DA BI XOA)
  12.000        ->  11.467
```

**File SRT:**

```
python scripts/remap.py --timemap cut.plan.timemap.json --srt sub.srt --srt-out sub_moi.srt
```

Cue nào bị xoá hết (sau khi map, `end - start < 0.04s`) thì **bỏ luôn** và các cue còn lại
được **đánh số lại**. Đọc `utf-8-sig` nên file có BOM cũng vào được.

**File JSON cue (SFX, overlay, logo...):**

```
python scripts/remap.py --timemap cut.plan.timemap.json --json sfx_cue.json --json-out sfx_cue_moi.json
```

Đi đệ quy qua cả cây JSON và đổi mọi giá trị số nằm ở các khoá:
`time`, `at`, `start`, `end`, `t0`, `t1`, `start_sec`, `end_sec`.
Cấu trúc còn lại giữ nguyên. In ra số mốc đã đổi để đối chiếu.

## Nối với các skill khác

| Bước sau | Nên làm |
|---|---|
| `nns-auto-sub` (caption karaoke) | **Transcribe lại trên file đã cắt.** Chuẩn hơn remap, vì word-level timing của bản gốc vốn đã sai chỗ (Whisper phình độ dài từ) và remap không sửa được cái đó. Chỉ remap khi bạn đã sửa tay transcript của bản gốc và không muốn làm lại |
| `nns-add-sfx` | Remap cue file, **và dùng `cut.wav`** làm nguồn tiếng chứ không lấy tiếng trong `.mp4` (tránh thêm một đời nén AAC) |
| `nns-face-highlight` | Không cần time map — nó tự dò mặt trên file đã cắt. Chạy sau khi cắt |
| Cắt lần thứ hai | Mốc `--protect` phải là mốc trên **file đã cắt**. Dùng `remap.py --times` để chuyển mốc cũ sang |

## Những chỗ dễ sai

1. **Dùng mốc timeline mới để đưa vào `--protect`.** `--protect` luôn là timeline **gốc**
   (tức file đang truyền vào `--video`).
2. **Map đầu và cuối của một cue riêng lẻ rồi tưởng độ dài không đổi.** Nếu cue vắt qua
   một nhát cắt thì độ dài **co lại**. Đúng như vậy — nó phải co, vì phần giữa đã bị xoá.
   Nhưng nếu cue là một SFX one-shot có độ dài cố định thì đừng map cả hai đầu: map điểm
   bắt đầu, giữ nguyên độ dài.
3. **Cộng dồn nhiều lần cắt bằng cách cộng các `shift`.** Không được. Mỗi lần cắt sinh
   một time map riêng, phải map **tuần tự** qua từng cái theo đúng thứ tự đã cắt.
4. **Sửa `output_duration` bằng tay.** `verify.py` đối chiếu số frame thật với plan;
   sửa tay là lệch và verify sẽ fail — đúng như nó phải làm.
