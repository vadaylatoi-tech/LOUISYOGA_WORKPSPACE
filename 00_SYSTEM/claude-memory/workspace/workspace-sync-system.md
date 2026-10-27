---
name: workspace-sync-system
description: How Louis Yoga workspace syncs across machines (GitHub repo D:/LOUGA_WORKSPACE + Drive log + SessionStart hook + linked skills)
metadata:
  node_type: memory
  type: project
  originSessionId: 53e115d5-0ed6-4c02-be7f-3aee102ae3d9
  modified: 2026-10-26T14:51:26.370Z
---

Set up 2026-10-26 at the user's request so Claude sessions on any machine share context:
- Repo `D:/LOUGA_WORKSPACE` (github.com/vadaylatoi-tech/LOUISYOGA_WORKPSPACE) holds code/skills/rules; Drive `G:/My Drive/LOUISYOGA_WORKSPACE/LOUGA_WORKSPACE_MEDIA` holds media, skill assets (same `04_AI_SKILLS/...` paths) and the work log `00_SYSTEM/NHAT-KY-LAM-VIEC.md`.
- `~/.claude/settings.json` SessionStart hook runs `00_SYSTEM/sync/dong_bo.py session-start` (git pull, asset sync, last 3 log entries, injects repo CLAUDE.md when the session is opened outside the repo — e.g. in the G: folder).
- All 14 skills in `~/.claude/skills/` are junctions into the repo: `louisyoga-reel-style1`, `duycongeditvideo-buoc1` (in their `04_AI_SKILLS/*-package/`) and the 12 `nns-*`/`edit-*`/`extract-edit-style`/`script-writer` (in `04_AI_SKILLS/video-skills/`, added 2026-10-27). Heavy assets (onnx, ttf, mp3) are gitignored and synced via Drive. Old copies in `~/.claude/skills-backup/`. `cai-dat` also seeds memory from `00_SYSTEM/claude-memory/workspace/`.
- New machine: clone repo to D:/LOUGA_WORKSPACE, run `00_SYSTEM/setup/CAI-DONG-BO.bat`.

**Why:** user switches machines and wants the next Claude to know what was just done and use the same skill version.

**How to apply:** at the end of work run `dong_bo.py ghi-nhat-ky --viec ... --file ... --con-lai ...`; commit + push any repo change (no git identity on this machine → `-c user.name=vadaylatoi-tech -c user.email=vadaylatoi-tech@users.noreply.github.com`). Related: [[final-video-location]]
