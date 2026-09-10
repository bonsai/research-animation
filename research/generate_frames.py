#!/usr/bin/env python3
"""Generate a small SD 1.5 frame pool for research-animation.

The local SD installation is intentionally kept outside this repository.
Default model root: /home/bons/.sd

Example:
  python research/generate_frames.py --prompt "a girl walking" --count 100

This script uses AUTOMATIC1111/SD.Next-style WebUI APIs when available.
Set SD_URL if the local WebUI is not running on http://127.0.0.1:7860.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

DEFAULT_SD_URL = os.environ.get("SD_URL", "http://127.0.0.1:7860")
DEFAULT_WIDTH = 128
DEFAULT_HEIGHT = 128
DEFAULT_STEPS = 12
DEFAULT_CFG = 7.0


def post_json(url: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=300) as response:
        return json.loads(response.read())


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
    parser.add_argument("--out", default="frames")
    parser.add_argument("--sd-url", default=DEFAULT_SD_URL)
    args = parser.parse_args()

    if args.width % 8 or args.height % 8:
        raise SystemExit("width/height must be multiples of 8")
    if args.count < 1:
        raise SystemExit("count must be >= 1")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / "frames.json"
    csv_path = out / "frames.csv"

    records = []
    existing = []
    if manifest.exists():
        existing = json.loads(manifest.read_text(encoding="utf-8")).get("frames", [])
        records.extend(existing)

    rng = random.SystemRandom()
    for i in range(args.count):
        frame_id = f"{len(records) + 1:06d}"
        seed = args.seed if args.seed >= 0 else rng.randrange(0, 2**32 - 1)
        payload = {
            "prompt": args.prompt,
            "negative_prompt": args.negative,
            "width": args.width,
            "height": args.height,
            "steps": args.steps,
            "cfg_scale": args.cfg,
            "seed": seed,
            "batch_size": 1,
            "n_iter": 1,
        }
        result = post_json(args.sd_url.rstrip("/") + "/sdapi/v1/txt2img", payload)
        if not result.get("images"):
            raise RuntimeError("SD API returned no image")

        image = base64.b64decode(result["images"][0].split(",", 1)[-1])
        filename = f"{frame_id}.png"
        (out / filename).write_bytes(image)
        records.append({
            "id": frame_id,
            "file": filename,
            "seed": seed,
            "prompt": args.prompt,
            "negative_prompt": args.negative,
            "model": "SD 1.5",
            "width": args.width,
            "height": args.height,
            "steps": args.steps,
            "cfg_scale": args.cfg,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": "local:" + os.path.expanduser("~/.sd"),
        })
        print(f"generated {frame_id} seed={seed}")

    manifest.write_text(json.dumps({"schema_version": 1, "frames": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fields = ["id", "file", "seed", "prompt", "negative_prompt", "model", "width", "height", "steps", "cfg_scale", "generated_at", "source"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    print(f"saved {len(records)} frames to {out}")


if __name__ == "__main__":
    main()
