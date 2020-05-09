from abc import ABC, abstractmethod

from ..linked.queue import Queue


class Tree(ABC):
    def __init__(self, printer):
        self._printer = printer
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __str__(self):
        tree = '\n'.join(f'{"|  " * depth}├─ {self._printer(node, depth)}' for node, depth in self._traverse('pre'))
        return f'{type(self).__name__} [\n{tree}\n]'

    def __iter__(self):
        return self.traverse()

    def _pre(self, node, / , *, depth=0):
        if node is None:
            return
        yield node, depth
        yield from self._pre(node.left, depth=depth + 1)
        yield from self._pre(node.right, depth=depth + 1)

    def _in(self, node, /, *, depth=0):
        if node is None:
            return
        yield from self._in(node.left, depth=depth + 1)
        yield node, depth
        yield from self._in(node.right, depth=depth + 1)

    def _post(self, node, / , *, depth=0):
        if node is None:
            return
        yield from self._post(node.left, depth=depth + 1)
        yield from self._post(node.right, depth=depth + 1)
        yield node, depth

    def _breadth(self, node, / , *, depth=0):
        queue = Queue()
        queue.offer((node, depth))
        while len(queue) > 0:
            node, depth = queue.poll()
            if node is None:
                continue
            yield node, depth
            queue.offer((node.left, depth + 1))
            queue.offer((node.right, depth + 1))

    def _traverse(self, mode='in'):
        return self._pre(self._root) if mode == 'pre' else \
            self._in(self._root) if mode == 'in' else \
            self._post(self._root) if mode == 'post' else \
            self._breadth(self._root)

    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def take(self, key):
        pass

    def get(self, key):
        node = self._root
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
        for node_key, node_value, depth in self:
            if value == node_value:
                return True
        return False

    def empty(self):
        return self._size == 0

    def traverse(self, mode='in'):
        return ((node.key, node.value, depth) for node, depth in self._traverse(mode))


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
