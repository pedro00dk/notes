import math


def quicksort_hoare(array: list):
    """
    Quicksort implementation using Hoare's partition algorithm with a few modifications.
    The center element is used as index.
    Random pivot is not used because python random functions are very slow.

    > complexity:
    - time: average: `O(n*log(n))`, worst: `O(n^2)`
    - space: average: `O(log(n))`, worst: `O(n)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    def rec(array: list, left: int, right: int):
        if left >= right:
            return
        pivot = array[(left + right) // 2]
        left_index, right_index = left, right
        while True:
            while array[left_index] < pivot:
                left_index += 1
            while array[right_index] > pivot:
                right_index -= 1
            if left_index >= right_index:
                break
            array[left_index], array[right_index] = array[right_index], array[left_index]
            left_index += 1
            right_index -= 1
        rec(array, left, right_index)
        rec(array, right_index + 1, right)

    rec(array, 0, len(array) - 1)
    return array


def quicksort_lomuto(array: list):
    """
    Quicksort implementation using Hoare's partition algorithm with a few modifications.
    The center element is used as index.
    Random pivot is not used because python random functions are very slow.

    > complexity:
    - time: average: `O(n*log(n))`, worst: `O(n^2)`
    - space: average: `O(log(n))`, worst: `O(n)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    def rec(array: list, left: int, right: int):
        if left >= right:
            return
        pivot_index = (left + right) // 2
        array[right], array[pivot_index] = array[pivot_index], array[right]
        pivot = array[right]
        left_index = left
        for center_index in range(left, right):
            if array[center_index] < pivot:
                array[left_index], array[center_index] = array[center_index], array[left_index]
                left_index += 1
        array[left_index], array[right] = array[right], array[left_index]
        rec(array, left, left_index - 1)
        rec(array, left_index + 1, right)

    rec(array, 0, len(array) - 1)
    return array


def quicksort_dual_pivot(array: list):
    """
    Quicksort dual-pivot implementation.

    > complexity:
    - time: average: `O(n*log(n))`, worst: `O(n^2)`
    - space: average: `O(log(n))`, worst: `O(n)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    def rec(array: list, left: int, right: int):
        if left >= right:
            return
        third = (right - left) / 3
        left_pivot_index = left + math.floor(third)
        right_pivot_index = left + math.ceil(third * 2)
        if array[left_pivot_index] > array[right_pivot_index]:
            array[left_pivot_index], array[right_pivot_index] = array[right_pivot_index], array[left_pivot_index]
        array[left], array[left_pivot_index] = array[left_pivot_index], array[left]
        array[right], array[right_pivot_index] = array[right_pivot_index], array[right]
        left_pivot, right_pivot = array[left], array[right]
        left_index, center_index, right_index = left + 1, left + 1, right - 1
        while center_index <= right_index:
            if array[center_index] < left_pivot:
                array[left_index], array[center_index] = array[center_index], array[left_index]
                left_index += 1
                center_index += 1
            elif array[center_index] > right_pivot:
                array[right_index], array[center_index] = array[center_index], array[right_index]
                right_index -= 1
            else:
                center_index += 1
        left_index -= 1
        right_index += 1
        array[left], array[left_index] = array[left_index], array[left]
        array[right], array[right_index] = array[right_index], array[right]
        rec(array, left, left_index - 1)
        rec(array, left_index + 1, right_index - 1)
        rec(array, right_index + 1, right)

    rec(array, 0, len(array) - 1)
    return array


def test():
    from ..test import benchmark
    benchmark(
        [
            ('     hoare', quicksort_hoare, 'quicksort_hoare(array)'),
            ('    lomuto', quicksort_lomuto, 'quicksort_lomuto(array)'),
            ('dual pivot', quicksort_dual_pivot, 'quicksort_dual_pivot(array)')
        ]
    )


if __name__ == '__main__':
    test()
