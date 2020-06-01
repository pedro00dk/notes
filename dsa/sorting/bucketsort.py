from .insertionsort import insertionsort


def bucketsort(array: list, /, k: int = None, subsort: type(lambda array: array) = None):
    """
    Bucketsort implementation.
    This implementation uses insertionsort as internal sorter.
    The default `k` value (which is `len(array)`) can be manually modified as well as the `subsort` algorithm.

    > complexity:
    - time: average: `O(n + (n^2/k) + k)`, worst `O(n^2)`, best: `O(n)` if `n ~ k` and uniform distribution.
    - space: `O(n * k)`

    > parameters:
    - `array: list`: array to be sorted
    - `k: int` (optional -> `len(array)`): number of buckets
    - `subsort: (list) -> list` (optional -> `insertionsort`): algorithm to sort buckets
    - `#return#: list`: `array` sorted
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
    from ..test import benchmark
    benchmark(
        [
            ('bucketsort k=8*n ', bucketsort, 'bucketsort(array, len(array) * 8)'),
            ('bucketsort k=4*n ', bucketsort, 'bucketsort(array, len(array) * 4)'),
            ('bucketsort k=2*n ', bucketsort, 'bucketsort(array, len(array) * 2)'),
            ('bucketsort k=n   ', bucketsort, 'bucketsort(array)'),
            ('bucketsort k=n/2 ', bucketsort, 'bucketsort(array, len(array) // 2)'),
            ('bucketsort k=n/4 ', bucketsort, 'bucketsort(array, len(array) // 4)'),
            ('bucketsort k=n/8 ', bucketsort, 'bucketsort(array, len(array) // 8)'),
            ('bucketsort k=n/16', bucketsort, 'bucketsort(array, len(array) // 16)'),
            ('bucketsort k=n/32', bucketsort, 'bucketsort(array, len(array) // 32)')
        ]
    )


if __name__ == '__main__':
    test()
