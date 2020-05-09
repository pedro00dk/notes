from abc import ABC, abstractmethod


class Linked(ABC):
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __str__(self):
        return f'{type(self).__name__} [{", ".join(str(value) for value in self)}]'

    def __len__(self):
        return self.size

    def empty(self):
        return self.size == 0


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next
