from abc import ABC, abstractmethod

from ..linked.queue import Queue


class Tree(ABC):
    def __init__(self, printer):
        self.printer = printer
        self.root = None
        self.size = 0

    def __iter__(self):
        return self.traverse()

    def __len__(self):
        return self.size

    def __str__(self):
        tree = '\n'.join(f'{"|  " * depth}├─ {self.printer(node, depth)}' for node, depth in self.traverse('pre'))
        return f'{type(self).__name__} [\n{tree}\n]'

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
        queue = Queue()
        queue.offer((node, depth))
        while len(queue) > 0:
            node, depth = queue.poll()
            if node is None:
                continue
            yield node, depth
            queue.offer((node.left, depth + 1))
            queue.offer((node.right, depth + 1))

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

    def contains(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def contains_value(self, value):
        for node, depth in self.traverse():
            if value == node.value:
                return True
        return False

    def empty(self):
        return self.size == 0

    def traverse(self, mode='in'):
        return self._pre_order(self.root) if mode == 'pre' else \
            self._in_order(self.root) if mode == 'in' else \
            self._post_order(self.root) if mode == 'post' else \
            self._breadth_order(self.root)


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
