#!/usr/bin/env python3
"""Generate a mock image (colored noise) for pipeline testing without a model."""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


def generate_mock(
    width: int,
    height: int,
    seed: int,
    out_dir: Path,
    run_id: str,
    prompt: str = "",
    negative: str = "",
) -> dict:
    rng = random.Random(seed)
    # Deterministic per-seed color bias
    r = rng.randint(30, 220)
    g = rng.randint(30, 220)
    b = rng.randint(30, 220)
    # Add some noise
    img = Image.new("RGB", (width, height), (r, g, b))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            nr = max(0, min(255, pixels[x, y][0] + rng.randint(-40, 40)))
            ng = max(0, min(255, pixels[x, y][1] + rng.randint(-40, 40)))
            nb = max(0, min(255, pixels[x, y][2] + rng.randint(-40, 40)))
            pixels[x, y] = (nr, ng, nb)

    out_dir.mkdir(parents=True, exist_ok=True)
    img_path = out_dir / f"{run_id}.png"
    img.save(img_path)

    meta = {
        "run_id": run_id,
        "model": "mock",
        "prompt": prompt,
        "negative_prompt": negative,
        "width": width,
        "height": height,
        "seed": seed,
        "image_path": str(img_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    json_path = img_path.with_suffix(".json")
    json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved mock: {img_path}")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="")
    parser.add_argument("--negative", default="")
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default="outputs")
    parser.add_argument("--run-id", default="run-001")
    args = parser.parse_args()

    generate_mock(
        width=args.width,
        height=args.height,
        seed=args.seed,
        out_dir=Path(args.out_dir),
        run_id=args.run_id,
        prompt=args.prompt,
        negative=args.negative,
    )


if __name__ == "__main__":
    main()
