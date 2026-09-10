#!/usr/bin/env python3
"""Render a playback recipe into an MP4 using ffmpeg."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--playback", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ERROR: ffmpeg not found. Install ffmpeg first.")

    playback_path = Path(args.playback)
    data = json.loads(playback_path.read_text(encoding="utf-8"))
    sequence = data.get("sequence", [])
    if not sequence:
        raise SystemExit("playback sequence is empty")

    with tempfile.TemporaryDirectory(prefix="research-animation-") as tmp:
        tmpdir = Path(tmp)
        concat = tmpdir / "concat.txt"
        with concat.open("w", encoding="utf-8") as f:
            for step in sequence:
                frame = (playback_path.parent / step["file"]).resolve()
                if not frame.exists():
                    raise SystemExit(f"frame not found: {frame}")
                f.write(f"file '{frame.as_posix().replace(chr(39), \"'\\''\")}'\n")
                f.write(f"duration {float(step['duration_sec']):.6f}\n")
            last = (playback_path.parent / sequence[-1]["file"]).resolve()
            f.write(f"file '{last.as_posix().replace(chr(39), \"'\\''\")}'\n")

        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            ffmpeg, "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat),
            "-vf", "scale=iw*4:ih*4:flags=nearest,format=yuv420p",
            "-vsync", "vfr", "-movflags", "+faststart", str(out),
        ]
        subprocess.run(cmd, check=True)

    print(f"rendered movie to {out}")


if __name__ == "__main__":
    main()
