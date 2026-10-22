# Her AI Social Reels — client runbook

This folder produces short Her AI educational demo reels for LinkedIn and Instagram. Each reel can include a real screen demonstration, an ElevenLabs voice-over, captions, and a branded end card.

## Before you begin

You need:

- A Mac with Python 3, FFmpeg, and Playwright installed.
- An ElevenLabs account and API key. The approved NL and EN voice IDs are already in `.env.example`.
- Permission to demonstrate the selected tool.
- A final script approved by Saskia.
- A safe demo account or workspace for anything requiring a login.

Never share passwords, browser profiles, cookies, recovery codes, billing details, or API keys in messages.

## First-time setup

1. Unzip the delivery folder.
2. Open the `her-ai-social-reels` folder in your coding workspace.
3. Duplicate `.env.example` and rename the copy to `.env`.
4. Add your own API key to `.env`. The approved Dutch and English voice IDs are already filled in:

```text
ELEVENLABS_API_KEY=your_key_here
ELEVENLABS_VOICE_ID_NL=3X7ciUtPZSohy2ElIALt
ELEVENLABS_VOICE_ID_EN=6Q9ThX6ZrbuYesPiCMhN
ELEVENLABS_MODEL=eleven_v4
```

5. Keep `.env` private. Do not upload it, email it, or commit it to GitHub.
6. In Terminal, inside this folder, install the required Python packages if they are not already present:

```bash
python3 -m pip install requests python-dotenv playwright pillow
python3 -m playwright install chromium
```

You also need FFmpeg. On a Mac with Homebrew:

```bash
brew install ffmpeg
```

## Creating a new reel

1. Copy an existing project folder such as `projects/01-it-doesnt-remember-you`.
2. Rename it with a short clear name, for example `projects/02-ai-calculator`.
3. Update `brief.md` with the tool, setting, exact prompt, background colour, and expected result.
4. Read `references/demo-reels-brief.md` before changing the script. It contains the approved her/ai structure and tone.
5. Get Saskia’s approval for the script before recording or generating the final voice.

### Choose a demo mode

- `live-public`: a real public website is recorded automatically with Playwright.
- `live-signed-in`: you log in yourself; the approved visible demo is recorded locally.
- `simulated`: a local, scripted interface illustrates a concept without accessing the real tool. Use this for workshops, sensitive tools, or repeatable examples. Every simulated reel must display `Illustrative simulation` or `Example interaction` and must not claim an invented result happened live.

Use `references/simulated-demo.example.json` as the starting brief for a simulation.

## First message in a new Codex chat

Copy, complete, and send this message when you want to make a reel:

```text
Create a new Her AI social reel.

Recording mode: live-public / live-signed-in / simulated
Tool or interface: [name and URL if public]
What should the viewer learn: [one clear message]
What should happen on screen: [exact steps]
Exact prompt(s): [text to type]
Expected live result or simulated response: [text]
Background: bright-green (#28B87A) / light-green (#BEE9D4) / dark-green (#0D403B) / beige (#F1E9DF) / orange (#D96A3A)
Format: LinkedIn / Instagram / both
Language: English / Dutch

Please create the project brief, script, recording plan, and approval checklist first. Do not record or generate voice-over until I approve the script.
```

## Faster new-demo request

Send this completed brief to avoid answering questions one by one:

```text
Create a Her AI reel.
Tool/website:
Demo mode: live-public / live-signed-in / simulated
Key lesson:
Exact action or prompt to show:
Audience and language:
Platform: LinkedIn / Instagram / both
Background: bright-green (#28B87A) / light-green (#BEE9D4) / dark-green (#0D403B) / beige (#F1E9DF) / orange (#D96A3A)
Language/voice: Dutch (NL voice) or English (EN voice):
CTA:
For a live demo, details to hide or blur:

Show the script and recording plan together. After I approve them, generate the reel and deliver clean plus captioned MP4 files.
```

## Recording a public website automatically

Use this only for public websites that do not require login or private data.

1. Create an action-plan JSON file based on `references/public-demo-actions.example.json`.
2. Test the action plan once.
3. Run:

```bash
python3 scripts/record_public_demo.py \
  --url https://example.com \
  --actions projects/<your-project>/public-actions.json \
  --out-dir projects/<your-project>/raw
```

