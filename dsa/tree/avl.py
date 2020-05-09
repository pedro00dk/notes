from .abc import Node, Tree


class AVL(Tree):
    def __init__(self):
        super().__init__(lambda node, depth: f'b:{node.balance} # {node.key}: {node.value}')

    def put(self, key, value=None):
        self._root, growth, old_value = self._put(key, value, self._root)
        return old_value

    def _put(self, key, value, node):
        if node is None:
            node, growth, old_value = AVLNode(key, value), 1, None
            self._size += 1
        elif key < node.key:
            node.left, child_growth, old_value = self._put(key, value, node.left)
            previous_balance = node.balance
            node.balance -= child_growth
            growth = max(0, abs(node.balance) - abs(previous_balance))
        elif key > node.key:
            node.right, child_growth, old_value = self._put(key, value, node.right)
            previous_balance = node.balance
            node.balance += child_growth
            growth = max(0, abs(node.balance) - abs(previous_balance))
        else:
            node.key, node.value, growth, old_value = key, value, 0, node.value
        return (*self._rotate(node, growth), old_value)

    def take(self, key):
        self._root, growth, value = self._take(key, self._root)
        return value

    def _take(self, key, node):
        if node is None:
            raise KeyError('not found')
        elif key < node.key:
            node.left, child_growth, value = self._take(key, node.left)
            previous_balance = node.balance
            node.balance -= child_growth
            growth = -min(0, abs(node.balance) - abs(previous_balance))
        elif key > node.key:
            node.right, child_growth, value = self._take(key, node.right)
            previous_balance = node.balance
            node.balance += child_growth
            growth = -min(0, abs(node.balance) - abs(previous_balance))
        elif node.left is not None and node.right is not None:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            successor_key, dummy_key = successor.key, node.left.key
            node.key, successor.key = dummy_key, node.key
            node.value, successor.value = successor.value, node.value
            current_node = node
            node, growth, value = self._take(key, node)
            current_node.key = successor_key
        else:
            node, growth, value = node.left if node.right is None else node.right, -1, node.value
            self._size -= 1
        return (*self._rotate(node, growth), value)

    def _rotate(self, node, growth, rank=2):
        if node is not None and node.balance <= -rank:
            if node.left.balance > 0:
                node, rotation_growth = self._rotate_left(node.left)
                growth += rotation_growth
            node, rotation_growth = self._rotate_right(node)
            growth += rotation_growth
        elif node is not None and node.balance >= rank:
            if node.right.balance < 0:
                node, rotation_growth = self._rotate_right(node.right)
                growth += rotation_growth
            node, rotation_growth = self._rotate_left(node)
            growth += rotation_growth
        return node, growth

    def _rotate_left(self, node):
        child = node.right
        node.right = child.left
        child.left = node
        growth = -1 if node.balance >= 2 else 0 if node.balance == 1 else 1
        node.balance = node.balance - 1 - max(child.balance, 0)
        child.balance = child.balance - 1 + min(node.balance, 0)
        return child, growth

    def _rotate_right(self, node):
        child = node.left
        node.left = child.right
        child.right = node
        growth = -1 if node.balance <= -2 else 0 if node.balance == -1 else 1
        node.balance = node.balance + 1 - min(child.balance, 0)
        child.balance = child.balance + 1 + max(node.balance, 0)
        return child, growth


class AVLNode(Node):
    def __init__(self, key, value=None):
        super().__init__(key, value)
        self.balance = 0


def test():
    from ..util import match
    t = AVL()
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
        (print, [t], None),
        (t.take, [0], None),
        (t.take, [-10], None),
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
