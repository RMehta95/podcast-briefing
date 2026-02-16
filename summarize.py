import os
from datetime import datetime
import anthropic


def generate_summary(episodes):
    """Generate a daily briefing script from episode descriptions using Claude."""
    if not episodes:
        return None

    # Build episode context
    episode_text = ""
    for ep in episodes:
        episode_text += f"\n--- {ep['podcast']}: {ep['title']} ---\n"
        episode_text += f"{ep['description']}\n"

    client = anthropic.Anthropic()

    prompt = f"""You are a podcast briefing host. Create a daily audio briefing script from these recent podcast episodes.

Rules:
- Maximum 2000 words (about 15 minutes when spoken aloud)
- Use a conversational, engaging tone as if you're a morning show host
- Organize by topic/theme, NOT by individual podcast
- Attribute insights to their source podcast naturally (e.g., "According to The Journal..." or "As discussed on All-In...")
- Start with a brief greeting and date
- End with a brief sign-off
- Focus on the most interesting and important stories
- Do NOT use any markdown formatting, bullet points, or special characters — this will be read aloud by text-to-speech
- Write in natural spoken English with clear sentence structure

Today's date: {datetime.now().strftime('%A, %B %d, %Y')}

Recent podcast episodes:
{episode_text}"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def save_summary(text, output_dir="output"):
    """Save summary text to a dated file."""
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(output_dir, f"{date_str}-summary.txt")
    with open(filepath, "w") as f:
        f.write(text)
    return filepath
