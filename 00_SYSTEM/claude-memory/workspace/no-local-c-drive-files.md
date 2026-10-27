---
name: no-local-c-drive-files
description: "Never write work files/backups/previews to C: (incl. Claude scratchpad) — read and write media only on G: (Google Drive)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7e681fd1-276f-4db7-a3f3-f6544d001dfb
  modified: 2026-10-27T14:13:15.085Z
---

Read and write work files only on G: (`G:/My Drive/LOUISYOGA_WORKSPACE/...`). Do NOT put copies, backups, previews, contact sheets or temp scripts on C: — not even in the Claude scratchpad. D: stays only for the git repo / skill assets / Remotion projects (see [[drive-offline-read-direct]]).

**Why:** 2026-10-27 the user was upset that I made covers for 29 videos while keeping 2.2 GB of backups and preview images in the C: scratchpad. G: is what syncs between their machines, so anything on C: is invisible to the other machine and goes out of sync.

**How to apply:** Temp/preview files go in the project's hồ sơ folder on G: (e.g. `05_VIDEO_PROJECTS/<dự án>/edit/<NN>/work/` or `00_SYSTEM/` on Drive). Don't make local backups before editing a Drive file; Drive's version history keeps the old version (say so to the user). If a step truly needs local disk, ask first.
