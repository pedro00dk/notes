def mergesort(array: list[float]) -> list[float]:
    """
    Sort `array` using mergesort.

    > complexity
    - time: `O(n*log(n))`
    - space: `O(n)`

    > parameters
    - `array`: array to be sorted
    - `return`: `array` sorted
    """
    def rec(array: list[float], left: int, right: int, temp: list[float]):
        center = (left + right) // 2
        if right - left + 1 > 2:
            rec(array, left, center, temp)
            rec(array, center + 1, right, temp)
        for i in range(left, right + 1):
            temp[i] = array[i]
        left_index = left
        right_index = center + 1
        i = left
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

    rec(array, 0, len(array) - 1, array.copy())
    return array


def test():
    from ..test import sort_benchmark

    sort_benchmark((('mergesort', mergesort),))


if __name__ == '__main__':
    test()
