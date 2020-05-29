def insertionsort(array: list):
    """
    Insertionsort implementation.

    > optimizations:
    - save current element to be sorted and override previous values rather than swapping, then place the saved value in
      its position.

    > complexity:
    - time: `O(n^2)`
    - space: `O(1)`

    > parameters:
    - `array: list`: array to be sorted
    - `#return#: list`: `array` sorted
    """
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


def test():
    from random import randint
    from timeit import repeat
    print(insertionsort([]))
    print(insertionsort([0]))
    print(insertionsort([*range(20)]))
    print(insertionsort([*range(20 - 1, -1, -1)]))
    for i in [5, 10, 50, 100, 500, 1000]:
        results = repeat(
            'insertionsort(array)',
            setup='array=[randint(0, i**2) for j in range(i)]',
            globals={**globals(), **locals()},
            number=1,
            repeat=100
        )
        print('array length:', i, sum(results))


if __name__ == '__main__':
    test()
