# Podcast Briefing

A daily podcast summary tool that fetches new episodes from your favorite podcasts, generates a concise briefing using Claude, and converts it to audio you can listen to on the go.

## How It Works

1. **Fetch** — Pulls RSS feeds from your configured podcasts and finds episodes published in the last 24 hours
2. **Summarize** — Sends episode titles and descriptions to Claude, which generates a ~15 minute conversational briefing organized by topic
3. **Audio** — Converts the summary to an M4A audio file using macOS text-to-speech (Zoe Premium voice)
4. **Sync** — Copies the audio file to iCloud Drive so you can listen on your iPhone

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your Anthropic API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

Run manually:

```bash
source .venv/bin/activate
python3 main.py
```

The output files are saved to `output/` and copied to `iCloud Drive/Podcast Briefings/`.

## Scheduling

The project is designed to run daily at 5:30am PT via macOS `launchd`. To install the launch agent:

```bash
cp com.rohanmehta.podcast-briefing.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.rohanmehta.podcast-briefing.plist
```

Unlike cron, `launchd` will run missed jobs when your Mac wakes up.

## Configuring Podcasts

Edit `podcasts.json` to add or remove podcasts:

```json
{
  "name": "Podcast Name",
  "feed_url": "https://example.com/rss-feed-url"
}
```
