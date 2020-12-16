import math


def stoogesort(array: list[float]) -> list[float]:
    """
    Sort `array` using stoogesort.

    > complexity
    - time: `O(n**(log(3)/log(1.5))) ~ O(n**2.7)`
    - space: `O(log(n, 3))`

    > parameters
    - `array`: array to be sorted
    - `return`: `array` sorted
    """
    def rec(array: list[float], first: int, last: int):
        if array[first] > array[last]:
            array[first], array[last] = array[last], array[first]
        if last - first + 1 <= 2:
            return
        third = (last - first + 1) / 3
        rec(array, first, math.ceil(last - third))
        rec(array, math.floor(first + third), last)
        rec(array, first, math.ceil(last - third))

    if len(array) == 0:
        return array
    rec(array, 0, len(array) - 1)
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark((('stoogesort', stoogesort),), bench_sizes=(0, 1, 10, 100, 1000))


if __name__ == '__main__':
    test()
