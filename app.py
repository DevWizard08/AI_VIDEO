from flask import Flask
from routes.generate_av import generate_av_bp

app = Flask(__name__)
app.register_blueprint(generate_av_bp)

if __name__ == '__main__':
    app.run(debug=True)
