import tester


def insertionsort(array):
    for i in range(1, len(array)):
        for j in range(i, 0, -1):
            if array[j] < array[j - 1]:
                array[j], array[j - 1] = array[j - 1], array[j]
    return array


def test():
    print(insertionsort([]))
    print(insertionsort([0]))
    print(insertionsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(insertionsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    tester.test_sort(insertionsort)


if __name__ == '__main__':
    test()
