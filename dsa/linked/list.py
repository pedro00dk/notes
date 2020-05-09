from .abc import Linked, Node


class LinkedList(Linked):
    def __init__(self):
        super().__init__()

    def _insert(self, index, value):
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
            current = self._find(index)[0]
            node = ListNode(value, current.prev, current)
            node.prev.next = node.next.prev = node
        self._size += 1

    def _delete(self, node):
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

    def _find(self, index):
        self._check(index)
        forward = index < self._size / 2
        node = self._head if forward else self._tail
        for i in range(index if forward else (self._size - 1 - index)):
            node = node.next if forward else node.prev
        return node, index

    def _find_value(self, value):
        for i, node in enumerate(self._nodes()):
            if value == node.value:
                return node, i
        raise ValueError('not found')

    def push(self, value, index=None):
        return self._insert(index if index is not None else self._size, value)

    def pop(self, index=None):
        return self._delete(self._find(index if index is not None else self._size - 1)[0])

    def remove(self, value):
        return self._delete(self._find_value(value)[0])

    def get(self, index=None):
        return self._find(index if index is not None else self.size - 1)[0].value

    def index(self, value):
        try:
            return self._find_value(value)[1]
        except ValueError:
            return -1

    def contains(self, value):
        return self.index(value) != -1

    def reverse(self):
        self._head, self._tail, node = self._tail, self._head, self._head
        for i in range(self._size):
            node.prev, node.next = node.next, node.prev
            node = node.prev


class ListNode(Node):
    def __init__(self, value, prev=None, next=None):
        super().__init__(value, next)
        self.prev = prev


def test():
    from ..util import match
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
