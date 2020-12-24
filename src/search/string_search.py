import collections


def brute_force(text: bytes, pattern: bytes) -> list[int]:
    """
    Brute force exact string searching algorithm.
    Some string searching algorithms do not support empty `pattern`.
    For maching specifications, all algorithms raise exceptions if the `pattern` is empty.

    > complexity
    - time: `O(n * p)`
    - space: `O(1)`

    > parameters
    - `text`: text to search for occurrences of pattern
    - `pattern`: pattern
    - `return`: list containing the starting index of all occurrences
    """
    if len(pattern) == 0:
        raise Exception('empty pattern')
    occurrences: list[int] = []
    for i in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern) and text[i + j] == pattern[j]:
            j += 1
        if j == len(pattern):
            occurrences.append(i)
    return occurrences


def rabin_karp(text: bytes, pattern: bytes, alphabet: int = 256, modulus: int = 2147483647) -> list[int]:
    """
    Rabin-Karp exact string searching algorithm.

    > complexity
    - time: average: `O(n + p)`, worst: `O(n * p)`
    - space: `O(1)`

    > parameters
    - `text`: text to search for occurrences of pattern
    - `pattern`: pattern
    - `alphabet`: size of the alphabet (max 256 because comparisons are done per byte)
    - `modulus`: modulus value use to limit the size of the hashes
    - `return`: list containing the starting index of all occurrences
    """

    def compute_power(pattern: bytes, alphabet: int, modulus: int) -> int:
        """
        Compute the largest multiplicative coefficient for a hash of length equals to `len(pattern)`.
        """
        power = 1
        for _ in range(len(pattern) - 1):
            power = (power * alphabet) % modulus
        return power

    def init_hash(text: bytes, pattern: bytes, alphabet: int, modulus: int) -> int:
        """
        Compute initial hash for `text` using the length of `pattern`.
        """
        hash = 0
        for i in range(len(pattern)):
            hash = (hash * alphabet + text[i]) % modulus
        return hash

    def roll_hash(text: bytes, pattern: bytes, hash: int, power: int, i: int, alphabet: int, modulus: int) -> int:
        """
        Roll the current `hash` of `text[i: i + len(pattern)]` to `text[i + 1: i + len(pattern) + 1]`.
        This is done by removing `text[index]` from the hash (which was multiplied by `power`), then multiply the hash
        by `alphabet` to update the coefficients of the remaining values, then add `text[index+length]` to the hash.
        """
        return ((hash - text[i] * power) * alphabet + text[i + len(pattern)]) % modulus

    def equals(text: bytes, pattern: bytes, i: int) -> bool:
        """
        Return `True` if `text[index:index+length] == pattern[:length]`.
        """
        j = 0
        while j < len(pattern) and text[i + j] == pattern[j]:
            j += 1
        return j == len(pattern)

    if len(pattern) == 0:
        raise Exception('empty pattern')
    if len(text) < len(pattern):
        return []
    alphabet = min(max(2, alphabet), 256)
    modulus = max(modulus, 257)
    occurrences: list[int] = []
    power = compute_power(pattern, alphabet, modulus)
    text_hash = init_hash(text, pattern, alphabet, modulus)
    pattern_hash = init_hash(pattern, pattern, alphabet, modulus)
    for i in range(len(text) - len(pattern)):
        if text_hash == pattern_hash and equals(text, pattern, i):
            occurrences.append(i)
        text_hash = roll_hash(text, pattern, text_hash, power, i, alphabet, modulus)
    return occurrences


