#!/usr/bin/env bash
set -euo pipefail

# research-animation PoC
# SD 1.5 -> frame pool -> random 2-7 fps playback
#
# Usage:
#   ./run.sh
#   ./run.sh 100
#
# The SD installation is external to this repository.
# Default: /home/bons/.sd

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SD_DIR="${SD_DIR:-${HOME}/.sd}"
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

# --------------------------------------------------
# 1. SD API / installation diagnostics
# --------------------------------------------------

echo "[1/4] checking SD API..."
echo "GET ${SD_URL}/sdapi/v1/sd-models"

echo

if curl -fsS --connect-timeout 3 --max-time 10 \
    "${SD_URL}/sdapi/v1/sd-models"; then
    echo
    echo "SD API: OK"
else
    echo
    echo "SD API: NOT READY"
    echo
    echo "Installation: ${SD_DIR}"

    if [[ ! -d "$SD_DIR" ]]; then
        echo "ERROR: SD directory does not exist: $SD_DIR"
        exit 1
    fi

    echo "SD directory exists. Detecting launcher..."

    WEBUI=""
    for candidate in \
        "$SD_DIR/webui.sh" \
        "$SD_DIR/stable-diffusion-webui/webui.sh" \
        "$SD_DIR/sd.next/webui.sh" \
        "$SD_DIR/SD.Next/webui.sh"; do
        if [[ -f "$candidate" ]]; then
            WEBUI="$candidate"
            break
        fi
    done

    if [[ -n "$WEBUI" ]]; then
        echo "Found WebUI launcher: $WEBUI"
        echo
        echo "Start it with:"
        echo "  cd $(dirname "$WEBUI")"
        echo "  ./$(basename "$WEBUI") --api --listen"
    else
        echo "No webui.sh found under ${SD_DIR} (depth <= 4)."
        echo
        echo "Detected candidate files:"
        find "$SD_DIR" -maxdepth 4 -type f \( \
            -name 'webui.sh' -o \
            -name 'launch.py' -o \
            -name 'main.py' -o \
            -name 'server.py' \
        \) -print 2>/dev/null | head -30 || true
        echo
        echo "Model files:"
        find "$SD_DIR" -type f \( \
            -name '*.safetensors' -o \
            -name '*.ckpt' \
        \) -print 2>/dev/null | head -20 || true
        echo
        echo "The repository only needs an SD API endpoint."
        echo "Set SD_URL if the API runs elsewhere, for example:"
        echo "  SD_URL=http://127.0.0.1:7861 ./run.sh 10"
    fi

    exit 1
fi

# --------------------------------------------------
# 2. Frame Pool
# --------------------------------------------------

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

# --------------------------------------------------
# 3. Random playback
# --------------------------------------------------

echo
echo "[3/4] creating random playback..."
python3 playback.py \
    --frames ../frames \
    --min-fps 2 \
    --max-fps 7

# --------------------------------------------------
# 4. Done
# --------------------------------------------------

echo
echo "[4/4] done."
echo "Frame Pool: ${ROOT}/../frames"
echo "Playback:   ${ROOT}/../frames/playback.json"
echo "=== complete ==="
