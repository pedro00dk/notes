class DisjointSet:
    """
    Disjoint Set implementation.
    """

    def __init__(self, /, sets=0):
        """
        > complexity:
        - time: `O(n)`
        - space: `O(n)`

        > parameters:
        - `sets: int? = 0`: number of initial sets
        """
        self._sets = [i for i in range(sets)]
        self._ranks = [0] * sets
        self._sizes = [1] * sets
        self._count = sets

    def __len__(self):
        return len(self._sets)

    def __str__(self):
        lines = '\n'.join(
            [f'{i} => {self._sets[i]} # rank: {self._ranks[i]} size: {self._sizes[i]}' for i in range(len(self._sets))]
        )
        return f'DisjointSet [\n{lines}\n]'

    def sets(self):
        """
        Return the number of disjoint sets.

        > `return: int`: number of sets
        """
        return self._count

    def set_size(self, key: int):
        """
        Return the size of the set containing `key`

        > parameters:
        - `key: int`: key of a set

        > `return: int`: size of set containing `key`
        """
        return self._sizes[self.find(key)]

    def make_set(self):
        """
        Create a new set with a single key.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > `return: int`: a new key of the created set
        """
        key = len(self._sets)
        self._sets.append(key)
        self._ranks.append(0)
        self._sizes.append(1)
        self._count += 1
        return key

    def find(self, key: int):
        """
        Find the root key of a set containing `key`.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `key: int`: key of a set

        > `return: int`: root key of the set containing `key`
        """
        if key < 0 or key >= len(self._sets):
            raise KeyError(f'key ({key}) out of range [0, {self._size})')
        root = key
        while root != self._sets[root]:
            root = self._sets[root]
        while key != self._sets[key]:
            key, self._sets[key] = self._sets[key], root
        return root

    def union(self, key_a: int, key_b: int):
        """
        Join sets that contain `key_a` and `key_b` in a single set.
        The hashtable store sizes and ranks, but only ranks are used to decide how to join sets.
        Size is only used to get sizes of sets.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `key_a: int`: key of a set
        - `key_b: int`: key of a set
        """
        key_a = self.find(key_a)
        key_b = self.find(key_b)
        if key_a == key_b:
            return
        if self._ranks[key_a] < self._ranks[key_b]:
            key_a, key_b = key_b, key_a
        self._sets[key_b] = key_a
        self._ranks[key_a] += 1 if self._ranks[key_a] == self._ranks[key_b] else 0
        self._sizes[key_a] += self._sizes[key_b]
        self._count -= 1

    def connected(self, key_a: int, key_b: int):
        """
        Return `True` if `key_a` and `key_b` are in the same set.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `key_a: int`: key of a set
        - `key_b: int`: key of a set

        > `return: bool`: if `key_a` and `key_b` are connected
        """
        return self.find(key_a) == self.find(key_b)


class HashDisjointSet:
    """
    Disjoint Set implementation with support for any type of key (keys must be provided).
    Assuming hashtable constant time operations, disjoint set operations have the same time and space complexity.
    """

    def __init__(self):
        self._table = {}
        self._disjoint_set = DisjointSet()
        self.sets = self._disjoint_set.sets

    def __len__(self):
        return len(self._disjoint_set)

    def __str__(self):
        return f'Hash Disjoint Set {{\n{self._disjoint_set}\n{self._table}\n}}'

    def set_size(self, key):
        return self._disjoint_set.set_size(self._table[key])

    def make_set(self, key):
        try:
            return self._table[key]
        except:
            inner_key = self._disjoint_set.make_set()
            self._table[key] = inner_key
            return inner_key

    def find(self, key):
        return self._disjoint_set.find(self._table[key])

    def union(self, key_a, key_b):
        return self._disjoint_set.union(self._table[key_a], self._table[key_b])

    def connected(self, key_a, key_b):
        return self._disjoint_set.connected(self._table[key_a], self._table[key_b])


def test():
    from .test import match
    d = HashDisjointSet()
    match([
        (d.make_set, ('a',)),
        (d.make_set, ('e',)),
        (d.make_set, ('i',)),
        (d.make_set, ('o',)),
        (d.make_set, ('u',)),
        (d.make_set, ('0',)),
        (d.make_set, ('1',)),
        (d.make_set, ('2',)),
        (d.make_set, ('3',)),
        (d.make_set, ('4',)),
        (print, (d,)),
        (d.union, ('a', 'e')),
        (d.union, ('i', 'o')),
        (d.union, ('a', 'o')),
        (d.union, ('u', 'a')),
        (d.union, ('0', '1')),
        (d.union, ('2', '3')),
        (d.union, ('4', '0')),
        (d.union, ('1', '2')),
        (print, (d,)),
        (d.connected, ('a', 'i'), True),
        (d.connected, ('e', 'o'), True),
        (d.connected, ('e', 'u'), True),
        (d.connected, ('3', 'u'), False),
        (d.connected, ('0', 'e'), False),
        (d.connected, ('1', '4'), True),
        (d.connected, ('1', '2'), True),
        (d.connected, ('2', '0'), True),
        (d.connected, ('i', '4'), False),
        (d.connected, ('u', '1'), False),
        (len, (d,), 10),
        (d.sets, (), 2),
        (d.set_size, ('a',), 5),
        (d.set_size, ('0',), 5)
    ])


if __name__ == '__main__':
    test()
