from typing import Generator, Optional, TypeVar

T = TypeVar('T')


def permutation(n: int, k: Optional[int] = None) -> int:
    """
    Count possible permutations of `k` size in `n` elements.

    > optimizations
    - cancel most of the multiplications by multiplying only the range [numerator:denominator)

    > complexity
    - time: `O(n)`
    - space: `O(1)`
    - `n`: absolute value of parameter `n`

    > parameters
    - `n`: number of items
    - `k`: size of permutations, defaults to `n`
    - `return`: the permutation `P(n, k)`
    """
    k = k if k is not None else n
    if n < 0 or k < 0 or k > n:
        return 0
    p = 1
    for i in range(n, n - k, -1):
        p *= i
    return p


def permutations_cycle(items: list[T], k: Optional[int] = None) -> Generator[tuple[T, ...], None, None]:
    """
    Generate permutations of `items` optionally containing `k` elements.
    Permutation algorithm based on permutation cycles (orbits).

    > complexity
    - time: `O(n**k)`, for `k == n` it can be approximated to `O(n!)`, although `O(n**n) ~ O(n!)`
    - space: `O(n)` or `O(n! * n)` if permutations are stored
    - `n`: absolute value of parameter `n`
    - `k`: absolute value of parameter `k`

    > parameters
    - `items`: items to generate the permutations
    - `k`: size of groups (k-cycle size)
    - `return`: `items` permutations of `k` size
    """
    n = len(items)
    k = k if k is not None else n
    if n == 0 or k <= 0 or k > n:
        yield ()
        return
    cycles = [*range(k)]
    indices = [*range(n)]
    yield (*(items[j] for j in indices[:k]),)
    while True:
        for i in range(k - 1, -1, -1):
            cycles[i] += 1
            if cycles[i] == n:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = i
                if i > 0:
                    continue
                return
            indices[i], indices[cycles[i]] = indices[cycles[i]], indices[i]
            yield (*(items[j] for j in indices[:k]),)
            break


def permutations_heap(items: list[T]) -> Generator[tuple[T, ...], None, None]:
    """
    Generate permutations of `items` using the heap algorithm.
    This algorithm minimizes the amount of swaps in the list of items.

    > complexity
    - time: `O(n!)`
    - space: `O(n)` or `O(n! * n)` if permutations are stored
    - `n`: absolute value of parameter `n`

    > parameters
    - `items`: items to generate the permutations
    - `return`: `items` permutations
    """
    def rec(items: list[T], k: int) -> Generator[tuple[T, ...], None, None]:
        if k == 1:
            yield (*items,)
            return
        yield from rec(items, k - 1)
        for i in range(k - 1):
            swap_index = i if i % 2 == 0 else 0
            items[swap_index], items[k - 1] = items[k - 1], items[swap_index]
            yield from rec(items, k - 1)

    if len(items) == 0:
        yield ()
        return
    yield from rec(items, len(items))


def test():
    import itertools
    import math

    from ..test import benchmark

    benchmark(
        (
            ('        count permutations', lambda n: permutation(n, n)),
            (' count permutations native', lambda n: math.perm(n, n)),
            ('       permutations cycles', lambda n: [*permutations_cycle([*range(n)])]),
            ('         permutations heap', lambda n: [*permutations_heap([*range(n)])]),
            ('       permutations native', lambda n: [*itertools.permutations(range(n))]),
        ),
        test_inputs=(*range(5),),
        bench_sizes=(0, 1, *range(2, 11, 2)),
        bench_input=lambda s: s,
    )


if __name__ == '__main__':
    test()
