import functools
from typing import Any, Callable, Literal, cast

from .abc import StringOffline, compare_slices, match_slices


class SuffixArray(StringOffline):
    """
    Suffix array implementation.

     > complexity
    - space: `O(n)`
    - `n`: length of `text` argument in `__init__`
    """

    def __init__(
        self, text: str, strategy: Literal["naive", "kmr", "kmr-opt"], lcp_strategy: Literal["naive", "kasai"]
    ):
        """
        Initialize the suffix tree given the received `text` and `strategy`.
        The space used is proportional to the length of `text` independently of `strategy`.

        > complexity
        - time suffix: `O(n*log(n))` if `strategy == 'kmr-opt'` else `O(n*log(n)**2)` if `strategy == 'kmr'` else `O(n**2)`
        - time lcp: `O(n*log(n))` if `lcp_strategy == 'kasai'` else `O(n**2)`
        - space: `O(n)`
        - `n`: length of `text`

        > parameters
        - `texts`: list of texts to be indexed
        - `strategy`: build strategy
        - `lcp_strategy`: longest common prefix build strategy
        """
        self._text = text + chr(0x10FFFF)
        build_function = {
            "kmr": lambda: self._build_karp_miller_rosenberg(False),
            "kmr-opt": lambda: self._build_karp_miller_rosenberg(True),
            "naive": self._build_naive
            # 1973 Weiner
            # 1976 mccreight
            # 1990 Manber and Myers
            # 1995 Ukkonen
            # 1997 Farach
            # 2002 Ko and Aluru
            # 2003 Kärkkäinen
            # 2008 Nong et al  SA-IS
        }[strategy]
        lcp_function = self._build_lcp_kasai if lcp_strategy == "kasai" else self._build_lcp_naive
        self._suffixes = build_function()
        self._longest_common_prefixes = lcp_function()

    def __str__(self) -> str:
        nodes: list[str] = []
        suffix_size = min(len(str(len(self._suffixes) - 1)), 3)
        lcp_size = min(len(str(len(self._longest_common_prefixes) - 1)), 3)
        suffix_formatter = f"%{suffix_size}d"
        lcp_formatter = f"%{lcp_size}d"
        for i, suffix_index in enumerate(self._suffixes):
            lcp = self._longest_common_prefixes[i] if i < len(self._longest_common_prefixes) else -1
            nodes.append(f"├ {lcp_formatter % lcp} {suffix_formatter % suffix_index} {self._text[suffix_index:]}")
        all_nodes = "\n".join(nodes)
        return f"{type(self).__name__} [\n{all_nodes}\n]"

    def _build_naive(self) -> list[int]:
        """
        Build the suffix array using the naive strategy.
        All suffixes are sorted using python's sorting algorithm (timsort ~> `O(n*log(n))`).
        Each suffix comparison might take up to `n` steps to complete, totalizing O(n*n*log(n) ~> `O(n**2*log(n))`).

        > complexity
        - time: `O(n**2*log(n))`
        - space: `O(n)`
        - `n`: length of `self._text`
        """
        suffixes: list[int] = [*range(len(self._text))]
        comparator: Callable[[int, int], int] = lambda i, j: compare_slices(
            self._text, i, len(self._text), self._text, j, len(self._text)
        )
        suffixes.sort(key=functools.cmp_to_key(comparator))
        return suffixes

    def _build_karp_miller_rosenberg(self, optimized: bool) -> list[int]:
        """
        Build the suffix array using the Karp-Miller-Rosenberg algorithm (prefix doubling).

        > complexity
        - time: `O(n*log(n))` if `optimized` else `O(n*log(n)**2)`
        - space: `O(n)`
        - `n`: length of `self._text`
        """

        def radixsort(data: list[tuple[tuple[int, int], int]]):
            data.sort()  # TODO implement radixsort that supports multiple integers as input

        sorter = radixsort if optimized else list[tuple[tuple[int, int], int]].sort
        order = [ord(char) for char in self._text]
        size = 1
        rank = 0
        # size == 1 so it has to go at least once through the loop to normalize the order (terminator character)
        while size == 1 or rank < len(self._text) - 1 and size < len(self._text):
            pairs = [((o, (order[i + size] if i + size < len(self._text) else -1)), i) for i, o in enumerate(order)]
            sorter(pairs)
            rank = 0
            for i, (pair, index) in enumerate(pairs):
                order[index] = rank
                rank += 1 if i + 1 < len(pairs) and pair < pairs[i + 1][0] else 0
            size *= 2
        suffixes = [0] * len(self._text)
        for i, o in enumerate(order):
            suffixes[o] = i
        return suffixes

    def _build_lcp_naive(self):
        """
        Build the longest common prefix.
        The longest common prefixes array can be naively computed in `O(n**2)`.
        Since each suffix comparison take up to `O(n)`, the resulting complexity.

        > complexity
        - time: `O(n**2)`
        - space: `O(n)`
        - `n`: length of `self._text`
        """
        return [
            match_slices(
                self._text, self._suffixes[i], len(self._text), self._text, self._suffixes[i + 1], len(self._text)
            )
            for i in range(len(self._text) - 1)
        ]

    def _build_lcp_kasai(self):
        """
        Build the longest common prefix using kasai's algorithm.

        > complexity
        - time: `O(n*log(n))`
        - space: `O(n)`
        - `n`: length of `self._text`
        """
        longest_common_prefixes = [0] * (len(self._suffixes) - 1)
        suffixes_inverse = [0] * len(self._suffixes)
        for i, suffix in enumerate(self._suffixes):
            suffixes_inverse[suffix] = i
        match = 0
        for i in range(len(self._suffixes)):
            if suffixes_inverse[i] == len(self._text) - 1:
                match = 0
                continue
            j = self._suffixes[suffixes_inverse[i] + 1]
            match += match_slices(self._text, i + match, len(self._text), self._text, j + match, len(self._text))
            longest_common_prefixes[suffixes_inverse[i]] = match
            match -= 1 if match > 0 else 0
        return longest_common_prefixes

    def occurrences(self, pattern: str) -> list[int]:
        """
        Check base class.

        > complexity
        - time: `O(p+q)`
        - space: `O(q)`
        - `p`: length of `pattern`
        - `q`: number of occurrences
        """
        # TODO
        return []

    def occurrences_count(self, pattern: str) -> int:
        """
        Check base class.

        > complexity
        - time: `O(p)`
        - space: `O(1)`
        - `p`: length of `pattern`
        """
        # TODO
        return 0

    def longest_repeated_substring(self, repetitions: int = 2) -> list[int]:
        """
        Check base class.

        > complexity
        - time: `O(n+q)`
        - space: `O(q)`
        - `n`: number of nodes in the suffix tree, which is proportional to the length of `self._text`
        - `q`: number of occurrences
        """
        # TODO
        return []

    def longest_common_prefix(self, i: int, j: int) -> int:
        """
        Check base class.

        > complexity
        - time: `O(1)`
        - space: `O(1)`
        """
        # TODO
        return 0


