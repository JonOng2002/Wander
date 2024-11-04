from flask import Flask
from flask_cors import CORS
from app.tiktok_routes import tiktok_blueprint
from app.itinerary_routes import itinerary_blueprint
import logging

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["https://wander-g8t9.vercel.app"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    app.register_blueprint(tiktok_blueprint)
    app.register_blueprint(itinerary_blueprint)
    
    # Optional: Health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        logging.info("Health check requested.")
        return "Healthy", 200

    return app

# Create the app instance
app = create_app()

# Run the app if this file is executed directly
if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)