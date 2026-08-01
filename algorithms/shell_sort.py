"""
algorithms/shell_sort.py

Shell Sort implementation, instrumented for step-by-step visualization.

Shell Sort generalizes Insertion Sort by comparing and moving elements
that are a certain "gap" apart, progressively shrinking the gap down to 1.
This moves out-of-place elements long distances early on, making the
final insertion-sort pass (gap = 1) much cheaper.
"""

from __future__ import annotations

from algorithms.base import BaseSorter, StepRecorder


class ShellSort(BaseSorter):
    name = "Shell Sort"
    best_case = "O(n log n)"
    average_case = "O(n^1.3) (gap-sequence dependent)"
    worst_case = "O(n^2)"
    space_complexity = "O(1)"
    is_stable = False
    is_in_place = True
    is_adaptive = True

    description = (
        "Shell Sort is an optimization of Insertion Sort that allows the "
        "exchange of elements that are far apart, using a shrinking gap "
        "sequence to reduce the total amount of shifting needed."
    )
    working_principle = (
        "Starting with a large gap (here, n/2, halved each round), the "
        "array is conceptually split into gap-many interleaved sub-lists, "
        "each of which is sorted using insertion sort. As the gap shrinks "
        "toward 1, the array becomes progressively more sorted, so the "
        "final gap = 1 pass (plain insertion sort) has very little work "
        "left to do."
    )
    advantages = [
        "Significantly faster than plain Insertion Sort on larger arrays",
        "In-place, O(1) extra memory",
        "Adaptive: performs well on partially sorted data",
        "Simple to implement, no recursion required",
    ]
    disadvantages = [
        "Not stable",
        "Performance heavily depends on the chosen gap sequence",
        "Worst-case complexity still not competitive with O(n log n) algorithms",
    ]
    applications = [
        "Medium-sized arrays where Quick/Merge Sort overhead isn't justified",
        "Embedded systems needing a simple, in-place, better-than-O(n^2)-in-practice sort",
        "Used historically in the uClibc qsort() implementation for small inputs",
    ]
    pseudo_code = (
        "procedure shellSort(A, n)\n"
        "  gap = n / 2\n"
        "  while gap > 0\n"
        "    for i from gap to n - 1\n"
        "      temp = A[i]\n"
        "      j = i\n"
        "      while j >= gap and A[j - gap] > temp\n"
        "        A[j] = A[j - gap]\n"
        "        j -= gap\n"
        "      A[j] = temp\n"
        "    gap = gap / 2\n"
        "  return A"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        n = len(recorder.array)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                j = i
                while j >= gap and recorder.compare(j - gap, j):
                    recorder.swap(j - gap, j)
                    j -= gap
            gap //= 2

        for idx in range(n):
            recorder.mark_sorted(idx)