def knuth_morris_pratt(text: bytes, pattern: bytes, optimized_border: bool = True) -> list[int]:
    """
    Knuth-Morris-Pratt exact string searching algorithm.

    > complexity
    - time: `O(n + p)` if `border_opt` else `O(n + p**2)`
    - space: `O(p)`

    > parameters
    - `text`: text to search for occurrences of pattern
    - `pattern`: pattern
    - `optimized_border`: use optimized border computation algorithm
    - `return`: list containing the starting index of all occurrences
    """
    def compute_border_lengths_brute_force(pattern: bytes) -> list[int]:
        """
        Compute the size of the pattern borders (longest proper prefixes which are also proper suffixes or vice versa)
        for all slices of `pattern` starting from 0.
        """
        border_lengths = [-1] * (len(pattern) + 1)
        for i in range(1, len(pattern) + 1):
            j = i - 1
            while pattern[:j] != pattern[i - j:i]:
                j -= 1
            border_lengths[i] = j
        return border_lengths

    def compute_border_lengths_opt(pattern: bytes) -> list[int]:
        """
        Optimized border computation algorithm.
        """
        border_lengths = [0] * (len(pattern) + 1)
        border_lengths[0] = -1
        i = 1
        j = 0
        while i < len(pattern):
            while j <= i + j < len(pattern) and pattern[i + j] == pattern[j]:
                j += 1
                border_lengths[i + j] = j
            i += max(1, j - border_lengths[j])
            j = max(0, border_lengths[j])
        return border_lengths

    if len(pattern) == 0:
        raise Exception('empty pattern')
    occurrences: list[int] = []
    border_lengths = compute_border_lengths_opt(
        pattern) if optimized_border else compute_border_lengths_brute_force(pattern)
    i = 0
    j = 0
    while i <= len(text) - len(pattern):
        while j < len(pattern) and text[i + j] == pattern[j]:
            j += 1
        if j == len(pattern):
            occurrences.append(i)
        i += max(1, j - border_lengths[j])
        j = border_lengths[j - 1]
    return occurrences


def baeza_yates_gonnet(text: bytes, pattern: bytes) -> list[int]:
    """
    Baeza-Yates–Gonnet exact string searching algorithm.
    This algorithm is also known as shift-or, shift-and, or bitap.

    > complexity
    - time: `O(n + p)`
    - space: `O(1)`

    > parameters
    - `text`: text to search for occurrences of pattern
    - `pattern: bytes`: pattern
    - `return`: list containing the starting index of all occurrences
    """
    def compute_char_masks(pattern: bytes) -> tuple[list[int], int]:
        """
        Compute character masks for the pattern, to be used in the shifting operations.
        """
        char_masks = [0] * 256
        match_mask = 1 << len(pattern) - 1
        for i, byte in enumerate(pattern):
            char_masks[byte] |= 1 << i
        return char_masks, match_mask

    if len(pattern) == 0:
        raise Exception('empty pattern')
    occurrences: list[int] = []
    char_masks, match_mask = compute_char_masks(pattern)
    current_mask = 0
    for i in range(len(text)):
        current_mask = ((current_mask << 1) | 1) & char_masks[text[i]]
        if current_mask & match_mask != 0:
            occurrences.append(i - len(pattern) + 1)
    return occurrences


