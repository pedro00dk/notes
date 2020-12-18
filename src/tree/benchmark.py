def test():
    import random

    from ..test import benchmark
    from .avl import AVL
    from .bst import BST
    from .rbt import RBT

    def test_bst(entries: list[int]):
        tree = BST[int, None]()
        for i in entries:
            tree.put(i, None)
        for i in entries:
            tree.take(i)

    def test_avl(entries: list[int], rank: int):
        tree = AVL[int, None](rank)
        for i in entries:
            tree.put(i, None)
        for i in entries:
            tree.take(i)

    def test_rbt(entries: list[int]):
        tree = RBT[int, None]()
        for i in entries:
            tree.put(i, None)
        for i in entries:
            tree.take(i)

    print('random insertions')
    benchmark(
        (
            (' binary search tree', test_bst),
            ('    avl tree rank 2', lambda entries: test_avl(entries, 2)),
            ('    avl tree rank 3', lambda entries: test_avl(entries, 3)),
            ('    avl tree rank 4', lambda entries: test_avl(entries, 4)),
            ('     red-black tree', test_rbt),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: random.sample([*range(s)], s),
    )
    print('sequential insertions')
    benchmark(
        (
            ('binary search tree', test_bst),
            ('   avl tree rank 2', lambda entries: test_avl(entries, 2)),
            ('   avl tree rank 3', lambda entries: test_avl(entries, 3)),
            ('   avl tree rank 4', lambda entries: test_avl(entries, 4)),
            ('    red-black tree', test_rbt),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: [*range(s)],
    )


if __name__ == '__main__':
    test()
