import abc
from typing import Generator, Generic, TypeVar

T = TypeVar("T")


class Priority(Generic[T], abc.ABC):
    """
    Abstract base class for priority queues.
    """

    def __str__(self) -> str:
        return f"{type(self).__name__} {str([*self])}"

    @abc.abstractmethod
    def __len__(self) -> int:
        ...

    @abc.abstractmethod
    def __iter__(self) -> Generator[T, None, None]:
        """
        Return a generator or values contained in the priority queue structure.
        The values are yielded in priority order, but not consumed from the priority queue.

        > complexity
        - see implementations

        - `return`: generator of values sorted by priority
        """

    def __contains__(self, value: T):
        """
        Explicitly implement contains protocol, `in` and `not in` operators.
        `__iter__` itself is usually enough to implement `in` and `not in` operators.

        > complexity
        - time: `O(Heap.__iter__)`
        - space: `O(Heap.__iter__)`
        - `Heap.__iter__`: cost of the `__iter__` function

        > parameters
        - `value`: value to check
        - `return`: if value exists
        """
        return any(value is v or value == v for v in self)

    @abc.abstractmethod
    def offer(self, value: T):
        """
        Insert `value` in the priority queue.

        > complexity
        - see implementations

        > parameters
        - `value`: value to insert
        """

    @abc.abstractmethod
    def poll(self) -> T:
        """
        Delete and return the next value from the priority queue.

        > complexity
        - see implementations

        - `return`: deleted value
        """

    @abc.abstractmethod
    def peek(self) -> T:
        """
        Get the next value from que priority queue without removing it.

        > complexity
        - see implementations

        - `return`: next value
        """
