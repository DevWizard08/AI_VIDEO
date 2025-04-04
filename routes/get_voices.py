# routes/get_voices.py
from flask import Blueprint, jsonify
from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()

get_voices_bp = Blueprint("get_voices_bp", __name__)
client = ElevenLabs(api_key=os.getenv("API_SECRET_KEY"))

@get_voices_bp.route("/api/get-voices", methods=["GET"])
def get_voices():
    try:
        voices_response = client.voices.get_all()
        voices = voices_response.voices

        voice_list = [{
            "name": voice.name,
            "voice_id": voice.voice_id,
            "labels": voice.labels
        } for voice in voices]

        return jsonify({"voices": voice_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
