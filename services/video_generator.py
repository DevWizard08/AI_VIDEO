import os
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, TextClip,VideoFileClip,concatenate_videoclips 
import librosa


load_dotenv()

VIDEO_OUTPUT_PATH = "static/video/story_video.mp4"
VIDEO_PATH = "static/video/base_video.mp4"  
AUDIO_PATH = "static/audio/story.mp3"       

os.makedirs("static/video", exist_ok=True)

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







def generate_video_with_dynamic_text(story_text):
    try:
        original_video = VideoFileClip(VIDEO_PATH).without_audio()
        original_duration = original_video.duration
        video_width, video_height = original_video.size  



        audio_clip = AudioFileClip(AUDIO_PATH)
        audio_duration = audio_clip.duration

        if audio_duration > original_duration:
            num_repeats = int(audio_duration // original_duration) + 1
            repeated_clips = [original_video] * num_repeats
            video_clip = concatenate_videoclips(repeated_clips)
            video_clip = video_clip.subclip(0, audio_duration)

        else:
            video_clip = original_video.subclip(0, audio_duration)
        

        # Avatar Clip (Temporarily Disabled)
        # avatar_clip = VideoFileClip(avatar_video_path).set_duration(audio_clip.duration)

        # Background Video
        #background_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio_clip.duration)
        font_size = int(video_width * 0.05)  
        text_width = int(video_width * 0.9)  

        # Text Overlay
        sentences = story_text.split(". ")
        sentence_timings = get_sentence_durations(AUDIO_PATH, sentences)

        text_clips = [
            TextClip(sentence, fontsize=font_size, color='white', font="Leelawadee-UI-Bold", method='caption', size=(text_width, None))
            .set_start(start)
            .set_duration(duration)
            .set_position(("center", video_height * 0.8))
            .fadein(0.5)
            .fadeout(0.5)
            for sentence, start, duration in sentence_timings
        ]

        # Merge Background + Text (Without Avatar)
        final_clip = CompositeVideoClip([video_clip] + text_clips).set_audio(audio_clip)

        final_clip.write_videofile(VIDEO_OUTPUT_PATH, fps=24)
        return True, VIDEO_OUTPUT_PATH

    except Exception as e:
        return False, str(e)
