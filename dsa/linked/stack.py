from .abc import Linked


class Stack(Linked):
    def __init__(self):
        super().__init__()
        self.head = None

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def push(self, value):
        if self.head is None:
            self.head = self.tail = Node(value)
        else:
            self.head = Node(value, self.head)
        self.size += 1

    def pop(self):
        if self.head is None:
            raise IndexError('empty stack')
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value

    def peek(self):
        if self.head is None:
            raise IndexError('empty stack')
        return self.head.value


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def test():
    from ..util import match
    s = Stack()
    match([
        (s.push, [0], None),
        (s.push, [1], None),
        (s.push, [2], None),
        (s.push, [3], None),
        (s.push, [4], None),
        (s.push, [5], None),
        (print, [s], None),
        (s.pop, [], 5),
        (s.pop, [], 4),
        (s.peek, [], 3),
        (print, [s], None),
        (s.pop, [], 3),
        (s.pop, [], 2),
        (s.peek, [], 1),
        (print, [s], None),
        (s.pop, [], 1),
        (s.pop, [], 0),
        (print, [s], None)
    ])


if __name__ == '__main__':
    test()
