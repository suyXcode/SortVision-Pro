"""
algorithms/__init__.py

Central registry mapping URL/API-friendly algorithm keys to their concrete
BaseSorter subclasses. Any code that needs to look up an algorithm by name
(the Flask routes, the comparison endpoint, etc.) should import
``ALGORITHM_REGISTRY`` from here rather than importing individual algorithm
classes directly — this keeps the list of supported algorithms in exactly
one place.
"""

from __future__ import annotations

from typing import Dict, Type

from algorithms.base import BaseSorter
from algorithms.bubble_sort import BubbleSort
from algorithms.selection_sort import SelectionSort
from algorithms.insertion_sort import InsertionSort
from algorithms.merge_sort import MergeSort
from algorithms.quick_sort import QuickSort
from algorithms.heap_sort import HeapSort
from algorithms.shell_sort import ShellSort
from algorithms.counting_sort import CountingSort
from algorithms.radix_sort import RadixSort

ALGORITHM_REGISTRY: Dict[str, Type[BaseSorter]] = {
    "bubble": BubbleSort,
    "selection": SelectionSort,
    "insertion": InsertionSort,
    "merge": MergeSort,
    "quick": QuickSort,
    "heap": HeapSort,
    "shell": ShellSort,
    "counting": CountingSort,
    "radix": RadixSort,
}


def get_sorter(key: str) -> BaseSorter:
    """Instantiate and return the sorter for the given algorithm key.

    Raises:
        KeyError: if ``key`` is not a recognized algorithm.
    """
    if key not in ALGORITHM_REGISTRY:
        raise KeyError(f"Unknown algorithm '{key}'. Valid options: {list(ALGORITHM_REGISTRY)}")
    return ALGORITHM_REGISTRY[key]()


def list_algorithms() -> list:
    """Return metadata (key + display name) for every registered algorithm."""
    return [
        {"key": key, "name": cls().name}
        for key, cls in ALGORITHM_REGISTRY.items()
    ]
