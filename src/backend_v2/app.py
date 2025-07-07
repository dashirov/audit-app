from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from models import db
from routes.core_routes import core_bp
from config import Config  # Make sure you have this defined
import os

# Logging configuration
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    load_dotenv()
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )
    logger.debug(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    db.init_app(app)
    # app.config.from_object(config_class)
    # db.init_app(app)
    CORS(app)
    app.register_blueprint(core_bp)

    return app


if __name__ == "__main__":

    app = create_app()
    logger.debug(f"Using DB: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    app.run(host="0.0.0.0", port=5172)