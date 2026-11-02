---
name: no-local-c-drive-files
description: "Work only on G: (Google Drive): never C:, Remotion projects on G: too; D: holds only git repo, skill assets, disposable render cache"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7e681fd1-276f-4db7-a3f3-f6544d001dfb
  modified: 2026-11-02T02:05:00.483Z
---

Read and write work files only on G: (`G:/My Drive/LOUISYOGA_WORKSPACE/...`). Nothing on C: — not even the Claude scratchpad. Since 2026-11-02 Remotion projects also live on G: (`05_VIDEO_PROJECTS/<dự án>/edit/<NN>/project`); D: only keeps the git repo, skill assets and the disposable render cache `D:/LOUGA_CACHE` (see [[drive-offline-read-direct]]).

**Why:** G: is what syncs between their machines. 2026-10-27 the user was upset about 2.2 GB of backups in the C: scratchpad; 2026-11-02 the other machine's Claude could not continue because projects were only on D:.

**How to apply:** Temp/preview files go in the hồ sơ folder on G: (`edit/<NN>/work/`). No local backups before editing a Drive file. Drive needs time to sync: after large writes to G:, wait for the user to say sync finished before testing. If a step truly needs local disk, say so first.
