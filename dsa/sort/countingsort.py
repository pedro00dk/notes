def countingsort(array: list):
    """
    Countingsort implementation.

    > complexity:
    - time: `O(n + k)` where `k` is `max_key - min_key`
    - space: `O(n + k)` where `k` is `max_key - min_key`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    if len(array) == 0:
        return array
    min_key, max_key = min(array), max(array)
    count = [0] * (max_key - min_key + 1)
    for i in array:
        count[i - min_key] += 1
    k = 0
    for i in range(len(count)):
        for j in range(count[i]):
            array[k + j] = i + min_key
        k += count[i]
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
