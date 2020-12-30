import abc
from typing import Generic, TypeVar

T = TypeVar('T')


class Heap(Generic[T], abc.ABC):
    """
    Abstract base class for heaps.
    """

    @abc.abstractmethod
    def __len__(self) -> int:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    def empty(self) -> bool:
        """
        Return if the structure is empty.

        - `return`: if empty
        """
        return len(self) == 0

    @abc.abstractmethod
    def offer(self, value: T):
        """
        Insert `value` in the heap.

        > complexity check subclass implementations

        > parameters
        - `value: <T>`: value to insert
        """
        pass

    @abc.abstractmethod
    def poll(self) -> T:
        """
        Delete the value at the top of the heap.

        > complexity check subclass implementations

        - `return`: deleted value
        """
        pass

    @abc.abstractmethod
    def peek(self) -> T:
        """
        Get the value at the top of the heap without removing it.

        > complexity check subclass implementations

        - `return`: value at the top of the heap
        """
        pass
