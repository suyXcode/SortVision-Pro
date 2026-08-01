"""
algorithms/heap_sort.py

Heap Sort implementation, instrumented for step-by-step visualization.

Heap Sort first builds a max-heap from the array, then repeatedly swaps
the root (maximum element) with the last unsorted element and "sifts
down" the new root to restore the heap property.
"""

from __future__ import annotations

from algorithms.base import BaseSorter, StepRecorder


class HeapSort(BaseSorter):
    name = "Heap Sort"
    best_case = "O(n log n)"
    average_case = "O(n log n)"
    worst_case = "O(n log n)"
    space_complexity = "O(1)"
    is_stable = False
    is_in_place = True
    is_adaptive = False

    description = (
        "Heap Sort uses a binary max-heap data structure, built in place on "
        "top of the array, to repeatedly extract the maximum element."
    )
    working_principle = (
        "The array is first rearranged into a max-heap, where every parent "
        "node is greater than or equal to its children (built bottom-up via "
        "sift-down / heapify). The root of the heap — the maximum element — "
        "is then swapped with the last element of the heap and the heap size "
        "shrinks by one. The new root is sifted down to restore the heap "
        "property, and the process repeats until the heap is empty, leaving "
        "the array fully sorted."
    )
    advantages = [
        "Guaranteed O(n log n) in all cases (best, average, worst)",
        "In-place: O(1) extra memory, no recursion stack blowup",
        "Useful base for priority queues and selection algorithms",
    ]
    disadvantages = [
        "Not stable",
        "Poor cache locality compared to Quick Sort / Merge Sort in practice",
        "Not adaptive: no speedup on nearly-sorted input",
    ]
    applications = [
        "Systems requiring guaranteed worst-case O(n log n) with O(1) memory",
        "Priority queue implementations",
        "Embedded or memory-constrained systems",
    ]
    pseudo_code = (
        "procedure heapSort(A, n)\n"
        "  buildMaxHeap(A, n)\n"
        "  for i from n - 1 down to 1\n"
        "    swap(A[0], A[i])\n"
        "    heapify(A, i, 0)\n"
        "\n"
        "procedure heapify(A, size, root)\n"
        "  largest = root; l = 2*root+1; r = 2*root+2\n"
        "  if l < size and A[l] > A[largest]: largest = l\n"
        "  if r < size and A[r] > A[largest]: largest = r\n"
        "  if largest != root\n"
        "    swap(A[root], A[largest])\n"
        "    heapify(A, size, largest)"
    )

    def _sort(self, recorder: StepRecorder) -> None:
        n = len(recorder.array)

        # Build a max-heap.
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(recorder, n, i)

        # Extract elements from the heap one at a time.
        for i in range(n - 1, 0, -1):
            recorder.swap(0, i)
            recorder.mark_sorted(i)
            self._heapify(recorder, i, 0)

        recorder.mark_sorted(0)

    def _heapify(self, recorder: StepRecorder, size: int, root: int) -> None:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size:
            recorder.mark([left, largest], "compare")
            if recorder.compare(left, largest):
                largest = left

        if right < size:
            recorder.mark([right, largest], "compare")
            if recorder.compare(right, largest):
                largest = right

        if largest != root:
            recorder.swap(root, largest)
            self._heapify(recorder, size, largest)
