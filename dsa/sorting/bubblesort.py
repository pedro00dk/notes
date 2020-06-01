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
    from .test import test
    test([('bubblesort', bubblesort, 'bubblesort(array)')], benchmark_tests=[0, 1, 10, 100, 1000])


if __name__ == '__main__':
    test()
