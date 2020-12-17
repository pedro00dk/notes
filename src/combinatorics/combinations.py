import itertools
from typing import Generator, TypeVar
from .factorial import factorial_itr
from .permutations import permutation


T = TypeVar('T')


def combination_pascal(n: int, k: int) -> int:
    """
    Count possible combinations of `n` items of `k` size using pascal triangle properties.

    > complexity
    - time: `O(min(n**k, n**(n-k)))`
    - space: `O(n)` 

    > parameters
    - `n`: number of items
    - `k`: size of combinations
    - `return`: the combination `C(n, k)`
    """
    return 1 if n <= 1 or k == 0 or n == k else combination_pascal(n - 1, k - 1) + combination_pascal(n - 1, k)


def combination_perm(n: int, k: int) -> int:
    """
    Count possible combinations of `n` items of `k`size using permutation divisions.

    > optimizations
    - since `C(n, k) == P(n, k)/k! == P(n, n-k)/(n-k)! (k complement)`
      - minimize `k` by making it the minimum of `k` and `n - k`
        - increase the P(n, k) denominator `n - k`, reducing the amount of multiplications (in optimized implementation)
        - decrease factorial multiplications of `k` in iteractive algorithm
    - multiplying and dividing at the same time is not necessary in python due to dynamic integer precision
      - reduces division and multiplication operations, but increased cost on very large values

    > complexity
    - time: `O(n)`
    - space: `O(1)`

    > parameters
    - `n`: number of items
    - `k`: size of combinations
    - `return`: the combination `C(n, k)`
    """
    k = min(k, n - k)
    return permutation(n, k) // factorial_itr(k)


def combinations_range(items: list[T], k: int) -> Generator[tuple[T, ...], None, None]:
    """
    Generate `items` combinations of `k` size using range update strategy.

    > complexity
    - time: `O(C(n, k))`
    - space: `O(n)` or `O(C(n, k) * n)` if combinations are stored

    > parameters
    - `items`: items to generate combinations
    - `k`: size of combinations
    - `return`: `items` combinations of `k` size
    """
    def rec(items: list[T], k: int, combination: list[T], at: int) -> Generator[tuple[T, ...], None, None]:
        if len(items) == 0 or k == 0:
            yield (*combination,)
            return
        for i in range(at, len(items) - k + 1):
            combination[len(combination) - k] = items[i]
            yield from rec(items, k - 1, combination, i + 1)

    yield from rec(items, k, items[:k], 0)


def bit_combinations_range(n: int, k: int) -> Generator[int, None, None]:
    """
    Generate combinations of `n` bits size integers with `k` bits set using range update strategy.

    > complexity
    - time: `O(C(n, k))`
    - space: `O(1)` or `O(C(n, k))` if numbers are stored

    > parameters:
    - `n`: number of bits
    - `k`: number of `1` bits
    - `return`: `n` sized bits combinations with `k` bits set
    """
    def rec(bits: int, n: int, k: int, at: int) -> Generator[int, None, None]:
        if k == 0:
            yield bits
            return
        for i in range(at, n - k + 1):
            yield from rec(bits | (1 << i), n, k - 1, i + 1)

    yield from rec(0, n, k, 0)


def bit_combinations_branch(n: int, k: int) -> Generator[int, None, None]:
    """
    Generate combinations of `n` bits size integers with `k` bits set using branching strategy.

    > complexity
    - time: `O(C(n, k))`
    - space: `O(1)` or `O(C(n, k))` if numbers are stored

    > parameters
    - `n: int`: number of bits
    - `k: int`: number of `1` bits
    - `return`: `n` sized bits combinations with `k` bits set
    """
    def rec(bits: int, n: int, k: int, at: int) -> Generator[int, None, None]:
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

    def bit_combinations_native(n: int, k: int) -> Generator[int, None, None]:
        for combination in itertools.combinations(range(n), k):
            v = 0
            for i in combination:
                v |= 1 << i
            yield v

    benchmark(
        (
            ('           count pascal', lambda args: combination_pascal(*args)),
            ('             count perm', lambda args: combination_perm(*args)),
            ('           count native', lambda args: math.comb(*args)),
            ('           combinations', lambda args: [*combinations_range([*range(args[0])], args[1])]),
            ('    combinations native', lambda args: [*itertools.combinations([*range(args[0])], args[1])]),
            (' bit combinations range', lambda args: [*bit_combinations_range(*args)]),
            ('bit combinations branch', lambda args: [*bit_combinations_branch(*args)]),
            ('bit combinations native', lambda args: [*bit_combinations_native(*args)]),
        ),
        test_inputs=((5, 2), (0, 0), (2, 0), (2, 1), (4, 3), (6, 2), (6, 5), (8, 6), (6, 3)),
        bench_sizes=(0, 1, *range(2, 21, 2)),
        bench_input=lambda s: (s, s // 2),
    )


if __name__ == '__main__':
    test()
