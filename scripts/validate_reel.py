#!/usr/bin/env python3
"""Validate the non-negotiable technical delivery requirements for a reel."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path


def probe(path: Path) -> dict:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True)
    if result.returncode: raise ValueError(result.stderr.strip())
    return json.loads(result.stdout)


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[1] != "--format" or sys.argv[2] not in {"instagram", "linkedin"}:
        raise SystemExit("Usage: validate_reel.py --format instagram|linkedin FILE [FILE ...]")
    profile = sys.argv[2]
    expected = (1080, 1920) if profile == "instagram" else (1080, 1350)
    failed = False
    for raw in sys.argv[3:]:
        path = Path(raw)
        try:
            data = probe(path); streams = data["streams"]; video = next(s for s in streams if s["codec_type"] == "video"); audio = next((s for s in streams if s["codec_type"] == "audio"), None); duration = float(data["format"].get("duration", 0))
            errors = []
            if (int(video["width"]), int(video["height"])) != expected: errors.append(f"expected {expected[0]}x{expected[1]}, got {video['width']}x{video['height']}")
            if duration > 40: errors.append(f"must be <= 40s, got {duration:.1f}s")
            if not audio: errors.append("missing audio stream")
            if errors:
                failed = True; print(f"FAIL {path}: " + "; ".join(errors))
            else: print(f"PASS {path}: {expected[0]}x{expected[1]}, {duration:.1f}s, audio present")
        except Exception as exc:
            failed = True; print(f"FAIL {path}: {exc}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__": main()
