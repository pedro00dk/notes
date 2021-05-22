import collections


def sellers(text: bytes, pattern: bytes, max_distance: int) -> list[tuple[int, int]]:
    """
    Sellers algorithm for approximate string search.
    This algorithm is based on Wagner-Fisher algorithm for computing edit distances.
    The difference is that each new index `i` in `text` starts at 0 distance rather than `ì`, implying that for any `i`,
    the suffix of `text` starting from `i` is considered as matching target, and not only the full `text` string.
    This algorithm also accepts the `max_distance` argument, which filters mathings with distance smaller or equal to
    `max_distance`.
    Since approximate searching algorithms only consider substrings ot `text`, `max_distance` is clamped to `pattern`
    length because as characters from `text` are ignored, no match with edit distance greater than `pattern` length can
    happen.
    Sellers performance does not depend on the `max_distance` argument.

    > complexity
    - time: `O(n*p)`
    - space: `O(p)`
    - `n`: length of `text`
    - `p`: length of `pattern`

    > parameters
    - `text`: text to find pattern matches
    - `pattern`: pattern
    - `max_distance`: maximum value of the edit distance to report an occurrence
    - `return`: a list of tuples containing the final index of the match (not the first index like exact algorithms) and
        the edit distance of that match
    """

    if len(pattern) == 0:
        raise Exception("empty pattern")
    occurrences: list[tuple[int, int]] = []
    max_distance = min(max_distance, len(pattern))
    distances = [[*range(len(pattern) + 1)], [0] * (len(pattern) + 1)]
    for i in range(1, len(text) + 1):
        distances[1][0] = 0
        for j in range(1, len(pattern) + 1):
            cost = text[i - 1] != pattern[j - 1]
            distances[1][j] = min(distances[0][j] + 1, distances[1][j - 1] + 1, distances[0][j - 1] + cost)
        if distances[1][len(pattern)] <= max_distance:
            occurrences.append((i - 1, distances[1][len(pattern)]))
        distances.reverse()
    return occurrences


def ukkonen(text: bytes, pattern: bytes, max_distance: int) -> list[tuple[int, int]]:
    """
    Ukkonen algorithm for approximate string search.
    This algorithm builds a finite state automaton similar to aho corasick's, each vertex in the automaton maps to a
    column of distances given a previous column of distances and a character.
    Although the asymptotic complexities are linear on `text` length, the performance rapidly degrades for larger
    patterns due to hidden multiplicative constants like alphabet size.

    > complexity
    - time: `O(n + (p*c*min(p, d)))`
    - space: `O(p)`
    - `n`: length of `text`
    - `p`: length of `pattern`
    - `d`: absolute value of `max_distance`
    - `c`: alphabet size, fixed 256

    > parameters
    - `text`: text to find pattern matches
    - `pattern`: pattern
    - `max_distance`: maximum value of the edit distance to report an occurrence
    - `return`: a list of tuples containing the final index of the match (not the first index like exact algorithms) and
        the edit distance of that match
    """

    def compute_next_column(column: tuple[int, ...], byte: int, pattern: bytes, max_distance: int) -> tuple[int, ...]:
        """
        Compute the column of distances given a previous column, a byte possibly from the text, and the pattern.
        The maximum edit distance is also used to limit the distance values in the column, this reduces the number of
        possible columns to be mapped in the build_fsa algorithm.

        > complexity
        - time: `O(p)`
        - space: `O(p)`
        - `p`: length of `pattern`

        > parameters
        - `column`: the previous column of distances
        - `byte`: the character byte used to compute the next column of distances
        - `pattern`: pattern
        - `max_distance`: limits the edit distances in the column of distances
        - `return`: the next column of distances
        """
        next_column = [0] * (len(pattern) + 1)
        for i in range(1, len(pattern) + 1):
            cost = pattern[i - 1] != byte
            next_column[i] = min(column[i] + 1, next_column[i - 1] + 1, column[i - 1] + cost, max_distance + 1)
        return (*next_column,)

    def build_fsa(pattern: bytes, max_distance: int) -> tuple[dict[tuple[int, int], int], dict[int, int]]:
        """
        Build the finite state automaton used in the approximate search.
        The automaton is composed of a trie containing only forward links, and the goals.
        The trie is a dictionary where each key is a tuple of a vertex index and a character (byte), and the value is
        the next vertex index.
        This function also returns the goal vertices, which is a dictionary with goal vertices as indices and the edit
        distance at that vertex as value.

        > complexity
        - time: `O(p*c*min(p, d))`
        - space: `O(p)`
        - `p`: length of `pattern`
        - `d`: absolute value of `max_distance`
        - `c`: alphabet size, fixed 256

        > parameters
        - `pattern`: pattern
        - `max_distance`: limits the edit distances in the column of distances to reduce number of states
        - `return`: tuple containing the trie and goal vertices with edit distances
        """
        trie: dict[tuple[int, int], int] = {}
        goals: dict[int, int] = {}
        vertex = 0
        column = (*range(0, len(pattern) + 1),)
        queue = collections.deque[tuple[tuple[int, ...], int]]()
        queue.append((column, vertex))
        column_states: dict[tuple[int, ...], int] = {}
        column_states[column] = vertex
        if column[-1] <= max_distance:
            goals[vertex] = column[-1]
        while len(queue) > 0:
            column, source_vertex = queue.popleft()
            for byte in range(256):
                next_column = compute_next_column(column, byte, pattern, max_distance)
                target_vertex = column_states.get(next_column, -1)
                if target_vertex == -1:
                    vertex += 1
                    target_vertex = vertex
                    column_states[next_column] = target_vertex
                    queue.append((next_column, target_vertex))
                    if next_column[-1] <= max_distance:
                        goals[vertex] = next_column[-1]
                trie[(source_vertex, byte)] = target_vertex
        return trie, goals

    if len(pattern) == 0:
        raise Exception("empty pattern")
    occurrences: list[tuple[int, int]] = []
    max_distance = min(max_distance, len(pattern))
    trie, goals = build_fsa(pattern, max_distance)
    cursor = 0
    for i, byte in enumerate(text):
        cursor = trie[(cursor, byte)]
        if cursor in goals:
            occurrences.append((i, goals[cursor]))
    return occurrences


