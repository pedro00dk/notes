import math
from typing import Callable, Optional, cast


def radixsort_lsd(array: list[int], block: Optional[int] = None) -> list[int]:
    """
    Sort `array` using Least-Significant-Digit radixsort.
    This implementation only supports integer values.
    Use bucketsort for floating-point values.

    The `block` parameter is used to define the radix `base`, which is `2**block`.
    The `word` size in binary representation (or when `base` = 2) is `word = log(value_range, 2)`.
    The `word` size is smaller for increasing `base` sizes, `word = log(value_range, base)`.
    `word` size is also exactly the amount of internal countingsort calls.

    Linear complexity is achieved when `n` (array length) is approximately `base`, meaning `block = ceil(log(n, 2))`.
    By having `base` ~ `n`, the asymptotic complexity of countingsort calls do not increase
    (`k` = `base`, `k` ~ `n`, then `O(n + k)` is still `O(n)`), also the number of countingsort calls will be
    `log(value_range, n)`, which tends to 1 when `n` tends to infinity.

    For most cases, the default `block` will provide the best performance, but for a `value_range` much smaller than
    `n`, a smaller `block` size may provide better performance.

    > complexity
    - time: `O(n * w)`
    - space: `O(n + w)`
    - `n`: length of `array`
    - `w`: `log(value_range, 2**block)`

    > parameters
    - `array`: array to be sorted
    - `block`: the amount of bits to use as radix, defaults to the number of bits needed to represent `array` length
    - `return`: `array` sorted
    """
    def radix_countingsort(array: list[int], output: list[int], base: int, block: int, index: int, min_value: int):
        """
        Countingsort implementation for radixsort lsd partial subsort.
        This implementation partially sorts the array using the provided mask region.
        This implementation is modified to reuse the same arrays in consecutive calls and reduce memory allocation.
        The last loop is reversed to maintain the stable property, preserving the least significant digits ordering from
        previous iterations.
        """
        shift = index * block
        radix = (base - 1) << shift
        frequencies = [0] * base
        for value in array:
            frequencies[(value - min_value & radix) >> shift] += 1
        for i in range(1, len(frequencies)):
            frequencies[i] += frequencies[i - 1]
        for value in reversed(array):
            masked = (value - min_value & radix) >> shift
            output[frequencies[masked] - 1] = value
            frequencies[masked] -= 1

    if len(array) == 0:
        return array
    min_value = min(array)
    max_value = max(array)
    value_range = max_value - min_value + 1
    block = max(block if block is not None else math.ceil(math.log2(max(len(array), 1))), 1)
    base = 2**block
    word = math.ceil(math.log(max(value_range, 2), base))
    input = array
    output = [0] * len(array)
    for i in range(word):
        radix_countingsort(input, output, base, block, i, min_value)
        input, output = output, input
    if array != input:
        array[:] = input
    return array


