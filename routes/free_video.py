from flask import Blueprint, request, jsonify
from services.video_generator import generate_video_with_dynamic_text
from services.audio_generator import generate_audio_from_text
from services.upload import upload_to_cloudinary

free_video_bp = Blueprint('free_video_bp', __name__)

@free_video_bp.route('/free-video', methods=['POST'])
def free_video():
    data = request.get_json() or {}
    text = data.get('text', '').strip()

    # Default values in case they aren't provided in the request
    video_url = data.get('video_url', 'https://res.cloudinary.com/dqrj0lcm1/video/upload/v1743761390/uploads/alrlpe7skvwrglihb8ws.mp4')
    voice_id = data.get('voice_id', 'JBFqnCBsd6RMkjVDRZzb')

    if not text:
        return jsonify({"error": "Please provide 'text' in JSON."}), 400

    # Step 1: Generate audio using ElevenLabs
    success, audio_path_or_error = generate_audio_from_text(text, voice_id)
    if not success:
        return jsonify({"error": "Failed to generate audio", "detail": audio_path_or_error}), 500

    audio_path = audio_path_or_error

    # ✅ Read bytes from saved audio path
    try:
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
    except Exception as e:
        return jsonify({"error": "Failed to read audio file", "detail": str(e)}), 500

    # Step 2: Generate video using video_url and audio bytes
    success, local_video_path = generate_video_with_dynamic_text(text, video_url, audio_bytes)
    if not success:
        return jsonify({"error": "Video generation failed", "detail": local_video_path}), 500

    # Step 3: Upload the locally rendered file to Cloudinary and return its public URL
    public_url = upload_to_cloudinary(local_video_path, folder="free-videos")
    
    return jsonify({"success": True, "video_url": public_url}), 200
