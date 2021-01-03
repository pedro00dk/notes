from typing import Any, Callable, Generic, Optional, cast

from ..map.abc import Map
from ..priority.abc import Priority
from .abc import Tree, V
from .bst import BST, K, Node


class RBTNode(Generic[K, V], Node[K, V]):
    """
    Node with extra `parent` and `red` properties.
    """

    def __init__(self, key: K, value: V):
        super().__init__(key, value)
        self.left: Optional[RBTNode[K, V]] = None
        self.right: Optional[RBTNode[K, V]] = None
        self.parent: Optional[RBTNode[K, V]] = None
        self.red: bool = True


class RBT(Generic[K, V], BST[K, V]):
    """
    Red-Black tree implementation.
    """

    def __init__(self):
        super().__init__()
        self._root: Optional[RBTNode[K, V]] = None

    def put(self, key: K, value: V, replacer: Optional[Callable[[V, V], V]] = None) -> Optional[V]:
        """
        Check base class.

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`
        """
        parent = None
        node = self._root
        while node is not None and key != node.key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            if parent is None:
                node = self._root = RBTNode(key, value)
            elif key < parent.key:
                node = parent.left = RBTNode(key, value)
                node.parent = parent
            else:
                node = parent.right = RBTNode(key, value)
                node.parent = parent
            self._size += 1
            self._root = self._put_fix(node)
        else:
            old_value = node.value
            node.key = key
            node.value = value if replacer is None else replacer(value, node.value)
            return old_value

    def _put_fix(self, created: RBTNode[K, V]):
        """
        Fix red black properties of the tree.
        `created` node color must be red.

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters
        - `created`: the created node
        - `return`: tree root node
        """
        node = created
        while self._red(parent := cast(RBTNode[K, V], self._parent(node))):
            uncle = cast(RBTNode[K, V], self._uncle(node))
            grand_parent = cast(RBTNode[K, V], self._grand_parent(node))
            if self._red(uncle):
                parent.red = uncle.red = False
                grand_parent.red = True
                node = grand_parent
                continue
            if node == parent.right and parent == grand_parent.left:
                self._rotate_left(parent)
                node, parent = parent, node
            elif node == parent.left and parent == grand_parent.right:
                self._rotate_right(parent)
                node, parent = parent, node
            if node == parent.right:
                self._rotate_left(grand_parent)
            elif node == parent.left:
                self._rotate_right(grand_parent)
            grand_parent.red = True
            parent.red = False
            node = parent
            break
        root = self._top(node)
        root.red = False
        return root

    def take(self, key: K) -> V:
        """
        Check abstract class for documentation.

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`
        """
        node = self._root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError(f'key ({key}) not found')
        if node.left is not None and node.right is not None:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key = successor.key
            node.value, successor.value = successor.value, node.value
            node = successor
        child: Optional[RBTNode[K, V]] = None
        if node.parent is None:
            child = self._root = node.left if node.left is not None else node.right
            if child is not None:
                child.parent = None
        elif node.parent.left == node:
            child = node.parent.left = node.left if node.left is not None else node.right
            if child is not None:
                child.parent = node.parent
        elif node.parent.right == node:
            child = node.parent.right = node.left if node.left is not None else node.right
            if child is not None:
                child.parent = node.parent
        self._size -= 1
        self._root = self._take_fix(node, child)
        return node.value

    def _take_fix(self, deleted: RBTNode[K, V], replacement: Optional[RBTNode[K, V]]):
        """
        Fix red black properties of the tree.
        The fix only works if the `deleted` node had 0 or 1 non null child.

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters
        - `deleted`: the deleted node
        - `replacement`: the only non None child of deleted node (or null if `deleted` had no non null child)

        - `return`: tree root node
        """

        if self._red(deleted):
            return self._root
        if self._red(replacement):
            cast(RBTNode[K, V], replacement).red = False
            return self._root
        node = replacement
        while (parent := self._parent(node)) is not None:
            node = cast(RBTNode[K, V], node)
            sibling = cast(RBTNode[K, V], self._sibling(node))
            if self._red(sibling):
                sibling.red = False
                parent.red = True
                if node == parent.left:
                    self._rotate_left(parent)
                else:
                    self._rotate_right(parent)
                sibling = self._sibling(node)
            if self._blk(node.parent) and sibling is not None and self._blk(sibling) and \
                    self._blk(sibling.left) and self._blk(sibling.right):
                sibling.red = True
                node = parent
                continue
            if self._red(node.parent) and sibling is not None and self._blk(sibling) and \
                    self._blk(sibling.left) and self._blk(sibling.right):
                sibling.red = True
                parent.red = False
                break
            if self._blk(parent) and sibling is not None and self._blk(sibling):
                if node == parent.left and self._red(sibling.left) and self._blk(sibling.right):
                    self._rotate_right(sibling)
                    sibling.red = True
                    cast(RBTNode[K, V], sibling.parent).red = False
                elif node == parent.right and self._blk(sibling.left) and self._red(sibling.right):
                    self._rotate_left(sibling)
                    sibling.red = True
                    cast(RBTNode[K, V], sibling.parent).red = False
                sibling = self._sibling(node)
            if sibling is not None and self._blk(sibling):
                if node == parent.left and self._red(sibling.right):
                    self._rotate_left(parent)
                    sibling.red = parent.red
                    parent.red = cast(RBTNode[K, V], sibling.right).red = False
                elif node == parent.right and self._red(sibling.left):
                    self._rotate_right(parent)
                    sibling.red = parent.red
                    parent.red = cast(RBTNode[K, V], sibling.left).red = False
            break
        return self._top(node if node is not None else deleted)

    def _top(self, node: RBTNode[K, V]) -> RBTNode[K, V]:
        while node.parent is not None:
            node = node.parent
        return node

    def _red(self, node: Optional[RBTNode[K, V]]) -> bool:
        return node is not None and node.red

    def _blk(self, node: Optional[RBTNode[K, V]]) -> bool:
        return node is None or not node.red

    def _parent(self, node: Optional[RBTNode[K, V]]) -> Optional[RBTNode[K, V]]:
        return node.parent if node is not None else None

    def _sibling(self, node: Optional[RBTNode[K, V]]) -> Optional[RBTNode[K, V]]:
        parent = self._parent(node)
        return None if node is None or parent is None else parent.left if node == parent.right else parent.right

    def _grand_parent(self, node: Optional[RBTNode[K, V]]) -> Optional[RBTNode[K, V]]:
        return self._parent(self._parent(node))

    def _uncle(self, node: Optional[RBTNode[K, V]]) -> Optional[RBTNode[K, V]]:
        return self._sibling(self._parent(node))

    def _rotate_left(self, node: RBTNode[K, V]) -> RBTNode[K, V]:
        """
        Red-Black left rotation.

        > parameters
        - `node`: the node to rotate
        - `return`: the new root of the rotated subtree
        """
        child = cast(RBTNode[K, V], node.right)
        node.right = child.left
        if node.right is not None:
            node.right.parent = node
        child.left = node
        child.parent = node.parent
        node.parent = child
        if child.parent is not None:
            if child.parent.left == node:
                child.parent.left = child
            else:
                child.parent.right = child
        return child

    def _rotate_right(self, node: RBTNode[K, V]) -> RBTNode[K, V]:
        """
        Red-Black right rotation.

        > parameters
        - `node`: the node to rotate
        - `return`: the new root of the rotated subtree
        """
        child = cast(RBTNode[K, V], node.left)
        node.left = child.right
        if node.left is not None:
            node.left.parent = node
        child.right = node
        child.parent = node.parent
        node.parent = child
        if child.parent is not None:
            if child.parent.left == node:
                child.parent.left = child
            else:
                child.parent.right = child
        return child


def test():
    from ..test import match

    tree = RBT[int, Optional[int]]()
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
