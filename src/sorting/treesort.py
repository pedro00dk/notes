from ..tree.abc import Tree
from ..tree.avl import AVL
from ..tree.bst import BST
from ..tree.rbt import RBT


def treesort(array: list, tree_constructor: Tree = RBT):
    """
    Treesort implementation.

    > complexity:
    - time: `O(n*O(tree.put))` 
    - space: `O(n)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted
    - `tree_constructor: (() => (<T> extends Tree))? = RBT`: tree constructor to be used in sorting

    > `return: (int | float)[]`: `array` sorted
    """
    replacer = lambda count, old_count: old_count + count
    tree = tree_constructor()
    for value in array:
        tree.put(value, 1, replacer)
    k = 0
    for key, value, depth in tree.traverse():
        for i in range(value):
            array[k + i] = key
        k += value
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark(
        [
            ('bstsort', lambda array: treesort(array, BST)),
            ('avlsort', lambda array: treesort(array, AVL)),
            ('rbtsort', lambda array: treesort(array, RBT))
        ]
    )


if __name__ == '__main__':
    test()
