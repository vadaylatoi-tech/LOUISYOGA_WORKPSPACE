# Khôi phục project Remotion video 05-lau-tham-moi-ngay trên máy khác

Git chỉ giữ mã nguồn (`src/`, `package.json`, cấu hình). `public/` (khoảng 300 MB) không lên git:
- Asset chung (font, SFX, nhạc, ảnh Louis, phim thương hiệu) lấy lại từ skill `louisyoga-reel-style1` (asset của skill tự tải từ Drive lúc mở phiên).
- Footage đã cắt: `LOUGA_WORKSPACE_MEDIA/05_VIDEO_PROJECTS/2026-10_san-sale/edit/05-lau-tham-moi-ngay/work/clean.mp4` trên Drive.

```bash
SKILL="D:/LOUGA_WORKSPACE/04_AI_SKILLS/louisyoga-reel-style1-package/louisyoga-reel-style1"
M="<o Drive>:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA/05_VIDEO_PROJECTS/2026-10_san-sale/edit/05-lau-tham-moi-ngay"
cd "D:/LOUGA_WORKSPACE/05_VIDEO_PROJECTS/2026-10_san-sale/edit-05-lau-tham-moi-ngay/project"
# project da co src/ -> new_project chi chep lai asset chung vao public/ + footage, khong dong vao src/
python "$SKILL/scripts/new_project.py" --dest . --clean "$M/work/clean.mp4" --install
npx remotion studio
```

Hồ sơ làm việc (work/, báo cáo, contact sheet) ở `edit/05-lau-tham-moi-ngay/` trên Drive. Bản final: `10_FINAL_DELIVERABLES/2026-10-27_san-sale/`.
Render lại bản sửa sau khi đã giao → `render_all.py` không `--replace` (ra `_v2`).
