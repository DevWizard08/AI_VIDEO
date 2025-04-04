import os
import tempfile
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
        
        # ✅ Create a temp file path for audio
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, "story_audio_temp.mp3")

        # ✅ Save audio to this path
        audio_bytes = b"".join(audio_generator)
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)

        return True, temp_audio_path

    except Exception as e:
        return False, str(e)
