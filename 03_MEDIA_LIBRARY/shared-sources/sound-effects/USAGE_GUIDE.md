# Dùng SFX nào cho tình huống nào — hướng dẫn tra nhanh

> Đây là lớp tổ chức lại theo TÌNH HUỐNG DỰNG VIDEO thật (khớp với các beat đã đo
> đạc trong `edit-style-cuongmeai` và `edit-style-gpt-secret-code`), xếp trên
> `library.json` — không thay thế `library.json` (vẫn là nguồn `tags`/`description`/
> `durationMs`/`license` chính xác cho từng file). Dùng file này để tra "mình cần
> tiếng gì cho khoảnh khắc này", rồi kiểm license trong `library.json` trước khi
> dùng cho video thương mại (xem cảnh báo ở `README.md`).
>
> Đã đối chiếu bằng `ffprobe`/thử-mở file thật, không chỉ tin mô tả cũ: 11 entry
> trong `library.json` trỏ tới file KHÔNG có trên đĩa (đúng như README cảnh báo —
> chủ yếu là đoạn nhận diện ngay của bên thứ 3, bị `.gitignore`) — liệt kê ở cuối
> file này để không ai mất công tìm. Các file còn lại dưới đây đều đã xác nhận có
> mặt thật trên đĩa.

## 1. Chuyển cảnh / chuyển tip (stinger, whoosh)
| File | Dài | Khi dùng |
|---|---|---|
| `swoosh.mp3` | 0.36s | Whoosh gọn, mặc định cho MỌI lần chuyển tip/chuyển card — khớp đúng kiểu "SFX ngắn tại stinger" mà `edit-style-cuongmeai` mục 1 yêu cầu |
| `quick-swoosh.mp3` | 0.73s | Khi cần whoosh có đuôi dài hơn 1 chút, cảm giác "lướt" rõ hơn |
| `whoosh.wav` | 3.27s | Whoosh DÀY, dùng cho chuyển cảnh lớn/kịch tính hơn (vd chuyển hẳn từ hook sang thân bài), không dùng cho stinger nhỏ vì quá dài |
| `glitch.mp3` | 0.84s | Chuyển cảnh kiểu "lỗi/nhiễu" — hợp với nội dung nói về AI ảo giác/lỗi (giai đoạn "cãi nhau" trong series script-writer) |
| `fast-forward.mp3` | 8.7s | Tua nhanh — dùng khi thật sự cần montage tua nhanh nhiều cảnh liên tiếp, không phải chuyển cảnh đơn |

## 2. Nhấn mạnh / punch-in / điểm số liệu
| File | Dài | Khi dùng |
|---|---|---|
| `ting.wav` | 2.57s | Ting sáng, dùng khi 1 chi tiết/từ khoá cần "sáng lên" (khớp `punch-in zoom tại điểm nhấn` của edit-style-cuongmeai) |
| `quick-ting.mp3` | 0.94s | Bản ngắn hơn của ting — ưu tiên dùng cái này nếu nhịp video nhanh, tránh ting.wav kéo dài đè lên câu tiếp |
| `pop.mp3` | 0.97s | Pop nhẹ khi 1 element/card VỪA xuất hiện trên khung |
| `pop-2.mp3` | 0.29s | Pop cực ngắn — dùng khi nhiều pop liên tiếp gần nhau (tránh pop.mp3 dồn dập nghe rối) |

## 3. Reveal kết quả / payoff / khoe thành quả
| File | Dài | Khi dùng |
|---|---|---|
| `ta-da.mp3` | 2.07s | "Ta-da" — đúng lúc Demo Screenshot lộ ra kết quả AI trả lời, hoặc Headline Payoff chốt lợi ích |
| `correct.mp3` | 1.27s | Chuông "đúng" — dùng khi VO xác nhận 1 cách làm là đúng/hiệu quả (không chỉ dành riêng gameshow) |
| `fairy-dust.mp3` | 7.06s | Bụi tiên lấp lánh — reveal mang tính "kỳ diệu", dùng cho payoff kiểu bất ngờ/wow, không dùng cho payoff thực dụng thường |

## 4. Sai / lỗi / hiểu lầm (giai đoạn "cãi nhau" trong series 30 ngày)
| File | Dài | Khi dùng |
|---|---|---|
| `error.mp3` | 0.99s | Lỗi hệ thống — đúng cho lúc VO nói AI "bịa"/hiểu sai (hallucination) |
| `wrong-answer-buzzer.mp3` | 1.06s | Còi sai — nhẹ hơn `buzzer.mp3`, hợp giọng hài tự trào hơn là nghiêm trọng |
| `buzzer.mp3` | 1.78s | Còi buzzer gameshow đầy đủ — dùng khi muốn nhấn mạnh "sai" rõ ràng, kịch tính hơn |
| `fail.mp3` | 5.04s | Nhạc hiệu thất bại — DÀI, chỉ dùng khi có cả 1 đoạn kể chuyện thất bại, không phải 1 khoảnh khắc ngắn |

## 5. Hài / meme / tự trào (không lạm dụng — chỉ 1 chi tiết/tập, đúng tinh thần "hài không gượng" của script-writer)
| File | Dài | Khi dùng |
|---|---|---|
| `boing.mp3` | 0.89s | Lò xo hoạt hình — nhấn 1 chi tiết hài ngắn, kiểu đùa nhẹ |
| `duck-toy.mp3` | 0.96s | Vịt kêu chít — hài kiểu "ngớ ngẩn dễ thương", hợp giọng gần gũi của series |
| `chomp.mp3` | 0.49s | Tiếng cắn — hợp nếu có chi tiết ăn uống/tự trào kiểu "cắn câu" |
| `crickets.mp3` | 5.28s | Dế kêu — im lặng gượng gạo, dùng đúng lúc VO tự trào "...và không ai vỗ tay" |
| `dry-fart.mp3` / `fart-echo.mp3` | 0.31s / 1.87s | Hài mạnh — CÂN NHẮC kỹ trước khi dùng, có thể lệch tông "gần gũi, có duyên" sang "nhảm", chỉ dùng nếu chắc chắn hợp khoảnh khắc |

