import enum
import math


class Gap(enum.Enum):
    """
    Gap generator functions to be used in the shellsort algorithm.
    """
    Shell1959 = lambda n, k: max(n / (2 * k), 1)                                  # O(n**2)
    FrankLazarus1960 = lambda n, k: 2 * math.floor(n / 2**k) + 1                  # O(n**(3/2))
    Hibbard1963 = lambda n, k: 2**k - 1                                           # O(n**(3/2))
    PapernovStasevich1965 = lambda n, k: 2**(k - 1) + 1 if k > 1 else 1           # O(n**(3/2))
    Knuth1973 = lambda n, k: min((3**k - 1) // 2, math.ceil(n / 3))               # O(n**(3/2))
    Sedgewick1982 = lambda n, k: 4**(k) - 1 + 3 * 2**(k - 2) + 1 if k > 1 else 1  # O(n**(4/3))
    Tokuda1992 = lambda n, k: math.ceil((1 / 5) * (9 * (9 / 4) ** (k - 1) - 4))   # unknown
    Ciura2001 = lambda n, k: (1, 4, 10, 23, 57, 132, 301, 701)[min(k - 1, 7)]     # unknown


def shellsort(array: list, gapgen=Gap.Ciura2001):
    """
    Shellsort implementation.

    > complexity:
    - time: `O(n * (log(n)/log(log(n)))**2)`, for any gaps
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted
    - `gapgen: ((int, int) -> int)? = Gap.Ciura2001`: gap generation algorithm

    > `return: typeof(array)`: `array` sorted
    """
    n = len(array)
    gaps = []
    first_gap = int(gapgen(n, 1))
    gaps.append(first_gap)
    if first_gap > 1:
        for k in range(2, n + 3):
            gap = int(gapgen(n, k))
            gaps.append(gap)
            if gap == 1:
                break
    else:
        for k in range(2, n + 3):
            gap = int(gapgen(n, k))
            if gap < n and gap != gaps[-1]:
                gaps.append(gap)
            else:
                break
        gaps.reverse()

    for gap in reversed(gaps):
        for i in range(gap, n):
            key = array[i]
            j = i - gap
            while j >= 0 and array[j] > key:
                array[j + gap] = array[j]
                j -= gap
            array[j + gap] = key
    return array


def test():
    from ..test import benchmark
    benchmark(
        [
            (
                '            shellsort Shell1959',
                lambda array: shellsort(array, gapgen=Gap.Shell1959),
                'shellsort(array, gapgen=Gap.Shell1959)'
            ),
            (
                '     shellsort FrankLazarus1960',
                lambda array: shellsort(array, gapgen=Gap.FrankLazarus1960),
                'shellsort(array, gapgen=Gap.FrankLazarus1960)'
            ),
            (
                '          shellsort Hibbard1963',
                lambda array: shellsort(array, gapgen=Gap.Hibbard1963),
                'shellsort(array, gapgen=Gap.Hibbard1963)'
            ),
            (
                'shellsort PapernovStasevich1965',
                lambda array: shellsort(array, gapgen=Gap.PapernovStasevich1965),
                'shellsort(array, gapgen=Gap.PapernovStasevich1965)'
            ),
            (
                '            shellsort Knuth1973',
                lambda array: shellsort(array, gapgen=Gap.Knuth1973),
                'shellsort(array, gapgen=Gap.Knuth1973)'
            ),
            (
                '        shellsort Sedgewick1982',
                lambda array: shellsort(array, gapgen=Gap.Sedgewick1982),
                'shellsort(array, gapgen=Gap.Sedgewick1982)'
            ),
            (
                '           shellsort Tokuda1992',
                lambda array: shellsort(array, gapgen=Gap.Tokuda1992),
                'shellsort(array, gapgen=Gap.Tokuda1992)'
            ),
            (
                '            shellsort Ciura2001',
                lambda array: shellsort(array, gapgen=Gap.Ciura2001),
                'shellsort(array, gapgen=Gap.Ciura2001)'
            )
        ],
        loads=[shellsort, Gap],
        benchmark_tests=[0, 1, 10, 100, 1000]
    )


if __name__ == '__main__':
    test()
