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

    def insert(self, key, value=None, node=True):
        if node == True:
            self.root = self.insert(key, value, self.root)
            self.size += 1
        elif not node: return Node(key, value)
        elif node.key > key: node.left = self.insert(key, value, node.left)
        elif node.key < key: node.right = self.insert(key, value, node.right)
        return node

    def remove(self, key, node=True):
        if node == True:
            self.root = self.remove(key, self.root)
            self.size -= 1
        elif not node: raise KeyError()
        elif node.key > key: node.left = self.remove(key, node.left)
        elif node.key < key: node.right = self.remove(key, node.right)
        elif not node.left: node = node.right
        elif not node.right: node = node.left
        else:
            def node_successor(node):
                if not node: return None
                node = node.right
                while node and node.left: node = node.left
                return node
            successor = node_successor(node)
            node.key, node.value, successor.key = successor.key, successor.value, node.key
            node.right = self.remove(key, node.right)
        return node

    def get(self, key):
        node = self.root
        while node and node.key != key: node = node.left if node.key > key else node.right
        if not node: raise KeyError()
        return node.value

    def pre_order(self, callback, node=True, depth=0):
        if node == True: return self.pre_order(callback, self.root)
        if not node: return
        callback(node.key, node.value, depth)
        self.pre_order(callback, node.left, depth + 1)
        self.pre_order(callback, node.right, depth + 1)

    def in_order(self, callback, node=True, depth=0):
        if node == True: return self.in_order(callback, self.root)
        if not node: return
        self.in_order(callback, node.left, depth + 1)
        callback(node.key, node.value, depth)
        self.in_order(callback, node.right, depth + 1)

    def post_order(self, callback, node=True, depth=0):
        if node == True: return self.post_order(callback, self.root)
        if not node: return
        self.post_order(callback, node.left, depth + 1)
        self.post_order(callback, node.right, depth + 1)
        callback(node.key, node.value, depth)

    def breadth_order(self, callback):
        q = Queue()
        q.offer((self.root, 0))
        while q.size:
            node, depth = q.pool()
            callback(node.key, node.value, depth)
            if node.left: q.offer((node.left, depth + 1))
            if node.right: q.offer((node.right, depth + 1))


class Node:
    def __init__(self, key, value=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right


def test():
    t = BST()
    t.insert(0)
    t.insert(-10)
    t.insert(10)
    t.insert(-15, -1000)
    t.insert(-5)
    t.insert(5, 1000)
    t.insert(15)
    print(t.get(5))
    print(t.get(-15))
    print(t)
    t.remove(5)
    t.remove(-10)
    print(t)
    t.pre_order(lambda key, value, depth: print(key, end=' '))
    print()
    t.in_order(lambda key, value, depth: print(key, end=' '))
    print()
    t.post_order(lambda key, value, depth: print(key, end=' '))
    print()
    t.breadth_order(lambda key, value, depth: print(key, end=' '))
    print()


if __name__ == '__main__': test()
