import math

from .abc import RangeMinimumQuery, lca_to_rmq, rmq_to_lca
from .naive import RangeMinimumQueryNaive
from .v3 import RangeMinimumQueryV3


class RangeMinimumQueryV4(RangeMinimumQuery[int]):
    """
    Extension of the V3 implementation of range minimum query.

    This implementation uses V3 implementation as base to query fully covered intervals in the promoted arrays.
    This means that even though, V3 query is `O(log(n))` fully covered intervals always are executed in `O(1)`.

    To support constant time query in the left and right partially covered groups, this implementations requires
    plus-minus-1 data arrays.
    Since each group has only `log(n) / 2` elements and each element only differs by 1, by considering only the
    differences between each element of the group, there is only `2**(log(n) / 2) ~> sqrt(n)` different groups.
    In this case any quadratic solution or better can be applied for these groups, and since many groups may have the
    same sequence of differences, the same solution can be applied for them, further reducing memory usage.

    Still, this implementation has large asymptotic time and space constants when building and querying.
    """

    def __init__(self, data: list[int]):
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
        self._promoted_rmq = RangeMinimumQueryV3(data)
        self._range_size = max(math.ceil(math.log2(len(data)) / 2), 1)
        self._group_codes: list[int] = []
        self._code_maps: dict[int, RangeMinimumQuery[int]] = {}
        for group in range(math.ceil(len(data) / self._range_size)):
            start = group * self._range_size
            end = min((group + 1) * self._range_size - 1, len(data) - 1)
            group_code = 0
            for s, i in enumerate(range(start + 1, end + 1)):
                group_code |= 1 << s if data[i] > data[i - 1] else 0
            self._group_codes.append(group_code)
            if group_code in self._code_maps:
                continue
            self._code_maps[group_code] = RangeMinimumQueryNaive(data[start: end + 1])  # V2 could also be used

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
        if group_i < group_i_prime:  # left group (naive lookup)
            group_code = self._group_codes[group_i]
            group_rmq = self._code_maps[group_code]
            local_i = i % self._range_size
            local_j = j % self._range_size if group_i == group_j else group_rmq.size() - 1
            local_k = group_rmq.rmq(local_i, local_j)
            k = local_k + group_i * self._range_size
            minimum = minimum if self._data[minimum] <= self._data[k] else k
        if group_i_prime <= group_j_prime:  # groups covered by promoted arrays
            k = self._promoted_rmq.rmq(i_prime, j_prime)
            minimum = minimum if self._data[minimum] <= self._data[k] else k
        if group_j > group_j_prime:  # right group (naive lookup)
            group_code = self._group_codes[group_j]
            group_rmq = self._code_maps[group_code]
            local_i = i % self._range_size if group_i == group_j else 0
            local_j = j % self._range_size
            local_k = group_rmq.rmq(local_i, local_j)
            k = local_k + group_j * self._range_size
            minimum = minimum if self._data[minimum] <= self._data[k] else k

        return minimum

    def size(self) -> int:
        return len(self._data)

    @classmethod
    def is_plus_minus_1(cls) -> bool:
        return True


def test():
    from ...test import match

    data = [8, 7, 2, 8, 6, 9, 4, 5, 2]
    _, _, root, _, get_children = rmq_to_lca(data)
    data_plus_minus_1, backward_mapper, forward_mapper = lca_to_rmq(
        root, lambda node: node.index, get_children, lambda node: node.index, True, True
    )
    rmq = RangeMinimumQueryV4(data_plus_minus_1)

    def rmq_map_plus_minus_1(i: int, j: int):
        return backward_mapper[rmq.rmq(forward_mapper[i][0], forward_mapper[j][0])]

    match((
        (rmq_map_plus_minus_1, (0, 0), 0),
        (rmq_map_plus_minus_1, (0, 2), 2),
        (rmq_map_plus_minus_1, (2, 5), 2),
        (rmq_map_plus_minus_1, (4, 5), 4),
        (rmq_map_plus_minus_1, (5, 7), 6),
        (rmq_map_plus_minus_1, (8, 8), 8),
        (rmq_map_plus_minus_1, (2, 8), 2),
    ))


if __name__ == '__main__':
    test()
