import os
import subprocess
from datetime import datetime


def text_to_audio(text, output_dir="output", voice="Zoe (Premium)", rate=175):
    """Convert text to audio using macOS say command.

    Args:
        text: The text to speak
        output_dir: Directory to save the audio file
        voice: macOS voice to use (Samantha is clear and natural)
        rate: Words per minute (default 175, normal speech is ~150-180)
    """
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    aiff_path = os.path.join(output_dir, f"{date_str}-briefing.aiff")
    m4a_path = os.path.join(output_dir, f"{date_str}-briefing.m4a")

    # Generate AIFF first, then convert to M4A
    subprocess.run(
        ["say", "-v", voice, "-r", str(rate), "-o", aiff_path, text],
        check=True,
    )
    subprocess.run(
        ["afconvert", "-f", "m4af", "-d", "aac", aiff_path, m4a_path],
        check=True,
    )
    os.remove(aiff_path)

    return m4a_path


def list_voices():
    """List available macOS voices."""
    result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
    return result.stdout
