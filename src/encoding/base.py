import enum
import math
import sys

# RFC4648 alphabets for the base_encode and base_decode algorithms
BASE16_ALPHABET = b'0123456789ABCDEF'
BASE32_ALPHABET = b'ABCEDFGHIJKLMNOPQRSTUVWXYZ234567'
BASE32_EXTHEX_ALPHABET = b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
BASE64_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
BASE64_URLSAFE_ALPHABET = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
PADCHAR = b'='
PADCHAR_ASCII = ord(PADCHAR)


def base_encode(data: bytes, alphabet=BASE64_ALPHABET, /, padding=True):
    """
    RFC4648 base64, base32, and base16 encoding algorithm.

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes`: data to encode
    - `alphabet: bytes? = BASE64_ALPHABET`: base16, base32 or base64 alphabet
    - `padding: bool? = None`: add padding bytes if necessary
    """
    bits = math.ceil(math.log2(len(alphabet)))
    decoded_word_bytes = bits // math.gcd(8, bits)
    encoded_word_bytes = decoded_word_bytes * 8 // bits
    encode_mask = 2 ** bits - 1
    encoded = bytearray()
    cache = 0
    shift = 0
    for char in data:
        cache = cache << 8 | char
        shift += 8
        for shift in range(shift - bits, -1, -bits):
            value = (cache >> shift) & encode_mask
            cache ^= value << shift
            encoded.append(alphabet[value])
    if shift > 0:
        value = cache << (bits - shift)
        encoded.append(alphabet[value])
    if padding:
        remaining = -len(encoded) % encoded_word_bytes
        encoded.extend(PADCHAR * remaining)
    return encoded


def base_decode(data: bytes, alphabet=BASE64_ALPHABET, /, padding=True):
    """
    RFC4648 base64, base32, and base16 decoding algorithm.

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes`: data to decode
    - `alphabet: bytes? = BASE64_ALPHABET`: base16, base32 or base64 alphabet
    - `padding: bool? = True`: require padded data
    """
    decoder = [None] * 256
    for i, char in enumerate(alphabet):
        decoder[char] = i
    bits = math.ceil(math.log2(len(alphabet)))
    encoded_word_bytes = 8 // math.gcd(8, bits)
    decoded_word_bytes = encoded_word_bytes * bits // 8
    decode_mask = 2 ** 8 - 1
    decoded = bytearray()
    cache = 0
    shift = 0
    if padding and len(data) % encoded_word_bytes != 0:
        raise Exception('data must be padded')
    pad_size = 0
    for pad_size, char in enumerate(memoryview(data)[::-1]):
        if char != PADCHAR_ASCII:
            break
    for char in memoryview(data)[:-pad_size if pad_size > 0 else None]:
        cache = (cache << bits) | decoder[char]
        shift += bits
        for shift in range(shift - 8, -1, -8):
            value = (cache >> shift) & decode_mask
            cache ^= value << shift
            decoded.append(value)
    return decoded


# ascii85 and base85 alphabets
ASCII85_ALPHABET = bytes(i for i in range(33, 118))
BASE85_ALPHABET = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'


def _x85_encode(data: bytes, encoded: bytearray, alphabet: bytes, padding=False, fold_null: bytes = None, fold_space: bytes = None):
    """
    Helper encoder for both ascii85 and base85 algorithms.

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes`: data to encode
    - `encoded: bytearray`: buffer to write encoded data
    - `alphabet: bytes`: ascii85 or base85 alphabet
    - `padding: bool? = False`: add null padding to `data` (works differently from base64 or base32)
    - `fold_null: bytes? = None`: fold four null bytes into `fold_null` byte, `fold_null` must not be in `alphabet`
    - `fold_space: bytes? = None`: fold four space bytes into `fold_space`, `fold_space` must not be in `alphabet`
    """
    padding_size = (-len(data)) % 4
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


def ascii85_encode(data: bytes, /, padding=False, fold_space=False, adobe=False):
    """
    Ascii85 encoding algorithm.
    This algorithm always folds four null bytes, `fold_space` is optionally available.
    `fold_space` is not compatible with standard `adobe` ascii85 decoders, but is encodeable by this implementation.
    This implementation does not support line wrapping.

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes`: data to encode
    - `padding: bool? = False`: add null padding to `data` (works differently from base64 or base32)
    - `fold_space: bool? = False`: fold four spaces into a single `b'y'` character
    - `adobe: bool? = False`: Add adobe prefix `b'<~'` and suffix `b'~>'` to the encoded data
    """
    encoded = bytearray()
    if adobe:
        encoded.extend(b'<~')
    result = _x85_encode(data, encoded, ASCII85_ALPHABET, padding, b'z', b'y' if fold_space else None)
    if adobe:
        encoded.extend(b'~>')
    return result


def base85_encode(data: bytes, /, padding=False):
    """
    Base85 encoding algorithm.
    This algorithm is based on the git binary diffs.
    This algorithm never folds null bytes of space bytes.

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes`: data to encode
    - `padding: bool? = False`: add null padding to `data` (works differently from base64 or base32)
    """
    return _x85_encode(data, bytearray(), BASE85_ALPHABET, padding)


def test():
    import base64
    import random
    from ..test import benchmark

    def random_bytes(size: int, alphabet_size: int):
        return bytes(random.randint(0, alphabet_size - 1) for i in range(size))

    def test_base(data: bytes, alphabet: bytes):
        encoded = base_encode(data, alphabet)
        decoded = base_decode(encoded, alphabet)
        return decoded, encoded

    def test_native(data: bytes, encode, decode):
        encoded = encode(data)
        decoded = decode(encoded)
        return decoded, encoded

    benchmark(
        [
            ('        base16', lambda data: test_base(data, BASE16_ALPHABET)),
            ('        base32', lambda data: test_base(data, BASE32_ALPHABET)),
            (' base32 exthex', lambda data: test_base(data, BASE32_EXTHEX_ALPHABET)),
            ('        base64', lambda data: test_base(data, BASE64_ALPHABET)),
            ('       ascii85', lambda data: ascii85_encode(data)),
            ('        base85', lambda data: base85_encode(data)),
            ('base64 urlsafe', lambda data: test_base(data, BASE64_URLSAFE_ALPHABET)),
            (' native base16', lambda data: test_native(data, base64.b16encode, base64.b16decode)),
            (' native base32', lambda data: test_native(data, base64.b32encode, base64.b32decode)),
            (' native base64', lambda data: test_native(data, base64.b64encode, base64.b64decode)),
            (' native base85', lambda data: test_native(data, base64.b85encode, base64.b85decode)),
            ('native ascii85', lambda data: test_native(data, base64.a85encode, base64.a85decode)),
        ],
        test_inputs=(b'Man', b'hello world!', b'Pedro'),
        bench_sizes=(100, 1000, 10000, 100000),
        bench_input=lambda s: random_bytes(s, 256)
    )


if __name__ == '__main__':
    test()
