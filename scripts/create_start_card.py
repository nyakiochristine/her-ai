#!/usr/bin/env python3
"""Create a reusable Her AI social-reel start-card PNG from approved brand assets."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
VIDEO_STYLE = json.loads((ROOT / "assets/brand/tokens/reel-video-style.json").read_text(encoding="utf-8"))
W, H = 1080, 1350


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


GREEN = hex_to_rgb(VIDEO_STYLE["backgrounds"]["bright-green"])
DARK = hex_to_rgb(VIDEO_STYLE["text"]["on-light"])
BEIGE = hex_to_rgb(VIDEO_STYLE["backgrounds"]["beige"])
LIGHT_GREEN = hex_to_rgb(VIDEO_STYLE["backgrounds"]["light-green"])


def fit_text(draw: ImageDraw.ImageDraw, text: str, font_path: Path, max_width: int, max_size: int) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(max_size, 35, -2):
        use_font = ImageFont.truetype(str(font_path), size)
        words, lines, line = text.split(), [], ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if draw.textlength(candidate, font=use_font) <= max_width or not line:
                line = candidate
            else:
                lines.append(line); line = word
        if line:
            lines.append(line)
        if len(lines) <= 3:
            return use_font, lines
    return ImageFont.truetype(str(font_path), 36), [text]


def centre(draw: ImageDraw.ImageDraw, text: str, y: int, use_font, fill) -> None:
    box = draw.textbbox((0, 0), text, font=use_font)
    draw.text(((W - (box[2] - box[0])) / 2, y), text, font=use_font, fill=fill)


def textured_background() -> Image.Image:
    rng = random.Random(20261014)
    image = Image.new("RGB", (W, H))
    pixels = image.load()
    for y in range(H):
        for x in range(W):
            # A subtly lit, gently grainy green background—not a copy of any reference image.
            dx, dy = (x - W * 0.52) / W, (y - H * 0.42) / H
            glow = max(-13, min(11, int(10 - (dx * dx + dy * dy) ** 0.5 * 42)))
            grain = rng.choice((-2, -1, 0, 0, 0, 1, 2))
            pixels[x, y] = tuple(max(0, min(255, c + glow + grain)) for c in GREEN)
    return image.convert("RGBA")


def create_card(title: str, subtitle: str, out: Path) -> None:
    image = textured_background()
    draw = ImageDraw.Draw(image)
    serif = ROOT / "assets/fonts/MyeongjoExt-Regular.ttf"
    sans = ROOT / "assets/fonts/DM-Sans-Variable.ttf"

    # A compact, ad-like brand label.
    pill = (300, 72, 780, 126)
    draw.rounded_rectangle(pill, radius=27, fill=BEIGE)
    label_font = ImageFont.truetype(str(sans), 25)
    centre(draw, "AI LITERACY, MADE PRACTICAL", 84, label_font, DARK)

    title_font, lines = fit_text(draw, title, serif, 850, 88)
    title_y = 205
    for line in lines:
        centre(draw, line, title_y, title_font, DARK)
        title_y += int(title_font.size * 1.08)
    subtitle_font = ImageFont.truetype(str(sans), 34)
    centre(draw, subtitle, title_y + 24, subtitle_font, DARK)

    # Friendly abstract chat/browser card: familiar, not a copy of any product UI.
    card = (108, 560, 972, 1012)
    draw.rounded_rectangle(card, radius=36, fill=(18, 44, 42), outline=(5, 52, 48), width=5)
    draw.rounded_rectangle((108, 560, 972, 626), radius=36, fill=(20, 38, 39))
    draw.rectangle((108, 594, 972, 626), fill=(20, 38, 39))
    for x, fill in ((148, "#ff605c"), (176, "#ffbd44"), (204, "#00ca4e")):
        draw.ellipse((x - 8, 585 - 8, x + 8, 585 + 8), fill=fill)
    draw.rounded_rectangle((152, 674, 611, 752), radius=24, fill=BEIGE)
    bubble_font = ImageFont.truetype(str(sans), 32)
    draw.text((184, 697), "A quick AI reality check", font=bubble_font, fill=DARK)
    draw.rounded_rectangle((367, 786, 928, 890), radius=28, fill=LIGHT_GREEN)
    draw.text((405, 819), "What does it remember?", font=bubble_font, fill=DARK)
    # Simple wiggly underline marks, a reusable brand-adjacent decorative device.
    draw.arc((172, 925, 328, 1055), 190, 342, fill=LIGHT_GREEN, width=12)
    draw.arc((746, 925, 902, 1055), 198, 350, fill=LIGHT_GREEN, width=12)

    logo = Image.open(ROOT / "assets/logo/her-ai-primary-dark-green-transparent.png").convert("RGBA")
    alpha_box = logo.getchannel("A").getbbox()
    if alpha_box:
        logo = logo.crop(alpha_box)
    logo.thumbnail((210, 110), Image.Resampling.LANCZOS)
    image.alpha_composite(logo, ((W - logo.width) // 2, 1165))

    out.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(out, quality=95)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="Does Claude remember you?")
    parser.add_argument("--subtitle", default="A quick AI reality check")
    parser.add_argument("--out", type=Path, default=ROOT / "assets/templates/reels/her-ai-start-card-template.png")
    args = parser.parse_args()
    create_card(args.title, args.subtitle, args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
