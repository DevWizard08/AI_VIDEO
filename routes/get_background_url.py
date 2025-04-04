# routes/get_background_url.py

from flask import Blueprint, jsonify
from models.background_video import BackgroundVideo  # ✅ Correct import

get_background_url_bp = Blueprint("get_background_url", __name__)

@get_background_url_bp.route("/api/get-latest-background-url", methods=["GET"])
def get_latest_background_url():
    latest_video = BackgroundVideo.collection.find_one(
        sort=[("_id", -1)]  # Sort by insertion order (ObjectId)
    )
    if not latest_video:
        return jsonify({"error": "No background video found"}), 404

    return jsonify({
        "video_url": latest_video["video_url"]
    })
