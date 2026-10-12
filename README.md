# Her AI Social Reels

Reusable production kit for screen-led educational AI videos. It uses ElevenLabs narration, local/public demo capture, FFmpeg composition, captions, and a short branded end card. It intentionally excludes avatars and HeyGen.

## Delivery profiles

Each approved reel can be exported twice from the same recording and narration:

| Platform | Format | Size | Use |
| --- | --- | --- | --- |
| Instagram | 9:16 | 1080×1920 | Reels-first master |
| LinkedIn | 4:5 | 1080×1350 | Feed-first version with larger legible UI |

These are separate compositions, not crops of the finished video. Keep essential text, logos, and captions inside each composition’s safe area.

## First setup

1. Copy `.env.example` to `.env` and add the client-controlled ElevenLabs key and approved voice ID.
2. Add approved logo, fonts, background exports, and wiggly accent assets to `assets/` from the Her AI design system.
3. Install local tools: Python 3.10+, FFmpeg, and Playwright for browser recording.
4. Complete the reel brief in `projects/<slug>/brief.md`.

See [SKILL.md](SKILL.md) for the production workflow.

## Brand asset structure

The source brandbook now lives in [`assets/brand/`](assets/brand/README.md). It is separate from render-ready assets so source guidance is preserved while each reel uses only approved exports. The supplied fonts, logos, and LinkedIn banner templates have been filed there. Before a final branded render, add the three vertical reel backgrounds and green brush accent to the locations listed there.
