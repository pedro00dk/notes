import math
from typing import Generic

from .abc import RangeMinimumQuery, T


class RangeMinimumQueryV2(Generic[T], RangeMinimumQuery[T]):

    """
    Better implementation of range minimum query.

    This implementation creates a table of `ceil(log(n)) - 1 by n` size.
    Each `i [0:ceil(log(n))]` level stores ranges of size `2**i`.
    In each level, there are `j [0:n/2**i)` ranges representing the interval `[j:j + i]`.

    > complexity
    - space: `O(n*log(n))`
    - `n`: length of the `data` argument in `__init__`
    """

    def __init__(self, data: list[T]):
        """
        See base class.

        > complexity
        - time: `O(n*log(n))`
        - space: `O(n*log(n))`
        - `n`: length of `data`
        """
        if len(data) == 0:
            raise Exception('data must contain at least one element')
        self._data = data
        max_power = math.ceil(math.log2(len(data)))
        self._table = [[*range(len(data))], *([-1] * len(data) for _ in range(1, max_power))]
        for power in range(1, max_power):
            previous = self._table[power - 1]
            current = self._table[power]
            previous_range_size = 2**(power - 1)
            for i in range(len(data)):
                j = min(i + previous_range_size, len(data) - 1)
                current[i] = previous[i] if data[previous[i]] <= data[previous[j]] else previous[j]

    def rmq(self, i: int, j: int) -> int:
        """
        See base class.

        > complexity
        - time: `O(1)`
        - space: `O(1)`
        """
        i, j = (i, j) if i < j else (j, i)
        if not (0 <= i <= j < len(self._data)):
            raise IndexError(f'indices i ({i}) and j ({j}) out of range [0:{len(self._data)})')
        size = (j - i) + 1
        if size == 1:
            return self._table[0][i]
        power = math.ceil(math.log2(size))
        query_power = power - 1
        partial_range_a = self._table[query_power][i]
        partial_range_b = self._table[query_power][j - int(2**query_power) + 1]
        return partial_range_a if self._data[partial_range_a] <= self._data[partial_range_b] else partial_range_b

    def size(self) -> int:
        return len(self._data)

    @classmethod
    def is_plus_minus_1(cls) -> bool:
        return False


def test():
    from ...test import match

    data = [8, 7, 2, 8, 6, 9, 4, 5, 2]
    rmq = RangeMinimumQueryV2(data)
    match((
        (rmq.rmq, (0, 0), 0),
        (rmq.rmq, (0, 2), 2),
        (rmq.rmq, (2, 5), 2),
        (rmq.rmq, (4, 5), 4),
        (rmq.rmq, (5, 7), 6),
        (rmq.rmq, (8, 8), 8),
        (rmq.rmq, (2, 8), 2),
    ))


if __name__ == '__main__':
    test()
