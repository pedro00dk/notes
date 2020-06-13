def test():
    import random
    from ..test import benchmark
    from .avl import AVL
    from .bst import BST
    from .rbt import RBT

    def test_bst(entries: list):
        t = BST()
        for i in entries:
            t.put(i)
        for i in entries:
            t.take(i)

    def test_avl_r2(entries: list):
        t = AVL(2)
        for i in entries:
            t.put(i)
        for i in entries:
            t.take(i)

    def test_avl_r4(entries: list):
        t = AVL(4)
        for i in entries:
            t.put(i)
        for i in entries:
            t.take(i)

    def test_rbt(entries: list):
        t = RBT()
        for i in entries:
            t.put(i)
        for i in entries:
            t.take(i)

    print('random insertions')
    benchmark(
        [
            ('binary search tree', test_bst),
            ('    avl tree (r=2)', test_avl_r2),
            ('    avl tree (r=4)', test_avl_r4),
            ('    red-black tree', test_rbt)
        ],
        test_input_iter=(),
        bench_size_iter=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s, r: random.sample([*range(s)], s),
        bench_tries=1,
        bench_repeats=100,
        test_print_input=False,
        test_print_output=False
    )
    print('sequential insertions')
    benchmark(
        [
            ('binary search tree', test_bst),
            ('    avl tree (r=2)', test_avl_r2),
            ('    avl tree (r=4)', test_avl_r4),
            ('    red-black tree', test_rbt)
        ],
        test_input_iter=(),
        bench_size_iter=(0, 1, 10, 100, 1000, 10000),
        bench_input=lambda s, r: [*range(s)],
        bench_tries=1,
        bench_repeats=100,
        test_print_input=False,
        test_print_output=False
    )


if __name__ == '__main__':
    test()
