import math


def factorial_rec(n: int):
    """
    Factorial algorithm, recursive implementation.
    ```
    n! = {
        1 if n == 0,
        n * (n - 1)!
    }
    ```

    > optimizations:
    - skip `n == 1` and `n == 0` steps because `1! == 1` and `0! == 1`

    > complexity:
    - time: `O(n)`
    - space: `O(log(n))`

    > parameters:
    - `n: int`: value to compute factorial

    > `return: int`: factorial of `n`
    """
    return 1 if n <= 1 else n * factorial_rec(n - 1)


def factorial_itr(n: int):
    """
    Factorial algorithm, interactive implementation.
    ```
    n! = ∏ i=[1:n] i
    ```

    > optimizations:
    - start loop from 2 because `0! == 1` and `1! == 1`

    > complexity:
    - time: `O(n)`
    - space: `O(1)`

    > parameters:
    - `n: int`: value to compute factorial

    > `return: int`: factorial of `n`
    """
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def factorial_stirling(n: float):
    """
    Stirling's factorial approximation.

    > complexity:
    - time: `O(1)`
    - space: `O(1)`

    > parameters:
    - `n: float`: value to compute factorial

    > `return: int`: factorial approximation of `n`
    """
    return (2 * math.pi * n) ** (0.5) * (n / math.e) ** n


def factorial_ramanujan(n: float):
    """
    Ramanujan's factorial approximation. Much more precise than Stirling's.

    > complexity:
    - time: `O(1)`
    - space: `O(1)`

    > parameters:
    - `n: int`: value to compute factorial

    > `return: int`: factorial approximation of `n`
    """
    return math.pi ** 0.5 * (1 / 30 + n * (1 + n * (4 + n * 8))) ** (1 / 6) * (n / math.e) ** n


def test():
    from ..test import benchmark
    benchmark(
        [
            (' recursive', factorial_rec),
            ('iteractive', factorial_itr),
            ('  stirling', factorial_stirling),
            (' ramanujan', factorial_ramanujan),
            ('    native', math.factorial)

        ],
        test_input_iter=(0, 1, 5, 10, 20, 30, 40, 50),
        bench_size_iter=range(0, 101, 10),
        bench_input=lambda s, r: s,
        bench_tries=100000
    )


if __name__ == '__main__':
    test()
