# Her AI Social Reels Production Kit

## Implementation status

**Status:** Working first version / ready for client feedback

This project is a repeatable production kit for short, branded AI-literacy reels. It is designed for LinkedIn and Instagram, with a current target length of **40 seconds or less**. It is inspired by the supplied reference workflow, but is a separate Her AI implementation and does not reuse the reference project's branding, credentials, scripts, or presenter assets.

## What has been implemented

### 1. Her AI project structure and brand assets

- Separate `her-ai-social-reels` project created, without modifying the Waimakers reference project.
- Her AI logos, fonts, colour system, source materials, and LinkedIn templates organised into the project.
- Brand fonts configured:
  - Myeongjo Ext for editorial/display headings
  - DM Sans for readable UI text, captions, and supporting copy
- Reusable Her AI reel design created:
  - bright textured green background
  - dark rounded browser window with browser controls
  - dark-green caption panels
  - branded title and end-card layout

### 2. Reel formats

- LinkedIn portrait output supported at **1080 × 1350**.
- Instagram portrait output supported at **1080 × 1920**.
- Video validator checks the expected dimensions, duration, and audio presence before delivery.

### 3. Script and content workflow

- A structured reel brief, script, recording plan, and timeline are stored per project.
- The first topic developed is: **“Does Claude remember you?”**
- The concept explains that a language model only knows information in the current chat unless a memory feature or connected tool is enabled.
- CTA implemented in the final script:

  > Follow her/ai and sign up for our upcoming workshops for more practical AI literacy.

### 4. ElevenLabs voice-over

- ElevenLabs API key integrated through the local environment file; the key is not committed to Git.
- Voice-over generator implemented.
- Narration uses the ElevenLabs `eleven_v4` model.
- The narration workflow creates:
  - individual narration clips
  - one combined MP3 voice-over
  - a timed JSON timeline for captions
- The current demo includes English AI narration.
- Approved voices are set per language: `ELEVENLABS_VOICE_ID_NL` and `ELEVENLABS_VOICE_ID_EN`. The narration script picks one from the script name or `--language`.

### 5. Captions

- Branded burned-in captions are generated from the narration timeline.
- Captions are placed in a dark-green, rounded Her AI caption bar.
- Caption timings are generated from the same narration sequence, keeping voice and captions aligned.
- Both captioned and clean MP4 versions are exported.

### 6. Screen-recording modes

Three recording approaches are supported:

| Mode | Use case | Current status |
|---|---|---|
| `simulated` | Explain a concept using a clearly labelled illustrative interface | Implemented and tested |
| `live-public` | Record a public website using Playwright automation | Implemented and tested on Wikipedia |
| `live-signed-in` | Record a real tool from a legitimate signed-in browser session | Workflow documented; needs client-side live recording test |

#### Simulated demo

- A Claude-style generic interface has been built for the memory/context example.
- It uses a permanent **“Illustrative simulation”** label.
- It demonstrates a user giving the fact “My favourite fruit is mango” in one chat, then beginning a new chat and asking for the same fact.
- The simulated response makes clear that the information is not in the new conversation.
- The interface is visually familiar but is not presented as an actual live Claude recording.

#### Public website automation

- Playwright recorder built for public, non-sensitive webpages.
- Supports scripted navigation, waiting, clicking, typing, keyboard presses, and scrolling.
- Visible typing animation included.
- Test recording successfully created using Wikipedia.

#### Signed-in tool workflow

- Safe workflow documented for real ChatGPT, Claude, and other login-protected tools.
- The client records from their legitimate signed-in browser session; passwords, browser profiles, and personal sessions are never shared.
- Manual Mac screen recording is supported now.
- OBS can be used later as an optional free upgrade for more automated start/stop recording.

### 7. Branded start-card system

- A playful branded start card has been designed for the Claude memory reel.
- It includes:
  - Her AI logo
  - bright green textured background
  - large reel title
  - “AI literacy, made practical” label
  - simple abstract browser/chat illustration
- A reusable generator is included. For a new reel, only the title, subtitle, and output filename need changing.

Example:

```bash
python3 scripts/create_start_card.py \
  --title "Can AI really do maths?" \
  --subtitle "A quick AI reality check" \
  --out assets/templates/reels/start-card-ai-maths.png
```

### 8. Final rendered prototype

The current completed prototype is a captioned LinkedIn reel:

- Topic: Claude and current-chat context
- Format: 1080 × 1350 LinkedIn portrait
- Duration: 39.7 seconds
- Includes: start card, narration, simulation disclosure, Claude-style demo, captions, CTA, and branded visual styling

Files:

- `projects/02-claude-current-chat-context/deliverables/claude-simulated-linkedin-with-start-card-captioned.mp4`
- `projects/02-claude-current-chat-context/deliverables/claude-simulated-linkedin-with-start-card-clean.mp4`

## Handover and client documentation

- `CLIENT-RUNBOOK.md` explains how a client can run the project after unzipping it.
- `SKILL.md` describes the repeatable production workflow for Codex.
- API credentials are kept in `.env` and must remain client-controlled, excluded from Git, and never placed in the frontend.

## Remaining work before full production use

1. Obtain client approval for the background, title treatment, captions, CTA, start card, and supplied end card.
2. Replace the placeholder end card once the approved client asset is received.
3. ~~Confirm the final ElevenLabs voice ID and Dutch voice requirements.~~ Done: NL and EN voice IDs are in `.env.example`.
4. Complete one real signed-in Claude demo from a safe, empty client session.
5. Test and refine the Instagram 1080 × 1920 layout.
6. Create the next approved topics, for example ChatGPT memory, AI maths/reasoning, and image-generation bias.
7. Complete client handover testing by having the client run a simulated or public demo using the runbook.

## Safety and disclosure rules

- Simulated content must stay visibly labelled as illustrative.
- Do not represent a simulation as an actual tool output.
- Do not ask clients to share passwords, browser sessions, or personal account access.
- Record only safe test data; hide names, notifications, emails, files, and sensitive material before recording.
- Use only client-approved brand assets, scripts, voices, and end cards.
