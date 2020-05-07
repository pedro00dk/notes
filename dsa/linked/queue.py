from .abc import Linked


class Queue(Linked):
    def __init__(self):
        super().__init__()
        self.head = self.tail = None

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def offer(self, value):
        if self.tail is None:
            self.head = self.tail = Node(value)
        else:
            self.tail.next = Node(value)
            self.tail = self.tail.next
        self.size += 1

    def poll(self):
        if self.head is None:
            raise IndexError('empty queue')
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return value

    def peek(self):
        if self.head is None:
            raise IndexError('empty queue')
        return self.head.value


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def test():
    from ..util import match
    q = Queue()
    match([
        (q.offer, [0], None),
        (q.offer, [1], None),
        (q.offer, [2], None),
        (q.offer, [3], None),
        (q.offer, [4], None),
        (q.offer, [5], None),
        (print, [q], None),
        (q.poll, [], 0),
        (q.poll, [], 1),
        (q.peek, [], 2),
        (print, [q], None),
        (q.poll, [], 2),
        (q.poll, [], 3),
        (q.peek, [], 4),
        (print, [q], None),
        (q.poll, [], 4),
        (q.poll, [], 5),
        (print, [q], None)
    ])


if __name__ == '__main__':
    test()
