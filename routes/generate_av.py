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
    background_video_url = data.get("video_url")
    voice_id = data.get("voice_id")

    if not story_text or not voice_id:
        return jsonify({"error": "Please provide both 'text' and 'voice_id' in the JSON payload"}), 400

    # 1. Generate Audio from ElevenLabs
    success, audio_result = generate_audio_from_text(story_text, voice_id)
    if not success:
        return jsonify({"error": "Audio generation failed", "detail": audio_result}), 500

    # 2. Read audio bytes
    with open(audio_result, "rb") as f:
        audio_bytes = f.read()

    # 3. Generate video
    success, final_video_result = generate_video_with_dynamic_text(story_text, background_video_url, audio_bytes)
    if not success:
        return jsonify({"error": "Video generation failed", "detail": final_video_result}), 500

    # 4. Upload to Cloudinary
    audio_url = upload_to_cloudinary(audio_result, folder="audio")
    video_url = upload_to_cloudinary(final_video_result, folder="video")

    # 5. Save metadata
    video_id = GeneratedVideo.save_video(audio_url, video_url, story_text)

    return jsonify({
        "success": True,
        "video_id": video_id,
        "audio_url": audio_url,
        "video_url": video_url
    })
