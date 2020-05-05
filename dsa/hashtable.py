import itertools


class Hashtable:
    def __init__(self, load_threshold=0.75, quadratic=True):
        self.capacity = 8
        self.size = 0
        self.table = [None] * self.capacity
        self.load_threshold = load_threshold
        self.quadratic = quadratic

    def __str__(self):
        lines = '\n'.join(f'k: {e.key}, v: {e.value}' for e in self.table if e is not None and not e.deleted)
        return f'Hashtable [\n{lines}\n]'

    def __len__(self):
        return self.size

    def _rebuild(self):
        previous_table = self.table
        self.size = 0
        self.capacity = self.capacity * 2
        self.table = [None] * self.capacity
        for entry in previous_table:
            if entry is None or entry.deleted:
                continue
            self.put(entry.key, entry.value)

    def _probe_linear(self, hash_, index, const=1):
        # works with greatest common divisor of capacity and const must be 1 for complete cycle
        return (hash_ + index * const) % self.capacity

    def _probe_quadratic_power(self, hash_, index):
        # capacity must be power of two for complete cycle
        return (hash_ + (index ** 2 + index) // 2) % self.capacity

    def _probe_quadratic_prime(self, hash_, index):
        # capacity must be prime > 3 and load_factor <= 0.5, complete cycle never garanteed
        return (hash_ + index ** 2) % self.capacity

    def put(self, key, value=None):
        if self.size / self.capacity > self.load_threshold:
            self._rebuild()
        probe = self._probe_quadratic_power if self.quadratic else self._probe_linear
        hash_ = hash(key)
        for i in range(self.capacity):
            index = probe(hash_, i)
            entry = self.table[index]
            if entry is None or entry.deleted or entry.hash_ == hash_ and entry.key == key:
                break
        if entry is None or entry.deleted:
            self.size += 1
        self.table[index] = Entry(hash_, False, key, value)

    def delete(self, key):
        probe = self._probe_quadratic_power if self.quadratic else self._probe_linear
        hash_ = hash(key)
        for i in range(self.capacity):
            index = probe(hash_, i)
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
        probe = self._probe_quadratic_power if self.quadratic else self._probe_linear
        hash_ = hash(key)
        for i in range(self.capacity):
            index = probe(hash_, i)
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
    import random
    from .util import match
    h = Hashtable()
    match([
        *((h.put, [i, i * 2], None) for i in random.sample([i for i in range(100)], 100)),
        (print, [h], None),
        *((h.delete, [i], i * 2) for i in random.sample([i for i in range(100)], 100) if i % 3 == 0),
        (print, [h], None)
    ])


if __name__ == '__main__':
    test()
