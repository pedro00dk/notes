import math


def binary_search(array: list, key, /, comparator=lambda a, b: a - b, left: int = None, right: int = None):
    """
    Binary search algorithm.
    Require `array` to be sorted based on `comparator`.

    > complexity:
    - time: `O(log(n))`
    - space: `O(1)`

    > parameters:
    - `array: <T>[]`: array to search `key`
    - `key: <T>`: key to be search in `array`
    - `comparator: (<T>, <T>) -> int`: comparator for `<T>` type values
    - `left: int? = 0`: starting index to search
    - `right: int? = len(array)`: ending index to search

    > `return: int`: index of `key` in `array`
    """
    left = left if left is not None else 0
    right = right if right is not None else len(array) - 1
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


def k_ary_search(array: list, key, /, k=4, comparator=(lambda a, b: a - b), left: int = None, right: int = None):
    """
    K-ary search algorithm.
    Require `array` to be sorted based on `comparator`.

    > complexity:
    - time: `O(k*log(n,k))`
    - space: `O(1)`

    > parameters:
    - `array: <T>[]`: array to search `key`
    - `key: <T>`: key to be search in `array`
    - `k: int? = 2`: number of buckets to subdivide search
    - `comparator: ((<T>, <T>) -> int)? = lambda a, b: a - b`: comparator for `<T>` type values
    - `left: int? = 0`: starting index to search
    - `right: int? = len(array)`: ending index to search

    > `return: int`: index of `key` in `array`
    """
    left = left if left is not None else 0
    right = right if right is not None else len(array) - 1
    k = max(k, 2)
    while left <= right:
        step = (right - left) / k
        base_left = left
        for i in range(1, k):
            center = base_left + math.floor(step * i)
            comparison = comparator(key, array[center])
            if comparison < 0:
                right = center - 1
                break
            elif comparison > 0:
                left = center + 1
            else:
                return center
    raise KeyError(f'key ({key}) not found')


def interpolation_search(array: list, key, /, comparator=lambda a, b: a - b, left: int = None, right: int = None):
    """
    Interpolation search algorithm.
    Faster than binary search for uniformly distributed arrays.
    Require `array` to be sorted based on `comparator`.

    > complexity:
    - time: `O(log(i))` where `i` is `key` index
    - space: `O(1)`

    > parameters:
    - `array: <T>[]`: array to search `key`
    - `key: <T>`: key to be search in `array`
    - `k: int? = 2`: number of buckets to subdivide search
    - `comparator: ((<T>, <T>) -> int)? = lambda a, b: a - b`: comparator for `<T>` type values
    - `left: int? = 0`: starting index to search
    - `right: int? = len(array)`: ending index to search

    > `return: int`: index of `key` in `array`
    """
    left = left if left is not None else 0
    right = right if right is not None else len(array) - 1
    while array[left] != array[right] and array[left] <= key <= array[right]:
        center = left + ((key - array[left]) * (right - left)) // (array[right] - array[left])
        comparison = comparator(key, array[center])
        if comparison < 0:
            right = center - 1
        elif comparison > 0:
            left = center + 1
        else:
            return center
    if comparator(key, array[left]) == 0:
        return left
    raise KeyError(f'key ({key}) not found')


def exponential_search(array: list, key, /, comparator=lambda a, b: a - b, left: int = None, right: int = None):
    """
    Exponential search algorithm.
    Require `array` to be sorted based on `comparator`.

    > complexity:
    - time: `O(log(log(n))) uniformly distributed arrays, worst: O(n)`
    - space: `O(1)`

    > parameters:
    - `array: <T>[]`: array to search `key`
    - `key: <T>`: key to be search in `array`
    - `comparator: ((<T>, <T>) -> int)? = lambda a, b: a - b`: comparator for `<T>` type values
    - `left: int? = 0`: starting index to search
    - `right: int? = len(array)`: ending index to search

    > `return: int`: index of `key` in `array`
    """
    left = left if left is not None else 0
    right = right if right is not None else len(array) - 1
    bound = 1
    while bound * 2 <= left or bound <= right and key > array[bound]:
        bound *= 2
    return binary_search(array, key, comparator, max(bound // 2, left), min(bound, right))


def test():
    import random
    from ..test import benchmark, match
    match([
        (binary_search, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6], 6),
        (binary_search, [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8], 4),
        (binary_search, [[1, 10, 100, 1000, 10000, 100000, 1000000], 10], 1),
        (k_ary_search, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6, 2], 6),
        (k_ary_search, [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8, 4], 4),
        (k_ary_search, [[1, 10, 100, 1000, 10000, 100000, 1000000], 10, 8], 1),
        (interpolation_search, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6], 6),
        (interpolation_search, [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8], 4),
        (interpolation_search, [[1, 10, 100, 1000, 10000, 100000, 1000000], 10], 1),
        (exponential_search, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6], 6),
        (exponential_search, [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8], 4),
        (exponential_search, [[1, 10, 100, 1000, 10000, 100000, 1000000], 10], 1)
    ])
    benchmark(
        [
            ('       binary search', lambda array: binary_search(array, random.sample(array, 1)[0])),
            ('  k-ary search (k=2)', lambda array: k_ary_search(array, random.sample(array, 1)[0], 2)),
            ('  k-ary search (k=4)', lambda array: k_ary_search(array, random.sample(array, 1)[0], 4)),
            ('  k-ary search (k=8)', lambda array: k_ary_search(array, random.sample(array, 1)[0], 8)),
            (' k-ary search (k=16)', lambda array: k_ary_search(array, random.sample(array, 1)[0], 16)),
            ('interpolation search', lambda array: interpolation_search(array, random.sample(array, 1)[0])),
            ('  exponential_search', lambda array: exponential_search(array, random.sample(array, 1)[0]))

        ],
        test_input_iter=(),
        # skip zero size inputs because search algorithms raise exceptions
        bench_size_iter=(1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s, r: [*range(s)],
        bench_tries=100000
    )


if __name__ == '__main__':
    test()
