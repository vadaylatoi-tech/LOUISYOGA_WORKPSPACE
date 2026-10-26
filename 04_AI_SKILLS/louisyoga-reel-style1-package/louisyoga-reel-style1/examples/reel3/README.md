# Ví dụ: reel "Thảm càng dày càng tốt? Chưa chắc!" (bản v4 — đã duyệt)

- Video thô: `Video ngắn - thảm yoga/05 - Thảm càng dày càng tốt - chưa chắc.mp4` (1440×2560, 65,4 s).
- `cuts.json` — 11 đoạn đã bỏ (giây file gốc) → 54,3 s.
- `fixes.json` — sửa thuật ngữ ASR, bỏ 3 từ thừa, thêm 2 từ bị rơi ở mối cắt (chỉ số tính trên clean.words.json).
- `LouisYoga_ThamCangDay_Reel_v4_DA-DUYET.mp4` — bản chủ thương hiệu chốt; `v4_contact_sheet.jpg` — 1 khung/giây.
- `BAO-CAO-REEL-3-lich-su-4-phien-ban.md` — báo cáo đầy đủ v1→v4 (vì sao từng thay đổi).
- Code dựng: chính là `remotion-template/src/reel/Reel.tsx` + `src/reel/data.ts` của template.

Chạy lại từ đầu bằng skill (kiểm chứng đã làm khi đóng gói): cùng cuts/fixes → data.ts trùng 100% bản gốc.
