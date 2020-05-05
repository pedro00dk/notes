def siftDown(heap, i, length):
    while (left:= i * 2 + 1) < length:
        right = left + 1
        chosen = i
        chosen = left if left < length and heap[left] > heap[chosen] else chosen
        chosen = right if right < length and heap[right] > heap[chosen] else chosen
        if chosen == i:
            break
        heap[i], heap[chosen] = heap[chosen], heap[i]
        i = chosen


def heapsort(array):
    length = len(array)
    for i in range(length // 2 - 1, -1, -1):
        siftDown(array, i, length)
    for i in range(len(array) - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        siftDown(array, 0, i)
    return array


def test():
    from ..util import benchmark
    print(heapsort([]))
    print(heapsort([0]))
    print(heapsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(heapsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    benchmark(heapsort)


if __name__ == '__main__':
    test()
