from queue import Queue


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def __str__(self):
        lines = []
        self.pre_order(lambda key, value, depth: lines.append(f'{f"|  " * depth}├─ {key}: {value}'))
        tree = '\n'.join(lines)
        return f'BST [\n{tree}\n]'

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
            node.key, node.value = key, value

    def delete(self, key):
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
        if node is None:
            return
        callback(node.key, node.value, depth)
        self.pre_order(callback, node.left, depth + 1)
        self.pre_order(callback, node.right, depth + 1)

    def in_order(self, callback, node=True, depth=0):
        if node is True:
            return self.in_order(callback, self.root)
        if node is None:
            return
        self.in_order(callback, node.left, depth + 1)
        callback(node.key, node.value, depth)
        self.in_order(callback, node.right, depth + 1)

    def post_order(self, callback, node=True, depth=0):
        if node is True:
            return self.post_order(callback, self.root)
        if node is None:
            return
        self.post_order(callback, node.left, depth + 1)
        self.post_order(callback, node.right, depth + 1)
        callback(node.key, node.value, depth)

    def breadth_order(self, callback):
        q = Queue()
        q.offer((self.root, 0))
        while q.size > 0:
            node, depth = q.pool()
            callback(node.key, node.value, depth)
            if node.left is not None:
                q.offer((node.left, depth + 1))
            if node.right is not None:
                q.offer((node.right, depth + 1))


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


def test():
    t = BST()
    t.put(0)
    t.put(-10)
    t.put(10)
    t.put(-15, -1000)
    t.put(-5)
    t.put(5, 1000)
    t.put(15)
    print(t.get(5))
    print(t.get(-15))
    print(t)
    t.delete(5)
    t.delete(-10)
    t.delete(0)
    print(t)
    t.pre_order(lambda key, value, depth: print(key, end=' '))
    print()
    t.in_order(lambda key, value, depth: print(key, end=' '))
    print()
    t.post_order(lambda key, value, depth: print(key, end=' '))
    print()
    t.breadth_order(lambda key, value, depth: print(key, end=' '))
    print()


if __name__ == '__main__':
    test()
