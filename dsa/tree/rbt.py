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

    def put(self, key, /, value=None, replacer=None):
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
            old_value = node.value
            node.key, node.value = key, replacer(value, node.value) if replacer is not None else value
            return old_value

    def _put_fix(self, created: RBTNode):
        """
        Fix red black properties of the tree.
        `created` node color must be red.

        > complexity:
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters:
        - `created: RBTNode`: the created node

        > `return: RBTNode`: tree root node
        """
        node = created
        while self._red(parent := self._parent(node)):
            uncle = self._uncle(node)
            grand_parent = self._grand_parent(node)
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
            raise KeyError(f'key ({key}) not found')
        if node.left is not None and node.right is not None:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key, node.value, successor.value = successor.key, successor.value, node.value
            node = successor
        if node.parent is None:
            child = self._root = node.left if node.left is not None else node.right
            if child is not None:
                self._root.parent = None
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

    def _take_fix(self, deleted: RBTNode, replacement: RBTNode):
        """
        Fix red black properties of the tree.
        The fix only works if the `deleted` node had 0 or 1 non null child.

        > complexity:
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters:
        - `deleted: RBTNode`: the deleted node
        - `replacement: RBTNode`: the only non null child of deleted node (or null if `deleted` had no non null child)

        > `return: RBTNode`: tree root node
        """

        if self._red(deleted):
            return self._root
        if self._red(replacement):
            replacement.red = False
            return self._root
        node = replacement
        while (parent := self._parent(node)) is not None:
            sibling = self._sibling(node)
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
                    sibling.parent.red = False
                elif node == parent.right and self._blk(sibling.left) and self._red(sibling.right):
                    self._rotate_left(sibling)
                    sibling.red = True
                    sibling.parent.red = False
                sibling = self._sibling(node)
            if sibling is not None and self._blk(sibling):
                if node == parent.left and self._red(sibling.right):
                    self._rotate_left(parent)
                    sibling.red = parent.red
                    parent.red = sibling.right.red = False
                elif node == parent.right and self._red(sibling.left):
                    self._rotate_right(parent)
                    sibling.red = parent.red
                    parent.red = sibling.left.red = False
            break
        return self._top(node if node is not None else deleted)

    def _top(self, node: RBTNode):
        while node.parent is not None:
            node = node.parent
        return node

    def _red(self, node: RBTNode):
        return node is not None and node.red

    def _blk(self, node: RBTNode):
        return node is None or not node.red

    def _parent(self, node: RBTNode):
        return node.parent if node is not None else None

    def _sibling(self, node: RBTNode):
        parent = self._parent(node)
        return None if node is None or parent is None else parent.left if node == parent.right else parent.right

    def _grand_parent(self, node: RBTNode):
        return self._parent(self._parent(node))

    def _uncle(self, node: RBTNode):
        return self._sibling(self._parent(node))

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
