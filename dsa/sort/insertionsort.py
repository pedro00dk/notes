def insertionsort(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


def test():
    from ..util import benchmark
    print(insertionsort([]))
    print(insertionsort([0]))
    print(insertionsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(insertionsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    benchmark(insertionsort)


if __name__ == '__main__':
    test()
