#!/usr/bin/env bash
set -euo pipefail

# Generate an SD 1.5 Frame Pool. Playback/FPS are intentionally separate.
# Usage: ./gen_img.sh [count] [preset]

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SD_DIR="${SD_DIR:-${HOME}/.sd}"
MODEL_DIR="${MODEL_DIR:-${SD_DIR}/sd15_model}"
COUNT="${1:-10}"
PRESET="${2:-default}"
WIDTH="${WIDTH:-128}"
HEIGHT="${HEIGHT:-128}"
STEPS="${STEPS:-12}"
CFG="${CFG:-7}"
PROMPTS_JSON="${PROMPTS_JSON:-${ROOT}/prompts.json}"

cd "$ROOT"
echo "=== gen_img ==="
echo "Model: $MODEL_DIR"
echo "Frames: $COUNT"
echo "Preset: $PRESET"
echo "Prompts: $PROMPTS_JSON"

if [[ ! -d "$MODEL_DIR" ]]; then
  echo "ERROR: model directory not found: $MODEL_DIR"; exit 1
fi
if [[ ! -f "$MODEL_DIR/v1-5-pruned-emaonly.safetensors" ]] && [[ ! -f "$MODEL_DIR/unet/diffusion_pytorch_model.safetensors" ]]; then
  echo "ERROR: SD 1.5 model files not found under: $MODEL_DIR"; exit 1
fi
if [[ ! -f "$PROMPTS_JSON" ]]; then
  echo "ERROR: prompts JSON not found: $PROMPTS_JSON"; exit 1
fi

PROMPT_DATA="$(python3 - "$PROMPTS_JSON" "$PRESET" <<'PY'
import json
import sys

path, preset = sys.argv[1:]
data = json.load(open(path, encoding="utf-8"))

if preset == "default":
    config = data.get("default", {})
else:
    config = data.get("presets", {}).get(preset)
    if config is None:
        available = ", ".join(data.get("presets", {}).keys())
        raise SystemExit(f"ERROR: unknown preset '{preset}'. Available: {available}")

print(config.get("prompt", data.get("default", {}).get("prompt", "")))
print(config.get("negative_prompt", data.get("default", {}).get("negative_prompt", "")))
PY
)"

PROMPT="$(printf '%s\n' "$PROMPT_DATA" | sed -n '1p')"
NEGATIVE_PROMPT="$(printf '%s\n' "$PROMPT_DATA" | sed -n '2p')"

python3 generate_frames.py \
  --count "$COUNT" \
  --width "$WIDTH" \
  --height "$HEIGHT" \
  --steps "$STEPS" \
  --cfg "$CFG" \
  --prompt "$PROMPT" \
  --negative-prompt "$NEGATIVE_PROMPT"

echo "=== image generation complete ==="
echo "Frame Pool: ${ROOT}/../frames"
