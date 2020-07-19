def slowsort(array: list):
    """
    Slowsort implementation.

    > complexity:
    - time: `O(T(n)), where T(n) = T(n-1) + T(n/2)*2 + 1`
    - space: `O(n)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted

    > `return: (int | float)[]`: `array` sorted
    """
    if len(array) == 0:
        return array

    def rec(array: list, first: int, last: int):
        if first >= last:
            return
        center = (first + last) // 2
        rec(array, first, center)
        rec(array, center + 1, last)
        if array[center] > array[last]:
            array[center], array[last] = array[last], array[center]
        rec(array, first, last - 1)

    rec(array, 0, len(array) - 1)
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark([('slowsort', slowsort)], bench_sizes=(0, 1, 10, 100, 1000))


if __name__ == '__main__':
    test()
