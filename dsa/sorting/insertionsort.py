def insertionsort(array: list):
    """
    Insertionsort implementation.

    > optimizations:
    - save current element to be sorted and override previous values rather than swapping, then place the saved value in
      its position.

    > complexity:
    - time: `O(n**2)`
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted

    > `return: typeof(array)`: `array` sorted
    """
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


def test():
    from ..test import benchmark
    benchmark([('insertionsort', insertionsort, 'insertionsort(array)')], benchmark_tests=[0, 1, 10, 100, 1000])


if __name__ == '__main__':
    test()
