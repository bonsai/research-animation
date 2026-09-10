#!/usr/bin/env python3
"""Generate a small SD 1.5 frame pool directly from a local Diffusers model."""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_MODEL_DIR = os.environ.get("SD_MODEL_DIR", os.path.expanduser("~/.sd/sd15_model"))
DEFAULT_WIDTH = 128
DEFAULT_HEIGHT = 128
DEFAULT_STEPS = 12
DEFAULT_CFG = 7.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="a tiny hand-drawn animation frame")
    parser.add_argument("--negative", default="low quality, blurry, distorted")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--cfg", type=float, default=DEFAULT_CFG)
    parser.add_argument("--seed", type=int, default=-1)
    parser.add_argument("--out", default="../frames")
    parser.add_argument("--model-dir", default=DEFAULT_MODEL_DIR)
    args = parser.parse_args()

    if args.width % 8 or args.height % 8:
        raise SystemExit("width/height must be multiples of 8")
    if args.count < 1:
        raise SystemExit("count must be >= 1")

    try:
        import torch
        from diffusers import StableDiffusionPipeline
    except ImportError as exc:
        raise SystemExit(
            "Missing local SD Python packages. Install torch and diffusers in the active Python environment."
        ) from exc

    model_dir = Path(os.path.expanduser(args.model_dir))
    if not model_dir.is_dir():
        raise SystemExit(f"SD model directory not found: {model_dir}")

    print(f"Loading SD 1.5 from {model_dir}")
    print(f"Torch: {torch.__version__}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    print(f"Device: {device}")

    pipe = StableDiffusionPipeline.from_pretrained(
        str(model_dir),
        torch_dtype=dtype,
        local_files_only=True,
        safety_checker=None,
    )
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / "frames.json"
    csv_path = out / "frames.csv"

    records = []
    if manifest.exists():
        records.extend(json.loads(manifest.read_text(encoding="utf-8")).get("frames", []))

    rng = random.SystemRandom()
    for _ in range(args.count):
        frame_id = f"{len(records) + 1:06d}"
        seed = args.seed if args.seed >= 0 else rng.randrange(0, 2**32 - 1)
        generator = torch.Generator(device=device).manual_seed(seed)
        result = pipe(
            prompt=args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            num_inference_steps=args.steps,
            guidance_scale=args.cfg,
            generator=generator,
        )
        image = result.images[0]
        filename = f"{frame_id}.png"
        image.save(out / filename)
        records.append({
            "id": frame_id,
            "file": filename,
            "seed": seed,
            "prompt": args.prompt,
            "negative_prompt": args.negative,
            "model": "SD 1.5",
            "model_dir": str(model_dir),
            "width": args.width,
            "height": args.height,
            "steps": args.steps,
            "cfg_scale": args.cfg,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "local-diffusers",
        })
        print(f"generated {frame_id} seed={seed}")

    manifest.write_text(
        json.dumps({"schema_version": 1, "frames": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    fields = [
        "id", "file", "seed", "prompt", "negative_prompt", "model", "model_dir",
        "width", "height", "steps", "cfg_scale", "generated_at", "source",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    print(f"saved {len(records)} frames to {out}")


if __name__ == "__main__":
    main()
