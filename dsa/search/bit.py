class BIT:
    def __init__(self, array):
        self._tree = [0] + array
        self._build()

    def __len__(self):
        return len(self._tree) - 1

    def __str__(self):
        return f'BIT {self._tree}'

    def _lsb(self, index):
        return index & -index

    def _build(self):
        for index in range(1, len(self._tree)):
            if (parent:= index + self._lsb(index)) < len(self._tree):
                self._tree[parent] += self._tree[index]

    def _prefix_sum(self, index):
        acc = 0
        while index > 0:
            acc += self._tree[index]
            index -= self._lsb(index)
        return acc

    def add(self, index, value):
        # index parameter is zero based
        index += 1
        while index < len(self._tree):
            self._tree[index] += value
            index += self._lsb(index)

    def set(self, index, value):
        # index parameter is zero based
        current = self.sum(index, index)
        self.add(index, value - current)

    def sum(self, i, j):
        # index parameters are zero based
        if (i > j or j >= len(self._tree)):
            raise IndexError('illegal index')
        return self._prefix_sum(j + 1) - self._prefix_sum(i)


def test():
    from ..util import match
    bit = BIT([3, 4, -2, 7, 3, 11, 5, -8, -9, 2, 4, -8])
    match([
        (print, [bit], None),
        (bit.sum, [0, 1], 7),
        (bit.sum, [0, 2], 5),
        (bit.sum, [5, 7], 8),
        (bit.sum, [8, 10], -3),
        (bit.sum, [11, 11], -8),
        (print, [bit], None),
        (bit.add, [0, 10], None),
        (bit.set, [5, -10], None),
        (bit.add, [10, 10], None),
        (print, [bit], None),
        (bit.sum, [0, 1], 17),
        (bit.sum, [0, 2], 15),
        (bit.sum, [5, 7], -13),
        (bit.sum, [8, 10], 7),
        (bit.sum, [11, 11], -8)
    ])


if __name__ == '__main__':
    test()
