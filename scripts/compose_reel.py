#!/usr/bin/env python3
"""Compose a vertical, screen-led Her AI reel plus a short end card."""
from __future__ import annotations
import argparse, json, random, subprocess, tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VIDEO_STYLE = json.loads((ROOT / "assets/brand/tokens/reel-video-style.json").read_text(encoding="utf-8"))
COLORS = VIDEO_STYLE["backgrounds"]
PROFILES = {
    # Reserve a fixed caption safe area beneath the framed demo.
    "instagram": {"width": 1080, "height": 1920, "panel_w": 920, "panel_h": 1100, "panel_y": 340, "title_y": 155, "brand_y": 720, "cta_y": 900},
    "linkedin": {"width": 1080, "height": 1350, "panel_w": 900, "panel_h": 740, "panel_y": 290, "title_y": 105, "brand_y": 470, "cta_y": 650},
}
FPS = 30


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def font(path: Path, size: int):
    return ImageFont.truetype(str(path), size=size)


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, use_font, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=use_font)
    draw.text(((draw._image.width - (box[2] - box[0])) / 2, y), text, font=use_font, fill=fill)


def centered_wrapped(draw: ImageDraw.ImageDraw, y: int, text: str, use_font, fill: str, max_width: int) -> None:
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=use_font) <= max_width or not current:
            current = candidate
        else:
            lines.append(current); current = word
    if current:
        lines.append(current)
    line_height = int(use_font.size * 1.3)
    for index, line in enumerate(lines):
        centered(draw, y + index * line_height, line, use_font, fill)


def make_background(path: Path, width: int, height: int, color: str) -> None:
    """Make a consistent, lightly textured Her AI background without using a reference screenshot."""
    base = tuple(int(color[index:index + 2], 16) for index in (1, 3, 5))
    rng = random.Random(42)
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            # Gentle brighter centre and barely-visible grain echo the approved visual direction.
            distance = (((x - width * 0.5) / width) ** 2 + ((y - height * 0.38) / height) ** 2) ** 0.5
            light = max(-13, min(10, int(10 - distance * 42))) + rng.choice((-2, -1, 0, 0, 0, 1, 2))
            pixels[x, y] = tuple(max(0, min(255, channel + light)) for channel in base)
    image.save(path)


