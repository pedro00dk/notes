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
    n = len(items)
    if n == 0:
        yield ()
        return

    def rec(items: list, k: int, n: int, index: int, first: int, indices: list):
        if index == k:
            yield (*(items[i] for i in indices),)
            return
        for i in range(first, (index + n - k) + 1):
            indices[index] = i
            yield from rec(items, k, n, index + 1, i + 1, indices)

    yield from rec(items, k, n, 0, 0, [*range(k)])


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


def test():
    from ..test import benchmark
    benchmark(
        [
            ('count recursive', lambda args: f'C({args[0]}, {args[1]}) = {combinations_count_rec(*args)}'),
            ('  count default', lambda args: f'C({args[0]}, {args[1]}) = {combinations_count_def(*args)}'),
            ('      recursive', lambda args: [*combinations_rec([*range(args[0])], args[1])]),
            ('      iterative', lambda args: [*combinations_itr([*range(args[0])], args[1])])
        ],
        test_input_iter=((5, 2), (0, 0), (2, 0), (2, 1), (4, 3), (6, 2), (6, 5), (8, 6), (6, 3)),
        bench_size_iter=range(16),
        bench_input=lambda s, r: (s, s // 2),
        bench_tries=100
    )


if __name__ == '__main__':
    test()
