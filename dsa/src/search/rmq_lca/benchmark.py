
def test():
    import random

    from ...test import benchmark
    from .abc import RangeMinimumQuery, lca_to_rmq, rmq_to_lca
    from .naive import RangeMinimumQueryNaive
    from .v2 import RangeMinimumQueryV2
    from .v3 import RangeMinimumQueryV3
    from .v4 import RangeMinimumQueryV4

    def test_v4_build(data: list[int]):
        _, _, root, _, get_children = rmq_to_lca(data)
        data_plus_minus_1, _, _ = lca_to_rmq(
            root, lambda node: node.index, get_children, lambda node: node.index, True, True
        )
        return RangeMinimumQueryV4(data_plus_minus_1)

    def test_query(rmq: RangeMinimumQuery[int], queries: list[tuple[int, int]]):
        for query in queries:
            i, j = query
            i, j = (i, j) if i < j else (j, i)
            rmq.rmq(i, j)

    def test_v4_query(
        rmq: RangeMinimumQueryV4,
        backward_mapper: list[int],
        forward_mapper: dict[int, list[int]],
        queries: list[tuple[int, int]],
    ):
        for query in queries:
            i, j = query
            i, j = (i, j) if i < j else (j, i)
            backward_mapper[rmq.rmq(forward_mapper[i][0], forward_mapper[j][-1])]

    print('build benchmark')
    benchmark(
        (
            ('range minimum query naive', lambda data: RangeMinimumQueryNaive[int](data)),
            ('range minimum query v2', lambda data: RangeMinimumQueryV2[int](data)),
            ('range minimum query v3', lambda data: RangeMinimumQueryV3[int](data)),
            ('range minimum query v4', lambda data: test_v4_build(data)),
        ),
        test_inputs=(),
        bench_sizes=(1, 10, 100, 1000),
        bench_input=lambda s: [random.randint(-1000, 1000) for _ in range(s)],
    )
    print('build benchmark without naive')
    benchmark(
        (
            ('range minimum query v2', lambda data: RangeMinimumQueryV2[int](data)),
            ('range minimum query v3', lambda data: RangeMinimumQueryV3[int](data)),
            ('range minimum query v4', lambda data: test_v4_build(data)),
        ),
        test_inputs=(),
        bench_sizes=(10000, 100000),
        bench_input=lambda s: [random.randint(-1000, 1000) for _ in range(s)],
    )
    length = 10000
    data = [random.randint(-1000, 1000) for _ in range(length)]
    _, _, root, _, get_children = rmq_to_lca(data)
    data_plus_minus_1, backward_mapper, forward_mapper = lca_to_rmq(
        root, lambda node: node.index, get_children, lambda node: node.index, True, True
    )
    rmq_naive = RangeMinimumQueryNaive(data)
    rmq_v2 = RangeMinimumQueryV2(data)
    rmq_v3 = RangeMinimumQueryV3(data)
    rmq_v4 = RangeMinimumQueryV4(data_plus_minus_1)
    print('query benchmark')
    benchmark(
        (
            ('range minimum query naive', lambda queries: test_query(rmq_naive, queries)),
            ('range minimum query v2', lambda queries: test_query(rmq_v2, queries)),
            ('range minimum query v3', lambda queries: test_query(rmq_v3, queries)),
            ('range minimum query v4', lambda queries: test_v4_query(rmq_v4, backward_mapper, forward_mapper, queries)),
        ),
        test_inputs=(),
        bench_sizes=(100000,),
        bench_input=lambda s: [(random.randint(0, length - 1), random.randint(0, length - 1)) for _ in range(s)],
    )


if __name__ == '__main__':
    test()
