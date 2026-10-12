#!/usr/bin/env python3
"""Render timeline captions as PNG overlays; works without FFmpeg subtitle filters."""
from __future__ import annotations

import argparse, json, subprocess, tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def dimensions(video: Path) -> tuple[int, int]:
    result = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", str(video)], capture_output=True, text=True, check=True)
    stream = json.loads(result.stdout)["streams"][0]
    return int(stream["width"]), int(stream["height"])


def wrap(draw: ImageDraw.ImageDraw, text: str, use_font, max_width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=use_font) <= max_width or not current:
            current = candidate
        else:
            lines.append(current); current = word
    if current: lines.append(current)
    return lines


def caption_image(path: Path, width: int, height: int, text: str, margin: int, font_path: Path) -> None:
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0)); draw = ImageDraw.Draw(image)
    use_font = ImageFont.truetype(str(font_path), size=38)
    lines = wrap(draw, text, use_font, width - 160)
    line_height = 50; box_height = len(lines) * line_height + 42; y = height - margin - box_height
    draw.rounded_rectangle((64, y, width - 64, y + box_height), radius=20, fill=(13, 64, 59, 220))
    for index, line in enumerate(lines):
        text_width = draw.textlength(line, font=use_font)
        draw.text(((width - text_width) / 2, y + 20 + index * line_height), line, font=use_font, fill="white")
    image.save(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path); ap.add_argument("--timeline", required=True, type=Path)
    ap.add_argument("--format", choices=("instagram", "linkedin"), required=True); ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    cues = json.loads(args.timeline.read_text(encoding="utf-8")); width, height = dimensions(args.input)
    margin = 250 if args.format == "instagram" else 140
    font_path = Path(__file__).resolve().parents[1] / "assets/fonts/DM-Sans-Variable.ttf"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp); command = ["ffmpeg", "-y", "-i", str(args.input)]; filters = []; previous = "0:v"
        for index, cue in enumerate(cues, 1):
            image_path = temp / f"caption-{index:02d}.png"
            caption_image(image_path, width, height, cue.get("caption_text", cue["voice_text"]), margin, font_path)
            command.extend(["-loop", "1", "-i", str(image_path)])
            output = f"v{index}"
            filters.append(f"[{previous}][{index}:v]overlay=0:0:enable='between(t,{cue['start']},{cue['end']})'[{output}]")
            previous = output
        command.extend(["-filter_complex", ";".join(filters), "-map", f"[{previous}]", "-map", "0:a?", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(args.out)])
        subprocess.run(command, check=True)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
