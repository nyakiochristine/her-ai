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
- A selected background: `orange`, `light-green`, or `dark-green`.
- A requested delivery profile: `instagram` (1080×1920, 9:16), `linkedin` (1080×1350, 4:5), or both.
- An approved English or Dutch narration script.
- A tool URL/app and exact demo steps.
- A legitimate local recording path for login-protected tools; never request passwords, browser profiles, cookies, or session files.
- A recording mode: `live-public`, `live-signed-in`, or `simulated`.

Brand-specific assets live under `assets/brand/`; read `assets/brand/README.md` when selecting them. Until approved production exports are added to `assets/logo/`, `assets/backgrounds/`, and `assets/brand/accents/`, use only the neutral fallback styling and flag the output as a draft. The SVG brandbook pages are reference material, not render assets.

## Workflow

1. Read `references/demo-reels-brief.md`, then the project brief. Keep one educational claim and one visible proof. If the claim concerns product behaviour, verify the exact state in the recording rather than relying on generic model knowledge.
2. Draft or revise the script with `scripts/generate_script.py`. Use the approved six beats: hook (0–4), demo (4–18), twist (18–22), why (22–32), takeaway (32–37), invite (37–40). Aim for 80–90 words, sentences of 12 words or fewer, and precise language such as “predicts”, “was trained”, or “uses a tool”.
3. Generate narration and `timeline.json` using `scripts/generate_voice.py`. Review pronunciation before recording a final take.
4. Capture the demo:
   - Use `record_public_demo.py` for public sites.
   - For a signed-in product, use **client-led live demo mode**: the client logs in themselves, opens the approved tool, and confirms the exact actions and visible data before control begins. Use `record_logged_in_demo.py` only for scripted post-login actions.
   - During client-led live demo mode, operate only in the agreed tool and workspace. Do not view, request, store, or export passwords, cookies, browser profiles, API keys, recovery codes, payment data, private chats, or unrelated client data. Do not publish, delete, change billing, invite users, or alter account settings unless the client gives a specific visible approval for that action.
   - For `simulated`, build a local generic interface from an approved simulation brief, then record that local page. It must visibly say `Illustrative simulation` or `Example interaction`; never present invented output as a live tool result.
5. Use the narration timeline to trim/pace the demo so actions occur while the related sentence is spoken. Do not show sensitive data, browser chrome, unrelated tabs, or login details.
6. Render each requested platform composition with `compose_reel.py`, then add captions with `make_subtitles.py`. Never crop a finished Instagram export into LinkedIn format; recompose from the source screen recording so type and UI remain legible.
7. Run `validate_reel.py` on every MP4. Deliver only if each file matches its platform profile, has audio, and is no longer than 40 seconds.

## Visual rules

- Screen recording is the visual focus; do not add an avatar or presenter.
- Keep the UI large and crop/zoom to the action rather than shrinking a whole desktop into the frame.
- Keep captions above platform controls and clear of relevant UI.
- Use the green wiggly/drawn element sparingly as an accent. Do not invent a replacement logo or permanent brand artwork.
- Use a single green wiggle only, beneath the selected highlight phrase when it appears in captions.
- End at 37–40 seconds on the approved branded card. Until Saskia supplies the final artwork, use the approved placeholder text: `Workshops & webinars · workshop.herai.work`.

## Secrets and approvals

Load keys from environment variables or the project `.env`; never commit keys or embed them in client-side code. Confirm the final script, chosen voice, visible data, captions, language, and final exports with the approval owner.

For a client-led live demo, use `projects/<slug>/client-demo-session.md` as the consent checklist. The client completes the pre-session steps, keeps control of login, and confirms the demo is safe to record before the demonstration begins.

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
