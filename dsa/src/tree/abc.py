import abc
from typing import Any, Generic, Optional, Protocol, TypeVar

from ..map.abc import Map
from ..priority.abc import Priority


class Comparable(Protocol):
    def __lt__(self, _other: Any) -> bool:
        ...

    def __le__(self, _other: Any) -> bool:
        ...

    def __gt__(self, _other: Any) -> bool:
        ...

    def __ge__(self, _other: Any) -> bool:
        ...


K = TypeVar("K", bound=Comparable)
V = TypeVar("V")


class Tree(Generic[K, V], Map[K, V], Priority[K]):
    """
    Abstract base class for trees.
    This abstract base class extends the `Priority` and `Map` abstract base classes.
    The `printer` attribute is used to generate the tree string representation.
    """

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def minimum(self) -> Optional[tuple[K, V]]:
        """
        Retrieve smallest key and value in the tree.
        Return `None` if the tree is empty.

        > complexity
        - see implementations

        - `return`: minimum key and its value
        """

    @abc.abstractmethod
    def maximum(self) -> Optional[tuple[K, V]]:
        """
        Retrieve greatest key and value in the tree.
        Return `None` if the tree is empty.

        > complexity
        - see implementations

        - `return`: maximum key and its value
        """

    @abc.abstractmethod
    def predecessor(self, key: K) -> Optional[tuple[K, V]]:
        """
        Retrieve the predecessor of `key`.
        `key` does not need to be inserted in the tree.
        If `key` is smaller or equal the maximum, or the tree is empty, `None` is returned.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters
        - `key`: key to retrieve predecessor
        - `return`: predecessor of `key`
        """

    @abc.abstractmethod
    def successor(self, key: K) -> Optional[tuple[K, V]]:
        """
        Retrieve the successor of `key`.
        `key` does not need to be inserted in the tree.
        If `key` is greater or equal the maximum, `None` is returned.

        > complexity
        - time: `O(n)` or `O(log(n))` for balanced trees
        - space: `O(n)` or `O(log(n))` for balanced trees

        > parameters
        - `key`: key to retrieve successor
        - `return`: successor of `key`
        """

    # heap abstract base class implementation

    def offer(self, value: K):
        """
        Check base class.

        > complexity
        - time: `O(Map.put)`
        - space: `O(Map.put)`
        - `Map.put`: cost of the `put` function
        """
        self.put(value, None)

    def poll(self) -> K:
        """
        Check base class.

        > complexity
        - time: `O(Tree.minimum + Map.take)`
        - space: `O(Tree.minimum + Map.take)`
        - `Tree.minimum`: cost of the `minimum` function
        - `Map.put`: cost of the `put` function
        """
        minimum = self.minimum()
        if minimum is None:
            raise IndexError("empty heap")
        self.take(minimum[0])
        return minimum[0]

    def peek(self) -> K:
        """
        Check base class.

        > complexity
        - time: `O(Tree.minimum)`
        - space: `O(Tree.minimum)`
        - `Tree.minimum`: cost of the `minimum` function
        """
        minimum = self.minimum()
        if minimum is None:
            raise IndexError("empty heap")
        return minimum[0]
