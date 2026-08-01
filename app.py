"""
app.py

Flask application factory for SortVision Pro. Wires together config,
CORS, blueprints, and error handlers. Keeping app creation in a factory
function (rather than a bare module-level `app = Flask(__name__)`) makes
the app testable and lets deployment platforms (Render/Railway/Docker)
and `run.py` all share a single, consistent entry point.
"""

from __future__ import annotations

from flask import Flask, jsonify
from flask_cors import CORS

from config import get_config
from routes.api import api_bp
from routes.views import views_bp


def create_app(config_name: str | None = None) -> Flask:
    """Application factory: builds and returns a configured Flask app."""
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp)

    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask) -> None:
    """Attach JSON error handlers so the API never leaks HTML error pages."""

    @app.errorhandler(404)
    def not_found(_error):
        if _wants_json():
            return jsonify({"success": False, "error": "Resource not found."}), 404
        from flask import render_template
        return render_template("404.html"), 404

    @app.errorhandler(400)
    def bad_request(_error):
        return jsonify({"success": False, "error": "Bad request."}), 400

    @app.errorhandler(413)
    def payload_too_large(_error):
        return jsonify({"success": False, "error": "Request payload too large."}), 413

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({"success": False, "error": "Internal server error."}), 500

    def _wants_json() -> bool:
        from flask import request
        return request.path.startswith("/api/")


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))
