# Cue sheet & mật độ SFX

## Quyết định gốc: HOOK-WEIGHTED

Creator của kênh này đã xem một bản **53 cue rải đều cả video** rồi tự tay cắt
lại chỉ còn **~20 giây đầu**. Đó là dữ kiện, không phải sở thích đoán ra.

Nên mặc định của skill:

| Vùng | Mật độ | Neo vào |
|---|---|---|
| Hook (20s đầu) | ~0.60 cue/s | cắt cảnh thật > đầu câu > đầu từ |
| Phần giải thích | ~0.12 cue/s | **chỉ** cắt cảnh thật |
| Video ≤ 30s | rải đều cả video, mật độ hook | như hook |

Ngoài hook **không rải đều**. Nếu không có cắt cảnh thật thì không có cue —
thà im còn hơn đánh vào chỗ không có gì xảy ra.

## Không bao giờ tự bịa mốc

Mọi cue đều neo vào một thứ **đo được**:

| Ưu tiên | Neo | Đo bằng |
|---|---|---|
| 3 | cắt cảnh thật | `select=gt(scene,0.25)` |
| 2 | đầu câu | từ ngay **sau** dấu chấm trong transcript |
| 1 | đầu từ (≥4 ký tự) | mốc word-level của Whisper |

Chọn theo ưu tiên giảm dần, và hai cue phải cách nhau ≥ `--min-gap` (0.45s).
Vẫn thiếu so với mật độ đề ra thì mới rải đều — và cột `vì sao` sẽ ghi rõ
`rải đều` để bạn thấy chỗ nào là suy ra chứ không phải đo được.

## Biên câu là biên MỞ

Câu mới bắt đầu từ từ **NGAY SAU** dấu chấm, không phải từ chính từ mang dấu
chấm. Mọi chỗ trong skill dùng đúng một luật này: `plan_cues.py` (neo cue),
`check_cards.py` (dò lặp lời thoại), `punct.py` (đếm câu).

Và phải chạy `punct.py` **trước** khi gom cụm sub: Whisper hay bỏ quên dấu chấm
ở từ cuối cùng và ở chỗ người nói nghỉ dài. Thiếu nó thì cụm cuối dính vào cụm
trước, và cue mất hết mốc đầu câu.

## Khối `optional`

Mọi cue **ngoài hook** đều mang `"optional": true`. Bỏ hết bằng một tham số:

```bash
python scripts/build_sfx.py --cues x.cues.json --out x.sfx.raw --total 79.233 --drop-optional
python scripts/master.py --video x.sub.mp4 --bed x.sfx.raw --out x.mp4
```

**Không phải render lại hình.** Lớp SFX là bước audio riêng, `master.py` mux
bằng `-c:v copy`. Đây chính là lý do thứ tự các bước phải là burn → sfx →
master, chứ không gộp burn với mix.

## Dạng cue

```json
{"t": 3.42, "file": "whoosh.wav", "gain_db": -19.4,
 "off": 0.031, "dur": 0.700, "fin": 0.0, "fout": 0.03,
 "optional": false, "role": "transition", "why": "cắt cảnh"}
```

| Trường | Nghĩa |
|---|---|
| `t` | mốc trên timeline video, giây |
| `off` | cắt bỏ bao nhiêu giây **đầu file** SFX. `null` = tự đo onset |
| `dur` | lấy bao nhiêu giây. `null` = để nguyên |
| `gain_db` | đo từ đỉnh thật của đoạn, kéo về mức đích của vai |
| `optional` | true = cue ngoài hook, bỏ được bằng một tham số |

## Đo onset từng file — bắt buộc

Rất nhiều file SFX **im lặng ở đầu**. Đo thật trên thư viện của máy này:
`mouse-click.mp3` im **1.02s**, `buzzer.mp3` 0.66s, `digital-counting-2.mp3`
0.66s, `new-item.wav` 0.65s, `funny.mp3` 0.52s, `pop.mp3` 0.23s.

Cắt 0.2s từ điểm 0 → **cue im ru**. Cue vẫn nằm trong file, verify pixel vẫn
đạt, nhưng người xem không nghe thấy gì.

`build_sfx_json.py` tự đo onset khi `off` là `null`, ngưỡng −42 dBFS, lùi lại
10ms cho khỏi cắt mất transient.

## File có đỉnh ở GIỮA — riser, whoosh dài

Lấy cả file thì nó lên sớm rồi im trước lúc cần đập. Đo thật:
`riser-metallic.mp3` leo tới đỉnh ở **1.77s** rồi tắt.

Cách làm đúng: lấy **ĐOẠN GIỮA** sao cho đỉnh rơi đúng mốc.

```
climax = mốc đỉnh trong file (đo bằng analyse_sfx)
lead   = đoạn trước đỉnh   (≤ 80% độ dài tối đa của vai)
tail   = đoạn sau  đỉnh    (≤ 20%)
off = climax − lead
dur = lead + tail
t   = mốc_muốn_đập − lead
```

Kết quả: tiếng bắt đầu leo từ `t`, đỉnh rơi **đúng** vào mốc cắt cảnh.

## Mức đích theo vai

Lấy từ 4 cue-sheet thật đã được duyệt trong project này (`ROLE_TARGET_PEAK` của
`nns-add-sfx/scripts/_common.py`):

| Vai | Đỉnh đích (dBFS) | Dài tối đa (s) |
|---|---|---|
| impact | −12.0 | 0.70 |
| negative | −19.0 | 1.10 |
| confirm | −20.0 | 1.30 |
| transition | −21.0 | 0.70 |
| accent | −22.0 | 0.80 |
| riser | −24.0 | 2.50 |
| bed | −34.0 | 4.00 |

`gain_db` = đích − đỉnh thật của đoạn đã cắt. Đo, không đoán.

## Kiểm lớp SFX

`build_sfx.py` in ra đỉnh và RMS của cả lớp, và **exit 1 nếu lớp tự nó đã clip**
(> 0.98). Lớp SFX clip trước khi trộn thì không cách nào cứu ở bước master.

Kiểm SFX có thật sự vào đúng chỗ trong bản cuối: xem `references/cac-bay-da-gap.md`
mục "Đo SFX bằng phép trừ".
