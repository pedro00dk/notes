import math


def radixsort_lsd(array: list, /, power=4):
    """
    Radixsort Least-Significant-Digit implementation.
    This implementation only supports integer values.
    Use bucketsort for floating-point values.

    This implementation can subwords of 2**power bases (default is 2**4 = 16).
    10**power bases are not supported due to focus in speed (2**power bases allow bit manupulation).

    Since this implementation has no fixed base, the time and space complexity will vary with `power`.
    By increasing `power`, the word size `w` becomes smaller, reducing a bit the amount of countingsort calls.
    However, countingsort's internal `k` (value-range, but in radixsort variation, it is the mask bit size) grows.
    Increasing `power` results in better time performance for larger arrays because decreases the amount of countingsort
    executions a the cost of a very small increment in countingsort's frequencies array.
    However, this cost on small arrays is much more pronounced, worsening the performance.

    > complexity:
    - time: `O(n * w)` where `w` is `log(value_range, 2**power)`
    - space: `O(n + w)` where `w` is `log(value_range, 2**power)`

    > parameters:
    - `array: int[]`: array to be sorted
    - `power: int? = 4`: the amount of bits to use as radix

    > `return: typeof(array)`: `array` sorted
    """
    if len(array) == 0:
        return array

    def radix_countingsort(array: list, output: list, radix: int, shift: int, min_value: int):
        """
        Countingsort implementation for radixsort lsd partial subsort.
        This implementation partially sorts the array using the provided mask region.
        This implementation is modified to reuse the same arrays in consecutive calls and reduce memory allocation.
        The last loop is reversed to maintain the stable property, preserving the least significant digits ordering from
        previous iterations.
        """
        radix_range = (radix >> shift) + 1
        frequencies = [0] * radix_range
        for value in array:
            frequencies[(value - min_value & radix) >> shift] += 1
        for i in range(1, len(frequencies)):
            frequencies[i] += frequencies[i - 1]
        for value in reversed(array):
            masked = (value - min_value & radix) >> shift
            output[frequencies[masked] - 1] = value
            frequencies[masked] -= 1

    min_value = min(array)
    max_value = max(array)
    value_range = max_value - min_value + 1
    base = 2**power
    word_size = math.ceil(math.log(max(value_range, 2), base))
    input = array
    output = [0] * len(array)
    for i in range(word_size):
        shift = i * power
        radix = (base - 1) << shift
        radix_countingsort(input, output, radix, shift, min_value)
        input, output = output, input
    if array != input:
        array[:] = input
    return array


def radixsort_msd(array: list, /, power=4):
    """
    Radixsort Most-Significant-Digit implementation.
    This implementation only supports integer values.
    Use bucketsort for floating-point values.
    The pure radixsort msd variation (radixsort + countingsort only) is slightly slower than the lsd variation.
    This is caused by bigger constants that come from very large amount of countingsort invocations, even though a
    divide an conquer is used in the msd variation.
    Radixsort msd variation performance can be improved by using a second subsort algorithm such as quicksort when the
    groups get smaller.

    This implementation can subwords of 2**power bases (default is 2**4 = 16).
    10**power bases are not supported due to focus in speed (2**power bases allow bit manupulation).

    Since this implementation has no fixed base, the time and space complexity will vary with `power`.
    By increasing `power`, the word size `w` becomes smaller.
    Different from the lsd variation, countingsort is executed much more often in the msd, regardless of `power`,
    because if power is small, the number of groups is also small, but the recussion depth is greater, and if power is
    big, the recurssion depth gets smaller but there will many more groups to recur into.
    So there is not too much benefit in increasing it too much, because the performance gets worse very fast.

    > complexity:
    - time: `O(n * w)` where `w` is `log(value_range, 2**power)`
    - space: `O(n + w)` where `w` is `log(value_range, 2**power)`

    > parameters:
    - `array: int[]`: array to be sorted
    - `power: int? = 4`: the amount of bits to use as radix

    > `return: typeof(array)`: `array` sorted
    """
    if len(array) == 0:
        return array

    def radix_countingsort(array: list, output: list, first: int, last: int, radix: int, shift: int, min_value: int):
        """
        Countingsort implementation for radixsort msb partial subsort.
        This implementation partially sorts the array using the provided mask region.
        This implementation is modified to reuse the same arrays in consecutive calls and reduce memory allocation.
        Only the section between first and last is ordered.
        The accumulated frequencies are returned to reused as indices for recursive calls.
        """
        radix_range = (radix >> shift) + 1
        frequencies = [0] * radix_range
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

    def rec(input: list, output: list, first: int, last: int, word_size_index: int, base: int, power: int, min_value: int):
        shift = word_size_index * power
        radix = (base - 1) << shift
        frequencies = radix_countingsort(input, output, first, last, radix, shift, min_value)
        input[first:last + 1] = (output[i] for i in range(first, last + 1))
        word_size_index -= 1
        if word_size_index < 0:
            return
        for i in range(0, len(frequencies)):
            next_first = first + frequencies[i]
            next_last = first + frequencies[i + 1] - 1 if i + 1 < len(frequencies) else last
            if next_first < next_last:
                rec(input, output, next_first, next_last, word_size_index, base, power, min_value)

    min_value = min(array)
    max_value = max(array)
    value_range = max_value - min_value + 1
    base = 2**power
    word_size = math.ceil(math.log(max(value_range, 2), base))
    input = array
    output = [0] * len(array)
    rec(input, output, 0, len(array) - 1, word_size - 1, base, power, min_value)
    return array


def test():
    from ..test import benchmark
    benchmark(
        [
            ('radixsort lsd p=1', radixsort_lsd, 'radixsort_lsd(array, 1)'),
            ('radixsort lsd p=2', radixsort_lsd, 'radixsort_lsd(array, 2)'),
            ('radixsort lsd p=3', radixsort_lsd, 'radixsort_lsd(array, 3)'),
            ('radixsort lsd p=4', radixsort_lsd, 'radixsort_lsd(array, 4)'),
            ('radixsort lsd p=5', radixsort_lsd, 'radixsort_lsd(array, 5)'),
            ('radixsort lsd p=6', radixsort_lsd, 'radixsort_lsd(array, 6)'),
            ('radixsort msd p=1', radixsort_msd, 'radixsort_msd(array, 1)'),
            ('radixsort msd p=2', radixsort_msd, 'radixsort_msd(array, 2)'),
            ('radixsort msd p=3', radixsort_msd, 'radixsort_msd(array, 3)'),
            ('radixsort msd p=4', radixsort_msd, 'radixsort_msd(array, 4)'),
            ('radixsort msd p=5', radixsort_msd, 'radixsort_msd(array, 5)'),
            ('radixsort msd p=6', radixsort_msd, 'radixsort_msd(array, 6)')
        ]
    )


if __name__ == '__main__':
    test()
