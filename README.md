# Discord music-bot

A simple Discord bot that plays music from YouTube (via `yt-dlp`).
Every command works both as a classic prefix command (`$play`) and as a slash command (`/play`).

## Project structure

```
src/
  main.py          # entry point
  bot.py           # MusicBot class, cog loading, slash command sync
  config.py        # paths, .env loading, ffmpeg lookup
  voice_utils.py   # shared voice-channel helpers
  cogs/
    music.py       # /play /join /pause /resume /stop /disconnect
    general.py     # /ping
```

## Requirements

- Python 3.10+ (3.13 recommended; discord.py voice needs the `davey` package, which has no wheels for older versions)
- ffmpeg (`ffmpeg.exe` in `venv/Scripts` or on PATH - download from <https://ffmpeg.org/download.html>)
- Packages from `requirements.txt`

## Setup

1. Create the bot application at the [Discord Developer Portal](https://discord.com/developers/applications):
   - click *New Application* and add a *Bot* to it
   - copy the **bot token**
   - in *Bot → Privileged Gateway Intents* enable **Message Content Intent** (needed for `$` prefix commands)
   - invite the bot to your server with the `bot` and `applications.commands` scopes
2. Clone the repository: `git clone https://github.com/MacTii/MusicBOT.git`
3. Create and activate a virtual environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and paste your bot token
6. Run the bot: `python src/main.py`

## Commands

| Command | Description |
| --- | --- |
| `/play <url or search>` | Play audio from a YouTube URL or search phrase |
| `/join` | Join your current voice channel |
| `/pause`, `/resume`, `/stop` | Control playback |
| `/disconnect` | Leave the voice channel |
| `/ping` | Latency check |

All commands also work with the `$` prefix, e.g. `$play never gonna give you up`.

Enjoy your music with bot :D
