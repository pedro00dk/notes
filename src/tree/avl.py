from __future__ import annotations

import dataclasses
from typing import Any, Callable, Generic, Optional, cast

from ..map.abc import Map
from ..priority.abc import Priority
from .abc import K, Tree, V
from .bst import BST


@dataclasses.dataclass
class AVLNode(Generic[K, V]):
    """
    Node with extra `height` property.
    """
    key: K
    value: V
    left: Optional[AVLNode[K, V]] = None
    right: Optional[AVLNode[K, V]] = None
    height = 1

    def balance(self) -> int:
        left_height = self.right.height if self.right is not None else 0
        right_height = self.left.height if self.left is not None else 0
        return left_height - right_height


class AVL(Generic[K, V], BST[K, V]):
    """
    AVL tree implementation.

    > complexity
    - space: `O(n)`
    - `n`: number of elements in the structure
    """

    def __init__(self):
        super().__init__()
        self._root: Optional[AVLNode[K, V]] = None

    def put(self, key: K, value: V, replacer: Optional[Callable[[V, V], V]] = None) -> Optional[V]:
        """
        Check base class.

        > complexity
        - time: `O(log(n))`
        - space: `O(log(n))`
        - `n`: size of the tree
        """
        def rec(key: K, value: V, node: Optional[AVLNode[K, V]]) -> tuple[AVLNode[K, V], Optional[V]]:
            if node is None:
                node = AVLNode(key, value)
                self._size += 1
                return node, None
            if key < node.key:
                node.left, old_value = rec(key, value, node.left)
                node.height = max(node.height, node.left.height + 1)
            elif key > node.key:
                node.right, old_value = rec(key, value, node.right)
                node.height = max(node.height, node.right.height + 1)
            else:
                node.key = key
                old_value = node.value
                node.value = value if replacer is None else replacer(value, node.value)
            return self._rotate(node), old_value

        self._root, previous_value = rec(key, value, self._root)
        return previous_value

    def take(self, key: K) -> V:
        """
        Check abstract class for documentation.

        > complexity
        - time: `O(log(n))`
        - space: `O(log(n))`
        """
        def rec(key: K, node: Optional[AVLNode[K, V]]) -> tuple[Optional[AVLNode[K, V]], V]:
            if node is None:
                raise KeyError(f'key ({key}) not found')
            if key < node.key:
                node.left, value = rec(key, node.left)
                node.height = max(
                    node.left.height if node.left is not None else 0,
                    node.right.height if node.right is not None else 0,
                ) + 1
            elif key > node.key:
                node.right, value = rec(key, node.right)
                node.height = max(
                    node.left.height if node.left is not None else 0,
                    node.right.height if node.right is not None else 0,
                ) + 1
            elif node.left is not None and node.right is not None:
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                successor_key = successor.key
                dummy_key = node.left.key
                node.key, successor.key = dummy_key, node.key
                node.value, successor.value = successor.value, node.value
                current_node = node
                node, value = rec(key, node)
                current_node.key = successor_key
            else:
                value = node.value
                node = node.left if node.left is not None else node.right
                self._size -= 1
            return self._rotate(node) if node is not None else None, value

        self._root, value = rec(key, self._root)
        return value

    def _rotate(self, node: AVLNode[K, V]):
        """
        Check if `node` needs rotation.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `node`: node to check and apply rotations
        - `return`: rotated subtree root
        """
        balance = node.balance()
        if balance <= -2:
            left = cast(AVLNode[K, V], node.left)
            if left.balance() > 0:
                node.left = self._rotate_left(left)
            node = self._rotate_right(node)
        elif balance >= 2:
            right = cast(AVLNode[K, V], node.right)
            if right.balance() < 0:
                node.right = self._rotate_right(right)
            node = self._rotate_left(node)
        return node

    def _rotate_left(self, node: AVLNode[K, V]):
        """
        Rotate `node` to the left and recompute balance.

        ```
        # () >> node
        # <> >> subtree
            (a)                     (b*)
           /   \\                  /   \\
          /     \\                /     \\
        <l>     (b)     >>>>    (a*)     <rr>
                / \\            / \\
               /   \\          /   \\
            <rl>   <rr>      <l>   <rl>
        ```

        The resulting balance can be easily recomputed from heights:
        - `H(a*) = max(H(l), H(rl)) + 1`
        - `B(a*) = H(rl) - H(l))`
        - `H(b*) = max(H(a*), H(rr)) + 1`
        - `B(b*) = H(a*) - H(rr))`

        There is a strategy for updating balances in rotations based on previous balances.
        However, it is more complicated to update after `take` operations when the tree shrinks.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `node: Node`: node to check for rotations

        - `return`: rotated subtree root
        """
        child = cast(AVLNode[K, V], node.right)
        node.right = child.left
        child.left = node
        node.height = max(
            node.left.height if node.left is not None else 0,
            node.right.height if node.right is not None else 0,
        ) + 1
        child.height = max(node.height, child.right.height if child.right is not None else 0) + 1
        return child

    def _rotate_right(self, node: AVLNode[K, V]):
        """
        Rotate `node` to the right and recompute balance.
        ```
        # () >> node
        # <> >> subtree
                (a)              (b*)
               /   \\           /   \\
              /     \\         /     \\
            (b)     <r> >>>> <ll>     (a*)
            / \\                      / \\
           /   \\                    /   \\
        <ll>   <lr>               <lr>   <r>    
        ```

        The balance computation is similar to _rotate_left.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `node: Node`: node to check for rotations

        - `return`: rotated subtree root
        """
        child = cast(AVLNode[K, V], node.left)
        node.left = child.right
        child.right = node
        node.height = max(
            node.left.height if node.left is not None else 0,
            node.right.height if node.right is not None else 0,
        ) + 1
        child.height = max(node.height, child.left.height if child.left is not None else 0) + 1
        return child


def test():
    from ..test import match

    tree = AVL[int, Optional[int]]()
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


if __name__ == '__main__':
    test()
