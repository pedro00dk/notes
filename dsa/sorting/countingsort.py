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
    from .test import test
    print('terrible input')
    test([('countingsort', countingsort, 'countingsort(array)')], array_min='-i*10', array_max='i*10')
    print()
    print('bad input')
    test([('countingsort', countingsort, 'countingsort(array)')], array_min='-i*5', array_max='i*5')
    print()
    print('good input')
    test([('countingsort', countingsort, 'countingsort(array)')], array_min='-i', array_max='i')
    print('best input')
    test([('countingsort', countingsort, 'countingsort(array)')], array_min='-10', array_max='10')
    print()


if __name__ == '__main__':
    test()
