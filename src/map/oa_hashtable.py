import dataclasses
from typing import Any, Callable, Generator, Generic, Literal, Optional, cast

from .abc import (LINEAR_PROBER, QUADRATIC_PRIME_PROBER,
                  QUADRATIC_TRIANGULAR_PROBER, K, Map, V)


@dataclasses.dataclass
class Entry(Generic[K, V]):
    hash_: int
    key: K
    value: V
    deleted = False


class OpenAddressingHashtable(Generic[K, V], Map[K, V]):
    """
    Open Addressing Hashtable implementation.

    > complexity
    - space: `O(n)`
    - `n`: number of elements in the structure
    """

    def __init__(self, prober_name: Literal['linear', 'prime', 'triangular'] = 'triangular'):
        """
        > parameters
        - `prober_name`: prober name
        """
        super().__init__()
        self._prober_name = prober_name
        self._prober = LINEAR_PROBER if self._prober_name == 'linear' else \
            QUADRATIC_PRIME_PROBER if self._prober_name == 'prime' else \
            QUADRATIC_TRIANGULAR_PROBER
        self._capacity_index: int = 0
        self._capacity = self._prober.capacity(0, self._capacity_index)
        self._length: int = 0
        self._table = cast(list[Optional[Entry[K, V]]], [None] * self._capacity)

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Generator[tuple[K, V], None, None]:
        """
        Check base class.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the hashtable
        """
        return ((entry.key, entry.value) for entry in self._table if entry is not None and not entry.deleted)

    def _rebuild(self, increase: bool):
        """
        Rebuild the hashtable to increase or decrease the internal capacity.
        This function should be used when the load factor reaches or surpass the allowed limit threshold, or when the
        load factor becomes smaller than the limit threshold divided by a factor greater then 2 (the factor is up to the
        hashtable implementation, 4 is recommended).

        > complexity
        - time: `O(n)`
        - space: `O(n)`
        - `n`: length of the hashtable

        > parameters
        - `increase`: if table should increase or decrease capacity
        """
        current_table = self._table
        self._capacity_index += 1 if increase else -1
        self._capacity = self._prober.capacity(self._capacity, self._capacity_index)
        self._length = 0
        self._table = cast(list[Optional[Entry[K, V]]], [None] * self._capacity)
        for entry in current_table:
            if entry is None or entry.deleted:
                continue
            self.put(entry.key, entry.value)

    def _find(self, key: K, free: bool = True) -> tuple[int, int, Optional[Entry[K, V]]]:
        """
        Suport function for hashtable operations.
        This function looks for indices and entries in the hashtable.
        It stops if:
        - `None` is found (free for insertion, not exists for deletion)
        - `free` is `True` and `entry.deleted` is `True` (free for insertion, not exists for deletion)
        - `free` is `False` and `entry.deleted` is `False` and `hash` equals (not free for insertion, deletion allowed)

        > complexity
        - time: `O(1) amortized`
        - space: `O(1) amortized`

        > parameters
        - `key`: key to search for in table entries
        - `free`: if should stop if entry with deleted flag set is found
        - `return`: tuple with key hash, index and entry (entry may be `None`)
        """
        hash_ = hash(key)
        index = 0
        entry: Optional[Entry[K, V]] = None
        for trie in range(self._capacity):
            index = self._prober.probe(self._capacity, hash_, trie)
            entry = self._table[index]
            if entry is None or \
                    free and entry.deleted or \
                    not entry.deleted and entry.hash_ == hash_ and entry.key == key:
                break
        return hash_, index, entry

    def put(self, key: K, value: V, replacer: Optional[Callable[[V, V], V]] = None) -> Optional[V]:
        """
        Check base class.

        > complexity
        - time: `O(1) amortized`
        - space: `O(1) amortized`
        """
        if self._length / self._capacity >= self._prober.load:
            self._rebuild(True)
        hash_, index, entry = self._find(key, True)
        if entry is None or entry.deleted:
            self._length += 1
        value = value if replacer is None or entry is None or entry.deleted else replacer(value, entry.value)
        self._table[index] = Entry(hash_, key, value)
        return entry.value if entry is not None and not entry.deleted else None

    def take(self, key: K) -> V:
        """
        Check base class.

        > complexity
        - time: `O(1) amortized`
        - space: `O(1) amortized`
        """
        if self._length / self._capacity < self._prober.load / 4:
            self._rebuild(False)
        _, _, entry = self._find(key, False)
        if entry is None:
            raise KeyError(f'key ({key}) not found')
        value = entry.value
        entry.deleted = True
        del entry.key
        del entry.value
        self._length -= 1
        return value

    def get(self, key: K) -> V:
        """
        Check base class.

        > complexity
        - time: `O(1) amortized`
        - space: `O(1) amortized`
        """
        _, _, entry = self._find(key, False)
        if entry is None:
            raise KeyError(f'key ({key}) not found')
        return entry.value


def test():
    import random

    from ..test import match

    for prober_name in ('linear', 'prime', 'triangular'):
        hashtable = OpenAddressingHashtable[int, int](cast(Any, prober_name))
        match((
            *((hashtable.put, (str(i), i * 2), None) for i in random.sample([i for i in range(100)], 100)),
            (print, (hashtable,)),
            *((hashtable.take, (str(i),), i * 2) for i in random.sample([i for i in range(100)], 100) if i % 3 == 0),
            (print, (hashtable,)),
        ))


if __name__ == '__main__':
    test()
