"""Pillow-only renderer for dot states."""
from __future__ import annotations

from PIL import Image, ImageDraw

from .aw import Dot


def render(dots: list[Dot], width: int, height: int) -> Image.Image:
    image = Image.new("RGBA", (width, height), (8, 8, 8, 255))
    draw = ImageDraw.Draw(image, "RGBA")
    for dot in dots:
        r = dot["radius"]
        alpha = int(dot["opacity"] * 255)
        box = (dot["x"] - r, dot["y"] - r, dot["x"] + r, dot["y"] + r)
        draw.ellipse(box, fill=(245, 245, 245, alpha))
    return image.convert("RGB")
