---
name: bug-two-attempt-rule
description: "Bugs - scan for all similar cases, group by root cause, fix once per group; max 2 attempts (shared across machines) then stop and propose a new direction"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7e681fd1-276f-4db7-a3f3-f6544d001dfb
  modified: 2026-10-28T00:29:59.280Z
---

Every bug goes into the shared bug book on Drive `LOUGA_WORKSPACE_MEDIA/00_SYSTEM/SO-BUG.md`. Before fixing: search everywhere for the same bug, group by root cause, fix the whole group at once. Each fix attempt is one "Lần N" line, counted across BOTH machines/all sessions. After attempt 2 still fails → stop (no attempt 3), mark `[DỪNG - XEM LẠI HƯỚNG]`, write a proposal (current approach, why it failed, 2–3 alternatives, recommendation) and wait for the user.

**Why:** 2026-10-28 the user said that every day both Claude sessions find bugs but never finish them (e.g. snap_cuts tried 4 ways, still wrong).

**How to apply:** Read SO-BUG.md before touching any bug; full rule in CLAUDE.md section "XỬ LÝ BUG — GIỚI HẠN 2 LẦN". Keep the book on G: ([[no-local-c-drive-files]]).
