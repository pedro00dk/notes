import ctypes
import io
import mmap


def read(*, file: str = None, filemap=None, string: str = None, byte: bytes = None):
    """
    Returns an indexable object from a file, string or bytes, this function allows running searching algorithms in any
    of these types.

    If a file is provided, it is assumed to use the `utf-8` encoding.
    If a string is provided, it is converted to `bytes` using `utf-8` encoding (requires copying).

    If a file is provided, an immutable `mmap.mmap` is returned (works like `bytes` and `bytearray`).
    If a string or bytes is provided, a `bytes` is returned, strings are converted to bytes using `utf-8`.

    `return: (mmap.mmap | bytes, () => void)`: buffer to access file, string or bytes, and a finalize function to close
        resources if any are open
    """
    if file is not None:
        file = open(file, 'rb')
        mm = mmap.mmap(file.fileno(), 0, prot=mmap.PROT_READ)
        return mm, lambda: (mm.close(), file.close())
    if string is not None:
        return io.BytesIO(bytes(string, 'utf-8')), lambda: ()
    if byte is not None:
        return io.BytesIO(byte), lambda: ()
    raise Exception('no source was provided')


def exact_brute_force(text: bytes, pattern: bytes):
    """
    Brute force exact string searching algorithm.
    Some string searching algorithms do not support empty `pattern`.
    For maching specifications, all algorithms raise exceptions if the `pattern` is empty.

    > complexity:
    - time: `O(n * p)`
    - space: `O(1)`

    > parameters:
    - `text: bytes | mmap.mmap`: text to search for occurrences of pattern
    - `pattern: bytes`: pattern

    > `return: int[]`: list containing the starting index of all occurrences
    """
    if len(pattern) == 0:
        raise Exception('empty pattern')
    occurrences = []
    for i in range(len(text) - len(pattern) + 1):
        j = 0
        while j < len(pattern) and text[i + j] == pattern[j]:
            j += 1
        if j == len(pattern):
            occurrences.append(i)
    return occurrences


def exact_rabin_karp(text: bytes, pattern: bytes, /, alphabet=256, modulus=2147483647):
    """
    Rabin-Karp exact string searching algorithm.

    > complexity:
    - time: average: `O(n + p)`, worst: `O(n * p)`
    - space: `O(1)`

    > parameters:
    - `text: bytes | mmap.mmap`: text to search for occurrences of pattern
    - `pattern: bytes`: pattern
    - `alphabet: int? = 256`: size of the alphabet (max 256 because comparisons are done per byte)
    - `modulus: int? = 2147483647`: modulus value use to limit the size of the hashes

    > `return: int[]`: list containing the starting index of all occurrences
    """
    alphabet = min(max(2, alphabet), 256)
    modulus = max(modulus, 257)

    def compute_power(pattern: int):
        """
        Compute the largest multiplicative coefficient for a hash of length equals to `len(pattern)`.
        """
        power = 1
        for i in range(len(pattern) - 1):
            power = (power * alphabet) % modulus
        return power

    def init_hash(text: bytes, pattern: int):
        """
        Compute initial hash for `text` using the length of `pattern`.
        """
        hash = 0
        for i in range(len(pattern)):
            hash = (hash * alphabet + text[i]) % modulus
        return hash

    def roll_hash(text: bytes, pattern: bytes, hash: int, power: int, i: int):
        """
        Roll the current `hash` of `text[i: i + len(pattern)]` to `text[i + 1: i + len(pattern) + 1]`.
        This is done by removing `text[index]` from the hash (which was multiplied by `power`), then multiply the hash
        by `alphabet` to update the coefficients of the remaining values, then add `text[index+length]` to the hash.
        """
        return ((hash - text[i] * power) * alphabet + text[i + len(pattern)]) % modulus

    def equals(text: bytes, pattern: bytes, i: int):
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
    occurrences = []
    power = compute_power(pattern)
    text_hash = init_hash(text, pattern)
    pattern_hash = init_hash(pattern, pattern)
    for i in range(len(text) - len(pattern)):
        if text_hash == pattern_hash and equals(text, pattern, i):
            occurrences.append(i)
        text_hash = roll_hash(text, pattern, text_hash, power, i)
    return occurrences


def exact_knuth_morris_pratt(text: bytes, pattern: bytes, /, border_opt=True):
    """
    Knuth-Morris-Pratt exact string searching algorithm.

    > complexity:
    - time: `O(n + p)` if `border_opt` else `O(n + p**2)`
    - space: `O(p)`

    > parameters:
    - `text: bytes | mmap.mmap`: text to search for occurrences of pattern
    - `pattern: bytes`: pattern
    - `border_opt: bool? = True`: use optimized border computation algorithm

    > `return: int[]`: list containing the starting index of all occurrences
    """
    def compute_border_lengths_brute_force(pattern: bytes):
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

    def compute_border_lengths_opt(pattern: bytes):
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
    occurrences = []
    border_lengths = compute_border_lengths_opt(pattern) if border_opt else compute_border_lengths_brute_force(pattern)
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


