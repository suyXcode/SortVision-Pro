"""
routes/views.py

Blueprint responsible for rendering the app's HTML pages (server-rendered
Jinja2 templates). Interactive behavior (running sorts, live re-rendering
on algorithm change) happens client-side via the JSON API in routes/api.py,
but algorithm metadata (descriptions, pseudocode, complexity) is rendered
server-side wherever it's the primary content of a page — this keeps that
content crawlable and visible without JavaScript, which matters both for
SEO and for fast first paint.
"""

from __future__ import annotations

from flask import Blueprint, render_template, request

from algorithms import ALGORITHM_REGISTRY, get_sorter, list_algorithms

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def home():
    """Landing page: hero section, feature overview, algorithm list."""
    return render_template("index.html", algorithms=list_algorithms())


@views_bp.route("/visualizer")
def visualizer():
    """Main sorting visualizer page."""
    requested = request.args.get("algo", "")
    default_key = requested if requested in ALGORITHM_REGISTRY else "bubble"
    default_info = get_sorter(default_key).info()
    return render_template(
        "visualizer.html",
        algorithms=list_algorithms(),
        default_key=default_key,
        default_info=default_info,
    )


@views_bp.route("/compare")
def compare():
    """Side-by-side algorithm comparison page."""
    return render_template("compare.html", algorithms=list_algorithms())


@views_bp.route("/learn")
def learn():
    """Learning hub: descriptions, pseudocode, complexity for every algorithm."""
    algo_details = []
    for key in ALGORITHM_REGISTRY:
        info = get_sorter(key).info()
        info["key"] = key
        algo_details.append(info)
    return render_template("learn.html", algorithms=list_algorithms(), algo_details=algo_details)
