def sift_down(heap: list, i: int, length: int):
    """
    Heap sift down algorithm.
    Appart from the sift down in the heap.py module, this one uses direct numeric comparisons rathen than comparators
    and is max only.

    > complexity:
    - time: `O(log(n))`
    - space: `O(1)`

    > parameters:
    - `heap: list`: array containing heap structure
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
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    length = len(array)
    for i in range(length // 2 - 1, -1, -1):
        sift_down(array, i, length)
    for i in range(len(array) - 1, 0, -1):
        array[0], array[i] = array[i], array[0]
        sift_down(array, 0, i)
    return array


def test():
    from random import randint
    from timeit import repeat
    print(heapsort([]))
    print(heapsort([0]))
    print(heapsort([*range(20)]))
    print(heapsort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000]:
        results = repeat(
            'heapsort(array)',
            setup='array=[randint(0, i**2) for j in range(i)]',
            globals={**globals(), **locals()},
            number=1,
            repeat=100
        )
        print('array length:', i, sum(results))



if __name__ == '__main__':
    test()
