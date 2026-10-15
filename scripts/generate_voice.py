#!/usr/bin/env python3
"""Generate ElevenLabs narration sentence-by-sentence and write cue timings."""
from __future__ import annotations

import argparse, json, os, re, subprocess
from pathlib import Path
import requests

from load_keys import load


def duration(path: Path) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(path)], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--timeline", type=Path)
    ap.add_argument("--pause", type=float, default=.35)
    args = ap.parse_args()
    load()
    key, voice = os.getenv("ELEVENLABS_API_KEY"), os.getenv("ELEVENLABS_VOICE_ID")
    if not key or not voice:
        raise SystemExit("Set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID in .env or the environment.")
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", args.script.read_text(encoding="utf-8").replace("\n", " ")) if s.strip()]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    clips, timeline, now = [], [], .30
    for i, sentence in enumerate(sentences, 1):
        output = args.out_dir / f"{i:02d}.mp3"
        response = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}", headers={"xi-api-key": key, "Content-Type": "application/json"}, json={"text": sentence, "model_id": os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"), "voice_settings": {"stability": .5, "similarity_boost": .75}}, timeout=90)
        response.raise_for_status()
        output.write_bytes(response.content)
        clip_duration = duration(output)
        timeline.append({"id": f"{i:02d}", "start": round(now, 3), "end": round(now + clip_duration, 3), "voice_text": sentence, "caption_text": sentence})
        now += clip_duration + args.pause
        clips.append(output)
    # Keep the exported narration and caption timeline in sync by embedding the
    # same pause that was included in the cue timings between sentences.
    pause_clip = args.out_dir / "pause.mp3"
    if len(clips) > 1 and args.pause > 0:
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-t", str(args.pause), "-c:a", "libmp3lame", str(pause_clip),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    manifest_entries = []
    for index, clip in enumerate(clips):
        manifest_entries.append(f"file '{clip.resolve()}'")
        if index < len(clips) - 1 and pause_clip.exists():
            manifest_entries.append(f"file '{pause_clip.resolve()}'")
    manifest = args.out_dir / "concat.txt"
    manifest.write_text("\n".join(manifest_entries) + "\n", encoding="utf-8")
    narration = args.out_dir / "narration.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(manifest), "-c:a", "libmp3lame", str(narration)], check=True)
    timeline_path = args.timeline or args.script.parent / "timeline.json"
    timeline_path.write_text(json.dumps(timeline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {narration} and {timeline_path}. Review pronunciation before recording.")


if __name__ == "__main__":
    main()
