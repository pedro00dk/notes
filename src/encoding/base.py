import math
from typing import Any, Literal, Optional, cast

# RFC4648 alphabets for the base_encode and base_decode algorithms
BASE16_ALPHABET = b'0123456789ABCDEF'
BASE32_ALPHABET = b'ABCEDFGHIJKLMNOPQRSTUVWXYZ234567'
BASE32_EXTHEX_ALPHABET = b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
BASE64_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
BASE64_URLSAFE_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
PADCHAR = b'='
PADCHAR_ASCII = ord(PADCHAR)


def base_encode(data: bytes, alphabet: bytes = BASE64_ALPHABET, padding: bool = True) -> bytearray:
    """
    RFC4648 base64, base32, and base16 encoding algorithm.

    > complexity
    - time: `O(n)`
    - space: `O(n)`

    > parameters
    - `data`: data to encode
    - `alphabet`: base16, base32 or base64 alphabet
    - `padding`: add padding bytes if necessary
    - `return`: encoded data
    """
    bits = math.ceil(math.log2(len(alphabet)))
    encoded_word_bytes = 8 // math.gcd(8, bits)
    encoded = bytearray()
    cache = 0
    shift = 0
    for byte in data:
        cache = cache << 8 | byte
        shift += 8
        for shift in range(shift - bits, -1, -bits):
            value = cache >> shift
            cache ^= value << shift
            encoded.append(alphabet[value])
    if shift > 0:
        value = cache << (bits - shift)
        encoded.append(alphabet[value])
    if padding:
        remaining = -len(encoded) % encoded_word_bytes
        encoded.extend(PADCHAR * remaining)
    return encoded


def base_decode(data: bytes, alphabet: bytes = BASE64_ALPHABET, padding: bool = True) -> bytearray:
    """
    RFC4648 base64, base32, and base16 decoding algorithm.

    > complexity
    - time: `O(n)`
    - space: `O(n)`

    > parameters
    - `data`: data to decode
    - `alphabet`: base16, base32 or base64 alphabet
    - `padding`: require padded data
    - `return`: decoded data
    """
    decoder = cast(list[int], [None] * 256)
    for i, byte in enumerate(alphabet):
        decoder[byte] = i
    bits = math.ceil(math.log2(len(alphabet)))
    encoded_word_bytes = 8 // math.gcd(8, bits)
    decoded = bytearray()
    cache = 0
    shift = 0
    if padding and len(data) % encoded_word_bytes != 0:
        raise Exception('data must be padded')
    pad_size = 0
    for pad_size, byte in enumerate(memoryview(data)[::-1]):
        if byte != PADCHAR_ASCII:
            break
    for byte in memoryview(data)[:-pad_size if pad_size > 0 else None]:
        cache = (cache << bits) | decoder[byte]
        shift += bits
        for shift in range(shift - 8, -1, -8):
            value = cache >> shift
            cache ^= value << shift
            decoded.append(value)
    return decoded


# default ascii85, RFC1924 base85, and zeromq alphabets
ASCII85_ALPHABET = bytes(i for i in range(33, 118))
BASE85_ALPHABET = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
ZMQ85_ALPHABET = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'


