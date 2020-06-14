def selectionsort(array: list):
    """
    Selectionsort implementation.

    > complexity:
    - time: `O(n**2)`
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted

    > `return: (int | float)[]`: `array` sorted
    """
    for i in range(0, len(array)):
        k = i
        for j in range(i + 1, len(array)):
            if array[j] < array[k]:
                k = j
        array[i], array[k] = array[k], array[i]
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark([('selectionsort', selectionsort)], bench_size_iter=(0, 1, 10, 100, 1000))


if __name__ == '__main__':
    test()
