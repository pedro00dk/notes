from .abc import Heap


def sift_up(heap: list, k: int, i: int, comparator):
    """
    K-Heap sift up algorithm.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.
    Sift up moves the element at `i` up in the heap according to `comparator`.

    > complexity:
    - time: `O(k*log(n, k))`
    - space: `O(1)`

    > parameters:
    - `heap: <T>[]`: array containing heap structure
    - `k: int`: heap arity
    - `i: int`: index of value to sift up
    - `comparator: (<T>, <T>) => int`: a min comparator to check values (smaller values go to the top)
    """
    while (parent := (i - 1) // k) >= 0 and comparator(heap[i], heap[parent]) < 0:
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def sift_down(heap: list, k: int, i: int, comparator, /, length: int = None):
    """
    K-Heap sift down algorithm.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.
    Sift down moves the element at `i` down in the heap, up to `length - 1` index, according to `comparator`.

    > complexity:
    - time: `O(k*log(n, k))`
    - space: `O(1)`

    > parameters:
    - `heap: <T>[]`: array containing heap structure
    - `k: int`: heap arity
    - `i: int`: index of value to sift up
    - `comparator: (<T>, <T>) => int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    while True:
        chosen = i
        broke = False
        for j in range(k):
            child = i * k + j + 1
            if child >= length:
                broke = True
                break
            if comparator(heap[chosen], heap[child]) > 0:
                chosen = child
        if chosen == i:
            break
        heap[i], heap[chosen] = heap[chosen], heap[i]
        if broke:
            break
        i = chosen


def heapify_top_down(heap: list, k: int, comparator, /, length: int = None):
    """
    Heapify the `heap` list using top down strategy.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.

    > complexity:
    - time: `O(n*k*log(n, k))`
    - space: `O(1)`

    > parameters:
    - `heap: <T>[]`: array containing heap structure
    - `k: int`: heap arity
    - `comparator: (<T>, <T>) => int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range(1, length):
        sift_up(heap, k, i, comparator)


def heapify_bottom_up(heap: list, k: int, comparator, /, length: int = None):
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
    - `k: int`: heap arity
    - `comparator: (<T>, <T>) => int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range((length - 2) // k, -1, -1):
        sift_down(heap, k, i, comparator, length)


class KHeap(Heap):
    """
    K-Heap implementation.
    """

    def __init__(self, /, data: list = None, comparator='max', k=4):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`
        """
        super().__init__(data, comparator)
        self._k = k
        # heapify_top_down(self._heap, self._k, self._comparator)
        heapify_bottom_up(self._heap, self._k, self._comparator)

    def __str__(self):
        return f'k={self._k} {super().__str__()}'

    def offer(self, value):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(k*log(n, k))`
        - space: `O(1)`
        """
        self._heap.append(value)
        sift_up(self._heap, self._k, len(self._heap) - 1, self._comparator)

    def poll(self):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(k*log(n, k))`
        - space: `O(1)`
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        value = self._heap[0]
        replacement = self._heap.pop()
        if len(self._heap) > 0:
            self._heap[0] = replacement
            sift_down(self._heap, self._k, 0, self._comparator)
        return value


def test():
    import random
    from ..test import match
    h = KHeap(random.sample([i for i in range(10)], 10), 'min', 4)
    match([
        (print, (h,)),
        (h.offer, (10,)),
        (h.offer, (11,)),
        (h.offer, (12,)),
        (h.offer, (13,)),
        (h.offer, (14,)),
        (h.offer, (15,)),
        (print, (h,)),
        (h.poll, (), 0),
        (h.poll, (), 1),
        (print, (h,)),
        (h.poll, (), 2),
        (h.poll, (), 3),
        (h.poll, (), 4),
        (print, (h,)),
        (h.poll, (), 5),
        (h.poll, (), 6),
        (h.poll, (), 7),
        (h.poll, (), 8),
        (print, (h,))
    ])


if __name__ == '__main__':
    test()