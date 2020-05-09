def binary_search(array, key, /, comparator=lambda x, y: x - y):
    left = 0
    right = len(array) - 1
    while left <= right:
        center = (left + right) // 2
        comparison = comparator(key, array[center])
        if comparison < 0:
            right = center - 1
        elif comparison > 0:
            left = center + 1
        else:
            return center
    raise KeyError('not found')


def test():
    from ..util import match
    match([
        (binary_search, [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6], 6),
        (binary_search, [[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20], 8], 4),
        (binary_search, [[1, 10, 100, 1000, 10000, 100000, 1000000], 10], 1)
    ])


if __name__ == '__main__':
    test()