def boyer_moore(text: bytes, pattern: bytes, extended_bad_char_table: bool = True):
    """
    Boyer-Moore exact string searching algorithm.

    > complexity
    - time: `O(n + p)`
    - space: `O(1)` if not `extended_bad_char_table` else `O(p)`

    > parameters
    - `text`: text to search for occurrences of pattern
    - `pattern`: pattern
    - `return`: list containing the starting index of all occurrences
    """
    def compute_basic_bad_char_table(pattern: bytes) -> list[list[int]]:
        """
        Compute the basic bad character table.
        Basic bad character table contains the index of the last occurrence of a character in the pattern.
        If the mismatch index is smaller than the last occurrence index, this table proposes a backward shift
        (or negative shift), which must be ignored by shifting +1 forward.
        The extended table does not have this issue.
        This table is placed inside another list for compatibility with the extended table.

        Example:
        ```
        pattern:
          0   1   2   3   4   5   6   len=7
        +---+---+---+---+---+---+---+
        | a | v | o | c | a | d | o |
        +---+---+---+---+---+---+---+

        bad character table:
          a   v   o   c   d   *
        +---+---+---+---+---+---+
        | 4 | 1 | 6 | 3 | 5 |-1 |
        +---+---+---+---+---+---+
        ```
        """
        table = [-1] * 256
        for i, byte in enumerate(pattern):
            table[byte] = i
        return [table]

    def compute_extended_bad_char_table(pattern: bytes) -> list[list[int]]:
        """
        Compute the extended bad character table.
        Extended bad character table contains the index of the last occurrence of a character in the pattern for each
        prefix (after mismatch index) of the pattern.
        This allows finding more skips when larger sequences were already matched before, but it uses `p` space.

        Example:
        ```
        pattern:
          0   1   2   3   4   5   6   len=7
        +---+---+---+---+---+---+---+
        | a | v | o | c | a | d | o |
        +---+---+---+---+---+---+---+

        extended bad character table:
          a   v   o   c   d   *
        +---+---+---+---+---+---+
        |-1 |-1 |-1 |-1 |-1 |-1 | <- mismatch at index 0 (a) prefix: ''
        +---+---+---+---+---+---+
        | 0 |-1 |-1 |-1 |-1 |-1 | <- mismatch at index 1 (v) prefix: 'a'
        +---+---+---+---+---+---+
        | 0 | 1 |-1 |-1 |-1 |-1 | <- mismatch at index 2 (o) prefix: 'av'
        +---+---+---+---+---+---+
        | 0 | 1 | 2 |-1 |-1 |-1 | <- mismatch at index 3 (c) prefix: 'avo'
        +---+---+---+---+---+---+
        | 0 | 1 | 2 | 3 |-1 |-1 | <- mismatch at index 4 (a) prefix: 'avoc'
        +---+---+---+---+---+---+
        | 4 | 1 | 2 | 3 |-1 |-1 | <- mismatch at index 5 (d) prefix: 'avoca'
        +---+---+---+---+---+---+
        | 4 | 1 | 2 | 3 | 5 |-1 | <- mismatch at index 6 (o) prefix: 'avocad'
        +---+---+---+---+---+---+
        | 4 | 1 | 6 | 3 | 5 |-1 | <- before any comparisons prefix: 'avocado' (not used, just for checking, this is the one used by the basic algorithm) 
        +---+---+---+---+---+---+
        ```
        """
        table = [[-1] * 256]
        for i in range(len(pattern)):
            byte = pattern[i]
            prefix_table = table[i][:]
            prefix_table[byte] = i
            table.append(prefix_table)
        return table

    def compute_good_suffix_table(pattern: bytes) -> list[int]:
        """
        Compute the strong good suffix heuristic.
        """
        shift = [0] * (len(pattern) + 1)
        i = len(pattern)
        j = len(pattern) + 1
        f = [0] * (len(pattern) + 1)
        f[i] = j
        while i > 0:
            while j <= len(pattern) and pattern[i - 1] != pattern[j - 1]:
                if shift[j] == 0:
                    shift[j] = j - i
                j = f[j]
            i -= 1
            j -= 1
            f[i] = j
        j = f[0]
        for i in range(0, len(pattern) + 1):
            if shift[i] == 0:
                shift[i] = j
            if i == j:
                j = f[j]
        return shift

    if len(pattern) == 0:
        raise Exception('empty pattern')
    occurrences: list[int] = []
    bad_char_table = compute_extended_bad_char_table(pattern) \
        if extended_bad_char_table else compute_basic_bad_char_table(pattern)
    good_suffix_table = compute_good_suffix_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            occurrences.append(i)
            i += good_suffix_table[0]
            continue
        i += max(j - bad_char_table[j % len(bad_char_table)][text[i + j]], good_suffix_table[j + 1])
    return occurrences


def aho_corasick(text: bytes, patterns: list[bytes]) -> dict[bytes, list[int]]:
    """
    Aho-Corasick string exact multi string searching algorithm.

    > complexity
    - time: `O(n + p)`, where `p` is the sum of the length of all patterns
    - space: `O(p)`, where `p` is the sum of the length of all patterns

    > parameters
    - `text`: text to search for occurrences of pattern
    - `patterns`: list of patterns to search
    - `return`: dictionary containing patterns and list with starting indices of the occurrences
    """
    def build_goto(patterns: list[bytes]) -> tuple[dict[tuple[int, int], int], list[list[bytes]]]:
        """
        Build all trie forward links (goto link) based on `patterns`.
        The trie is a dictionary where each key is a tuple of a vertex index and a character (byte), and the value is
        the next vertex index.
        This function also returns the goal vertices, which is a list indexable by a trie vertex index, each index
        contains a list o patterns that occur at the vertex.

        > complexity
        - time: `O(p)`, where `p` is the sum of the length of all patterns
        - space: `O(p)`, where `p` is the sum of the length of all patterns

        > parameters
        - `patterns`: list of patterns to be searched
        - `return`: tuple containing the trie and goal vertices
        """
        trie: dict[tuple[int, int], int] = {}
        goals: list[list[bytes]] = [[]]
        vertex = 0
        for pattern in patterns:
            if len(pattern) == 0:
                raise Exception('empty pattern')
            cursor = 0
            for byte in pattern:
                if (cursor, byte) in trie:
                    cursor = trie[(cursor, byte)]
                else:
                    vertex += 1
                    trie[(cursor, byte)] = vertex
                    cursor = vertex
                    goals.append([])
            goals[cursor].append(pattern)
        for byte in range(256):
            if (0, byte) not in trie:
                trie[(0, byte)] = 0
        return trie, goals

    def build_fail(trie: dict[tuple[int, int], int], goals: list[list[bytes]]) -> tuple[list[int], list[list[bytes]]]:
        """
        Build all trie fail links, and update goals when fails happen in goal vertices.

        > complexity
        - time: `O(p)`, where `p` is the sum of the length of all patterns
        - space: `O(p)`, where `p` is the sum of the length of all patterns

        > parameters
        - `trie`: the trie computed in `build_goto`
        - `goals`: the goals computed in `build_goto`
        - `return`: tuple containing the fail links and goals vertices updated
        """
        vertices = len(goals)
        fail = [0] * vertices
        queue = collections.deque[int]()
        for byte in range(256):
            if trie[(0, byte)] != 0:
                queue.append(trie[(0, byte)])
                fail[trie[(0, byte)]] = 0
        while len(queue) > 0:
            cursor = queue.popleft()
            for byte in range(256):
                if (cursor, byte) in trie:
                    next = trie[(cursor, byte)]
                    queue.append(next)
                    brd = fail[cursor]
                    while (brd, byte) not in trie:
                        brd = fail[brd]
                    fail[next] = trie[(brd, byte)]
                    goals[next].extend(goals[fail[next]])
        return fail, goals

    def build_trie(patterns: list[bytes]) -> tuple[dict[tuple[int, int], int], list[int], list[list[bytes]]]:
        """
        Call `build_goto` and `build_fail` to create the trie.
        """
        trie, goals = build_goto(patterns)
        fail, goals = build_fail(trie, goals)
        return trie, fail, goals

    trie, fail, goals = build_trie(patterns)
    occurrences: dict[bytes, list[int]] = {pattern: [] for pattern in patterns}
    cursor = 0
    for i, byte in enumerate(text):
        while (cursor, byte) not in trie:
            cursor = fail[cursor]
        cursor = trie[(cursor, byte)]
        for pattern in goals[cursor]:
            occurrences[pattern].append(i - len(pattern) + 1)
    return occurrences


