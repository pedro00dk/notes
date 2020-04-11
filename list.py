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
    l = LinkedList()
    l.prepend(2)
    l.prepend(1)
    l.prepend(0)
    l.append(5)
    l.append(6)
    l.append(7)
    l.insert(3, 3)
    l.insert(4, 4)
    print(l)
    print(l.get(6))
    print(l.get(2))
    print(l.delete(5))
    print(l.delete(3))
    print(l.pop())
    print(l.prepop())
    print(l)
    l.reverse()
    print(l)


if __name__ == '__main__':
    test()
