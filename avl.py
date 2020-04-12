from queue import Queue


class AVL:
    def __init__(self):
        self.root = None
        self.size = 0

    def __str__(self):
        lines = []
        self.pre_order(
            lambda key, value, depth, balance: lines.append(f'{f"|  " * depth}├─ b:{balance} # {key}: {value}')
        )
        tree = '\n'.join(lines)
        return f'AVL [\n{tree}\n]'

    def put(self, key, value=None, node=True):
        if node is True:
            self.root, growth = self.put(key, value, self.root)
            return
        if node is None:
            node, growth = Node(key, value), 1
            self.size += 1
        elif key < node.key:
            node.left, child_growth = self.put(key, value, node.left)
            previous_balance = node.balance
            node.balance -= child_growth
            growth = max(0, abs(node.balance) - abs(previous_balance))
        elif key > node.key:
            node.right, child_growth = self.put(key, value, node.right)
            previous_balance = node.balance
            node.balance += child_growth
            growth = max(0, abs(node.balance) - abs(previous_balance))
        else:
            node.value, growth = value, 0
        return self._rotate(node, growth)

    def delete(self, key, node=True):
        if node is True:
            self.root, growth = self.delete(key, self.root)
            return
        if node is None:
            raise KeyError('not found')
        elif key < node.key:
            node.left, child_growth = self.delete(key, node.left)
            previous_balance = node.balance
            node.balance -= child_growth
            growth = -min(0, abs(node.balance) - abs(previous_balance))
        elif key > node.key:
            node.right, child_growth = self.delete(key, node.right)
            previous_balance = node.balance
            node.balance += child_growth
            growth = -min(0, abs(node.balance) - abs(previous_balance))
        elif node.left is not None and node.right is not None:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            successor_key, dummy_key = successor.key, node.left.key
            node.key, node.value, successor.key = dummy_key, successor.value, node.key
            current_node = node
            node, growth = self.delete(key, node)
            current_node.key = successor_key
        else:
            node, growth = node.left if node.right is None else node.right, -1
            self.size -= 1
        return self._rotate(node, growth)

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

    def get(self, key):
        node = self.root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError()
        return node.value

    def pre_order(self, callback, node=True, depth=0):
        if node is True:
            return self.pre_order(callback, self.root)
        #
        if node is None:
            return
        callback(node.key, node.value, depth, node.balance)
        self.pre_order(callback, node.left, depth + 1)
        self.pre_order(callback, node.right, depth + 1)

    def in_order(self, callback, node=True, depth=0):
        if node is True:
            return self.in_order(callback, self.root)
        #
        if node is None:
            return
        self.in_order(callback, node.left, depth + 1)
        callback(node.key, node.value, depth, node.balance)
        self.in_order(callback, node.right, depth + 1)

    def post_order(self, callback, node=True, depth=0):
        if node is True:
            return self.post_order(callback, self.root)
        #
        if node is None:
            return
        self.post_order(callback, node.left, depth + 1)
        self.post_order(callback, node.right, depth + 1)
        callback(node.key, node.value, depth, node.balance)

    def breadth_order(self, callback):
        q = Queue()
        q.offer((self.root, 0))
        while q.size > 0:
            node, depth = q.pool()
            callback(node.key, node.value, depth, node.balance)
            if node.left is not None:
                q.offer((node.left, depth + 1))
            if node.right is not None:
                q.offer((node.right, depth + 1))


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.balance = 0
        self.left = None
        self.right = None


def test():
    t = AVL()
    t.put(-15, -1000)
    t.put(-10)
    t.put(-5)
    t.put(0)
    t.put(5, 1000)
    t.put(10)
    t.put(15)
    print(t.get(5))
    print(t.get(-15))
    print(t)
    t.delete(0)
    t.delete(-10)
    t.delete(15)
    print(t)
    t.pre_order(lambda key, value, depth, balance: print(key, end=' '))
    print()
    t.in_order(lambda key, value, depth, balance: print(key, end=' '))
    print()
    t.post_order(lambda key, value, depth, balance: print(key, end=' '))
    print()
    t.breadth_order(lambda key, value, depth, balance: print(key, end=' '))
    print()


if __name__ == '__main__':
    test()
