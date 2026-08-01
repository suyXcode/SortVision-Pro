"""
algorithms/selection_sort.py

Selection Sort implementation, instrumented for step-by-step visualization.

Selection Sort divides the array into a sorted prefix and an unsorted
suffix. On each pass it scans the unsorted suffix to find the minimum
element and swaps it into place at the front of the suffix.
"""

from __future__ import annotations

from algorithms.base import BaseSorter, StepRecorder


class SelectionSort(BaseSorter):
    name = "Selection Sort"
    best_case = "O(n^2)"
    average_case = "O(n^2)"
    worst_case = "O(n^2)"
    space_complexity = "O(1)"
    is_stable = False
    is_in_place = True
    is_adaptive = False

    description = (
        "Selection Sort grows a sorted region at the front of the array by "
        "repeatedly selecting the smallest remaining element and swapping it "
        "into place."
    )
    working_principle = (
        "For each position i from left to right, the algorithm scans the "
        "remaining unsorted portion of the array to find the index of the "
        "minimum value, tracking it as it goes. Once the scan completes, that "
        "minimum is swapped with the element currently at position i. This "
        "guarantees exactly one swap per pass, regardless of how unsorted the "
        "input is."
    )
    advantages = [
        "Simple to implement and reason about",
        "Performs at most n - 1 swaps, useful when writes are expensive",
        "In-place, requires no extra memory",
    ]
    disadvantages = [
        "O(n^2) comparisons even on already-sorted input (not adaptive)",
        "Not stable in its typical implementation",
        "Outperformed by Insertion Sort and O(n log n) algorithms in practice",
    ]
    applications = [
        "Situations where the cost of swapping/writing is much higher than comparing",
        "Small arrays or educational contexts",
        "Memory-constrained environments needing an in-place sort",
    ]
    pseudo_code = (
        "procedure selectionSort(A, n)\n"
        "  for i from 0 to n - 2\n"
        "    minIndex = i\n"
        "    for j from i + 1 to n - 1\n"
        "      if A[j] < A[minIndex]\n"
        "        minIndex = j\n"
        "    if minIndex != i\n"
        "      swap(A[i], A[minIndex])\n"
        "  return A"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        n = len(recorder.array)
        for i in range(n):
            min_index = i
            recorder.mark([min_index], "min")
            for j in range(i + 1, n):
                # compare(j, min_index) records array[j] > array[min_index];
                # we want the reverse relation (is array[j] smaller?).
                is_greater = recorder.compare(min_index, j)
                if is_greater:
                    min_index = j
                    recorder.mark([min_index], "min")
            if min_index != i:
                recorder.swap(i, min_index)
            recorder.mark_sorted(i)
