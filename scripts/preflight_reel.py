#!/usr/bin/env python3
"""Fast delivery preflight for a paired Her AI clean and captioned reel.

This inspects existing files and their small JSON sidecars only. It never
re-renders video and never sends a request to ElevenLabs.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from load_keys import load
from compose_reel import COLORS, PROFILES
from make_subtitles import CAPTION_STYLE, caption_image


ROOT = Path(__file__).resolve().parents[1]
MAX_DURATION_SECONDS = 40.0
MIN_MEAN_VOLUME_DB = -35.0


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "ffprobe could not read this file")
    return json.loads(result.stdout)


def video_checks(path: Path, expected: tuple[int, int]) -> list[str]:
    if not path.exists():
        return ["file does not exist"]
    try:
        data = probe(path)
        streams = data["streams"]
        video = next(stream for stream in streams if stream["codec_type"] == "video")
        audio = next((stream for stream in streams if stream["codec_type"] == "audio"), None)
        duration = float(data["format"].get("duration", 0))
    except Exception as exc:
        return [str(exc)]
    issues = []
    if (int(video["width"]), int(video["height"])) != expected:
        issues.append(f"expected {expected[0]}x{expected[1]}, got {video['width']}x{video['height']}")
    if duration <= 0 or duration > MAX_DURATION_SECONDS:
        issues.append(f"duration must be > 0 and <= {MAX_DURATION_SECONDS:.0f}s; got {duration:.1f}s")
    if not audio:
        issues.append("missing audio stream")
    return issues


def mean_volume_db(path: Path) -> float | None:
    """Return mean dBFS from a local FFmpeg pass, or None for silence."""
    result = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-map", "0:a:0", "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    match = re.search(r"mean_volume:\s+(-?\d+(?:\.\d+)?|-inf) dB", result.stderr)
    if not match or match.group(1) == "-inf":
        return None
    return float(match.group(1))


def read_manifest(video: Path) -> dict | None:
    path = video.with_suffix(".render.json")
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def caption_clearance_issues(timeline: Path, profile_name: str) -> list[str]:
    """Ensure every caption begins below the framed demo, not over its UI."""
    try:
        cues = json.loads(timeline.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"cannot read timeline: {exc}"]
    profile = PROFILES[profile_name]
    font_path = ROOT / "assets/fonts" / CAPTION_STYLE["font"]
    demo_bottom = profile["panel_y"] + profile["panel_h"]
    clearance = CAPTION_STYLE["screen_clearance"]
    issues = []
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        for index, cue in enumerate(cues, 1):
            text = cue.get("caption_text", cue.get("voice_text", ""))
            if not text.strip():
                issues.append(f"caption {index} has no text")
                continue
            _, box_height = caption_image(temp / f"caption-{index}.png", profile["width"], text, font_path)
            caption_top = profile["height"] - CAPTION_STYLE["bottom_safe_margin"][profile_name] - box_height
            if caption_top < demo_bottom + clearance:
                issues.append(
                    f"caption {index} would overlap the demo frame (top {caption_top}px; "
                    f"needs >= {demo_bottom + clearance}px). Shorten or split it."
                )
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Fast post-export validation; does not re-render video.")
    parser.add_argument("--format", choices=PROFILES, required=True)
    parser.add_argument("--background", choices=COLORS, required=True)
    parser.add_argument("--clean", type=Path, required=True)
    parser.add_argument("--captioned", type=Path, required=True)
    parser.add_argument("--timeline", type=Path, required=True)
    parser.add_argument("--allow-quiet-audio", action="store_true", help="Use only for an intentionally silent visual draft.")
    args = parser.parse_args()

    expected = (PROFILES[args.format]["width"], PROFILES[args.format]["height"])
    failures: list[str] = []
    for label, video in (("clean", args.clean), ("captioned", args.captioned)):
        failures.extend(f"{label}: {issue}" for issue in video_checks(video, expected))

    clean_manifest, caption_manifest = read_manifest(args.clean), read_manifest(args.captioned)
    if not clean_manifest:
        failures.append(f"clean: missing or invalid manifest {args.clean.with_suffix('.render.json').name}; re-run compose_reel.py")
    elif clean_manifest.get("format") != args.format or clean_manifest.get("background") != args.background or clean_manifest.get("background_hex") != COLORS[args.background]:
        failures.append("clean: manifest does not match the requested format/background token")
    if not caption_manifest:
        failures.append(f"captioned: missing or invalid manifest {args.captioned.with_suffix('.render.json').name}; re-run make_subtitles.py")
    elif caption_manifest.get("format") != args.format or caption_manifest.get("caption_style") != CAPTION_STYLE:
        failures.append("captioned: manifest does not match the fixed approved caption style")

    failures.extend(f"captions: {issue}" for issue in caption_clearance_issues(args.timeline, args.format))
    load()
    if os.getenv("ELEVENLABS_MODEL") != "eleven_v4":
        failures.append("voice: ELEVENLABS_MODEL must be exactly eleven_v4 in .env")

    audio_status = "audio present and audible"
    if not failures:
        volume = mean_volume_db(args.captioned)
        if volume is None and not args.allow_quiet_audio:
            failures.append("audio: silent or unreadable; create narration before final delivery")
        elif volume is None:
            print("Audio: intentionally silent draft accepted by --allow-quiet-audio")
            audio_status = "intentionally silent draft"
        elif volume < MIN_MEAN_VOLUME_DB and not args.allow_quiet_audio:
            failures.append(f"audio: mean volume is {volume:.1f} dBFS (minimum is {MIN_MEAN_VOLUME_DB:.0f} dBFS)")
        else:
            print(f"Audio mean volume: {volume:.1f} dBFS")
            if volume < MIN_MEAN_VOLUME_DB:
                audio_status = "intentionally quiet draft"

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(1)
    print(f"PASS preflight: {args.format} {expected[0]}x{expected[1]}, {args.background} ({COLORS[args.background]}), eleven_v4, clean + captioned exports, caption safe area, {audio_status}")


if __name__ == "__main__":
    main()
