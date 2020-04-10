import random


def mergesort(l, left=None, right=None, acc=None):
    left = left if left is not None else 0
    right = right if right is not None else len(l) - 1
    acc = acc if acc is not None else [None] * len(l)
    center = (left + right) // 2

    if right - left + 1 > 2:
        mergesort(l, left, center, acc)
        mergesort(l, center + 1, right, acc)

    for i in range(left, right + 1):
        acc[i] = l[i]

    left_index, right_index, i = left, center + 1, left
    while left_index <= center and right_index <= right:
        if acc[left_index] <= acc[right_index]:
            l[i] = acc[left_index]
            left_index += 1
        else:
            l[i] = acc[right_index]
            right_index += 1
        i += 1
    while left_index <= center:
        l[i] = acc[left_index]
        left_index += 1
        i += 1
    while right_index <= right:
        l[i] = acc[right_index]
        right_index += 1
        i += 1

    return l


def test():
    print(mergesort([]))
    print(mergesort([0]))
    print(mergesort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(mergesort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    print(mergesort(random.sample([i for i in range(10)], 10)))


if __name__ == "__main__":
    test()
