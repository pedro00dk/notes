from __future__ import annotations

import abc
from typing import Generator, Generic, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    """
    Base Node class for linear data structures.
    """

    def __init__(self, value: T, next: Optional[Node[T]] = None):
        self.value = value
        self.next: Optional[Node[T]] = next


class Linear(Generic[T], abc.ABC):
    """
    Abstract base class for linear data structures.
    This class provides basic fields used in common linear data structures, which are `head`, `tail` and `size`
    """

    @abc.abstractmethod
    def __init__(self):
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        return f'{type(self).__name__} [{", ".join(str(value) for value in self)}]'

    def __iter__(self) -> Generator[T, None, None]:
        return self.values()

    def _check(self, index: int, insert: bool = False):
        """
        Checks by raising an exception if index is inside the structure range.
        If `insert`, the `_size` value is also allowed.

        > parameters
        - `index`: index to check
        - `insert`: if is an insertion index
        """
        if index < 0 or insert and index > self._size or not insert and index >= self._size:
            raise IndexError(f'index ({index}) out of range [0, {self._size}{"]" if insert else ")"}')

    def _nodes(self) -> Generator[Node[T], None, None]:
        """
        Return a generator for the structure nodes.

        - `return`: iterator of structure nodes
        """
        node = self._head
        while node is not None:
            yield node
            node = node.next

    def values(self) -> Generator[T, None, None]:
        """
        Return a generator for the structure values.

        - `return`: iterator of structure values
        """
        return (node.value for node in self._nodes())

    def empty(self) -> bool:
        """
        Return if the structure is empty.

        - `return`: if empty
        """
        return self._size == 0

    def index(self, value: T):
        """
        Return the index of `value` in the structure, or `None` if not found.

        > parameters
        - `value`: value to check
        - `return`: index of value
        """
        for i, v in enumerate(self.values()):
            if value == v:
                return i
        return None

    def contains(self, value: T):
        """
        Return if the structure contains `value`.

        > parameters
        - `value`: value to check
        - `return`: if contains
        """
        return any(value == v for v in self.values())
