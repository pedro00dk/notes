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

        > `return: any`: deleted value
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

        > `return: any`: value at the top of the stack
        """
        if self._head is None:
            raise IndexError('empty stack')
        return self._head.value


def test():
    import collections
    from ..test import benchmark, match
    s = Stack()
    match([
        (s.push, (0,)),
        (s.push, (1,)),
        (s.push, (2,)),
        (s.push, (3,)),
        (s.push, (4,)),
        (s.push, (5,)),
        (print, (s,)),
        (s.pop, (), 5),
        (s.pop, (), 4),
        (s.peek, (), 3),
        (print, (s,)),
        (s.pop, (), 3),
        (s.pop, (), 2),
        (s.peek, (), 1),
        (print, (s,)),
        (s.pop, (), 1),
        (s.pop, (), 0),
        (print, (s,))
    ])

    def test_stack(count: int):
        s = Stack()
        for i in range(count):
            s.push(i)
        for i in range(count):
            s.pop()

    def test_native_list(count: int):
        l = list()
        for i in range(count):
            l.append(i)
        for i in range(count):
            l.pop()

    def test_native_deque(count: int):
        d = collections.deque()
        for i in range(count):
            d.append(i)
        for i in range(count):
            d.pop()

    benchmark(
        [
            ('       stack', test_stack),
            (' native list', test_native_list),
            ('native deque', test_native_deque)
        ],
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s: s
    )


if __name__ == '__main__':
    test()
