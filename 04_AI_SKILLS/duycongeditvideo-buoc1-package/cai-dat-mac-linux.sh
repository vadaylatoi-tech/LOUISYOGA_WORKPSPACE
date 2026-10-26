#!/bin/sh
# Cai skill Duycongeditvideo_Buoc1 cho Claude Code (moi du an tren may nay)
DIR="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/duycongeditvideo-buoc1"
mkdir -p "$DEST" && cp -R "$DIR/duycongeditvideo-buoc1/." "$DEST/" && echo "  Da chep skill vao: $DEST"
python3 -m pip install -q faster-whisper numpy
echo "  Chua co ffmpeg: macOS 'brew install ffmpeg' | Ubuntu 'sudo apt install ffmpeg'"
python3 "$DEST/scripts/preflight.py"
