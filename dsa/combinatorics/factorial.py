import math


def factorial_rec(n: int):
    """
    Factorial algorithm, recursive implementation.
    ```
    n! = {
        n * (n - 1)! if n > 0,
        1 if n == 0
    }
    ```

    > optimizations:
    - skip the `n == 1` and `n == 0` recursive steps because `1! == 1` and `0! == 1`

    > complexity:
    - time: `O(n)`
    - space: `O(log(n))`

    > parameters:
    - `n: int`: value to compute factorial
    - `#return#: int`: factorial of `n`
    """
    return n * factorial_rec(n - 1) if n > 1 else 1


def factorial_itr(f: int):
    """
    Factorial algorithm, interactive implementation.
    ```
    n! = ∏ i=[1:n] i
    ```

    > optimizations:
    - start loop from 2 because `0! == 1` and `1! == 1`

    > complexity:
    - time: `O(f)`
    - space: `O(1)`

    > parameters:
    - `f: int`: value to compute factorial
    - `#return#: int`: factorial of `f`
    """
    r = 1
    for i in range(2, f + 1):
        r *= i
    return r


def factorial_stirling(n: float):
    """
    Stirling's factorial approximation.

    > complexity:
    - time: `O(1)` (float exponentiation is constant, `pow` and `**` use float exponentiation only if operands are float)
    - space: `O(1)`

    > parameters:
    - `f: int`: value to compute factorial
    - `#return#: int`: factorial approximation of `f`
    """
    return (2 * math.pi * n) ** (0.5) * (n / math.e) ** n


def factorial_ramanujan(n: float):
    """
    Ramanujan's factorial approximation. Much more precise than Stirling's.

    > complexity:
    - time: `O(1)` (float exponentiation is constant, `pow` and `**` use float exponentiation only if operands are float)
    - space: `O(1)`

    > parameters:
    - `f: int`: value to compute factorial
    - `#return#: int`: factorial approximation of `f`
    """
    return math.pi ** 0.5 * (1 / 30 + n * (1 + n * (4 + n * 8))) ** (1 / 6) * (n / math.e) ** n


def test():
    from timeit import timeit
    for i in (0, 1, 5, 10, 20, 30, 40, 50):
        print('n =', i)
        print(' recursive', factorial_rec(i))
        print('iteractive', factorial_itr(i))
        print('  stirling', factorial_stirling(i))
        print(' ramanujan', factorial_ramanujan(i))
        print()
    print('benchmark')
    print(' recursive', timeit('for i in range(50): factorial_rec(i)', globals=globals(), number=10000))
    print('iteractive', timeit('for i in range(50): factorial_itr(i)', globals=globals(), number=10000))
    print('  stirling', timeit('for i in range(50): factorial_stirling(i)', globals=globals(), number=10000))
    print(' ramanujan', timeit('for i in range(50): factorial_ramanujan(i)', globals=globals(), number=10000))


if __name__ == '__main__':
    test()
