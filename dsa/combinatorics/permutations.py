def permutations_count(n: int, /, k: int = None):
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

    > `return: Generator<any()>`: generator of `items` permutations of `k` size
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


def permutations_heap_rec(items: list):
    """
    Heap algorithm for generating permutations of items.
    This algorithm minimizes the amount of swaps in the list of items.

    > complexity:
    - time: `O(n!)`
    - space: `O(n! * n)` or `O(n)` if permutations are not stored

    > parameters:
    - `items: any[]`: items to generate the permutations

    > `return: Generator<any()>`: generator of `items` permutations
    """
    n = len(items)
    if n == 0:
        yield ()
        return

    def rec(items: list, k: int):
        if k == 1:
            yield (*items,)
            return
        yield from rec(items, k=k - 1)
        for i in range(k - 1):
            swap_index = i if i % 2 == 0 else 0
            items[swap_index], items[k - 1] = items[k - 1], items[swap_index]
            yield from rec(items, k=k - 1)

    yield from rec(items, len(items))


def permutations_heap_itr(items: list):
    """
    Iterative version of the permutation_heap algorithm.

    > complexity:
    - time: `O(n!)`
    - space: `O(n! * n)` or `O(n)` if permutations are not stored

    > parameters:
    - `items: any[]`: elements to generate the permutations

    > `return: Generator<any()>`: generator of `items` permutations
    """
    n = len(items)
    if n == 0:
        yield ()
        return
    k = 0
    i = [0] * n
    yield (*items,)
    while k < n:
        if i[k] >= k:
            i[k] = 0
            k += 1
            continue
        swap_index = i[k] if i[k] % 2 == 0 else 0
        items[swap_index], items[k] = items[k], items[swap_index]
        yield (*items,)
        i[k] += 1
        k = 0


def test():
    import itertools
    from ..test import benchmark
    benchmark(
        [
            ('         count', lambda n: f'P({n}, {n}) = {permutations_count(n)}'),
            ('        cycles', lambda n: [*permutations_cycle([*range(n)])]),
            ('heap recursive', lambda n: [*permutations_heap_rec([*range(n)])]),
            ('heap iterative', lambda n: [*permutations_heap_itr([*range(n)])]),
            ('        native', lambda n: [*itertools.permutations([*range(n)])]),
        ],
        test_input_iter=range(5),
        bench_size_iter=range(10),
        bench_input=lambda s, r: s
    )


if __name__ == '__main__':
    test()
