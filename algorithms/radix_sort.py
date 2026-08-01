"""
algorithms/radix_sort.py

Radix Sort implementation (LSD, base 10), instrumented for step-by-step
visualization.

Radix Sort is a non-comparison-based algorithm that sorts integers digit
by digit, from the least significant digit (LSD) to the most significant,
using a stable Counting Sort as the subroutine for each digit pass.
Negative numbers are handled by offsetting the array to be non-negative
before sorting and restoring the offset afterward.
"""

from __future__ import annotations

from algorithms.base import BaseSorter, StepRecorder


class RadixSort(BaseSorter):
    name = "Radix Sort"
    best_case = "O(d * (n + b))"
    average_case = "O(d * (n + b))"
    worst_case = "O(d * (n + b))"
    space_complexity = "O(n + b)"
    is_stable = True
    is_in_place = False
    is_adaptive = False

    description = (
        "Radix Sort sorts integers digit by digit, using a stable sort "
        "(Counting Sort) as a subroutine for each digit, from least to most "
        "significant."
    )
    working_principle = (
        "Numbers are processed one digit position at a time, starting from "
        "the least significant digit (ones place). For each digit position, "
        "a stable counting sort buckets the entire array by the digit's "
        "value (0-9), producing a new ordering. Because each pass is stable, "
        "the relative order established by earlier (less significant) "
        "digits is preserved. After processing the most significant digit "
        "of the largest number, the array is fully sorted. Here d is the "
        "number of digits, n is array size, and b is the base (10)."
    )
    advantages = [
        "Linear time O(d * (n + b)) — can beat O(n log n) comparison sorts when d is small",
        "Stable, preserving relative order",
        "No comparisons needed between elements",
    ]
    disadvantages = [
        "Only applicable to integers (or fixed-format keys like strings)",
        "Requires extra memory for counting buckets each pass",
        "Performance degrades if the numbers have many digits (large d)",
    ]
    applications = [
        "Sorting large sets of fixed-width integers (e.g. phone numbers, IDs)",
        "String sorting via a similar digit-by-digit (character-by-character) approach",
        "Card-sorting machines historically inspired this algorithm's structure",
    ]
    pseudo_code = (
        "procedure radixSort(A, n)\n"
        "  max = max(A)\n"
        "  exp = 1\n"
        "  while max / exp > 0\n"
        "    countingSortByDigit(A, n, exp)\n"
        "    exp = exp * 10\n"
        "\n"
        "procedure countingSortByDigit(A, n, exp)\n"
        "  output = array of size n\n"
        "  count = array of zeros, size 10\n"
        "  for x in A: count[(x / exp) % 10] += 1\n"
        "  for i from 1 to 9: count[i] += count[i - 1]\n"
        "  for i from n - 1 down to 0\n"
        "    digit = (A[i] / exp) % 10\n"
        "    output[count[digit] - 1] = A[i]; count[digit] -= 1\n"
        "  A = output"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        arr = recorder.array
        n = len(arr)
        if n == 0:
            return

        # Radix Sort classically handles non-negative integers. Offset by
        # the minimum value (if negative) so all values become >= 0, then
        # restore the offset once sorting is complete.
        offset = min(arr)
        if offset < 0:
            for i in range(n):
                recorder.overwrite(i, recorder.array[i] - offset)

        max_val = max(recorder.array)
        exp = 1
        while max_val // exp > 0:
            self._counting_sort_by_digit(recorder, exp)
            exp *= 10

        if offset < 0:
            for i in range(n):
                recorder.overwrite(i, recorder.array[i] + offset)

        for i in range(n):
            recorder.mark_sorted(i)

    def _counting_sort_by_digit(self, recorder: StepRecorder, exp: int) -> None:
        arr = recorder.array
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for value in arr:
            digit = (value // exp) % 10
            count[digit] += 1
            recorder.comparisons += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            digit = (arr[i] // exp) % 10
            output[count[digit] - 1] = arr[i]
            count[digit] -= 1
            recorder.mark([i], "compare")

        for i in range(n):
            recorder.overwrite(i, output[i])
