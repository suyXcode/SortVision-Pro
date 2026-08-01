"""
algorithms/insertion_sort.py

Insertion Sort implementation, instrumented for step-by-step visualization.

Insertion Sort builds a sorted prefix one element at a time, taking each
new element from the unsorted region and inserting it into its correct
position within the sorted prefix by shifting larger elements right.
"""

from __future__ import annotations

from algorithms.base import BaseSorter, StepRecorder


class InsertionSort(BaseSorter):
    name = "Insertion Sort"
    best_case = "O(n)"
    average_case = "O(n^2)"
    worst_case = "O(n^2)"
    space_complexity = "O(1)"
    is_stable = True
    is_in_place = True
    is_adaptive = True

    description = (
        "Insertion Sort builds the final sorted array one item at a time, "
        "similar to how a person sorts playing cards in their hands."
    )
    working_principle = (
        "Starting from the second element, each element is compared "
        "backward against the already-sorted prefix. Elements greater than "
        "the current 'key' are shifted one position to the right, opening a "
        "gap. Once an element smaller than (or equal to) the key is found, "
        "the key is dropped into that gap. Repeating this for every element "
        "produces a fully sorted array."
    )
    advantages = [
        "Very fast on small or nearly-sorted arrays (adaptive)",
        "Stable and in-place",
        "Simple, low-overhead implementation; good for online sorting (data arriving one at a time)",
    ]
    disadvantages = [
        "O(n^2) worst-case time on reverse-sorted input",
        "Requires shifting elements, which is costly for large arrays",
    ]
    applications = [
        "Small datasets, or as the base case in hybrid sorts like Timsort",
        "Nearly-sorted data streams",
        "Online algorithms where data arrives incrementally",
    ]
    pseudo_code = (
        "procedure insertionSort(A, n)\n"
        "  for i from 1 to n - 1\n"
        "    key = A[i]\n"
        "    j = i - 1\n"
        "    while j >= 0 and A[j] > key\n"
        "      A[j + 1] = A[j]\n"
        "      j = j - 1\n"
        "    A[j + 1] = key\n"
        "  return A"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        n = len(recorder.array)
        for i in range(1, n):
            j = i - 1
            # Shift elements greater than array[i] one position to the right.
            while j >= 0 and recorder.compare(j, j + 1):
                recorder.swap(j, j + 1)
                j -= 1
            recorder.mark_sorted(i)

        for idx in range(n):
            recorder.mark_sorted(idx)
