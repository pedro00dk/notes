from typing import Callable, Generic, Optional, TypeVar
from .abc import Node, Tree


T = TypeVar('T', bool, int, float, str)
U = TypeVar('U')


class BST(Generic[T, U], Tree[T, U]):
    """
    Binary Search Tree implementation.
    """

    def __init__(self):
        super().__init__()
        self._root: Optional[Node[T, U]] = None

    def put(self, key: T, value: U, replacer: Optional[Callable[[U, U], U]] = None) -> Optional[U]:
        """
        Check abstract class for documentation.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: `O(1)`
        """
        parent = None
        node = self._root
        while node is not None and key != node.key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            if parent is None:
                self._root = Node(key, value)
            elif key < parent.key:
                parent.left = Node(key, value)
            else:
                parent.right = Node(key, value)
            self._size += 1
        else:
            old_value = node.value
            node.key = key
            node.value = replacer(value, node.value) if replacer is not None else value
            return old_value

    def take(self, key: T) -> U:
        """
        Check abstract class for documentation.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: `O(1)`
        """
        parent = None
        node = self._root
        while node is not None and key != node.key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError(f'key ({key}) not found')
        if node.left is not None and node.right is not None:
            parent = node
            successor = node.right
            while successor.left is not None:
                parent = successor
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node = successor
        if parent is None:
            self._root = node.left if node.left is not None else node.right
        elif parent.left == node:
            parent.left = node.left if node.left is not None else node.right
        elif parent.right == node:
            parent.right = node.left if node.left is not None else node.right
        self._size -= 1
        return node.value


def test():
    from ..test import match

    tree = BST[int, Optional[int]]()
    match((
        (tree.put, (-15, -1000)),
        (tree.put, (-10, None)),
        (tree.put, (-5, None)),
        (tree.put, (0, None)),
        (tree.put, (5, 1000)),
        (tree.put, (10, None)),
        (tree.put, (15, None)),
        (tree.get, (5,), 1000),
        (tree.get, (-15,), -1000),
        (print, (tree,)),
        (tree.take, (0,)),
        (tree.take, (-10,)),
        (tree.take, (-15,), -1000),
        (print, (tree,)),
    ))
    for key, *_ in tree.traverse('pre'):
        print(key, end=' ')
    print()
    for key, *_ in tree.traverse('in'):
        print(key, end=' ')
    print()
    for key, *_ in tree.traverse('post'):
        print(key, end=' ')
    print()
    for key, *_ in tree.traverse('breadth'):
        print(key, end=' ')
    print()


if __name__ == '__main__':
    test()
