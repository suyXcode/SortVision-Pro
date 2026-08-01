"""
algorithms/bubble_sort.py

Bubble Sort implementation, instrumented for step-by-step visualization.

Bubble Sort repeatedly steps through the array, compares adjacent elements,
and swaps them if they are in the wrong order. Larger elements "bubble up"
to the end of the array on each pass. An early-exit flag is used so already
sorted arrays finish in a single adaptive pass.
"""

from __future__ import annotations

from typing import List

from algorithms.base import BaseSorter, StepRecorder


class BubbleSort(BaseSorter):
    name = "Bubble Sort"
    best_case = "O(n)"
    average_case = "O(n^2)"
    worst_case = "O(n^2)"
    space_complexity = "O(1)"
    is_stable = True
    is_in_place = True
    is_adaptive = True

    description = (
        "Bubble Sort is one of the simplest sorting algorithms. It repeatedly "
        "compares adjacent elements and swaps them if they are out of order, "
        "causing larger values to 'bubble' toward the end of the array."
    )
    working_principle = (
        "On each pass through the array, adjacent pairs are compared left to "
        "right. If a pair is out of order, the two elements are swapped. "
        "After each full pass, the largest unsorted element is guaranteed to "
        "be in its final position, so the range considered shrinks by one "
        "each time. A flag tracks whether any swap occurred during a pass; "
        "if not, the array is already sorted and the algorithm exits early."
    )
    advantages = [
        "Extremely simple to understand and implement",
        "Stable sort (equal elements keep their relative order)",
        "Adaptive: runs in O(n) time on nearly-sorted input",
        "No extra memory required (in-place)",
    ]
    disadvantages = [
        "O(n^2) time complexity makes it impractical for large datasets",
        "Far slower in practice than Insertion Sort despite similar complexity",
        "Many redundant comparisons on random data",
    ]
    applications = [
        "Teaching sorting fundamentals and algorithmic thinking",
        "Sorting tiny datasets where simplicity outweighs performance",
        "Detecting whether a list is already sorted (single pass, no swaps)",
    ]
    pseudo_code = (
        "procedure bubbleSort(A, n)\n"
        "  for i from 0 to n - 1\n"
        "    swapped = false\n"
        "    for j from 0 to n - i - 2\n"
        "      if A[j] > A[j + 1]\n"
        "        swap(A[j], A[j + 1])\n"
        "        swapped = true\n"
        "    if not swapped\n"
        "      break\n"
        "  return A"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        n = len(recorder.array)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if recorder.compare(j, j + 1):
                    recorder.swap(j, j + 1)
                    swapped = True
            recorder.mark_sorted(n - i - 1)
            if not swapped:
                break

        # Mark any remaining untouched indices as sorted (e.g. early exit).
        for idx in range(n):
            recorder.mark_sorted(idx)