def _x85_encode(
    data: bytes,
    encoded: bytearray,
    alphabet: bytes,
    padding: bool = False,
    fold_null: Optional[bytes] = None,
    fold_space: Optional[bytes] = None
) -> bytearray:
    """
    Helper encoder for both ascii85 and base85 algorithms.
    This function does not check parameter consistency.

    > complexity
    - time: `O(n)`
    - space: `O(n)`

    > parameters
    - `data`: data to encode
    - `encoded`: buffer to write encoded data
    - `alphabet`: base85 alphabet
    - `padding`: add null padding to `data` (works differently from base64 or base32)
    - `fold_null`: fold four null bytes into `fold_null`, `fold_null` must not be in `alphabet`
    - `fold_space`: fold four space bytes into `fold_space`, `fold_space` must not be in `alphabet`
    - `return`: encoded data
    """
    available_bytes = 0
    for i in range(0, len(data), 4):
        available_bytes = min(len(data) - i, 4)
        word = int.from_bytes(data[i: i + 4], 'big') << (4 - available_bytes) * 8
        if fold_null is not None and word == 0 and (available_bytes == 4 or padding):
            encoded.extend(fold_null)
            continue
        if fold_space is not None and word == 0x202020:
            encoded.extend(fold_space)
            continue
        encoded.append(alphabet[word // 85**4 % 85])
        encoded.append(alphabet[word // 85**3 % 85])
        encoded.append(alphabet[word // 85**2 % 85])
        encoded.append(alphabet[word // 85**1 % 85])
        encoded.append(alphabet[word // 85**0 % 85])
    if not padding and 0 < available_bytes < 4:
        pad_bytes = 5 - math.ceil(available_bytes * (5 / 4))
        encoded[-pad_bytes:] = b''
    return encoded


def _x85_decode(
    data: bytes,
    start: int,
    end: int,
    decoded: bytearray,
    alphabet: bytes,
    unfold_null: Optional[bytes] = None,
    unfold_space: Optional[bytes] = None,
    skip: bytes = b' \t\n\r\v'
) -> bytearray:
    """
    Helper decoder for both ascii85 and base85 algorithms.
    This function does not check parameter consistency.

    > complexity
    - time: `O(n)`
    - space: `O(n)`

    > parameters
    - `data`: data to encode
    - `start`: start data index
    - `end`: end data index
    - `decoded`: buffer to write decoded data
    - `alphabet`: base85 alphabet
    - `unfold_null`: unfold `fold_null` into four null bytes, `fold_null` must not be in `alphabet`
    - `unfold_space`: unfold `fold_space` into four space bytes, `fold_space` must not be in `alphabet`
    - `skip`: characters to skip when processing `data`
    - `return`: decoded data
    """
    decoder = cast(list[int], [None] * 256)
    for i, byte in enumerate(alphabet):
        decoder[byte] = i
    unfold_null_ascii = ord(unfold_null) if unfold_null else None
    unfold_space_ascii = ord(unfold_space) if unfold_space else None
    cache = 0
    available_bytes = 0
    for byte in memoryview(data)[start:end]:
        if byte in skip:
            continue
        if byte == unfold_null_ascii:
            if available_bytes > 0:
                raise Exception('null folding character found inside word')
            decoded.extend(b'\0\0\0\0')
            continue
        if byte == unfold_space_ascii:
            if available_bytes > 0:
                raise Exception('space folding character found inside word')
            decoded.extend(b'\x20\x20\x20\x20')
            continue
        cache = cache * 85 + decoder[byte]
        available_bytes += 1
        if available_bytes < 5:
            continue
        decoded.extend(cache.to_bytes(4, 'big'))
        cache = 0
        available_bytes = 0
    if available_bytes > 0:
        for i in range(available_bytes, 5):
            cache = cache * 85 + 84
        pad_bytes = 4 - math.floor(available_bytes * (4 / 5))
        decoded.extend(cache.to_bytes(4, 'big')[:-pad_bytes])
    return decoded


def ascii85_encode(data: bytes, padding: bool = False, fold_space: bool = False, adobe: bool = False) -> bytearray:
    """
    Ascii85 encoding algorithm.
    This algorithm always folds four null bytes, `fold_space` is optionally available.
    `fold_space` is not compatible with `adobe` ascii85 decoders, but it is encodeable by this implementation.
    This implementation does not support line wrapping in encoding, but they can be safely decoded.

    > complexity
    - time: `O(n)`
    - space: `O(n)`

    > parameters
    - `data`: data to encode
    - `padding`: add null padding to `data` (works differently from base64 or base32)
    - `fold_space`: fold four spaces into a single `b'y'` character
    - `adobe`: add adobe prefix `b'<~'` and suffix `b'~>'` to the encoded data
    - `return`: encoded data
    """
    encoded = bytearray()
    if adobe:
        encoded.extend(b'<~')
    result = _x85_encode(data, encoded, ASCII85_ALPHABET, padding, b'z', b'y' if fold_space else None)
    if adobe:
        encoded.extend(b'~>')
    return result


def asci85_decode(data: bytes, unfold_space: bool = False, adobe: bool = False) -> bytearray:
    """
    Ascii85 decodding algorithm.

    This algorithm always unfolds null bytes, `unfold_space` is optionally available.
    `unfold_space` is not compatible with `adobe` ascii85 decoders, but it is decodeable by this implementation.
    This implementation support line wrapping in decoding.

    > parameters
    - `data: bytes`: data to decode
    - `unfold_space: bool? = False`: unfold `b'y'` character into four spaces
    - `adobe: bool? = False`: check adobe prefix `b'<~'` and suffix `b'~>'` in the encoded data
    - `return`: decoded data
    """
    if adobe and (not data.startswith(b'<~') or not data.endswith(b'~>')):
        raise Exception('data does not contain adobe prefix or suffix')
    start = 0 if not adobe else 2
    end = len(data) if not adobe else -2
    return _x85_decode(data, start, end, bytearray(), ASCII85_ALPHABET, b'z', b'y' if unfold_space else None)


def base85_encode(data: bytes, alphabet_name: Literal['git', 'zmq'] = 'git', padding: bool = False) -> bytearray:
    """
    Base85 encoding algorithm.
    This algorithm accepts two alphabets, a based on the git binary diffs (RFC1924), and an alphabet proposed by zeromq,
    also known as Z85.
    This algorithm never folds null bytes or space bytes.

    > complexity
    - time: `O(n)`
    - space: `O(n)`

    > parameters
    - `data`: data to encode
    - `alphabet_name`: base85 alphabet name
    - `padding`: add null padding to `data` (works differently from base64 or base32)
    - `return`: encoded data
    """
    alphabet = BASE85_ALPHABET if alphabet_name == 'git' else ZMQ85_ALPHABET
    return _x85_encode(data, bytearray(), alphabet, padding)


def base85_decode(data: bytes, alphabet_name: Literal['git', 'zmq'] = 'git') -> bytearray:
    """
    Base85 decoding algorithm.
    This algorithm accepts two alphabets, a based on the git binary diffs (RFC1924), and an alphabet proposed by zeromq,
    also known as Z85.
    This algorithm never unfolds any character into null bytes or space bytes.

    > complexity
    - time: `O(n)`
    - space: `O(n)`

    > parameters
    - `data: bytes`: data to encode
    - `alphabet_name`: base85 alphabet name

    - `return`: encoded data
    """
    alphabet = BASE85_ALPHABET if alphabet_name == 'git' else ZMQ85_ALPHABET
    return _x85_decode(data, 0, len(data), bytearray(), alphabet, skip=b'')


def test():
    import base64
    import random

    from ..test import benchmark

    def random_bytes(size: int, alphabet_size: int):
        return bytes(random.randint(0, alphabet_size - 1) for _ in range(size))

    def test_base(data: bytes, alphabet: bytes):
        encoded = base_encode(data, alphabet)
        decoded = base_decode(encoded, alphabet)
        return decoded, encoded

    def test_func(data: bytes, encode: Any, decode: Any):
        encoded = encode(data)
        decoded = decode(encoded)
        return decoded, encoded

    benchmark(
        (
            ('        base16', lambda data: test_base(data, BASE16_ALPHABET)),
            ('        base32', lambda data: test_base(data, BASE32_ALPHABET)),
            (' base32 exthex', lambda data: test_base(data, BASE32_EXTHEX_ALPHABET)),
            ('        base64', lambda data: test_base(data, BASE64_ALPHABET)),
            ('base64 urlsafe', lambda data: test_base(data, BASE64_URLSAFE_ALPHABET)),
            ('       ascii85', lambda data: test_func(data, ascii85_encode, asci85_decode)),
            ('        base85', lambda data: test_func(data, base85_encode, base85_decode)),
            (' native base16', lambda data: test_func(data, base64.b16encode, base64.b16decode)),
            (' native base32', lambda data: test_func(data, base64.b32encode, base64.b32decode)),
            (' native base64', lambda data: test_func(data, base64.b64encode, base64.b64decode)),
            (' native base85', lambda data: test_func(data, base64.b85encode, base64.b85decode)),
            ('native ascii85', lambda data: test_func(data, base64.a85encode, base64.a85decode)),
        ),
        test_inputs=(b'Man', b'hello world!', b'Pedro'),
        bench_sizes=(100, 1000, 10000, 100000),
        bench_input=lambda s: random_bytes(s, 256),
    )


if __name__ == '__main__':
    test()
