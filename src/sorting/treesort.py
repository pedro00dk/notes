from typing import Callable
from ..tree.abc import Tree
from ..tree.avl import AVL
from ..tree.bst import BST
from ..tree.rbt import RBT


def treesort(array: list[float], tree: Tree[float, int]) -> list[float]:
    """
    Sort `array` using treesort.

    > complexity
    - time: `O(n*O(tree.put))` 
    - space: `O(n)`

    > parameters
    - `array`: array to be sorted
    - `tree`: an empty tree instance
    - `return`: `array` sorted
    """
    assert tree.empty(), 'tree must be empty'
    replacer: Callable[[int, int], int] = lambda count, old_count: old_count + count
    for value in array:
        tree.put(value, 1, replacer)
    k = 0
    for key, value, _ in tree.traverse():
        for i in range(value):
            array[k + i] = key
        k += value
    return array


def test():
    from ..test import sort_benchmark

    sort_benchmark(
        (
            ('bstsort', lambda array: treesort(array, BST())),
            ('avlsort', lambda array: treesort(array, AVL())),
            ('rbtsort', lambda array: treesort(array, RBT()))
        )
    )


if __name__ == '__main__':
    test()
