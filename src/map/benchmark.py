from typing import Any, cast


def test():
    from ..test import benchmark
    from ..tree.abc import Tree
    from ..tree.avl import AVL
    from ..tree.bst import BST
    from ..tree.rbt import RBT
    from .oa_hashtable import OpenAddressingHashtable
    from .sc_hashtable import SequenceChainingHashtable

    def test_oa_hashtable(entries: list[int], prober_name: str):
        hashtable = OpenAddressingHashtable[int, int](cast(Any, prober_name))
        for i in entries:
            hashtable.put(i, i)
        for i in entries:
            hashtable.take(i)

    def test_sc_hashtable(entries: list[int], prober_name: str):
        hashtable = SequenceChainingHashtable[int, int](cast(Any, prober_name))
        for i in entries:
            hashtable.put(i, i)
        for i in entries:
            hashtable.take(i)

    def test_tree(entries: list[int], tree: Tree[int, int]):
        for i in entries:
            tree.put(i, i)
        for i in entries:
            tree.take(i)

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
                '                                 binary search tree',
                lambda entries: test_tree(entries, BST[int, int]())
            ),
            (
                '                                           avl tree',
                lambda entries: test_tree(entries, AVL[int, int]())
            ),
            (
                '                                     red-black tree',
                lambda entries: test_tree(entries, RBT[int, int]())
            ),
            (
                '                                        native dict',
                lambda entries: test_native_dict(entries)
            ),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [str(i) for i in range(s)],
    )


if __name__ == '__main__':
    test()
