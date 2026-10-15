#!/usr/bin/env python3
"""Prepend a reusable still start card and shift a reel's caption timeline."""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def video_dimensions(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "" "stream=width,height", "-of", "csv=p=0", str(path)],
        text=True,
        capture_output=True,
        check=True,
    )
    return tuple(map(int, result.stdout.strip().split(",")))


def media_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
        capture_output=True,
        check=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path, help="Clean reel with audio.")
    parser.add_argument("--card", required=True, type=Path)
    parser.add_argument("--timeline", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--shifted-timeline", required=True, type=Path)
    parser.add_argument("--duration", type=float, default=1.4)
    args = parser.parse_args()
    if not all(path.exists() for path in (args.input, args.card, args.timeline)):
        raise SystemExit("Input reel, start card, and timeline must exist.")
    width, height = video_dimensions(args.input)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.shifted_timeline.parent.mkdir(parents=True, exist_ok=True)
    # Both segments are normalised to H.264/AAC mono before a stream-copy
    # concat. This is faster and preserves the full source reel.
    with tempfile.TemporaryDirectory() as temp_dir:
        intro = Path(temp_dir) / "intro.mp4"
        listing = Path(temp_dir) / "concat.txt"
        run([
            "ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-i", str(args.card),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=44100",
            "-t", str(args.duration), "-vf", f"scale={width}:{height}", "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-ac", "1", str(intro),
        ])
        listing.write_text(f"file '{intro}'\nfile '{args.input.resolve()}'\n")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(args.out)])
    cues = json.loads(args.timeline.read_text(encoding="utf-8"))
    shifted = [{**cue, "start": round(float(cue["start"]) + args.duration, 3), "end": round(float(cue["end"]) + args.duration, 3)} for cue in cues]
    args.shifted_timeline.write_text(json.dumps(shifted, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out} and {args.shifted_timeline}")


if __name__ == "__main__":
    main()
