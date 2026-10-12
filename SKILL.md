---
name: her-ai-social-reels
description: Produce a short Her AI-branded vertical educational demo reel from an approved brief and screen recording. Use for Instagram, TikTok, or LinkedIn reels explaining how AI tools and LLMs work, including limitations and bias. Do not use for presenter/avatar videos or horizontal WAI Makers-style explainers.
---

# Her AI Social Reels

Create a concise, screen-led social video: narration, a clearly paced tool demo, captions, and a branded end card. Render platform-specific layouts from the same approved master. Maximum runtime is **40 seconds**.

## Required inputs

- An approved `brief.md` in `projects/<slug>/`.
- A selected background: `orange`, `light-green`, or `dark-green`.
- A requested delivery profile: `instagram` (1080×1920, 9:16), `linkedin` (1080×1350, 4:5), or both.
- An approved English or Dutch narration script.
- A tool URL/app and exact demo steps.
- A legitimate local recording path for login-protected tools; never request passwords, browser profiles, cookies, or session files.

Brand-specific assets live under `assets/brand/`; read `assets/brand/README.md` when selecting them. Until approved production exports are added to `assets/logo/`, `assets/backgrounds/`, and `assets/brand/accents/`, use only the neutral fallback styling and flag the output as a draft. The SVG brandbook pages are reference material, not render assets.

## Workflow

1. Read the brief. Keep one educational claim and one visible proof. If the claim concerns product behaviour, verify the exact state in the recording rather than relying on generic model knowledge.
2. Draft or revise the script with `scripts/generate_script.py`. Aim for 70–85 words and use hook → demonstration → takeaway → brief CTA.
3. Generate narration and `timeline.json` using `scripts/generate_voice.py`. Review pronunciation before recording a final take.
4. Capture the demo:
   - Use `record_public_demo.py` for public sites.
   - For a signed-in product, start already logged in, record locally, and use `record_logged_in_demo.py` only for scripted post-login actions.
5. Use the narration timeline to trim/pace the demo so actions occur while the related sentence is spoken. Do not show sensitive data, browser chrome, unrelated tabs, or login details.
6. Render each requested platform composition with `compose_reel.py`, then add captions with `make_subtitles.py`. Never crop a finished Instagram export into LinkedIn format; recompose from the source screen recording so type and UI remain legible.
7. Run `validate_reel.py` on every MP4. Deliver only if each file matches its platform profile, has audio, and is no longer than 40 seconds.

## Visual rules

- Screen recording is the visual focus; do not add an avatar or presenter.
- Keep the UI large and crop/zoom to the action rather than shrinking a whole desktop into the frame.
- Keep captions above platform controls and clear of relevant UI.
- Use the green wiggly/drawn element sparingly as an accent. Do not invent a replacement logo or permanent brand artwork.
- End on a simple 2–3 second branded card with one takeaway and optional CTA.

## Secrets and approvals

Load keys from environment variables or the project `.env`; never commit keys or embed them in client-side code. Confirm the final script, chosen voice, visible data, captions, language, and final exports with the approval owner.

## Commands

```bash
python3 scripts/generate_script.py --brief projects/<slug>/brief.md --language en
python3 scripts/generate_voice.py --script projects/<slug>/script.en.txt --out-dir projects/<slug>/working/narration
python3 scripts/compose_reel.py --screen projects/<slug>/working/screen_edit.mp4 --audio projects/<slug>/working/narration/narration.mp3 --timeline projects/<slug>/timeline.json --background orange --format instagram --out projects/<slug>/deliverables/reel-instagram-clean.mp4
python3 scripts/make_subtitles.py --input projects/<slug>/deliverables/reel-instagram-clean.mp4 --timeline projects/<slug>/timeline.json --format instagram --out projects/<slug>/deliverables/reel-instagram-captioned.mp4
python3 scripts/compose_reel.py --screen projects/<slug>/working/screen_edit.mp4 --audio projects/<slug>/working/narration/narration.mp3 --timeline projects/<slug>/timeline.json --background orange --format linkedin --out projects/<slug>/deliverables/reel-linkedin-clean.mp4
python3 scripts/make_subtitles.py --input projects/<slug>/deliverables/reel-linkedin-clean.mp4 --timeline projects/<slug>/timeline.json --format linkedin --out projects/<slug>/deliverables/reel-linkedin-captioned.mp4
python3 scripts/validate_reel.py --format instagram projects/<slug>/deliverables/reel-instagram-clean.mp4 projects/<slug>/deliverables/reel-instagram-captioned.mp4
python3 scripts/validate_reel.py --format linkedin projects/<slug>/deliverables/reel-linkedin-clean.mp4 projects/<slug>/deliverables/reel-linkedin-captioned.mp4
```
