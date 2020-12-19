import abc
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar('T')


class Heap(Generic[T], abc.ABC):
    """
    Abstract base class for heaps.
    This class provides basic fields used in common heap data structures, which are `heap` and `comparator`
    """

    @abc.abstractmethod
    def __init__(
        self,
        comparator: Callable[[T, T], float],
        data: Optional[list[T]] = None,
    ):
        """
        > complexity check tree implementations

        > parameters
        - `data: <T>[]`: initial data to populate the heap
        - `comparator: ('min' | 'max' | (<T>, <T>) => int)? = max`: a comparator string for numeric values
            (`min`, `max`) or a min comparator to check values (smaller values go to the top)
        """
        self._comparator = comparator
        self._heap: list[T] = data if data is not None else []

    def __len__(self) -> int:
        return len(self._heap)

    def __str__(self) -> str:
        return f'{type(self).__name__} {self._heap}'

    def empty(self) -> bool:
        """
        Return if the structure is empty.

        - `return`: if empty
        """
        return len(self._heap) == 0

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

    def peek(self) -> T:
        """
        Get the value at the top of the heap without removing it.

        > complexity check subclass implementations

        - `return`: value at the top of the heap
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        return self._heap[0]
