#!/usr/bin/env python3
"""Render timeline captions as PNG overlays; works without FFmpeg subtitle filters."""
from __future__ import annotations

import argparse, json, subprocess, tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VIDEO_STYLE = json.loads((ROOT / "assets/brand/tokens/reel-video-style.json").read_text(encoding="utf-8"))
CAPTION_STYLE = VIDEO_STYLE["captions"]


def hex_to_rgba(value: str, opacity: int) -> tuple[int, int, int, int]:
    """Convert one approved #RRGGBB brand colour to a Pillow RGBA tuple."""
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4)) + (opacity,)


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


def caption_image(path: Path, width: int, text: str, font_path: Path) -> tuple[int, int]:
    # Render only the caption box, not a transparent full-video frame. This
    # greatly reduces FFmpeg's per-frame compositing work.
    box_width = width - (CAPTION_STYLE["horizontal_margin"] * 2)
    image = Image.new("RGBA", (box_width, 10), (0, 0, 0, 0)); draw = ImageDraw.Draw(image)
    use_font = ImageFont.truetype(str(font_path), size=CAPTION_STYLE["font_size"])
    lines = wrap(draw, text, use_font, box_width - (CAPTION_STYLE["horizontal_padding"] * 2))
    line_height = CAPTION_STYLE["line_height"]
    box_height = len(lines) * line_height + (CAPTION_STYLE["vertical_padding"] * 2) + 2
    image = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0)); draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (0, 0, box_width, box_height),
        radius=CAPTION_STYLE["corner_radius"],
        fill=hex_to_rgba(CAPTION_STYLE["background"], CAPTION_STYLE["background_opacity"]),
    )
    for index, line in enumerate(lines):
        text_width = draw.textlength(line, font=use_font)
        draw.text(
            ((box_width - text_width) / 2, CAPTION_STYLE["vertical_padding"] + index * line_height),
            line,
            font=use_font,
            fill=VIDEO_STYLE["text"]["caption"],
        )
    image.save(path)
    return box_width, box_height


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path); ap.add_argument("--timeline", required=True, type=Path)
    ap.add_argument("--format", choices=("instagram", "linkedin"), required=True); ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    cues = json.loads(args.timeline.read_text(encoding="utf-8")); width, height = dimensions(args.input)
    margin = CAPTION_STYLE["bottom_safe_margin"][args.format]
    font_path = ROOT / "assets/fonts" / CAPTION_STYLE["font"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp); command = ["ffmpeg", "-y", "-i", str(args.input)]; filters = []; previous = "0:v"
        for index, cue in enumerate(cues, 1):
            image_path = temp / f"caption-{index:02d}.png"
            box_width, box_height = caption_image(image_path, width, cue.get("caption_text", cue["voice_text"]), font_path)
            command.extend(["-loop", "1", "-i", str(image_path)])
            output = f"v{index}"
            y = height - margin - box_height
            filters.append(f"[{previous}][{index}:v]overlay={CAPTION_STYLE['horizontal_margin']}:{y}:enable='between(t,{cue['start']},{cue['end']})'[{output}]")
            previous = output
        command.extend(["-filter_complex", ";".join(filters), "-map", f"[{previous}]", "-map", "0:a?", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(args.out)])
        subprocess.run(command, check=True)
    manifest_path = args.out.with_suffix(".render.json")
    manifest_path.write_text(json.dumps({
        "kind": "her-ai-captioned-reel",
        "format": args.format,
        "source": str(args.input),
        "timeline": str(args.timeline),
        "video_style": "assets/brand/tokens/reel-video-style.json",
        "caption_style": CAPTION_STYLE,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}\nWrote caption manifest: {manifest_path}")


if __name__ == "__main__":
    main()
