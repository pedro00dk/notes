import abc
import enum

# prime numbers near to the 2**powers for power range of [1, 32]
PRIMES = (
    2, 3, 7, 17, 31, 67, 131, 257, 509, 1021, 2053, 4093, 8191, 16381, 32771, 65537, 131071, 262147, 524287, 1048573,
    2097143, 4194301, 8388617, 16777213, 33554467, 67108859, 134217757, 268435459, 536870909, 1073741827, 2147483647,
    4294967291
)


class Prober(enum.Enum):
    """
    Open Addressing probe strategies.
    - `'threshold'` contains the default and max load threshold for the hashtable for the probe function.
    - `'capacity'` a function to generate capacities for rebuilds, the first capacity and index must be 0.
    - `'probe'` is a function that creates indices from a hash and number of tries to place entries in the hashtable.
    """

    # Linear probing using prime size capacities.
    # Probing constants: probe: c1 = 1
    # For capacities above 2^32 it uses odd values based on the last prime.
    LINEAR = {
        'threshold': (0.65, 1),
        'capacity': lambda capacity, index: PRIMES[index + 3] if index + 3 < len(PRIMES) else capacity * 2 - 1,
        'probe': lambda capacity, hash_, trie: (hash_ + trie) % capacity
    }

    # Quadratic probing using prime size capacities.
    # However, due to probe the function, only half the indices are accessible.
    # Probing constants probe: c1 = c2 = 1; probe2: c1 = 0, c2 = 1; probe3: c1 = c2 = 1/2
    # For capacities above 2^32 it uses odd values based on the last prime (may fail).
    QUADRATIC_PRIME = {
        'threshold': (0.5, 0.5),
        'capacity': lambda capacity, index: PRIMES[index + 3] if index + 3 < len(PRIMES) else capacity * 2 - 1,
        'probe': lambda capacity, hash_, trie: (hash_ + trie ** 2 + trie) % capacity,
        'probe_2': lambda capacity, hash_, trie: (hash_ + trie ** 2) % capacity,
        'probe_3': lambda capacity, hash_, trie: (hash_ + (trie * 0.5) ** 2 + (trie * 0.5)) % capacity
    }

    # Quadratic probing using triangular numbers that fully covers indices on a hashtable of capacity 2**n.
    # Probing constants for triangular numbers probe: c1 = c2 = 1/2
    # However, because of the even capacity, it may increase collisions among keys even and odd keys independently.
    QUADRATIC_TRIANGULAR = {
        'threshold': (0.75, 1),
        'capacity': lambda capacity, index: 2**(index + 3),
        'probe': lambda capacity, hash_, trie: (hash_ + (trie ** 2 + trie) // 2) % capacity
    }


class Entry:
    """
    Base Entry class for hashtables.
    """

    def __init__(self, hash_: int, key, /, value=None):
        self.hash_ = hash_
        self.key = key
        self.value = value


class Hashtable(abc.ABC):
    """
    Abstract base class for hashtables.
    This class provides fields used in common hashtables, which are `table`, `load_threshold`, `capacity` and `size`
    """

    def __init__(self, /, prober=Prober.QUADRATIC_TRIANGULAR, load_threshold: int = None):
        """
        > parameters:
        - `prober: Prober? = Prober.QUADRATIC_TRIANGULAR`: hashtable index prober
        - `load_threshold: float`: hashtable load threshold, may be clamped to prober max threshold
        """
        self._prober = prober
        self._load_threshold = min(
            max(0.1, load_threshold if load_threshold is not None else self._prober.value['threshold'][0]),
            self._prober.value['threshold'][1]
        )
        self._capacity = self._prober.value['capacity'](0, 0)
        self._capacity_index = 1
        self._probe = self._prober.value['probe']
        self._table = [None] * self._capacity
        self._size = 0

    def __len__(self):
        return self._size

    def __str__(self):
        lines = '\n'.join(f'k: {key}, v: {value}' for key, value in self)
        return f'{type(self).__name__} prober={self._prober.name} {self._load_threshold} [\n{lines}\n]'

    def __iter__(self):
        return self.entries()

    def _rebuild(self):
        """
        Rebuild the hashtable to increase the internal capacity.
        This function should be used when the load factor surpass the allowed limit.
        This function relies on the `entries` (and consequently `__iter__`) generators continue using the old table
        while the new is being rebuilt.

        > complexity:
        - time: `O(n)`
        - space: `O(n)`
        > 
        """
        entries = iter(self)  # generator obtained before updating _table
        first = next(entries)  # start generator before updating references to ensure reference loads
        self._size = 0
        self._capacity = self._prober.value['capacity'](self._capacity, self._capacity_index)
        self._capacity_index += 1
        self._table = [None] * self._capacity
        self.put(*first)
        for key, value in entries:
            self.put(key, value)

    @abc.abstractmethod
    def entries(self):
        """
        Return a generator for hashtable keys and values.
        The generator must continue yielding entries from the hashtable correctly even it is being rebuilt.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > `return: Generator<(any, any)>`: generator of keys and values
        """
        pass

    def keys(self):
        """
        Return a generator for hashtable keys.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > `return: Generator<(any, any)>`: generator of keys
        """
        return (key for key, value in self.entries())

    def values(self):
        """
        Return a generator for hashtable values.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > `return: Generator<(any, any)>`: generator of values
        """
        return (value for key, value in self.entries())

    def empty(self):
        """
        Return if the structure is empty.

        > `return: bool`: if empty
        """
        return self._size == 0

    @abc.abstractmethod
    def put(self, key, /, value=None):
        """
        Insert a new entry containing `key` and `value` in the hashtable.
        If `key` already exists, then, `value` is replaced.

        > complexity:
        - time: `O(1)` amortized
        - space: `O(1)` amortized

        > parameters:
        - `key: any`: key of the entry
        - `value: any? = None`: value of the entry

        > `return: any`: `None` if it is a new key, otherwise the previous value associated with `key`
        """
        pass

    @abc.abstractmethod
    def take(self, key):
        """
        Remove from the entry containing `key` from the hashtable and return its value.

        > complexity: check subclass implementations

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > `return: any`: value associated with `key`
        """
        pass

    @abc.abstractmethod
    def get(self, key):
        """
        Retrieve the value associated with `key`.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `key: (int | float)`: key of value to retrieve

        > `return: any`: value associated with `key`
        """
        pass

    def contains(self, key):
        """
        Return `True` if `key` exists in the hashtable, `False` otherwise.

        > complexity:
        - time: `O(1)`
        - space: `O(log(n))`

        > parameters:
        - `key: any`: key to check

        > `return: bool`: if `key` exists
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def contains_value(self, value):
        """
        Return `True` if `value` exists in the hashtable, `False` otherwise.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > parameters:
        - `value: any`: value to check

        > `return: bool`: if `value` exists
        """
        for entry_key, entry_value in self:
            if value == entry_value:
                return True
        return False
