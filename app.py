from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import timedelta


load_dotenv()


# Blueprints
from routes.generate_av import generate_av_bp
from routes.upload_background import upload_bg
from routes.get_background_url import get_background_url_bp
from routes.list_videos import list_videos_bp
from routes.get_voices import get_voices_bp
from routes.free_video import free_video_bp
from routes.auth import auth_bp



# Models
from models.generated_video import GeneratedVideo
from models.background_video import BackgroundVideo
from models.user import User


import config

app = Flask(__name__)
@app.route("/", methods=["GET"])
def index():
    return "Welcome to the Video API!"

app.config["JWT_SECRET_KEY"] =  os.getenv("JWT_SECRET_KEY")
raw_access_expires = os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "0")
if raw_access_expires.endswith("d"):
    days = int(raw_access_expires[:-1])
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=days)
else:
    try:
        seconds = int(raw_access_expires)
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=seconds)
    except ValueError:
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
jwt = JWTManager(app)

# MongoDB config
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

# Set collection
GeneratedVideo.collection = mongo.db["Generated-Video"]
BackgroundVideo.collection = mongo.db["Background-Video"]
User.collection             = mongo.db["users"]


# Register routes
app.register_blueprint(free_video_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(list_videos_bp)
app.register_blueprint(get_voices_bp)
app.register_blueprint(generate_av_bp)



if __name__ == '__main__':
    app.run(host="0.0.0.0",port =5000)