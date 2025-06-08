import os
import io
import tempfile
import requests
from dotenv import load_dotenv

load_dotenv()

OPEN_TTS_TTS_URL = os.getenv("OPEN_TTS_TTS_URL", "http://localhost:5004/api/tts")


def generate_audio_from_text(story_text: str, voice_uid: str, speaker_idx: int = None) -> tuple[bool, str]:
    """
    Sends a text-to-speech request to the OpenTTS server using query parameters and saves the result to a temp file.

    Args:
        story_text: The text to synthesize.
        voice_uid: The voice identifier from the voices list.
        speaker_idx: Optional numeric speaker index for multispeaker voices.

    Returns:
        (success: bool, path_or_error: str)
    """
    try:
        # Build query params instead of JSON to avoid POST JSON parsing issues
        params = {"text": story_text, "voice": voice_uid}
        if speaker_idx is not None:
            params["speaker"] = speaker_idx

        # Increase read timeout to accommodate longer texts
        resp = requests.get(
            OPEN_TTS_TTS_URL,
            params=params,
            timeout=(5, 120)  # 5s connect, 120s read
        )
        resp.raise_for_status()

        # Save to temp WAV file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "story_audio.wav")
        with open(temp_path, "wb") as f:
            f.write(resp.content)

        return True, temp_path

    except Exception as e:
        return False, str(e)
