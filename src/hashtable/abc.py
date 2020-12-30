import abc
from typing import (Callable, Generator, Generic, Literal, Optional, TypeVar,
                    cast)


class Prober:
    """
    Hash probing strategies.
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


K = TypeVar('K')
V = TypeVar('V')


class Entry(Generic[K, V]):
    """
    Base Entry class for hashtables.
    """

    def __init__(self, hash_: int, key: K, value: V):
        self.hash_ = hash_
        self.key = key
        self.value = value


class Hashtable(Generic[K, V], abc.ABC):
    """
    Abstract base class for hashtables.
    This class provides fields used in common hashtables, which are `table`, `load_threshold`, `capacity` and `size`
    """

    def __init__(self, prober_name: Literal['linear', 'prime', 'triangular'] = 'triangular'):
        """
        > parameters
        - `prober`: prober data
        """
        self._prober_name = prober_name
        self._prober = LINEAR_PROBER if self._prober_name == 'linear' else \
            QUADRATIC_PRIME_PROBER if self._prober_name == 'prime' else \
            QUADRATIC_TRIANGULAR_PROBER
        self._capacity_index: int = 0
        self._capacity = self._prober.capacity(0, self._capacity_index)
        self._size: int = 0
        self._table = cast(list[Optional[Entry[K, V]]], [None] * self._capacity)

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        lines = '\n'.join(f'k: {key}, v: {value}' for key, value in self)
        return f'{type(self).__name__} prober={self._prober_name} {self._prober.load} [\n{lines}\n]'

    def __iter__(self) -> Generator[tuple[K, V], None, None]:
        return self.entries()

    def _rebuild(self, increase: bool):
        """
        Rebuild the hashtable to increase or decrease the internal capacity.
        This function should be used when the load factor reaches or surpass the allowed limit threshold, or when the
        load factor becomes smaller than the limit threshold divided by a factor greater then 2 (the factor is up to the
        hashtable implementation, 4 is recommended).
        This function relies on the `entries` (and consequently `__iter__`) iterators to continue using the old table
        while the new is being rebuilt.

        > complexity
        - time: `O(n)`
        - space: `O(n)`

        > parameters
        - `increase: bool`: if table should increase or decrease size
        """
        entries = iter(self)  # iterator obtained before updating _table
        first = next(entries)  # start iterator before updating references to ensure reference loads
        self._size = 0
        self._capacity_index += 1 if increase else -1
        self._capacity = self._prober.capacity(self._capacity, self._capacity_index)
        self._table = [None] * self._capacity
        self.put(*first)
        for key, value in entries:
            self.put(key, value)

    @abc.abstractmethod
    def entries(self) -> Generator[tuple[K, V], None, None]:
        """
        Return a iterator for hashtable keys and values.
        The iterator must continue yielding entries from the hashtable correctly even it is being rebuilt.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        - `return`: generator of keys and values
        """
        pass

    def keys(self) -> Generator[K, None, None]:
        """
        Return a iterator for hashtable keys.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        - `return`: generator of keys
        """
        return (key for key, _ in self.entries())

    def values(self) -> Generator[V, None, None]:
        """
        Return a iterator for hashtable values.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        - `return`: generator of values
        """
        return (value for _, value in self.entries())

    def empty(self):
        """
        Return if the structure is empty.

        - `return`: if empty
        """
        return self._size == 0

    @abc.abstractmethod
    def put(self, key: K, value: V) -> Optional[V]:
        """
        Insert a new entry containing `key` and `value` in the hashtable.
        If `key` already exists, then, `value` is replaced.

        > complexity
        - time: `O(1)` amortized
        - space: `O(1)` amortized

        > parameters
        - `key`: key of the entry
        - `value`: value of the entry
        - `return`: `None` if it is a new key, otherwise the previous value associated with `key`
        """
        pass

    @abc.abstractmethod
    def take(self, key: K) -> V:
        """
        Remove from the entry containing `key` from the hashtable and return its value.

        > complexity check subclass implementations

        > complexity
        - time: `O(1)` amortized
        - space: `O(1)` amortized

        > parameters
        - `key`: key of the entry
        - `return`: value associated with `key`
        """
        pass

    @abc.abstractmethod
    def get(self, key: K) -> V:
        """
        Retrieve the value associated with `key`.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `key`: key of value to retrieve
        - `return`: value associated with `key`
        """
        pass

    def contains(self, key: K) -> bool:
        """
        Return `True` if `key` exists in the hashtable, `False` otherwise.

        > complexity
        - time: `O(1)`
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

    def contains_value(self, value: V) -> bool:
        """
        Return `True` if `value` exists in the hashtable, `False` otherwise.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        > parameters
        - `value`: value to check
        - `return`: if `value` exists
        """
        for _, entry_value in self:
            if value == entry_value:
                return True
        return False
