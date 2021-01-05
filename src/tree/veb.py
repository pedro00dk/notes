import math
from typing import Any, Callable, Generator, Generic, Optional, TypeVar, cast

from .abc import Tree

V = TypeVar('V')


class VEBNode(Generic[V]):
    def __init__(self, word_size: int):
        self.word_size = word_size
        self.min = -1
        self.max = -1
        self.min_value: V = cast(Any, None)
        self.max_value: V = cast(Any, None)
        self.summary: VEBNode[V] = cast(Any, None)
        self.clusters: dict[int, VEBNode[V]] = {}


class VEB(Generic[V], Tree[int, V]):
    """
    van Emde Boas tree implementation.
    This implementation uses hashtables to reduce space usage from `O(u)` to `O(n)`.
    Only power of two word sizes are supported.
    This implementation stores both minimum and maximum values of a node not recursively, so predecessor and successor
    can be implemented symmetrically and the space usage is reduced.
    """

    def __init__(self, word_size: int = 64):
        log_word_size = math.log2(word_size)
        if log_word_size != round(log_word_size):
            raise Exception(f'word_size must be a power of 2 ({word_size})')
        self._word_size = word_size
        self._universe = 2**word_size
        self._root = VEBNode[V](self._word_size)
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Generator[tuple[int, V], None, None]:
        """
        Check base class.

        > complexity
        - time: `O(n*log(w)) ~> O(n*log(log(u))`
        - space: `O(n*log(w)) ~> O(n*log(log(u))`
        - `w`: tree `word_size`
        - `u`: tree `universe`, which is `word_size**2`
        """
        cursor = self.minimum()
        while cursor is not None:
            yield cursor
            cursor = self.successor(cursor[0])

    def put(self, key: int, value: V, replacer: Optional[Callable[[V, V], V]] = None) -> Optional[V]:
        """
        Check base class.

        > complexity
        - time: `O(log(w)) ~> O(log(log(u))`
        - space: `O(log(w)) ~> O(log(log(u))`
        - `w`: tree `word_size`
        - `u`: tree `universe`, which is `word_size**2`
        """
        def rec(key: int, value: V, node: VEBNode[V], summary: bool) -> Optional[V]:
            if node.min == node.max:
                if node.min == -1:
                    node.min = node.max = key
                    node.min_value = node.max_value = value
                elif key < node.min:
                    node.min = key
                    node.min_value = value
                elif key > node.max:
                    node.max = key
                    node.max_value = value
                else:
                    node.min = node.max = key
                    old_value = node.min_value
                    node.min_value = node.max_value = value if replacer is None else replacer(value, node.min_value)
                    return old_value
                self._size += not summary
                return None
            if key < node.min:
                node.min, key = key, node.min
                node.min_value, value = value, node.min_value
            elif key > node.max:
                node.max, key = key, node.max
                node.max_value, value = value, node.max_value
            elif key == node.min:
                node.min = key
                old_value = node.min_value
                node.min_value = value if replacer is None else replacer(value, node.min_value)
                return old_value
            elif key == node.max:
                node.max = key
                old_value = node.max_value
                node.max_value = value if replacer is None else replacer(value, node.max_value)
                return old_value
            high = key >> (node.word_size >> 1)
            low = key & ((1 << (node.word_size >> 1)) - 1)
            if high not in node.clusters:
                node.clusters[high] = VEBNode(node.word_size >> 1)
                node.summary = VEBNode(node.word_size >> 1) if node.summary is None else node.summary
                rec(high, cast(Any, None), node.summary, summary or True)
            return rec(low, value, node.clusters[high], summary or False)

        if not (0 <= key < self._universe):
            raise Exception(f'key ({key}) out of universe [0, {self._universe})')
        return rec(key, value, self._root, False)

    def take(self, key: int) -> V:
        """
        Check base class.

        > complexity
        - time: `O(log(w)) ~> O(log(log(u))`
        - space: `O(log(w)) ~> O(log(log(u))`
        - `w`: tree `word_size`
        - `u`: tree `universe`, which is `word_size**2`
        """
        def rec(complete_key: int, key: int, node: VEBNode[V], summary: bool) -> V:
            if key == node.min:
                if node.min == node.max:
                    node.min = node.max = -1
                    self._size -= not summary
                    return node.min_value
                elif node.summary is None:
                    node.min = node.max
                    old_value = node.min_value
                    node.min_value = node.max_value
                    self._size -= not summary
                    return old_value
                else:
                    key = node.min = node.summary.min << (node.word_size >> 1) | node.clusters[node.summary.min].min
            elif key == node.max:
                if node.max == node.min:
                    node.max = node.min = -1
                    self._size -= not summary
                    return node.max_value
                elif node.summary is None:
                    node.max = node.min
                    old_value = node.max_value
                    node.max_value = node.min_value
                    self._size -= not summary
                    return old_value
                else:
                    key = node.max = node.summary.max << (node.word_size >> 1) | node.clusters[node.summary.max].max
            high = key >> (node.word_size >> 1)
            low = key & ((1 << (node.word_size >> 1)) - 1)
            if high not in node.clusters:
                raise KeyError(f'key ({complete_key}) not found')
            value = rec(complete_key, low, node.clusters[high], summary or False)
            if node.clusters[high].min == -1:
                del node.clusters[high]
                rec(complete_key, high, node.summary, summary or True)  # delete summary if -1
                node.summary = cast(Any, None) if node.summary.min == -1 else node.summary
            return value

        if not (0 <= key < self._universe):
            raise Exception(f'key ({key}) out of universe [0, {self._universe})')
        return rec(key, key, self._root, False)

    def get(self, key: int) -> V:
        """
        Check base class.

        > complexity
        - time: `O(log(w)) ~> O(log(log(u))`
        - space: `O(log(w)) ~> O(log(log(u))`
        - `w`: tree `word_size`
        - `u`: tree `universe`, which is `word_size**2`
        """
        def rec(complete_key: int, key: int, node: VEBNode[V]) -> V:
            if key == node.min:
                return node.min_value
            if key == node.max:
                return node.max_value
            high = key >> (node.word_size >> 1)
            low = key & ((1 << (node.word_size >> 1)) - 1)
            if high not in node.clusters:
                raise KeyError(f'key ({complete_key}) not found')
            return rec(complete_key, low, node.clusters[high])

        return rec(key, key, self._root)

    def minimum(self) -> Optional[tuple[int, V]]:
        """
        Check base class.

        > complexity
        - time: `O(1)`
        - space: `O(1)`
        """
        return (self._root.min, self._root.min_value) if self._root.min != -1 else None

    def maximum(self) -> Optional[tuple[int, V]]:
        """
        Check base class.

        > complexity
        - time: `O(1)`
        - space: `O(1)`
        """
        return (self._root.max, self._root.max_value) if self._root.max != -1 else None

    def predecessor(self, key: int) -> Optional[tuple[int, V]]:
        """
        Check base class.

        > complexity
        - time: `O(log(w)) ~> O(log(log(u))`
        - space: `O(log(w)) ~> O(log(log(u))`
        - `w`: tree `word_size`
        - `u`: tree `universe`, which is `word_size**2`
        """
        def rec(key: int, node: VEBNode[V]) -> tuple[int, V]:
            if key > node.max:
                return node.max, node.max_value
            if key > node.min and (
                node.summary is None or
                key <= (node.summary.min << (node.word_size >> 1)) | node.clusters[node.summary.min].min
            ):
                return node.min, node.min_value
            high = key >> (node.word_size >> 1)
            low = key & ((1 << (node.word_size >> 1)) - 1)
            if high in node.clusters and low > node.clusters[high].min:
                low, value = rec(low, node.clusters[high])
            else:
                high, _ = rec(high, node.summary)
                low, value = node.clusters[high].max, node.clusters[high].max_value
            successor = (high << (node.word_size >> 1)) | low
            return successor, value

        return rec(key, self._root) if self._root.min != -1 and key > self._root.min else None

    def successor(self, key: int) -> Optional[tuple[int, V]]:
        """
        Check base class.

        > complexity
        - time: `O(log(w)) ~> O(log(log(u))`
        - space: `O(log(w)) ~> O(log(log(u))`
        - `w`: tree `word_size`
        - `u`: tree `universe`, which is `word_size**2`
        """
        def rec(key: int, node: VEBNode[V]) -> tuple[int, V]:
            if key < node.min:
                return node.min, node.min_value
            if key < node.max and (
                node.summary is None or
                key >= (node.summary.max << (node.word_size >> 1)) | node.clusters[node.summary.max].max
            ):
                return node.max, node.max_value
            high = key >> (node.word_size >> 1)
            low = key & ((1 << (node.word_size >> 1)) - 1)
            if high in node.clusters and low < node.clusters[high].max:
                low, value = rec(low, node.clusters[high])
            else:
                high, _ = rec(high, node.summary)
                low, value = node.clusters[high].min, node.clusters[high].min_value
            successor = (high << (node.word_size >> 1)) | low
            return successor, value

        return rec(key, self._root) if self._root.max != -1 and key < self._root.max else None
