from flask import Flask
from flask_cors import CORS
from .endpoint import main as main

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main)

    CORS(app, resources={r"/video-info-comments/*": {"origins": "http://localhost:8080"}})

    return app
