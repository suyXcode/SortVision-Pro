"""
config.py

Environment-driven configuration classes for the Flask app. Selecting the
active config is done via the FLASK_ENV / APP_CONFIG environment variable
in app.py's create_app() factory, so the same codebase runs identically
in development, testing, and production (Render/Railway/Docker).
"""

from __future__ import annotations

import os


class BaseConfig:
    """Settings shared by every environment."""

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    JSON_SORT_KEYS: bool = False
    MAX_CONTENT_LENGTH: int = 1 * 1024 * 1024  # 1 MB request body cap
    CORS_ORIGINS: str = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    ENV: str = "development"


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    ENV: str = "production"


class TestingConfig(BaseConfig):
    DEBUG: bool = True
    TESTING: bool = True
    ENV: str = "testing"


CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(name: str | None = None):
    """Resolve a config class from an environment name (defaults to production)."""
    name = (name or os.environ.get("APP_CONFIG") or os.environ.get("FLASK_ENV") or "production").lower()
    return CONFIG_MAP.get(name, ProductionConfig)
