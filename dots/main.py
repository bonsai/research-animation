"""Run the AW -> Pillow dots animation PoC."""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from .aw import AnimationState, build_graph
from .render import render


def initial_state(count: int, width: int, height: int, seed: int) -> AnimationState:
    import random

    rng = random.Random(seed)
    return {
        "dots": [
            {
                "id": f"dot-{i:03d}",
                "x": rng.uniform(0, width),
                "y": rng.uniform(0, height),
                "radius": rng.uniform(2, 7),
                "opacity": rng.uniform(0.55, 1),
                "phase": rng.uniform(0, math.tau),
            }
            for i in range(count)
        ],
        "frame": 0,
        "width": width,
        "height": height,
        "seed": seed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", type=int, default=60)
    parser.add_argument("--dots", type=int, default=24)
    parser.add_argument("--width", type=int, default=256)
    parser.add_argument("--height", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("output/dots.gif"))
    args = parser.parse_args()

    graph = build_graph()
    state = initial_state(args.dots, args.width, args.height, args.seed)
    frames = []
    for _ in range(args.frames):
        frames.append(render(state["dots"], args.width, args.height))
        state = graph.invoke(state)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
    )
    print(f"wrote {args.output} ({len(frames)} frames)")


if __name__ == "__main__":
    main()
