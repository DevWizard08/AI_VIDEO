import os
import tempfile
from dotenv import load_dotenv
from moviepy.editor import (
    AudioFileClip, CompositeVideoClip, TextClip,
    VideoFileClip, concatenate_videoclips
)
import librosa
import requests

load_dotenv()
imagemagick_path = os.getenv("IMAGEMAGICK_BINARY")


def download_video_from_url(url, save_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def get_sentence_durations(audio_path, sentences):
    audio_duration = librosa.get_duration(path=audio_path)
    num_words = sum(len(sentence.split()) for sentence in sentences)
    avg_word_duration = audio_duration / max(1, num_words)

    durations = []
    start_time = 0

    for sentence in sentences:
        sentence_words = len(sentence.split())
        sentence_duration = sentence_words * avg_word_duration
        durations.append((sentence, start_time, sentence_duration))
        start_time += sentence_duration

    return durations


def generate_video_with_dynamic_text(story_text, video_url, tts_audio_bytes):
    try:
        # Temporary files
        temp_dir = tempfile.gettempdir()
        downloaded_video_path = os.path.join(temp_dir, "base_video.mp4")
        audio_path = os.path.join(temp_dir, "story.mp3")
        output_video_path = os.path.join(temp_dir, "story_video.mp4")

        # Save TTS audio to temp audio path
        with open(audio_path, "wb") as f:
            f.write(tts_audio_bytes)

        # Download video from provided URL
        download_video_from_url(video_url, downloaded_video_path)

        # Load video and audio
        original_video = VideoFileClip(downloaded_video_path).without_audio()
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration
        original_duration = original_video.duration
        video_width, video_height = original_video.size

        # Repeat or trim video to match audio duration
        if audio_duration > original_duration:
            num_repeats = int(audio_duration // original_duration) + 1
            repeated_clips = [original_video] * num_repeats
            video_clip = concatenate_videoclips(repeated_clips).subclip(0, audio_duration)
        else:
            video_clip = original_video.subclip(0, audio_duration)

        # Generate text overlay
        font_size = int(video_width * 0.05)
        text_width = int(video_width * 0.9)
        sentences = story_text.split(". ")
        sentence_timings = get_sentence_durations(audio_path, sentences)

        text_clips = [
            TextClip(sentence, fontsize=font_size, color='white', font="Leelawadee-UI-Bold", method='caption', size=(text_width, None))
            .set_start(start)
            .set_duration(duration)
            .set_position(("center", video_height * 0.8))
            .fadein(0.5)
            .fadeout(0.5)
            for sentence, start, duration in sentence_timings
        ]

        # Compose final video
        final_clip = CompositeVideoClip([video_clip] + text_clips).set_audio(audio_clip)
        final_clip.write_videofile(output_video_path, fps=24)

        return True, output_video_path

    except Exception as e:
        return False, str(e)
