def test():
    from ..test import benchmark
    from .abc import Prober
    from .oa_hashtable import OAHashtable
    from .sc_hashtable import SCHashtable

    def test_oa_hashtable(entries: list, prober: Prober):
        h = OAHashtable(prober)
        for i in entries:
            h.put(i)
        for i in entries:
            h.take(i)

    def test_sc_hashtable(entries: list, prober: Prober):
        h = SCHashtable(prober)
        for i in entries:
            h.put(i)
        for i in entries:
            h.take(i)

    def test_native_dict(entries: list):
        d = dict()
        for i in entries:
            d[i] = None
        for i in entries:
            d.pop(i)

    benchmark(
        [
            (
                '                open addressing hashtable (linear)',
                lambda entries: test_oa_hashtable(entries, Prober.LINEAR)
            ),
            (
                '       open addressing hashtable (quadratic prime)',
                lambda entries: test_oa_hashtable(entries, Prober.QUADRATIC_PRIME)
            ),
            (
                '  open addressing hashtable (quadratic triangular)',
                lambda entries: test_oa_hashtable(entries, Prober.QUADRATIC_TRIANGULAR)
            ),
            (
                '              sequence chaining hashtable (linear)',
                lambda entries: test_sc_hashtable(entries, Prober.LINEAR)
            ),
            (
                '     sequence chaining hashtable (quadratic prime)',
                lambda entries: test_sc_hashtable(entries, Prober.QUADRATIC_PRIME)
            ),
            (
                'sequence chaining hashtable (quedratic triangular)',
                lambda entries: test_sc_hashtable(entries, Prober.QUADRATIC_TRIANGULAR)
            ),
            (
                '                                       native dict',
                lambda entries: test_native_dict(entries)
            )
        ],
        test_input_iter=(),
        bench_size_iter=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s, r: [str(i) for i in range(s)],
        test_print_input=False,
        test_print_output=False
    )


if __name__ == '__main__':
    test()
