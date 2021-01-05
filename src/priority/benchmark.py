from typing import Callable


def test():
    import heapq
    import random

    from ..test import benchmark
    from ..tree.avl import AVL
    from ..tree.bst import BST
    from ..tree.rbt import RBT
    from ..tree.veb import VEB
    from .abc import Priority
    from .heap import Heap
    from .kheap import KHeap

    def test_priority(data: list[int], priority: Priority[int]):
        for v in data:
            priority.offer(v)
        for _ in range(len(data)):
            priority.poll()

    def test_heap(data: list[int], initializer: Callable[[list[int]], Priority[int]]):
        # heaps can do heapify on initialization
        heap = initializer(data)
        for _ in range(len(data)):
            heap.poll()

        # heap = KHeap[int](lambda a, b: a - b, data, k)

    def test_native_heap(data: list[int]):
        heap = data
        heapq.heapify(heap)
        for _ in range(len(data)):
            heapq.heappop(heap)

    benchmark(
        (
            ('                      heap', lambda data: test_priority(data, Heap[int](lambda a, b: a - b))),
            ('            heap (heapify)', lambda d: test_heap(d, lambda d: Heap[int](lambda a, b: a - b, d))),
            ('          k-ary heap (k=2)', lambda data: test_priority(data, KHeap[int](lambda a, b: a - b, k=2))),
            (' k-ary heap (k=2, heapify)', lambda d: test_heap(d, lambda d: KHeap[int](lambda a, b: a - b, d, 2))),
            ('          k-ary heap (k=4)', lambda data: test_priority(data, KHeap[int](lambda a, b: a - b, k=4))),
            (' k-ary heap (k=4, heapify)', lambda d: test_heap(d, lambda d: KHeap[int](lambda a, b: a - b, d, 4))),
            ('          k-ary heap (k=8)', lambda data: test_priority(data, KHeap[int](lambda a, b: a - b, k=8))),
            (' k-ary heap (k=8, heapify)', lambda d: test_heap(d, lambda d: KHeap[int](lambda a, b: a - b, d, 8))),
            ('         k-ary heap (k=16)', lambda data: test_priority(data, KHeap[int](lambda a, b: a - b, k=16))),
            ('k-ary heap (k=16, heapify)', lambda d: test_heap(d, lambda d: KHeap[int](lambda a, b: a - b, d, 16))),
            ('        binary search tree', lambda data: test_priority(data, BST[int, None]())),
            ('                  avl tree', lambda data: test_priority(data, AVL[int, None]())),
            ('            red-black tree', lambda data: test_priority(data, RBT[int, None]())),
            ('        van Emde Boas tree', lambda data: test_priority(data, VEB[None]())),
            ('               native heap', lambda data: test_native_heap(data)),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [*random.sample(range(s), s)],
        preprocess_input=list[int].copy
    )


if __name__ == '__main__':
    test()
