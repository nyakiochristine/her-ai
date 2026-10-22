---
name: her-ai-social-reels
description: Produce a short Her AI-branded vertical educational demo reel from an approved brief and screen recording. Use for Instagram, TikTok, or LinkedIn reels explaining how AI tools and LLMs work, including limitations and bias. Do not use for presenter/avatar videos or horizontal WAI Makers-style explainers.
---

# Her AI Social Reels

Create a concise, screen-led social video: narration, a clearly paced tool demo, captions, and a branded end card. Render platform-specific layouts from the same approved master. Maximum runtime is **40 seconds**.

## Source of truth

Before creating or revising any Her AI script, read
`references/demo-reels-brief.md`. It is the client-approved source of truth
for content, wording, recording, visual rules, and delivery. The PDFs under
`references/client-source/` preserve the supplied source material. Do not use
the older WAI Makers rules or `references/example-scripts.md` to override it.

Every approved reel must include: title, tool and setting, one exact message,
background colour, 80–90 word voice-over, hook, one highlighted phrase,
pre-recording state, a six-beat timing plan, fallback, and Instagram caption.
Show the script to Saskia for approval before making the final voice-over or
recording.

## Required inputs

- An approved `brief.md` in `projects/<slug>/`.
- A selected background: `bright-green` (`#28B87A`), `light-green` (`#BEE9D4`), `dark-green` (`#0D403B`), `beige` (`#F1E9DF`), or `orange` (`#D96A3A`). These are defined once in `assets/brand/tokens/reel-video-style.json`; do not substitute approximate greens.
- A requested delivery profile: `instagram` (1080×1920, 9:16), `linkedin` (1080×1350, 4:5), or both.
- An approved English or Dutch narration script.
- A tool URL/app and exact demo steps.
- A legitimate local recording path for login-protected tools; never request passwords, browser profiles, cookies, or session files.
- A recording mode: `live-public`, `live-signed-in`, or `simulated`.

Brand-specific assets live under `assets/brand/`; read `assets/brand/README.md` when selecting them. Until approved production exports are added to `assets/logo/`, `assets/backgrounds/`, and `assets/brand/accents/`, use only the neutral fallback styling and flag the output as a draft. The SVG brandbook pages are reference material, not render assets.

## One-shot demo intake

Ask missing content questions together, not one at a time: tool/URL, demo mode, lesson, exact action or prompt, audience/language, platform, background, voice, CTA, and live-demo details to hide or blur. Then show the script and recording plan in one approval message. Once the client approves them, generate the draft without further piecemeal content questions unless an unexpected privacy or safety issue appears.

## Workflow

1. Read `references/demo-reels-brief.md`, then the project brief. Keep one educational claim and one visible proof. If the claim concerns product behaviour, verify the exact state in the recording rather than relying on generic model knowledge.
2. Draft or revise the script with `scripts/generate_script.py`. Use the approved six beats: hook (0–4), demo (4–18), twist (18–22), why (22–32), takeaway (32–37), invite (37–40). Aim for 80–90 words, sentences of 12 words or fewer, and precise language such as “predicts”, “was trained”, or “uses a tool”.
3. Generate narration and `timeline.json` using `scripts/generate_voice.py`. Review pronunciation before recording a final take.
4. Capture the demo:
   - Use `record_public_demo.py` for public sites.
   - For a signed-in product, use **client-led live demo mode**: the client logs in themselves, opens the approved tool in a dedicated clean browser window with only the demo tab, and confirms the exact actions and visible data before control begins. Use `record_logged_in_demo.py` only for scripted post-login actions.
   - During client-led live demo mode, operate only in the agreed tool and workspace. Do not view, request, store, or export passwords, cookies, browser profiles, API keys, recovery codes, payment data, private chats, or unrelated client data. Do not publish, delete, change billing, invite users, or alter account settings unless the client gives a specific visible approval for that action.
   - For `simulated`, build a local generic interface from an approved simulation brief, then record that local page. It must visibly say `Illustrative simulation` or `Example interaction`; never present invented output as a live tool result.
