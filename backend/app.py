import os
import sys
from flask import Flask
from flask_cors import CORS
from backend.books_routes import books_bp




# -------------------------------------------------
# Add project root to sys.path
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from config.config import SECRET_KEY
from backend.auth_routes import auth_bp
from backend.upload_routes import upload_bp

def create_app():
    app = Flask(__name__)

    # 🔐 Secret key (required for sessions)
    app.secret_key = SECRET_KEY or "dev-secret-key"

    # 🔑 SESSION CONFIG (CRITICAL)
    app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)


    # 🌐 CORS CONFIG (CRITICAL)
    CORS(app, supports_credentials=True)


    # -------------------------------------------------
    # Register blueprints
    # -------------------------------------------------
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(upload_bp)
    app.register_blueprint(books_bp)
    @app.route("/")
    def health():
        return {"status": "Backend running"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
