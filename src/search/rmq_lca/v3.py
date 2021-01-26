import math
from typing import Generic

from .abc import RangeMinimumQuery, T
from .v2 import RangeMinimumQueryV2


class RangeMinimumQueryV3(Generic[T], RangeMinimumQuery[T]):
    """
    Extension of the V2 implementation of range minimum query.

    This implementation conceptually splits `data` into ranges of size `log(n) / 2` called groups.
    Each group's minimum value and its index is promoted and saved into the promoted arrays of size `2n / log(n)`.
    In this new array, the RangeMinimumQueryV2 is used, the resulting size of the data structure will still be `O(n)`
    because even though the V2 version adds a multiplicative `log(n)` factor, the array passed to it has already shaved
    this factor.
    This will increase the cost of `rmq` to `O(log(n))` because given a query range `i:j`, only the query
    interval `i':j'` in `i<=i'<j'<=j` may be covered by the promoted array (V2 implementation has `O(1)` query cost).
    The slices `i:i'` and `j':j` still have to be manually covered, resulting in the `O(log(n))` query time.

    > complexity
    - space: `O(n)`
    - `n`: length of the `data` argument in `__init__`
    """

    def __init__(self, data: list[T]):
        """
        See base class.

        > complexity
        - time: `O(n)`
        - space: `O(n)`
        - `n`: length of `data`
        """
        if len(data) == 0:
            raise Exception('data must contain at least one element')
        self._data = data
        self._range_size = max(math.ceil(math.log2(len(data)) / 2), 1)
        self._promoted_indices: list[int] = []
        self._promoted_values: list[T] = []
        for group in range(math.ceil(len(data) / self._range_size)):
            start = group * self._range_size
            end = min((group + 1) * self._range_size - 1, len(data) - 1)
            minimum = start
            for i in range(start + 1, end + 1):
                minimum = minimum if data[minimum] <= data[i] else i
            self._promoted_indices.append(minimum)
            self._promoted_values.append(data[minimum])
        self._promoted_rmq = RangeMinimumQueryV2(self._promoted_values)

    def rmq(self, i: int, j: int) -> int:
        """
        See base class.

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`
        """
        i, j = (i, j) if i < j else (j, i)
        if not (0 <= i <= j < len(self._data)):
            raise IndexError(f'indices i ({i}) and j ({j}) out of range [0:{len(self._data)})')
        group_i = i // self._range_size
        group_i_prime = group_i + (1 if i > group_i * self._range_size else 0)
        group_j = j // self._range_size
        group_j_prime = group_j - (1 if j < min((group_j + 1) * self._range_size - 1, len(self._data)) else 0)
        i_prime = group_i_prime * self._range_size
        j_prime = min((group_j_prime + 1) * self._range_size - 1, len(self._data))
        minimum = i
        for k in range(i, min(i_prime, j + 1)):  # left group (partially covered)
            minimum = minimum if self._data[minimum] <= self._data[k] else k
        if group_i_prime <= group_j_prime:  # groups covered by promoted arrays
            k = self._promoted_indices[self._promoted_rmq.rmq(group_i_prime, group_j_prime)]
            minimum = minimum if self._data[minimum] <= self._data[k] else k
        for k in range(max(j_prime + 1, i), j + 1):  # right group (partially covered)
            minimum = minimum if self._data[minimum] <= self._data[k] else k
        return minimum

    def size(self) -> int:
        return len(self._data)

    @classmethod
    def is_plus_minus_1(cls) -> bool:
        return False


def test():
    from ...test import match

    data = [8, 7, 2, 8, 6, 9, 4, 5, 2]
    rmq = RangeMinimumQueryV3(data)
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
