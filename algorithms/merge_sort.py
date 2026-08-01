"""
algorithms/merge_sort.py

Merge Sort implementation, instrumented for step-by-step visualization.

Merge Sort is a divide-and-conquer algorithm: it recursively splits the
array into halves until each sub-array has a single element, then merges
adjacent sub-arrays back together in sorted order.
"""

from __future__ import annotations

from typing import List

from algorithms.base import BaseSorter, StepRecorder


class MergeSort(BaseSorter):
    name = "Merge Sort"
    best_case = "O(n log n)"
    average_case = "O(n log n)"
    worst_case = "O(n log n)"
    space_complexity = "O(n)"
    is_stable = True
    is_in_place = False
    is_adaptive = False

    description = (
        "Merge Sort is a divide-and-conquer algorithm that recursively splits "
        "the array in half, sorts each half, and merges the sorted halves "
        "back together."
    )
    working_principle = (
        "The array is recursively divided into two halves until each "
        "sub-array contains a single element (trivially sorted). Pairs of "
        "sorted sub-arrays are then merged: elements from the front of each "
        "sub-array are compared and the smaller one is written into the "
        "output, repeating until both sub-arrays are exhausted. This merge "
        "step happens bottom-up as recursion unwinds, producing a single "
        "sorted array at the top."
    )
    advantages = [
        "Guaranteed O(n log n) performance regardless of input order",
        "Stable sort, preserving relative order of equal elements",
        "Well suited to sorting linked lists and external (disk-based) sorting",
        "Parallelizes naturally since sub-arrays are independent",
    ]
    disadvantages = [
        "Requires O(n) additional memory, not in-place",
        "Slower than in-place O(n log n) sorts like Quick Sort in practice due to copying overhead",
        "Not adaptive: does not speed up on nearly-sorted input",
    ]
    applications = [
        "Sorting linked lists (no random access needed)",
        "External sorting of datasets too large to fit in memory",
        "As the backbone of Python's and Java's stable hybrid sorts (Timsort)",
    ]
    pseudo_code = (
        "procedure mergeSort(A, l, r)\n"
        "  if l >= r: return\n"
        "  m = (l + r) / 2\n"
        "  mergeSort(A, l, m)\n"
        "  mergeSort(A, m + 1, r)\n"
        "  merge(A, l, m, r)\n"
        "\n"
        "procedure merge(A, l, m, r)\n"
        "  left = A[l..m], right = A[m+1..r]\n"
        "  i = j = 0, k = l\n"
        "  while i < len(left) and j < len(right)\n"
        "    if left[i] <= right[j]: A[k] = left[i]; i++\n"
        "    else: A[k] = right[j]; j++\n"
        "    k++\n"
        "  copy any remaining elements of left/right into A"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        n = len(recorder.array)
        if n <= 1:
            return
        self._merge_sort(recorder, 0, n - 1)

    def _merge_sort(self, recorder: StepRecorder, left: int, right: int) -> None:
        if left >= right:
            return
        mid = (left + right) // 2
        self._merge_sort(recorder, left, mid)
        self._merge_sort(recorder, mid + 1, right)
        self._merge(recorder, left, mid, right)

    def _merge(self, recorder: StepRecorder, left: int, mid: int, right: int) -> None:
        left_part: List[int] = recorder.array[left:mid + 1]
        right_part: List[int] = recorder.array[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_part) and j < len(right_part):
            recorder.comparisons += 1
            recorder.mark([left + i, mid + 1 + j], "compare")
            if left_part[i] <= right_part[j]:
                recorder.overwrite(k, left_part[i])
                i += 1
            else:
                recorder.overwrite(k, right_part[j])
                j += 1
            k += 1

        while i < len(left_part):
            recorder.overwrite(k, left_part[i])
            i += 1
            k += 1

        while j < len(right_part):
            recorder.overwrite(k, right_part[j])
            j += 1
            k += 1

        for idx in range(left, right + 1):
            recorder.mark_sorted(idx)
