import random


def siftUp(heap, i, length, comparer):
    while (parent:= (i - 1) // 2) >= 0 and comparer(heap[i], heap[parent]):
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def siftDown(heap, i, length, comparer):
    while (left:= i * 2 + 1) < length:
        right = left + 1
        chosen = i
        chosen = left if left < length and comparer(heap[left], heap[chosen]) else chosen
        chosen = right if right < length and comparer(heap[right], heap[chosen]) else chosen
        if chosen == i:
            break
        heap[i], heap[chosen] = heap[chosen], heap[i]
        i = chosen


def heapifyTopDown(heap, length, comparer: lambda x, y: x > y):
    for i in range(0, length):
        siftUp(heap, i, length, comparer)


def heapifyBottomUp(heap, length, comparer: lambda x, y: x > y):
    for i in range(length // 2 - 1, -1, -1):
        siftDown(heap, i, length, comparer)


class Heap:
    def __init__(self, content=None, mode='max'):
        self.heap = content if content is not None else []
        self.comparer = (lambda x, y: x > y) if mode == 'max' else (lambda x, y: x < y)
        # heapifyTopDown(self.heap, len(self.heap), self.comparer)
        heapifyBottomUp(self.heap, len(self.heap), self.comparer)

    def __str__(self):
        return f'Heap {self.heap}'

    def offer(self, value):
        self.heap.append(value)
        siftUp(self.heap, len(self.heap) - 1, len(self.heap), self.comparer)

    def pool(self):
        if len(self.heap) == 0:
            raise IndexError('empty queue')
        chosen = self.heap[0]
        self.heap[0] = self.heap.pop()
        siftDown(self.heap, 0, len(self.heap), self.comparer)
        return chosen

    def peek(self):
        if len(self.heap) == 0:
            raise IndexError('empty queue')
        return self.heap[0]


def test():
    h = Heap(random.sample([i for i in range(10)], 10), mode='min')
    h.offer(10)
    h.offer(11)
    h.offer(12)
    h.offer(13)
    h.offer(14)
    h.offer(15)
    print(h)
    print(h.pool())
    print(h.pool())
    print(h)
    print(h.pool())
    print(h.pool())
    print(h.pool())
    print(h)
    print(h.pool())
    print(h.pool())
    print(h.pool())
    print(h.pool())
    print(h)


if __name__ == '__main__':
    test()