def exact_baeza_yates_gonnet(text: bytes, pattern: bytes):
    """
    Baeza-Yates–Gonnet exact string searching algorithm.
    This algorithm is also known as shift-or, shift-and, or bitap.

    > complexity:
    - time: `O(n + p)`
    - space: `O(1)`

    > parameters:
    - `text: bytes | mmap.mmap`: text to search for occurrences of pattern
    - `pattern: bytes`: pattern

    > `return: int[]`: list containing the starting index of all occurrences
    """
    def compute_char_masks(pattern: bytes):
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
    occurrences = []
    char_masks, match_mask = compute_char_masks(pattern)
    current_mask = 0
    for i in range(len(text)):
        current_mask = ((current_mask << 1) | 1) & char_masks[text[i]]
        if current_mask & match_mask != 0:
            occurrences.append(i - len(pattern) + 1)
    return occurrences


def exact_boyer_moore(text: bytes, pattern: bytes, /, extended_bad_char_table=True):
    """
    Boyer-Moore exact string searching algorithm.

    > complexity:
    - time: `O(n + p)`
    - space: `O(1)` if not `extended_bad_char_table` else `O(p)`

    > parameters:
    - `text: bytes | mmap.mmap`: text to search for occurrences of pattern
    - `pattern: bytes`: pattern

    > `return: int[]`: list containing the starting index of all occurrences
    """
    def compute_basic_bad_char_table(pattern: bytes):
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

    def compute_extended_bad_char_table(pattern: bytes):
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
        table = [None] * (len(pattern) + 1)
        table[0] = [-1] * 256
        for i in range(len(pattern)):
            byte = pattern[i]
            prefix_table = table[i][:]
            prefix_table[byte] = i
            table[i + 1] = prefix_table
        return table

    def compute_good_suffix_table(pattern: bytes):
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
    occurrences = []
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


def exact_aho_corasick(text: bytes, patterns: list):
    """
    Aho-Corasick string exact multi string searching algorithm.

    > complexity:
    - time: `O()`
    - space: `O()`

    > parameters:
    - `text: bytes | mmap.mmap`: text to search for occurrences of pattern
    - `patterns: bytes[]`: list of patterns to search

    > `return: (int, int)[]`: list of tuples containing the index of the pattern and starting index of the occurrence
    """
    pass


def test():
    import random
    from ..test import benchmark

    def random_bytes(size: int, alphabet_size: int):
        return bytes(random.randint(0, alphabet_size - 1) for i in range(size))

    def test_exact_native(text: bytes, pattern: bytes):
        occurrences = []
        i = -1
        while (i := text.find(pattern, i + 1)) != -1:
            occurrences.append(i)
        return occurrences

    print('alphabet size = 4')
    benchmark(
        [
            ('           exact brute force', lambda args: exact_brute_force(*args)),
            ('            exact rabin karp', lambda args: exact_rabin_karp(*args)),
            ('    exact knuth morris pratt', lambda args: exact_knuth_morris_pratt(*args, False)),
            ('exact knuth morris pratt opt', lambda args: exact_knuth_morris_pratt(*args, True)),
            ('    exact baeza yates gonnet', lambda args: exact_baeza_yates_gonnet(*args)),
            ('           exact boyer moore', lambda args: exact_boyer_moore(*args, False)),
            ('       exact boyer moore opt', lambda args: exact_boyer_moore(*args, True)),
            ('                exact native', lambda args: test_exact_native(*args))
        ],
        test_inputs=((b'hello world!', b'o w'), (b'cagtcatgcatacgtctatatcggctgc', b'cat')),
        bench_sizes=((1000, 1), (1000, 5), (1000, 10), (1000, 20), (10000, 1), (10000, 5), (10000, 10), (10000, 20)),
        bench_input=lambda s: (random_bytes(s[0], 4), random_bytes(s[1], 4))
    )

    print('alphabet size = 256')
    benchmark(
        [
            ('           exact brute force', lambda args: exact_brute_force(*args)),
            ('            exact rabin karp', lambda args: exact_rabin_karp(*args)),
            ('    exact knuth morris pratt', lambda args: exact_knuth_morris_pratt(*args, False)),
            ('exact knuth morris pratt opt', lambda args: exact_knuth_morris_pratt(*args, True)),
            ('    exact baeza yates gonnet', lambda args: exact_baeza_yates_gonnet(*args)),
            ('           exact boyer moore', lambda args: exact_boyer_moore(*args, False)),
            ('       exact boyer moore opt', lambda args: exact_boyer_moore(*args, True)),
            ('                exact native', lambda args: test_exact_native(*args))
        ],
        test_inputs=(),
        bench_sizes=((1000, 1), (1000, 5), (1000, 10), (1000, 20), (10000, 1), (10000, 5), (10000, 10), (10000, 20)),
        bench_input=lambda s: (random_bytes(s[0], 256), random_bytes(s[1], 256))
    )


if __name__ == '__main__':
    test()
