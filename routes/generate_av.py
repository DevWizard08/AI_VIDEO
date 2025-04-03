from flask import Blueprint, request, jsonify
from services.audio_generator import generate_audio_from_text
from services.video_generator import generate_video_with_dynamic_text

generate_av_bp = Blueprint('generate_av', __name__)

@generate_av_bp.route('/generate-av', methods=['POST'])
def generate_av():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Please provide text in the JSON payload"}), 400

    story_text = data["text"]

    success, audio_result = generate_audio_from_text(story_text)
    if not success:
        return jsonify({"error": "Audio generation failed", "detail": audio_result}), 500

    success, video_result = generate_video_with_dynamic_text(story_text)
    if not success:
        return jsonify({"error": "Video generation failed", "detail": video_result}), 500

    return jsonify({"video_url": video_result})
