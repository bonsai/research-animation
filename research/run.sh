#!/usr/bin/env bash
set -euo pipefail

# research-animation PoC
# SD 1.5 (local Diffusers model) -> frame pool -> random 2-7 fps playback
#
# Usage:
#   ./run.sh
#   ./run.sh 100
#
# The SD model is external to this repository.
# Default model root: /home/bons/.sd/sd15_model

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SD_DIR="${SD_DIR:-${HOME}/.sd}"
MODEL_DIR="${MODEL_DIR:-${SD_DIR}/sd15_model}"
COUNT="${1:-10}"
WIDTH=128
HEIGHT=128
STEPS=12
CFG=7

cd "$ROOT"

echo "=== research-animation ==="
echo "SD       : $SD_DIR"
echo "Model    : $MODEL_DIR"
echo "Frames   : $COUNT"
echo "Size     : ${WIDTH}x${HEIGHT}"
echo "FPS      : 2-7"
echo

# --------------------------------------------------
# 1. Local SD model diagnostics
# --------------------------------------------------

echo "[1/4] checking local SD 1.5 model..."

if [[ ! -d "$MODEL_DIR" ]]; then
    echo "ERROR: model directory not found: $MODEL_DIR"
    exit 1
fi

if [[ ! -f "$MODEL_DIR/v1-5-pruned-emaonly.safetensors" ]] &&
   [[ ! -f "$MODEL_DIR/unet/diffusion_pytorch_model.safetensors" ]]; then
    echo "ERROR: SD 1.5 model files not found under: $MODEL_DIR"
    exit 1
fi

echo "SD model: OK"

echo
# --------------------------------------------------
# 2. Frame Pool
# --------------------------------------------------

echo "[2/4] generating frames..."
python3 generate_frames.py \
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
