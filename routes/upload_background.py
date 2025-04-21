from flask import Blueprint, request, jsonify
from services.upload import upload_to_cloudinary
from models.background_video import BackgroundVideo  # 🔁 yahan se import karo
from flask_jwt_extended import jwt_required


upload_bg = Blueprint('upload_bg', __name__)

@upload_bg.route('/upload-background', methods=['POST'])
@jwt_required()
def upload_background():
    if not request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files.get('video')  # 👈 safer way to get 'video'

    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        public_url = upload_to_cloudinary(file, folder="uploads")

        # 🔁 Directly use your BackgroundVideo model to save
        BackgroundVideo.save_video(public_url)

        return jsonify({"message": "✅ Uploaded & Saved", "video_url": public_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
