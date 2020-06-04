from .abc import Node, Tree


class RBTNode(Node):
    """
    Node with extra `parent` and `red` properties.
    """

    def __init__(self, key, /, value=None):
        super().__init__(key, value)
        self.parent = None
        self.red = True


class RBT(Tree):
    """
    Red-Black tree implementation.
    """

    def __init__(self):
        super().__init__(lambda node, depth: f'{"R" if node.red else "B"} # {node.key}: {node.value}')

    def put(self, key, /, value=None):
        """
        Check abstract class for documentation.

        > complexity:
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
                parent.left.parent = parent
            else:
                node = parent.right = RBTNode(key, value)
                parent.right.parent = parent
            self._size += 1
            self._root = self._put_fix(node)
        else:
            node.key, node.value, old_value = key, value, node.value
            return old_value

    def _put_fix(self, created: RBTNode):
        node = created
        while self._red(parent := self._parent(node)):
            uncle = self._uncle(node)
            grand_parent = self._grand_parent(node)
            if self._red(uncle):
                parent.red = uncle.red = False
                grand_parent.red = True
                node = grand_parent
                continue
            if node == parent.right:
                if parent == grand_parent.left:
                    parent = self._rotate_left(parent)
                    node = parent.left
                grand_parent = self._rotate_left(grand_parent)
            elif node == parent.left:
                if parent == grand_parent.right:
                    parent = self._rotate_right(parent)
                    node = parent.right
                grand_parent = self._rotate_right(grand_parent)
            grand_parent.red = False
            grand_parent.left.red = grand_parent.right.red = True
            break
        root = self._top(node)
        root.red = False
        return root

    def take(self, key):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(log(n))`
        - space: `O(1)`
        """
        node = self._root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError('not found')
        if node.left is not None and node.right is not None:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key, successor.key = successor.key, node.key
            node.value, successor.value = successor.value, node.value
            node = successor
        if node.parent is None:
            child = self._root = None
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

    def _take_fix(self, deleted: RBTNode, replacer: RBTNode):
        if self._red(deleted):
            return self._root
        if self._red(replacer):
            replacer.red = False
            return self._root
        node = replacer
        while (parent := self._parent(node)) is not None:
            sibling = self._sibling(node)
            if self._red(sibling):
                sibling.red = False
                parent.red = True
                if node == node.parent.left:
                    self._rotate_left(parent)
                    sibling = parent.right
                else:
                    self._rotate_right(parent)
                    sibling = parent.left
            if self._blk(parent) and self._blk(sibling) and sibling is not None and \
                    self._blk(sibling.left) and self._blk(sibling.right):
                sibling.red = True
                node = parent
                continue
            if self._red(parent) and self._blk(sibling) and sibling is not None and \
                    self._blk(sibling.left) and self._blk(sibling.right):
                sibling.red = True
                parent.red = False
                break
            if self._blk(sibling) and sibling is not None:
                if node == parent.left and self._red(sibling.left) and self._blk(sibling.right):
                    sibling.red = True
                    sibling.left.red = False
                    sibling = self._rotate_right(sibling)
                elif node == parent.right and self._blk(sibling.left) and self._left(sibling.right):
                    sibling.red = True
                    sibling.right.red = False
                    sibling = self._rotate_left(sibling)
            sibling.red = parent.red
            parent.red = False
            if node == parent.left:
                sibling.right.red = False
                self._rotate_left(parent)
            else:
                sibling.left.red = False
                self._rotate_right(parent)
            break
        return self._top(node if node is not None else deleted)

    def _red(self, node: RBTNode):
        return node is not None and node.red

    def _blk(self, node: RBTNode):
        return node is None or not node.red

    def _left(self, node: RBTNode):
        return node.left if node is not None else None

    def _right(self, node: RBTNode):
        return node.right if node is not None else None

    def _parent(self, node: RBTNode):
        return node.parent if node is not None else None

    def _grand_parent(self, node: RBTNode):
        return self._parent(self._parent(node))

    def _sibling(self, node: RBTNode):
        parent = self._parent(node)
        return None if node is None or parent is None else parent.left if node == parent.right else parent.right

    def _uncle(self, node: RBTNode):
        return self._sibling(self._parent(node))

    def _top(self, node: RBTNode):
        while (parent := self._parent(node)) is not None:
            node = parent
        return node

    def _rotate_left(self, node: RBTNode):
        """
        Red-Black left rotation.

        > paremeters:
        - `node: RBTNode`: the node to rotate

        > `return: RBTNode`: the new root of the rotated subtree
        """
        child = node.right
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

    def _rotate_right(self, node: RBTNode):
        """
        Red-Black right rotation.

        > paremeters:
        - `node: RBTNode`: the node to rotate

        > `return: RBTNode`: the new root of the rotated subtree
        """
        child = node.left
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
    t = RBT()
    match([
        (t.put, [-15, -1000], None),
        (t.put, [-10], None),
        (t.put, [-5], None),
        (t.put, [0], None),
        (t.put, [5, 1000], None),
        (t.put, [10], None),
        (t.put, [15], None),
        (t.get, [5], 1000),
        (t.get, [-15], -1000),
        (print, [t], True),
        (t.take, [0], None),
        (print, [t], True),
        (t.take, [-10], None),
        (print, [t], True),
        (t.take, [-15], -1000),
        (print, [t], None)
    ])
    for key, value, depth in t.traverse('pre'):
        print(key, end=' ')
    print()
    for key, value, depth in t.traverse('in'):
        print(key, end=' ')
    print()
    for key, value, depth in t.traverse('post'):
        print(key, end=' ')
    print()
    for key, value, depth in t.traverse('breadth'):
        print(key, end=' ')
    print()


if __name__ == '__main__':
    test()
