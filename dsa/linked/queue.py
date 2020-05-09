from .abc import Linked, Node


class Queue(Linked):
    def __init__(self):
        super().__init__()

    def offer(self, value):
        if self._tail is None:
            self._head = self._tail = Node(value)
        else:
            self._tail.next = Node(value)
            self._tail = self._tail.next
        self._size += 1

    def poll(self):
        if self._head is None:
            raise IndexError('empty queue')
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return value

    def peek(self):
        if self._head is None:
            raise IndexError('empty queue')
        return self._head.value


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
