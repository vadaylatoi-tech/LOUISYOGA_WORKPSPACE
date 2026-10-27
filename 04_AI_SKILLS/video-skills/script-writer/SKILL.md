---
name: script-writer
description: "Viết KỊCH BẢN (lời thoại) cho video talking-head để user tự cầm quay raw footage, sau đó đưa footage đó vào một skill `edit-style-*` để AI dựng. Đây là bước NGƯỢC với các skill edit-style — edit-style nhận footage có sẵn rồi tạo blueprint dựng; skill này nhận 1 chủ đề/ý tưởng NGẮN rồi viết ra lời thoại đầy đủ trước khi quay, đúng nhịp/cấu trúc/độ dài mà edit-style cần để cắt dựng mượt. Mặc định phục vụ series 'Cường mê AI' / '30 ngày tìm hiểu bạn AI' — giọng văn hài hước, gần gũi, kiểu tâm sự/chia sẻ với bạn bè, KHÔNG phải giọng giảng dạy/hướng dẫn khô khan, xuyên suốt ẩn dụ 'làm quen với AI giống như tìm hiểu người yêu'. Trigger: '/script-writer', 'viết kịch bản cho video AI', 'lên lời thoại để quay video về [chủ đề Claude/AI]', 'kịch bản ngày thứ N series tìm hiểu bạn AI'."
---

# Script Writer — Kịch bản cho series "30 ngày tìm hiểu bạn AI"

> Đây là skill viết LỜI THOẠI để user cầm quay, khác hẳn các skill `edit-style-*`
> (nhận footage/transcript CÓ SẴN rồi tạo blueprint dựng). Thứ tự dùng đúng của cả
> pipeline: **script-writer (skill này) → user tự quay theo kịch bản → `edit-style-*`
> (dùng transcript thật của bản quay) → HyperFrames build/render.**
>
> Không tự động gọi skill dựng video ở cuối — output của skill này LUÔN LÀ VĂN BẢN
> kịch bản, dừng lại ở đó trừ khi user nói rõ muốn bước tiếp theo.

---

## 0. Vì sao giọng văn là phần quan trọng nhất ở đây

Cấu trúc nhịp cắt (hook/tip-cycle/outro) đã có sẵn, đo đạc thật từ
`edit-style-nns/SKILL.md` mục 1 — phần đó tái dùng nguyên, không cần bịa lại.
Cái CHƯA có, và là lý do user tạo ra skill này, là **giọng văn**: user muốn nội dung
nghe như đang **tâm sự/chia sẻ** với một người bạn, không phải một người đang "dạy"
khán giả cách dùng AI. Nếu quên mất điều này, kịch bản viết ra vẫn đúng cấu trúc
nhưng sẽ SAI mục đích — nó sẽ đọc lên nghe như video hướng dẫn công nghệ thông
thường (rất nhiều kênh đã làm), không phải video mà user hình dung.

Ẩn dụ chủ đạo user chốt: **coi việc tìm hiểu/dùng AI (đặc biệt Claude) giống như
tìm hiểu một người yêu** — có giai đoạn làm quen, có lúc ngại ngùng, có lúc phát
hiện ra "ơ bạn này hiểu mình phết", có mâu thuẫn/thất vọng khi dùng sai cách, có
lúc gắn bó lâu dài. Đây KHÔNG phải một câu đùa dùng 1 lần ở hook rồi bỏ — ẩn dụ này
là khung xuyên suốt cả kịch bản mỗi tập, y như cấu trúc tip-cycle là khung xuyên
suốt cả cảnh quay.

---

## 1. Giọng văn DNA (bắt buộc áp cho mọi kịch bản viết ra)

