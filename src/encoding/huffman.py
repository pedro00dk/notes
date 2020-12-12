import collections
import heapq


def huffman_tree(data: bytes):
    """
    Build a huffman coding tree from `data`.

    > complexity:
    - time: `O(n*log(n))`
    - space: `O(n*log(n))`

    > parameters:
    - `data: bytes`: data to generate the huffman coding tree

    > `return: T = (frequency: int, byte: int, left: T, right: T)`: a tree structure made of tuples
    """
    frequencies = collections.Counter(data)
    heap = [(frequency, byte, None, None) for byte, frequency in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        right = heapq.heappop(heap)
        left = heapq.heappop(heap)
        heapq.heappush(heap, (left[0] + right[0], -1, left, right))
    return heap[0]


def huffman_tree_to_code(tree: tuple):
    """
    Build the huffman code table based on the huffman tree.

    > parameters:
    - `tree: T = (frequency: int, byte: int, left: T, right: T)`: a tree structure made of tuples

    > `return: {[byte: int]: (size: int, value: int)}`: the huffman code
    """
    def build_code(node: tuple, size: int, value: int, code: dict):
        frequency, byte, left, right = node
        if byte != -1:
            code[byte] = size, value
            return code
        build_code(left, size + 1, value << 1, code)
        build_code(right, size + 1, (value << 1) + 1, code)
        return code

    return build_code(tree, 0, 0, {})


def huffman_code_to_tree(code: dict):
    """
    Build the huffman tree based on the huffman code table.
    Note that the resulting tree structure is made of lists rather than tuples.

    > parameters:
    > `code: {[byte: int]: (size: int, value: int)}`: the huffman code

    > `return: T = [frequency: int, byte: int, left: T, right: T]`: a tree structure made of lists
    """
    tree = [-1, -1, None, None]
    for byte, (size, value) in code.items():
        cursor = tree
        for i in range(size - 1, -1, -1):
            bit = value >> i & 1
            side = -2 if bit == 0 else -1  # left (-2) or right (-1) index on cursor
            cursor[side] = cursor[side] if cursor[side] is not None else [0, -1, None, None]
            cursor = cursor[side]
        cursor[1] = byte
    return tree


def canonized_huffman_code(code: dict):
    """
    Create a canonized version of `code`.
    The tree itself cannot be easily canonized, but the code table can.

    > parameters:
    - `code: {[byte: int]: (size: int, value: int)}`: the huffman code

    > `return: {[byte: int]: (size: int, value: int)}`: a canonized huffman code
    """
    sizes = [(size, byte) for byte, (size, value) in code.items() if byte != -1]
    sizes.sort()
    values = []
    current_value = 0
    current_size = sizes[0][0]
    canonized_code = {}
    for size, byte in sizes:
        current_value <<= size - current_size
        current_size = size
        canonized_code[byte] = current_size, current_value
        current_value += 1
    return canonized_code


def serialize_huffman_code(code: dict):
    """
    Serialize `code` into a bytearray.
    `code` must be canonical, otherwise the deserialization process will fail.
    Two serialization strategies may be used depending on the alphabet length.
    If there is less than 128 bytes in the alphabet, each byte is encoded together with its size.
    If there is 128 or more bytes, all 256 bytes are encoded, but only their sizes.

    > parameters:
    - `code: {[byte: int]: (size: int, value: int)}`: the huffman code, it must be canonical

    > `return: bytearray`: serialized code
    """
    serialized = bytearray()
    length = len(code)
    serialized.append(length - 1)  # -1 to fit a size 256 alphabet into 0-255
    if length < 128:
        for byte, (size, value) in code.items():
            serialized.append(byte)
            serialized.append(size)
    else:
        for byte in range(256):
            size = code.get(byte, (0, 0))[0]
            serialized.append(size)
    return serialized


def deserialize_huffman_code(serialized: bytes):
    """
    Deserialize `serialized` into a canonical huffman code.
    Two deserialization strategies may be used depending on the alphabet length, see serialize function.

    > parameters:
    - `serialized: bytearray`: serialized code

    > `return: {[byte: int]: (size: int, value: int)}`: a canonical huffman code
    """
    length = serialized[0] + 1  # -1 to fit a size 256 alphabet into 0-255
    serialized = memoryview(serialized)[1:]
    if length < 128:
        partial_code = {serialized[i * 2]: (serialized[i * 2 + 1], None) for i in range(length)}
    else:
        partial_code = {i: (serialized[i], None) for i in range(256) if serialized[i] != 0}
    return canonized_huffman_code(partial_code)


def huffman_encode(data: bytes):
    """
    Encode `data` using huffman code.

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `data: bytes`: data to be encoded

    > `return: bytes`: encoded data
    """
    if len(data) == 0:
        return data
    code = canonized_huffman_code(huffman_tree_to_code(huffman_tree(data)))
    encoded = serialize_huffman_code(code)
    encoded.extend(len(data).to_bytes(4, 'little'))
    cache = 0
    shift = 0
    for byte in data:
        size, value = code[byte]
        cache = (cache << size) | value
        shift += size
        if shift >= 8:
            shift -= 8
            value = cache >> shift
            cache ^= value << shift
            encoded.append(value)
    if shift > 0:
        remaining = 8 - shift
        encoded.append(cache << remaining)
    return encoded


def huffman_decode(encoded: bytes):
    """
    Decode `encoded` using huffman code.

    > complexity:
    - time: `O(n)`
    - space: `O(n)`

    > parameters:
    - `encoded: bytes`: data to be decoded

    > `return: bytes`: decoded data
    """
    if len(data) == 0:
        return data
    code = deserialize_huffman_code(encoded)
    tree = huffman_code_to_tree(code)
    encoded = memoryview(encoded)[len(code) * 2 + 1 if len(code) < 128 else 257:]  # skipping serialized code part
    length = int.from_bytes(encoded[:4], 'little')
    decoded = bytearray()
    cursor = tree
    for byte in encoded[4:]:
        for i in range(7, -1, -1):
            bit = (byte >> i) & 1
            side = -2 if bit == 0 else -1  # left (-2) or right (-1) index on cursor
            cursor = cursor[side]
            if cursor[1] != -1:
                decoded.append(cursor[1])
                cursor = tree
    if len(decoded) < length:
        decoded.extend([[*code.keys()][0]] * (length - len(decoded)))
    if len(decoded) > length:
        decoded[length:] = b''
    return decoded


def test():
    from ..test import match

    def test_huffman(data: bytes):
        encoded = huffman_encode(data)
        decoded = huffman_decode(encoded)
        return decoded, encoded

    match([
        (test_huffman, (b'man',)),
        (test_huffman, (b'hello world!',)),
        (test_huffman, (b'pedro',)),
    ])


if __name__ == '__main__':
    test()
