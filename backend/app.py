import os
import sys
from flask import Flask
from flask_cors import CORS



# -------------------------------------------------
# FIX PATH FIRST (CRITICAL)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# -------------------------------------------------
# NOW import blueprints
# -------------------------------------------------
from config.config import SECRET_KEY
from backend.auth_routes import auth_bp
from backend.upload_routes import upload_bp
from backend.books_routes import books_bp   
from backend.admin_routes import admin_bp
from backend.summary_management_routes import summary_mgmt_bp
# from models.summarization_model import summarize_text


from backend.summarization_routes import summary_bp


def create_app():
    app = Flask(__name__)

    app.secret_key = SECRET_KEY or "dev-secret-key"

    app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)


    CORS(app, supports_credentials=True)

    # -------------------------------------------------
    # REGISTER BLUEPRINTS
    # -------------------------------------------------
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(upload_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(summary_bp)  # later
    app.register_blueprint(admin_bp)
    app.register_blueprint(summary_mgmt_bp)
    @app.route("/")
    def health():
        return {"status": "Backend running"}, 200

    

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)

