from typing import Any, cast


def countingsort(array: list[int]) -> list[int]:
    """
    Sort `array` using countingsort.
    This implementation only supports integer values.
    `bucketsort` can be used for floating-point values.

    > complexity
    - time: `O(n + k)`
    - space: `O(n + k)`
    - `n`: length of `array`
    - `k`: difference between smallest and greatest value in `array`

    > parameters
    - `array`: array to be sorted
    - `return`: `array` sorted
    """
    if len(array) == 0:
        return array
    min_value = min(array)
    max_value = max(array)
    value_range = max_value - min_value + 1
    frequencies = [0] * value_range
    for value in array:
        frequencies[value - min_value] += 1
    for i in range(1, len(frequencies)):
        frequencies[i] += frequencies[i - 1]
    output = [0] * len(array)
    for value in array:
        output[frequencies[value - min_value] - 1] = value
        frequencies[value - min_value] -= 1
    array[:] = output
    return array


def test():
    from ..test import sort_benchmark

    print('terrible input')
    sort_benchmark((('countingsort', cast(Any, countingsort)),), value_range=lambda s: (-s * 10, s * 10))
    print()
    print('bad input')
    sort_benchmark((('countingsort', cast(Any, countingsort)),), value_range=lambda s: (-s * 5, s * 5))
    print()
    print('good input')
    sort_benchmark((('countingsort', cast(Any, countingsort)),), value_range=lambda s: (-s, s))
    print()
    print('best input')
    sort_benchmark((('countingsort', cast(Any, countingsort)),), value_range=lambda s: (-10, 10))
    print()


if __name__ == '__main__':
    test()
