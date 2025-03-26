import os
from dotenv import load_dotenv

load_dotenv()
imagemagick_path = os.getenv("IMAGEMAGICK_BINARY")
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, VideoClip, TextClip

VIDEO_OUTPUT_PATH = "static/video/story_video.mp4"
os.makedirs("static/video", exist_ok=True)

def generate_video_with_dynamic_text(story_text):
    try:
        # Load the generated audio
        audio_clip = AudioFileClip("static/audio/story.mp3")
        duration = audio_clip.duration

        # Create a black background clip
        background_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)

        # **Sentence-wise processing**
        sentences = story_text.split(". ")
        num_sentences = len(sentences)
        sentence_duration = duration / num_sentences  # Equal duration per sentence

        text_clips = []
        for i, sentence in enumerate(sentences):
            start_time = i * sentence_duration
            end_time = start_time + sentence_duration

            txt_clip = (TextClip(sentence, fontsize=50, color='white', font="Leelawadee-UI-Bold",
                                 method='caption', size=(1200, 200))
                        .set_start(start_time)
                        .set_duration(sentence_duration)
                        .set_position(("center", "bottom"))
                        .fadein(0.5)
                        .fadeout(0.5))

            text_clips.append(txt_clip)

        # Merge all clips
        final_clip = CompositeVideoClip([background_clip.set_audio(audio_clip)] + text_clips)

        # Export video
        final_clip.write_videofile(VIDEO_OUTPUT_PATH, fps=24)
        return True, VIDEO_OUTPUT_PATH

    except Exception as e:
        return False, str(e)
