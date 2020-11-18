import enum
import math
import sys


class BaseAlphabet(enum.Enum):
    """
    Enumeration of base16, base32 and base64 alphabets supported by `base_encode` and `base_decode` algorithms.
    The alphabets are byre of size 32 + 1 or 64 + 1, where the last index is the padding character.
    """
    HEX = b'0123456789ABCDEF='
    RFC4648 = b'ABCEDFGHIJKLMNOPQRSTUVWXYZ234567='
    Z = b'ybndrfg8ejkmcpqxot1uwisza345h769='
    WORD_SAFE = b'23456789CFGHJMPQRVWXcfghjmpqrvwx='
    MIME64 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='


def base_encode(data: bytes, alphabet=BaseAlphabet.MIME64, padding=True, linebreak=0):
    """
    Base encode implementation.
    This implementation is based on integer shifting and will work on both little and big endian environments (both
    byte and word endianess).

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes | bytearray`: data to encode
    - `alphabet: (BaseAlphabet = BaseAlphabet.MIME54`: base alphabet
    - `padding: bool? = True`: add padding bytes if necessary
    - `linebreak: int? = 0`: if greater than 0, break the encoded data after `linebreak` bytes

    > `return: bytearray`: the encoded bytes
    """
    alphabet = alphabet.value
    bits = math.ceil(math.log2(len(alphabet) - 1))
    mask = 2 ** bits - 1
    encoded = bytearray()
    cache = 0
    shift = 0

    def consume_cache():
        """
        Consume the integer cache containing unencoded bits and append the encoded equivalent from the alphabed.
        """
        nonlocal cache
        nonlocal shift
        while (value_shift := shift - bits) >= 0:
            value = (cache >> value_shift) & mask
            cache = cache ^ (value << value_shift)
            shift -= bits
            if linebreak > 0 and len(encoded) % (linebreak + 1) == linebreak:
                encoded.extend(b'\n')
            encoded.append(alphabet[value])

    def add_padding(padchar: int, count: int):
        """
        Add padding bytes at the end of the encoded data.
        """
        for i in range(count):
            if linebreak > 0 and len(encoded) % (linebreak + 1) == linebreak:
                encoded.extend(b'\n')
            encoded.append(padchar)

    for char in data:
        cache = cache << 8 | char
        shift += 8
        consume_cache()
    if shift > 0:
        cache = cache << (bits - shift)
        shift += bits - shift
        consume_cache()
    if padding:
        byte_block = round(8 / math.gcd(8, bits))
        byte_count = len(encoded) if linebreak == 0 else len(encoded) - math.floor(len(encoded) / (linebreak + 1))
        remaining = -byte_count % byte_block
        add_padding(alphabet[-1], remaining)
    return encoded


def base_decode(data: bytes, alphabet=BaseAlphabet.MIME64, ignore_garbage=False):
    """
    Base decode implementation.
    This implementation is based on integer shifting and will work on both little and big endian environments (both
    byte and word endianess).

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes | bytearray`: data to decode
    - `alphabet: (BaseAlphabet = BaseAlphabet.MIME54`: base alphabet
    - `ignore_garbage: bool? = False`: ignore invalid bytes (line breaks and paddings are always ignored)

    > `return: bytearray`: the decoded bytes
    """
    alphabet = alphabet.value
    reversed_alphabed = [None] * 256
    for i, char in enumerate(alphabet[:-1]):
        reversed_alphabed[char] = i
    linebreak_ascii = ord(b'\n')
    padding_ascii = alphabet[-1]
    bits = math.ceil(math.log2(len(alphabet) - 1))
    mask = 2 ** 8 - 1
    decoded = bytearray()
    cache = 0
    shift = 0

    def consume_cache():
        """
        Consume the integer cache containing unencoded bits and append the available bytes to the decoded data.
        """
        nonlocal cache
        nonlocal shift
        while (value_shift := shift - 8) >= 0:
            value = (cache >> value_shift) & mask
            cache = cache ^ (value << value_shift)
            shift -= 8
            decoded.append(value)

    for char in data:
        data = reversed_alphabed[char]
        if char == linebreak_ascii or char == padding_ascii:
            continue
        if data is None and not ignore_garbage:
            raise Exception('data contains garbage characters')
        cache = cache << bits | data
        shift += bits
        consume_cache()
    return decoded


def test():
    import base64
    import random
    from ..test import benchmark

    def random_bytes(size: int, alphabet_size: int):
        return bytes(random.randint(0, alphabet_size - 1) for i in range(size))

    def test_base(data: bytes, alphabet: BaseAlphabet):
        encoded = base_encode(data, alphabet)
        decoded = base_decode(encoded, alphabet)
        return decoded, encoded

    def test_native(data: bytes, encode, decode):
        encoded = encode(data)
        decoded = decode(encoded)
        return decoded, encoded

    print('alphabet size = 4')
    benchmark(
        [
            ('      base16 HEX', lambda data: test_base(data, BaseAlphabet.HEX)),
            ('  base32 RFC4648', lambda data: test_base(data, BaseAlphabet.RFC4648)),
            ('        base32 Z', lambda data: test_base(data, BaseAlphabet.Z)),
            ('base32 Word Safe', lambda data: test_base(data, BaseAlphabet.WORD_SAFE)),
            ('   base64 MIME64', lambda data: test_base(data, BaseAlphabet.MIME64)),
            ('   native base16', lambda data: test_native(data, base64.b16encode, base64.b16decode)),
            ('   native base32', lambda data: test_native(data, base64.b32encode, base64.b32decode)),
            ('   native base64', lambda data: test_native(data, base64.b64encode, base64.b64decode)),
            ('   native base85', lambda data: test_native(data, base64.b85encode, base64.b85decode)),
            ('  native ascii85', lambda data: test_native(data, base64.a85encode, base64.a85decode)),
        ],
        test_inputs=(b'Man', b'hello world!', b'Pedro'),
        bench_sizes=(100, 1000, 10000, 100000),
        bench_input=lambda s: random_bytes(s, 256)
    )


if __name__ == '__main__':
    test()
