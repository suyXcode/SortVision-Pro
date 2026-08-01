"""
algorithms/base.py

Shared building blocks used by every sorting algorithm implementation:

- ``Step``: a single frame of the visualization (array snapshot + metadata
  about which indices are being compared / swapped / marked).
- ``StepRecorder``: an instrumented recorder that algorithms call into while
  they run. It tracks comparisons, swaps, and the full step-by-step history
  needed to animate the sort on the frontend.
- ``SortResult``: the final payload returned to the API layer, containing
  everything the UI needs (steps, stats, timing, memory usage).
- ``BaseSorter``: an abstract base class that every concrete algorithm
  (BubbleSort, QuickSort, ...) subclasses. It wires timing + memory profiling
  around the algorithm's ``_sort`` implementation so individual algorithm
  files only need to focus on the sorting logic itself.

Keeping this logic centralized avoids duplicating instrumentation code
across nine algorithm files and guarantees every algorithm reports stats in
an identical shape.
"""

from __future__ import annotations

import time
import tracemalloc
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Step / action types
# ---------------------------------------------------------------------------

# Action tags understood by the frontend visualizer. Each maps to a color:
#   compare -> red, swap -> green, min -> yellow,
#   pivot -> purple, sorted -> orange, default -> blue
VALID_ACTIONS = {"compare", "swap", "overwrite", "min", "pivot", "sorted", "default"}


@dataclass
class Step:
    """A single animation frame.

    Attributes:
        array: Full snapshot of the array at this point in time.
        indices: Indices involved in this step (e.g. the two being compared).
        action: One of VALID_ACTIONS, tells the frontend how to color bars.
        sorted_indices: Indices that are confirmed to be in final sorted
            position as of this step (rendered orange, accumulates over time).
    """

    array: List[int]
    indices: List[int]
    action: str
    sorted_indices: List[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "array": list(self.array),
            "indices": list(self.indices),
            "action": self.action,
            "sortedIndices": list(self.sorted_indices),
        }


@dataclass
class SortResult:
    """Final result returned to the caller after a sort completes."""

    algorithm: str
    original_array: List[int]
    sorted_array: List[int]
    steps: List[Step]
    comparisons: int
    swaps: int
    execution_time_ms: float
    memory_usage_kb: float
    array_length: int
    is_stable: bool
    is_in_place: bool
    is_adaptive: bool

    def to_dict(self) -> dict:
        return {
            "algorithm": self.algorithm,
            "originalArray": self.original_array,
            "sortedArray": self.sorted_array,
            "steps": [s.to_dict() for s in self.steps],
            "stepCount": len(self.steps),
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "executionTimeMs": round(self.execution_time_ms, 4),
            "memoryUsageKb": round(self.memory_usage_kb, 4),
            "arrayLength": self.array_length,
            "isStable": self.is_stable,
            "isInPlace": self.is_in_place,
            "isAdaptive": self.is_adaptive,
            "sortedSuccessfully": self.sorted_array == sorted(self.original_array),
        }


# ---------------------------------------------------------------------------
# Step recorder
# ---------------------------------------------------------------------------

