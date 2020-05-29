from .insertionsort import insertionsort


def bucketsort(array: list, /, k: int = None, subsort: type(abs) = insertionsort):
    """
    Bucketsort implementation.
    This implementation uses insertionsort as internal sorter.
    The deafult `k` value (which is `len(array)`) can be manually modified as well as the `subsort` algorithm.

    > complexity:
    - time: average: `O(n + (n^2/k) + k)`, worst `O(n^2)`, best: `O(n)` if `n ~ k` and uniform distribution.
    - space: `O(n * k)`

    > parameters:
    - `array: list`: array to be sorted
    - `k: int` (optional -> `len(array)`): number of buckets
    - `subsort: (a) -> list` (optional -> `insertionsort`): algorithm to sort buckets
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
    from random import randint
    from timeit import repeat
    print(bucketsort([]))
    print(bucketsort([0]))
    print(bucketsort([*range(20)]))
    print(bucketsort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000, 5000, 10000]:
        results = repeat(
            'bucketsort(array)',
            setup='array=[randint(0, i**2) for j in range(i)]',
            globals={**globals(), **locals()},
            number=1,
            repeat=100
        )
        print('array length:', i, sum(results))


if __name__ == '__main__':
    test()
