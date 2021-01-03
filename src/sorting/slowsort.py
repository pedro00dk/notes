def slowsort(array: list[float]) -> list[float]:
    """
    Sort `array` using slowsort.

    > complexity
    - time: `O(T(n))`
    - space: `O(n)`
    - `n`: length of `array`
    - `T(x)`: recursive function T(x) = T(x - 1) + T(x/2)*2 + 1`

    > parameters
    - `array`: array to be sorted
    - `return`: `array` sorted
    """
    def rec(array: list[float], first: int, last: int):
        if first >= last:
            return
        center = (first + last) // 2
        rec(array, first, center)
        rec(array, center + 1, last)
        if array[center] > array[last]:
            array[center], array[last] = array[last], array[center]
        rec(array, first, last - 1)

    if len(array) == 0:
        return array
    rec(array, 0, len(array) - 1)
    return array


def test():
    from ..test import sort_benchmark

    sort_benchmark((('slowsort', slowsort),), bench_sizes=(0, 1, 10, 100, 1000))


if __name__ == '__main__':
    test()
