"""
run.py

Convenience entry point for local development.

Usage:
    python run.py

For production, use a WSGI server pointed at `app:app`, e.g.:
    gunicorn --bind 0.0.0.0:$PORT app:app
"""

from __future__ import annotations

import os

from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
