#!/usr/bin/env python3
"""Generate a reproducible architectural construction animation.

Scene progression:
site -> grid -> structure -> wall -> opening -> light -> human -> movement
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pyvista as pv


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * np.clip(t, 0.0, 1.0)


def box(center, scale):
    return pv.Box(bounds=(
        center[0] - scale[0] / 2, center[0] + scale[0] / 2,
        center[1] - scale[1] / 2, center[1] + scale[1] / 2,
        center[2] - scale[2] / 2, center[2] + scale[2] / 2,
    ))


def stage_progress(t: float, start: float, end: float) -> float:
    return float(np.clip((t - start) / (end - start), 0.0, 1.0))


def scene(t: float, seed: int = 7):
    """Return meshes and metadata for normalized time t in [0, 1]."""
    rng = np.random.default_rng(seed)
    del rng  # reserved for deterministic future variations

    meshes: list[tuple[pv.DataSet, str]] = []

    site = box((0, 0, -0.15), (14, 10, 0.3))
    meshes.append((site, "site"))

    grid_p = stage_progress(t, 0.05, 0.22)
    if grid_p:
        spacing = 2.0
        for x in np.arange(-6, 7, spacing):
            meshes.append((box((x, 0, 0.02), (0.025, 8 * grid_p, 0.03)), "grid"))
        for y in np.arange(-4, 5, spacing):
            meshes.append((box((0, y, 0.025), (12 * grid_p, 0.025, 0.03)), "grid"))

    structure_p = stage_progress(t, 0.18, 0.50)
    if structure_p:
        height = lerp(0.3, 4.8, structure_p)
        for x in (-5, -2.5, 0, 2.5, 5):
            for y in (-3.5, 3.5):
                meshes.append((box((x, y, height / 2), (0.22, 0.22, height)), "structure"))

    wall_p = stage_progress(t, 0.40, 0.68)
    if wall_p:
        h = lerp(0.1, 4.2, wall_p)
        thickness = 0.18
        # Perimeter walls, with a front opening.
        meshes.append((box((0, 3.5, h / 2), (10, thickness, h)), "wall"))
        meshes.append((box((-5, 0, h / 2), (thickness, 7, h)), "wall"))
        meshes.append((box((5, 0, h / 2), (thickness, 7, h)), "wall"))
        meshes.append((box((-2.8, -3.5, h / 2), (4.4, thickness, h)), "wall"))
        meshes.append((box((2.8, -3.5, h / 2), (4.4, thickness, h)), "wall"))

    opening_p = stage_progress(t, 0.58, 0.78)
    if opening_p:
        # Reveal the front doorway as a moving vertical cut marker.
        x = lerp(-2.0, 0.0, opening_p)
        meshes.append((box((x, -3.62, 1.8), (0.06, 0.12, 3.6)), "opening"))

    light_p = stage_progress(t, 0.68, 0.88)
    if light_p:
        lx = lerp(-4.5, 4.5, light_p)
        ly = 2.0 * np.sin(light_p * np.pi)
        meshes.append((pv.Sphere(radius=0.22, center=(lx, ly, 5.2)), "light"))

    movement_p = stage_progress(t, 0.76, 1.0)
    if movement_p:
        hx = lerp(-4.0, 3.8, movement_p)
        hy = -2.0 + 0.6 * np.sin(movement_p * np.pi)
        body = pv.Cylinder(center=(hx, hy, 1.0), direction=(0, 0, 1), radius=0.18, height=1.4)
        head = pv.Sphere(radius=0.23, center=(hx, hy, 1.9))
        meshes.extend([(body, "human"), (head, "human")])

    return meshes


def render(args: argparse.Namespace) -> None:
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    frames = max(1, int(args.duration * args.fps))

    pl = pv.Plotter(off_screen=True, window_size=(args.width, args.height))
    pl.set_background("white")
    pl.camera_position = [(16, -18, 13), (0, 0, 1.8), (0, 0, 1)]

    if args.format in {"gif", "both"}:
        gif = out.with_suffix(".gif")
        pl.open_gif(gif, fps=args.fps)
        for i in range(frames):
            t = i / max(1, frames - 1)
            pl.clear_actors()
            for mesh, kind in scene(t, args.seed):
                pl.add_mesh(mesh, color=args.colors.get(kind, "lightgray"), show_edges=False)
            pl.add_text(f"architectural animation  {t * args.duration:05.1f}s", name="time")
            pl.write_frame()
        pl.close()

    if args.format in {"mp4", "both"}:
        mp4 = out.with_suffix(".mp4")
        pl = pv.Plotter(off_screen=True, window_size=(args.width, args.height))
        pl.set_background("white")
        pl.camera_position = [(16, -18, 13), (0, 0, 1.8), (0, 0, 1)]
        pl.open_movie(mp4, framerate=args.fps)
        pl.show(auto_close=False)
        for i in range(frames):
            t = i / max(1, frames - 1)
            pl.clear_actors()
            for mesh, kind in scene(t, args.seed):
                pl.add_mesh(mesh, color=args.colors.get(kind, "lightgray"), show_edges=False)
            pl.add_text(f"architectural animation  {t * args.duration:05.1f}s", name="time")
            pl.write_frame()
        pl.close()

    manifest = out.with_name(out.stem + ".manifest.json")
    manifest.write_text(json.dumps({
        "experiment": "EXP-ARCH-001",
        "duration_seconds": args.duration,
        "fps": args.fps,
        "frames": frames,
        "seed": args.seed,
        "renderer": "PyVista/VTK",
        "format": args.format,
        "camera": [(16, -18, 13), (0, 0, 1.8), (0, 0, 1)],
        "stages": ["site", "grid", "structure", "wall", "opening", "light", "human", "movement"],
    }, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs/architectural-construction")
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=540)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--format", choices=["gif", "mp4", "both"], default="gif")
    parser.set_defaults(colors={
        "site": "whitesmoke", "grid": "lightgray", "structure": "dimgray",
        "wall": "silver", "opening": "black", "light": "gold",
        "human": "royalblue",
    })
    args = parser.parse_args()
    render(args)


if __name__ == "__main__":
    main()
