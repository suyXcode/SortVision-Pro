"""
routes/views.py

Blueprint responsible for rendering the app's HTML pages (server-rendered
Jinja2 templates). All interactive behavior happens client-side via the
JSON API defined in routes/api.py; this blueprint just serves the shell
pages those scripts run inside.
"""

from __future__ import annotations

from flask import Blueprint, render_template

from algorithms import list_algorithms

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def home():
    """Landing page: hero section, feature overview, algorithm list."""
    return render_template("index.html", algorithms=list_algorithms())


@views_bp.route("/visualizer")
def visualizer():
    """Main sorting visualizer page."""
    return render_template("visualizer.html", algorithms=list_algorithms())


@views_bp.route("/compare")
def compare():
    """Side-by-side algorithm comparison page."""
    return render_template("compare.html", algorithms=list_algorithms())


@views_bp.route("/learn")
def learn():
    """Learning hub: descriptions, pseudocode, complexity for every algorithm."""
    return render_template("learn.html", algorithms=list_algorithms())
