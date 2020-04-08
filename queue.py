class Queue:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def __str__(self):
        values = []
        node = self.head
        for i in range(self.size):
            values.append(str(node.value))
            node = node.next
        return f'Queue [ {", ".join(values)} ]'

    def offer(self, value):
        if self.size == 0:
            self.head = self.tail = Node(value)
        else:
            self.tail.next = Node(value)
            self.tail = self.tail.next
        self.size += 1

    def pool(self):
        if self.size == 0:
            raise IndexError('empty queue')
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return value

    def peek(self):
        if self.size == 0:
            raise IndexError('empty queue')
        return self.head.value


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def test():
    q = Queue()
    q.offer(0)
    q.offer(1)
    q.offer(2)
    q.offer(3)
    q.offer(4)
    q.offer(5)
    print(q)
    q.pool()
    q.pool()
    print(q.peek())
    print(q)
    q.pool()
    q.pool()
    print(q.peek())
    print(q)
    q.pool()
    q.pool()
    print(q)


if __name__ == '__main__':
    test()
