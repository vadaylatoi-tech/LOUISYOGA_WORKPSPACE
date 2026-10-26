# Skill edit video — Phong cách 1 Louis Yoga

Bộ skill cho **Claude Code** dựng video ngắn talking-head tiếng Việt (TikTok / Reels / Shorts 9:16) đúng phong cách
đã duyệt ở bản "Thảm càng dày càng tốt? Chưa chắc!" (v4):
- hình tràn khung, zoom giấu mối cắt, B-roll phim thương hiệu;
- đồ hoạ hồng + vàng gold, caption karaoke;
- hook đập mạnh, SFX vừa đủ;
- giọng rõ và ấm, nhạc nhẹ, chuẩn −14 LUFS.

Bộ này **tự đủ**: đã có script, template Remotion, model dò mặt, font, SFX, nhạc, ảnh sản phẩm và B-roll. Chép sang máy
khác hoặc tài khoản khác đều dùng được, không cần các skill cũ.

## Trong thư mục có gì

```
Skilleditvideo_phongcach1_louisyoga/
├── HUONG-DAN-CAI-DAT.md        ← file này
├── PROMPT-BAT-DAU.txt          ← prompt copy-dán để bắt đầu
├── CAI-DAT-WINDOWS.bat         ← cài 1 chạm (Windows)
├── cai-dat-mac-linux.sh        ← cài 1 chạm (macOS/Linux)
└── louisyoga-reel-style1/      ← CHÍNH LÀ SKILL (chép thư mục này vào .claude/skills/)
    ├── SKILL.md                ← quy trình + luật cứng
    ├── references/             ← phong cách hình, SFX & âm thanh, lệnh kỹ thuật, QC, lịch sử góp ý, mốc B-roll
    ├── scripts/                ← preflight, transcribe, analyze_pauses, cut_words, track (mặt), gen_data,
    │                              new_project, process_voice, measure_sfx, render_all, mix_stems, contact_sheet
    ├── remotion-template/      ← project Remotion mẫu: src/kit (thành phần đồ hoạ) + src/reel/Reel.tsx (bản v4)
    ├── assets/                 ← det_10g.onnx, fonts, sfx (11 tiếng), music, brand (logo, ảnh thảm), broll (phim 92s)
    └── examples/reel3/         ← bảng cắt, fixes, báo cáo và video v4 đã duyệt để tham chiếu
```

## Máy cần có

| thứ | cài thế nào |
|---|---|
| Claude Code (CLI, app desktop hoặc extension VS Code) | https://claude.com/claude-code |
| Python 3.9+ | https://www.python.org/downloads/ (Windows: tick "Add to PATH") |
| ffmpeg bản full | Windows: `winget install --id Gyan.FFmpeg -e` · macOS: `brew install ffmpeg` |
| Node.js 20+ (LTS) | https://nodejs.org |
| Mạng Internet | lần đầu tải model Whisper (~1,5 GB) và gói Remotion (npm) |

GPU NVIDIA thì tốt nhưng không bắt buộc: chép lời bằng CPU vẫn chạy, chỉ chậm hơn.

## Cài đặt (5 phút)

**Cách 1: cài 1 chạm**
1. Chép cả thư mục `Skilleditvideo_phongcach1_louisyoga` sang máy mới (USB, Google Drive, file zip…).
2. Windows: nháy đúp `CAI-DAT-WINDOWS.bat`. macOS/Linux: `sh cai-dat-mac-linux.sh`.
3. Script sẽ:
   - chép skill vào `~/.claude/skills/louisyoga-reel-style1`;
   - cài thư viện Python;
   - chạy kiểm tra máy.
   Thấy dòng **"DAY DU. CHAY DUOC ROI."** là xong.
4. Đóng hẳn rồi mở lại Claude Code.

**Cách 2: thủ công**
- Chép thư mục `louisyoga-reel-style1` vào:
  - Windows: `C:\Users\<tên>\.claude\skills\`
  - macOS/Linux: `~/.claude/skills/`
- Chạy: `python -m pip install faster-whisper numpy onnxruntime Pillow "av>=11,<16"`
- Kiểm tra: `python ~/.claude/skills/louisyoga-reel-style1/scripts/preflight.py`

Chỉ muốn dùng trong 1 project? Chép vào `<project>/.claude/skills/` thay vì thư mục người dùng.

**Tài khoản Claude khác trên cùng máy:** skill nằm trong thư mục người dùng của máy, nên đăng nhập tài khoản nào cũng
dùng được. **Máy khác:** lặp lại các bước cài ở trên.

**claude.ai (bản web):** có thể nén thư mục `louisyoga-reel-style1` thành zip rồi tải lên mục Skills của claude.ai.
Tuy nhiên bước dựng cần ffmpeg, Node và Remotion chạy trên máy, nên **nên dùng Claude Code** để ra video hoàn chỉnh.

## Bắt đầu dùng

Mở Claude Code ở thư mục bất kỳ, gõ `/louisyoga-reel-style1` rồi dán prompt trong `PROMPT-BAT-DAU.txt`.
Claude sẽ:
1. Kiểm tra máy.
2. Chép lời và nghiên cứu nội dung.
3. **Đưa anh bảng cắt và ý tưởng để duyệt.**
4. Dựng, mix âm, kiểm tra chất lượng.
5. Giao video + báo cáo.

## Lưu ý bản quyền

- Nhạc "Inspired" – Kevin MacLeod, CC BY 4.0. **Phải ghi** trong caption bài đăng:
  `Music: "Inspired" – Kevin MacLeod (incompetech.com), CC BY 4.0`
- Ảnh `foam_mat.jpg`: "Yoga mat.jpg" của Gausanchennai trên Wikimedia Commons, CC BY-SA 4.0 (ghi nguồn khi dùng).
- Font Montserrat: SIL OFL. Remotion miễn phí cho cá nhân và công ty ≤ 3 người; lớn hơn cần mua license (remotion.dev/license).
- 11 file SFX lấy từ thư viện của bộ skill gốc, không ghi license. Nếu chạy quảng cáo thương mại, nên thay bằng tiếng có license rõ.
- Logo, ảnh sản phẩm và phim thương hiệu thuộc Louis Yoga, chỉ dùng cho nội dung của Louis Yoga.
