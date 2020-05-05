def selectionsort(array):
    for i in range(0, len(array)):
        k = i
        for j in range(i + 1, len(array)):
            if array[j] < array[k]:
                k = j
        array[i], array[k] = array[k], array[i]
    return array


def test():
    print(selectionsort([]))
    print(selectionsort([0]))
    print(selectionsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(selectionsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    from ..util import benchmark
    benchmark(selectionsort)


if __name__ == '__main__':
    test()
