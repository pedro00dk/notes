from .abc import Node, Tree


class AVLNode(Node):
    """
    Node with extra `balance` property.
    """

    def __init__(self, key, /, value=None):
        super().__init__(key, value)
        self.balance = 0


class AVL(Tree):
    """
    AVL tree implementation (with ranks).
    """

    def __init__(self, /, rank=2):
        """
        > parameters:
        - `rank: int? = 2`: tree rank, must be > 1. If 2, the behavior is the same as an default AVL tree
        """
        super().__init__(lambda node, depth: f'b:{node.balance} # {node.key}: {node.value}')
        self._rank = rank

    def put(self, key, /, value=None):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(log(n))`
        - space: `O(log(n))`
        """
        def rec(key, value, node: AVLNode):
            if node is None:
                node, growth, old_value = AVLNode(key, value), 1, None
                self._size += 1
            elif key < node.key:
                node.left, child_growth, old_value = rec(key, value, node.left)
                previous_balance = node.balance
                node.balance -= child_growth
                growth = max(0, abs(node.balance) - abs(previous_balance))
            elif key > node.key:
                node.right, child_growth, old_value = rec(key, value, node.right)
                previous_balance = node.balance
                node.balance += child_growth
                growth = max(0, abs(node.balance) - abs(previous_balance))
            else:
                node.key, node.value, growth, old_value = key, value, 0, node.value
            return (*self._rotate(node, growth), old_value)

        self._root, growth, old_value = rec(key, value, self._root)
        return old_value

    def take(self, key):
        """
        Check abstract class for documentation.

        > complexity:
        - time: `O(log(n))`
        - space: `O(log(n))`
        """
        def rec(key, node: AVLNode):
            if node is None:
                raise KeyError(f'key ({str(key)}) not found')
            elif key < node.key:
                node.left, child_growth, value = rec(key, node.left)
                previous_balance = node.balance
                node.balance -= child_growth
                growth = -min(0, abs(node.balance) - abs(previous_balance))
            elif key > node.key:
                node.right, child_growth, value = rec(key, node.right)
                previous_balance = node.balance
                node.balance += child_growth
                growth = -min(0, abs(node.balance) - abs(previous_balance))
            elif node.left is not None and node.right is not None:
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                successor_key, dummy_key = successor.key, node.left.key
                node.key, successor.key = dummy_key, node.key
                node.value, successor.value = successor.value, node.value
                current_node = node
                node, growth, value = rec(key, node)
                current_node.key = successor_key
            else:
                node, growth, value = node.left if node.right is None else node.right, -1, node.value
                self._size -= 1
            return (*self._rotate(node, growth), value)

        self._root, growth, value = rec(key, self._root)
        return value

    def _rotate(self, node: Node, growth: int):
        """
        Check if `node` needs rotation.

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `node: Node`: node to check for rotations
        - `growth: int`: current tree growth

        > `return: (Node, int)`: the top node and tree growth after `Node` rotation
        """
        if node is not None and node.balance <= -self._rank:
            if node.left.balance > 0:
                node, rotation_growth = self._rotate_left(node.left)
                growth += rotation_growth
            node, rotation_growth = self._rotate_right(node)
            growth += rotation_growth
        elif node is not None and node.balance >= self._rank:
            if node.right.balance < 0:
                node, rotation_growth = self._rotate_right(node.right)
                growth += rotation_growth
            node, rotation_growth = self._rotate_left(node)
            growth += rotation_growth
        return node, growth

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

        However, this implementation computes `B(c*)` and `B(n*)` only the balances of the children.
        Calculating `B(a*)` (balance of `a` after rotation):
        - 1: `B(a*) = H(rl) - H(l))`
        - 2: `B(a) = H(b) - H(l)`

        subtracting 2 from 1:
        - 3: `B(a*) - B(a) = H(rl) - H(l) - (H(b) - H(l)) = H(rl) - H(l) - H(b) + H(l)`
        - 4: `B(a*) - B(a) = H(rl) - H(b)`

        expanding `H(b)` from 4:
        - 5: `B(a*) - B(a) = H(rl) - (max(H(rl), H(rr)) + 1) = H(rl) - max(H(rl), H(rr)) - 1`
        - 6: `B(a*) - B(a) = -1 - max(H(rl), H(rr)) + H(rl)`
        - 7: `B(a*) - B(a) = -1 - (max(H(rl), H(rr)) - H(rl))`

        since `max(x, y) - z == max(x-z, y-z)`, from 7:
        - 8: `B(a*) - B(a) = -1 - max(H(rl) - H(rl), H(rr) - H(rl)`
        - 9: `B(a*) - B(a) = -1 - max(0, H(rr) - H(rl)`

        since `H(rr) - H(rl) == B(b)`, from 9:
        - 10: `B(a*) - B(a) = -1 - max(0, B(b)`

        adding `B(a)` in both sides in 10:
        - 11: `B(a*) = B(a) - 1 - max(B(b), 0)` <<<< `B(a*)` in terms of previous balances only

        Calculating `B(b*)` (balance of `b` after rotation):
        - 12: `B(b*) = H(rr) - H(a*)`
        - 13: `B(b) = H(rr) - H(rl)`

        subtracting 12 from 13:
        - 14: `B(b*) - B(b) = H(rr) - H(a*) - (H(rr) - H(rl)) = H(rr) - H(a*) - H(rr) + H(rl)`
        - 15: `B(b*) - B(b) = H(rl) - H(a*)`

        expanding `H(a*)` from 15:
        - 16: `B(b*) - B(b) = H(rl) - (max(H(l), H(rl)) + 1) = H(rl) - max(H(l), H(rl)) - 1`
        - 17: `B(b*) - B(b) = -1 - max(H(l), H(rl)) + H(rl)`
        - 18: `B(b*) - B(b) = -1 - (max(H(l), H(rl)) - H(rl))`

        since `max(x, y) - z == max(x-z, y-z)`, from 18:
        - 19: `B(b*) - B(b) = -1 - max(H(l)-H(rl), H(rl)-H(rl))`
        - 20: `B(b*) - B(b) = -1 - max(H(l)-H(rl), 0)`

        since `H(rl) - H(l) == B(a*)` so `H(l) - H(rl) == -B(a*)`, from 20:
        - 21: `B(b*) - B(b) = -1 - max(-B(a*), 0)`

        since `-max(-x, -y) == min(x, y)`, from 21:
        - 22: `B(b*) - B(b) = -1 + min(B(a*), 0)` <<<< `B(b*)` in terms of previous balances and `B(a*)`

        > complexity:
        - time: `O(1)`
        - space: `O(1)`

        > parameters:
        - `node: Node`: node to check for rotations

        > `return: (Node, int)`: the top node and tree growth after `Node` rotation
        """
        child = node.right
        node.right = child.left
        child.left = node
        growth = -1 if node.balance >= 2 else 0 if node.balance == 1 else 1
        node.balance = node.balance - 1 - max(child.balance, 0)
        child.balance = child.balance - 1 + min(node.balance, 0)
        return child, growth

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

        > `return: (Node, int)`: the top node and tree growth after `Node` rotation
        """
        child = node.left
        node.left = child.right
        child.right = node
        growth = -1 if node.balance <= -2 else 0 if node.balance == -1 else 1
        node.balance = node.balance + 1 - min(child.balance, 0)
        child.balance = child.balance + 1 + max(node.balance, 0)
        return child, growth


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
