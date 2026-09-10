#!/usr/bin/env bash
set -euo pipefail

# Generate an SD 1.5 Frame Pool. Playback/FPS are intentionally separate.
# Usage: ./gen_img.sh [count]

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SD_DIR="${SD_DIR:-${HOME}/.sd}"
MODEL_DIR="${MODEL_DIR:-${SD_DIR}/sd15_model}"
COUNT="${1:-10}"
WIDTH="${WIDTH:-128}"
HEIGHT="${HEIGHT:-128}"
STEPS="${STEPS:-12}"
CFG="${CFG:-7}"

cd "$ROOT"
echo "=== gen_img ==="
echo "Model: $MODEL_DIR"
echo "Frames: $COUNT"

if [[ ! -d "$MODEL_DIR" ]]; then
  echo "ERROR: model directory not found: $MODEL_DIR"; exit 1
fi
if [[ ! -f "$MODEL_DIR/v1-5-pruned-emaonly.safetensors" ]] && [[ ! -f "$MODEL_DIR/unet/diffusion_pytorch_model.safetensors" ]]; then
  echo "ERROR: SD 1.5 model files not found under: $MODEL_DIR"; exit 1
fi

python3 generate_frames.py \
  --count "$COUNT" \
  --width "$WIDTH" \
  --height "$HEIGHT" \
  --steps "$STEPS" \
  --cfg "$CFG" \
  --prompt "a tiny hand-drawn animation frame"

echo "=== image generation complete ==="
echo "Frame Pool: ${ROOT}/../frames"
