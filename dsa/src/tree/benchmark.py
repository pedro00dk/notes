def test():
    import random

    from ..test import benchmark
    from .abc import Tree
    from .avl import AVL
    from .bst import BST
    from .rbt import RBT
    from .veb import VEB

    def test_tree(entries: list[int], tree: Tree[int, None]):
        for i in entries:
            tree.put(i, None)
        for i in entries:
            tree.take(i)

    print('random insertions')
    benchmark(
        (
            ('binary search tree', lambda data: test_tree(data, BST[int, None]())),
            ('          avl tree', lambda data: test_tree(data, AVL[int, None]())),
            ('    red-black tree', lambda data: test_tree(data, RBT[int, None]())),
            ('van Emde Boas tree', lambda data: test_tree(data, VEB[None](16))),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s: random.sample(range(s), s),
    )
    print('sequential insertions')
    benchmark(
        (
            ('binary search tree', lambda data: test_tree(data, BST[int, None]())),
            ('          avl tree', lambda data: test_tree(data, AVL[int, None]())),
            ('    red-black tree', lambda data: test_tree(data, RBT[int, None]())),
            ('van Emde Boas tree', lambda data: test_tree(data, VEB[None](16))),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000),
        bench_input=lambda s: [*range(s)],
    )


if __name__ == '__main__':
    test()
