def selectionsort(array: list):
    """
    Selectionsort implementation.

    > complexity:
    - time: `O(n^2)`
    - space: `O(1)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    for i in range(0, len(array)):
        k = i
        for j in range(i + 1, len(array)):
            if array[j] < array[k]:
                k = j
        array[i], array[k] = array[k], array[i]
    return array


def test():
    from random import randint
    from timeit import timeit
    print(selectionsort([]))
    print(selectionsort([0]))
    print(selectionsort([*range(20)]))
    print(selectionsort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000]:
        print(
            'array length:', i,
            timeit(
                'selectionsort(array)',
                setup='array=[randint(0, i**2) for j in range(i)]',
                globals={**globals(), **locals()},
                number=100
            )
        )


if __name__ == '__main__':
    test()
