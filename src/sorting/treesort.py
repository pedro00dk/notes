from typing import Callable

from ..tree.abc import Tree
from ..tree.avl import AVL
from ..tree.bst import BST
from ..tree.rbt import RBT


def treesort(array: list[float], tree: Tree[float, int]) -> list[float]:
    """
    Sort `array` using treesort.

    > complexity
    - time: `O(n*Tree.put + Tree.__iter__)` 
    - space: `O(n)`
    - `n`: length of `array`

    > parameters
    - `array`: array to be sorted
    - `tree`: an empty tree instance
    - `return`: `array` sorted
    """
    if len(tree) > 0:
        raise Exception('tree must be empty')
    replacer: Callable[[int, int], int] = lambda count, old_count: old_count + count
    for value in array:
        tree.put(value, 1, replacer)
    k = 0
    for key, value in tree:
        for i in range(value):
            array[k + i] = key
        k += value
    return array


def test():
    from ..test import sort_benchmark

    sort_benchmark(
        (
            ('treesort bst', lambda array: treesort(array, BST[float, int]())),
            ('treesort avl', lambda array: treesort(array, AVL[float, int]())),
            ('treesort rbt', lambda array: treesort(array, RBT[float, int]())),
        ),
    )


if __name__ == '__main__':
    test()
