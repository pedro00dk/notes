from typing import Any, Generator, Generic, Literal, Optional, cast

from .abc import Entry, Hashtable, T, U


class OAEntry(Generic[T, U], Entry[T, U]):
    """
    Entry with extra `deleted` property.
    """

    def __init__(self, hash_: int, key: T, value: U):
        super().__init__(hash_, key, value)
        self.deleted = False


class OAHashtable(Generic[T, U], Hashtable[T, U]):
    """
    Open Addressing Hashtable implementation.
    """

    def __init__(self, prober_name: Literal['linear', 'prime', 'triangular'] = 'triangular'):
        """
        > parameters
        - `prober_name`: prober data
        """
        super().__init__(prober_name)
        self._table = cast(list[Optional[OAEntry[T, U]]], [None] * self._capacity)

    def _find(self, key: T, free: bool = True) -> tuple[int, int, Optional[OAEntry[T, U]]]:
        """
        Suport function for hashtable operations.
        This function looks for indices and entries in the hashtable.
        It stops if:
        - `None` is found (free for insertion, not exists for deletion)
        - `free` is `True` and `entry.deleted` is `True` (free for insertion, not exists for deletion)
        - `free` is `False` and `entry.deleted` is `False` and `hash` equals (not free for insertion, deletion allowed)

        > parameters
        - `key`: key to search for in table entries
        - `free`: if should stop if entry with deleted flag set is found
        - `return`: tuple with key hash, index and entry (entry may be `None`)
        """
        hash_ = hash(key)
        index = 0
        entry: Optional[OAEntry[T, U]] = None
        for trie in range(self._capacity):
            index = self._prober.probe(self._capacity, hash_, trie)
            entry = self._table[index]
            if entry is None or \
                    free and entry.deleted or \
                    not entry.deleted and entry.hash_ == hash_ and entry.key == key:
                break
        return hash_, index, entry

    def entries(self) -> Generator[tuple[T, U], None, None]:
        """
        Check abstract class for documentation.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        """
        return ((entry.key, entry.value) for entry in self._table if entry is not None and not entry.deleted)

    def put(self, key: T, value: U):
        """
        Check abstract class for documentation.
        """
        if self._size / self._capacity >= self._prober.load:
            self._rebuild(True)
        hash_, index, entry = self._find(key, True)
        if entry is None or entry.deleted:
            self._size += 1
        self._table[index] = OAEntry(hash_, key, value)

    def take(self, key: T) -> U:
        if self._size / self._capacity < self._prober.load / 4:
            self._rebuild(False)
        _, _, entry = self._find(key, False)
        if entry is None:
            raise KeyError(f'key ({key}) not found')
        value = entry.value
        entry.deleted = True
        del entry.key
        del entry.value
        self._size -= 1
        return value

    def get(self, key: T) -> U:
        _, _, entry = self._find(key, False)
        if entry is None:
            raise KeyError(f'key ({key}) not found')
        return entry.value


def test():
    import random

    from ..test import match

    for prober_name in ('linear', 'prime', 'triangular'):
        hashtable = OAHashtable[int, int](cast(Any, prober_name))
        match((
            *((hashtable.put, (str(i), i * 2), None) for i in random.sample([i for i in range(100)], 100)),
            (print, (hashtable,)),
            *((hashtable.take, (str(i),), i * 2) for i in random.sample([i for i in range(100)], 100) if i % 3 == 0),
            (print, (hashtable,)),
        ))


if __name__ == '__main__':
    test()
