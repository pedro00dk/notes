from abc import ABC, abstractmethod

from ..linked.queue import Queue


class Tree(ABC):
    def __init__(self, name, print_node):
        self.name = name
        self.print_node = print_node
        self.root = None
        self.size = 0

    def __str__(self):
        lines = []
        self.pre_order(lambda node, depth: lines.append(f'{f"|  " * depth}├─ {self.print_node(node, depth)}'))
        tree = '\n'.join(lines)
        return f'{self.name} [\n{tree}\n]'

    def __len__(self):
        return self.size

    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def delete(self, key):
        pass

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
        callback(node, depth)
        self.pre_order(callback, node.left, depth + 1)
        self.pre_order(callback, node.right, depth + 1)

    def in_order(self, callback, node=True, depth=0):
        if node is True:
            return self.in_order(callback, self.root)
        if node is None:
            return
        self.in_order(callback, node.left, depth + 1)
        callback(node, depth)
        self.in_order(callback, node.right, depth + 1)

    def post_order(self, callback, node=True, depth=0):
        if node is True:
            return self.post_order(callback, self.root)
        if node is None:
            return
        self.post_order(callback, node.left, depth + 1)
        self.post_order(callback, node.right, depth + 1)
        callback(node, depth)

    def breadth_order(self, callback):
        q = Queue()
        q.offer((self.root, 0))
        while q.size > 0:
            node, depth = q.poll()
            callback(node, depth)
            if node.left is not None:
                q.offer((node.left, depth + 1))
            if node.right is not None:
                q.offer((node.right, depth + 1))


class Node(ABC):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
