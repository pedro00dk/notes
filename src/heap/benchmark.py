

def test():
    import heapq

    from ..test import benchmark
    from ..tree.abc import Tree
    from ..tree.avl import AVL
    # from ..tree.bst import BST
    from ..tree.rbt import RBT
    from .heap import BHeap
    from .kheap import KHeap

    def test_bheap(data: list[int]):
        heap = BHeap[int](lambda a, b: a - b, data)
        for _ in range(len(data)):
            heap.poll()

    def test_kheap(data: list[int], k: int):
        heap = KHeap[int](lambda a, b: a - b, data, k)
        for _ in range(len(data)):
            heap.poll()

    def test_tree_heap(data: list[int], tree: Tree[int, None]):
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
            ('       binary heap', lambda data: test_bheap(data)),
            ('  k-ary heap (k=2)', lambda data: test_kheap(data, 2)),
            ('  k-ary heap (k=4)', lambda data: test_kheap(data, 4)),
            ('  k-ary heap (k=8)', lambda data: test_kheap(data, 8)),
            (' k-ary heap (k=16)', lambda data: test_kheap(data, 16)),
            # ('binary search tree', lambda data: test_tree_heap(data, BST[int, None]())), # too slow
            ('          avl tree', lambda data: test_tree_heap(data, AVL[int, None]())),
            ('    red-black tree', lambda data: test_tree_heap(data, RBT[int, None]())),
            ('       native heap', lambda data: test_native_heap(data)),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [*reversed(range(s))],
        preprocess_input=list[int].copy
    )


if __name__ == '__main__':
    test()
