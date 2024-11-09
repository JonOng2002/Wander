from flask import Flask
from flask_cors import CORS
from app.tiktok_routes import tiktok_blueprint
from app.itinerary_routes import itinerary_blueprint

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["https://wander-g8t9.vercel.app", "http://localhost:8080", "http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    app.register_blueprint(tiktok_blueprint)
    app.register_blueprint(itinerary_blueprint)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(port=5000, debug=True)