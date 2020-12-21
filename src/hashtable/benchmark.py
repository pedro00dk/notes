from typing import Any, cast


def test():
    from ..test import benchmark
    from .oa_hashtable import OAHashtable
    from .sc_hashtable import SCHashtable

    def test_oa_hashtable(entries: list[int], prober_name: str):
        hashtable = OAHashtable[int, int](cast(Any, prober_name))
        for i in entries:
            hashtable.put(i, i)
        for i in entries:
            hashtable.take(i)

    def test_sc_hashtable(entries: list[int], prober_name: str):
        hashtable = SCHashtable[int, int](cast(Any, prober_name))
        for i in entries:
            hashtable.put(i, i)
        for i in entries:
            hashtable.take(i)

    def test_native_dict(entries: list[int]):
        dct = dict[int, int]()
        for i in entries:
            dct[i] = i
        for i in entries:
            dct.pop(i)

    benchmark(
        (
            (
                '                hashtable (open addressing, linear)',
                lambda entries: test_oa_hashtable(entries, 'linear')
            ),
            (
                '       hashtable (open addressing, quadratic prime)',
                lambda entries: test_oa_hashtable(entries, 'prime')
            ),
            (
                '  hashtable (open addressing, quadratic triangular)',
                lambda entries: test_oa_hashtable(entries, 'triangular')
            ),
            (
                '              hashtable (sequence chaining, linear)',
                lambda entries: test_sc_hashtable(entries, 'linear')
            ),
            (
                '     hashtable (sequence chaining, quadratic prime)',
                lambda entries: test_sc_hashtable(entries, 'prime')
            ),
            (
                'hashtable (sequence chaining, quadratic triangular)',
                lambda entries: test_sc_hashtable(entries, 'triangular')
            ),
            (
                '                                       native dict',
                lambda entries: test_native_dict(entries)
            ),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [str(i) for i in range(s)],
    )


if __name__ == '__main__':
    test()
