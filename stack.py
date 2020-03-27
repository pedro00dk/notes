class Stack:
    def __init__(self):
        self.head = None
        self.size = 0

    def __str__(self):
        values = []
        node = self.head
        for i in range(self.size):
            values.append(str(node.value))
            node = node.next
        return f'Stack [ {", ".join(values)} ]'

    def push(self, value):
        if not self.size: self.head = self.tail = Node(value)
        else: self.head = Node(value, self.head)
        self.size += 1

    def pop(self):
        if not self.size: raise IndexError('empty stack')
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        return value

    def peek(self):
        if not self.size: raise IndexError('empty stack')
        return self.head.value


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def test():
    s = Stack()
    s.push(0)
    s.push(1)
    s.push(2)
    s.push(3)
    s.push(4)
    s.push(5)
    print(s)
    s.pop()
    s.pop()
    print(s.peek())
    print(s)
    s.pop()
    s.pop()
    print(s.peek())
    print(s)
    s.pop()
    s.pop()
    print(s)


if __name__ == '__main__': test()
