import math


def stoogesort(array: list):
    """
    Stoogesort implementation.

    > complexity:
    - time: `O(n^(log(3)/log(1.5))) ~ O(n^2.7)`
    - space: `O(log(n, 3))`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    if len(array) == 0:
        return array

    def rec(array: list, first: int, last: int):
        if array[first] > array[last]:
            array[first], array[last] = array[last], array[first]
        if last - first + 1 <= 2:
            return
        third = (last - first + 1) / 3
        rec(array, first, math.ceil(last - third))
        rec(array, math.floor(first + third), last)
        rec(array, first, math.ceil(last - third))

    rec(array, 0, len(array) - 1)
    return array


def test():
    from .test import test
    test([('stoogesort', stoogesort, 'stoogesort(array)')], benchmark_tests=[0, 1, 10, 100, 1000])


if __name__ == '__main__':
    test()
