def sift_up(heap: list, k: int, i: int, comparator: type(lambda a, b: 0)):
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
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
    """
    while (parent := (i - 1) // k) >= 0 and comparator(heap[i], heap[parent]) < 0:
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def sift_down(heap: list, k: int, i: int, comparator: type(lambda a, b: 0), /, length: int = None):
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
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
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


def heapify_top_down(heap: list, k: int, comparator: type(lambda a, b: 0), /, length: int = None):
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
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range(1, length):
        sift_up(heap, k, i, comparator)


def heapify_bottom_up(heap: list, k: int, comparator: type(lambda a, b: 0), /, length: int = None):
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
    - `comparator: (<T>, <T>) -> int`: a min comparator to check values (smaller values go to the top)
    - `length: int? = len(heap)`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range((length - 2) // k, -1, -1):
        sift_down(heap, k, i, comparator, length)


class KHeap:
    """
    K-Heap implementation.
    """

    def __init__(self, /, data: list = None, k=4, comparator='max'):
        """
        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > parameters:
        - `data: <T>[]`: initial data to populate the heap
        - `k: int? = 4`: heap arity
        - `comparator: 'min' | 'max' | (<T>, <T>) -> int`: a comparator string for numeric values (`min`, `max`) or a
            min comparator to check values (smaller values go to the top)
        """
        self._heap = data if data is not None else []
        self._k = k
        self._comparator = (lambda a, b: a - b) if comparator == 'min' else \
            (lambda a, b: b - a) if comparator == 'max' else comparator
        # heapify_top_down(self._heap, self._k, self._comparator)
        heapify_bottom_up(self._heap, self._k, self._comparator)

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return f'Heap {self._heap}'

    def offer(self, value):
        """
        Insert `value` in the heap.

        > complexity:
        - time: `O(k*log(n, k))`
        - space: `O(1)`

        > parameters:
        - `value: <T>`: value to insert
        """
        self._heap.append(value)
        sift_up(self._heap, self._k, len(self._heap) - 1, self._comparator)

    def poll(self):
        """
        Delete the value at the top of the heap.

        > complexity:
        - time: `O(k*log(n, k))`
        - space: `O(1)`

        > `return: <T>`: deleted value
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        value = self._heap[0]
        replacement = self._heap.pop()
        if len(self._heap) > 0:
            self._heap[0] = replacement
            sift_down(self._heap, self._k, 0, self._comparator)
        return value

    def peek(self):
        """
        Get the value at the top of the heap without removing it.

        > complexity:
        > time: `O(1)`
        > space: `O(1)`

        > `return: <T>`: value at the top of the heap
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        return self._heap[0]

    def empty(self):
        return len(self._heap) == 0


def test():
    import random
    from ..test import match
    h = KHeap(random.sample([i for i in range(10)], 10), 4, 'min')
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
