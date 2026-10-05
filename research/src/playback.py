#!/usr/bin/env python3
"""Create a reproducible random-tempo playback recipe from a frame pool."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", default="frames/frames.csv")
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--min-fps", type=int, default=2)
    parser.add_argument("--max-fps", type=int, default=7)
    parser.add_argument("--out", default="playback/playback.json")
    args = parser.parse_args()

    if args.min_fps < 1 or args.max_fps < args.min_fps:
        raise SystemExit("invalid fps range")

    with open(args.frames, newline="", encoding="utf-8") as f:
        frames = list(csv.DictReader(f))
    if not frames:
        raise SystemExit("frame pool is empty")

    rng = random.Random(args.seed)
    sequence = []
    for _ in range(args.count):
        frame = rng.choice(frames)
        fps = rng.randint(args.min_fps, args.max_fps)
        sequence.append({
            "frame": frame["id"],
            "file": frame["file"],
            "fps": fps,
            "duration_sec": round(1.0 / fps, 6),
        })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "schema_version": 1,
        "playback_seed": args.seed,
        "fps_range": [args.min_fps, args.max_fps],
        "sequence": sequence,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"saved {len(sequence)} playback steps to {out}")


if __name__ == "__main__":
    main()
