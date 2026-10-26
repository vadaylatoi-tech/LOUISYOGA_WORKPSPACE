#!/usr/bin/env sh
# Cai skill "louisyoga-reel-style1" cho Claude Code tren macOS / Linux.
# Chep skill vao ~/.claude/skills/ (dung cho moi project tren may), cai thu vien Python, kiem tra may.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/louisyoga-reel-style1"
DST="$HOME/.claude/skills/louisyoga-reel-style1"
[ -f "$SRC/SKILL.md" ] || { echo "[LOI] khong thay $SRC/SKILL.md"; exit 1; }

echo " 1/3  Chep skill -> $DST"
mkdir -p "$HOME/.claude/skills"
cp -R "$SRC/." "$DST/"

echo " 2/3  Cai thu vien Python"
python3 -m pip install --upgrade faster-whisper numpy onnxruntime Pillow "av>=11,<16" || echo "[CANH BAO] pip loi"

echo " 3/3  Kiem tra may"
python3 "$DST/scripts/preflight.py" || true

echo
echo " XONG. Mo lai Claude Code roi go: /louisyoga-reel-style1   (prompt mau: PROMPT-BAT-DAU.txt)"
