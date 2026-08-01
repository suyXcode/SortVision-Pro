"""
utils/helpers.py

Small, generic helper functions shared across route handlers: standardized
JSON API responses and plain-text report generation for the "download
results" feature.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from flask import jsonify


def success_response(data: Any, status_code: int = 200):
    """Wrap payload data in a consistent success envelope."""
    return jsonify({"success": True, "data": data}), status_code


def error_response(message: str, status_code: int = 400):
    """Wrap an error message in a consistent error envelope."""
    return jsonify({"success": False, "error": message}), status_code


def build_report_text(result: Dict[str, Any]) -> str:
    """Build a human-readable plain-text report from a single sort result dict."""
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append("SORTVISION PRO — SORT EXECUTION REPORT")
    lines.append("=" * 60)
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()} UTC")
    lines.append("")
    lines.append(f"Algorithm:            {result.get('algorithm')}")
    lines.append(f"Array Length:         {result.get('arrayLength')}")
    lines.append(f"Comparisons:          {result.get('comparisons')}")
    lines.append(f"Swaps:                {result.get('swaps')}")
    lines.append(f"Execution Time (ms):  {result.get('executionTimeMs')}")
    lines.append(f"Memory Usage (KB):    {result.get('memoryUsageKb')}")
    lines.append(f"Stable:               {result.get('isStable')}")
    lines.append(f"In-Place:             {result.get('isInPlace')}")
    lines.append(f"Adaptive:             {result.get('isAdaptive')}")
    lines.append(f"Sorted Successfully:  {result.get('sortedSuccessfully')}")
    lines.append("")
    lines.append(f"Original Array: {result.get('originalArray')}")
    lines.append(f"Sorted Array:   {result.get('sortedArray')}")
    lines.append("=" * 60)
    return "\n".join(lines)


def build_comparison_report_text(results: List[Dict[str, Any]]) -> str:
    """Build a plain-text report comparing multiple sort results side by side."""
    lines: List[str] = []
    lines.append("=" * 70)
    lines.append("SORTVISION PRO — ALGORITHM COMPARISON REPORT")
    lines.append("=" * 70)
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()} UTC")
    lines.append("")

    header = f"{'Algorithm':<18}{'Time(ms)':<12}{'Comparisons':<14}{'Swaps':<10}{'Memory(KB)':<12}"
    lines.append(header)
    lines.append("-" * len(header))
    for result in results:
        lines.append(
            f"{result.get('algorithm', ''):<18}"
            f"{result.get('executionTimeMs', 0):<12}"
            f"{result.get('comparisons', 0):<14}"
            f"{result.get('swaps', 0):<10}"
            f"{result.get('memoryUsageKb', 0):<12}"
        )
    lines.append("=" * 70)
    return "\n".join(lines)
