"""
utils/array_generator.py

Helpers for generating random arrays and validating user-supplied arrays
before they're handed off to a sorting algorithm.
"""

from __future__ import annotations

import random
from typing import List, Tuple

MAX_ARRAY_SIZE = 200
MIN_ARRAY_SIZE = 2
MIN_VALUE_BOUND = -10_000
MAX_VALUE_BOUND = 10_000


class ArrayValidationError(ValueError):
    """Raised when a user-supplied array or generation request is invalid."""


def generate_random_array(size: int, min_value: int, max_value: int) -> List[int]:
    """Generate a random array of integers within the given bounds.

    Raises:
        ArrayValidationError: if the parameters are out of acceptable range.
    """
    if not (MIN_ARRAY_SIZE <= size <= MAX_ARRAY_SIZE):
        raise ArrayValidationError(
            f"Array size must be between {MIN_ARRAY_SIZE} and {MAX_ARRAY_SIZE}."
        )
    if min_value > max_value:
        raise ArrayValidationError("Minimum value cannot exceed maximum value.")
    if min_value < MIN_VALUE_BOUND or max_value > MAX_VALUE_BOUND:
        raise ArrayValidationError(
            f"Values must fall between {MIN_VALUE_BOUND} and {MAX_VALUE_BOUND}."
        )
    return [random.randint(min_value, max_value) for _ in range(size)]


def parse_manual_array(raw_input: str) -> List[int]:
    """Parse a comma/whitespace separated string of integers into a list.

    Accepts formats like "5, 3, 8, 1" or "5 3 8 1".

    Raises:
        ArrayValidationError: if parsing fails or constraints are violated.
    """
    if not raw_input or not raw_input.strip():
        raise ArrayValidationError("Array input cannot be empty.")

    tokens = [t for t in raw_input.replace(",", " ").split() if t]
    if not tokens:
        raise ArrayValidationError("No numeric values found in input.")

    parsed: List[int] = []
    for token in tokens:
        try:
            parsed.append(int(float(token)))
        except ValueError as exc:
            raise ArrayValidationError(f"'{token}' is not a valid integer.") from exc

    validate_array(parsed)
    return parsed


def validate_array(array: List[int]) -> None:
    """Validate size/value bounds on an already-parsed array."""
    if not (MIN_ARRAY_SIZE <= len(array) <= MAX_ARRAY_SIZE):
        raise ArrayValidationError(
            f"Array length must be between {MIN_ARRAY_SIZE} and {MAX_ARRAY_SIZE} "
            f"(got {len(array)})."
        )
    for value in array:
        if value < MIN_VALUE_BOUND or value > MAX_VALUE_BOUND:
            raise ArrayValidationError(
                f"Value {value} is outside the allowed range "
                f"[{MIN_VALUE_BOUND}, {MAX_VALUE_BOUND}]."
            )


def bounds() -> Tuple[int, int, int, int]:
    """Expose the configured size/value bounds (useful for frontend hints)."""
    return MIN_ARRAY_SIZE, MAX_ARRAY_SIZE, MIN_VALUE_BOUND, MAX_VALUE_BOUND
