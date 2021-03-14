from __future__ import annotations

import abc

"""
Different from other string search modules (string_exact.py, string_distance.py, string_fuzzy.py), this module works
with `str` objects, rather than `bytes` objects.
"""


class StringOffline(abc.ABC):
    """
    Abstract base class for offline string data structures.
    """

    @abc.abstractmethod
    def __str__(self) -> str: ...

    @abc.abstractmethod
    def occurrences(self, pattern: str) -> list[int]:
        """
        Compute the occurrences of `pattern` and return indices of occurrences.

        > complexity
        - see implementations

        > parameters
        - `pattern`: pattern
        - `return`: list of occurrences
        """

    @abc.abstractmethod
    def occurrences_count(self, pattern: str) -> int:
        """
        Compute the number of occurrences of `pattern`.

        > complexity
        - see implementations

        > parameters
        - `pattern`: pattern
        - `return`: number of occurrences
        """

    @abc.abstractmethod
    def longest_repeated_substring(self, repetitions: int = 2) -> list[int]:
        """
        Return the longest repeated substring occurrences given a minimum number of `repetitions`.
        If the empty string is the longest repeated substring, due to empty texts or large `repetitions` values, an
        empty list is returned.

        > complexity
        - see implementations

        > parameters
        - `repetitions`: minimum number of repetitions of the string
        - `return`: occurrences of the longest string
        """

    @abc.abstractmethod
    def longest_common_prefix(self, i: int, j: int) -> int:
        """
        Given two starting indices `i` and `j` from text, find the longest common prefix of them.

        > parameters
        - `i`: index in text
        - `j`: index in text
        - `return`: length of the matching prefix
        """


def match_slices(text_a: str, left_a: int, right_a: int, text_b: str, left_b: int, right_b: int) -> int:
    """
    Match the following slices `text_a[left_a: right_a] == text_b[left_b: right_b]`.
    The matching is done manually, without using string slices which would create copies of the slices.
    Right indices are exclusive.

    > complexity
    - time: `O(min(a, b))`
    - space: `O(1)`
    - `a`: absolute value of `right_a - left_a`
    - `b`: absolute value of `right_b - left_b`

    > parameters
    - see function description
    - `return`: length of the matching prefix
    """
    length = min(right_a - left_a, right_b - left_b)
    i = 0
    while i < length and text_a[i + left_a] == text_b[i + left_b]:
        i += 1
    return i


def compare_slices(text_a: str, left_a: int, right_a: int, text_b: str, left_b: int, right_b: int) -> int:
    """
    Lexicographically compare the slices `text_a[left_a: right_a]` and `text_b[left_b: right_b]`.
    The comparison is done manually, without using string slices which would create copies of the slices.
    Right indices are exclusive.

    > complexity
    - time: `O(min(a, b))`
    - space: `O(1)`
    - `a`: absolute value of `right_a - left_a`
    - `b`: absolute value of `right_b - left_b`

    > parameters
    - see function description
    - `return`: -1 if the first slice is smaller than the second, 1 if the second slice is smaller than the first or 0
        if the slices are equal
    """
    length_a = right_a - left_a
    length_b = right_b - left_b
    length = min(length_a, length_b)
    i = 0
    while i < length and text_a[i + left_a] == text_b[i + left_b]:
        i += 1
    if i == length:
        return -1 if length_a < length_b else 1 if length_a > length_b else 0
    return -1 if text_a[i + left_a] < text_b[i + left_b] else 1
