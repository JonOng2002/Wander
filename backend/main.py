from flask import Flask
from flask_cors import CORS
from app.tiktok_routes import tiktok_blueprint
from app.itinerary_routes import itinerary_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    app.register_blueprint(tiktok_blueprint)
    app.register_blueprint(itinerary_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)