import abc
import collections
from typing import Callable, Generator, Generic, Literal, Optional, TypeVar, Union


T = TypeVar('T', bool, int, float, str)
U = TypeVar('U')


class Node(Generic[T, U]):
    """
    Base Node class for trees.
    """

    def __init__(self, key: T, value: U):
        self.key = key
        self.value = value
        self.left: Optional[Node[T, U]] = None
        self.right: Optional[Node[T, U]] = None


class Tree(Generic[T, U], abc.ABC):
    """
    Abstract base class for binary trees.
    This class provides basic fields used in common tree data structures, which are `root` and `size`
    The `printer` attribute is used to generate the tree string representation
    """

    def __init__(self, printer: Callable[[Node[T, U], int], str]):
        """
        > parameters
        - `printer: (Node, int) => str`: function to print a tree node info from the node object and its depth
        """
        self._root: Optional[Node[T, U]] = None
        self._size = 0
        self._printer = printer

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        tree = '\n'.join(f'{"|  " * depth}├─ {self._printer(node, depth)}' for node, depth in self._traverse('pre'))
        return f'{type(self).__name__} [\n{tree}\n]'

    def __iter__(self) -> Generator[tuple[T, Union[U, None], int], None, None]:
        return self.traverse()

    def _pre(self, node: Optional[Node[T, U]], depth: int = 0) -> Generator[tuple[Node[T, U], int], None, None]:
        """
        Return a generator for tree pre-order traversals.

        > complexity
        - time: `O(n)`
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters
        - `node`: root node for traversal
        - `depth`: base depth
        - `return`: generator of nodes and depths
        """
        if node is None:
            return
        yield node, depth
        yield from self._pre(node.left, depth=depth + 1)
        yield from self._pre(node.right, depth=depth + 1)

    def _in(self, node: Optional[Node[T, U]], depth: int = 0) -> Generator[tuple[Node[T, U], int], None, None]:
        """
        Return a generator for tree in-order traversals.

        > complexity
        - time: `O(n)`
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters
        - `node`: root node for traversal
        - `depth`: base depth
        - `return`: generator of nodes and depths
        """
        if node is None:
            return
        yield from self._in(node.left, depth=depth + 1)
        yield node, depth
        yield from self._in(node.right, depth=depth + 1)

    def _post(self, node: Optional[Node[T, U]], depth: int = 0) -> Generator[tuple[Node[T, U], int], None, None]:
        """
        Return a generator for tree post-order traversals.

        > complexity
        - time: `O(n)`
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters
        - `node`: root node for traversal
        - `depth`: base depth
        - `return`: generator of nodes and depths
        """
        if node is None:
            return
        yield from self._post(node.left, depth=depth + 1)
        yield from self._post(node.right, depth=depth + 1)
        yield node, depth

    def _breadth(self, node: Optional[Node[T, U]], depth: int = 0) -> Generator[tuple[Node[T, U], int], None, None]:
        """
        Return a generator for tree breadth-order traversals.

        > complexity
        - time: `O(n)`
        - space: `O(n)`

        > parameters
        - `node`: root node for traversal
        - `depth`: base depth
        - `return`: generator of nodes and depths
        """
        if node is None:
            return
        queue = collections.deque[tuple[Node[T, U], int]]()
        queue.append((node, depth))
        while len(queue) > 0:
            node, depth = queue.popleft()
            yield node, depth
            if node.left is not None:
                queue.append((node.left, depth + 1))
            if node.right is not None:
                queue.append((node.right, depth + 1))

    def _traverse(
        self,
        mode: Literal['pre', 'in', 'post', 'breadth'] = 'in'
    ) -> Generator[tuple[Node[T, U], int], None, None]:
        """
        Return a generator for tree node traversal in the provided `mode`.

        > complexity
        - time: `O(n)`
        - space: `O(log(n))` or `O(n)` depending on the mode and tree type

        > parameters
        - `mode`: traversal mode
        - `return`: generator of nodes and depths
        """
        return self._pre(self._root) if mode == 'pre' else \
            self._in(self._root) if mode == 'in' else \
            self._post(self._root) if mode == 'post' else \
            self._breadth(self._root)

    def traverse(
        self,
        mode: Literal['pre', 'in', 'post', 'breadth'] = 'in'
    ) -> Generator[tuple[T, U, int], None, None]:
        """
        Return a generator for tree keys and values traversal in the provided `mode`.

        > complexity
        - time: `O(n)`
        - space: `O(log(n))` or `O(n)` depending on the mode and tree type

        > parameters
        - `mode`: traversal mode
        - `return`: generator of nodes and depths
        """
        return ((node.key, node.value, depth) for node, depth in self._traverse(mode))

    def empty(self) -> bool:
        """
        Return if the structure is empty.

        - `return`: if empty
        """
        return self._size == 0

    @abc.abstractmethod
    def put(self, key: T, value: U, replacer: Optional[Callable[[U, U], U]] = None) -> Optional[U]:
        """
        Insert a new entry containing `key` and `value` in the tree.
        If `key` already exists, then, `value` is replaced.

        > complexity
        - check subclass implementations

        > parameters
        - `key`: key of the entry
        - `value`: value of the entry
        - `replacer`: function to run if `key` already exists, the function parametes are the new and old values
            respectively, the return is the new value
        - `return`: `None` if it is a new key, otherwise the previous value associated with `key`
        """
        pass

    @abc.abstractmethod
    def take(self, key: T) -> U:
        """
        Remove from the entry containing `key` from the tree and return its value.

        > complexity
        - check subclass implementations

        > parameters
        - `key`: key of the entry
        - `return`: value associated with `key`
        """
        pass

    def get(self, key: T) -> U:
        """
        Retrieve the value associated with `key`.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(1)`

        > parameters
        - `key`: key of value to retrieve
        - `return`: value associated with `key`
        """
        node = self._root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError(f'key ({key}) not found')
        return node.value

    def contains(self, key: T) -> bool:
        """
        Return `True` if `key` exists in the tree, `False` otherwise.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(log(n))`

        > parameters
        - `key`: key to check
        - `return`: if `key` exists
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def contains_value(self, value: U) -> bool:
        """
        Return `True` if `value` exists in the tree, `False` otherwise.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        > parameters
        - `value`: value to check
        - `return`: if `value` exists
        """
        for _, node_value, _ in self:
            if value == node_value:
                return True
        return False

    def minimum(self) -> Optional[tuple[T, U]]:
        """
        Retrieve smallest key and value in the tree.
        Return `None` if the tree is empty.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(1)`

        - `return`: minimum key and its value
        """
        node = self._root
        while node is not None and node.left is not None:
            node = node.left
        return (node.key, node.value) if node is not None else None

    def maximum(self) -> Optional[tuple[T, U]]:
        """
        Retrieve greatest key and value in the tree.
        Return `None` if the tree is empty.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(1)`

        - `return`: maximum key and its value
        """
        node = self._root
        while node is not None and node.right is not None:
            node = node.right
        return (node.key, node.value) if node is not None else None

    def ancestor(self, key: T) -> Optional[tuple[T, U]]:
        """
        Retrieve the ancestor of `key`.
        If `key` is the tree `min`, then `None` is returned.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters
        - `key`: key of value to retrieve ancestor
        - `return`: key and value ancestor of `key`
        """
        parents: list[Node[T, U]] = []
        node = self._root
        while node is not None and key != node.key:
            parents.append(node)
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError(f'key ({key}) not found')
        if node.left is not None:
            ancestor = node.left
            while ancestor.right is not None:
                ancestor = ancestor.right
            return ancestor.key, ancestor.value
        for parent in reversed(parents):
            if parent.key < key:
                return parent.key, parent.value
        return None

    def successor(self, key: T) -> Optional[tuple[T, U]]:
        """
        Retrieve the successor of `key`.
        If `key` is the tree `max`, then `None` is returned.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters
        - `key: int | float`: key of value to retrieve ancestor

        - `return`: key and value successor of `key`
        """
        parents: list[Node[T, U]] = []
        node = self._root
        while node is not None and key != node.key:
            parents.append(node)
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError(f'key ({key}) not found')
        if node.right is not None:
            ancestor = node.right
            while ancestor.left is not None:
                ancestor = ancestor.left
            return ancestor.key, ancestor.value
        for parent in reversed(parents):
            if parent.key > key:
                return parent.key, parent.value
        return None
