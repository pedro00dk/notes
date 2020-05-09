class Heap:
    def __init__(self, content=None, mode='max'):
        self._heap = content if content is not None else []
        self.comparer = (lambda x, y: x > y) if mode == 'max' else (lambda x, y: x < y) if mode == 'min' else mode
        # self._heapifyTopDown(len(self._heap))
        self._heapify_bottom_up(len(self._heap))

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return f'Heap {self._heap}'

    def _sift_up(self, i, length):
        while (parent:= (i - 1) // 2) >= 0 and self.comparer(self._heap[i], self._heap[parent]):
            self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
            i = parent

    def _sift_down(self, i, length):
        while (left:= i * 2 + 1) < length:
            right = left + 1
            chosen = i
            chosen = left if left < length and self.comparer(self._heap[left], self._heap[chosen]) else chosen
            chosen = right if right < length and self.comparer(self._heap[right], self._heap[chosen]) else chosen
            if chosen == i:
                break
            self._heap[i], self._heap[chosen] = self._heap[chosen], self._heap[i]
            i = chosen

    def _heapify_top_down(self, length):
        for i in range(0, length):
            self._sift_up(i, length)

    def _heapify_bottom_up(self, length):
        for i in range(length // 2 - 1, -1, -1):
            self._sift_down(i, length)

    def offer(self, value):
        self._heap.append(value)
        self._sift_up(len(self._heap) - 1, len(self._heap))

    def poll(self):
        if len(self._heap) == 0:
            raise IndexError('empty queue')
        chosen = self._heap[0]
        replacement = self._heap.pop()
        if len(self._heap) > 0:
            self._heap[0] = replacement
        self._sift_down(0, len(self._heap))
        return chosen

    def peek(self):
        if len(self._heap) == 0:
            raise IndexError('empty queue')
        return self._heap[0]


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
