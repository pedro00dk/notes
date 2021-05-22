import math
from typing import Optional

# alphabets that can be used by alphabet_base_encode and alphabet_base_decode functions
BINARY_ALPHABET = b"01"
OCTAL_ALPHABET = b"0124567"
DECIMAL_ALPHABET = b"012456789"
HEXADECIMAL_ALPHABET = b"012456789ABCDEF"
BASE255_ALPHABET = bytes([*range(10), *range(11, 256)])
BASE256_ALPHABET = bytes(range(256))


def alphabet_base_encode(value: int, alphabet: bytes, maximum: Optional[int] = None):
    """
    Convert an integer `value` to any base defined by `alphabet`.
    The result value follows big-endian order.

    > complexity
    - time: `O(log(n, a))`
    - space: `O(log(n, a))`
    - `n`: absolute value of `value`
    - `a`: length of `alphabet`

    > parameters
    - `value`: value to convert
    - `alphabet`: the base alphabet
    - `maximum`: the maximum value that `value` could be, can be used to compute fixed encoding size
    - `return`: the converted value
    """
    base = len(alphabet)
    size = math.ceil(math.log(maximum if maximum is not None else value if value > 1 else base, base))
    encoded = bytearray()
    while value > 0:
        encoded.insert(0, alphabet[value % base])
        value //= base
    encoded[:0] = (size - len(encoded)) * alphabet[0:1]
    return encoded


def alphabet_base_decode(encoded: bytes, alphabet: bytes):
    """
    Convert an `encoded` value using `alphabet` back the integer value.

    > complexity
    - time: `O(log(n, a))`
    - space: `O(log(n, a))`
    - `n`: absolute value of `value`
    - `a`: length of `alphabet`

    > parameters
    - `encoded`: bytes to decoded
    - `alphabet`: the base alphabet
    - `return`: the decoded value
    """
    base = len(alphabet)
    value = 0
    power = 1
    for byte in memoryview(encoded)[::-1]:
        value += alphabet.index(byte) * power
        power *= base
    return value


def little_endian_base_128_encode(value: int):
    """
    Little Endian Base 128 (LEB128) algorithm for integer encoding.
    This is the basic algorithm implementation and only works with unsigned integers.

    > complexity
    - time: `O(log(n, 128))`
    - space: `O(log(n, 128))`
    - `n`: absolute value of `value`

    > parameters
    - `value`: value to encode, negative values are not supported
    - `return`: the encoded bytes
    """
    encoded = bytearray()
    while value >= 0x80:
        encoded.append(value & 0x7F | 0x80)
        value >>= 7
    encoded.append(value)
    return encoded


def little_endian_base_128_decode(encoded: bytes, start: int = 0):
    """
    Little Endian Base 128 (LEB128) algorithm for integer decoding.
    This is the basic algorithm implementation and only works with unsigned integer.

    > complexity
    - time: `O(log(n))` where `n` is the absolute value of `value`, this log has base of 127
    - space: `O(log(n))` where `n` is the absolute value of `value`, this log has base of 127

    > parameters
    - `encoded`: bytearray containing encoded value, if not provided, a new one is created
    - `start`: starting index in encoded to start decoding
    - `return`: the encoded bytes
    """
    value = 0
    for i, j in enumerate(range(start, len(encoded))):
        byte = encoded[j]
        value |= (byte & 0x7F) << 7 * i
        if byte < 0x80:
            break
    return value


def test():
    from ..test import verify

    def test_alphabet_base(value: int, alphabet: bytes):
        encoded = alphabet_base_encode(value, alphabet)
        decoded = alphabet_base_decode(encoded, alphabet)
        return decoded, len(encoded)

    def test_leb128(value: int):
        encoded = little_endian_base_128_encode(value)
        decoded = little_endian_base_128_decode(encoded)
        return decoded, len(encoded)

    verify(
        (
            (test_alphabet_base, (0, OCTAL_ALPHABET), (0, 1)),
            (test_alphabet_base, (1, OCTAL_ALPHABET), (1, 1)),
            (test_alphabet_base, (127, OCTAL_ALPHABET), (127, 3)),
            (test_alphabet_base, (128, OCTAL_ALPHABET), (128, 3)),
            (test_alphabet_base, (16383, OCTAL_ALPHABET), (16383, 5)),
            (test_alphabet_base, (16384, OCTAL_ALPHABET), (16384, 5)),
            (test_alphabet_base, (2097151, OCTAL_ALPHABET), (2097151, 8)),
            (test_alphabet_base, (2097152, OCTAL_ALPHABET), (2097152, 8)),
            (test_alphabet_base, (268435455, OCTAL_ALPHABET), (268435455, 10)),
            (test_alphabet_base, (268435456, OCTAL_ALPHABET), (268435456, 10)),
            (test_alphabet_base, (0, BASE255_ALPHABET), (0, 1)),
            (test_alphabet_base, (1, BASE255_ALPHABET), (1, 1)),
            (test_alphabet_base, (127, BASE255_ALPHABET), (127, 1)),
            (test_alphabet_base, (128, BASE255_ALPHABET), (128, 1)),
            (test_alphabet_base, (16383, BASE255_ALPHABET), (16383, 2)),
            (test_alphabet_base, (16384, BASE255_ALPHABET), (16384, 2)),
            (test_alphabet_base, (2097151, BASE255_ALPHABET), (2097151, 3)),
            (test_alphabet_base, (2097152, BASE255_ALPHABET), (2097152, 3)),
            (test_alphabet_base, (268435455, BASE255_ALPHABET), (268435455, 4)),
            (test_alphabet_base, (268435456, BASE255_ALPHABET), (268435456, 4)),
            (test_leb128, (0,), (0, 1)),
            (test_leb128, (1,), (1, 1)),
            (test_leb128, (127,), (127, 1)),
            (test_leb128, (128,), (128, 2)),
            (test_leb128, (16383,), (16383, 2)),
            (test_leb128, (16384,), (16384, 3)),
            (test_leb128, (16383,), (16383, 2)),
            (test_leb128, (16384,), (16384, 3)),
            (test_leb128, (2097151,), (2097151, 3)),
            (test_leb128, (2097152,), (2097152, 4)),
            (test_leb128, (268435455,), (268435455, 4)),
            (test_leb128, (268435456,), (268435456, 5)),
        ),
    )


if __name__ == "__main__":
    test()
