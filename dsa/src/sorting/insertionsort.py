def insertionsort(array: list[float]) -> list[float]:
    """
    Sort `array` using insertionsort.

    > complexity
    - time: `O(n**2)`
    - space: `O(1)`
    - `n`: length of `array`

    > parameters
    - `array`: array to be sorted
    - `return`: `array` sorted
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
    from ..test import sort_benchmark

    sort_benchmark((("insertionsort", insertionsort),), bench_sizes=(0, 1, 10, 100, 1000))


if __name__ == "__main__":
    test()
