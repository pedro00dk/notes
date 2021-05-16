def edit_distance_brute_force(text_a: bytes, text_b: bytes, i: int = 0, j: int = 0) -> int:
    """
    Compute the edit distance between `text_a` and `text_b`, starting from `i` and `j` respectively.
    The distance used is the Levenshtein distance, which allows deletion, insertion and substitution.

    > complexity
    - time: `O(3**(n + m))`
    - space: `O(n + m)`
    - `n`: length of `text_a`
    - `m`: length of `text_b`

    > parameters
    - `text_a`: data to compute distance
    - `text_b`: data to compute distance
    - `i`: staring index in `text_a`
    - `j`: staring index in `text_b`
    - `return`: edit distance between `text_a` and `text_b`
    """
    if i == len(text_a):
        return len(text_b) - j  # text_a fully consumed, insert remaining text_b in text_a or remove from text_b
    elif j == len(text_b):
        return len(text_a) - i  # text_a fully consumed, insert remaining text_a in text_b or remove from text_a
    return min(
        edit_distance_brute_force(text_a, text_b, i + 1, j) + 1,  # delete text_a char (insert text_b char)
        edit_distance_brute_force(text_a, text_b, i, j + 1) + 1,  # insert text_a char (delete text_b char)
        edit_distance_brute_force(text_a, text_b, i + 1, j + 1) + (text_a[i] != text_b[j]),  # swap if different
    )


def edit_distance_wagner_fischer(text_a: bytes, text_b: bytes) -> int:
    """
    Wagner-Fisher edit distance algorithm.
    The distance used is the Levenshtein distance.

    > complexity
    - time: `O(n*m)`
    - space: `O(n*m)`
    - `n`: length of `text_a`
    - `m`: length of `text_b`

    > parameters
    - `text_a`: data to compute distance
    - `text_b`: data to compute distance
    - `return`: edit distance between `text_a` and `text_b`
    """
    distances = [[0] * (len(text_b) + 1) for _ in range(len(text_a) + 1)]
    for i in range(1, len(text_a) + 1):
        distances[i][0] = i
    for i in range(1, len(text_b) + 1):
        distances[0][i] = i
    for i in range(1, len(text_a) + 1):
        for j in range(1, len(text_b) + 1):
            cost = text_a[i - 1] != text_b[j - 1]
            distances[i][j] = min(distances[i - 1][j] + 1, distances[i][j - 1] + 1, distances[i - 1][j - 1] + cost)
    return distances[-1][-1]


def edit_distance_wagner_fischer_opt(text_a: bytes, text_b: bytes) -> int:
    """
    Check base Wagner-Fisher algorithm for documentation.

    > optimizations
    - reuse same arrays by swapping them

    > complexity
    - time: `O(n*m)`
    - space: `O(min(n, m))`
    - `n`: length of `text_a`
    - `m`: length of `text_b`
    """
    if len(text_a) < len(text_b):
        text_a, text_b = text_b, text_a
    distances = [[*range(len(text_b) + 1)], [0] * (len(text_b) + 1)]
    for i in range(1, len(text_a) + 1):
        distances[1][0] = i
        for j in range(1, len(text_b) + 1):
            cost = text_a[i - 1] != text_b[j - 1]
            distances[1][j] = min(distances[0][j] + 1, distances[1][j - 1] + 1, distances[0][j - 1] + cost)
        distances.reverse()
    return distances[0][-1]


def test():
    import random

    from ..test import benchmark

    def random_bytes(size: int, alphabet_size: int) -> bytes:
        return bytes(random.randint(0, alphabet_size - 1) for _ in range(size))

    print('all algorithms')
    benchmark(
        (
            ('        edit distance brute force', lambda args: edit_distance_brute_force(*args)),
            ('     edit distance wagner-fischer', lambda args: edit_distance_wagner_fischer(*args)),
            (' edit distance wagner-fischer opt', lambda args: edit_distance_wagner_fischer_opt(*args)),
        ),
        test_inputs=((b'kitten', b'sitting'), (b'saturday', b'monday'), (b'', b'')),
        bench_sizes=((0, 0), (1, 1), (5, 3), (10, 5)),
        bench_input=lambda s: (random_bytes(s[0], 256), random_bytes(s[1], 256)),
    )
    print('without brute force')
    benchmark(
        (
            ('     edit distance wagner-fischer', lambda args: edit_distance_wagner_fischer(*args)),
            (' edit distance wagner-fischer opt', lambda args: edit_distance_wagner_fischer_opt(*args)),
        ),
        test_inputs=(),
        bench_sizes=((20, 8), (20, 16), (100, 35), (100, 70), (1000, 350), (1000, 700)),
        bench_input=lambda s: (random_bytes(s[0], 256), random_bytes(s[1], 256)),
    )


if __name__ == '__main__':
    test()
