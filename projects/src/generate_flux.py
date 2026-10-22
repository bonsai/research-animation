#!/usr/bin/env python3
"""Generate an image using diffusers pipeline (Flux or SD fallback).

Tries Flux schnell first; falls back to SD 1.5 if model unavailable or OOM.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_flux_pipeline(device: str):
    try:
        from diffusers import FluxPipeline
        import torch

        model_id = "black-forest-labs/FLUX.1-schnell"
        cache = Path.home() / ".cache" / "huggingface" / "hub"
        dtype = torch.bfloat16 if device == "cuda" else torch.float32

        pipe = FluxPipeline.from_pretrained(
            model_id,
            torch_dtype=dtype,
            cache_dir=str(cache),
        )
        pipe = pipe.to(device)
        return pipe, "flux-schnell"
    except Exception as exc:
        print(f"Flux load failed: {exc}")
        return None, None


def load_sd_pipeline(device: str, model_dir: str | None = None):
    try:
        from diffusers import StableDiffusionPipeline
        import torch

        dtype = torch.float16 if device == "cuda" else torch.float32

        if model_dir and Path(model_dir).is_dir():
            pipe = StableDiffusionPipeline.from_pretrained(
                model_dir,
                torch_dtype=dtype,
                local_files_only=True,
                safety_checker=None,
            )
        else:
            pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=dtype,
                safety_checker=None,
            )
        pipe = pipe.to(device)
        return pipe, "sd15"
    except Exception as exc:
        print(f"SD load failed: {exc}")
        return None, None


def generate(
    prompt: str,
    negative: str,
    width: int,
    height: int,
    steps: int,
    cfg: float,
    seed: int,
    out_dir: Path,
    run_id: str = "run-001",
) -> dict:
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    # Try Flux first, then SD
    pipe, model_name = load_flux_pipeline(device)
    if pipe is None:
        sd_dir = os.environ.get("SD_MODEL_DIR")
        pipe, model_name = load_sd_pipeline(device, sd_dir)
    if pipe is None:
        raise SystemExit("No usable pipeline found.")

    print(f"Model: {model_name}")

    generator = torch.Generator(device=device).manual_seed(seed)

    # Flux uses guidance_scale differently; typically fixed or omitted for schnell
    if model_name.startswith("flux"):
        result = pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_inference_steps=min(steps, 4) if model_name.endswith("schnell") else steps,
            generator=generator,
        )
    else:
        result = pipe(
            prompt=prompt,
            negative_prompt=negative,
            height=height,
            width=width,
            num_inference_steps=steps,
            guidance_scale=cfg,
            generator=generator,
        )

    image = result.images[0]
    img_path = ensure_dir(out_dir) / f"{run_id}.png"
    image.save(img_path)

    meta = {
        "run_id": run_id,
        "model": model_name,
        "prompt": prompt,
        "negative_prompt": negative,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg,
        "seed": seed,
        "device": device,
        "image_path": str(img_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    json_path = img_path.with_suffix(".json")
    json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved: {img_path}")
    print(f"Meta : {json_path}")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative", default="low quality, blurry, distorted, text, watermark")
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--cfg", type=float, default=7.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default="outputs")
    parser.add_argument("--run-id", default="run-001")
    args = parser.parse_args()

    out = Path(args.out_dir)
    generate(
        prompt=args.prompt,
        negative=args.negative,
        width=args.width,
        height=args.height,
        steps=args.steps,
        cfg=args.cfg,
        seed=args.seed,
        out_dir=out,
        run_id=args.run_id,
    )


if __name__ == "__main__":
    main()
