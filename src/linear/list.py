from __future__ import annotations

from typing import Generic, Optional, cast

from .abc import Linear, Node, T


class ListNode(Generic[T], Node[T]):
    """
    Node with the extra `tail` property for doubly linked lists.
    """

    def __init__(self, value: T, prev: Optional[ListNode[T]] = None, next: Optional[ListNode[T]] = None):
        super().__init__(value)
        self.prev: Optional[ListNode[T]] = prev
        self.next: Optional[ListNode[T]] = next


class LinkedList(Generic[T], Linear[T]):
    """
    Doubly Linked List implementation.
    """

    def __init__(self):
        super().__init__()
        self._head: Optional[ListNode[T]] = None
        self._tail: Optional[ListNode[T]] = None

    def _node_index(self, index: int) -> tuple[ListNode[T], int]:
        """
        Get the node at `index`, or raise exception if index is invalid.

        > optimizations
        -  only go through half the list by checking the index beforehand.

        > complexity
        > time: `O(n)`
        > space: `O(1)`

        > parameters
        - `index`: node index
        - `return`: node at `index`
        """
        self._check(index)
        forward = index < self._size / 2
        node = cast(ListNode[T], self._head if forward else self._tail)
        for _ in range(index if forward else (self._size - 1 - index)):
            node = cast(ListNode[T], node.next if forward else node.prev)
        return node, index

    def _node_value(self, value: T):
        """
        Get the first node that contains`value`, or raise exception if not found.

        > complexity
        > time: `O(n)`
        > space: `O(1)`

        > parameters
        - `value`: node value
        - `return`: node containing `value`
        """
        for i, node in enumerate(self._nodes()):
            if value == node.value:
                return cast(ListNode[T], node), i
        raise ValueError(f'value ({value}) not found')

    def _insert(self, index: int, value: T):
        """
        Create and insert a new node with `value` in the specified `index`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        > parameters
        - `index`: insertion index
        - `value`: value to insert
        """
        self._check(index, True)
        if self._head is None:
            self._head = self._tail = ListNode(value)
        elif index == 0:
            self._head = ListNode(value, None, self._head)
            cast(ListNode[T], self._head.next).prev = self._head
        elif index == self._size:
            self._tail = ListNode(value, self._tail, None)
            cast(ListNode[T], self._tail.prev).next = self._tail
        else:
            current = self._node_index(index)[0]
            node = ListNode(value, current.prev, current)
            cast(ListNode[T], node.prev).next = cast(ListNode[T], node.next).prev = node
        self._size += 1

    def _delete(self, node: ListNode[T]) -> T:
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
        self._size -= 1
        return node.value

    def push(self, value: T, index: Optional[int] = None):
        """
        Insert `value` at the end of the list.
        If `index` is provided, then insert at `index`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        > parameters
        - `value`: value to insert
        - `index`: insertion index
        """
        self._insert(index if index is not None else self._size, value)

    def pop(self, index: Optional[int] = None) -> T:
        """
        Delete the value at the end of the list.
        If `index` is provided, then delete at `index`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        > parameters
        - `index`: deletion index
        - `return`: value from the deleted node
        """
        return self._delete(self._node_index(index if index is not None else self._size - 1)[0])

    def remove(self, value: T) -> T:
        """
        Remove the first node that contains `value`.

        > complexity
        - time: `O(n)`
        - space: `O(1)`

        > parameters
        - `index`: deletion index
        - `return`: value from the deleted node
        """
        return self._delete(self._node_value(value)[0])

    def get(self, index: Optional[int] = None) -> T:
        """
        Get the value at the end of the list.
        If `index` is provided, then get at `index`.

        > complexity
        > time: `O(n)`
        > space: `O(1)`

        > parameters
        - `index`: value index
        - `return`: value at `index`
        """
        return self._node_index(index if index is not None else self._size - 1)[0].value

    def reverse(self):
        """
        Reverse the list nodes.

        > complexity
        > time: `O(n)`
        > space: `O(1)`
        """
        node = cast(ListNode[T], self._head)
        self._head, self._tail = self._tail, self._head
        for _ in range(self._size):
            node.prev, node.next = node.next, node.prev
            node = cast(ListNode[T], node.prev)


def test():
    import collections

    from ..test import benchmark, match

    linked_list = LinkedList[int]()
    match((
        (linked_list.push, (2, 0)),
        (linked_list.push, (1, 0)),
        (linked_list.push, (0, 0)),
        (linked_list.push, (5,)),
        (linked_list.push, (6,)),
        (linked_list.push, (7,)),
        (linked_list.push, (3, 3,)),
        (linked_list.push, (4, 4,)),
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
    ))

    def test_linkedlist(count: int):
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
            ('  linkedlist', test_linkedlist),
            (' native list', test_native_list),
            ('native deque', test_native_deque),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s: s,
    )


if __name__ == '__main__':
    test()
