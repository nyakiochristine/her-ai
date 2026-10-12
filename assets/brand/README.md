# Her AI brand assets

This directory separates source brand guidance from assets that are safe to render into a reel.

```text
assets/
├── backgrounds/       Approved 1080×1920 reel backgrounds, exported from Figma
├── brand/
│   ├── brandbook/     Source/reference pages — do not render directly into reels
│   │   └── pages/     Ten SVG pages from the Her AI brandbook
│   ├── figma-plugin/  Local Figma token-plugin source
│   └── tokens/        Machine-readable colour, spacing, radius, and type tokens
├── fonts/             Licensed font files approved for rendered video
├── logo/              Approved logo variants for reel use
└── templates/
    └── linkedin/      Wide LinkedIn header/banner templates; not reel canvases
```

## Current source of truth

- Colours, spacing, radius, and typography: `brand/tokens/herai-tokens.json`.
- The original design-system pages: `brand/brandbook/pages/`.
- The Figma import/token instructions: `brand/brandbook/README.md`.

## Available production assets

- `fonts/DM-Sans-Variable.ttf` — source body/caption font. Four supplied DM Sans copies were identical; one canonical file is retained.
- `fonts/MyeongjoExt-Regular.ttf` — display/brand font. Its public-use licence still needs confirmation before delivery.
- `logo/her-ai-primary-transparent.png` — default logo for compositing onto a chosen background.
- `logo/her-ai-primary-dark-green-transparent.png` — dark-green logo variant.
- `logo/her-ai-primary-on-beige.png`, `logo/her-ai-primary-on-green.png`, and `logo/her-ai-icon-on-dark-green.png` — precomposed logo variants; use as supplied, without attempting to remove their backgrounds.
- `templates/linkedin/` — supplied English LinkedIn header/banner imagery. These are wide templates and must not be stretched into the 4:5 LinkedIn video output.

## Production-ready exports still needed

Export these from Figma only after Her AI approves them:

- `backgrounds/orange-1080x1920.png`, `backgrounds/light-green-1080x1920.png`, and `backgrounds/dark-green-1080x1920.png`.
- `brand/accents/brush-green.png` — transparent, reusable green brush/wiggle element.
- Font files only where licensing permits. The brandbook notes that MyeongjoExt licensing must be confirmed; do not distribute it until that is confirmed.

Do not substitute brandbook SVG pages for logos or backgrounds. They are visual documentation, not ready-to-use production artwork.
