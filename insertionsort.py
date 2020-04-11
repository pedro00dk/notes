import random


def insertionsort(l):
    for i in range(1, len(l)):
        for j in range(i, 0, -1):
            if l[j] < l[j - 1]:
                l[j], l[j - 1] = l[j - 1], l[j]
    return l


def test():
    print(insertionsort([]))
    print(insertionsort([0]))
    print(insertionsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(insertionsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    print(insertionsort(random.sample([i for i in range(10)], 10)))


if __name__ == '__main__':
    test()
