from .abc import Node, Tree


class BST(Tree):
    def __init__(self):
        super().__init__(lambda node, depth: f'{node.key}: {node.value}')

    def put(self, key, value=None):
        parent = None
        node = self.root
        while node is not None and key != node.key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            if parent is None:
                self.root = Node(key, value)
            elif key < parent.key:
                parent.left = Node(key, value)
            else:
                parent.right = Node(key, value)
            self.size += 1
        else:
            node.key, node.value, old_value = key, value, node.value
            return old_value

    def take(self, key):
        parent = None
        node = self.root
        while node is not None and key != node.key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError('not found')
        if node.left is not None and node.right is not None:
            parent = node
            successor = node.right
            while successor.left is not None:
                parent = successor
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node = successor
        if parent is None:
            self.root = None
        elif parent.left == node:
            parent.left = node.left if node.left is not None else node.right
        elif parent.right == node:
            parent.right = node.left if node.left is not None else node.right
        self.size -= 1
        return node.value


def test():
    from ..util import match
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
    for node, depth in t.traverse('pre'):
        print(node.key, end=' ')
    print()
    for node, depth in t.traverse('in'):
        print(node.key, end=' ')
    print()
    for node, depth in t.traverse('post'):
        print(node.key, end=' ')
    print()
    for node, depth in t.traverse('breadth'):
        print(node.key, end=' ')
    print()


if __name__ == '__main__':
    test()
