# routes/get_voices.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import os
import requests
from dotenv import load_dotenv

load_dotenv()

get_voices_bp = Blueprint("get_voices_bp", __name__)
OPEN_TTS_VOICES_URL = os.getenv("OPEN_TTS_VOICES_URL", "http://localhost:5004/api/voices")

@get_voices_bp.route("/api/get-voices", methods=["GET"])
@jwt_required()
def get_voices():
    """
    Fetches the list of available voices from the self-hosted OpenTTS server
    and returns them in the ElevenLabs-like format.
    """
    try:
        resp = requests.get(OPEN_TTS_VOICES_URL, timeout=10)
        resp.raise_for_status()
        voices = resp.json()  # dict mapping voice_id -> metadata

        voice_list = []
        for vid, meta in voices.items():
            entry = {
                "name": meta.get("name", vid),
                "voice_id": vid,
                "labels": []  # no labels in OpenTTS
            }
            voice_list.append(entry)

        return jsonify({"voices": voice_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
