import random
from heap import heapifyBottomUp, siftDown


def heapsort(l):
    comparer = lambda x, y: x > y
    heapifyBottomUp(l, len(l), comparer)
    for i in range(len(l) - 1, 0, -1):
        l[0], l[i] = l[i], l[0]
        siftDown(l, 0, i, comparer)
    return l


def test():
    print(heapsort([]))
    print(heapsort([0]))
    print(heapsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(heapsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    print(heapsort(random.sample([i for i in range(10)], 10)))


if __name__ == "__main__":
    test()
