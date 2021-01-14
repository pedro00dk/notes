from typing import Callable, Generator, Generic, Literal, Optional

from .abc import Priority, T


def sift_up(heap: list[T], k: int, i: int, comparator: Callable[[T, T], float]):
    """
    K-Heap sift up algorithm.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.
    Sift up moves the element at `i` up in the heap according to `comparator`.

    > complexity
    - time: `O(k*log(n, k))`
    - space: `O(1)`
    - `n`: length of `heap`
    - `k`: heap arity

    > parameters
    - `heap`: array containing heap structure
    - `k`: heap arity
    - `i`: index of value to sift up
    - `comparator`: a min comparator to check values (smaller values go to the top)
    """
    while (parent := (i - 1) // k) >= 0 and comparator(heap[i], heap[parent]) < 0:
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def sift_down(heap: list[T], k: int, i: int, comparator: Callable[[T, T], float], length: Optional[int] = None):
    """
    K-Heap sift down algorithm.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.
    Sift down moves the element at `i` down in the heap, up to `length - 1` index, according to `comparator`.

    > complexity
    - time: `O(k*log(n, k))`
    - space: `O(1)`
    - `n`: length of `heap`
    - `k`: heap arity

    > parameters
    - `heap`: array containing heap structure
    - `k`: heap arity
    - `i`: index of value to sift up
    - `comparator`: a min comparator to check values (smaller values go to the top)
    - `length`: limit the length of the heap
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


def heapify_top_down(heap: list[T], k: int, comparator: Callable[[T, T], float], length: Optional[int] = None):
    """
    Heapify the `heap` list using top down strategy.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.

    > complexity
    - time: `O(n*k*log(n, k))`
    - space: `O(1)`
    - `n`: length of `heap`
    - `k`: heap arity

    > parameters
    - `heap`: array containing heap structure
    - `k`: heap arity
    - `comparator`: a min comparator to check values (smaller values go to the top)
    - `length`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range(1, length):
        sift_up(heap, k, i, comparator)


def heapify_bottom_up(heap: list[T], k: int, comparator: Callable[[T, T], float], length: Optional[int] = None):
    """
    Heapify the `heap` list using bottom up strategy.
    This strategy is faster then top down.
    The `comparator` function is used to compare for a min heap.
    For a max heap, `comparator` output or logic can be negated.

    > complexity
    - time: `O(n*k)`
    - space: `O(1)`
    - `n`: length of `heap`
    - `k`: heap arity

    > parameters
    - `heap`: array containing heap structure
    - `k`: heap arity
    - `comparator`: a min comparator to check values (smaller values go to the top)
    - `length`: limit the length of the heap
    """
    length = length if length is not None else len(heap)
    for i in range((length - 2) // k, -1, -1):
        sift_down(heap, k, i, comparator, length)


class KHeap(Generic[T], Priority[T]):
    """
    K-Heap implementation.

    > complexity
    - space: `O(n)`
    - `n`: number of elements in the structure.
    """

    def __init__(
        self,
        comparator: Callable[[T, T], float],
        data: Optional[list[T]] = None,
        k: int = 4,
        strategy: Literal['bottom-up', 'top-down'] = 'bottom-up',
    ):
        """
        Initialize the binary heap

        > complexity
        - time: `O(n)` if `strategy == 'bottom-up'` else `O(n*k*log(n, k))`
        - space: `O(n)`
        - `n`: length of `data`
        - `k`: heap arity

        > parameters
        - `comparator`: a comparator function for heap values
        - `data`: initial data to populate the heap
        - `strategy`: initial heapify strategy, only impacts initial `data`
        """
        super().__init__()
        self._comparator = comparator
        self._heap: list[T] = data if data is not None else []
        self._k = k
        heapify_function = heapify_bottom_up if strategy == 'bottom-up' else heapify_top_down
        heapify_function(self._heap, self._k, self._comparator)

    def __str__(self) -> str:
        return f'{type(self).__name__} k={self._k} {str([*self])}'

    def __len__(self) -> int:
        return len(self._heap)

    def __iter__(self) -> Generator[T, None, None]:
        """
        Check base class.

        > complexity
        - time: `O(n*k*log(n, k))`
        - space: `O(n)`
        - `n`: length of the heap
        - `k`: arity of the heap
        """
        heap = self._heap.copy()
        for _ in range(len(heap)):
            yield heap[0]
            replacement = heap.pop()
            if len(heap) == 0:
                break
            heap[0] = replacement
            sift_down(heap, self._k, 0, self._comparator)

    def offer(self, value: T):
        """
        Check base class.

        > complexity
        - time: `O(k*log(n, k))`
        - space: `O(1)`
        - `n`: length of the heap
        - `k`: arity of the heap
        """
        self._heap.append(value)
        sift_up(self._heap, self._k, len(self._heap) - 1, self._comparator)

    def poll(self) -> T:
        """
        Check base class.

        > complexity
        - time: `O(k*log(n, k))`
        - space: `O(1)`
        - `n`: length of the heap
        - `k`: arity of the heap
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        value = self._heap[0]
        replacement = self._heap.pop()
        if len(self._heap) > 0:
            self._heap[0] = replacement
            sift_down(self._heap, self._k, 0, self._comparator)
        return value

    def peek(self) -> T:
        """
        Check base class.

        > complexity
        - time: `O(1)`
        - space: `O(1)`
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        return self._heap[0]


def test():
    import random

    from ..test import match

    heap = KHeap[int](lambda a, b: a - b, random.sample([i for i in range(10)], 10), 4)
    match((
        (print, (heap,)),
        (heap.offer, (10,)),
        (heap.offer, (11,)),
        (heap.offer, (12,)),
        (heap.offer, (13,)),
        (heap.offer, (14,)),
        (heap.offer, (15,)),
        (print, (heap,)),
        (heap.poll, (), 0),
        (heap.poll, (), 1),
        (print, (heap,)),
        (heap.poll, (), 2),
        (heap.poll, (), 3),
        (heap.poll, (), 4),
        (print, (heap,)),
        (heap.poll, (), 5),
        (heap.poll, (), 6),
        (heap.poll, (), 7),
        (heap.poll, (), 8),
        (print, (heap,)),
    ))


if __name__ == '__main__':
    test()