| Khía cạnh | Làm | Tránh |
|---|---|---|
| Ngôi xưng | "mình", "tụi mình", nói thẳng với người xem như đang nhắn tin cho 1 người bạn | "các bạn", "quý vị", giọng MC/host trang trọng |
| Mở đầu mỗi tip/ý | Tối đa 1 câu dẫn ngắn rồi vào thẳng nội dung/prompt/kết quả — không kể lể tình huống dài trước khi cho xem cái hay | Liệt kê khô "Tiếp theo, bước 2..." **hoặc** dẫn chuyện lan man 2-3 câu trước khi vào nội dung thật |
| Ẩn dụ tình yêu | **Chỉ là gia vị điểm xuyết** — 1 câu ngắn, tự giễu, bật ra rồi đi tiếp ngay (vd chêm giữa câu: "...kiểu ghen tuông vô cớ luôn á" rồi qua ý khác) | Kéo ẩn dụ thành cả đoạn văn tình cảm/ngôn tình ("càng thật càng dễ thân", "thật sự lắng nghe mình nói") — đây là lỗi đã gặp thực tế (bản nháp Ngày 1 bị chê "sến súa"), tuyệt đối không lặp lại kiểu này |
| Hài hước | Tự trào (tự chọc mình từng dùng AI sai/ngại/quê), quan sát đời thường hài, twist bất ngờ ở cuối câu | Chọc cười gượng, joke không liên quan nội dung, hài kiểu chê bai người khác |
| Vai trò với người xem | Người đang CHIA SẺ trải nghiệm của mình, để người xem tự rút ra bài học | Người đang DẠY người xem phải làm gì ("bạn nên", "bạn phải", "hãy nhớ") |
| Prompt cụ thể | Vẫn phải đọc nguyên văn 1 câu prompt thật (để lên Prompt Card) — dẫn vào bằng nửa câu ngắn, không phải "Prompt cần dùng là:" | Giới thiệu prompt như 1 slide kỹ thuật tách rời khỏi mạch chuyện |
| Kết mỗi tập | 1 câu chốt ngắn (được phép có chút ẩn dụ) rồi tới CTA follow ngay | CTA khô đứng 1 mình, **hoặc** kéo dài đoạn cảm xúc trước CTA |

**Nguyên tắc trên hết, quan trọng hơn cả giọng văn: mỗi câu phải trả lời được
"viewer đang xem/học được cái gì HAY ngay lúc này"** — nếu 1 câu chỉ đang tả cảm
xúc/dẫn chuyện mà chưa cho viewer thấy nội dung cụ thể, cắt hoặc rút ngắn xuống
tối đa 1 câu. Kịch bản hay không phải kịch bản văn vẻ nhất, mà là kịch bản không
có câu nào thừa trước khi tới phần viewer thực sự muốn xem (xem thêm mục 4.2 về
cách mở Hook).

**Cách tự kiểm tra nhanh 1 đoạn vừa viết:** đọc to lên, tự hỏi 2 câu:
1. Nghe giống bạn bè kể chuyện hay giống tutorial/ngôn tình? (mục tiêu: bạn bè kể chuyện)
2. Nếu cắt bỏ câu này, viewer có mất đi 1 thông tin/hình ảnh cụ thể nào không? Nếu
   không mất gì (chỉ mất cảm xúc/không khí) — khả năng cao câu đó đang lan man, cân
   nhắc cắt.

---

## 2. Series "30 NGÀY TÌM HIỂU BẠN AI" — khung nội dung

Mượn đúng khung 1 mối quan hệ đang phát triển, chia thành 5 giai đoạn (không cứng
nhắc phải đúng 30 tập/30 ngày lịch — "30 ngày" là tên/khung cảm xúc của series, số
tập thật tuỳ user):

| Giai đoạn | Cảm xúc chủ đạo | Loại nội dung AI phù hợp |
|---|---|---|
| 1. Làm quen (những ngày đầu) | Tò mò, hơi ngại, thử vài câu bâng quơ xem "người ta" phản ứng sao | Cách mở đầu 1 cuộc chat, cách viết prompt đầu tiên, những câu hỏi "test thử" hay dùng |
| 2. Hẹn hò thật sự (bắt đầu dùng nghiêm túc) | Hào hứng, khám phá ra bạn ấy giỏi hơn mình tưởng | Các tính năng cụ thể (Projects, Artifacts, upload file...), prompt tips cho công việc thật |
| 3. Hiểu tính nhau (dùng quen tay) | Aha-moment, "ơ hoá ra phải nói kiểu này bạn mới hiểu đúng ý" | Kỹ thuật prompt nâng cao (context, ví dụ mẫu, chia nhỏ yêu cầu), so sánh cách hỏi dở vs hỏi hay |
| 4. Cãi nhau/hiểu lầm (khi dùng sai) | Bực, thất vọng, rồi vỡ lẽ lỗi tại mình chứ không phải tại AI | Các lỗi prompt phổ biến, ảo giác (hallucination), khi nào KHÔNG nên tin AI 100% |
| 5. Gắn bó lâu dài (thành thói quen) | Ấm áp, biết ơn, đã thành 1 phần quy trình làm việc/sống | Workflow tích hợp AI vào công việc hằng ngày, dùng AI như 1 "đồng đội" chứ không phải công cụ tra cứu |

