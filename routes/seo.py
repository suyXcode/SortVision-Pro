"""
routes/seo.py

Blueprint dedicated to crawler-facing endpoints: robots.txt and a
dynamically generated sitemap.xml. Both are served from the app's own
config (SITE_URL) rather than hardcoded, so they resolve correctly on
whichever host each deployment is running on (localhost, a Render preview
URL, or the production domain), without a template change per environment.
"""

from __future__ import annotations

from datetime import date

from flask import Blueprint, Response, current_app, url_for

from algorithms import ALGORITHM_REGISTRY

seo_bp = Blueprint("seo", __name__)


@seo_bp.route("/robots.txt")
def robots_txt():
    site_url = current_app.config["SITE_URL"]
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /api/",
        "",
        f"Sitemap: {site_url}/sitemap.xml",
    ]
    return Response("\n".join(lines), mimetype="text/plain")


@seo_bp.route("/sitemap.xml")
def sitemap_xml():
    site_url = current_app.config["SITE_URL"]
    today = date.today().isoformat()

    # Core pages, weighted by how often their content changes / how central
    # they are to the product.
    static_entries = [
        (url_for("views.home"), "1.0", "weekly"),
        (url_for("views.visualizer"), "0.9", "weekly"),
        (url_for("views.compare"), "0.8", "weekly"),
        (url_for("views.learn"), "0.9", "monthly"),
    ]

    # One deep link per algorithm (e.g. /visualizer?algo=quick) so searches
    # like "quick sort visualizer" or "heap sort animation" can land
    # directly on the right pre-selected algorithm.
    algo_entries = [
        (f"{url_for('views.visualizer')}?algo={key}", "0.6", "monthly")
        for key in ALGORITHM_REGISTRY
    ]

    urls_xml = []
    for path, priority, changefreq in static_entries + algo_entries:
        urls_xml.append(
            "  <url>\n"
            f"    <loc>{site_url}{path}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls_xml)
        + "\n</urlset>"
    )
    return Response(xml, mimetype="application/xml")
