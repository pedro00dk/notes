from typing import Generic, TypeVar

T = TypeVar('T')


class DisjointSet:
    """
    Disjoint Set implementation.

    > complexity
    - space: `O(n)`
    - `n`: number of starting sets plus created sets
    """

    def __init__(self, sets: int = 0):
        """
        > complexity
        - time: `O(n)`
        - space: `O(n)`
        - `n`: absolute value of `sets`

        > parameters
        - `sets`: number of initial sets
        """
        self._sets = [i for i in range(sets)]
        self._ranks = [0] * sets
        self._sizes = [1] * sets
        self._count = sets

    def __str__(self) -> str:
        lines = '\n'.join(
            f'{i} => {self._sets[i]} # rank: {self._ranks[i]} size: {self._sizes[i]}' for i in range(len(self._sets))
        )
        return f'DisjointSet [\n{lines}\n]'

    def __len__(self) -> int:
        return len(self._sets)

    def sets(self) -> int:
        """
        Return the number of disjoint sets.

        - `return`: number of sets
        """
        return self._count

    def set_size(self, key: int) -> int:
        """
        Return the size of the set containing `key`

        > parameters
        - `key`: key of a set

        - `return`: size of set containing `key`
        """
        return self._sizes[self.find(key)]

    def make_set(self) -> int:
        """
        Create a new set with a single key.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        - `return`: a new key of the created set
        """
        key = len(self._sets)
        self._sets.append(key)
        self._ranks.append(0)
        self._sizes.append(1)
        self._count += 1
        return key

    def find(self, key: int) -> int:
        """
        Find the root key of a set containing `key`.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `key`: key of a set
        - `return`: root key of the set containing `key`
        """
        if key < 0 or key >= len(self._sets):
            raise KeyError(f'key ({key}) out of range [0, {len(self._sets)})')
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

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
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

    def connected(self, key_a: int, key_b: int) -> bool:
        """
        Return `True` if `key_a` and `key_b` are in the same set.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `key_a: int`: key of a set
        - `key_b: int`: key of a set

        - `return`: if `key_a` and `key_b` are connected
        """
        return self.find(key_a) == self.find(key_b)


class HashDisjointSet(Generic[T]):
    """
    Disjoint Set implementation with support for any type of key (keys must be provided).
    Assuming hashtable constant time operations, disjoint set operations have the same time and space complexity.
    """

    def __init__(self):
        self._table: dict[T, int] = {}
        self._disjoint_set = DisjointSet()
        self.sets = self._disjoint_set.sets

    def __str__(self) -> str:
        return f'Hash Disjoint Set {{\n{self._disjoint_set}\n{self._table}\n}}'

    def __len__(self) -> int:
        return len(self._disjoint_set)

    def set_size(self, key: T) -> int:
        return self._disjoint_set.set_size(self._table[key])

    def make_set(self, key: T) -> int:
        try:
            return self._table[key]
        except:
            inner_key = self._disjoint_set.make_set()
            self._table[key] = inner_key
            return inner_key

    def find(self, key: T) -> int:
        return self._disjoint_set.find(self._table[key])

    def union(self, key_a: T, key_b: T):
        self._disjoint_set.union(self._table[key_a], self._table[key_b])

    def connected(self, key_a: T, key_b: T) -> bool:
        return self._disjoint_set.connected(self._table[key_a], self._table[key_b])


def test():
    from .test import match

    disjoint_set = HashDisjointSet['str']()
    match((
        (disjoint_set.make_set, ('a',)),
        (disjoint_set.make_set, ('e',)),
        (disjoint_set.make_set, ('i',)),
        (disjoint_set.make_set, ('o',)),
        (disjoint_set.make_set, ('u',)),
        (disjoint_set.make_set, ('0',)),
        (disjoint_set.make_set, ('1',)),
        (disjoint_set.make_set, ('2',)),
        (disjoint_set.make_set, ('3',)),
        (disjoint_set.make_set, ('4',)),
        (print, (disjoint_set,)),
        (disjoint_set.union, ('a', 'e')),
        (disjoint_set.union, ('i', 'o')),
        (disjoint_set.union, ('a', 'o')),
        (disjoint_set.union, ('u', 'a')),
        (disjoint_set.union, ('0', '1')),
        (disjoint_set.union, ('2', '3')),
        (disjoint_set.union, ('4', '0')),
        (disjoint_set.union, ('1', '2')),
        (print, (disjoint_set,)),
        (disjoint_set.connected, ('a', 'i'), True),
        (disjoint_set.connected, ('e', 'o'), True),
        (disjoint_set.connected, ('e', 'u'), True),
        (disjoint_set.connected, ('3', 'u'), False),
        (disjoint_set.connected, ('0', 'e'), False),
        (disjoint_set.connected, ('1', '4'), True),
        (disjoint_set.connected, ('1', '2'), True),
        (disjoint_set.connected, ('2', '0'), True),
        (disjoint_set.connected, ('i', '4'), False),
        (disjoint_set.connected, ('u', '1'), False),
        (len, (disjoint_set,), 10),
        (disjoint_set.sets, (), 2),
        (disjoint_set.set_size, ('a',), 5),
        (disjoint_set.set_size, ('0',), 5),
    ))


if __name__ == '__main__':
    test()