def make_overlays(temp: Path, profile: dict, color: str, title: str, cta: str, logo: Path) -> tuple[Path, Path, Path]:
    width, height = profile["width"], profile["height"]
    display_font = ROOT / "assets/fonts/MyeongjoExt-Regular.ttf"
    body_font = ROOT / "assets/fonts/DM-Sans-Variable.ttf"
    title_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    title_draw = ImageDraw.Draw(title_image)
    # Dark-green cards need light type; dark type remains readable on the other brand colours.
    ink = VIDEO_STYLE["text"]["on-dark"] if color.lower() == COLORS["dark-green"] else VIDEO_STYLE["text"]["on-light"]
    centered(title_draw, profile["title_y"], title, font(display_font, 56), ink)
    title_path = temp / "title.png"; title_image.save(title_path)

    # A browser frame makes tool demonstrations feel like a polished product reel.
    frame = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    frame_draw = ImageDraw.Draw(frame)
    panel_x = (width - profile["panel_w"]) // 2
    panel_y = profile["panel_y"]
    panel_w, panel_h = profile["panel_w"], profile["panel_h"]
    radius, chrome_h = 22, 46
    frame_draw.rounded_rectangle((panel_x - 3, panel_y - 3, panel_x + panel_w + 3, panel_y + panel_h + 3), radius=radius + 3, fill=(7, 25, 25, 80))
    frame_draw.rounded_rectangle((panel_x, panel_y, panel_x + panel_w, panel_y + panel_h), radius=radius, fill=(23, 31, 34, 255))
    frame_draw.rectangle((panel_x, panel_y + chrome_h, panel_x + panel_w, panel_y + panel_h), fill=(0, 0, 0, 0))
    for offset, dot_color in ((22, "#ff605c"), (42, "#ffbd44"), (62, "#00ca4e")):
        frame_draw.ellipse((panel_x + offset - 5, panel_y + 18 - 5, panel_x + offset + 5, panel_y + 18 + 5), fill=dot_color)
    frame_path = temp / "browser-frame.png"; frame.save(frame_path)

    endcard = Image.new("RGBA", (width, height), color)
    logo_image = Image.open(logo).convert("RGBA")
    bbox = logo_image.getchannel("A").getbbox()
    if bbox:
        logo_image = logo_image.crop(bbox)
    logo_image.thumbnail((min(width - 220, 620), 280), Image.Resampling.LANCZOS)
    endcard.alpha_composite(logo_image, ((width - logo_image.width) // 2, profile["brand_y"] - 80))
    end_draw = ImageDraw.Draw(endcard)
    centered_wrapped(end_draw, profile["cta_y"], cta, font(body_font, 38), ink, width - 180)
    end_path = temp / "endcard.png"; endcard.save(end_path)
    return title_path, end_path, frame_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen", required=True, type=Path)
    ap.add_argument("--audio", required=True, type=Path)
    ap.add_argument("--timeline", required=True, type=Path, help="Retained as an explicit production input for timing review.")
    ap.add_argument("--background", choices=COLORS, required=True)
    ap.add_argument("--format", choices=PROFILES, required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--logo", type=Path, default=Path(__file__).resolve().parents[1] / "assets/logo/her-ai-primary-transparent.png")
    ap.add_argument("--title", default="AI, explained clearly")
    ap.add_argument("--cta", default="Follow her/ai and sign up for our upcoming workshops for more practical AI literacy.")
    args = ap.parse_args()
    if not args.timeline.exists(): raise SystemExit(f"Missing timeline: {args.timeline}")
    if not args.logo.exists(): raise SystemExit(f"Missing logo: {args.logo}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    color = COLORS[args.background]
    profile = PROFILES[args.format]
    width, height = profile["width"], profile["height"]
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        body, ending, list_file = temp/"body.mp4", temp/"ending.mp4", temp/"concat.txt"
        background_image = temp / "background.png"
        make_background(background_image, width, height, color)
        title_image, endcard_image, frame_image = make_overlays(temp, profile, color, args.title, args.cta, args.logo)
        # Crop to a tall panel, preserving legibility over showing an entire desktop.
        panel_w, panel_h = profile["panel_w"], profile["panel_h"]
        chrome_h = 46
        content_w, content_h = panel_w - 4, panel_h - chrome_h - 2
        vf = f"scale={content_w}:{content_h}:force_original_aspect_ratio=decrease,pad={content_w}:{content_h}:(ow-iw)/2:(oh-ih)/2:color=0xf8f7f3,format=rgba"
        panel_x = (width - panel_w) // 2 + 2
        screen_y = profile["panel_y"] + chrome_h
        fc = (f"[0:v]{vf}[screen];"
              f"[2:v]format=rgba[bg];[bg][screen]overlay={panel_x}:{screen_y}:shortest=1[base];"
              f"[base][4:v]overlay=0:0:shortest=1[framed];"
              f"[framed][3:v]overlay=0:0:shortest=1[v]")
        run(["ffmpeg", "-y", "-i", str(args.screen), "-i", str(args.audio), "-loop", "1", "-i", str(background_image), "-loop", "1", "-i", str(title_image), "-loop", "1", "-i", str(frame_image), "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-shortest", str(body)])
        run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(endcard_image),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-map", "0:v", "-map", "1:a", "-shortest",
            "-t", "2.5", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", str(ending),
        ])
        list_file.write_text(f"file '{body}'\nfile '{ending}'\n")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(args.out)])
    manifest_path = args.out.with_suffix(".render.json")
    manifest_path.write_text(json.dumps({
        "kind": "her-ai-clean-reel",
        "format": args.format,
        "background": args.background,
        "background_hex": color,
        "video_style": "assets/brand/tokens/reel-video-style.json",
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote draft composition: {args.out}.\nWrote render manifest: {manifest_path}.")


if __name__ == "__main__":
    main()
