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
