from flask import Blueprint, request, jsonify
from services.audio_generator import generate_audio_from_text
from services.video_generator import generate_video_with_dynamic_text
from services.upload import upload_to_cloudinary
from models.generated_video import GeneratedVideo

generate_av_bp = Blueprint('generate_av', __name__)

@generate_av_bp.route('/generate-av', methods=['POST'])
def generate_av():
    data = request.get_json()

    story_text = data.get("text")
    background_video_url = data.get("video_url")  # background video
    voice_id = data.get("voice_id")

    if not story_text or not voice_id:
        return jsonify({"error": "Please provide both 'text' and 'voice_id' in the JSON payload"}), 400

    # 1. Generate Audio from dynamic voice
    success, audio_result = generate_audio_from_text(story_text, voice_id)
    if not success:
        return jsonify({"error": "Audio generation failed", "detail": audio_result}), 500

    # 2. Generate Video using background video and story
    success, final_video_result = generate_video_with_dynamic_text(story_text, background_video_url)
    if not success:
        return jsonify({"error": "Video generation failed", "detail": final_video_result}), 500

    # 3. Upload audio and video to Cloudinary
    audio_url = upload_to_cloudinary(audio_result, folder="audio")
    video_url = upload_to_cloudinary(final_video_result, folder="video")

    # 4. Save the generated video metadata
    video_id = GeneratedVideo.save_video(audio_url, video_url, story_text)

    return jsonify({
        "success": True,
        "video_id": video_id,
        "audio_url": audio_url,
        "video_url": video_url
    })
