from .abc import Linear, Node


class ListNode(Node):
    """
    Node with the extra `tail` property for doubly linked lists.
    """

    def __init__(self, value, prev=None, next=None):
        super().__init__(value, next)
        self.prev = prev


class LinkedList(Linear):
    """
    Doubly Linked List implementation.
    """

    def __init__(self):
        super().__init__()

    def _node_index(self, index: int):
        """
        Get the node at `index`, or raise exception if index is invalid.

        > optimizations:
        -  only go through half the list by checking the index beforehand.

        > complexity:
        > time: `O(n)`
        > space: `O(1)`

        > parameters:
        - `index: int`: node index
        - `#return#: ListNode`: node at `index`
        """
        self._check(index)
        forward = index < self._size / 2
        node = self._head if forward else self._tail
        for i in range(index if forward else (self._size - 1 - index)):
            node = node.next if forward else node.prev
        return node, index

    def _node_value(self, value):
        """
        Get the first node that contains`value`, or raise exception if not found.

        > complexity:
        > time: `O(n)`
        > space: `O(1)`

        > parameters:
        - `value: any`: node value
        - `#return#: ListNode`: node containing `value`
        """
        for i, node in enumerate(self._nodes()):
            if value == node.value:
                return node, i
        raise ValueError(f'value ({str(value)}) not found')

    def _insert(self, index: int, value):
        """
        Create and insert a new node with `value` in the specified `index`.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > parameters:
        - `index: int`: insertion index
        - `value: any`: value to insert
        """
        self._check(index, True)
        if self._head is None:
            self._head = self._tail = ListNode(value)
        elif index == 0:
            self._head = ListNode(value, None, self._head)
            self._head.next.prev = self._head
        elif index == self._size:
            self._tail = ListNode(value, self._tail, None)
            self._tail.prev.next = self._tail
        else:
            current = self._node_index(index)[0]
            node = ListNode(value, current.prev, current)
            node.prev.next = node.next.prev = node
        self._size += 1

    def _delete(self, node: type(ListNode)):
        """
        Delete the received `node` from the data structure.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `node: ListNode`: node to delete
        """
        if node.prev is None and node.next is None:
            self._head = self._tail = None
        elif node.prev is None:
            self._head = node.next
            self._head.prev = None
        elif node.next is None:
            self._tail = node.prev
            self._tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        self._size -= 1
        return node.value

    def push(self, value, /, index: int = None):
        """
        Insert `value` at the end of the list.
        If `index` is provided, then insert at `index`.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > parameters:
        - `value: any`: value to insert
        - `index: int` (optional -> `len(self)`): insertion index
        """
        return self._insert(index if index is not None else self._size, value)

    def pop(self, /, index: int = None):
        """
        Delete the value at the end of the list.
        If `index` is provided, then delete at `index`.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > parameters:
        - `index: int` (optional -> `len(self) - 1`): deletion index
        - `#return#: any`: value from the deleted node
        """
        return self._delete(self._node_index(index if index is not None else self._size - 1)[0])

    def remove(self, value):
        """
        Remove the first node that contains `value`.

        > complexity:
        - time: `O(n)`
        - space: `O(1)`

        > parameters:
        - `index: int` (optional -> `len(self) - 1`): deletion index
        - `#return#: any`: value from the deleted node
        """
        return self._delete(self._node_value(value)[0])

    def get(self, /, index: int = None):
        """
        Get the value at the end of the list.
        If `index` is provided, then get at `index`.

        > complexity:
        > time: `O(n)`
        > space: `O(1)`

        > parameters:
        - `index: int`: value index
        - `#return#: any`: value at `index`
        """
        return self._node_index(index if index is not None else self.size - 1)[0].value

    def reverse(self):
        """
        Reverse the list nodes.

        > complexity:
        > time: `O(n)`
        > space: `O(1)`
        """
        self._head, self._tail, node = self._tail, self._head, self._head
        for i in range(self._size):
            node.prev, node.next = node.next, node.prev
            node = node.prev


def test():
    from ..test import match
    l = LinkedList()
    match([
        (l.push, [2, 0], None),
        (l.push, [1, 0], None),
        (l.push, [0, 0], None),
        (l.push, [5], None),
        (l.push, [6], None),
        (l.push, [7], None),
        (l.push, [3, 3], None),
        (l.push, [4, 4], None),
        (print, [l], None),
        (l.get, [6], 6),
        (l.get, [2], 2),
        (l.pop, [4], 4),
        (l.pop, [3], 3),
        (print, [l], None),
        (l.pop, [], 7),
        (l.pop, [0], 0),
        (print, [l], None),
        (l.reverse, [], None),
        (l.index, [5], 1),
        (l.index, [2], 2),
        (print, [l], None)
    ])


if __name__ == '__main__':
    test()
