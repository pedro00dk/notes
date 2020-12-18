from typing import Callable, Generic, Optional, cast

from .abc import Node, T, Tree, U


class AVLNode(Generic[T, U], Node[T, U]):
    """
    Node with extra `height` property.
    """

    def __init__(self, key: T, value: U):
        super().__init__(key, value)
        self.left: Optional[AVLNode[T, U]] = None
        self.right: Optional[AVLNode[T, U]] = None
        self.height: int = 1

    def balance(self) -> int:
        left_height = self.right.height if self.right is not None else 0
        right_height = self.left.height if self.left is not None else 0
        return left_height - right_height


class AVL(Generic[T, U], Tree[T, U]):
    """
    AVL tree implementation (with ranks).
    """

    def __init__(self, rank: int = 2):
        """
        > parameters
        - `rank`: tree rank, if < 2, the value is clamped
        """
        super().__init__()
        self._root: Optional[AVLNode[T, U]] = None
        printer: Callable[[AVLNode[T, U], int], str] = \
            lambda node, depth: f'b:{node.balance()} # {node.key}: {node.value}'
        self._printer = printer
        self._rank = max(rank, 2)

    def put(self, key: T, value: U, replacer: Optional[Callable[[U, U], U]] = None) -> Optional[U]:
        """
        Check abstract class for documentation.

        > complexity
        - time: `O(log(n))`
        - space: `O(log(n))`
        """
        def rec(key: T, value: U, node: Optional[AVLNode[T, U]]) -> tuple[AVLNode[T, U], Optional[U]]:
            if node is None:
                node = AVLNode(key, value)
                self._size += 1
                return node, None
            if key < node.key:
                node.left, previous_value = rec(key, value, node.left)
                node.height = max(node.height, node.left.height + 1)
            elif key > node.key:
                node.right, previous_value = rec(key, value, node.right)
                node.height = max(node.height, node.right.height + 1)
            else:
                previous_value = node.value
                node.key = key
                node.value = replacer(value, node.value) if replacer is not None else value
            return self._rotate(node), previous_value

        self._root, previous_value = rec(key, value, self._root)
        return previous_value

    def take(self, key: T) -> U:
        """
        Check abstract class for documentation.

        > complexity
        - time: `O(log(n))`
        - space: `O(log(n))`
        """
        def rec(key: T, node: Optional[AVLNode[T, U]]) -> tuple[Optional[AVLNode[T, U]], U]:
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

    def _rotate(self, node: AVLNode[T, U]):
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
        if balance <= -self._rank:
            left = cast(AVLNode[T, U], node.left)
            if left.balance() > 0:
                node.left = self._rotate_left(left)
            node = self._rotate_right(node)
        elif balance >= self._rank:
            right = cast(AVLNode[T, U], node.right)
            if right.balance() < 0:
                node.right = self._rotate_right(right)
            node = self._rotate_left(node)
        return node

    def _rotate_left(self, node: AVLNode[T, U]):
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
        child = cast(AVLNode[T, U], node.right)
        node.right = child.left
        child.left = node
        node.height = max(
            node.left.height if node.left is not None else 0,
            node.right.height if node.right is not None else 0,
        ) + 1
        child.height = max(node.height, child.right.height if child.right is not None else 0) + 1
        return child

    def _rotate_right(self, node: AVLNode[T, U]):
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
        child = cast(AVLNode[T, U], node.left)
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

    for i in (2, 3, 4):
        print(f'rank {i} tree')
        tree = AVL[int, Optional[int]](i)
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
