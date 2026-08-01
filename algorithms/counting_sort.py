"""
algorithms/counting_sort.py

Counting Sort implementation, instrumented for step-by-step visualization.

Counting Sort is a non-comparison-based algorithm: it counts occurrences
of each value, derives cumulative positions, and places elements directly
into their sorted position. It only works efficiently for non-negative
integer keys within a bounded range.
"""

from __future__ import annotations

from algorithms.base import BaseSorter, StepRecorder


class CountingSort(BaseSorter):
    name = "Counting Sort"
    best_case = "O(n + k)"
    average_case = "O(n + k)"
    worst_case = "O(n + k)"
    space_complexity = "O(n + k)"
    is_stable = True
    is_in_place = False
    is_adaptive = False

    description = (
        "Counting Sort is a non-comparison integer sorting algorithm that "
        "counts the occurrences of each distinct value and uses those counts "
        "to place elements directly into sorted output positions."
    )
    working_principle = (
        "A count array of size (max - min + 1) is built, where each bucket "
        "tallies how many times that value appears in the input. Running "
        "(prefix) sums are then computed over the count array so each bucket "
        "holds the final index at which that value's run should end. "
        "Finally, the original array is scanned once more (from the end, to "
        "preserve stability) and each element is placed directly at its "
        "computed position in the output array."
    )
    advantages = [
        "Linear O(n + k) time, no comparisons needed",
        "Stable, preserving relative order of equal keys",
        "Extremely fast when the value range k is small relative to n",
    ]
    disadvantages = [
        "Requires O(n + k) extra memory, impractical for large value ranges",
        "Only works for discrete keys (typically non-negative integers)",
        "Not in-place and not comparison-based, so it cannot sort arbitrary comparable objects directly",
    ]
    applications = [
        "Sorting integers with a small, known range (e.g. exam scores, ages)",
        "As a subroutine within Radix Sort",
        "Bucketing/histogram-style data processing",
    ]
    pseudo_code = (
        "procedure countingSort(A, n)\n"
        "  min = min(A); max = max(A)\n"
        "  count = array of zeros, size (max - min + 1)\n"
        "  for x in A: count[x - min] += 1\n"
        "  for i from 1 to len(count) - 1: count[i] += count[i - 1]\n"
        "  output = array of size n\n"
        "  for i from n - 1 down to 0\n"
        "    output[count[A[i] - min] - 1] = A[i]\n"
        "    count[A[i] - min] -= 1\n"
        "  return output"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        arr = recorder.array
        n = len(arr)
        if n == 0:
            return

        lo, hi = min(arr), max(arr)
        range_size = hi - lo + 1
        count = [0] * range_size

        for value in arr:
            count[value - lo] += 1
            recorder.comparisons += 1  # counting each element as a pass-through op

        for i in range(1, range_size):
            count[i] += count[i - 1]

        output = [0] * n
        for i in range(n - 1, -1, -1):
            value = arr[i]
            position = count[value - lo] - 1
            output[position] = value
            count[value - lo] -= 1
            recorder.mark([i], "compare")

        for i in range(n):
            recorder.overwrite(i, output[i])
            recorder.mark_sorted(i)

    # Counting Sort performs no swaps by nature; swaps stays 0 which is
    # correctly reported since StepRecorder.swaps is never incremented here.
