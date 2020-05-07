def quicksort(array):
    sort(array, 0, len(array) - 1)
    return array


def sort(array, left, right):
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
    sort(array, left, right_index)
    sort(array, right_index + 1, right)


def test():
    from ..util import benchmark
    print(quicksort([]))
    print(quicksort([0]))
    print(quicksort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(quicksort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    benchmark(quicksort)


if __name__ == '__main__':
    test()
