from flask import Blueprint, request, jsonify
from services.audio_generator import generate_audio_from_text
from services.video_generator import generate_video_with_dynamic_text
from services.upload import upload_to_cloudinary  # ✅ Cloudinary uploader import
from models.video import Video  

generate_av_bp = Blueprint('generate_av', __name__)

@generate_av_bp.route('/generate-av', methods=['POST'])
def generate_av():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Please provide text in the JSON payload"}), 400

    story_text = data["text"]

    # 🔹 **Step 1: Audio Generate karo**
    success, audio_result = generate_audio_from_text(story_text)
    if not success:
        return jsonify({"error": "Audio generation failed", "detail": audio_result}), 500

    # 🔹 **Step 2: Video Generate karo**
    success, final_video_result = generate_video_with_dynamic_text(story_text)
    if not success:
        return jsonify({"error": "Video generation failed", "detail": final_video_result}), 500

    # 🔹 **Step 3: Audio ko Cloudinary pe Upload karo**
    audio_url = upload_to_cloudinary(audio_result, folder="audio")

    # 🔹 **Step 4: Video ko Cloudinary pe Upload karo**
    video_url = upload_to_cloudinary(final_video_result, folder="video")

    # 🔹 **Step 5: MongoDB me Save karo**
    video_id = Video.save_video(audio_url, video_url, story_text)

    return jsonify({
        "success": True,
        "video_id": video_id,
        "audio_url": audio_url,
        "video_url": video_url
    })
