from flask import Flask
from flask_cors import CORS
# Import blueprints or routes from your other files

def create_app():
    app = Flask(__name__)
    CORS(app)  # You can configure CORS here if needed

    # Register blueprints/routes
    # app.register_blueprint(main_blueprint)

    return app