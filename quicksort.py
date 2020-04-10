import random


def quicksort(l, left=None, right=None):
    left = left if left is not None else 0
    right = right if right is not None else len(l) - 1

    if right - left <= 0:
        return l

    pivot = l[random.randint(left, right)]
    left_index, right_index = left, right
    while True:
        while l[left_index] < pivot:
            left_index += 1
        while l[right_index] > pivot:
            right_index -= 1
        if left_index >= right_index:
            break
        l[left_index], l[right_index] = l[right_index], l[left_index]
        left_index += 1
        right_index -= 1

    quicksort(l, left, right_index)
    quicksort(l, right_index + 1, right)
    return l


def test():
    print(quicksort([]))
    print(quicksort([0]))
    print(quicksort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(quicksort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    print(quicksort(random.sample([i for i in range(10)], 10)))


if __name__ == "__main__":
    test()