Chi tiết ý tưởng từng "ngày" cụ thể (đã brainstorm sẵn để không phải nghĩ lại từ
đầu mỗi lần) nằm ở [references/series-30-ngay-tim-ban-ai.md](references/series-30-ngay-tim-ban-ai.md) — đọc file
đó khi user chỉ đưa "ngày thứ N" mà không nói rõ chủ đề, hoặc khi cần gợi ý chủ đề
tiếp theo.

---

## 3. Input cần có

1. **Chủ đề/ý tưởng ngắn** — bắt buộc. Có thể chỉ 1 câu (vd "cách dùng Claude
   Projects để nó nhớ ngữ cảnh dự án"), hoặc chỉ nói "ngày thứ 7" (khi đó tra
   `references/series-30-ngay-tim-ban-ai.md` để lấy chủ đề gợi ý cho ngày đó, xác
   nhận lại với user trước khi viết).
2. **Khuôn cấu trúc** (tuỳ chọn, mặc định tự chọn dựa theo chủ đề):
   - Chủ đề có 2-3 mẹo/tip rõ ràng → khuôn 3-tip của `edit-style-nns`.
   - Chủ đề liệt kê nhiều bước ngắn (4 trở lên) → khuôn N-step của dự án
     `hyperframes/buoc7-ai` (mỗi ý 1 step card gọn, không cần đầy đủ
     prompt+demo+payoff cho từng ý).
   - Chủ đề chỉ có 1 thông điệp/CTA duy nhất (không phải dạng liệt kê) → khuôn
     1-arc của dự án `hyperframes/hoc-ai`.
   Nếu không chắc, hỏi user thay vì tự ép chủ đề vào khuôn không hợp.
3. **Độ dài mục tiêu** (tuỳ chọn) — mặc định ~60-65s để khớp pattern 3 video đã
   làm trước đó trong project; user có thể yêu cầu dài/ngắn hơn.

Không cần audio/transcript ở bước này — đây là bước VIẾT TRƯỚC KHI QUAY, khác
`edit-style-*` (cần audio/transcript CỦA BẢN ĐÃ QUAY).

---

## 4. Thuật toán viết kịch bản

1. **Chọn giai đoạn trong hành trình tình yêu** khớp với chủ đề (bảng mục 2) —
   dùng để chọn 1 câu ẩn dụ điểm xuyết phù hợp, KHÔNG dùng để viết cả đoạn mở
   bài theo cảm xúc giai đoạn đó (xem lỗi "sến súa" đã ghi ở mục 1).
