from typing import Generic

from .abc import RangeMinimumQuery, T


class RangeMinimumQueryNaive(Generic[T], RangeMinimumQuery[T]):
    """
    Naive implementation of range minimum queries.
    This implementation creates a table of `n+1 by n` size.
    Each `i [0:n]` level stores ranges of size `i`, the array at `i == 0` is empty because there is no rmq of zero sized
    ranges. For each level, there are `j [0:n - i)` ranges representing the interval `[j:j + i]`.

    > complexity
    - space: `O(n**2)`
    - `n`: length of the `data` argument in `__init__`
    """

    def __init__(self, data: list[T]):
        """
        Check base class.

        > complexity
        - time: `O(n**2)`
        - space: `O(n**2)`
        - `n`: length of `data`
        """
        if len(data) == 0:
            raise Exception('data must contain at least one element')
        self._data = data
        self._table = [
            [],
            [*range(len(data))],
            *([-1] * (len(data) - (range_size - 1)) for range_size in range(2, len(data) + 1)),
        ]
        for range_size in range(2, len(data) + 1):
            previous = self._table[range_size - 1]
            current = self._table[range_size]
            for i in range(len(data) - (range_size - 1)):
                j = i + 1
                current[i] = previous[i] if data[previous[i]] <= data[previous[j]] else previous[j]

    def rmq(self, i: int, j: int) -> int:
        """
        Check base class.

        > complexity
        - time: `O(1)`
        - space: `O(1)`
        """
        i, j = (i, j) if i < j else (j, i)
        if not (0 <= i <= j < len(self._data)):
            raise IndexError(f'indices i ({i}) and j ({j}) out of range [0:{len(self._data)})')
        size = (j - i) + 1
        index = self._table[size][i]
        return index

    def size(self) -> int:
        return len(self._data)

    @classmethod
    def is_plus_minus_1(cls) -> bool:
        return False


def test():
    from ...test import match

    data = [8, 7, 2, 8, 6, 9, 4, 5, 2]
    rmq = RangeMinimumQueryNaive(data)
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
