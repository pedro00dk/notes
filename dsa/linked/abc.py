from abc import ABC, abstractmethod


class Linked(ABC):
    def __init__(self):
        self.size = 0

    @abstractmethod
    def __iter__(self):
        pass

    def __str__(self):
        return f'{type(self).__name__} [ {", ".join(str(value) for value in self)} ]'

    def __len__(self):
        return self.size
