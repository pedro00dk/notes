from .abc import Linked, Node


class LinkedList(Linked):
    def __init__(self):
        super().__init__()

    def _check_index(self, index, insert=False):
        if index < 0 or insert and index > self.size or not insert and index >= self.size:
            raise IndexError('out of range')

    def _find_index(self, index):
        self._check_index(index)
        forward = index < self.size / 2
        node = self.head if forward else self.tail
        for i in range(index if forward else (self.size - 1 - index)):
            node = node.next if forward else node.prev
        return node

    def _find_value(self, value):
        node = self.head
        for i in range(self.size):
            if value == node.value:
                break
            node = node.next
        if node is None:
            raise ValueError('not found')
        return node, i

    def _insert(self, index, value):
        self._check_index(index, True)
        if self.head is None:
            self.head = self.tail = ListNode(value)
        elif index == 0:
            self.head = ListNode(value, None, self.head)
            self.head.next.prev = self.head
        elif index == self.size:
            self.tail = ListNode(value, self.tail, None)
            self.tail.prev.next = self.tail
        else:
            current = self._find_index(index)
            node = ListNode(value, current.prev, current)
            node.prev.next = node.next.prev = node
        self.size += 1

    def _delete(self, node):
        if node.prev is None and node.next is None:
            self.head = self.tail = None
        elif node.prev is None:
            self.head = node.next
            self.head.prev = None
        elif node.next is None:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        self.size -= 1
        return node.value

    def push(self, value, index=None):
        return self._insert(index if index is not None else self.size, value)

    def pop(self, index=None):
        return self._delete(self._find_index(index if index is not None else self.size - 1))

    def remove(self, value):
        return self._delete(self._find_value(value)[0])

    def get(self, index=None):
        return self._find_index(index if index is not None else self.size - 1).value

    def index(self, value):
        try:
            return self._find_value(value)[1]
        except ValueError:
            return -1

    def contains(self, value):
        return self.index(value) != -1

    def reverse(self):
        node = self.head
        self.head, self.tail = self.tail, self.head
        for i in range(self.size):
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
        (print, [l], None)
    ])


if __name__ == '__main__':
    test()
