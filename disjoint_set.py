from hashtable import Hashtable


class DisjointSet:
    def __init__(self, size=0):
        self.sets = [i for i in range(size)]
        self.ranks = [0 for i in range(size)]

    def __str__(self):
        lines = '\n'.join([f'{i} -> {self.sets[i]} # {self.ranks[i]}' for i in range(len(self.sets))])
        return f'Disjoint Set [\n{lines}\n]'

    def make_set(self):
        key = len(self.sets)
        self.sets.append(key)
        self.ranks.append(0)
        return key

    def find(self, key, compress=True):
        if key < 0 or key >= len(self.sets):
            raise KeyError('not found')
        while key != self.sets[key]:
            if compress:
                self.sets[key] = self.sets[self.sets[key]]
            key = self.sets[key]
        return key

    def union(self, key_a, key_b):
        key_a = self.find(key_a)
        key_b = self.find(key_b)
        if key_a == key_b:
            return
        if self.ranks[key_a] < self.ranks[key_b]:
            key_a, key_b = key_b, key_a
        self.sets[key_b] = key_a
        if self.ranks[key_a] == self.ranks[key_b]:
            self.ranks[key_a] += 1
        return key_a

    def compress(self):
        for i in range(len(self.sets)):
            self.find(i)
            self.ranks[i] = 0



class HashDisjointSet:
    def __init__(self):
        super().__init__()
        self.disjoint_set = DisjointSet()
        self.key_map = Hashtable()

    def __str__(self):
        return f'Hash Disjoint Set {{\n{str(self.disjoint_set)}\n{str(self.key_map)}\n}}'

    def make_set(self, key):
        try:
            self.key_map.get(key)
        except:
            self.key_map.put(key, self.disjoint_set.make_set())
        return key

    def find(self, key, compress=True):
        return self.disjoint_set.find(self.key_map.get(key), compress)

    def union(self, key_a, key_b):
        return self.disjoint_set.union(self.key_map.get(key_a), self.key_map.get(key_b))
    
    def compress(self):
        self.disjoint_set.compress()


def test():
    d = HashDisjointSet()
    d.make_set('a')
    d.make_set('e')
    d.make_set('i')
    d.make_set('o')
    d.make_set('u')
    d.make_set('0')
    d.make_set('1')
    d.make_set('2')
    d.make_set('3')
    d.make_set('4')
    print(d)
    d.union('a', 'e')
    d.union('i', 'o')
    d.union('a', 'o')
    d.union('u', 'a')
    d.union('0', '1')
    d.union('2', '3')
    d.union('4', '0')
    d.union('1', '2')
    print(d)
    d.compress()
    print(d)


if __name__ == "__main__":
    test()
