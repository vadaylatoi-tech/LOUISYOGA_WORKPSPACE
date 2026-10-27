---
name: drive-offline-read-direct
description: "Google Drive G: is set to offline (files cached locally) — read media straight from G:, don't copy to D:"
metadata:
  node_type: memory
  type: user
  originSessionId: 0d18914e-8001-45a0-bc67-108dc80397b2
  modified: 2026-10-27T01:28:13.445Z
---

Anh Hùng đã bật chế độ offline cho Google Drive ở G: (2026-10-27), nên media trong `G:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA/` (video cuts, hồ sơ, brief) đã nằm sẵn trên ổ máy.

**Why:** Phiên 2026-10-27 em chép 12 video san-sale từ G: về D: cho "nhanh" — thừa, và bản chép có thể lệch khi video trên Drive được sửa.

**How to apply:** Đọc video/hồ sơ trực tiếp từ đường dẫn G:, không chép về D:. Chỉ những thứ bắt buộc ở D: mới để ở D: (repo code/skill, asset skill do dong_bo.py đồng bộ, project Remotion có node_modules). Liên quan [[workspace-sync-system]], [[final-video-location]].
