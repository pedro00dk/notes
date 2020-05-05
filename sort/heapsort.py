from heap import heapifyBottomUp, siftDown
import tester


def heapsort(array):
    comparer = lambda x, y: x > y
    heapifyBottomUp(array, len(array), comparer)
    for i in range(len(array) - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        siftDown(array, 0, i, comparer)
    return array


def test():
    print(heapsort([]))
    print(heapsort([0]))
    print(heapsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(heapsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    tester.test_sort(heapsort)


if __name__ == '__main__':
    test()
