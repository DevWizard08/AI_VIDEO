from flask import Flask
from flask_pymongo import PyMongo
from routes.generate_av import generate_av_bp

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Video"
mongo = PyMongo(app)

from models.video import Video  
Video.collection = mongo.db["Generated-Video"]

app.register_blueprint(generate_av_bp)

if __name__ == '__main__':
    app.run(debug=True)
