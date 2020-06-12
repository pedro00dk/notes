import abc


class Node:
    """
    Base Node class for linear data structures.
    """

    def __init__(self, value, /, next=None):
        self.value = value
        self.next = next


class Linear(abc.ABC):
    """
    Abstract base class for linear data structures.
    This class provides basic fields used in common linear data structures, which are `head`, `tail` and `size`
    """

    @abc.abstractmethod
    def __init__(self):
        self._head = self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __str__(self):
        return f'{type(self).__name__} [{", ".join(str(value) for value in self)}]'

    def __iter__(self):
        return self.values()

    def _check(self, index: int, /, insert=False):
        """
        Checks by raising an exception if index is inside the structure range.
        If `insert`, the `_size` value is also allowed.

        > parameters:
        - `index: int`: index to check
        - `insert: bool? = False`: if is an insertion index
        """
        if index < 0 or insert and index > self._size or not insert and index >= self._size:
            raise IndexError(f'index ({index}) out of range [0, {self._size}{"]" if insert else ")"}')

    def _nodes(self):
        """
        Return a generator for the structure nodes.

        > `return: Generator(Node)`: generator of structure nodes
        """
        node = self._head
        while node is not None:
            yield node
            node = node.next

    def values(self):
        """
        Return a generator for the structure values.

        > `return: Generator(any)`: generator of structure values
        """
        return (node.value for node in self._nodes())

    def empty(self):
        """
        Return if the structure is empty.

        > `return: bool`: if empty
        """
        return self._size == 0

    def index(self, value):
        """
        Return the index of `value` in the structure, or `None` if not found.

        > parameters:
        - `value: any`: value to check

        > `return: int`: index of value
        """
        for i, v in enumerate(self.values()):
            if value == v:
                return i
        return None

    def contains(self, value):
        """
        Return if the structure contains `value`.

        > parameters:
        - `value: any`: value to check

        > `return: bool`: if contains
        """
        return any(value == v for v in self.values())
