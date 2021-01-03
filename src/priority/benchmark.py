

def test():
    import heapq
    import random

    from ..test import benchmark
    from ..tree.abc import Tree
    from ..tree.avl import AVL
    from ..tree.bst import BST
    from ..tree.rbt import RBT
    from .heap import Heap
    from .kheap import KHeap

    def test_heap(data: list[int]):
        heap = Heap[int](lambda a, b: a - b, data)
        for _ in range(len(data)):
            heap.poll()

    def test_kheap(data: list[int], k: int):
        heap = KHeap[int](lambda a, b: a - b, data, k)
        for _ in range(len(data)):
            heap.poll()

    def test_tree(data: list[int], tree: Tree[int, None]):
        for v in data:
            tree.offer(v)
        for _ in range(len(data)):
            tree.poll()

    def test_native_heap(data: list[int]):
        heap = data
        heapq.heapify(heap)
        for _ in range(len(data)):
            heapq.heappop(heap)

    benchmark(
        (
            ('              heap', lambda data: test_heap(data)),
            ('  k-ary heap (k=2)', lambda data: test_kheap(data, 2)),
            ('  k-ary heap (k=4)', lambda data: test_kheap(data, 4)),
            ('  k-ary heap (k=8)', lambda data: test_kheap(data, 8)),
            (' k-ary heap (k=16)', lambda data: test_kheap(data, 16)),
            ('binary search tree', lambda data: test_tree(data, BST[int, None]())),  # too slow
            ('          avl tree', lambda data: test_tree(data, AVL[int, None]())),
            ('    red-black tree', lambda data: test_tree(data, RBT[int, None]())),
            ('       native heap', lambda data: test_native_heap(data)),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [*random.sample(range(s), s)],
        preprocess_input=list[int].copy
    )


if __name__ == '__main__':
    test()
