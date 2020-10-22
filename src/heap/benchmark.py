def test():
    import heapq
    from ..test import benchmark
    from .heap import BHeap
    from .kheap import KHeap

    def test_bheap(data: list):
        h = BHeap(data, 'max')
        for i in range(len(data)):
            h.poll()

    def test_kheap(data: list, k: int):
        h = KHeap(data, 'max', k)
        for i in range(len(data)):
            h.poll()
    
    def test_native_heap(data: list):
        h = data
        heapq.heapify(h)
        for i in range(len(data)):
            heapq.heappop(h)

    benchmark(
        [
            ('      binary heap', lambda data: test_bheap([*data])),
            (' k-ary heap (k=2)', lambda data: test_kheap([*data], 2)),
            (' k-ary heap (k=4)', lambda data: test_kheap([*data], 4)),
            (' k-ary heap (k=8)', lambda data: test_kheap([*data], 8)),
            ('k-ary heap (k=16)', lambda data: test_kheap([*data], 16)),
            ('      native heap', lambda data: test_native_heap([*data]))
        ],
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [*range(s)]
    )


if __name__ == '__main__':
    test()
