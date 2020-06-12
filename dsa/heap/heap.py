from .abc import Heap


def sift_up(heap: list, i: int, comparator):
    """
    Binary Heap sift up algorithm.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.
    Sift up moves the element at `i` up in the heap according to `comparator`.

    > complexity:
    - time: `O(log(n))`
    - space: `O(1)`

    > parameters:
    - `heap: <T>[]`: array containing heap structure
    - `i: int`: index of value to sift up
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
    """
    while (parent := (i - 1) // 2) >= 0 and comparator(heap[i], heap[parent]) < 0:
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def sift_down(heap: list, i: int, comparator, /, length: int = None):
    """
    Binary Heap sift down algorithm.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.
    Sift down moves the element at `i` down in the heap, up to `length - 1` index, according to `comparator`.

    > complexity:
    - time: `O(log(n))`
    - space: `O(1)`

    > parameters:
    - `heap: <T>[]`: array containing heap structure
    - `i: int`: index of value to sift up
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    while (left := i * 2 + 1) and left < length:
        right = left + 1
        chosen = i
        if comparator(heap[chosen], heap[left]) > 0:
            chosen = left
        if right < length and comparator(heap[chosen], heap[right]) > 0:
            chosen = right
        if chosen == i:
            break
        heap[i], heap[chosen] = heap[chosen], heap[i]
        i = chosen


def heapify_top_down(heap: list, comparator, /, length: int = None):
    """
    Heapify the `heap` list using top down strategy.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.

    > complexity:
    - time: `O(n*log(n))`
    - space: `O(1)`

    > parameters:
    - `heap: <T>[]`: array containing heap structure
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range(1, length):
        sift_up(heap, i, comparator)


def heapify_bottom_up(heap: list, comparator, /, length: int = None):
    """
    Heapify the `heap` list using bottom up strategy.
    This strategy is faster then top down.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.

    > complexity:
    - time: `O(n)`
    - space: `O(1)`

    > parameters:
    - `heap: <T>[]`: array containing heap structure
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range((length - 2) // 2, -1, -1):
        sift_down(heap, i, comparator, length)


class BHeap(Heap):
    """
    Binary Heap implementation.
    """

    def __init__(self, /, data: list = None, comparator='max'):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`
        """
        super().__init__(data, comparator)
        # heapify_top_down(self._heap, self._comparator)
        heapify_bottom_up(self._heap, self._comparator)

    def offer(self, value):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(log(n))`
        - space: `O(1)`
        """
        self._heap.append(value)
        sift_up(self._heap, len(self._heap) - 1, self._comparator)

    def poll(self):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(log(n))`
        - space: `O(1)`
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        value = self._heap[0]
        replacement = self._heap.pop()
        if len(self._heap) > 0:
            self._heap[0] = replacement
            sift_down(self._heap, 0, self._comparator)
        return value


def test():
    import random
    from ..test import match
    h = BHeap(random.sample([i for i in range(10)], 10), 'min')
    match([
        (print, [h], None),
        (h.offer, [10], None),
        (h.offer, [11], None),
        (h.offer, [12], None),
        (h.offer, [13], None),
        (h.offer, [14], None),
        (h.offer, [15], None),
        (print, [h], None),
        (h.poll, [], 0),
        (h.poll, [], 1),
        (print, [h], None),
        (h.poll, [], 2),
        (h.poll, [], 3),
        (h.poll, [], 4),
        (print, [h], None),
        (h.poll, [], 5),
        (h.poll, [], 6),
        (h.poll, [], 7),
        (h.poll, [], 8),
        (print, [h], None)
    ])


if __name__ == '__main__':
    test()
