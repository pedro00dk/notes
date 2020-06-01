from .abc import Linear, Node


class Stack(Linear):
    def __init__(self):
        super().__init__()

    def push(self, value):
        """
        Insert `value` at the top of the stack.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `value: any`: value to insert
        """
        if self._head is None:
            self._head = Node(value)
        else:
            self._head = Node(value, self._head)
        self._size += 1

    def pop(self):
        """
        Delete the value at the top of the stack.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `#return#: any`: deleted value
        """
        if self._head is None:
            raise IndexError('empty stack')
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        return value

    def peek(self):
        """
        Get the value at the top of the stack without removeing it.

        > complexity:
        > time: `O(1)`
        > space: `O(1)`

        > parameters:
        - `#return#: any`: value at the top of the stack
        """
        if self._head is None:
            raise IndexError('empty stack')
        return self._head.value


def test():
    from ..test import match
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
