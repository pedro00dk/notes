import enum

from .abc import Entry, Hashtable, Prober


class OAEntry(Entry):
    """
    Entry with extra `deleted` property.
    """

    def __init__(self, hash_: int, key, /, value=None):
        super().__init__(hash_, key, value)
        self.deleted = False


class OAHashtable(Hashtable):
    """
    Open Addressing Hashtable implementation.
    """

    def _find(self, key, /, free=True):
        """
        Suport function for hashtable operations.
        This function looks for indices and entries in the hashtable.
        It stops if:
        - `None` is found (free for insertion, not exists for deletion)
        - `free` is `True` and `entry.deleted` is `True` (free for insertion, not exists for deletion)
        - `free` is `False` and `entry.deleted` is `False` and `hash` equals (not free for insertion, deletion allowed)

        > parameters:
        - `key: any`: key to search for in table entries
        - `free: bool? = True`: if should stop if entry with deleted flag set is found

        > `return: (int, int, OAEntry)`: tuple with key hash, index and entry (entry may be `None`)
        """
        hash_ = hash(key)
        for trie in range(self._capacity):
            index = self._probe(self._capacity, hash_, trie)
            entry = self._table[index]
            if entry is None or \
                    free and entry.deleted or \
                    not entry.deleted and entry.hash_ == hash_ and entry.key == key:
                break
        return hash_, index, entry

    def entries(self):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`
        """
        return ((entry.key, entry.value) for entry in self._table if entry is not None and not entry.deleted)

    def put(self, key, /, value=None):
        """
        Check abstract class for documentation.
        """
        if self._size / self._capacity >= self._load_threshold:
            self._rebuild()
        hash_, index, entry = self._find(key, True)
        if entry is None or entry.deleted:
            self._size += 1
        self._table[index] = OAEntry(hash_, key, value)

    def take(self, key):
        hash_, index, entry = self._find(key, False)
        if entry is None:
            raise KeyError(f'key ({str(key)}) not found')
        value = entry.value
        entry.deleted = True
        entry.key = entry.value = None
        self._size -= 1
        return value

    def get(self, key):
        hash_, index, entry = self._find(key, False)
        if entry is None:
            raise KeyError(f'key ({str(key)}) not found')
        return entry.value


def test():
    import random
    from ..test import match
    for prober in Prober:
        h = OAHashtable(prober)
        match([
            *((h.put, [str(i), i * 2], None) for i in random.sample([i for i in range(100)], 100)),
            (print, [h], None),
            *((h.take, [str(i)], i * 2) for i in random.sample([i for i in range(100)], 100) if i % 3 == 0),
            (print, [h], None)
        ])


if __name__ == '__main__':
    test()