def radixsort_msd(array: list[int], block: int = 4) -> list[int]:
    """
    Sort `array` using Most-Significant-Digit radixsort.
    This implementation only supports integer values.
    Use bucketsort for floating-point values.

    The `block` parameter is used to define the radix `base`, which is `2**block`.
    The `word` size in binary representation (or when `base` = 2) is `word = log(value_range, 2)`.
    The `word` size is smaller for increasing `base` sizes, `word = log(value_range, base)`.

    Linear complexity is achieved when `n` (array length) is approximately `base`, meaning `block = ceil(log(n, 2))`.
    By having `base` ~ `n`, the asymptotic complexity of countingsort calls do not increase
    (`k` = `base`, `k` ~ `n`, then `O(n + k)` is still `O(n)`), also the number of countingsort calls will be
    `log(value_range, n)`, which tends to 1 when `n` tends to infinity.

    However in practice, msd radix sort is slower than the lsd variation.
    This is caused by bigger constants that come from very large amount of countingsort invocations, even though a
    divide an conquer is used in the msd variation.
    Different from the lsd variation, countingsort is executed much more often in the msd, regardless of `block`,
    because if `block` is small, the number of groups is also small, but the recussion depth is greater, and if `block`
    is big, the recurssion depth gets smaller but there will many more groups to recur into.
    So there is not too much benefit in increasing it too much, because the performance gets worse very fast.

    A good experimental value for `block` is `4`, which is the default value.

    > complexity
    - time: `O(n * w)`
    - space: `O(n + w)`
    - `n`: length of `array`
    - `w`: `log(value_range, 2**block)`

    > parameters
    - `array`: array to be sorted
    - `block`: the amount of bits to use as radix, defaults to 4
    - `return`: `array` sorted
    """
    def radix_countingsort(array: list[int], output: list[int], first: int, last: int, base: int, block: int, index: int, min_value: int):
        """
        Countingsort implementation for radixsort msb partial subsort.
        This implementation partially sorts the array using the provided mask region.
        This implementation is modified to reuse the same arrays in consecutive calls and reduce memory allocation.
        Only the section between first and last is ordered.
        The accumulated frequencies are returned to reused as indices for recursive calls.
        """
        shift = index * block
        radix = (base - 1) << shift
        frequencies = [0] * base
        for i in range(first, last + 1):
            frequencies[(array[i] - min_value & radix) >> shift] += 1
        for i in range(1, len(frequencies)):
            frequencies[i] += frequencies[i - 1]
        for i in range(first, last + 1):
            value = array[i]
            masked = (value - min_value & radix) >> shift
            output[first + frequencies[masked] - 1] = value
            frequencies[masked] -= 1
        return frequencies

    def rec(input: list[int], output: list[int], first: int, last: int, base: int, block: int, word_remaining: int, min_value: int):
        frequencies = radix_countingsort(input, output, first, last, base, block, word_remaining, min_value)
        input[first:last + 1] = (output[i] for i in range(first, last + 1))
        word_remaining -= 1
        if word_remaining < 0:
            return
        for i in range(0, len(frequencies)):
            next_first = first + frequencies[i]
            next_last = first + frequencies[i + 1] - 1 if i + 1 < len(frequencies) else last
            if next_first < next_last:
                rec(input, output, next_first, next_last, base, block, word_remaining, min_value)

    if len(array) == 0:
        return array
    min_value = min(array)
    max_value = max(array)
    value_range = max_value - min_value + 1
    block = max(block if block is not None else math.ceil(math.log2(max(len(array), 1))), 1)
    base = 2**block
    word = math.ceil(math.log(max(value_range, 2), base))
    input = array
    output = [0] * len(array)
    rec(input, output, 0, len(array) - 1, base, block, word - 1, min_value)
    return array


def test():
    from ..test import sort_benchmark

    sort_lsd = cast(Callable[[list[float], Optional[int]], list[float]], radixsort_lsd)
    sort_msd = cast(Callable[[list[float], Optional[int]], list[float]], radixsort_msd)
    sort_benchmark(
        (
            ('radixsort lsd block=1', lambda array: sort_lsd(array, 1)),
            ('radixsort lsd block=2', lambda array: sort_lsd(array, 2)),
            ('radixsort lsd block=3', lambda array: sort_lsd(array, 3)),
            ('radixsort lsd block=4', lambda array: sort_lsd(array, 4)),
            ('radixsort lsd block=5', lambda array: sort_lsd(array, 5)),
            ('radixsort lsd block=6', lambda array: sort_lsd(array, 6)),
            ('radixsort lsd block=n', lambda array: sort_lsd(array, None)),
            ('radixsort msd block=1', lambda array: sort_msd(array, 1)),
            ('radixsort msd block=2', lambda array: sort_msd(array, 2)),
            ('radixsort msd block=3', lambda array: sort_msd(array, 3)),
            ('radixsort msd block=4', lambda array: sort_msd(array, 4)),
            ('radixsort msd block=5', lambda array: sort_msd(array, 5)),
            ('radixsort msd block=6', lambda array: sort_msd(array, 6)),
        ),
    )


if __name__ == '__main__':
    test()
