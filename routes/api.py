"""
routes/api.py

JSON API blueprint. Every endpoint here is consumed by the frontend
JavaScript (static/js/*.js) via fetch() calls — no server-rendered HTML
is produced by this blueprint. All responses use the success_response /
error_response envelope from utils.helpers for a consistent contract.

Endpoints:
    GET  /api/algorithms            -> list of supported algorithms + metadata
    GET  /api/algorithms/<key>      -> complexity + learning info for one algorithm
    POST /api/array/random          -> generate a random array
    POST /api/array/validate        -> validate/parse a manually entered array
    POST /api/sort/<key>             -> run one algorithm, return steps + stats
    POST /api/compare                -> run 2+ algorithms on the same array
    POST /api/export/report          -> download a single-run text report
    POST /api/export/compare-report  -> download a comparison text report
"""

from __future__ import annotations

from flask import Blueprint, Response, request

from algorithms import ALGORITHM_REGISTRY, get_sorter, list_algorithms
from utils.array_generator import (
    ArrayValidationError,
    generate_random_array,
    parse_manual_array,
    validate_array,
)
from utils.helpers import (
    build_comparison_report_text,
    build_report_text,
    error_response,
    success_response,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------------------------------------------------------
# Algorithm metadata
# ---------------------------------------------------------------------------

@api_bp.route("/algorithms", methods=["GET"])
def algorithms_list():
    return success_response(list_algorithms())


@api_bp.route("/algorithms/<string:key>", methods=["GET"])
def algorithm_info(key: str):
    try:
        sorter = get_sorter(key)
    except KeyError as exc:
        return error_response(str(exc), 404)
    return success_response(sorter.info())


# ---------------------------------------------------------------------------
# Array generation / validation
# ---------------------------------------------------------------------------

@api_bp.route("/array/random", methods=["POST"])
def array_random():
    payload = request.get_json(silent=True) or {}
    try:
        size = int(payload.get("size", 30))
        min_value = int(payload.get("minValue", 5))
        max_value = int(payload.get("maxValue", 500))
    except (TypeError, ValueError):
        return error_response("size, minValue, and maxValue must be integers.")

    try:
        array = generate_random_array(size, min_value, max_value)
    except ArrayValidationError as exc:
        return error_response(str(exc))

    return success_response({"array": array})


@api_bp.route("/array/validate", methods=["POST"])
def array_validate():
    payload = request.get_json(silent=True) or {}
    raw_input = payload.get("raw", "")
    try:
        array = parse_manual_array(raw_input)
    except ArrayValidationError as exc:
        return error_response(str(exc))
    return success_response({"array": array})


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

@api_bp.route("/sort/<string:key>", methods=["POST"])
def sort_array(key: str):
    payload = request.get_json(silent=True) or {}
    array = payload.get("array")

    if not isinstance(array, list) or not all(isinstance(x, int) for x in array):
        return error_response("Field 'array' must be a list of integers.")

    try:
        validate_array(array)
    except ArrayValidationError as exc:
        return error_response(str(exc))

    try:
        sorter = get_sorter(key)
    except KeyError as exc:
        return error_response(str(exc), 404)

    result = sorter.run(array)
    return success_response(result.to_dict())


@api_bp.route("/compare", methods=["POST"])
def compare_algorithms():
    payload = request.get_json(silent=True) or {}
    array = payload.get("array")
    keys = payload.get("algorithms")

    if not isinstance(array, list) or not all(isinstance(x, int) for x in array):
        return error_response("Field 'array' must be a list of integers.")
    if not isinstance(keys, list) or not (2 <= len(keys) <= len(ALGORITHM_REGISTRY)):
        return error_response(
            f"Field 'algorithms' must list between 2 and {len(ALGORITHM_REGISTRY)} algorithm keys."
        )

    try:
        validate_array(array)
    except ArrayValidationError as exc:
        return error_response(str(exc))

    results = []
    for key in keys:
        try:
            sorter = get_sorter(key)
        except KeyError as exc:
            return error_response(str(exc), 404)
        results.append(sorter.run(array).to_dict())

    return success_response({"results": results})


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

@api_bp.route("/export/report", methods=["POST"])
def export_report():
    payload = request.get_json(silent=True) or {}
    result = payload.get("result")
    if not isinstance(result, dict):
        return error_response("Field 'result' must be a sort result object.")

    text = build_report_text(result)
    algo_name = str(result.get("algorithm", "sort")).lower().replace(" ", "_")
    return Response(
        text,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment; filename={algo_name}_report.txt"},
    )


@api_bp.route("/export/compare-report", methods=["POST"])
def export_compare_report():
    payload = request.get_json(silent=True) or {}
    results = payload.get("results")
    if not isinstance(results, list) or not results:
        return error_response("Field 'results' must be a non-empty list of sort results.")

    text = build_comparison_report_text(results)
    return Response(
        text,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=comparison_report.txt"},
    )
