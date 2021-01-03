import abc
from typing import Callable, Generator, Generic, Optional, TypeVar

K = TypeVar('K')
V = TypeVar('V')


class Prober:
    """
    Hash probing strategies for map implemantations based on hashtables.
    """

    def __init__(self, load: float, capacity: Callable[[int, int], int], probe: Callable[[int, int, int], int]):
        """
        > parameters
        - `load`: load threshold for the hashtable for the probe function
        - `capacity`: a function to generate capacities for rebuilds, the first capacity and index must be 0
        - `probe`: is a function that creates indices from a hash and number of tries to place entries in the hashtable
        """
        self.load = load
        self.capacity = capacity
        self.probe = probe


# prime numbers near to the 2**powers for power range of [1, 32]
PRIMES = (
    2, 3, 7, 17, 31, 67, 131, 257, 509, 1021, 2053, 4093, 8191, 16381, 32771, 65537, 131071, 262147, 524287, 1048573,
    2097143, 4194301, 8388617, 16777213, 33554467, 67108859, 134217757, 268435459, 536870909, 1073741827, 2147483647,
    4294967291
)

# Linear probing using prime size capacities.
# Probing constants: probe: c1 = 1
# For capacities above 2^32 it uses odd values based on the last prime.
LINEAR_PROBER = Prober(
    0.65,
    lambda capacity, index: PRIMES[index + 3] if index + 3 < len(PRIMES) else capacity * 2 - 1,
    lambda capacity, hash_, trie: (hash_ + trie) % capacity,
)

# Quadratic probing using prime size capacities.
# However, due to probe the function, only half the indices are accessible.
# Probing constants probe: c1 = c2 = 1; probe2: c1 = 0, c2 = 1; probe3: c1 = c2 = 1/2
# For capacities above 2^32 it uses odd values based on the last prime (may fail).
QUADRATIC_PRIME_PROBER = Prober(
    0.5,
    lambda capacity, index: PRIMES[index + 3] if index + 3 < len(PRIMES) else capacity * 2 - 1,
    lambda capacity, hash_, trie: (hash_ + trie**2 + trie) % capacity,
)
# lambda capacity, hash_, trie: (hash_ + trie**2) % capacity,
# lambda capacity, hash_, trie: (hash_ + (trie * 0.5)**2 + (trie * 0.5)) % capacity

# Quadratic probing using triangular numbers that fully covers indices on a hashtable of capacity 2**n.
# Probing constants for triangular numbers probe: c1 = c2 = 1/2
# However, because of the even capacity, it may increase collisions among keys even and odd keys independently.
QUADRATIC_TRIANGULAR_PROBER = Prober(
    0.75,
    lambda capacity, index: 2**(index + 3),
    lambda capacity, hash_, trie: (hash_ + (trie**2 + trie) // 2) % capacity,
)


class Map(Generic[K, V], abc.ABC):
    """
    Abstract base class for mapping data structures.
    """

    def __str__(self) -> str:
        lines = '\n'.join(f'k: {key}, v: {value}' for key, value in self)
        return f'{type(self).__name__} [\n{lines}\n]'

    @abc.abstractmethod
    def __len__(self) -> int:
        pass

    @abc.abstractmethod
    def __iter__(self) -> Generator[tuple[K, V], None, None]:
        """
        Return a generator of entries (key and value tuples) contained in the map structure.
        If the map implementation is key order aware, tuples must be generated in order.

        > complexity
        - see implementations

        - `return`: generator of map entries
        """
        pass

    def __contains__(self, key: K) -> bool:
        """
        Explicitly implement contains protocol, `in` and `not in` operators.
        `__iter__` itself is usually enough to implement `in` and `not in` operators.

        > complexity
        - time: `O(Map.get)`
        - space: `O(Map.get)`
        - `Map.get`: cost of the `get` function

        > parameters
        - `key`: key to check
        - `return`: if key exists
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def keys(self) -> Generator[K, None, None]:
        """
        Return a generator of map keys.

        > complexity
        - time: `O(Map.__iter__)`
        - space: `O(Map.__iter__)`
        - `Map.get`: cost of the `get` function

        - `return`: generator of keys
        """
        return (key for key, _ in self)

    def values(self) -> Generator[V, None, None]:
        """
        Return a generator of map values.

        > complexity
        - time: `O(Map.__iter__)`
        - space: `O(Map.__iter__)`
        - `Map.__iter__`: cost of the `__iter__` function

        - `return`: generator of values
        """
        return (value for _, value in self)

    @abc.abstractmethod
    def put(self, key: K, value: V, replacer: Optional[Callable[[V, V], V]] = None) -> Optional[V]:
        """
        Insert a new entry containing `key` and `value` in the map.
        If `key` already exists, then, `value` is replaced.

        > complexity
        - see implementations

        > parameters
        - `key`: key of the entry
        - `value`: value of the entry
        - `replacer`: function to run if `key` already exists, the function parametes are the new and old values
            respectively, the return is the new value
        - `return`: `None` if it is a new key, otherwise the previous value associated with `key`
        """
        pass

    @abc.abstractmethod
    def take(self, key: K) -> V:
        """
        Remove from the entry containing `key` from the map and return its value.
        If `key` does not exist in the map, an exception is raised.

        > complexity check subclass implementations

        > complexity
        - see implementations

        > parameters
        - `key`: key of the entry
        - `return`: value associated with `key`
        """
        pass

    @abc.abstractmethod
    def get(self, key: K) -> V:
        """
        Retrieve the value associated with `key`.
        If `key` does not exist in the map, an exception is raised.

        > complexity
        - see implementations

        > parameters
        - `key`: key of value to retrieve
        - `return`: value associated with `key`
        """
        pass

    def contains_value(self, value: V) -> bool:
        """
        Return `True` if `value` exists in the map, `False` otherwise.

        > complexity
        - time: `O(Map.__iter__)`
        - space: `O(Map.__iter__)`
        - `Map.__iter__`: cost of the `__iter__` function

        > parameters
        - `value`: value to check
        - `return`: if `value` exists
        """
        for _, v in self:
            if value is v or value == v:
                return True
        return False
