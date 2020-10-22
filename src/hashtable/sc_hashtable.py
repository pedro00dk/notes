from .abc import Entry, Hashtable, Prober


class SCEntryNode(Entry):
    """
    Entry with extra `next` property.
    """

    def __init__(self, hash_: int, key, /, value=None):
        super().__init__(hash_, key, value)
        self.next = None


class SCHashtable(Hashtable):
    """
    Sequence chaining Hashtable implementation.
    Probers have minimal impact in sequence chaining performance, if probers produce the same index for `trie = 0`,
    the only change is the capacity and threshold limits. 
    """

    def _find(self, key):
        """
        Suport function for hashtable operations.
        This function looks for indices and entries in the hashtable.

        > parameters:
        - `key: any`: key to search for in table entries

        > `return: (int, int, SCEntryNode)`: tuple with key hash, index and the first entry (entry may be `None`)
        """
        hash_ = hash(key)
        index = self._probe(self._capacity, hash_, 0)
        entry = self._table[index]
        return hash_, index, entry

    def entries(self):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`
        """
        for entry in self._table:
            cursor = entry
            while cursor is not None:
                yield (cursor.key, cursor.value)
                cursor = cursor.next

    def put(self, key, /, value=None):
        """
        Check abstract class for documentation.
        """
        if self._size / self._capacity >= self._load_threshold:
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

    def take(self, key):
        """
        Check abstract class for documentation.
        """
        if self._size / self._capacity < self._load_threshold / 4:
            self._rebuild(False)
        hash_, index, entry = self._find(key)
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

    def get(self, key):
        """
        Check abstract class for documentation.
        """
        hash_, index, entry = self._find(key)
        node = entry
        while node is not None and key != node.key:
            node = node.next
        if node is None:
            raise KeyError(f'key ({key}) not found')
        return node.value


def test():
    import random
    from ..test import match
    for prober in Prober:
        h = SCHashtable(prober)
        match([
            *((h.put, (str(i), i * 2), None) for i in random.sample([i for i in range(100)], 100)),
            (print, (h,)),
            *((h.take, (str(i),), i * 2) for i in random.sample([i for i in range(100)], 100) if i % 3 == 0),
            (print, (h,))
        ])


if __name__ == '__main__':
    test()
