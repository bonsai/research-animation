#!/usr/bin/env bash
set -euo pipefail

# research-animation PoC
# SD 1.5 -> frame pool -> random 2-7 fps playback
#
# Usage:
#   ./run.sh
#   ./run.sh 100
#
# SD installation: /home/bons/.sd

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SD_DIR="${HOME}/.sd"
SD_URL="${SD_URL:-http://127.0.0.1:7860}"
COUNT="${1:-10}"
WIDTH=128
HEIGHT=128
STEPS=12
CFG=7

cd "$ROOT"

echo "=== research-animation ==="
echo "SD       : $SD_DIR"
echo "SD API   : $SD_URL"
echo "Frames   : $COUNT"
echo "Size     : ${WIDTH}x${HEIGHT}"
echo "FPS      : 2-7"
echo

echo "[1/4] checking SD API..."
if ! curl -fsS "${SD_URL}/sdapi/v1/sd-models" >/dev/null 2>&1; then
    echo
    echo "SD APIが起動していません。"
    echo
    echo "別ターミナルで:"
    echo "  cd ${SD_DIR}"
    echo "  ./webui.sh --api --listen"
    echo
    exit 1
fi
echo "SD API: OK"

echo
echo "[2/4] generating frames..."
python3 generate_frames.py \
    --sd-url "$SD_URL" \
    --count "$COUNT" \
    --width "$WIDTH" \
    --height "$HEIGHT" \
    --steps "$STEPS" \
    --cfg "$CFG" \
    --prompt "a tiny hand-drawn animation frame"

echo
echo "[3/4] creating random playback..."
python3 playback.py \
    --frames ../frames \
    --min-fps 2 \
    --max-fps 7

echo
echo "[4/4] done."
echo "Frame Pool: ${ROOT}/../frames"
echo "Playback:   ${ROOT}/../frames/playback.json"
echo "=== complete ==="
