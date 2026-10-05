#!/usr/bin/env bash
set -euo pipefail

# Create reproducible playback JSON and render MP4 from the existing Frame Pool.
# Usage: ./gen_mov.sh [count] [seed]

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COUNT="${1:-30}"
SEED="${2:-42}"
MIN_FPS="${MIN_FPS:-2}"
MAX_FPS="${MAX_FPS:-7}"
FRAMES_DIR="${ROOT}/../frames"
CSV="${FRAMES_DIR}/frames.csv"
PLAYBACK="${FRAMES_DIR}/playback.json"
OUTPUT_DIR="${ROOT}/../output"
OUTPUT="${OUTPUT_DIR}/animation.mp4"

cd "$ROOT"
echo "=== gen_mov ==="
echo "Frame Pool: $FRAMES_DIR"
echo "Count: $COUNT"
echo "Seed: $SEED"
echo "FPS: $MIN_FPS-$MAX_FPS"

if [[ ! -f "$CSV" ]]; then
  echo "ERROR: frame pool not found: $CSV"; exit 1
fi

python3 playback.py \
  --frames "$CSV" \
  --count "$COUNT" \
  --seed "$SEED" \
  --min-fps "$MIN_FPS" \
  --max-fps "$MAX_FPS" \
  --out "$PLAYBACK"

python3 render_video.py \
  --playback "$PLAYBACK" \
  --out "$OUTPUT"

echo "=== movie generation complete ==="
echo "Playback: $PLAYBACK"
echo "Movie:    $OUTPUT"
