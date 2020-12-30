import math
from typing import Callable

GapFunction = Callable[[int, int], int]

# Functions to be used in the shellsort algorithm to create gap sequences.
#
# > parameters
# - `n`: the array size
# - `k`: the current gap size (must start at 1)
#
# Gap functions may produce increasing or decresing gap sizes.
# Increasing sequences stop when the gap is greater than `n`, or two equal gaps where generated.
# Decreasing sequences stop at 1.
SHELL1959: GapFunction = lambda n, k: max(n // (2 * k), 1)                                 # O(n**2)
FRANKLAZARUS1960: GapFunction = lambda n, k: 2 * math.floor(n / 2**k) + 1                  # O(n**(3/2))
HIBBARD1963: GapFunction = lambda n, k: 2**k - 1                                           # O(n**(3/2))
PAPERNOVSTASEVICH1965: GapFunction = lambda n, k: 2**(k - 1) + 1 if k > 1 else 1           # O(n**(3/2))
KNUTH1973: GapFunction = lambda n, k: min((3**k - 1) // 2, math.ceil(n / 3))               # O(n**(3/2))
SEDGEWICK1982: GapFunction = lambda n, k: 4**(k) - 1 + 3 * 2**(k - 2) + 1 if k > 1 else 1  # O(n**(4/3))
TOKUDA1992: GapFunction = lambda n, k: math.ceil((1 / 5) * (9 * (9 / 4)**(k - 1) - 4))     # unknown
CIURA2001: GapFunction = lambda n, k: (1, 4, 10, 23, 57, 132, 301, 701)[min(k - 1, 7)]     # unknown


def gapgen(length: int, gap_function: GapFunction) -> list[int]:
    """
    Generate all gap sizes to sort an array of size `n` based on `gap_function`.

    > parameters
    - `length`: length of the array to sort
    - `gap_function`: function to generate gaps
    - `return`: list containing gap sizes
    """
    gaps = [int(gap_function(length, 1))]
    if gaps[0] > 1:
        for k in range(2, length + 3):
            gap = int(gap_function(length, k))
            gaps.append(gap)
            if gap == 1:
                break
    else:
        for k in range(2, length + 3):
            gap = int(gap_function(length, k))
            if gap >= length or gap == gaps[-1]:
                break
            gaps.append(gap)
        gaps.reverse()
    return gaps


def shellsort(array: list[float], gap_function: GapFunction = CIURA2001):
    """
    Sort `array` using shellsort.

    > complexity
    - time: `O(n * (log(n)/log(log(n)))**2)` for any gap function
    - space: `O(1)`

    > parameters
    - `array`: array to be sorted
    - `gap_function`: funcion to generate gaps
    - `return`: `array` sorted
    """
    gaps = gapgen(len(array), gap_function)
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
        (
            ('             shellsort Shell 1959', lambda array: shellsort(array, gap_function=SHELL1959)),
            ('      shellsort FrankLazarus 1960', lambda array: shellsort(array, gap_function=FRANKLAZARUS1960)),
            ('           shellsort Hibbard 1963', lambda array: shellsort(array, gap_function=HIBBARD1963)),
            ('shellsort Papernov Stasevich 1965', lambda array: shellsort(array, gap_function=PAPERNOVSTASEVICH1965)),
            ('             shellsort Knuth 1973', lambda array: shellsort(array, gap_function=KNUTH1973)),
            ('         shellsort Sedgewick 1982', lambda array: shellsort(array, gap_function=SEDGEWICK1982)),
            ('            shellsort Tokuda 1992', lambda array: shellsort(array, gap_function=TOKUDA1992)),
            ('             shellsort Ciura 2001', lambda array: shellsort(array, gap_function=CIURA2001)),
        ),
        bench_sizes=(0, 1, 10, 100, 1000),
    )


if __name__ == '__main__':
    test()
