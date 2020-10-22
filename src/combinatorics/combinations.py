import itertools

from .factorial import factorial_itr
from .permutations import count_permutations


def count_combinations_rec(n: int, k: int):
    """
    Implementation of combinations of `n` items of `k`size using pascal triangle properties.
    ```
    C(n, k) = {
        1 if n == 0 or k == 0 or n == k,
        C(n-1, k-1) + C(n-1, k)
    }
    ```

    > complexity:
    - time: `O(min(n**k, n**(n-k)))`
    - space: `O(n)` 

    > parameters:
    - `n: int`: number of items
    - `k: int`: size of combinations

    > `return: int`: C(n, k)
    """
    return 1 if n <= 1 or k == 0 or n == k else count_combinations_rec(n - 1, k - 1) + count_combinations_rec(n - 1, k)


def count_combinations_itr(n: int, k: int):
    """
    Implementation of combinations of `n` items of `k`size using permutation divisions.
    ```
    C(n, k) = P(n, k) / P(k, k) = (n!/(n-k)!) / (k!/(k-k)!) = P(n, k)/k! = (n!/(n - k)!)/k! = n!/((n-k)!k!)
    ```

    > optimizations:
    - since `C(n, k) == P(n, k)/k! (third do last formula) == P(n, n-k)/(n-k)! (k complement)`
      - minimize `k` by making it the minimum of `k` and `n - k`
        - increase the P(n, k) denominator `n - k`, reducing the amount of multiplications (in optimized implementation)
        - decrease factorial multiplications of `k` in iteractive algorithm
    - multiplying and dividing at the same time is not necessary in python due to dynamic integer precision
      - reduces division and multiplication operations, but increased cost on very large values

    > complexity:
    - time: `O(n)`
    - space: `O(1)`

    > parameters:
    - `n: int`: number of items
    - `k: int`: size of combinations

    > `return: int`: C(n, k)
    """
    k = min(k, n - k)
    return count_permutations(n, k) // factorial_itr(k)


def combinations(items: list, k: int):
    """
    Implementation of combinations generator.

    > complexity:
    - time: `O(C(n, k))`
    - space: `O(C(n, k) * n)` or `O(n)` if combinations are not stored

    > parameters:
    - `items: any[]`: items to generate combinations
    - `k: int`: size of combinations

    > `return: iter<any()>`: iterator of `items` combinations of `k` size
    """
    def rec(items: list, combination: list, n: int, k: int, at: int):
        if k == 0 or n == 0:
            yield (*combination,)
            return
        for i in range(at, n - k + 1):
            combination[len(combination) - k] = items[i]
            yield from rec(items, combination, n, k - 1, i + 1)

    yield from rec(items, [None] * k, len(items), k, 0)


def bit_combinations_range(n: int, k: int):
    """
    Implementation of bit combinations generator.
    Implementation based on ranging current set bit from `at` to `n - (remaining k) + 1`.
    Recursion depth goes up to `k`.

    > complexity:
    - time: `O(C(n, k))`
    - space: `O(C(n, k))` or `O(1)` if numbers are not stored

    > parameters:
    - `n: int`: number of bits
    - `k: int`: number of `1` bits

    > `return: iter<int>`: iterator of `n` bits combinations of `k` size
    """
    def rec(bits: int, n: int, k: int, at: int):
        if k == 0:
            yield bits
            return
        for i in range(at, n - k + 1):
            yield from rec(bits | (1 << i), n, k - 1, i + 1)

    yield from rec(0, n, k, 0)


def bit_combinations_rec_branch(n: int, k: int):
    """
    Implementation of bit combinations generator.
    Implementation based on setting or unsetting bit at `at` position and branching to the next position.
    Recursion depth goes up to `n`.
    This implementation is slightly slower than the range based.

    > complexity:
    - time: `O(C(n, k))`
    - space: `O(C(n, k))` or `O(1)` if numbers are not stored

    > parameters:
    - `n: int`: number of bits
    - `k: int`: number of `1` bits

    > `return: iter<int>`: iterator of `n` bits combinations of `k` size
    """
    def rec(bits: int, n: int, k: int, at: int):
        if k == 0 or n == 0:
            yield bits
            return
        yield from rec(bits | (1 << at), n, k - 1, at + 1)
        if at < n - k:
            yield from rec(bits, n, k, at + 1)

    yield from rec(0, n, k, 0)


def test():
    import math
    from ..test import benchmark

    def test_bit_combinations_native(n: int, k: int):
        for combination in itertools.combinations(range(n), k):
            v = 0
            for i in combination:
                v |= 1 << i
            yield v

    benchmark(
        [
            ('        count recursive', lambda args: count_combinations_rec(*args)),
            ('        count iterative', lambda args: count_combinations_itr(*args)),
            ('           count native', lambda args: math.comb(*args)),
            ('           combinations', lambda args: [*combinations([*range(args[0])], args[1])]),
            ('    combinations native', lambda args: [*itertools.combinations([*range(args[0])], args[1])]),
            (' bit combinations range', lambda args: [*bit_combinations_range(*args)]),
            ('bit combinations branch', lambda args: [*bit_combinations_rec_branch(*args)]),
            ('bit combinations native', lambda args: [*test_bit_combinations_native(*args)])
        ],
        test_inputs=((5, 2), (0, 0), (2, 0), (2, 1), (4, 3), (6, 2), (6, 5), (8, 6), (6, 3)),
        bench_sizes=(0, 1, *range(2, 21, 2)),
        bench_input=lambda s: (s, s // 2),
        bench_repeat=1,
        bench_tries=100
    )


if __name__ == '__main__':
    test()
