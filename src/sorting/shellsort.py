import enum
import math


class Gap(enum.Enum):
    """
    Functions to be used in the shellsort algorithm to create gap sequences.
    Enum functions are directly bound to values, meaning it is not necessary to access the `value` field, which does not
    even exist for functions.

    > all gap functions accept the following parameters:
    - `n: int`: the array size
    - `k: int`: the current gap size (must start at 1)

    Gap functions may produce increasing or decresing gap sizes.
    Increasing sequences stop when the gap is greater than `n` of two equal gaps where generated.
    Decreasing sequences stop at 1.
    """
    SHELL1959 = lambda n, k: max(n / (2 * k), 1)                                  # O(n**2)
    FRANKLAZARUS1960 = lambda n, k: 2 * math.floor(n / 2**k) + 1                  # O(n**(3/2))
    HIBBARD1963 = lambda n, k: 2**k - 1                                           # O(n**(3/2))
    PAPERNOV_STASEVICH1965 = lambda n, k: 2**(k - 1) + 1 if k > 1 else 1          # O(n**(3/2))
    KNUTH1973 = lambda n, k: min((3**k - 1) // 2, math.ceil(n / 3))               # O(n**(3/2))
    SEDGEWICK1982 = lambda n, k: 4**(k) - 1 + 3 * 2**(k - 2) + 1 if k > 1 else 1  # O(n**(4/3))
    TOKUDA1992 = lambda n, k: math.ceil((1 / 5) * (9 * (9 / 4) ** (k - 1) - 4))   # unknown
    CIURA2001 = lambda n, k: (1, 4, 10, 23, 57, 132, 301, 701)[min(k - 1, 7)]     # unknown

    @staticmethod
    def gap(array: list, gapgen):
        n = len(array)
        gaps = [int(gapgen(n, 1))]
        if gaps[0] > 1:
            for k in range(2, n + 3):
                gap = int(gapgen(n, k))
                gaps.append(gap)
                if gap == 1:
                    break
        else:
            for k in range(2, n + 3):
                gap = int(gapgen(n, k))
                if gap >= n or gap == gaps[-1]:
                    break
                gaps.append(gap)
            gaps.reverse()
        return gaps


def shellsort(array: list, gapgen=Gap.CIURA2001):
    """
    Shellsort implementation.

    > complexity:
    - time: `O(n * (log(n)/log(log(n)))**2)`, for any gaps
    - space: `O(1)`

    > parameters:
    - `array: (int | float)[]`: array to be sorted
    - `gapgen: ((int, int) => int)? = Gap.Ciura2001`: gap generation algorithm

    > `return: (int | float)[]`: `array` sorted
    """
    gaps = Gap.gap(array, gapgen)
    for gap in gaps:
        for i in range(gap, len(array)):
            key = array[i]
            j = i - gap
            while j >= 0 and array[j] > key:
                array[j + gap] = array[j]
                j -= gap
            array[j + gap] = key
    return array


def test():
    from ..test import sort_benchmark
    sort_benchmark(
        [
            ('             shellsort Shell 1959', lambda array: shellsort(array, gapgen=Gap.SHELL1959)),
            ('      shellsort FrankLazarus 1960', lambda array: shellsort(array, gapgen=Gap.FRANKLAZARUS1960)),
            ('           shellsort Hibbard 1963', lambda array: shellsort(array, gapgen=Gap.HIBBARD1963)),
            ('shellsort Papernov Stasevich 1965', lambda array: shellsort(array, gapgen=Gap.PAPERNOV_STASEVICH1965)),
            ('             shellsort Knuth 1973', lambda array: shellsort(array, gapgen=Gap.KNUTH1973)),
            ('         shellsort Sedgewick 1982', lambda array: shellsort(array, gapgen=Gap.SEDGEWICK1982)),
            ('            shellsort Tokuda 1992', lambda array: shellsort(array, gapgen=Gap.TOKUDA1992)),
            ('             shellsort Ciura 2001', lambda array: shellsort(array, gapgen=Gap.CIURA2001))
        ],
        bench_sizes=(0, 1, 10, 100, 1000)
    )


if __name__ == '__main__':
    test()
