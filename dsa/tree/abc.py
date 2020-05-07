from abc import ABC, abstractmethod

from ..linked.queue import Queue


class Tree(ABC):
    def __init__(self, printer):
        self.printer = printer
        self.root = None
        self.size = 0

    def __iter__(self):
        return self.traverse()

    def __str__(self):
        tree = '\n'.join(f'{"|  " * depth}├─ {self.printer(node, depth)}' for node, depth in self.traverse('pre'))
        return f'{type(self).__name__} [\n{tree}\n]'

    def __len__(self):
        return self.size

    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def take(self, key):
        pass

    def get(self, key):
        node = self.root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError('not found')
        return node.value

    def traverse(self, mode='in'):
        return self._pre_order(self.root) if mode == 'pre' else \
            self._in_order(self.root) if mode == 'in' else \
            self._post_order(self.root) if mode == 'post' else \
            self._breadth_order(self.root)

    def _pre_order(self, node, depth=0):
        if node is None:
            return
        yield node, depth
        yield from self._pre_order(node.left, depth + 1)
        yield from self._pre_order(node.right, depth + 1)

    def _in_order(self, node, depth=0):
        if node is None:
            return
        yield from self._in_order(node.left, depth + 1)
        yield node, depth
        yield from self._in_order(node.right, depth + 1)

    def _post_order(self, node, depth=0):
        if node is None:
            return
        yield from self._post_order(node.left, depth + 1)
        yield from self._post_order(node.right, depth + 1)
        yield node, depth

    def _breadth_order(self, node, depth=0):
        q = Queue()
        q.offer((node, depth))
        while q.size > 0:
            node, depth = q.poll()
            if node is None:
                continue
            yield node, depth
            q.offer((node.left, depth + 1))
            q.offer((node.right, depth + 1))


class Node(ABC):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None