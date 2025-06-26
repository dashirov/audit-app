from flask import Flask, jsonify
from config import Config
from models import db
from models.core import Subject, MaturityRubric, Area
from routes.audit_routes import audit_bp
from routes.core_routes import core_bp  # Your existing routes
import pandas as pd


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Register blueprints
app.register_blueprint(audit_bp)
app.register_blueprint(core_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)