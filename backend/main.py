from app import create_app
import logging
import os
from flask_cors import CORS

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

if __name__ == "__main__":
    app = create_app()
    CORS(app)
    app.run(port=5000, debug=True)

