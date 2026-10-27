# Khôi phục project Remotion video 01 trên máy khác

Git chỉ giữ mã nguồn (`src/`, `package.json`, cấu hình). Asset trong `public/` (footage, B-roll, SFX, nhạc, font, ảnh — 124 MB) nằm trên Drive:

`LOUGA_WORKSPACE_MEDIA/05_VIDEO_PROJECTS/2026-10_san-sale/edit/01-lau-tham-bang-con/remotion-public/`

```bash
cd "D:/LOUGA_WORKSPACE/05_VIDEO_PROJECTS/2026-10_san-sale/edit-01-lau-tham-bang-con/project"
cp -r "<o Drive>:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA/05_VIDEO_PROJECTS/2026-10_san-sale/edit/01-lau-tham-bang-con/remotion-public/." public/
npm ci
npx remotion studio
```

Hồ sơ làm việc (work/, báo cáo, contact sheet) ở cùng thư mục `edit/01-lau-tham-bang-con/` trên Drive. Bản final: `10_FINAL_DELIVERABLES/2026-10-26_san-sale/`.
