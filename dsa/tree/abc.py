from abc import ABC, abstractmethod

from ..linear.queue import Queue


class Node:
    """
    Base Node class for tree data structures.
    """

    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Tree(ABC):
    """
    Abstract base class for binary tree data structures.
    This class provides basic fields used in common tree data structures, which are `root` and `size`
    The `printer` attribute is used to generate the tree string representation
    """

    def __init__(self, printer: type(lambda node, depth: '')):
        self._root = None
        self._size = 0
        self._printer = printer

    def __len__(self):
        return self._size

    def __str__(self):
        tree = '\n'.join(f'{"|  " * depth}├─ {self._printer(node, depth)}' for node, depth in self._traverse('pre'))
        return f'{type(self).__name__} [\n{tree}\n]'

    def __iter__(self):
        return self.traverse()

    def _pre(self, node: Node, depth=0):
        """
        Return a generator for tree pre-order traversals.

        > complexity:
        - time: `O(n)`
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters:
        - `node: Node`: root node for traversal
        - `depth: int`: base depth

        > `return: Generator<(Node, int)>`: generator of nodes and depths
        """
        if node is None:
            return
        yield node, depth
        yield from self._pre(node.left, depth=depth + 1)
        yield from self._pre(node.right, depth=depth + 1)

    def _in(self, node, /, *, depth=0):
        """
        Return a generator for tree in-order traversals.

        > complexity:
        - time: `O(n)`
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters:
        - `node: Node`: root node for traversal
        - `depth: int`: base depth

        > `return: Generator<(Node, int)>`: generator of nodes and depths
        """
        if node is None:
            return
        yield from self._in(node.left, depth=depth + 1)
        yield node, depth
        yield from self._in(node.right, depth=depth + 1)

    def _post(self, node, /, *, depth=0):
        """
        Return a generator for tree post-order traversals.

        > complexity:
        - time: `O(n)`
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters:
        - `node: Node`: root node for traversal
        - `depth: int`: base depth

        > `return: Generator<(Node, int)>`: generator of nodes and depths
        """
        if node is None:
            return
        yield from self._post(node.left, depth=depth + 1)
        yield from self._post(node.right, depth=depth + 1)
        yield node, depth

    def _breadth(self, node, /, *, depth=0):
        """
        Return a generator for tree breadth-order traversals.

        > complexity:
        - time: `O(n)`
        - space: `O(n)`

        > parameters:
        - `node: Node`: root node for traversal
        - `depth: int`: base depth

        > `return: Generator<(Node, int)>`: generator of nodes and depths
        """
        queue = Queue()
        queue.offer((node, depth))
        while not queue.empty():
            node, depth = queue.poll()
            if node is None:
                continue
            yield node, depth
            queue.offer((node.left, depth + 1))
            queue.offer((node.right, depth + 1))

    def _traverse(self, /, mode='in'):
        """
        Return a generator for tree node traversal in the provided `mode`.

        > complexity:
        - time: `O(n)`
        - space: `O(log(n))` or `O(n)` depending on the mode and tree type

        > parameters:
        - `mode: str? = `'in'`: traversal mode, one of `'pre', 'in', 'post', 'breadth'`

        > `return: Generator<(Node, int)>`: generator of nodes and depths
        """
        return self._pre(self._root) if mode == 'pre' else \
            self._in(self._root) if mode == 'in' else \
            self._post(self._root) if mode == 'post' else \
            self._breadth(self._root)

    def traverse(self, /, mode='in'):
        """
        Return a generator for tree keys and values traversal in the provided `mode`.

        > complexity:
        - time: `O(n)`
        - space: `O(log(n))` or `O(n)` depending on the mode and tree type

        > parameters:
        - `mode: str? = `'in'`: traversal mode, one of `'pre', 'in', 'post', 'breadth'`

        > `return: Generator<((int | float), any, int)>`: generator of nodes and depths
        """
        return ((node.key, node.value, depth) for node, depth in self._traverse(mode))

    def empty(self):
        """
        Return if the structure is empty.

        > `return: bool`: if empty
        """
        return self._size == 0

    @abstractmethod
    def put(self, key, /, value=None):
        """
        Insert a new entry containing `key` and `value` in the tree.
        If `key` already exists, then, `value` is replaced.

        > complexity: check tree implementations

        > parameters:
        - `key: (int | float)`: key of the entry
        - `value: any? = None`: value of the entry

        > `return: any`: `None` if it is a new key, otherwise the previous value associated with `key`
        """
        pass

    @abstractmethod
    def take(self, key):
        """
        Remove from the entry containing `key` from the tree and return its value.

        > complexity: check tree implementations

        > parameters:
        - `key: (int | float)`: key of the entry

        > `return: any`: value associated with `key`
        """
        pass

    def get(self, key):
        """
        Retrieve the value associated with `key`.

        > complexity:
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(1)`

        > parameters:
        - `key: (int | float)`: key of value to retrieve

        > `return: any`: value associated with `key`
        """
        node = self._root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError('not found')
        return node.value

    def contains(self, key):
        """
        Return `True` if `key` exists in the tree, `False` otherwise.

        > complexity:
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(log(n))`

        > parameters:
        - `key: (int | float)`: key to check

        > `return: bool`: if `key` exists
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def contains_value(self, value):
        """
        Return `True` if `value` exists in the tree, `False` otherwise.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > parameters:
        - `value: any`: value to check

        > `return: bool`: if `value` exists
        """
        for node_key, node_value, depth in self:
            if value == node_value:
                return True
        return False
