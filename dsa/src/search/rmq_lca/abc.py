from __future__ import annotations

import abc
import collections
import dataclasses
from typing import Any, Callable, Generic, Iterator, Protocol, TypeVar, cast


class Comparable(Protocol):
    def __lt__(self, _other: Any) -> bool: ...
    def __le__(self, _other: Any) -> bool: ...
    def __gt__(self, _other: Any) -> bool: ...
    def __ge__(self, _other: Any) -> bool: ...


T = TypeVar('T', bound=Comparable)
U = TypeVar('U')
N = TypeVar('N')


class RangeMinimumQuery(Generic[T], abc.ABC):
    """
    Interface for range minimum query implementations.
    Implementations do not need to convert rmq problems to rmq plus-minus-1 problems, but they have to specify if only
    rmq plus-minus-1 is supported through the `is_plus_minus_1` function.
    """

    @ abc.abstractmethod
    def __init__(self, data: list[T]):
        """
        Initialize and the rmq internal data structure based on `data` content.

        > complexity
        - see implementations

        > parameters
        - `data`: list to be indexed for range minimum queries
        """

    @ abc.abstractmethod
    def rmq(self, i: int, j: int) -> int:
        """
        Compute the minimum index and value of the data `i:j` interval (inclusive)

        > complexity
        - see implementations

        > parameters
        - `i`: index in `data` (provided in `__init__` call)
        - `j`: index in `data` (provided in `__init__` call)
        - `return`: tuple containing index of minimum value and the minimum value itself
        """

    @ abc.abstractmethod
    def size(self) -> int:
        """
        Return the size of `data` used to create the rmq data structure.

        > parameters
        - `return`: size of `data`
        """

    @ abc.abstractclassmethod
    def is_plus_minus_1(cls) -> bool:
        """
        Indicates if the implementation supports only the plus-minus-1 version of the range minimum query problem.

        > complexity
        - see implementations

        > parameters
        - `return`: if only supports rmq plus-minus-1
        """


# The CartesianTree class, rmq_to_lca and lca_to_rmq functions provide equivalence between the range minimum query and
# lowest common ancestor problems, they can be used to transform transform the following problems:
# - range minimum query -> lowest common ancestor
# - lowest common ancestor -> range minimum query
# - lowest common ancestor -> range minimum query plus-minus-1
# - range minimum query -> lowest common ancestor -> range minimum query plus-minus-1
# - range minimum query -> lowest common ancestor -> universe reduction of range minimum query


@dataclasses.dataclass
class CartesianTree:
    index: int
    parent: CartesianTree = cast(Any, None)
    left: CartesianTree = cast(Any, None)
    right: CartesianTree = cast(Any, None)


def rmq_to_lca(
    array: list[T],
) -> tuple[
        list[T],
        list[CartesianTree],
        CartesianTree,
        Callable[[CartesianTree], CartesianTree],
        Callable[[CartesianTree], Iterator[CartesianTree]],
]:
    """
    Transform `array` in a binary cartesian tree where lowest common ancestor calls can be executed.
    The cartesian tree nodes store only the index of each element of `array`.

    > complexity
    - time: `O(n)`
    - space: `O(n)`
    - `n`: length of `array`

    > parameters
    - `array`: array with comparable elements to be transformed in a cartesian tree
    - `return`: a tuple containing:
        - `array` itself
        - a mapper list where each index contains a node of the cartesian tree equivalent to the same index in `array`
        - the root of the cartesian tree
        - a function that given a cartesian tree node, returns its parent
        - a function that given a cartesian tree node, returns an iterator to its children, the iterator may produce
            `None` elements if the left or right subtrees do not exist
    """
    if len(array) < 1:
        raise Exception('data must contain at least one element')
    root = CartesianTree(0)
    mapper: list[CartesianTree] = [root]
    cursor = root
    for i in range(1, len(array)):
        node = CartesianTree(i)
        mapper.append(node)
        while array[node.index] < array[cursor.index] and cursor.parent is not None:
            cursor = cursor.parent
        if array[node.index] < array[cursor.index]:
            node.left = cursor
            cursor.parent = node
            root = cursor = node
        else:
            node.left = cursor.right
            if node.left is not None:
                node.left.parent = node
            cursor.right = node
            node.parent = cursor
            cursor = node
    get_parent: Callable[[CartesianTree], CartesianTree] = lambda node: node.parent
    get_children: Callable[[CartesianTree], Iterator[CartesianTree]] = lambda node: iter((node.left, node.right))
    return array, mapper, root, get_parent, get_children


def lca_to_rmq(
    root: N,
    node_id: Callable[[N], int],
    node_children: Callable[[N], Iterator[N]],
    node_data: Callable[[N], U] = lambda node: node,
    is_binary: bool = False,
    plus_minus_1: bool = True,
) -> tuple[list[int], list[U], dict[int, list[int]]]:
    """
    Transform a tree represented by `root` into an array where rmq algorithms can execute queries.

    > complexity
    - time: `O(n)`
    - space: `O(n)`
    - `n`: number of nodes in the tree represented by `root`

    > parameters
    - `root`: root of the tree
    - `node_id`: a function that takes a node and maps it into a unique id, used to build a mapper, which helps to
        identify which indices of the resulting array are equivalent to each node
    - `node_children`: a function that provides an iterator for the node children, if the tree is binary and the left or
        right nodes are not present, `None` must still be yielded, non binary trees only need to yield existing values
    - `node_data`: a function that maps a node into another data, by default the node itself is used, but mapping is
        useful when transforming rmq into rmq plus-minus-1 problems
    - `is_binary`: indicates the tree is binary
    - `plus_minus_1`: if `True` a rmq plus minus 1 array is generated, otherwise, a standard rmq array is generated,
        standard rmq array can only be created from binary trees
    - `return`: a tuple containing:
        - the rmq array, which is a list of integers representing the depth of each node in the tree
        - the backward mapper, which is a list of mapped values obtained from `node_data`, the result in rmq array can
            be used to index this array
        - the forward mapper, a dictionary where each key is a node id and the value is a list of indices of the rmq
            array that represent that node
    """
    if not is_binary and not plus_minus_1:
        raise Exception('lca in non binary trees can only be converted to rmq plus-minus-1 problems')
    rmq: list[int] = []
    backward_mapper: list[U] = []
    forward_mapper: dict[int, list[int]] = collections.defaultdict(lambda: [])

    # in_order traversal used for default rmq
    def in_order(node: N, depth: int):
        left, right = node_children(node)
        if left is not None:
            in_order(left, depth + 1)
        rmq.append(depth)
        backward_mapper.append(node_data(node))
        forward_mapper[node_id(node)].append(len(rmq) - 1)
        if right is not None:
            in_order(right, depth + 1)

    # pre_order traversal with revisit used for rmq plus-minus-1
    def pre_order(node: N, depth: int):
        id = node_id(node)
        data = node_data(node)
        rmq.append(depth)
        backward_mapper.append(data)
        forward_mapper[id].append(len(rmq) - 1)
        for child in node_children(node):
            if child is None:
                continue
            pre_order(child, depth + 1)
            rmq.append(depth)
            backward_mapper.append(data)
            forward_mapper[id].append(len(rmq) - 1)

    traverse_function = in_order if is_binary and not plus_minus_1 else pre_order
    traverse_function(root, 0)
    return rmq, backward_mapper, forward_mapper
