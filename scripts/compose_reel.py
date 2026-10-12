#!/usr/bin/env python3
"""Compose a vertical, screen-led Her AI reel plus a short end card."""
from __future__ import annotations
import argparse, subprocess, tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

COLORS = {"orange": "#d96a3a", "light-green": "#bee9d4", "dark-green": "#0d403b"}
PROFILES = {
    "instagram": {"width": 1080, "height": 1920, "panel_w": 920, "panel_h": 1300, "panel_y": 340, "title_y": 155, "brand_y": 720, "cta_y": 900},
    "linkedin": {"width": 1080, "height": 1350, "panel_w": 900, "panel_h": 800, "panel_y": 290, "title_y": 105, "brand_y": 470, "cta_y": 650},
}
FPS = 30


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def font(path: Path, size: int):
    return ImageFont.truetype(str(path), size=size)


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, use_font, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=use_font)
    draw.text(((draw._image.width - (box[2] - box[0])) / 2, y), text, font=use_font, fill=fill)


def make_overlays(temp: Path, profile: dict, color: str, title: str, cta: str, logo: Path) -> tuple[Path, Path]:
    width, height = profile["width"], profile["height"]
    root = Path(__file__).resolve().parents[1]
    display_font = root / "assets/fonts/MyeongjoExt-Regular.ttf"
    body_font = root / "assets/fonts/DM-Sans-Variable.ttf"
    title_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    title_draw = ImageDraw.Draw(title_image)
    centered(title_draw, profile["title_y"], title, font(display_font, 56), "#0d403b")
    title_path = temp / "title.png"; title_image.save(title_path)

    endcard = Image.new("RGBA", (width, height), color)
    logo_image = Image.open(logo).convert("RGBA")
    bbox = logo_image.getchannel("A").getbbox()
    if bbox:
        logo_image = logo_image.crop(bbox)
    logo_image.thumbnail((min(width - 220, 620), 280), Image.Resampling.LANCZOS)
    endcard.alpha_composite(logo_image, ((width - logo_image.width) // 2, profile["brand_y"] - 80))
    end_draw = ImageDraw.Draw(endcard)
    centered(end_draw, profile["cta_y"], cta, font(body_font, 38), "#0d403b")
    end_path = temp / "endcard.png"; endcard.save(end_path)
    return title_path, end_path


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
    ap.add_argument("--cta", default="Follow Her AI for practical AI literacy")
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
        title_image, endcard_image = make_overlays(temp, profile, color, args.title, args.cta, args.logo)
        # Crop to a tall panel, preserving legibility over showing an entire desktop.
        panel_w, panel_h = profile["panel_w"], profile["panel_h"]
        vf = (f"scale={panel_w}:{panel_h}:force_original_aspect_ratio=decrease,pad={panel_w}:{panel_h}:(ow-iw)/2:(oh-ih)/2:color=0x101716,"
              f"format=rgba,drawbox=x=-12:y=-12:w={panel_w + 24}:h={panel_h + 24}:color=black@0.26:t=24")
        fc = f"color=c={color}:s={width}x{height}:r={FPS}[bg];[0:v]{vf}[screen];[bg][screen]overlay=(W-w)/2:{profile['panel_y']}:shortest=1[base];[base][2:v]overlay=0:0:shortest=1[v]"
        run(["ffmpeg", "-y", "-i", str(args.screen), "-i", str(args.audio), "-loop", "1", "-i", str(title_image), "-filter_complex", fc, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-shortest", str(body)])
        run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(endcard_image),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-map", "0:v", "-map", "1:a", "-shortest",
            "-t", "2.5", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(ending),
        ])
        list_file.write_text(f"file '{body}'\nfile '{ending}'\n")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(args.out)])
    print(f"Wrote draft composition: {args.out}.")


if __name__ == "__main__":
    main()
