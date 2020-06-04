def selectionsort(array: list):
    """
    Selectionsort implementation.

    > complexity:
    - time: `O(n**2)`
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted

    > `return: typeof(array)`: `array` sorted
    """
    for i in range(0, len(array)):
        k = i
        for j in range(i + 1, len(array)):
            if array[j] < array[k]:
                k = j
        array[i], array[k] = array[k], array[i]
    return array


def test():
    from ..test import benchmark
    benchmark([('selectionsort', selectionsort, 'selectionsort(array)')], benchmark_tests=[0, 1, 10, 100, 1000])


if __name__ == '__main__':
    test()
