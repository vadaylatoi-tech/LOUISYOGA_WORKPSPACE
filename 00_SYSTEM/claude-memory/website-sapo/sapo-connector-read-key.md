---
name: sapo-connector-read-key
description: How to read a single Sapo theme asset via the louisyoga MCP connector (get_theme_asset is broken)
metadata:
  node_type: memory
  type: reference
  originSessionId: d56b120b-45c4-41d2-8bad-0ffdf7e031ab
  modified: 2026-10-17T08:10:28.635Z
---

On 2026-10-17, `get_theme_asset` and `sapo_request` with `asset[key]` returned the whole (truncated ~90k) asset listing instead of the file. What works: `sapo_request` GET `themes/<id>/assets.json` with query `{"key": "<key>"}` returns `asset.value`. CSS/JS can also be fetched/hashed from the CDN `public_url` with curl. Write = PUT same path with `{"asset":{"key","value"}}`, then compare CDN sha256 with the local file. Re-verified 2026-10-17 (second session): still broken. Note the layout folder is `layouts/` (e.g. `layouts/theme.bwt`), not `layout/`; a wrong key gives HTTP 404.

No python/node on this machine; Windows.Data.Pdf via PowerShell can render the design PDFs to PNG.
Upload ảnh nhỏ (19/10): PUT assets.json `{"asset":{"key":"assets/x.png","base64":"..."}}` chạy được tới ~12 KB base64. Phải chép nguyên chuỗi base64 vào lệnh → dễ sai 1 ký tự (đã gặp với favicon 180px): LUÔN so sha256 file CDN với file gốc sau khi ghi, sai thì `cmp -l` tìm byte lệch rồi ghi lại. Favicon theme: assets/ly-favicon-32.png (tab, chỉ bông sen) + assets/favicon.png (180, apple-touch, có chữ); sao lưu zz-backup-*-20261019.png. Tạo ảnh bằng PowerShell System.Drawing (scratchpad fav.ps1).
