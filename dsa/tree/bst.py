from .abc import Node, Tree


class BST(Tree):
    """
    Binary Search Tree implementation.
    """

    def __init__(self):
        super().__init__(lambda node, depth: f'{node.key}: {node.value}')

    def put(self, key, /, value=None, replacer=None):
        """
        Check abstract class for documentation.

        > complexity:
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
            node.key, node.value = key, replacer(value, node.value) if replacer is not None else value
            return old_value

    def take(self, key):
        """
        Check abstract class for documentation.

        > complexity:
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
    t = BST()
    match([
        (t.put, [0], None),
        (t.put, [-10], None),
        (t.put, [10], None),
        (t.put, [-15, -1000], None),
        (t.put, [-5], None),
        (t.put, [5, 1000], None),
        (t.put, [15], None),
        (t.get, [5], 1000),
        (t.get, [-15], -1000),
        (print, [t], True),
        (t.take, [5], 1000),
        (t.take, [-10], None),
        (t.take, [0], None),
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
