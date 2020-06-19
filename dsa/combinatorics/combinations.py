import itertools

from .factorial import factorial_itr
from .permutations import permutations_count


def combinations_count_rec(n: int, k: int):
    """
    Recursive implementation of `n` combinations of `k`size using pascal triangle properties.
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
    - `k: int`: size of groups

    > `return: int`: C(n, k)
    """
    return 1 if n <= 1 or k == 0 or n == k else combinations_count_rec(n - 1, k - 1) + combinations_count_rec(n - 1, k)


def combinations_count_def(n: int, k: int):
    """
    Count `n` combinations of `k`size using permutation divisions.
    ```
    C(n, k) = P(n, k) / P(k, k) = (n!/(n-k)!) / (k!/(k-k)!) = P(n, k)/k! = (n!/(n - k)!)/k! = n!/((n-k)!k!)
    ```

    > optimizations:
    - since `C(n, k) == P(n, k)/k! (third do last formula) == P(n, n-k)/(n-k)! (k complement)`
      - minimize `k` by making it the minimum of `k` and `n - k`
        - increase the P(n, k) denominator `n - k`, reducing the amount of multiplications (in optimized implementation)
        - decrease factorial multiplications of `k` in iteractive algorithm
    - strats multiplying and dividing at the same time are not necessary in python due to dynamic integer precision
      - reduces division and multiplication operations, but increased cost on very large values

    > complexity:
    - time: `O(n)`
    - space: `O(1)`

    > parameters:
    - `n: int`: number of items
    - `k: int`: size of groups

    > `return: int`: C(n, k)
    """
    k = min(k, n - k)
    return permutations_count(n, k) // factorial_itr(k)


def combinations_rec(items: list, k: int):
    """
    Recursive implementation of combinations generator.

    > complexity:
    - time: `O(C(n, k))`
    - space: `O(C(n, k) * n)` or `O(n)` if combinations are not stored

    > parameters:
    - `items: any[]`: items to generate combinations
    - `k: int`: size of groups

    > `return: Generator<any()>`: generator of `items` combinations of `k` size
    """
    def rec(items: list, combination: list, n: int, k: int, at: int, count: int):
        if count == k or n == 0:
            yield (*combination,)
            return
        for i in range(at, n - (k - count) + 1):
            combination[count] = items[i]
            yield from rec(items, combination, n, k, i + 1, count + 1)

    yield from rec(items, [None] * k, len(items), k, 0, 0)


def combinations_itr(items: list, k: int):
    """
    Iterative implementation of combinations generator.

    > complexity:
    - time: `O(C(n, k))`
    - space: `O(C(n, k) * n)` or `O(n)` if combinations are not stored

    > parameters:
    - `items: any[]`: items to generate combinations
    - `k: int`: size of groups

    > `return: Generator<any()>`: generator of `items` combinations of `k` size
    """
    n = len(items)
    if n == 0 or k <= 0 or k > n:
        yield ()
        return
    indices = [*range(k)]
    yield (*(items[i] for i in indices),)
    while True:
        for i in range(k - 1, -1, -1):
            if indices[i] < i + n - k:
                break
            if i > 0:
                continue
            return
        indices[i] += 1
        for j in range(i + 1, k):
            indices[j] = indices[j - 1] + 1
        yield (*(items[i] for i in indices),)


def bit_combinations_rec_range(n: int, k: int):
    """
    Recursive implementation of bit combinations generator.
    Implementation based on ranging current set bit from `at` to `n - (remaining k) + 1`.
    Recursion depth goes up to `k`.

    > optimizations:
    - ignore `count` variable in recursive function because set bit order does not matter (see `combinations_rec`)

    > complexity:
    - time: `O(C(n, k))`
    - space: `O(C(n, k))` or `O(1)` if numbers are not stored

    > parameters:
    - `n: int`: number of bits
    - `k: int`: number of `1` bits

    > `return: Generator<int>`: generator of `n` bits combinations of `k` size
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
    Recursive implementation of bit combinations generator.
    Implementation based on seting or unseting bit at `at` position anb branching to the next possition.
    Recursion depth goes up to `n`.
    This implementation is slightly slower than the range based.

    > complexity:
    - time: `O(C(n, k))`
    - space: `O(C(n, k))` or `O(1)` if numbers are not stored

    > parameters:
    - `n: int`: number of bits
    - `k: int`: number of `1` bits

    > `return: Generator<int>`: generator of `n` bits combinations of `k` size
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

    def test_native_based_bit_combinations(n: int, k: int):
        for combination in itertools.combinations([*range(n)], k):
            v = 0
            for i in combination:
                v |= 1 << i
            yield v

    benchmark(
        [
            ('     count recursive', lambda args: f'C({args[0]}, {args[1]}) = {combinations_count_rec(*args)}'),
            ('       count default', lambda args: f'C({args[0]}, {args[1]}) = {combinations_count_def(*args)}'),
            ('        count native', lambda args: f'C({args[0]}, {args[1]}) = {math.comb(*args)}'),
            ('           recursive', lambda args: [*combinations_rec([*range(args[0])], args[1])]),
            ('           iterative', lambda args: [*combinations_itr([*range(args[0])], args[1])]),
            ('              native', lambda args: [*itertools.combinations([*range(args[0])], args[1])]),
            (' recursive range bit', lambda args: [*bit_combinations_rec_range(*args)]),
            ('recursive branch bit', lambda args: [*bit_combinations_rec_branch(*args)]),
            ('          native bit', lambda args: [*test_native_based_bit_combinations(*args)])
        ],
        test_input_iter=((5, 2), (0, 0), (2, 0), (2, 1), (4, 3), (6, 2), (6, 5), (8, 6), (6, 3)),
        bench_size_iter=range(20),
        bench_input=lambda s, r: (s, s // 2)
    )


if __name__ == '__main__':
    test()
