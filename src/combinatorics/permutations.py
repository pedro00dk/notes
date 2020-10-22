def count_permutations(n: int, /, k: int = None):
    """
    Count permutations of `k` size in `n` elements.
    ```
    P(n, k) = ∏ i:[0,k) n - i = n!/(n - k)!
    ```
    > optimizations:
    - cancel most of the multiplications by multiplying only the range [numerator:denominator)

    > complexity:
    - time: `O(n)`
    - space: `O(1)`

    > parameters:
    - `n: int`: number of items
    - `k: int? = n`: size of groups

    > `return: int`: P(n, k)
    """
    k = k if k is not None else n
    if n < 0 or k < 0 or k > n:
        return 0
    p = 1
    for i in range(n, n - k, -1):
        p *= i
    return p


def permutations_cycle(items: list, /, k: int = None):
    """
    Permutation algorithm based on permutation cycles (orbits).
    This algorithm allows subset permutations of a fixed size `k` by using reduced k-cycles.

    > complexity:
    - time: `O(n**k)`, for `k == n` it can be approximated to `O(n!)`, although `O(n**n) ~ O(n!)`
    - space: `O(n! * n)` or `O(n)` if permutations are not stored

    > parameters:
    - `items: any[]`: items to generate the permutations
    - `k: int = len(items)`: size of groups (k-cycle size)

    > `return: iter<any()>`: iter of `items` permutations of `k` size
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


def permutations_heap(items: list):
    """
    Heap algorithm for generating permutations of items.
    This algorithm minimizes the amount of swaps in the list of items.

    > complexity:
    - time: `O(n!)`
    - space: `O(n! * n)` or `O(n)` if permutations are not stored

    > parameters:
    - `items: any[]`: items to generate the permutations

    > `return: iter<any()>`: iter of `items` permutations
    """
    n = len(items)
    if n == 0:
        yield ()
        return

    def rec(items: list, k: int):
        if k == 1:
            yield (*items,)
            return
        yield from rec(items, k - 1)
        for i in range(k - 1):
            swap_index = i if i % 2 == 0 else 0
            items[swap_index], items[k - 1] = items[k - 1], items[swap_index]
            yield from rec(items, k - 1)

    yield from rec(items, len(items))


def test():
    import itertools
    import math
    from ..test import benchmark
    benchmark(
        [
            ('        count permutations', lambda n: count_permutations(n, n)),
            (' count permutations native', lambda n: math.perm(n, n)),
            ('       permutations cycles', lambda n: [*permutations_cycle([*range(n)])]),
            ('         permutations heap', lambda n: [*permutations_heap([*range(n)])]),
            ('       permutations native', lambda n: [*itertools.permutations(range(n))]),
        ],
        test_inputs=range(5),
        bench_sizes=(0, 1, *range(2, 11, 2)),
        bench_input=lambda s: s,
        bench_repeat=1,
        bench_tries=100,
    )


if __name__ == '__main__':
    test()
