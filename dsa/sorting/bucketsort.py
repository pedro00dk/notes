from .insertionsort import insertionsort


def bucketsort(array: list, /, k: int = None, subsort=None):
    """
    Bucketsort implementation.
    This implementation uses insertionsort as internal sorter.
    The default `k` value (which is `len(array)`) can be manually modified as well as the `subsort` algorithm.

    > complexity:
    - time: average: `O(n + (n**2/k) + k)`, worst `O(n**2)`, best: `O(n)` if `n ~ k` and uniform distribution.
    - space: `O(n * k)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted
    - `k: int? = len(array)`: number of buckets
    - `subsort: ((int | float)[] => (int | float)[])? = insertionsort`: algorithm to sort buckets

    > `return: typeof(array)`: `array` sorted
    """
    if len(array) == 0:
        return array
    k = max(k if k is not None else len(array), 1)
    subsort = subsort if subsort is not None else insertionsort
    min_value, max_value = min(array), max(array)
    value_range = max_value - min_value + 1
    buckets = [[] for i in range(k)]
    for value in array:
        buckets[int((value - min_value) / value_range * k)].append(value)
    for bucket in buckets:
        insertionsort(bucket)
    array[:] = (value for bucket in buckets for value in bucket)
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark(
        [
            ('bucketsort k=8*n ', lambda array: bucketsort(array, len(array) * 8)),
            ('bucketsort k=4*n ', lambda array: bucketsort(array, len(array) * 4)),
            ('bucketsort k=2*n ', lambda array: bucketsort(array, len(array) * 2)),
            ('bucketsort k=n   ', lambda array: bucketsort(array)),
            ('bucketsort k=n/2 ', lambda array: bucketsort(array, len(array) // 2)),
            ('bucketsort k=n/4 ', lambda array: bucketsort(array, len(array) // 4)),
            ('bucketsort k=n/8 ', lambda array: bucketsort(array, len(array) // 8)),
            ('bucketsort k=n/16', lambda array: bucketsort(array, len(array) // 16)),
            ('bucketsort k=n/32', lambda array: bucketsort(array, len(array) // 32))
        ]
    )


if __name__ == '__main__':
    test()