5. Use the narration timeline to trim/pace the demo so actions occur while the related sentence is spoken. Do not show sensitive data, browser chrome, unrelated tabs, or login details. Before final export, inspect the whole recording and blur every approved personal detail that cannot be removed by re-recording.
6. Render each requested platform composition with `compose_reel.py`, then add captions with `make_subtitles.py`. Never crop a finished Instagram export into LinkedIn format; recompose from the source screen recording so type and UI remain legible.
7. Run `preflight_reel.py` on each clean/captioned pair. It checks the format, duration, approved background token, `eleven_v4` configuration, both exports, fixed caption placement below the demo frame, and audio level without re-rendering. Deliver only after it passes.

## Visual rules

- Screen recording is the visual focus; do not add an avatar or presenter.
- Use the fixed caption treatment from `assets/brand/tokens/reel-video-style.json`: DM Sans, white text, dark-green rounded panel, 64 px side margins, and the platform safe-bottom margin. Do not introduce a second subtitle style within a reel or between reels.
- Keep the UI large and crop/zoom to the action rather than shrinking a whole desktop into the frame.
- Keep captions above platform controls and clear of relevant UI.
- Use the green wiggly/drawn element sparingly as an accent. Do not invent a replacement logo or permanent brand artwork.
- Use a single green wiggle only, beneath the selected highlight phrase when it appears in captions.
- End at 37–40 seconds on the approved branded card. Until Saskia supplies the final artwork, use the approved placeholder text: `Workshops & webinars · workshop.herai.work`.

## Secrets and approvals

Load keys from environment variables or the `.env` in the skill root (copy `.env.example`). Voices are per language: `ELEVENLABS_VOICE_ID_NL` for Dutch and `ELEVENLABS_VOICE_ID_EN` for English. `generate_voice.py` picks one from the script name (`script.nl.txt` / `script.en.txt`) or `--language`. Narration uses the ElevenLabs `eleven_v4` model (`ELEVENLABS_MODEL`); v4 does not support SSML; never commit keys or embed them in client-side code. Confirm the final script, chosen voice, visible data, captions, language, and final exports with the approval owner.

For a client-led live demo, use `projects/<slug>/client-demo-session.md` as the consent checklist. The client completes the pre-session steps, keeps control of login, and confirms the demo is safe to record before the demonstration begins.

## Commands

```bash
python3 scripts/generate_script.py --brief projects/<slug>/brief.md --language en
python3 scripts/generate_voice.py --script projects/<slug>/script.en.txt --out-dir projects/<slug>/working/narration
# Dutch reel: script.nl.txt automatically uses the NL voice
python3 scripts/generate_voice.py --script projects/<slug>/script.nl.txt --out-dir projects/<slug>/working/narration
python3 scripts/compose_reel.py --screen projects/<slug>/working/screen_edit.mp4 --audio projects/<slug>/working/narration/narration.mp3 --timeline projects/<slug>/timeline.json --background orange --format instagram --out projects/<slug>/deliverables/reel-instagram-clean.mp4
python3 scripts/make_subtitles.py --input projects/<slug>/deliverables/reel-instagram-clean.mp4 --timeline projects/<slug>/timeline.json --format instagram --out projects/<slug>/deliverables/reel-instagram-captioned.mp4
python3 scripts/compose_reel.py --screen projects/<slug>/working/screen_edit.mp4 --audio projects/<slug>/working/narration/narration.mp3 --timeline projects/<slug>/timeline.json --background orange --format linkedin --out projects/<slug>/deliverables/reel-linkedin-clean.mp4
python3 scripts/make_subtitles.py --input projects/<slug>/deliverables/reel-linkedin-clean.mp4 --timeline projects/<slug>/timeline.json --format linkedin --out projects/<slug>/deliverables/reel-linkedin-captioned.mp4
python3 scripts/validate_reel.py --format instagram projects/<slug>/deliverables/reel-instagram-clean.mp4 projects/<slug>/deliverables/reel-instagram-captioned.mp4
python3 scripts/validate_reel.py --format linkedin projects/<slug>/deliverables/reel-linkedin-clean.mp4 projects/<slug>/deliverables/reel-linkedin-captioned.mp4
python3 scripts/preflight_reel.py --format linkedin --background orange --clean projects/<slug>/deliverables/reel-linkedin-clean.mp4 --captioned projects/<slug>/deliverables/reel-linkedin-captioned.mp4 --timeline projects/<slug>/timeline.json
```
