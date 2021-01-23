from __future__ import annotations

import collections
import dataclasses
from typing import Any, Callable, Generator, Generic, Literal, Optional, cast

from ..map.abc import Map
from ..priority.abc import Priority
from .abc import K, Tree, V


@dataclasses.dataclass
class Node(Generic[K, V]):
    """
    Base Node class for trees.
    """
    key: K
    value: V
    left: Optional[Node[K, V]] = None
    right: Optional[Node[K, V]] = None


class BST(Generic[K, V], Tree[K, V]):
    """
    Binary Search Tree implementation.

    > complexity
    - space: `O(n)`
    - `n`: number of elements in the structure
    """

    def __init__(self):
        super().__init__()
        self._root: Optional[Node[K, V]] = None
        self._size: int = 0

    def __str__(self) -> str:
        nodes = '\n'.join(f'{"|  " * depth}├─ {key}: {value}' for key, value, depth in self.traverse('pre'))
        return f'{type(self).__name__} [\n{nodes}\n]'

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Generator[tuple[K, V], None, None]:
        """
        Check base class.

        > complexity
        - time: `O(n)`
        - space: average: `O(log(n))`, worst: `O(n)`
        - `n`: size of the tree
        """
        return ((key, value) for key, value, _ in self.traverse())

    def _pre(self, node: Optional[Node[K, V]], depth: int = 0) -> Generator[tuple[K, V, int], None, None]:
        if node is None:
            return
        yield node.key, node.value, depth
        yield from self._pre(node.left, depth=depth + 1)
        yield from self._pre(node.right, depth=depth + 1)

    def _in(self, node: Optional[Node[K, V]], depth: int = 0) -> Generator[tuple[K, V, int], None, None]:
        if node is None:
            return
        yield from self._in(node.left, depth=depth + 1)
        yield node.key, node.value, depth
        yield from self._in(node.right, depth=depth + 1)

    def _post(self, node: Optional[Node[K, V]], depth: int = 0) -> Generator[tuple[K, V, int], None, None]:
        if node is None:
            return
        yield from self._post(node.left, depth=depth + 1)
        yield from self._post(node.right, depth=depth + 1)
        yield node.key, node.value, depth

    def _breadth(self, node: Optional[Node[K, V]], depth: int = 0) -> Generator[tuple[K, V, int], None, None]:
        if node is None:
            return
        queue = collections.deque[tuple[Node[K, V], int]]()
        queue.append((node, depth))
        while len(queue) > 0:
            node, depth = queue.popleft()
            yield node.key, node.value, depth
            if node.left is not None:
                queue.append((node.left, depth + 1))
            if node.right is not None:
                queue.append((node.right, depth + 1))

    def traverse(self, mode: Literal['pre', 'in', 'post', 'breadth'] = 'in') -> Generator[tuple[K, V, int], None, None]:
        """
        Return a generator for tree keys, values and depth of nodes in the provided `mode`.

        > complexity
        - time: `O(n)`
        - space: average: `O(log(n))`, worst: `O(n)`
        - `n`: size of the tree

        > parameters
        - `mode`: traversal mode
        - `return`: generator of key, values and depths
        """
        return self._pre(self._root) if mode == 'pre' else \
            self._in(self._root) if mode == 'in' else \
            self._post(self._root) if mode == 'post' else \
            self._breadth(self._root)

    def put(self, key: K, value: V, replacer: Optional[Callable[[V, V], V]] = None) -> Optional[V]:
        """
        See base class.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: `O(1)`
        - `n`: size of the tree
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
            return None
        else:
            node.key = key
            old_value = node.value
            node.value = value if replacer is None else replacer(value, node.value)
            return old_value

    def take(self, key: K) -> V:
        """
        See base class.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: `O(1)`
        - `n`: size of the tree
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

    def get(self, key: K) -> V:
        """
        See base class.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: `O(1)`
        - `n`: size of the tree
        """
        node = self._root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError(f'key ({key}) not found')
        return node.value

    def minimum(self) -> Optional[tuple[K, V]]:
        """
        See base class.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: `O(1)`
        - `n`: size of the tree
        """
        node = self._root
        while node is not None and node.left is not None:
            node = node.left
        return (node.key, node.value) if node is not None else None

    def maximum(self) -> Optional[tuple[K, V]]:
        """
        See base class.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: `O(1)`
        - `n`: size of the tree
        """
        node = self._root
        while node is not None and node.right is not None:
            node = node.right
        return (node.key, node.value) if node is not None else None

    def predecessor(self, key: K) -> Optional[tuple[K, V]]:
        """
        See base class.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: average: `O(log(n))`, worst: `O(n)`
        - `n`: size of the tree
        """
        parents: list[Node[K, V]] = []
        node = self._root
        while node is not None and key != node.key:
            parents.append(node)
            node = node.left if key < node.key else node.right
        if node is not None and node.left is not None:
            predecessor = node.left
            while predecessor.right is not None:
                predecessor = predecessor.right
            return predecessor.key, predecessor.value
        for parent in reversed(parents):
            if parent.key < key:
                return parent.key, parent.value
        return None

    def successor(self, key: K) -> Optional[tuple[K, V]]:
        """
        See base class.

        > complexity
        - time: average: `O(log(n))`, worst: `O(n)`
        - space: average: `O(log(n))`, worst: `O(n)`
        - `n`: size of the tree
        """
        parents: list[Node[K, V]] = []
        node = self._root
        while node is not None and key != node.key:
            parents.append(node)
            node = node.left if key < node.key else node.right
        if node is not None and node.right is not None:
            ancestor = node.right
            while ancestor.left is not None:
                ancestor = ancestor.left
            return ancestor.key, ancestor.value
        for parent in reversed(parents):
            if parent.key > key:
                return parent.key, parent.value
        return None


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
    print('test print functions from abstract base classes')
    print('self:\n', tree)
    print('tree:\n', cast(Any, Tree).__str__(tree))
    print('map:\n', cast(Any, Map).__str__(tree))
    print('priority queue:\n', cast(Any, Priority).__str__(tree))
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
