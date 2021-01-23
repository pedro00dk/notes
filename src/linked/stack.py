from __future__ import annotations

import dataclasses
from typing import Generator, Generic, Optional

from .abc import Linked, T


@dataclasses.dataclass
class Node(Generic[T]):
    value: T
    next: Optional[Node[T]] = None


class Stack(Generic[T], Linked[T]):
    """
    Linked stack implementation.

    > complexity
    - space: `O(n)`
    - `n`: number of elements in the structure
    """

    def __init__(self):
        super().__init__()
        self._head: Optional[Node[T]] = None
        self._length = 0

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Generator[T, None, None]:
        """
        Check base class.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the stack
        """
        cursor = self._head
        while cursor is not None:
            yield cursor.value
            cursor = cursor.next

    def push(self, value: T):
        """
        Insert `value` at the top of the stack.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `value`: value to insert
        """
        self._head = Node(value, self._head)
        self._length += 1

    def pop(self):
        """
        Delete the value at the top of the stack.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        - `return`: deleted value
        """
        if self._head is None:
            raise IndexError('empty stack')
        value = self._head.value
        self._head = self._head.next
        self._length -= 1
        return value

    def peek(self):
        """
        Get the value at the top of the stack without removing it.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        - `return`: value at the top of the stack
        """
        if self._head is None:

            raise IndexError('empty stack')
        return self._head.value


def test():
    import collections

    from ..test import benchmark, match
    stack = Stack[int]()
    match((
        (stack.push, (0,)),
        (stack.push, (1,)),
        (stack.push, (2,)),
        (stack.push, (3,)),
        (stack.push, (4,)),
        (stack.push, (5,)),
        (print, (stack,)),
        (stack.pop, (), 5),
        (stack.pop, (), 4),
        (stack.peek, (), 3),
        (print, (stack,)),
        (stack.pop, (), 3),
        (stack.pop, (), 2),
        (stack.peek, (), 1),
        (print, (stack,)),
        (stack.pop, (), 1),
        (stack.pop, (), 0),
        (print, (stack,)),
    ))

    def test_stack(count: int):
        stack = Stack[int]()
        for i in range(count):
            stack.push(i)
        for i in range(count):
            stack.pop()

    def test_native_list(count: int):
        lst = list[int]()
        for i in range(count):
            lst.append(i)
        for i in range(count):
            lst.pop()

    def test_native_deque(count: int):
        deque = collections.deque[int]()
        for i in range(count):
            deque.append(i)
        for i in range(count):
            deque.pop()

    benchmark(
        (
            ('       stack', test_stack),
            (' native list', test_native_list),
            ('native deque', test_native_deque),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s: s,
    )


if __name__ == '__main__':
    test()
