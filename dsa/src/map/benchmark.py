def test():
    from ..test import benchmark
    from ..tree.avl import AVL
    from ..tree.bst import BST
    from ..tree.rbt import RBT
    from ..tree.veb import VEB
    from .abc import Map
    from .oa_hashtable import OpenAddressingHashtable
    from .sc_hashtable import SequenceChainingHashtable

    def test_map(data: list[int], map: Map[int, int]):
        for i in data:
            map.put(i, i)
        for i in data:
            map.take(i)

    def test_native(entries: list[int]):
        dct = dict[int, int]()
        for i in entries:
            dct[i] = i
        for i in entries:
            dct.pop(i)

    benchmark(
        (
            (
                '                open addressing hashtable - linear',
                lambda data: test_map(data, OpenAddressingHashtable[int, int]('linear')),
            ),
            (
                '       open addressing hashtable - quadratic prime',
                lambda data: test_map(data, OpenAddressingHashtable[int, int]('prime')),
            ),
            (
                '  open addressing hashtable - quadratic triangular',
                lambda data: test_map(data, OpenAddressingHashtable[int, int]('triangular')),
            ),
            (
                '              sequence chaining hashtable - linear',
                lambda data: test_map(data, SequenceChainingHashtable[int, int]('linear')),
            ),
            (
                '     sequence chaining hashtable - quadratic prime',
                lambda data: test_map(data, SequenceChainingHashtable[int, int]('prime')),
            ),
            (
                'sequence chaining hashtable - quadratic triangular',
                lambda data: test_map(data, SequenceChainingHashtable[int, int]('triangular')),
            ),
            (
                '                                binary search tree',
                lambda data: test_map(data, BST[int, int]()),
            ),
            (
                '                                          avl tree',
                lambda data: test_map(data, AVL[int, int]()),
            ),
            (
                '                                    red-black tree',
                lambda data: test_map(data, RBT[int, int]()),
            ),
            (
                '                                van Emde Boas tree',
                lambda data: test_map(data, VEB[int](16)),
            ),
            (
                '                                       native dict',
                lambda data: test_native(data),
            ),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [i for i in range(s)],
    )


if __name__ == '__main__':
    test()
