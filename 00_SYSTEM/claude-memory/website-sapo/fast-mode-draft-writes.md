---
name: fast-mode-draft-writes
description: "Louis Yoga workflow since 2026-10-17 — old kits banned; handoff doc is \"4. Hiện trạng/CLAUDE.md\"; back up on Sapo via source_key before each write"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 78bfac4f-22b4-4c7d-a90e-4927e139b20f
  modified: 2026-10-17T08:10:23.470Z
---

Since 2026-10-17 anh Công has banned both old kits (`louis-yoga-claude-kit`, `Louis-Yoga-Claude-Code-Kit`). Don't read them, use them or ask for them, and that includes their Git, backups/ folder and skills. The only handoff doc is `4. Hiện trạng/CLAUDE.md`, and the source of truth is the theme on Sapo. Work one page at a time on draft theme 1170160. Before each write, back up on Sapo itself: PUT `themes/1170160/assets.json` with `{"asset":{"key":"snippets/zz-backup-<name>-<yyyymmdd>.bwt" or "assets/zz-backup-…css","source_key":"<original key>"}}`. This copies on the server without sending the file content, so it saves tokens. Keep reports short and avoid side documents.

**Why:** the user wants token-lean work, but explicitly said not to save tokens by skipping theme verification, reading before writing, backups or functional checks.

**How to apply:** never write or publish live theme 1170134. Built-in browser preview at `louisyoga.vn/<path>?previewThemeId=1170160` works without login (verified 2026-10-17, even at 390px). Don't put real items in the cart; to see a filled cart, inject sample DOM. Related: [[sapo-connector-read-key]].
