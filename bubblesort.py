import random


def bubblesort(l):
    for i in range(len(l) - 1, -1, -1):
        for j in range(0, i):
            if l[j] > l[j + 1]:
                l[j], l[j + 1] = l[j + 1], l[j]
    return l


def test():
    print(bubblesort([]))
    print(bubblesort([0]))
    print(bubblesort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(bubblesort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    print(bubblesort(random.sample([i for i in range(10)], 10)))


if __name__ == "__main__":
    test()
