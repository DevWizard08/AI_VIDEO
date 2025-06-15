from flask import Blueprint, request, jsonify
from services.audio_generator import generate_audio_from_text
from services.video_generator import generate_video_with_dynamic_text
from services.upload import upload_to_cloudinary
from models.generated_video import GeneratedVideo
from flask_jwt_extended import jwt_required
import asyncio
import io
import concurrent.futures

generate_av_bp = Blueprint('generate_av', __name__)

# Helper to run sync function in async
def run_sync(func, *args):
    loop = asyncio.get_event_loop()
    return loop.run_in_executor(None, func, *args)

@generate_av_bp.route('/generate-av', methods=['POST'])
@jwt_required()
def generate_av():
    data = request.get_json()

    story_text = data.get("text")
    background_video_url = data.get("video_url")
    voice_id = data.get("voice_id")

    if not story_text or not voice_id:
        return jsonify({"error": "Please provide both 'text' and 'voice_id' in the JSON payload"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(process_av(story_text, voice_id, background_video_url))
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Unexpected error", "detail": str(e)}), 500
    finally:
        loop.close()

async def process_av(text, voice_id, video_url):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Run audio generation concurrently
        audio_task = asyncio.get_event_loop().run_in_executor(
            executor, generate_audio_from_text, text, voice_id
        )

        # Wait for audio to finish
        success_audio, audio_buffer_or_err = await audio_task
        if not success_audio:
            return {"error": "Audio generation failed", "detail": audio_buffer_or_err}

        audio_bytes = audio_buffer_or_err.getvalue()  # Get raw bytes from BytesIO

        # Now generate video with audio bytes
        success_video, video_buffer_or_err = await asyncio.get_event_loop().run_in_executor(
            executor, generate_video_with_dynamic_text, text, video_url, audio_bytes
        )
        if not success_video:
            return {"error": "Video generation failed", "detail": video_buffer_or_err}

        # Upload both audio and video buffers to cloud
        upload_audio_task = asyncio.get_event_loop().run_in_executor(
            executor, upload_to_cloudinary, audio_buffer_or_err, "audio"
        )
        upload_video_task = asyncio.get_event_loop().run_in_executor(
            executor, upload_to_cloudinary, video_buffer_or_err, "video"
        )

        audio_url, video_url = await asyncio.gather(upload_audio_task, upload_video_task)

        # Save video metadata
        video_id = GeneratedVideo.save_video(audio_url, video_url, text)

        return {
            "success": True,
            "video_id": video_id,
            "audio_url": audio_url,
            "video_url": video_url
        }
