
def binary_search(l, key, getter=lambda x: x):
    left = 0
    right = len(l) - 1
    while left <= right:
        center = (left + right) // 2
        center_key = getter(l[center])
        if key < center_key:
            right = center - 1
        elif key > center_key:
            left = center + 1
        else:
            return center
    return None


def test():
    print(binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6))
    print(binary_search([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8))
    print(binary_search([1, 10, 100, 1000, 10000, 100000, 1000000], 10))


if __name__ == '__main__':
    test()
