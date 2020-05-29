def mergesort(array):
    """
    Heapsort implementation.

    > complexity:
    - time: `O(n*log(n))`
    - space: `O(n)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    def rec(array: list, left: int, right: int, temp: list):
        center = (left + right) // 2
        if right - left + 1 > 2:
            rec(array, left, center, temp)
            rec(array, center + 1, right, temp)
        for i in range(left, right + 1):
            temp[i] = array[i]
        left_index, right_index, i = left, center + 1, left
        while left_index <= center and right_index <= right:
            if temp[left_index] <= temp[right_index]:
                array[i] = temp[left_index]
                left_index += 1
            else:
                array[i] = temp[right_index]
                right_index += 1
            i += 1
        while left_index <= center:
            array[i] = temp[left_index]
            left_index += 1
            i += 1
        while right_index <= right:
            array[i] = temp[right_index]
            right_index += 1
            i += 1

    rec(array, 0, len(array) - 1, [0] * len(array))
    return array


def test():
    from random import randint
    from timeit import timeit
    print(mergesort([]))
    print(mergesort([0]))
    print(mergesort([*range(20)]))
    print(mergesort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000]:
        print(
            'array length:', i,
            timeit(
                'mergesort(array)',
                setup='array=[randint(0, i**2) for j in range(i)]',
                globals={**globals(), **locals()},
                number=100
            )
        )


if __name__ == '__main__':
    test()
