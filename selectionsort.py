import random


def selectionsort(l):
    for i in range(0, len(l)):
        k = i
        for j in range(i + 1, len(l)):
            if l[j] < l[k]:
                k = j
        l[i], l[k] = l[k], l[i]
    return l


def test():
    print(selectionsort([]))
    print(selectionsort([0]))
    print(selectionsort([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    print(selectionsort([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))
    print(selectionsort(random.sample([i for i in range(10)], 10)))


if __name__ == "__main__":
    test()
