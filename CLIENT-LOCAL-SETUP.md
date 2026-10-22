# Her AI Social Reels — Local Setup for macOS

This guide lets you run the Her AI Social Reels kit on your own Mac. It supports simulated demos and public website demos first. Logged-in demos require extra privacy checks.

## What you need

- A Mac running macOS.
- The `her-ai-social-reels` delivery folder.
- A Terminal app.
- An ElevenLabs account and API key. The approved NL and EN voice IDs are already in `.env.example`.
- A local coding assistant such as Claude Code or Codex if you want help running the commands. Claude in a web browser can write briefs and scripts, but cannot perform the local recording and video-rendering steps.

## 1. Put the project in Documents

1. Unzip the delivery folder.
2. Move `her-ai-social-reels` to your Documents folder.
3. Open **Terminal**.
4. Run:

```bash
cd /Users/YOUR-MAC-USERNAME/Documents/her-ai-social-reels
```

Replace `YOUR-MAC-USERNAME` with your Mac account name. You can type `whoami` in Terminal to find it.

## 2. Install the local tools

You need Python, FFmpeg, and a Playwright browser.

If you do not already have Homebrew, install it from https://brew.sh. Then run:

```bash
brew install python ffmpeg
```

Install the project’s Python packages and browser support:

```bash
python3 -m pip install requests python-dotenv playwright pillow
python3 -m playwright install chromium
```

Check the installation:

```bash
python3 --version
ffmpeg -version
```

## 3. Add your ElevenLabs credentials privately

1. In Finder, duplicate `.env.example`.
2. Rename the copy to `.env`.
3. Open `.env` in a text editor and add your real API key. The approved Dutch and English voice IDs are already filled in:

```text
ELEVENLABS_API_KEY=your_real_key
ELEVENLABS_VOICE_ID_NL=3X7ciUtPZSohy2ElIALt
ELEVENLABS_VOICE_ID_EN=6Q9ThX6ZrbuYesPiCMhN
ELEVENLABS_MODEL=eleven_v4
```

Never email, upload, commit, or paste the real `.env` file into a chat.

## 4. Run a safe first test

Start with a **simulated** or **public** demo. Do not start with a signed-in account.

Use the intake template in `DEMO-INTAKE-TEMPLATE.md` to prepare the reel brief. Then ask your local coding assistant to create the project, script, recording plan, and draft.

To test the existing local simulation in a browser:

```bash
open projects/02-claude-current-chat-context/working/simulation.html
```

Finished videos appear in each project’s `deliverables/` folder.

## 5. Public website demos

Use only websites that do not require login and do not contain private data. The public recorder can automate navigation, visible typing, clicking, and scrolling.

## 6. Signed-in demos: privacy rules

For ChatGPT, Claude, or another logged-in tool:

1. Log in yourself before the recording begins.
2. Open a **new browser window** with only one tab: the approved demo tool.
3. Never show passwords, API keys, profile photos, names, emails, private conversations, account settings, notifications, browser history, or other tabs.
4. Use only safe test prompts and an empty/demo workspace.
5. Review the recording before export. Re-record where possible; otherwise mark any necessary areas for blur.

Never share your password, cookies, browser profile, recovery codes, or active session with anyone.

## 7. Where to find output files

Each reel is stored in:

```text
projects/<reel-name>/deliverables/
```

There are normally two files:

- `...-clean.mp4` — narration and branding without burned-in captions
- `...-captioned.mp4` — narration, branding, and captions

## If something does not work

- **`ffmpeg: command not found`**: run `brew install ffmpeg`.
- **Browser recording fails**: run `python3 -m playwright install chromium` again.
- **No voice generated**: check that `.env` exists, that the API key is correct, and that it has `ELEVENLABS_VOICE_ID_NL` and `ELEVENLABS_VOICE_ID_EN`.
- **A video is slow to generate**: screen recording runs in real time; captions and final rendering add extra time. Start with a short simulation or public demo.
