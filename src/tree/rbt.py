from typing import Callable, Generic, Optional, cast

from .abc import Node, T, Tree, U


class RBTNode(Generic[T, U], Node[T, U]):
    """
    Node with extra `parent` and `red` properties.
    """

    def __init__(self, key: T, value: U):
        super().__init__(key, value)
        self.left: Optional[RBTNode[T, U]] = None
        self.right: Optional[RBTNode[T, U]] = None
        self.parent: Optional[RBTNode[T, U]] = None
        self.red: bool = True


class RBT(Generic[T, U], Tree[T, U]):
    """
    Red-Black tree implementation.
    """

    def __init__(self):
        super().__init__()
        self._root: Optional[RBTNode[T, U]] = None
        printer: Callable[[RBTNode[T, U], int], str] = \
            lambda node, depth: f'{"R" if node.red else "B"} # {node.key}: {node.value}'
        self._printer = printer

    def put(self, key: T, value: U, replacer: Optional[Callable[[U, U], U]] = None) -> Optional[U]:
        """
        Check abstract class for documentation.

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
            node.value = replacer(value, node.value) if replacer is not None else value
            return old_value

    def _put_fix(self, created: RBTNode[T, U]):
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
        while self._red(parent := cast(RBTNode[T, U], self._parent(node))):
            uncle = cast(RBTNode[T, U], self._uncle(node))
            grand_parent = cast(RBTNode[T, U], self._grand_parent(node))
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

    def take(self, key: T) -> U:
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
        child: Optional[RBTNode[T, U]] = None
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

    def _take_fix(self, deleted: RBTNode[T, U], replacement: Optional[RBTNode[T, U]]):
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
            cast(RBTNode[T, U], replacement).red = False
            return self._root
        node = replacement
        while (parent := self._parent(node)) is not None:
            node = cast(RBTNode[T, U], node)
            sibling = cast(RBTNode[T, U], self._sibling(node))
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
                    cast(RBTNode[T, U], sibling.parent).red = False
                elif node == parent.right and self._blk(sibling.left) and self._red(sibling.right):
                    self._rotate_left(sibling)
                    sibling.red = True
                    cast(RBTNode[T, U], sibling.parent).red = False
                sibling = self._sibling(node)
            if sibling is not None and self._blk(sibling):
                if node == parent.left and self._red(sibling.right):
                    self._rotate_left(parent)
                    sibling.red = parent.red
                    parent.red = cast(RBTNode[T, U], sibling.right).red = False
                elif node == parent.right and self._red(sibling.left):
                    self._rotate_right(parent)
                    sibling.red = parent.red
                    parent.red = cast(RBTNode[T, U], sibling.left).red = False
            break
        return self._top(node if node is not None else deleted)

    def _top(self, node: RBTNode[T, U]) -> RBTNode[T, U]:
        while node.parent is not None:
            node = node.parent
        return node

    def _red(self, node: Optional[RBTNode[T, U]]) -> bool:
        return node is not None and node.red

    def _blk(self, node: Optional[RBTNode[T, U]]) -> bool:
        return node is None or not node.red

    def _parent(self, node: Optional[RBTNode[T, U]]) -> Optional[RBTNode[T, U]]:
        return node.parent if node is not None else None

    def _sibling(self, node: Optional[RBTNode[T, U]]) -> Optional[RBTNode[T, U]]:
        parent = self._parent(node)
        return None if node is None or parent is None else parent.left if node == parent.right else parent.right

    def _grand_parent(self, node: Optional[RBTNode[T, U]]) -> Optional[RBTNode[T, U]]:
        return self._parent(self._parent(node))

    def _uncle(self, node: Optional[RBTNode[T, U]]) -> Optional[RBTNode[T, U]]:
        return self._sibling(self._parent(node))

    def _rotate_left(self, node: RBTNode[T, U]) -> RBTNode[T, U]:
        """
        Red-Black left rotation.

        > parameters
        - `node`: the node to rotate
        - `return`: the new root of the rotated subtree
        """
        child = cast(RBTNode[T, U], node.right)
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

    def _rotate_right(self, node: RBTNode[T, U]) -> RBTNode[T, U]:
        """
        Red-Black right rotation.

        > parameters
        - `node`: the node to rotate
        - `return`: the new root of the rotated subtree
        """
        child = cast(RBTNode[T, U], node.left)
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
