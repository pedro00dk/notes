def sift_down(heap: list, i: int, length: int):
    """
    Heap sift down algorithm.
    Appart from the sift down in the heap.py module, this one uses direct numeric comparisons rathen than comparators
    and is max only.

    > complexity:
    - time: `O(log(n))`
    - space: `O(1)`

    > parameters:
    - `heap: (int | float)[]`: array containing heap structure
    - `i: int`: index of value to sift down
    - `length: int`: length of the heap (may be smaller than `len(heap)`)
    """
    while (left := i * 2 + 1) < length:
        right = left + 1
        chosen = i
        chosen = left if heap[left] > heap[chosen] else chosen
        chosen = right if right < length and heap[right] > heap[chosen] else chosen
        if chosen == i:
            break
        heap[i], heap[chosen] = heap[chosen], heap[i]
        i = chosen


def heapsort(array: list):
    """
    Heapsort implementation.

    > complexity:
    - time: `O(n*log(n))`
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted
    
    > `return: (int | float)[]`: `array` sorted
    """
    length = len(array)
    for i in range(length // 2 - 1, -1, -1):
        sift_down(array, i, length)
    for i in range(len(array) - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        sift_down(array, 0, i)
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark([('heapsort', heapsort)])


if __name__ == '__main__':
    test()