class StepRecorder:
    """Instrumentation helper passed into every algorithm implementation.

    Algorithms call ``compare``/``swap``/``mark``/``overwrite`` as they run;
    the recorder both counts operations and stores a Step snapshot for
    frontend animation. Keeping this separate from the algorithm logic means
    each algorithm file reads almost identically to its textbook pseudocode.
    """

    def __init__(self, array: List[int], max_steps: int = 20000) -> None:
        self.array: List[int] = list(array)
        self.steps: List[Step] = []
        self.comparisons: int = 0
        self.swaps: int = 0
        self._max_steps = max_steps
        self._sorted_marked: List[int] = []

    def _snapshot(self, indices: List[int], action: str) -> None:
        if len(self.steps) >= self._max_steps:
            return
        self.steps.append(
            Step(
                array=list(self.array),
                indices=list(indices),
                action=action,
                sorted_indices=list(self._sorted_marked),
            )
        )

    def compare(self, i: int, j: int) -> bool:
        """Record a comparison between indices i and j; returns array[i] > array[j]."""
        self.comparisons += 1
        self._snapshot([i, j], "compare")
        return self.array[i] > self.array[j]

    def swap(self, i: int, j: int) -> None:
        """Swap indices i and j in place and record the operation."""
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self.swaps += 1
        self._snapshot([i, j], "swap")

    def overwrite(self, i: int, value: int) -> None:
        """Overwrite array[i] with value (used by merge/counting/radix sort)."""
        self.array[i] = value
        self._snapshot([i], "overwrite")

    def mark(self, indices: List[int], action: str) -> None:
        """Record a purely visual marker (e.g. current pivot or minimum)."""
        if action not in VALID_ACTIONS:
            action = "default"
        self._snapshot(indices, action)

    def mark_sorted(self, index: int) -> None:
        """Flag an index as permanently sorted (rendered orange going forward)."""
        if index not in self._sorted_marked:
            self._sorted_marked.append(index)
        self._snapshot([index], "sorted")

    def finalize_all_sorted(self) -> None:
        """Mark every index as sorted for the final animation frame."""
        self._sorted_marked = list(range(len(self.array)))
        self._snapshot(list(range(len(self.array))), "sorted")


# ---------------------------------------------------------------------------
# Base algorithm class
# ---------------------------------------------------------------------------

class BaseSorter(ABC):
    """Abstract base class every sorting algorithm implementation extends.

    Subclasses implement ``_sort(recorder)`` using the recorder's
    compare/swap/mark helpers to mutate ``recorder.array`` in place (or to
    build up a new array via ``overwrite``, for non-in-place algorithms).
    This base class handles timing, memory profiling, and packaging the
    final ``SortResult``.
    """

    name: str = "Base"
    best_case: str = "-"
    average_case: str = "-"
    worst_case: str = "-"
    space_complexity: str = "-"
    is_stable: bool = False
    is_in_place: bool = True
    is_adaptive: bool = False
    description: str = ""
    working_principle: str = ""
    advantages: List[str] = []
    disadvantages: List[str] = []
    applications: List[str] = []
    pseudo_code: str = ""

    @abstractmethod
    def _sort(self, recorder: StepRecorder) -> None:
        """Run the sorting algorithm, mutating recorder.array via its helpers."""
        raise NotImplementedError

    def run(self, array: List[int]) -> SortResult:
        """Execute the algorithm with full instrumentation and return a SortResult."""
        recorder = StepRecorder(array)

        tracemalloc.start()
        start_time = time.perf_counter()

        self._sort(recorder)

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        _current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        recorder.finalize_all_sorted()

        return SortResult(
            algorithm=self.name,
            original_array=array,
            sorted_array=recorder.array,
            steps=recorder.steps,
            comparisons=recorder.comparisons,
            swaps=recorder.swaps,
            execution_time_ms=elapsed_ms,
            memory_usage_kb=peak / 1024,
            array_length=len(array),
            is_stable=self.is_stable,
            is_in_place=self.is_in_place,
            is_adaptive=self.is_adaptive,
        )

    def info(self) -> dict:
        """Static metadata about this algorithm (complexity + learning content)."""
        return {
            "name": self.name,
            "bestCase": self.best_case,
            "averageCase": self.average_case,
            "worstCase": self.worst_case,
            "spaceComplexity": self.space_complexity,
            "isStable": self.is_stable,
            "isInPlace": self.is_in_place,
            "isAdaptive": self.is_adaptive,
            "description": self.description,
            "workingPrinciple": self.working_principle,
            "advantages": self.advantages,
            "disadvantages": self.disadvantages,
            "applications": self.applications,
            "pseudoCode": self.pseudo_code,
        }
