def mergesort(array, left=None, right=None, acc=None):
    left = left if left is not None else 0
    right = right if right is not None else len(array) - 1
    acc = acc if acc is not None else [None] * len(array)
    center = (left + right) // 2

    if right - left + 1 > 2:
        mergesort(array, left, center, acc)
        mergesort(array, center + 1, right, acc)

    for i in range(left, right + 1):
        acc[i] = array[i]

    left_index, right_index, i = left, center + 1, left
    while left_index <= center and right_index <= right:
        if acc[left_index] <= acc[right_index]:
            array[i] = acc[left_index]
            left_index += 1
        else:
            array[i] = acc[right_index]
            right_index += 1
        i += 1
    while left_index <= center:
        array[i] = acc[left_index]
        left_index += 1
        i += 1
    while right_index <= right:
        array[i] = acc[right_index]
        right_index += 1
        i += 1

    return array


def test():
    from ..util import benchmark
    print(mergesort([]))
    print(mergesort([0]))
    print(mergesort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(mergesort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    benchmark(mergesort)


if __name__ == '__main__':
    test()
