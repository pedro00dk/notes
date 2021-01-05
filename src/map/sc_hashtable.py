from typing import Any, Callable, Generator, Generic, Literal, Optional, cast

from .abc import (LINEAR_PROBER, QUADRATIC_PRIME_PROBER,
                  QUADRATIC_TRIANGULAR_PROBER, K, Map, V)


class EntryNode(Generic[K, V]):
    def __init__(self, hash_: int, key: K, value: V):
        self.hash_ = hash_
        self.key = key
        self.value = value
        self.next: Optional[EntryNode[K, V]] = None


class SequenceChainingHashtable(Generic[K, V], Map[K, V]):
    """
    Sequence chaining Hashtable implementation.
    Probers have minimal impact in sequence chaining performance, if probers produce the same index for `trie = 0`,
    the only change is the capacity and threshold limits. 

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
        self._table = cast(list[Optional[EntryNode[K, V]]], [None] * self._capacity)

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
        for entry in self._table:
            cursor = entry
            while cursor is not None:
                yield cursor.key, cursor.value
                cursor = cursor.next

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
        self._table = cast(list[Optional[EntryNode[K, V]]], [None] * self._capacity)
        for entry in current_table:
            cursor = entry
            while cursor is not None:
                self.put(cursor.key, cursor.value)
                cursor = cursor.next

    def _find(self, key: K) -> tuple[int, int, Optional[EntryNode[K, V]]]:
        """
        Suport function for hashtable operations.
        This function looks for indices and entries in the hashtable.

        > parameters
        - `key: any`: key to search for in table entries

        - `return`: tuple with key hash, index and the first entry (entry may be `None`)
        """
        hash_ = hash(key)
        index = self._prober.probe(self._capacity, hash_, 0)
        entry = self._table[index]
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
        hash_, index, entry = self._find(key)
        parent = None
        node = entry
        while node is not None and key != node.key:
            parent = node
            node = node.next
        if node is None:
            if parent is None:
                self._table[index] = EntryNode(hash_, key, value)
            else:
                parent.next = EntryNode(hash_, key, value)
            self._length += 1
            return None
        else:
            old_value = node.value
            node.key, node.value = key, (value if replacer is None else replacer(value, node.value))
            return old_value

    def take(self, key: K) -> V:
        """
        Check base class.

        > complexity
        - time: `O(1) amortized`
        - space: `O(1) amortized`
        """
        if self._length / self._capacity < self._prober.load / 4:
            self._rebuild(False)
        _, index, entry = self._find(key)
        parent = None
        node = entry
        while node is not None and key != node.key:
            parent = node
            node = node.next
        if node is None:
            raise KeyError(f'key ({key}) not found')
        if parent is None:
            self._table[index] = node.next
        else:
            parent.next = node.next
        self._length -= 1
        return node.value

    def get(self, key: K) -> V:
        """
        Check base class.

        > complexity
        - time: `O(1) amortized`
        - space: `O(1) amortized`
        """
        _, _, entry = self._find(key)
        node = entry
        while node is not None and key != node.key:
            node = node.next
        if node is None:
            raise KeyError(f'key ({key}) not found')
        return node.value


def test():
    import random

    from ..test import match

    for prober_name in ('linear', 'prime', 'triangular'):
        hashtable = SequenceChainingHashtable[int, int](cast(Any, prober_name))
        match((
            *((hashtable.put, (str(i), i * 2), None) for i in random.sample([i for i in range(100)], 100)),
            (print, (hashtable,)),
            *((hashtable.take, (str(i),), i * 2) for i in random.sample([i for i in range(100)], 100) if i % 3 == 0),
            (print, (hashtable,)),
        ))


if __name__ == '__main__':
    test()
