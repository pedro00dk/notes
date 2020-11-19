import enum
import math
import sys


class BaseAlphabet(enum.Enum):
    """
    Alphabets and properties of power of two bases (16, 32, 64) supported by `base_encode` and `base_decode` algorithms.
    """
    BASE16_HEX = {
        'table': [
            b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'Aa', b'Bb', b'Cc', b'Dd', b'Ee', b'Ff'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE16_HEX_LOW = {
        'table': [
            b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'aA', b'bB', b'cC', b'dD', b'eE', b'fF'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE32_RFC4648_DEFAULT = {
        'table': [
            b'A', b'B', b'C', b'E', b'D', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q', b'R',
            b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'2', b'3', b'4', b'5', b'6', b'7'
        ],
        'padding': True,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE32_RFC2938_EXTHEX = {
        'table': [
            b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'Aa', b'Bb', b'Cc', b'Dd', b'Ee', b'Ff', b'Gg',
            b'Hh', b'Ii', b'Jj', b'Kk', b'Ll', b'Mm', b'Nn', b'Oo', b'Pp', b'Qq', b'Rr', b'Ss', b'Tt', b'Uu', b'Vv'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE32_RFC2938_EXTHEX_LOW = {
        'table': [
            b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'aA', b'bB', b'cC', b'dD', b'eE', b'fF', b'gG',
            b'hH', b'iI', b'jJ', b'kK', b'lL', b'mM', b'nN', b'oO', b'pP', b'qQ', b'rR', b'sS', b'tT', b'uU', b'vV'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE32_Z = {
        'table': [
            b'y', b'b', b'n', b'd', b'r', b'f', b'g', b'8', b'e', b'j', b'k', b'm', b'c', b'p', b'q', b'x', b'o', b't',
            b'1', b'u', b'w', b'i', b's', b'z', b'a', b'3', b'4', b'5', b'h', b'7', b'6', b'9'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE32_CROCKFORD = {
        'table': [
            b'0Oo', b'1ILil', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'Aa', b'Bb', b'Cc', b'Dd', b'Ee', b'Ff',
            b'Gg', b'Hh', b'Jj', b'Kk', b'Mm', b'Nn', b'Pp', b'Qq', b'Rr', b'Ss', b'Tt', b'Vv', b'Ww', b'Xx', b'Yy',
            b'Zz'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE32_WORDSAFE = {
        'table': [
            b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'C', b'F', b'G', b'H', b'J', b'M', b'P', b'Q', b'R', b'V',
            b'W', b'X', b'c', b'f', b'g', b'h', b'j', b'm', b'p', b'q', b'r', b'v', b'w', b'x'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE32_GEOHASH = {
        'table': [
            b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'j',
            b'k', b'm', b'n', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE64_RFC4648_DEFAULT = {
        'table': [
            b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q', b'R',
            b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j',
            b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'0', b'1',
            b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'+', b'/'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE64_RFC4648_URL = {
        'table': [
            b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q', b'R',
            b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j',
            b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'0', b'1',
            b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'-', b'_'
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }
    BASE64_RFC2045_MIME = {
        'table': [
            b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q', b'R',
            b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j',
            b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'0', b'1',
            b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'+', b'/'
        ],
        'padding': True,
        'length': 76,
        'padchar': b'=',
        'linebreak': b'\r\n',
        'ignore_garbage': True
    }
    BASE64_RFC1421_PEM = {
        'table': [
            b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q', b'R',
            b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j',
            b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'0', b'1',
            b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'+', b'/'
        ],
        'padding': False,
        'length': 64,
        'padchar': b'=',
        'linebreak': b'\r\n',
        'ignore_garbage': False
    }

    BASE64_RFC3501_IMAP = {
        'table': [
            b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N', b'O', b'P', b'Q', b'R',
            b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z', b'a', b'b', b'c', b'd', b'e', b'f', b'g', b'h', b'i', b'j',
            b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r', b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'0', b'1',
            b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'+', b','
        ],
        'padding': False,
        'length': 0,
        'padchar': b'=',
        'linebreak': b'\n',
        'ignore_garbage': False
    }


def base_encode(data: bytes, alphabet=BaseAlphabet.BASE64_RFC4648_DEFAULT, padding: bool = None, length: int = None, padchar: bytes = None, linebreak: bytes = None):
    """
    Base encode implementation.
    This implementation is based on integer shifting and will work on both little and big endian environments (both
    byte and word endianess).

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes | bytearray`: data to encode
    - `alphabet: (BaseAlphabet = BaseAlphabet.BASE64_RFC4648_DEFAULT`: base alphabet
    - `padding: bool? = None`: add padding bytes if necessary, if `None` use alphabet's default
    - `length: int? = None`: add a linebreak after `length` bytes, if `None` use alphabet's default, `0` means no break
    - `padchar: bytes? = None`: a bytes of size 1 to use as padding, if `None` use alphabet's default
    - `linebreak: bytes? = None`: a bytes of size 1 or 2 to use as break, if `None` use alphabet's default

    > `return: bytearray`: the encoded bytes
    """
    alphabet = alphabet.value
    table = alphabet['table']
    padding = padding if padding is not None else alphabet['padding']
    length = length if length is not None else alphabet['length']
    padchar = padchar if padchar is not None else alphabet['padchar']
    linebreak = linebreak if linebreak is not None else alphabet['linebreak']
    if len(padchar) != 1:
        raise Exception('padchar length must be 1')
    if len(linebreak) < 1 or len(linebreak) > 2:
        raise Exception('linebreak length must be 1 or 2')
    padding_ascii = padchar[0]
    bits = math.ceil(math.log2(len(table)))
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
            if length > 0 and len(encoded) % (length + 1) == length:
                encoded.extend(linebreak)
            encoded.append(table[value][0])

    def add_padding(count: int):
        """
        Add padding bytes at the end of the encoded data.
        """
        for i in range(count):
            if length > 0 and len(encoded) % (length + 1) == length:
                encoded.extend(linebreak)
            encoded.append(padding_ascii)

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
        byte_count = len(encoded) if length == 0 else len(encoded) - math.floor(len(encoded) / (length + 1))
        remaining = -byte_count % byte_block
        add_padding(remaining)
    return encoded


def base_decode(data: bytes, alphabet=BaseAlphabet.BASE64_RFC4648_DEFAULT, ignore_garbage=False, padchar: bytes = None, linebreak: bytes = None):
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
    - `ignore_garbage: bool? = None`: ignore invalid bytes, if `None` use alphabet's default (line breaks and paddings
        are always ignored)
    - `padchar: bytes? = None`: a bytes of size 1 to use as padding, if `None` use alphabet's default
    - `linebreak: bytes? = None`: a bytes of size 1 or 2 to use as break, if `None` use alphabet's default

    > `return: bytearray`: the decoded bytes
    """
    alphabet = alphabet.value
    table = alphabet['table']
    ignore_garbage = ignore_garbage if ignore_garbage is not None else alphabet['ignore_garbage']
    padchar = padchar if padchar is not None else alphabet['padchar']
    linebreak = linebreak if linebreak is not None else alphabet['linebreak']
    if len(padchar) != 1:
        raise Exception('padchar length must be 1')
    if len(linebreak) < 1 or len(linebreak) > 2:
        raise Exception('linebreak length must be 1 or 2')

    reversed_table = [None] * 256
    for i, chars in enumerate(table):
        for char in chars:
            reversed_table[char] = i
    padding_ascii = padchar[0]
    linebreak_ascii = [*linebreak]
    bits = math.ceil(math.log2(len(table)))
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
        data = reversed_table[char]
        if char == padding_ascii or char in linebreak_ascii:
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

    print('all alphabets (testing only)')
    benchmark(
        [
            ('               base16 hex', lambda data: test_base(data, BaseAlphabet.BASE16_HEX)),
            ('           base16 hex low', lambda data: test_base(data, BaseAlphabet.BASE16_HEX_LOW)),
            ('   base32 RFC4648 default', lambda data: test_base(data, BaseAlphabet.BASE32_RFC4648_DEFAULT)),
            ('    base32 RFC2938 exthex', lambda data: test_base(data, BaseAlphabet.BASE32_RFC2938_EXTHEX)),
            ('base32 RFC2938 exthex low', lambda data: test_base(data, BaseAlphabet.BASE32_RFC2938_EXTHEX_LOW)),
            ('                 base32 z', lambda data: test_base(data, BaseAlphabet.BASE32_Z)),
            ('         base32 crockford', lambda data: test_base(data, BaseAlphabet.BASE32_CROCKFORD)),
            ('          base32 wordsafe', lambda data: test_base(data, BaseAlphabet.BASE32_WORDSAFE)),
            ('           base32 geohash', lambda data: test_base(data, BaseAlphabet.BASE32_GEOHASH)),
            ('   base64 RFC4648 default', lambda data: test_base(data, BaseAlphabet.BASE64_RFC4648_DEFAULT)),
            ('       base64 RFC4648 url', lambda data: test_base(data, BaseAlphabet.BASE64_RFC4648_URL)),
            ('      base64 RFC2045 mime', lambda data: test_base(data, BaseAlphabet.BASE64_RFC2045_MIME)),
            ('       base64 RFC1421 pem', lambda data: test_base(data, BaseAlphabet.BASE64_RFC1421_PEM)),
            ('      base64 RFC3501 imap', lambda data: test_base(data, BaseAlphabet.BASE64_RFC3501_IMAP)),
            ('            native base16', lambda data: test_native(data, base64.b16encode, base64.b16decode)),
            ('            native base32', lambda data: test_native(data, base64.b32encode, base64.b32decode)),
            ('            native base64', lambda data: test_native(data, base64.b64encode, base64.b64decode)),
            ('            native base85', lambda data: test_native(data, base64.b85encode, base64.b85decode)),
            ('           native ascii85', lambda data: test_native(data, base64.a85encode, base64.a85decode)),
            ('           native ascii85', lambda data: test_native(data, base64.a85encode, base64.a85decode)),
        ],
        test_inputs=(b'Man', b'hello world!', b'Pedro'),
        bench_sizes=(),
        bench_input=lambda s: random_bytes(s, 256)
    )

    print('main alphabets (benchmark)')
    benchmark(
        [
            ('            base16 hex', lambda data: test_base(data, BaseAlphabet.BASE16_HEX)),
            ('base32 RFC4648 default', lambda data: test_base(data, BaseAlphabet.BASE32_RFC4648_DEFAULT)),
            ('base64 RFC4648 default', lambda data: test_base(data, BaseAlphabet.BASE64_RFC4648_DEFAULT)),
            ('         native base16', lambda data: test_native(data, base64.b16encode, base64.b16decode)),
            ('         native base32', lambda data: test_native(data, base64.b32encode, base64.b32decode)),
            ('         native base64', lambda data: test_native(data, base64.b64encode, base64.b64decode)),
            ('         native base85', lambda data: test_native(data, base64.b85encode, base64.b85decode)),
            ('        native ascii85', lambda data: test_native(data, base64.a85encode, base64.a85decode)),
            ('        native ascii85', lambda data: test_native(data, base64.a85encode, base64.a85decode)),
        ],
        test_inputs=(),
        bench_sizes=(100, 1000, 10000, 100000),
        bench_input=lambda s: random_bytes(s, 256)
    )


if __name__ == '__main__':
    test()