def wu_manber(text: bytes, pattern: bytes, max_distance: int) -> list[tuple[int, int]]:
    """
    Wu-Manber algorithm for approximate string search.
    This algorithm is an extension of the Baeza-Yates–Gonnet exact string searching algorithm (also known as shift-or,
    shift-and, or bitap) to support approximate matching.
    The matching edit distance is not easily obtainable as in other algorithms, each `current_mask` except for the last
    care the information that the distance is closer to 0 by 1 (if the match against `match_mask`), by adding all
    matchings masks and subtracting from max distance, we have the final match distance.
    Wu-Manber performance mainly depends on the `max_distance` argument, `pattern` length has minimal impact.

    > complexity
    - time: `O(n*min(p, d) + p)`
    - space: `O(c + min(p, d))`
    - `n`: length of `text`
    - `p`: length of `pattern`
    - `d`: absolute value of `max_distance`
    - `c`: alphabet size, fixed 256

    > parameters
    - `text`: text to find pattern matches
    - `pattern`: pattern
    - `max_distance`: maximum value of the edit distance to report an occurrence
    - `return`: a list of tuples containing the final index of the match (not the first index like exact algorithms) and
        the edit distance of that match
    """

    def compute_char_masks(pattern: bytes) -> tuple[list[int], int]:
        """
        Compute character masks for the pattern, to be used in the shifting operations, and the match mask.
        The semantics of the 0 and 1 bits are reversed from their meanings in the exact matching verstion, but the match
        mask is not reversed.
        Matches can be checked by applying the AND operator between the last `current_mask` and `match_mask`, if the
        result is equals 0, there is a match.
        This behavior is the opposite of the exact version.

        > complexity
        - time: `O(p)`
        - space: `O(c)`
        - `p`: length of `pattern`
        - `c`: alphabet size, fixed 256
        """
        char_masks = [~0] * 256
        match_mask = 1 << len(pattern) - 1
        for i, byte in enumerate(pattern):
            char_masks[byte] = char_masks[byte] & (~0 ^ (1 << i))
        return char_masks, match_mask

    if len(pattern) == 0:
        raise Exception("empty pattern")
    occurrences: list[tuple[int, int]] = []
    max_distance = min(max_distance, len(pattern))
    char_masks, match_mask = compute_char_masks(pattern)
    current_masks = [~0 << i for i in range(max_distance + 1)]
    for i, byte in enumerate(text):
        previous_mask = current_masks[0]
        current_masks[0] = (current_masks[0] << 1) | char_masks[byte]
        for j in range(1, max_distance + 1):
            temp = current_masks[j]
            current_masks[j] = (
                ((current_masks[j] << 1) | char_masks[byte])
                & (current_masks[j - 1] << 1)
                & (previous_mask << 1)
                & previous_mask
            )
            previous_mask = temp
        if current_masks[max_distance] & match_mask == 0:
            distance = max_distance + 1 - sum(mask & match_mask == 0 for mask in current_masks)
            occurrences.append((i, distance))
    return occurrences


def test():
    import random

    from ..test import benchmark

    def random_bytes(size: int, alphabet_size: int) -> bytes:
        return bytes(random.randint(0, alphabet_size - 1) for _ in range(size))

    benchmark(
        (
            ("  sellers", lambda args: sellers(args[0], args[1], args[2])),
            ("  ukkonen", lambda args: ukkonen(args[0], args[1], args[2])),
            ("wu manber", lambda args: wu_manber(args[0], args[1], args[2])),
        ),
        test_inputs=((b"if you would like", b"love", 2), (b"cagtcatgcatacgtctatatcggctgc", b"ctata", 1)),
        bench_sizes=((1000, 5, 2), (1000, 5, 5), (1000, 10, 2), (1000, 10, 5), (1000, 10, 10)),
        bench_input=lambda s: (random_bytes(s[0], 256), random_bytes(s[1], 256), s[2]),
        bench_repeat=10,
    )


if __name__ == "__main__":
    test()
