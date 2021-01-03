import math


def factorial_rec(n: int) -> int:
    """
    Recursive factorial algorithm.

    > optimizations
    - skip `n == 1` and `n == 0` steps because `1! == 1` and `0! == 1`

    > complexity
    - time: `O(n)`
    - space: `O(log(n))`
    - `n`: absolute value of parameter `n`

    > parameters
    - `n`: value to compute factorial
    - `return`: factorial of `n`
    """
    return 1 if n <= 1 else n * factorial_rec(n - 1)


def factorial_itr(n: int) -> int:
    """
    Iterative factorial algorithm.

    > optimizations
    - start loop from 2 because `0! == 1` and `1! == 1`

    > complexity
    - time: `O(n)`
    - space: `O(1)`
    - `n`: absolute value of parameter `n`

    > parameters
    - `n: int`: value to compute factorial
    - `return`: factorial of `n`
    """
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def factorial_stirling(n: float) -> float:
    """
    Stirling's factorial approximation.

    > complexity
    - time: `O(1)`
    - space: `O(1)`

    > parameters
    - `n`: value to compute factorial, floats are supported
    - `return`: factorial approximation of `n`
    """
    return (2 * math.pi * n)**(0.5) * (n / math.e)**n


def factorial_ramanujan(n: float):
    """
    Ramanujan's factorial approximation, more precise than Stirling's.

    > complexity
    - time: `O(1)`
    - space: `O(1)`

    > parameters
    - `n`: value to compute factorial, floats are supported
    - `return`: factorial approximation of `n`
    """
    return math.pi**0.5 * (1 / 30 + n * (1 + n * (4 + n * 8)))**(1 / 6) * (n / math.e)**n


def test():
    from ..test import benchmark

    benchmark(
        (
            ('factorial recursive', factorial_rec),
            ('factorial iterative', factorial_itr),
            (' factorial stirling', factorial_stirling),
            ('factorial ramanujan', factorial_ramanujan),
            ('   factorial native', math.factorial),
        ),
        test_inputs=(0, 1, *range(2, 11, 2)),
        bench_sizes=(*range(0, 101, 10),),
        bench_input=lambda s: s,
        bench_repeat=100000,
    )


if __name__ == '__main__':
    test()
