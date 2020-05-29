def quicksort(array: list):
    """
    Quicksort implementation.
    This implementation uses Hoare's partition algorithm with a few modifications.
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
        if right - left <= 0:
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


def test():
    from random import randint
    from timeit import timeit
    print(quicksort([]))
    print(quicksort([0]))
    print(quicksort([*range(20)]))
    print(quicksort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000]:
        print(
            'array length:', i,
            timeit(
                'quicksort(array)',
                setup='array=[randint(0, i**2) for j in range(i)]',
                globals={**globals(), **locals()},
                number=100
            )
        )


if __name__ == '__main__':
    test()
