import itertools
import random


def bogosort_random(array: list):
    """
    Bogosort implementation, randomized version.

    > complexity:
    - time: `unbounded`
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted

    > `return: typeof(array)`: `array` sorted
    """
    while any(array[i] > array[i + 1] for i in range(len(array) - 1)):
        random.shuffle(array)
    return array


def bogosort_deterministic(array: list):
    """
    Bogosort implementation, deterministic version.

    > complexity:
    - time: `O((n + 1)!)`
    - space: `O(n)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted

    > `return: typeof(array)`: `array` sorted
    """
    for permutation in itertools.permutations(array):
        if any(permutation[i] > permutation[i + 1] for i in range(len(permutation) - 1)):
            continue
        break
    array[:] = permutation
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark(
        [
            ('       bogosort random', bogosort_random),
            ('bogosort deterministic', bogosort_deterministic),
        ],
        test_size=5,
        bench_size_iter=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        bench_repeats=10
    )


if __name__ == '__main__':
    test()
