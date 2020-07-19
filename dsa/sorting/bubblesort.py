def bubblesort(array: list):
    """
    Bubblesort implementation.

    > complexity:
    - time: `O(n**2)`
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted

    > `return: (int | float)[]`: `array` sorted
    """
    for i in range(len(array) - 1, -1, -1):
        for j in range(0, i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark([('bubblesort', bubblesort)], bench_sizes=(0, 1, 10, 100, 1000))


if __name__ == '__main__':
    test()
