from .abc import Node, Tree


class AVLNode(Node):
    """
    Node with extra `balance` property.
    """

    def __init__(self, key, /, value=None):
        super().__init__(key, value)
        self.height = 1

    def balance(self):
        return (self.right.height if self.right is not None else 0) - (self.left.height if self.left is not None else 0)


class AVL(Tree):
    """
    AVL tree implementation (with ranks).
    """

    def __init__(self, /, rank=2):
        """
        > parameters:
        - `rank: int? = 2`: tree rank, must be > 1. If 2, the behavior is the same as an default AVL tree
        """
        super().__init__(lambda node, depth: f'b:{node.balance()} # {node.key}: {node.value}')
        self._rank = rank

    def put(self, key, /, value=None):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(log(n))`
        - space: `O(log(n))`
        """
        old_value = [None]

        def rec(key, value, node: AVLNode):
            if node is None:
                node = AVLNode(key, value)
                self._size += 1
                return node
            if key < node.key:
                node.left = rec(key, value, node.left)
                node.height = max(node.height, node.left.height + 1)
            elif key > node.key:
                node.right = rec(key, value, node.right)
                node.height = max(node.height, node.right.height + 1)
            else:
                old_value[0] = node.value
                node.key, node.value = key, value
            balance = node.balance()
            return node if abs(balance) < self._rank else self._rotate(node, balance)

        self._root = rec(key, value, self._root)
        return old_value[0]

    def take(self, key):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(log(n))`
        - space: `O(log(n))`
        """
        value = [None]

        def rec(key, node: AVLNode):
            if node is None:
                raise KeyError(f'key ({key}) not found')
            if key < node.key:
                node.left = rec(key, node.left)
                node.height = max(
                    node.left.height if node.left is not None else 0,
                    node.right.height if node.right is not None else 0
                ) + 1
            elif key > node.key:
                node.right = rec(key, node.right)
                node.height = max(
                    node.left.height if node.left is not None else 0,
                    node.right.height if node.right is not None else 0
                ) + 1
            elif node.left is not None and node.right is not None:
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                successor_key, dummy_key = successor.key, node.left.key
                node.key, successor.key = dummy_key, node.key
                node.value, successor.value = successor.value, node.value
                current_node = node
                node = rec(key, node)
                current_node.key = successor_key
            else:
                value[0] = node.value
                node = node.left if node.right is None else node.right
                self._size -= 1
                return node
            balance = node.balance()
            return node if abs(balance) < self._rank else self._rotate(node, balance)

        self._root = rec(key, self._root)
        return value[0]

    def _rotate(self, node: Node, balance: int):
        """
        Check if `node` needs rotation.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `node: Node`: node to check for rotations
        - `balance: int`: node balance (to prevent recomputation)

        > `return: Node`: rotated subtree root
        """
        if balance <= -self._rank:
            if node.left.balance() > 0:
                node.left = self._rotate_left(node.left)
            node = self._rotate_right(node)
        elif balance >= self._rank:
            if node.right.balance() < 0:
                node.right = self._rotate_right(node.right)
            node = self._rotate_left(node)
        return node

    def _rotate_left(self, node: AVLNode):
        """
        Rotate `node` to the left and recompute balance.

        ```
        # () >> node
        # <> >> subtree
            (a)                     (b*)
           /   \\                  /   \\
          /     \\                /     \\
        <l>     (b)     >>>>    (a*)     <rr>
                / \\            / \\
               /   \\          /   \\
            <rl>   <rr>      <l>   <rl>
        ```

        The resulting balance can be easily recomputed from heights:
        - `H(a*) = max(H(l), H(rl)) + 1`
        - `B(a*) = H(rl) - H(l))`
        - `H(b*) = max(H(a*), H(rr)) + 1`
        - `B(b*) = H(a*) - H(rr))`

        There is a strategy for updating balances in rotations based on previous balances.
        However, it is more complicated to update after `take` operations when the tree shrinks.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `node: Node`: node to check for rotations

        > `return: Node`: rotated subtree root
        """
        child = node.right
        node.right = child.left
        child.left = node
        node.height = max(
            node.left.height if node.left is not None else 0,
            node.right.height if node.right is not None else 0
        ) + 1
        child.height = max(node.height, child.right.height if child.right is not None else 0) + 1
        return child

    def _rotate_right(self, node: AVLNode):
        """
        Rotate `node` to the right and recompute balance.
        ```
        # () >> node
        # <> >> subtree
                (a)              (b*)
               /   \\           /   \\
              /     \\         /     \\
            (b)     <r> >>>> <ll>     (a*)
            / \\                      / \\
           /   \\                    /   \\
        <ll>   <lr>               <lr>   <r>    
        ```

        The balance computation is similar to _rotate_left.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `node: Node`: node to check for rotations

        > `return: Node`: rotated subtree root
        """
        child = node.left
        node.left = child.right
        child.right = node
        node.height = max(
            node.left.height if node.left is not None else 0,
            node.right.height if node.right is not None else 0
        ) + 1
        child.height = max(node.height, child.left.height if child.left is not None else 0) + 1
        return child


def test():
    from ..test import match
    t = AVL()
    print('rank 2 tree')
    match([
        (t.put, [-15, -1000], None),
        (t.put, [-10], None),
        (t.put, [-5], None),
        (t.put, [0], None),
        (t.put, [5, 1000], None),
        (t.put, [10], None),
        (t.put, [15], None),
        (t.get, [5], 1000),
        (t.get, [-15], -1000),
        (print, [t], None),
        (t.take, [0], None),
        (t.take, [-10], None),
        (t.take, [-15], -1000),
        (print, [t], None)
    ])
    t3 = AVL(rank=3)
    print('rank 3 tree')
    match([
        (t3.put, [-15, -1000], None),
        (t3.put, [-10], None),
        (t3.put, [-5], None),
        (t3.put, [0], None),
        (t3.put, [5, 1000], None),
        (t3.put, [10], None),
        (t3.put, [15], None),
        (t3.get, [5], 1000),
        (t3.get, [-15], -1000),
        (print, [t3], None),
        (t3.take, [0], None),
        (t3.take, [-10], None),
        (t3.take, [-15], -1000),
        (print, [t3], None)
    ])
    for key, value, depth in t.traverse('pre'):
        print(key, end=' ')
    print()
    for key, value, depth in t.traverse('in'):
        print(key, end=' ')
    print()
    for key, value, depth in t.traverse('post'):
        print(key, end=' ')
    print()
    for key, value, depth in t.traverse('breadth'):
        print(key, end=' ')
    print()


if __name__ == '__main__':
    test()
