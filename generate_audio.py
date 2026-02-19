import os
from datetime import datetime
from openai import OpenAI


def text_to_audio(text, output_dir="output", voice="nova"):
    """Convert text to audio using OpenAI TTS.

    Args:
        text: The text to speak
        output_dir: Directory to save the audio file
        voice: OpenAI voice to use (alloy, echo, fable, onyx, nova, shimmer)
    """
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(output_dir, f"{date_str}-briefing.mp3")

    client = OpenAI()

    # OpenAI TTS has a 4096 char limit per request, so we chunk the text
    chunks = _split_text(text, max_chars=4000)
    temp_files = []

    for i, chunk in enumerate(chunks):
        temp_path = os.path.join(output_dir, f"_chunk_{i}.mp3")
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=chunk,
            response_format="mp3",
        )
        response.write_to_file(temp_path)
        temp_files.append(temp_path)

    if len(temp_files) == 1:
        os.rename(temp_files[0], filepath)
    else:
        _concat_audio(temp_files, filepath)
        for f in temp_files:
            os.remove(f)

    return filepath


def _split_text(text, max_chars=4000):
    """Split text into chunks at sentence boundaries."""
    chunks = []
    current = ""
    for sentence in text.replace("\n", " ").split(". "):
        candidate = current + sentence + ". "
        if len(candidate) > max_chars and current:
            chunks.append(current.strip())
            current = sentence + ". "
        else:
            current = candidate
    if current.strip():
        chunks.append(current.strip())
    return chunks


def _concat_audio(files, output_path):
    """Concatenate multiple MP3 files using ffmpeg, or raw concatenation as fallback."""
    import subprocess
    list_path = output_path + ".txt"
    with open(list_path, "w") as f:
        for path in files:
            f.write(f"file '{os.path.abspath(path)}'\n")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
             "-c", "copy", output_path],
            check=True, capture_output=True,
        )
    except FileNotFoundError:
        # ffmpeg not installed — MP3 frames are self-contained so raw concat works
        with open(output_path, "wb") as out:
            for path in files:
                with open(path, "rb") as inp:
                    out.write(inp.read())
    finally:
        os.remove(list_path)
