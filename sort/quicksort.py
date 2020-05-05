import random
import tester


def quicksort(array, left=None, right=None):
    left = left if left is not None else 0
    right = right if right is not None else len(array) - 1

    if right - left <= 0:
        return array

    pivot = array[random.randint(left, right)]
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

    quicksort(array, left, right_index)
    quicksort(array, right_index + 1, right)
    return array


def test():
    print(quicksort([]))
    print(quicksort([0]))
    print(quicksort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(quicksort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    tester.test_sort(quicksort)


if __name__ == '__main__':
    test()
