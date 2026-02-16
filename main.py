#!/usr/bin/env python3
"""Daily Podcast Briefing — fetches new episodes, summarizes, and generates audio."""

import shutil
import sys
import os
from datetime import datetime

# Ensure the script's directory is in the path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Load .env file
env_path = os.path.join(script_dir, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key, val)

from fetch_episodes import fetch_recent_episodes
from summarize import generate_summary, save_summary
from generate_audio import text_to_audio


def main():
    print(f"=== Podcast Briefing — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

    # Step 1: Fetch recent episodes
    print("Fetching recent episodes...")
    episodes = fetch_recent_episodes(hours=24)
    print(f"Found {len(episodes)} new episodes.\n")

    if not episodes:
        print("No new episodes found. Skipping summary generation.")
        return

    for ep in episodes:
        print(f"  [{ep['podcast']}] {ep['title']}")
    print()

    # Step 2: Generate summary
    print("Generating summary with Claude...")
    summary = generate_summary(episodes)
    if not summary:
        print("Failed to generate summary.")
        return

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    summary_path = save_summary(summary, output_dir)
    print(f"Summary saved to: {summary_path}\n")

    # Step 3: Generate audio
    print("Generating audio...")
    audio_path = text_to_audio(summary, output_dir)
    print(f"Audio saved to: {audio_path}\n")

    # Step 4: Copy to iCloud Drive for iPhone access
    icloud_dir = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Podcast Briefings")
    os.makedirs(icloud_dir, exist_ok=True)
    icloud_path = os.path.join(icloud_dir, os.path.basename(audio_path))
    shutil.copy2(audio_path, icloud_path)
    print(f"Copied to iCloud Drive: {icloud_path}\n")

    print("Done! You can play the briefing with:")
    print(f"  afplay {audio_path}")
    print(f"  Or on iPhone: Files → iCloud Drive → Podcast Briefings")


if __name__ == "__main__":
    main()
