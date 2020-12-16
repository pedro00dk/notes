import itertools
import random


def bogosort_random(array: list[float]) -> list[float]:
    """
    Sort `array` using randomized bogosort.

    > complexity
    - time: `unbounded`
    - space: `O(1)`

    > parameters
    - `array`: array to be sorted
    - `return`: `array` sorted
    """
    while any(array[i] > array[i + 1] for i in range(len(array) - 1)):
        random.shuffle(array)
    return array


def bogosort_deterministic(array: list[float]) -> list[float]:
    """
    Sort `array` using deterministic bogosort.

    > complexity
    - time: `O((n + 1)!)`
    - space: `O(n)`

    > parameters
    - `array`: array to be sorted
    - `return`: `array` sorted
    """
    for permutation in itertools.permutations(array):
        if all(permutation[i] <= permutation[i + 1] for i in range(len(permutation) - 1)):
            continue
        array[:] = permutation
        break
    return array


def test():
    from ..test import sort_benchmark

    sort_benchmark(
        (
            ('       bogosort random', bogosort_random),
            ('bogosort deterministic', bogosort_deterministic),
        ),
        test_size=5,
        bench_sizes=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        bench_repeat=10
    )


if __name__ == '__main__':
    test()
