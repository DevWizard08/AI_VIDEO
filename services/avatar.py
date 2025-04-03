import os

AVATAR_OUTPUT_PATH = "static/avatar/avatar_video.mp4"
os.makedirs("static/avatar", exist_ok=True)

def generate_avatar_video(audio_path):
    try:
        # Temporary disabled avatar generation
        return False, "Avatar generation is currently disabled."
    except Exception as e:
        return False, str(e)
