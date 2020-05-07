class Heap:
    def __init__(self, content=None, mode='max'):
        self.heap = content if content is not None else []
        self.comparer = (lambda x, y: x > y) if mode == 'max' else (lambda x, y: x < y)
        # self.heapifyTopDown(len(self.heap))
        self.heapifyBottomUp(len(self.heap))

    def __str__(self):
        return f'Heap {self.heap}'

    def _siftUp(self, i, length):
        while (parent:= (i - 1) // 2) >= 0 and self.comparer(self.heap[i], self.heap[parent]):
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent

    def _siftDown(self, i, length):
        while (left:= i * 2 + 1) < length:
            right = left + 1
            chosen = i
            chosen = left if left < length and self.comparer(self.heap[left], self.heap[chosen]) else chosen
            chosen = right if right < length and self.comparer(self.heap[right], self.heap[chosen]) else chosen
            if chosen == i:
                break
            self.heap[i], self.heap[chosen] = self.heap[chosen], self.heap[i]
            i = chosen

    def heapifyTopDown(self, length):
        for i in range(0, length):
            self._siftUp(i, length)

    def heapifyBottomUp(self, length):
        for i in range(length // 2 - 1, -1, -1):
            self._siftDown(i, length)

    def offer(self, value):
        self.heap.append(value)
        self._siftUp(len(self.heap) - 1, len(self.heap))

    def poll(self):
        if len(self.heap) == 0:
            raise IndexError('empty queue')
        chosen = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._siftDown(0, len(self.heap))
        return chosen

    def peek(self):
        if len(self.heap) == 0:
            raise IndexError('empty queue')
        return self.heap[0]


def test():
    import random
    from ..util import match
    h = Heap(random.sample([i for i in range(10)], 10), mode='min')
    match([
        (print, [h], None),
        (h.offer, [10], None),
        (h.offer, [11], None),
        (h.offer, [12], None),
        (h.offer, [13], None),
        (h.offer, [14], None),
        (h.offer, [15], None),
        (print, [h], None),
        (h.poll, [], 0),
        (h.poll, [], 1),
        (print, [h], None),
        (h.poll, [], 2),
        (h.poll, [], 3),
        (h.poll, [], 4),
        (print, [h], None),
        (h.poll, [], 5),
        (h.poll, [], 6),
        (h.poll, [], 7),
        (h.poll, [], 8),
        (print, [h], None)
    ])


if __name__ == '__main__':
    test()
