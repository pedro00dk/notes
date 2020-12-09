import math


def little_endian_base_128_encode(value: int):
    """
    Little Endian Base 128 (LEB128) algorithm for integer encoding.
    This is the basic algorithm implementation and only works with unsigned integers.

    > complexity:
    - time: `O(log(n))` where `n` is the absolute value of `value`, this log has base 128
    - space: `O(log(n))` where `n` is the absolute value of `value`, this log has base 128

    > parameters:
    - `value: int`: value to encode, negative values are not supported

    > `return: bytearray`: the encoded bytes
    """
    encoded = bytearray()
    while value >= 0x80:
        encoded.append(value & 0x7f | 0x80)
        value >>= 7
    encoded.append(value)
    return encoded


def little_endian_base_128_decode(encoded=bytes, /, start=0):
    """
    Little Endian Base 128 (LEB128) algorithm for integer decoding.
    This is the basic algorithm implementation and only works with unsigned integer.

    > complexity:
    - time: `O(log(n))` where `n` is the absolute value of `value`, this log has base of 127
    - space: `O(log(n))` where `n` is the absolute value of `value`, this log has base of 127

    > parameters:
    - `encoded: bytearray? = bytearray()`: bytearray containing encoded value, if not provided, a new one is created
    - `start: int? = 0`: starting index in encoded to start decoding

    > `return: bytearray`: the encoded bytes
    """
    value = 0
    for i, j in enumerate(range(start, len(encoded))):
        byte = encoded[j]
        value |= (byte & 0x7f) << 7 * i
        if byte < 0x80:
            break
    return value


def test():
    import random
    from ..test import match

    def test_encoder(value: int):
        encoded = little_endian_base_128_encode(value)
        decoded = little_endian_base_128_decode(encoded)
        return decoded, len(encoded)

    match(
        [
            (test_encoder, (0,), (0, 1)),
            (test_encoder, (1,), (1, 1)),
            (test_encoder, (127,), (127, 1)),
            (test_encoder, (128,), (128, 2)),
            (test_encoder, (16383,), (16383, 2)),
            (test_encoder, (16384,), (16384, 3)),
            (test_encoder, (16383,), (16383, 2)),
            (test_encoder, (16384,), (16384, 3)),
            (test_encoder, (2097151,), (2097151, 3)),
            (test_encoder, (2097152,), (2097152, 4)),
            (test_encoder, (268435455,), (268435455, 4)),
            (test_encoder, (268435456,), (268435456, 5)),
        ]
    )


if __name__ == '__main__':
    test()
