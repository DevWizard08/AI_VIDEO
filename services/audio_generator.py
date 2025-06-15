import os
import io
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVEN_API_KEY = os.getenv("API_SECRET_KEY")
client = ElevenLabs(api_key=ELEVEN_API_KEY)

def generate_audio_from_text(story_text, voice_uid):
    try:
        audio_generator = client.text_to_speech.convert(
            text=story_text,
            voice_id=voice_uid,
            model_id="eleven_multilingual_v2",
            optimize_streaming_latency=1,
            output_format="mp3_44100_128"
        )

        # Collect bytes and return BytesIO object
        audio_bytes = b"".join(audio_generator)
        audio_buffer = io.BytesIO(audio_bytes)
        audio_buffer.seek(0)

        return True, audio_buffer

    except Exception as e:
        return False, str(e)
