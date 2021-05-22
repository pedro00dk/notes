import abc
from typing import Generator, Generic, TypeVar

T = TypeVar("T")


class Linked(Generic[T], abc.ABC):
    """
    Abstract base class for linear data structures.
    """

    def __str__(self) -> str:
        return f"{type(self).__name__} {str([*self])}"

    @abc.abstractmethod
    def __len__(self) -> int:
        ...

    @abc.abstractmethod
    def __iter__(self) -> Generator[T, None, None]:
        """
        Return a generator or values contained in the linked structure.

        > complexity
        - see implementations

        - `return`: generator of values
        """

    def __contains__(self, value: T):
        """
        Explicitly implement contains protocol, `in` and `not in` operators.
        `__iter__` itself is usually enough to implement `in` and `not in` operators.

        > complexity
        - time: `O(Linked.__iter__)`
        - space: `O(Linked.__iter__)`
        - `Linked.__iter__`: cost of the `__iter__` function

        > parameters
        - `value`: value to check
        - `return`: if value exists
        """
        return any(value is v or value == v for v in self)

    def index(self, value: T):
        """
        Return the index of `value` in the structure.
        If `value` does not exist in the structure, an exception is raised.

        > complexity
        - time: `O(Linked.__iter__)`
        - space: `O(Linked.__iter__)`
        - `Linked.__iter__`: cost of the `__iter__` function

        > parameters
        - `value`: value to check
        - `return`: index of value
        """
        for i, v in enumerate(self):
            if value == v:
                return i
        raise ValueError(f"value {str(value)} not found")