Playwright opens the site, performs the approved clicks/typing, and saves a video automatically.

## Recording a logged-in tool

For ChatGPT, Claude, Midjourney, or another private tool:

1. Log in yourself. Do not give the system your password or browser session.
2. Open a **new dedicated browser window** for the recording. Keep only one tab open: the approved demo tool. Do not record from a window containing other tabs, browser history, private chats, email, or notifications.
3. Complete `client-demo-session.md` in the project folder.
4. Use the exact approved prompt and actions only.
5. Record the visible post-login demo and save the raw `.mov` or `.mp4` in `projects/<your-project>/raw/`.
6. Before export, review the full take. Re-record if possible; otherwise provide the timestamps and on-screen areas that need blurring (names, profile photos, email addresses, private messages, file names, notifications, or account details).

For an automated start/stop recorder later, install OBS Studio on the recording Mac and grant it Screen Recording permission. OBS is free; this is an optional upgrade, not required for the first reels.

## Generate narration

After script approval:

```bash
python3 scripts/generate_voice.py \
  --script projects/<your-project>/script.en.txt \
  --out-dir projects/<your-project>/working/narration \
  --timeline projects/<your-project>/timeline.json
```

The voice is chosen from the script name: `script.nl.txt` uses the Dutch voice, `script.en.txt` the English one. Add `--language nl` or `--language en` if the file is named differently.

Listen to `narration.mp3`. Check the voice, pace, and how it pronounces “her/ai” before making final exports.

## Produce the LinkedIn reel

Put your cleaned screen recording at `projects/<your-project>/working/screen_edit.mp4`, then run:

```bash
python3 scripts/compose_reel.py \
  --screen projects/<your-project>/working/screen_edit.mp4 \
  --audio projects/<your-project>/working/narration/narration.mp3 \
  --timeline projects/<your-project>/timeline.json \
  --background dark-green \
  --format linkedin \
  --title "Your reel title" \
  --out projects/<your-project>/deliverables/reel-linkedin-clean.mp4
```

Create captions:

```bash
python3 scripts/make_subtitles.py \
  --input projects/<your-project>/deliverables/reel-linkedin-clean.mp4 \
  --timeline projects/<your-project>/timeline.json \
  --format linkedin \
  --out projects/<your-project>/deliverables/reel-linkedin-captioned.mp4
```

The temporary end card says `Workshops & webinars · workshop.herai.work`. Replace it with Saskia’s approved end-card artwork before public delivery.

## Final checks

Run this once for each clean/captioned pair:

```bash
python3 scripts/preflight_reel.py \
  --format linkedin \
  --background dark-green \
  --clean projects/<your-project>/deliverables/reel-linkedin-clean.mp4 \
  --captioned projects/<your-project>/deliverables/reel-linkedin-captioned.mp4 \
  --timeline projects/<your-project>/timeline.json
```

It takes only a few seconds. It does not re-render the video or make an ElevenLabs call. It verifies the dimensions, length, approved background token, `eleven_v4`, paired exports, fixed caption safe area, and audio level. Use `--allow-quiet-audio` only for an intentionally silent visual draft.

Before posting, check:

- the demo result is real and matches the voice-over;
- recording was made from a new dedicated browser window with only the approved demo tab open;
- no private details, notifications, unrelated tabs, or browser history are visible;
- any unavoidable personal details have been approved for blurring and checked after the final export;
- captions are readable and do not cover important UI;
- the script, voice, language, and end card are approved;
- the final file is under 40 seconds;
- LinkedIn output is 1080 × 1350 and Instagram output is 1080 × 1920.

## If something goes wrong

- **ElevenLabs error:** check that the API key and both `ELEVENLABS_VOICE_ID_NL` and `ELEVENLABS_VOICE_ID_EN` are present in `.env`.
- **Playwright error:** run `python3 -m playwright install chromium` again.
- **No FFmpeg:** install FFmpeg, then restart Terminal.
- **Unexpected AI result:** do not edit or fake it. Test up to three times, then revise or drop the demo.
- **Private content appeared:** stop recording, delete that raw take locally, and make a fresh safe recording.
