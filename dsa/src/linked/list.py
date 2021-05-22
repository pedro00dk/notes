from __future__ import annotations

import dataclasses
from typing import Generator, Generic, Optional, cast

from .abc import Linked, T


@dataclasses.dataclass
class Node(Generic[T]):
    value: T
    prev: Optional[Node[T]] = None
    next: Optional[Node[T]] = None


class LinkedList(Generic[T], Linked[T]):
    """
    Doubly Linked List implementation.

    > complexity
    - space: `O(n)`
    - `n`: number of elements in the structure
    """

    def __init__(self):
        super().__init__()
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None
        self._length = 0

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Generator[T, None, None]:
        """
        Check base class.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list
        """
        cursor = self._head
        while cursor is not None:
            yield cursor.value
            cursor = cursor.next

    def _node_index(self, index: int) -> Node[T]:
        """
        Get the node at `index`, or raise exception if index is invalid.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list

        > parameters
        - `index`: node index
        - `return`: node at `index`
        """
        if index < 0 or index >= self._length:
            raise IndexError(f"index ({index}) out of range [0, {self._length})")
        forward = index < self._length / 2
        cursor = cast(Node[T], self._head if forward else self._tail)
        for _ in range(index if forward else (self._length - 1 - index)):
            cursor = cast(Node[T], cursor.next if forward else cursor.prev)
        return cursor

    def _node_value(self, value: T) -> Node[T]:
        """
        Get the first node that contains`value`, or raise exception if `value` is not found.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list

        > parameters
        - `value`: node value
        - `return`: node containing `value`
        """
        cursor = self._head
        while cursor is not None and cursor.value is not value and cursor.value != value:
            cursor = cursor.next
        if cursor is None:
            raise ValueError(f"value ({value}) not found")
        return cursor

    def _insert(self, index: int, value: T):
        """
        Create and insert a new node with `value` in the specified `index`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list

        > parameters
        - `index`: insertion index
        - `value`: value to insert
        """
        if index < 0 or index > self._length:
            raise IndexError(f"index ({index}) out of range [0, {self._length}]")
        if self._head is None:
            self._head = self._tail = Node(value)
        elif index == 0:
            self._head = Node(value, None, self._head)
            cast(Node[T], self._head.next).prev = self._head
        elif index == self._length:
            self._tail = Node(value, self._tail, None)
            cast(Node[T], self._tail.prev).next = self._tail
        else:
            current = self._node_index(index)
            node = Node(value, current.prev, current)
            cast(Node[T], node.prev).next = cast(Node[T], node.next).prev = node
        self._length += 1

    def _delete(self, node: Node[T]) -> T:
        """
        Delete the received `node` from the data structure.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `node`: node to delete
        """
        if node.prev is not None and node.next is not None:
            node.prev.next = node.next
            node.next.prev = node.prev
        elif node.next is not None:
            self._head = node.next
            self._head.prev = None
        elif node.prev is not None:
            self._tail = node.prev
            self._tail.next = None
        else:
            self._head = self._tail = None
        self._length -= 1
        return node.value

    def push(self, value: T, index: Optional[int] = None):
        """
        Insert `value` at the end of the list.
        If `index` is provided, then insert at `index`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list

        > parameters
        - `value`: value to insert
        - `index`: insertion index
        """
        self._insert(index if index is not None else self._length, value)

    def pop(self, index: Optional[int] = None) -> T:
        """
        Delete the value at the end of the list.
        If `index` is provided, then delete at `index`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list

        > parameters
        - `index`: deletion index
        - `return`: value from the deleted node
        """
        return self._delete(self._node_index(index if index is not None else self._length - 1))

    def remove(self, value: T) -> T:
        """
        Remove the first node that contains `value`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list

        > parameters
        - `index`: deletion index
        - `return`: value from the deleted node
        """
        return self._delete(self._node_value(value))

    def get(self, index: Optional[int] = None) -> T:
        """
        Get the value at the end of the list.
        If `index` is provided, then get at `index`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`
        - `n`: length of the list

        > parameters
        - `index`: value index
        - `return`: value at `index`
        """
        return self._node_index(index if index is not None else self._length - 1).value

    def reverse(self):
        """
        Reverse the list nodes.

        > complexity
        > time: `O(n)`
        > space: `O(1)`
        """
        node = cast(Node[T], self._head)
        self._head, self._tail = self._tail, self._head
        for _ in range(self._length):
            node.prev, node.next = node.next, node.prev
            node = cast(Node[T], node.prev)


def test():
    import collections

    from ..test import benchmark, verify

    linked_list = LinkedList[int]()
    verify(
        (
            (linked_list.push, (2, 0)),
            (linked_list.push, (1, 0)),
            (linked_list.push, (0, 0)),
            (linked_list.push, (5,)),
            (linked_list.push, (6,)),
            (linked_list.push, (7,)),
            (
                linked_list.push,
                (
                    3,
                    3,
                ),
            ),
            (
                linked_list.push,
                (
                    4,
                    4,
                ),
            ),
            (print, (linked_list,)),
            (linked_list.get, (6,), 6),
            (linked_list.get, (2,), 2),
            (linked_list.pop, (4,), 4),
            (linked_list.pop, (3,), 3),
            (print, (linked_list,)),
            (linked_list.pop, (), 7),
            (linked_list.pop, (0,), 0),
            (print, (linked_list,)),
            (linked_list.reverse, ()),
            (linked_list.index, (5,), 1),
            (linked_list.index, (2,), 2),
            (print, (linked_list,)),
        )
    )

    def test_linked_list(count: int):
        linked_list = LinkedList[int]()
        for i in range(count):
            linked_list.push(i)
        for i in range(count // 2):
            linked_list.pop()
            linked_list.pop(0)

    def test_native_list(count: int):
        lst = list[int]()
        for i in range(count):
            lst.append(i)
        for i in range(count // 2):
            lst.pop()
            lst.pop(0)

    def test_native_deque(count: int):
        deque = collections.deque[int]()
        for i in range(count):
            deque.append(i)
        for i in range(count // 2):
            deque.pop()
            deque.popleft()

    benchmark(
        (
            (" linked list", test_linked_list),
            (" native list", test_native_list),
            ("native deque", test_native_deque),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s: s,
    )


if __name__ == "__main__":
    test()
