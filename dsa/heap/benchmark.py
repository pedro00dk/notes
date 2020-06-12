def test():
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

    benchmark(
        [
            ('      binary heap', lambda data: test_bheap([*data])),
            (' k-ary heap (k=2)', lambda data: test_kheap([*data], 2)),
            (' k-ary heap (k=4)', lambda data: test_kheap([*data], 4)),
            (' k-ary heap (k=8)', lambda data: test_kheap([*data], 8)),
            ('k-ary heap (k=16)', lambda data: test_kheap([*data], 16))
        ],
        test_input_iter=(),
        bench_size_iter=(1, 10, 100, 1000, 10000),
        bench_input=lambda s, r: [*range(s)],
        test_print_input=False,
        test_print_output=False
    )


if __name__ == '__main__':
    test()
