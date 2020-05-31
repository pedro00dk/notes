def countingsort(array: list):
    """
    Countingsort implementation.
    This implementation only supports integer values.
    Use bucketsort for floating-point values.

    > complexity:
    - time: `O(n + k)` where `k` is `value_range`
    - space: `O(n + k)` where `k` is `value_range`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    if len(array) == 0:
        return array
    min_value, max_value = min(array), max(array)
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
    from random import randint
    from timeit import repeat
    print(countingsort([]))
    print(countingsort([0]))
    print(countingsort([*range(20)]))
    print(countingsort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000, 5000, 10000]:
        results = repeat(
            'countingsort(array)',
            setup='array=[randint(-i, i) for j in range(i)]', # input optimized for countingsort (small spread)
            globals={**globals(), **locals()},
            number=1,
            repeat=100
        )
        print('array length:', i, sum(results))


if __name__ == '__main__':
    test()
