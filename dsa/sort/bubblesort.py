def bubblesort(array: list):
    """
    Bubblesort implementation.

    > complexity:
    - time: `O(n^2)`
    - space: `O(1)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    for i in range(len(array) - 1, -1, -1):
        for j in range(0, i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def test():
    from random import randint
    from timeit import timeit
    print(bubblesort([]))
    print(bubblesort([0]))
    print(bubblesort([*range(20)]))
    print(bubblesort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000]:
        print(
            'array length:', i,
            timeit(
                'bubblesort(array)',
                setup='array=[randint(0, i**2) for j in range(i)]',
                globals={**globals(), **locals()},
                number=100
            )
        )


if __name__ == '__main__':
    test()
