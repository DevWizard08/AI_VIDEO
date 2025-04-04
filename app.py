from flask import Flask
from flask_pymongo import PyMongo

# Blueprints
from routes.generate_av import generate_av_bp
from routes.upload_background import upload_bg
from routes.get_background_url import get_background_url_bp
from routes.list_videos import list_videos_bp
from routes.get_voices import get_voices_bp


# Models
from models.generated_video import GeneratedVideo
from models.background_video import BackgroundVideo

import config

app = Flask(__name__)

# MongoDB config
app.config["MONGO_URI"] = "mongodb://localhost:27017/Video"
mongo = PyMongo(app)

# Set collection
GeneratedVideo.collection = mongo.db["Generated-Video"]
BackgroundVideo.collection = mongo.db["Background-Video"]

# Register routes
app.register_blueprint(generate_av_bp)
app.register_blueprint(upload_bg)
app.register_blueprint(get_background_url_bp)
app.register_blueprint(list_videos_bp)
app.register_blueprint(get_voices_bp)


if __name__ == '__main__':
    app.run(debug=True)
