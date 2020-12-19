from typing import Generic, Optional

from .abc import Linear, Node, T


class Queue(Generic[T], Linear[T]):
    def __init__(self):
        super().__init__()
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None

    def offer(self, value: T):
        """
        Insert `value` at the end of the queue.

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        > parameters
        - `value`: value to insert
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

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        - `return`: deleted value
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

        > complexity
        - time: `O(1)`
        - space: `O(1)`

        - `return`: value at the begginging of the queue
        """
        if self._head is None:
            raise IndexError('empty queue')
        return self._head.value


def test():
    import collections

    from ..test import benchmark, match

    queue = Queue[int]()
    match((
        (queue.offer, (0,)),
        (queue.offer, (1,)),
        (queue.offer, (2,)),
        (queue.offer, (3,)),
        (queue.offer, (4,)),
        (queue.offer, (5,)),
        (print, (queue,)),
        (queue.poll, (), 0),
        (queue.poll, (), 1),
        (queue.peek, (), 2),
        (print, (queue,)),
        (queue.poll, (), 2),
        (queue.poll, (), 3),
        (queue.peek, (), 4),
        (print, (queue,)),
        (queue.poll, (), 4),
        (queue.poll, (), 5),
        (print, (queue,)),
    ))

    def test_queue(count: int):
        queue = Queue[int]()
        for i in range(count):
            queue.offer(i)
        for i in range(count):
            queue.poll()

    def test_native_list(count: int):
        lst = list[int]()
        for i in range(count):
            lst.append(i)
        for i in range(count):
            lst.pop(0)

    def test_native_deque(count: int):
        deque = collections.deque[int]()
        for i in range(count):
            deque.append(i)
        for i in range(count):
            deque.popleft()

    benchmark(
        (
            ('       queue', test_queue),
            (' native list', test_native_list),
            ('native deque', test_native_deque),
        ),
        test_inputs=(),
        bench_sizes=(0, 1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s: s,
    )


if __name__ == '__main__':
    test()