2. **Viết Hook (~5-8% thời lượng, tối đa 1-2 câu NGẮN) — đây là phần QUYẾT ĐỊNH
   viewer ở lại hay lướt qua, ưu tiên số 1 khi viết:**
   - **Đập thẳng vào việc, không tường thuật.** Câu đầu tiên phải LÀ nội dung
     hoặc 1 mệnh lệnh/tuyên bố trực tiếp, không phải câu dẫn kiểu "Đây là...",
     "Hôm đó mình...", "Đây là đúng câu mình gõ..." — bản thân cụm "đây là đúng
     câu mình gõ" đã là 1 vòng dẫn thừa, viewer chưa thấy gì cụ thể cho tới khi
     nghe hết câu đó.
   - Cách kiểm tra "đập thẳng" hay chưa: đọc câu đầu tiên và dừng lại — nếu
     TRONG câu đó đã có nội dung/prompt/con số/kết quả cụ thể thì đạt. Nếu câu
     đầu chỉ đang GIỚI THIỆU rằng sắp có nội dung ("đây là câu mình gõ", "để
     mình kể bạn nghe") thì chưa đạt, cắt câu giới thiệu, cho nội dung lên làm
     câu đầu luôn.
   - Ví dụ SAI (vẫn là tường thuật dù đã ngắn): "Đây là đúng câu mình gõ vào
     Claude lần đầu tiên — xong nó hỏi ngược lại làm mình khựng luôn." Ví dụ
     ĐÚNG (đập thẳng, không giới thiệu): "Gõ đúng câu này vào Claude đi, nó hỏi
     ngược lại mình liền cho mà xem." — vào thẳng bằng động từ mệnh lệnh, prompt
     coi như đã bắt đầu ngay trong hook thay vì đợi qua Prompt Card mới lộ diện.
   - Ẩn dụ tình yêu (nếu dùng ở hook) chỉ 1 cụm 2-3 chữ chêm cuối câu, không bao
     giờ chiếm cả câu hay đứng làm câu mở đầu.
   - Không cần câu bắc cầu riêng trước Prompt Card nữa nếu hook đã trực tiếp
     nhắc tới prompt — Prompt Card lúc đó chỉ là "phóng to" đúng câu vừa nói.
3. **Viết thân bài theo khuôn đã chọn** (mục 3.2) — với mỗi tip/step:
   - Câu dẫn (talking head): 1-2 câu cảm xúc/tình huống trước khi vào nội dung.
   - Câu prompt cụ thể (để lên Prompt Card, nếu khuôn có phần này): viết NGUYÊN
     VĂN câu lệnh thật sự dùng được, đọc tự nhiên như đang gõ trước mặt người xem
     ("mình gõ thế này nè: ...") — không viết prompt mơ hồ/không dùng được thật.
   - Câu kết quả/demo (nếu khuôn có): mô tả AI phản hồi ra sao, có thể chèn 1 câu
     ngạc nhiên/hài kiểu aha-moment.
   - Câu payoff: chốt lợi ích NHƯNG lồng qua lăng kính quan hệ (vd "đúng kiểu bạn
     nói cho mình nghe hết chứ không giấu bài" thay vì "tiết kiệm 50% thời gian").
4. **Viết Outro**: 1 câu chốt cảm xúc/liên hệ tình yêu → CTA follow, dẫn vào tập
   tiếp theo trong series nếu hợp (vd "ngày mai tụi mình học tiếp cách...").
5. **Ước lượng timing**: tốc độ nói tự nhiên tiếng Việt đo được từ transcript thật
   của 3 video trước trong project là **~2.2-2.8 âm tiết/giây** (chậm hơn ở câu
   prompt được đọc chậm/nhấn — lấy cận dưới ~2.0-2.2 cho các câu đó). Đếm âm tiết
   mỗi câu, chia tốc độ, cộng dồn ra timestamp ước lượng cho từng đoạn — LUÔN ghi
   rõ đây là ước lượng để quay/dựng tham khảo, số thật sẽ theo transcript sau khi
   quay xong.
6. **Ghi chú quay (quay note)** cho mỗi đoạn — vì kịch bản này còn phải hướng dẫn
   CÁCH QUAY, không chỉ nội dung nói:
   - Đoạn nào cần dừng 1 nhịp (khoảng lặng ngắn ~0.3-0.5s) trước/sau để dễ tìm
     điểm cắt khi dựng — thường là ranh giới giữa các tip/step.
   - Đoạn nào nên đổi tông giọng/tốc độ (vd chậm lại rõ ràng khi đọc prompt, để
     karaoke word-highlight sau này dễ khớp).
   - Đoạn nào nên nhìn thẳng cam vs được phép nhìn lệch (nếu quay có góc phụ dùng
     cho PiP).

---

## 5. Output — cấu trúc cố định

Luôn xuất đủ các phần sau, theo đúng thứ tự:

### A. Tên tập + vị trí trong series
Vd: "Ngày 7 — Khi bạn AI không hiểu ý mình (và hoá ra lỗi tại mình)". Nếu không rõ
số ngày, để trống phần số và chỉ ghi tên chủ đề.

### B. Kịch bản đầy đủ theo đoạn, có timestamp ước lượng

`| Thời điểm (ước lượng) | Đoạn | Lời thoại đầy đủ | Quay note |`

Đủ từ Hook → từng tip/step → Outro, đúng khuôn đã chọn ở mục 3.

### C. Danh sách câu prompt sẽ lên Prompt Card
Liệt kê riêng, nguyên văn, để dễ đối chiếu khi dựng — mỗi câu kèm timestamp sẽ đọc.

### D. Gợi ý B-roll/demo cần chuẩn bị trước khi quay
Nếu kịch bản có nhắc tới 1 kết quả demo cụ thể (vd 1 đoạn chat thật với Claude),
ghi rõ cần chuẩn bị/chụp màn hình gì trước, để lúc dựng có sẵn không phải tìm gấp.
Nếu kịch bản nêu TÊN 1 công cụ/thương hiệu cụ thể (Claude, ChatGPT, Gemini,
DeepSeek...) và khuôn cần 1 Tool Card hiện logo, ghi chú là đã có sẵn logo trong
`SON_AI_VIDEO/shared-sources/brand-logos/` — không cần tự vẽ/tìm logo mới.

### E. Ghi chú bàn giao cho `edit-style-*`
1 câu nhắc: sau khi quay xong theo kịch bản này, đưa file quay + transcript thật
vào `/edit-style-nns` (hoặc style tương ứng) để ra blueprint dựng — timestamp
ở mục B là ước lượng, blueprint dựng sau sẽ dùng timestamp thật.

---

## 6. Checklist QC trước khi giao kịch bản

```
[ ] 1. Đọc to toàn bộ kịch bản — nghe như tâm sự/chia sẻ, KHÔNG nghe như hướng dẫn/tutorial
[ ] 2. Ẩn dụ tình yêu xuất hiện tự nhiên, làm rõ cảm xúc/trải nghiệm thật — không gượng ép
[ ] 3. Có ít nhất 1 chi tiết hài/tự trào, không phải hài "cho có"
[ ] 4. Mọi câu prompt trong mục C là prompt THẬT dùng được, không mơ hồ
[ ] 5. Timing ước lượng cộng dồn khớp tổng thời lượng mục tiêu (mục 3.3)
[ ] 6. Cấu trúc khớp đúng khuôn đã chọn (3-tip / N-step / 1-arc) — không lẫn lộn giữa khuôn
[ ] 7. Outro có câu chốt cảm xúc TRƯỚC CTA, không CTA khô đứng một mình
[ ] 8. Không trùng chủ đề/góc tiếp cận với các tập đã liệt kê trong SCRIPT_LOG.md (mục 7)
```

---

## 7. Nhật ký series — tránh trùng ý tưởng

Sau khi giao 1 kịch bản cho user, thêm 1 dòng vào
`SON_AI_VIDEO/SCRIPT_LOG.md` (tạo file này nếu chưa có, ở thư mục gốc project):

`| Ngày/số tập | Giai đoạn | Chủ đề | Ngày viết |`

Trước khi viết kịch bản mới, đọc file này để không lặp lại đúng góc tiếp cận đã
dùng — nếu chủ đề mới trùng ý với 1 tập cũ, báo cho user và hỏi có muốn đổi góc
tiếp cận khác hay vẫn tiếp tục (vd làm phần 2 của cùng chủ đề).

---

## 8. Demo giao diện thật — KHÔNG làm ở đây, chỉ đánh dấu

Nếu kịch bản có đoạn yêu cầu viewer làm A→B trên giao diện Claude thật, việc này
chỉ cần **đánh dấu rõ trong mục D (Chuẩn bị trước khi quay)** — ghi lại đúng
prompt/thao tác cần demo. Việc THỰC SỰ thao tác trên giao diện thật để lấy
ảnh/luồng demo (dùng Claude trong Chrome thật của user) thuộc trách nhiệm của
skill dựng (`edit-style-nns` mục "Demo Screenshot"/B-roll), vì đó là nơi xử
lý asset thật cho blueprint — script-writer chỉ viết văn bản, không cầm trình
duyệt đi thao tác. Không lặp lại quy trình đó ở đây, chỉ trỏ sang.

---

*Skill này chỉ viết kịch bản (văn bản) — không tự quay footage người thật, không
tự quay demo giao diện, không tự dựng, không tự gọi skill edit-style hay
HyperFrames tiếp theo. Chờ user quay xong và mang transcript thật quay lại mới
sang bước dựng.*
