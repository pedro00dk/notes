from .abc import Linear, Node


class Queue(Linear):
    def __init__(self):
        super().__init__()

    def offer(self, value):
        """
        Insert `value` at the end of the queue.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `value: any`: value to insert
        """
        if self._tail is None:
            self._head = self._tail = Node(value)
        else:
            self._tail.next = Node(value)
            self._tail = self._tail.next
        self._size += 1

    def poll(self):
        """
        Delete the value at the begginging of the queue.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > `return: any`: deleted value
        """
        if self._head is None:
            raise IndexError('empty queue')
        value = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return value

    def peek(self):
        """
        Get the value at the beggening of the queue without removing it.

        > complexity:
        > time: `O(1)`
        > space: `O(1)`

        > `return: any`: value at the begginging of the queue
        """
        if self._head is None:
            raise IndexError('empty queue')
        return self._head.value


def test():
    from ..test import benchmark, match
    from collections import deque
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

    def test_queue(count: int):
        q = Queue()
        for i in range(count):
            q.offer(i)
        for i in range(count):
            q.poll()

    def test_native_list(count: int):
        l = list()
        for i in range(count):
            l.append(i)
        for i in range(count):
            l.pop(0)

    def test_native_deque(count: int):
        d = deque()
        for i in range(count):
            d.append(i)
        for i in range(count):
            d.popleft()

    benchmark(
        [
            ('       queue', test_queue),
            (' native list', test_native_list),
            ('native deque', test_native_deque)
        ],
        test_input_iter=(),
        bench_size_iter=(1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s, r: s,
        test_print_input=False,
        test_print_output=False
    )


if __name__ == '__main__':
    test()
