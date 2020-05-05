def bubblesort(array):
    for i in range(len(array) - 1, -1, -1):
        for j in range(0, i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


def test():
    from ..util import benchmark
    print(bubblesort([]))
    print(bubblesort([0]))
    print(bubblesort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(bubblesort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    benchmark(bubblesort)


if __name__ == '__main__':
    test()
