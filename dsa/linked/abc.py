from abc import ABC, abstractmethod


class Linked(ABC):
    def __init__(self):
        self._head = self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def __str__(self):
        return f'{type(self).__name__} [{", ".join(str(value) for value in self)}]'

    def __iter__(self):
        return self.values()

    def _check(self, index, insert=False):
        if index < 0 or insert and index > self._size or not insert and index >= self._size:
            raise IndexError('out of range')

    def _nodes(self):
        node = self._head
        while node is not None:
            yield node
            node = node.next

    def empty(self):
        return self._size == 0

    def values(self):
        return (node.value for node in self._nodes())


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next