def test():
    import random
    import string

    from ...test import benchmark, verify

    for strategies in (("naive", "naive"), ("kmr", "kasai")):
        print("strategies:", strategies)
        suffix_array = SuffixArray("senselessness", cast(Any, strategies[0]), cast(Any, strategies[1]))
        print(suffix_array)
        verify(
            (
                (suffix_array.occurrences, ("s",)),
                (suffix_array.occurrences, ("e",)),
                (suffix_array.occurrences, ("ss",)),
                (suffix_array.occurrences_count, ("s",)),
                (suffix_array.occurrences_count, ("ss",)),
                (suffix_array.longest_repeated_substring, (2,)),
                (suffix_array.longest_repeated_substring, (4,)),
                (suffix_array.longest_common_prefix, (0, 0)),
                (suffix_array.longest_common_prefix, (0, 3)),
                (suffix_array.longest_common_prefix, (6, 10)),
            )
        )
        print()

    benchmark(
        (
            ("                suffix tree naive | naive", lambda text: SuffixArray(text, "naive", "naive")),
            ("                suffix tree naive | kasai", lambda text: SuffixArray(text, "naive", "kasai")),
            ("suffix tree karp miller rosenberg | naive", lambda text: SuffixArray(text, "kmr", "naive")),
            ("suffix tree karp miller rosenberg | kasai", lambda text: SuffixArray(text, "kmr", "kasai")),
        ),
        test_inputs=("hello world!", "cagtcatgcatacgtctatatcggctgc"),
        bench_sizes=(0, 1, 10, 100, 1000, 10000, 100000),
        bench_input=lambda s: "".join(random.choices(string.printable, k=s)),
        bench_repeat=10,
    )


if __name__ == "__main__":
    test()
