def countingsort(array: list):
    """
    Countingsort implementation.
    Countingsort assumes all values contained in `array` are of `int` type.

    > complexity:
    - time: `O(n + k)` where `k` is `max_value - min_value`
    - space: `O(n + k)` where `k` is `max_value - min_value`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    if len(array) == 0:
        return array
    min_value, max_value = min(array), max(array)
    value_range = max_value - min_value + 1
    count = [0] * value_range
    for value in array:
        count[value - min_value] += 1
    k = 0
    for value in range(len(count)):
        for j in range(count[value]):
            array[k + j] = value + min_value
        k += count[value]
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
            setup='array=[randint(-i, i) for j in range(i)]',
            globals={**globals(), **locals()},
            number=1,
            repeat=100
        )
        print('array length:', i, sum(results))


if __name__ == '__main__':
    test()
