class LinkedList:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def __str__(self):
        values = []
        node = self.head
        for i in range(self.size):
            values.append(str(node.value))
            node = node.next
        return f'LinkedList [ {", ".join(values)} ]'

    def __len__(self):
        return size

    def _node(self, index):
        if index < 0 or index >= self.size:
            raise IndexError('out of range')
        direction = 1 if index < self.size / 2 else -1
        node = self.head if direction == 1 else self.tail
        if direction == 1:
            for i in range(index):
                node = node.next
        else:
            for i in range(self.size - 1, index - 1, -1):
                node = node.prev
        return node

    def prepend(self, value):
        if self.head is None:
            self.head = self.tail = Node(value)
        else:
            self.head = Node(value, None, self.head)
            self.head.next.prev = self.head
        self.size += 1

    def append(self, value):
        if self.tail is None:
            self.head = self.tail = Node(value)
        else:
            self.tail = Node(value, self.tail, None)
            self.tail.prev.next = self.tail
        self.size += 1

    def insert(self, index, value):
        if index == 0:
            return self.prepend(value)
        elif index == self.size:
            return self.append(value)
        node = self._node(index)
        node.prev.next = Node(value, node.prev, node)
        node.prev = node.prev.next
        self.size += 1

    def prepop(self):
        if self.head is None:
            raise IndexError('empty list')
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
        return value

    def pop(self):
        if self.tail is None:
            raise IndexError('empty list')
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
        return value

    def delete(self, index):
        if index == 0:
            return self.prepop()
        elif index == self.size - 1:
            return self.pop()
        node = self._node(index)
        node.next.prev = node.prev
        node.prev.next = node.next
        self.size -= 1
        return node.value

    def get(self, index):
        return self._node(index).value

    def reverse(self):
        if self.size == 0:
            return
        node = self.head
        self.head, self.tail = self.tail, self.head
        for i in range(self.size):
            node.prev, node.next = node.next, node.prev
            node = node.prev


class Node:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


def test():
    from ..util import match
    l = LinkedList()
    match([
        (l.prepend, [2], None),
        (l.prepend, [1], None),
        (l.prepend, [0], None),
        (l.append, [5], None),
        (l.append, [6], None),
        (l.append, [7], None),
        (l.insert, [3, 3], None),
        (l.insert, [4, 4], None),
        (print, [l], None),
        (l.get, [6], 5),
        (l.get, [2], 2),
        (l.delete, [4], 4),
        (l.delete, [3], 2),
        (print, [l], None),
        (l.pop, [], 7),
        (l.prepop, [], 0),
        (print, [l], None),
        (l.reverse, [], None),
        (print, [l], None)
    ])


if __name__ == '__main__':
    test()
