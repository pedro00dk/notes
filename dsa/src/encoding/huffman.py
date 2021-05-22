from __future__ import annotations

import collections
import dataclasses
import heapq
from typing import Any, cast

# huffman code stores each byte (character) mapping to its compressed version
# the compressed version is represented by the number of bits (size) and the actual value (value)
# huffman code is used in the encoding process and can be easily canonized, serialized and deserialized
HuffmanCode = dict[int, tuple[int, int]]  # {[byte]: (size, value)}


@dataclasses.dataclass(order=True)
# huffman tree stores paths to bytes where left banches represents a 0 bit and right branches represents a 1 bit
# huffman tree is easier to be created from initial data than huffman code
# huffman tree is used in the decoding process, for all other purposes, it is converted to a huffman code
class HuffmanTree:
    frequency: int
    byte: int
    left: HuffmanTree = cast(Any, None)
    right: HuffmanTree = cast(Any, None)


def huffman_tree(data: bytes) -> HuffmanTree:
    """
    Build a huffman coding tree from `data`.

    > complexity
    - time: `O(n)`
    - space: `O(n)`
    - `n`: length of `data`

    > parameters
    - `data`: data to generate the huffman coding tree
    - `return`: a huffman tree
    """
    frequencies = collections.Counter(data)
    heap = [HuffmanTree(frequency, byte) for byte, frequency in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        right = heapq.heappop(heap)
        left = heapq.heappop(heap)
        heapq.heappush(heap, HuffmanTree(left.frequency + right.frequency, -1, left, right))
    return heap[0]


def huffman_tree_to_code(tree: HuffmanTree) -> HuffmanCode:
    """
    Build the huffman code table based on the huffman tree.

    > parameters
    - `tree`: the huffman tree
    - `return`: a huffman code
    """

    def build_code(node: HuffmanTree, size: int, value: int, code: HuffmanCode) -> HuffmanCode:
        if node.byte != -1:
            code[node.byte] = size, value
            return code
        build_code(node.left, size + 1, value << 1, code)
        build_code(node.right, size + 1, (value << 1) + 1, code)
        return code

    return build_code(tree, 0, 0, {})


def huffman_code_to_tree(code: HuffmanCode) -> HuffmanTree:
    """
    Build the huffman tree based on the huffman code table.
    Note that the resulting tree structure is made of lists rather than tuples.

    > parameters
    > `code`: the huffman code
    - `return`: a huffman tree
    """
    tree = HuffmanTree(-1, -1)
    for byte, (size, value) in code.items():
        cursor = tree
        for i in range(size - 1, -1, -1):
            bit = value >> i & 1
            if bit == 0:
                cursor.left = cursor.left if cursor.left is not None else HuffmanTree(0, -1)
                cursor = cursor.left
            else:
                cursor.right = cursor.right if cursor.right is not None else HuffmanTree(0, -1)
                cursor = cursor.right
        cursor.byte = byte
    return tree


def canonized_huffman_code(code: HuffmanCode) -> HuffmanCode:
    """
    Create a canonized version of `code`.
    The tree itself cannot be easily canonized, but the code table can.

    > parameters
    - `code`: the huffman code
    - `return`: a canonized huffman code
    """
    sizes = [(size, byte) for byte, (size, _) in code.items() if byte != -1]
    sizes.sort()
    current_value = 0
    current_size = sizes[0][0]
    canonized_code: HuffmanCode = {}
    for size, byte in sizes:
        current_value <<= size - current_size
        current_size = size
        canonized_code[byte] = current_size, current_value
        current_value += 1
    return canonized_code


def serialize_huffman_code(code: HuffmanCode) -> bytearray:
    """
    Serialize `code` into a bytearray.
    `code` must be canonical, otherwise the deserialization process will fail.
    Two serialization strategies may be used depending on the alphabet length.
    If there is less than 128 bytes in the alphabet, each byte is encoded together with its size.
    If there is 128 or more bytes, all 256 bytes are encoded, but only their sizes.

    > parameters
    - `code`: the huffman code, it must be canonical
    - `return`: serialized code
    """
    serialized = bytearray()
    length = len(code)
    serialized.append(length - 1)  # -1 to map 1-256 alphabet size into 0-255
    if length < 128:
        for byte, (size, _) in code.items():
            serialized.append(byte)
            serialized.append(size)
    else:
        for byte in range(256):
            size = code.get(byte, (0, 0))[0]
            serialized.append(size)
    return serialized


def deserialize_huffman_code(serialized: bytes) -> HuffmanCode:
    """
    Deserialize `serialized` into a canonical huffman code.
    Two deserialization strategies may be used depending on the alphabet length, see serialize function.

    > parameters
    - `serialized`: serialized code
    - `return`: a canonical huffman code
    """
    length = serialized[0] + 1  # +1 to map 0-255 to 1-256 alphabet size
    serialized = memoryview(serialized)[1:]
    partial_code: HuffmanCode = (
        {serialized[i * 2]: (serialized[i * 2 + 1], 0) for i in range(length)}
        if length < 128
        else {i: (serialized[i], 0) for i in range(256) if serialized[i] != 0}
    )
    return canonized_huffman_code(partial_code)


def huffman_encode(data: bytes) -> bytearray:
    """
    Encode `data` using huffman code.

    > complexity
    - time: `O(n)`
    - space: `O(n)`
    - `n`: length of `data`

    > parameters
    - `data`: data to be encoded
    - `return`: encoded data
    """
    if len(data) == 0:
        return bytearray()
    code = canonized_huffman_code(huffman_tree_to_code(huffman_tree(data)))
    encoded = serialize_huffman_code(code)
    encoded.extend(len(data).to_bytes(4, "little"))
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


def huffman_decode(encoded: bytes) -> bytearray:
    """
    Decode `encoded` using huffman code.

    > complexity
    - time: `O(n)`
    - space: `O(n)`
    - `n`: length of `encoded`

    > parameters
    - `encoded`: data to be decoded
    - `return`: decoded data
    """
    if len(encoded) == 0:
        return bytearray()
    code = deserialize_huffman_code(encoded)
    tree = huffman_code_to_tree(code)
    encoded = memoryview(encoded)[len(code) * 2 + 1 if len(code) < 128 else 257 :]  # skipping serialized code part
    length = int.from_bytes(encoded[:4], "little")
    decoded = bytearray()
    cursor = tree
    for byte in encoded[4:]:
        for i in range(7, -1, -1):
            bit = (byte >> i) & 1
            cursor = cursor.left if bit == 0 else cursor.right
            if cursor.byte != -1:
                decoded.append(cursor.byte)
                cursor = tree
    if len(decoded) < length:
        decoded.extend([[*code.keys()][0]] * (length - len(decoded)))
    if len(decoded) > length:
        decoded[length:] = b""
    return decoded


def test():
    from ..test import verify

    def test_huffman(data: bytes):
        encoded = huffman_encode(data)
        decoded = huffman_decode(encoded)
        return decoded, encoded

    verify(
        (
            (test_huffman, (b"man",)),
            (test_huffman, (b"hello world!",)),
            (test_huffman, (b"pedro",)),
        )
    )


if __name__ == "__main__":
    test()
