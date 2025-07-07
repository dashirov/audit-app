from flask import Flask, jsonify
from config import Config
from models import db
from routes.audit_routes import audit_bp
from routes.core_routes import core_bp  # Your existing routes
import os


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Register blueprints
app.register_blueprint(audit_bp)
app.register_blueprint(core_bp)

if __name__ == "__main__":
    print("FLASK_ENV:", os.getenv("FLASK_ENV"))
    print("FLASK_DEBUG:", os.getenv("FLASK_DEBUG"))
    print("DATABASE URL:", os.getenv("SQLALCHEMY_DATABASE_URI"))
    app.run(host="0.0.0.0", port=5172, debug=True)