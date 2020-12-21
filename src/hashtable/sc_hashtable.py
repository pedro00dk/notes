from typing import Any, Generator, Generic, Literal, Optional, cast

from .abc import Entry, Hashtable, T, U


class SCEntryNode(Generic[T, U], Entry[T, U]):
    """
    Entry with extra `next` property.
    """

    def __init__(self, hash_: int, key: T, value: U):
        super().__init__(hash_, key, value)
        self.next: Optional[SCEntryNode[T, U]] = None


class SCHashtable(Generic[T, U], Hashtable[T, U]):
    """
    Sequence chaining Hashtable implementation.
    Probers have minimal impact in sequence chaining performance, if probers produce the same index for `trie = 0`,
    the only change is the capacity and threshold limits. 
    """

    def __init__(self, prober_name: Literal['linear', 'prime', 'triangular'] = 'triangular'):
        """
        > parameters
        - `prober_name`: prober data
        """
        super().__init__(prober_name)
        self._table = cast(list[Optional[SCEntryNode[T, U]]], [None] * self._capacity)

    def _find(self, key: T) -> tuple[int, int, Optional[SCEntryNode[T, U]]]:
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

    def entries(self) -> Generator[tuple[T, U], None, None]:
        """
        Check abstract class for documentation.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        """
        for entry in self._table:
            cursor = entry
            while cursor is not None:
                yield (cursor.key, cursor.value)
                cursor = cursor.next

    def put(self, key: T, value: U):
        """
        Check abstract class for documentation.
        """
        if self._size / self._capacity >= self._prober.load:
            self._rebuild(True)
        hash_, index, entry = self._find(key)
        parent = None
        node = entry
        while node is not None and key != node.key:
            parent = node
            node = node.next
        if node is None:
            if parent is None:
                self._table[index] = SCEntryNode(hash_, key, value)
            else:
                parent.next = SCEntryNode(hash_, key, value)
            self._size += 1
        else:
            old_value = node.value
            node.key, node.value = key, value
            return old_value

    def take(self, key: T) -> U:
        """
        Check abstract class for documentation.
        """
        if self._size / self._capacity < self._prober.load / 4:
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
        self._size -= 1
        return node.value

    def get(self, key: T) -> U:
        """
        Check abstract class for documentation.
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
        hashtable = SCHashtable[int, int](cast(Any, prober_name))
        match((
            *((hashtable.put, (str(i), i * 2), None) for i in random.sample([i for i in range(100)], 100)),
            (print, (hashtable,)),
            *((hashtable.take, (str(i),), i * 2) for i in random.sample([i for i in range(100)], 100) if i % 3 == 0),
            (print, (hashtable,)),
        ))


if __name__ == '__main__':
    test()
