class BIT:
    """
    Binary Index Tree implementation.
    This data structure is also known as Fenwick Tree.
    """

    def __init__(self, array: list[float]):
        """
        Initialize the BIT.
        `array` is assumed to be zero-based, so a new array has to be created to allow fast index computation based only
        on bitwise operations.
        All function index parameters however, assume to be zero-based, functions will automatically increment indices.

        > complexity
        - time: `O(n)`
        - space: `O(n)`

        > parameters
        - `array`: base array for building the tree
        """
        self._tree = [0.0] + array
        for index in range(1, len(self._tree)):
            if (parent := index + self._lsb(index)) < len(self._tree):
                self._tree[parent] += self._tree[index]

    def __len__(self) -> int:
        return len(self._tree) - 1

    def __str__(self) -> str:
        return f'BIT {self._tree}'

    def _lsb(self, value: int) -> int:
        """
        Compute the least significant bit of `value`.

        > parameters
        - `value: int`: value to compute lsb

        - `return`: lsb of `value`
        """
        return value & -value

    def sum(self, index: int) -> float:
        """
        Return the prefix sum [0, `index`] in the original array (zero-based).

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters
        - `index: int`: index to compute sum

        - `return`: the sum
        """
        index += 1  # change index base to 1 (if not incremented, the sum range is open at index)
        acc = 0
        while index > 0:
            acc += self._tree[index]
            index -= self._lsb(index)
        return acc

    def sum_range(self, from_index: int, to_index: int) -> float:
        """
        Return the prefix sum [`from_index`, `to_index`] in the original array (zero-based).

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters
        - `from_index: int`: first index to compute sum (inclusive)
        - `to_index: int`: last index to compute sum (inclusive)

        - `return`: the sum
        """
        return self.sum(to_index) - self.sum(from_index - 1)

    def add(self, index: int, value: float):
        """
        Increment the value at `index` in the original array by `value` (zero-based).

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters
        - `index: int`: index to increment value
        - `value: int | float`: increment value

        - `return`: the sum
        """
        index += 1
        while index < len(self._tree):
            self._tree[index] += value
            index += self._lsb(index)

    def set(self, index: int, value: float):
        """
        Set `value` at `index` in the original array (zero-based).

        > complexity
        - time: `O(log(n))`
        - space: `O(1)`

        > parameters
        - `index: int`: index to set value
        - `value: int | float`: value to set

        - `return`: the sum
        """
        current = self.sum_range(index, index)
        self.add(index, value - current)


def test():
    from .test import match

    bit = BIT([3, 4, -2, 7, 3, 11, 5, -8, -9, 2, 4, -8])
    match((
        (print, (bit,)),
        (bit.sum_range, (0, 1), 7),
        (bit.sum_range, (0, 2), 5),
        (bit.sum_range, (5, 7), 8),
        (bit.sum_range, (8, 10), -3),
        (bit.sum_range, (11, 11), -8),
        (print, (bit,)),
        (bit.add, (0, 10)),
        (bit.set, (5, -10)),
        (bit.add, (10, 10)),
        (print, (bit,)),
        (bit.sum_range, (0, 1), 17),
        (bit.sum_range, (0, 2), 15),
        (bit.sum_range, (5, 7), -13),
        (bit.sum_range, (8, 10), 7),
        (bit.sum_range, (11, 11), -8),
    ))


if __name__ == '__main__':
    test()
