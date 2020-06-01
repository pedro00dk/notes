from random import shuffle

from ..combinatorics.permutations import permutations_cycle


def bogosort_random(array: list):
    """
    Bogosort implementation, randomized version.

    > complexity:
    - time: `unbounded`
    - space: `O(1)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    while any(array[i] > array[i + 1] for i in range(len(array) - 1)):
        shuffle(array)
    return array


def bogosort_deterministic(array: list):
    """
    Bogosort implementation, deterministic version.

    > complexity:
    - time: `O((n + 1)!)`
    - space: `O(n)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    for permutation in permutations_cycle(array):
        if any(permutation[i] > permutation[i + 1] for i in range(len(permutation) - 1)):
            continue
        break
    array[:] = permutation
    return array


def test():
    from .test import test
    test(
        [
            ('       bogosort random', bogosort_random, 'bogosort_random(array)'),
            ('bogosort deterministic', bogosort_deterministic, 'bogosort_deterministic(array)'),
        ],
        print_length=5,
        benchmark_tests=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        tries=10
    )


if __name__ == '__main__':
    test()
