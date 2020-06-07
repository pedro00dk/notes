import math


def binary_search(array: list, key, /, comparator=lambda a, b: a - b):
    """
    Binary search algorithm.
    Require `array` to be sorted based on `comparator`

    > complexity:
    - time: `O(log(n))`
    - space: `O(1)`

    > parameters:
    - `array: <T>[]`: array to search `key`
    - `key: <T>`: key to be search in `array`
    - `comparator: (<T>, <T>) -> int`: comparator for `<T>` type values

    > `return: int`: index of `key` in `array`
    """
    left = 0
    right = len(array) - 1
    while left <= right:
        center = (left + right) // 2
        comparison = comparator(key, array[center])
        if comparison < 0:
            right = center - 1
        elif comparison > 0:
            left = center + 1
        else:
            return center
    raise KeyError(f'key ({key}) not found')


def k_ary_search(array, key, /, k=4, comparator=(lambda a, b: a - b)):
    """
    K-ary search algorithm.
    Require `array` to be sorted based on `comparator`

    > complexity:
    - time: `O(k*log(n,k))`
    - space: `O(1)`

    > parameters:
    - `array: <T>[]`: array to search `key`
    - `key: <T>`: key to be search in `array`
    - `k: int? = 2`: number of buckets to subdivide search
    - `comparator: ((<T>, <T>) -> int)? = lambda a, b: a - b`: comparator for `<T>` type values

    > `return: int`: index of `key` in `array`
    """
    left = 0
    right = len(array) - 1
    k = max(k, 2)
    while left <= right:
        step = (right - left) / k
        for i in range(k):
            center = left + round(step * (i + 1))
            comparison = comparator(key, array[center])
            if comparison < 0:
                left = left + round(step * i)
                right = center - 1
                break
            elif comparison > 0:
                left = center + 1
                right = left + round(step * (i + 2))
                break
            else:
                return center
    raise KeyError(f'key ({key}) not found')


def test():
    from ..test import match
    match([
        (binary_search, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6], 6),
        (binary_search, [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8], 4),
        (binary_search, [[1, 10, 100, 1000, 10000, 100000, 1000000], 10], 1),
        (k_ary_search, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6, 4], 6),
        (k_ary_search, [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8, 8], 4),
        (k_ary_search, [[1, 10, 100, 1000, 10000, 100000, 1000000], 10, 16], 1)
    ])


if __name__ == '__main__':
    test()
