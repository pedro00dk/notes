import itertools
import random


class Hashtable:
    LOAD_THRESHOLD = 0.5

    def __init__(self):
        self.size = 0
        self.capacity = 11
        self.table = [None] * self.capacity

    def __str__(self):
        lines = '\n'.join(f'k: {e.key}, v: {e.value}' for e in self.table if e is not None and not e.deleted)
        return f'Hashtable [\n{lines}\n]'

    def _rebuild(self):
        previous_table = self.table
        self.size = 0
        self.capacity = self.capacity * 2 + 1
        self.table = [None] * self.capacity
        for entry in previous_table:
            if entry is None or entry.deleted:
                continue
            self.put(entry.key, entry.value)

    def _probe(self, hash, index):
        return (hash + index ** 2) % self.capacity

    def put(self, key, value=None):
        if self.size / self.capacity > Hashtable.LOAD_THRESHOLD:
            self._rebuild()
        hash_ = hash(key)
        for i, index in enumerate(map(lambda i: self._probe(hash_, i), itertools.count())):
            entry = self.table[index]
            if entry is None or entry.deleted or entry.hash_ == hash_ and entry.key == key:
                break
        if entry is None or entry.deleted:
            self.size += 1
        self.table[index] = Entry(hash_, False, key, value)

    def delete(self, key):
        hash_ = hash(key)
        for index in map(lambda i: self._probe(hash_, i), itertools.count()):
            entry = self.table[index]
            if entry is None or not entry.deleted and entry.hash_ == hash_ and entry.key == key:
                break
        if entry is None:
            raise KeyError('not found')
        value = entry.value
        entry.hash_ = None
        entry.deleted = True
        entry.key = None
        entry.value = None
        self.size -= 1
        return value

    def get(self, key):
        hash_ = hash(key)
        for index in map(lambda i: self._probe(hash_, i), itertools.count()):
            entry = self.table[index]
            if entry is None or not entry.deleted and entry.hash_ == hash_ and entry.key == key:
                break
        if entry is None:
            raise KeyError('not found')
        return entry.value


class Entry:
    def __init__(self, hash_, deleted, key, value=None):
        self.hash_ = hash_
        self.deleted = deleted
        self.key = key
        self.value = value


def test():
    h = Hashtable()
    for i in random.sample([i for i in range(100)], 100):
        h.put(i, i)
    print(h)
    for i in random.sample([i * 2 for i in range(50)], 50):
        h.delete(i)
    print(h)


if __name__ == '__main__':
    test()