def test():
    import random

    from ..test import benchmark

    def random_bytes(size: int, alphabet_size: int):
        return bytes(random.randint(0, alphabet_size - 1) for _ in range(size))

    def test_native(text: bytes, pattern: bytes):
        occurrences = []
        i = -1
        while (i := text.find(pattern, i + 1)) != -1:
            occurrences.append(i)
        return occurrences

    print('alphabet size = 4')
    benchmark(
        (
            ('           brute force', lambda args: brute_force(*args)),
            ('            rabin karp', lambda args: rabin_karp(*args)),
            ('    knuth morris pratt', lambda args: knuth_morris_pratt(*args, False)),
            ('knuth morris pratt opt', lambda args: knuth_morris_pratt(*args, True)),
            ('    baeza yates gonnet', lambda args: baeza_yates_gonnet(*args)),
            ('           boyer moore', lambda args: boyer_moore(*args, False)),
            ('       boyer moore opt', lambda args: boyer_moore(*args, True)),
            ('          aho corasick', lambda args: aho_corasick(args[0], [args[1]])),
            ('                native', lambda args: test_native(*args)),
        ),
        test_inputs=((b'hello world!', b'o w'), (b'cagtcatgcatacgtctatatcggctgc', b'cat')),
        bench_sizes=((1000, 1), (1000, 5), (1000, 10), (1000, 20), (10000, 1), (10000, 5), (10000, 10), (10000, 20)),
        bench_input=lambda s: (random_bytes(s[0], 4), random_bytes(s[1], 4)),
    )
    print('alphabet size = 256')
    benchmark(
        (
            ('           brute force', lambda args: brute_force(*args)),
            ('            rabin karp', lambda args: rabin_karp(*args)),
            ('    knuth morris pratt', lambda args: knuth_morris_pratt(*args, False)),
            ('knuth morris pratt opt', lambda args: knuth_morris_pratt(*args, True)),
            ('    baeza yates gonnet', lambda args: baeza_yates_gonnet(*args)),
            ('           boyer moore', lambda args: boyer_moore(*args, False)),
            ('       boyer moore opt', lambda args: boyer_moore(*args, True)),
            ('          aho corasick', lambda args: aho_corasick(args[0], [args[1]])),
            ('                native', lambda args: test_native(*args)),
        ),
        test_inputs=(),
        bench_sizes=((1000, 1), (1000, 5), (1000, 10), (1000, 20), (10000, 1), (10000, 5), (10000, 10), (10000, 20)),
        bench_input=lambda s: (random_bytes(s[0], 256), random_bytes(s[1], 256)),
    )


if __name__ == '__main__':
    test()
