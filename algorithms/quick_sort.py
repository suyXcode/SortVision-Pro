"""
algorithms/quick_sort.py

Quick Sort implementation, instrumented for step-by-step visualization.

Quick Sort is a divide-and-conquer algorithm that picks a "pivot" element,
partitions the array so smaller elements sit to its left and larger ones
to its right, then recursively sorts each partition (Lomuto scheme).
"""

from __future__ import annotations

from algorithms.base import BaseSorter, StepRecorder


class QuickSort(BaseSorter):
    name = "Quick Sort"
    best_case = "O(n log n)"
    average_case = "O(n log n)"
    worst_case = "O(n^2)"
    space_complexity = "O(log n)"
    is_stable = False
    is_in_place = True
    is_adaptive = False

    description = (
        "Quick Sort is a divide-and-conquer algorithm that partitions the "
        "array around a pivot element, then recursively sorts the "
        "partitions on either side of it."
    )
    working_principle = (
        "A pivot (here, the last element of the current range) is chosen. "
        "The array is partitioned in place so that elements smaller than "
        "the pivot end up to its left and elements greater end up to its "
        "right, using the Lomuto partition scheme with a moving boundary "
        "index. The pivot is then swapped into its final sorted position, "
        "and the same process recurses independently on the left and right "
        "sub-ranges."
    )
    advantages = [
        "Excellent average-case performance, O(n log n)",
        "In-place: only O(log n) extra memory for the recursion stack",
        "Cache-friendly due to in-place partitioning; fast in practice",
    ]
    disadvantages = [
        "Worst-case O(n^2) on already-sorted or adversarial input (with naive pivot choice)",
        "Not stable",
        "Recursive; deep recursion on unbalanced partitions can hit stack limits",
    ]
    applications = [
        "General-purpose in-memory sorting (used in many standard library implementations)",
        "Systems where average-case speed matters more than worst-case guarantees",
        "As a building block for selection algorithms (quickselect)",
    ]
    pseudo_code = (
        "procedure quickSort(A, low, high)\n"
        "  if low < high\n"
        "    p = partition(A, low, high)\n"
        "    quickSort(A, low, p - 1)\n"
        "    quickSort(A, p + 1, high)\n"
        "\n"
        "procedure partition(A, low, high)\n"
        "  pivot = A[high]\n"
        "  i = low - 1\n"
        "  for j from low to high - 1\n"
        "    if A[j] < pivot\n"
        "      i++\n"
        "      swap(A[i], A[j])\n"
        "  swap(A[i + 1], A[high])\n"
        "  return i + 1"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        n = len(recorder.array)
        if n <= 1:
            return
        self._quick_sort(recorder, 0, n - 1)

    def _quick_sort(self, recorder: StepRecorder, low: int, high: int) -> None:
        if low < high:
            pivot_index = self._partition(recorder, low, high)
            recorder.mark_sorted(pivot_index)
            self._quick_sort(recorder, low, pivot_index - 1)
            self._quick_sort(recorder, pivot_index + 1, high)
        elif low == high:
            recorder.mark_sorted(low)

    def _partition(self, recorder: StepRecorder, low: int, high: int) -> int:
        recorder.mark([high], "pivot")
        i = low - 1
        for j in range(low, high):
            recorder.mark([high], "pivot")
            # compare(high, j) -> pivot > array[j]; we want array[j] < pivot.
            if recorder.compare(high, j):
                i += 1
                recorder.swap(i, j)
        recorder.swap(i + 1, high)
        return i + 1
