# routes/list_videos.py
from flask import Blueprint, jsonify
from models.background_video import BackgroundVideo  # ✅ Correct import

list_videos_bp = Blueprint("list_videos_bp", __name__)

@list_videos_bp.route("/all-generated-videos", methods=["GET"])
def get_all_videos():
    videos = list(BackgroundVideo.collection.find().sort("_id", -1))  # ✅ Latest first
    for video in videos:
        video["_id"] = str(video["_id"])  # Convert ObjectId to string
    return jsonify(videos)
