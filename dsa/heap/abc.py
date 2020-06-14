import abc


class Heap(abc.ABC):
    """
    Abstract base class for heaps.
    This class provides basic fields used in common heap data structures, which are `heap` and `comparator`
    """

    @abc.abstractmethod
    def __init__(self, /, data: list = None, comparator='max'):
        """
        > complexity: check tree implementations

        > parameters:
        - `data: <T>[]`: initial data to populate the heap
        - `comparator: ('min' | 'max' | (<T>, <T>) => int)? = max`: a comparator string for numeric values
            (`min`, `max`) or a min comparator to check values (smaller values go to the top)
        """
        self._heap = data if data is not None else []
        self._comparator = (lambda a, b: a - b) if comparator == 'min' else \
            (lambda a, b: b - a) if comparator == 'max' else comparator

    def __len__(self):
        return len(self._heap)

    def __str__(self):
        return f'{type(self).__name__} {self._heap}'

    def empty(self):
        """
        Return if the structure is empty.

        > `return: bool`: if empty
        """
        return len(self._heap) == 0

    @abc.abstractmethod
    def offer(self, value):
        """
        Insert `value` in the heap.

        > complexity: check subclass implementations

        > parameters:
        - `value: <T>`: value to insert
        """
        pass

    @abc.abstractmethod
    def poll(self):
        """
        Delete the value at the top of the heap.

        > complexity: check subclass implementations

        > `return: <T>`: deleted value
        """
        pass

    def peek(self):
        """
        Get the value at the top of the heap without removing it.

        > complexity: check subclass implementations

        > `return: <T>`: value at the top of the heap
        """
        if len(self._heap) == 0:
            raise IndexError('empty heap')
        return self._heap[0]