## 6. Gõ phím / thao tác demo (Prompt Card, screen-recording Claude/ChatGPT)
| File | Dài | Khi dùng |
|---|---|---|
| `mechanical-keyboard.mp3` | 12.1s | Gõ bàn phím cơ — nền cho đoạn đang "gõ prompt", cắt độ dài khớp lúc VO đọc prompt |
| `iphone-typing.mp3` | 16.9s | Gõ phím điện thoại — dùng nếu ngữ cảnh là gõ trên mobile thay vì laptop |
| `mouse-click.mp3` | 3.07s | Click chuột — dùng khi demo có thao tác chọn/bấm nút trên giao diện |
| `click-button.mp3` | 0.50s | Click UI ngắn — hợp hơn cho 1 cú bấm đơn lẻ (vd bấm nút Gửi) |
| `camera-shutter.mp3` / `camera-snap.wav` | 0.34s / 2.70s | Chụp màn hình/freeze frame — dùng khi cần "chụp" lại 1 khoảnh khắc demo để nhấn |
| `camera-flash-1.wav` | 1.24s | Đèn flash — đi kèm camera-shutter nếu muốn hiệu ứng chụp ảnh rõ hơn |

## 7. Đếm số / dữ liệu / build-up
| File | Dài | Khi dùng |
|---|---|---|
| `digital-counting-1.mp3` | 0.51s | Đếm số ngắn — số liệu nhỏ, count-up nhanh |
| `digital-counting-2.mp3` | 7.06s | Đếm số dài — dùng khi count-up 1 con số lớn cần thời gian "chạy" |
| `build-up.mp3` | 7.37s | Dồn nhịp tăng dần — dẫn vào payoff/cao trào, đặt trước khi ta-da/correct vang lên |
| `riser-metallic.mp3` | 2.76s | Riser ngắn hơn build-up — dùng khi cần dồn nhịp nhanh, không đủ chỗ cho build-up 7s |
| `take-off.mp3` | 2.55s | Cất cánh vút lên — hợp payoff kiểu "tăng trưởng/hiệu suất x10" |

## 8. Hồi hộp / khoảnh khắc "khựng lại" (aha-moment, giai đoạn Hiểu tính nhau/Cãi nhau)
| File | Dài | Khi dùng |
|---|---|---|
| `heartbeat-single.mp3` | 1.5s | 1 nhịp tim đơn — đúng cho beat "khựng lại một giây" đã dùng trong kịch bản Ngày 1 (script-writer) |
| `heartbeat-calm-1.mp3` | 4.5s | Nhịp tim chậm rãi — hồi hộp nhẹ kéo dài, dùng khi cả 1 đoạn cần không khí chờ đợi |
| `heartbeat-fast.mp3` | 4.22s | Nhịp tim nhanh — căng thẳng rõ hơn, dùng cho đoạn kể lúc bực/thất vọng |

## 9. Tiền / hiệu quả kinh tế / CTA thắng
| File | Dài | Khi dùng |
|---|---|---|
| `ka-ching.mp3` | 2.44s | Máy tính tiền — chốt đơn/hiệu quả kinh doanh cụ thể |
| `buy.mp3` | 1.20s | Mua hàng thành công — hợp payoff dạng "xong việc" |
| `money.mp3` | 2.48s | Tiền xào xạc — nhẹ hơn ka-ching, dùng khi chỉ ẩn ý về tiền/lợi ích không cần nhấn quá mạnh |

## 10. Thông báo / CTA follow
| File | Dài | Khi dùng |
|---|---|---|
| `ding.mp3` | 2.95s | Ding thông báo sáng — hợp lúc badge CTA follow xuất hiện (outro) |

---

## File trong `library.json` nhưng KHÔNG có trên đĩa (đã kiểm tra thật, không dùng được)

Đúng như cảnh báo trong `README.md` (đoạn nhận diện ngay của bên thứ 3 bị
`.gitignore`) — các entry sau tồn tại trong `library.json` nhưng file thực tế
KHÔNG có trong thư mục này, nên đừng tham chiếu tới chúng khi lên blueprint:
`anime-wow-1.mp3`, `anime-wow-2.mp3`, `clash-royale-startup.mp3`,
`hava-nagila.mp3`, `jontron-what.mp3`, `mario-coin.mp3`, `mii-channel-music.mp3`,
`netflix-jingle.mp3`, `run-vine.mp3`, `sonic-ring.mp3`,
`spongebob-a-few-moments-later.mp3`, `spongebob-two-hours-later.mp3`,
`video0_k03U0Iy.mp3`, `vine-boom.mp3`, `windows-xp-startup.mp3`,
`x-files-theme-1.mp3`, `x-files-theme-2.mp3`, `y2mate_VKI8qDn.mp3`.

Nếu cần đúng hiệu ứng kiểu "chuyển thời gian" (vd SpongeBob "a few moments
later") hay "khởi động hệ thống" (Windows XP) mà bản gốc bị thiếu — báo cho user,
đừng tự thay bằng file khác rồi coi như tương đương, vì cảm giác/nhận diện meme
của bản gốc không thể thay thế bằng file khác trong kho.
