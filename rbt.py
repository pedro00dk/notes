from queue import Queue


class RBT:
    def __init__(self):
        self.root = None
        self.size = 0

    def __str__(self):
        lines = []
        self.pre_order(
            lambda key, value, depth, red: lines.append(f'{f"|  " * depth}├─ {"R" if red else "B"} # {key}: {value}')
        )
        tree = '\n'.join(lines)
        return f'RBT [\n{tree}\n]'

    def put(self, key, value=None):
        parent = None
        node = self.root
        while node is not None and key != node.key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            if parent is None:
                node = self.root = Node(key, value)
            elif key < parent.key:
                node = parent.left = Node(key, value)
                parent.left.parent = parent
            else:
                node = parent.right = Node(key, value)
                parent.right.parent = parent
            self.size += 1
            self.root = self._put_fix(node)
        else:
            node.key, node.value = key, value

    def _put_fix(self, created):
        node = created
        while self._red(parent:= self._parent(node)):
            uncle = self._uncle(node)
            grand_parent = self._grand_parent(node)
            if self._red(uncle):
                parent.red = uncle.red = False
                grand_parent.red = True
                node = grand_parent
                continue
            if node == parent.right:
                if parent == grand_parent.left:
                    parent = self._rotate_left(parent)
                    node = parent.left
                grand_parent = self._rotate_left(grand_parent)
            elif node == parent.left:
                if parent == grand_parent.right:
                    parent = self._rotate_right(parent)
                    node = parent.right
                grand_parent = self._rotate_right(grand_parent)
            grand_parent.red = False
            grand_parent.left.red = grand_parent.right.red = True
            break
        root = self._root(node)
        root.red = False
        return root

    def delete(self, key):
        node = self.root
        while node is not None and key != node.key:
            node = node.left if key < node.key else node.right
        if node is None:
            raise KeyError('not found')
        if node.left is not None and node.right is not None:
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node = successor
        if node.parent is None:
            child = self.root = None
        elif node.parent.left == node:
            child = node.parent.left = node.left if node.left is not None else node.right
            if child is not None:
                child.parent = node.parent
        elif node.parent.right == node:
            child = node.parent.right = node.left if node.left is not None else node.right
            if child is not None:
                child.parent = node.parent
        self.size -= 1
        self.root = self._delete_fix(node, child)

    def _delete_fix(self, deleted, replacer):
        if self._red(deleted):
            return self.root
        if self._red(replacer):
            replacer.red = False
            return self.root
        node = replacer
        while (parent:= self._parent(node)) is not None:
            sibling = self._sibling(node)
            if self._red(sibling):
                sibling.red = False
                parent.red = True
                if node == node.parent.left:
                    self._rotate_left(parent)
                    sibling = parent.right
                else:
                    self._rotate_right(parent)
                    sibling = parent.left
            if self._blk(parent) and self._blk(sibling) and sibling is not None and \
                    self._blk(sibling.left) and self._blk(sibling.right):
                sibling.red = True
                node = parent
                continue
            if self._red(parent) and self._blk(sibling) and sibling is not None and \
                    self._blk(sibling.left) and self._blk(sibling.right):
                sibling.red = True
                parent.red = False
                break
            if self._blk(sibling) and sibling is not None:
                if node == parent.left and self._red(sibling.left) and self._blk(sibling.right):
                    sibling.red = True
                    sibling.left.red = False
                    sibling = self._rotate_right(sibling)
                elif node == parent.right and self._blk(sibling.left) and self._left(sibling.right):
                    sibling.red = True
                    sibling.right.red = False
                    sibling = self._rotate_left(sibling)
            sibling.red = parent.red
            parent.red = False
            if node == parent.left:
                sibling.right.red = False
                self._rotate_left(parent)
            else:
                sibling.left.red = False
                self._rotate_right(parent)
            break
        return self._root(node if node is not None else deleted)

    def _red(self, node):
        return node is not None and node.red
    
    def _blk(self, node):
        return node is None or not node.red

    def _left(self, node):
        return node.left if node is not None else None

    def _right(self, node):
        return node.right if node is not None else None

    def _parent(self, node):
        return node.parent if node is not None else None

    def _grand_parent(self, node):
        return self._parent(self._parent(node))

    def _sibling(self, node):
        parent = self._parent(node)
        return None if node is None or parent is None else parent.left if node == parent.right else parent.right

    def _uncle(self, node):
        return self._sibling(self._parent(node))

    def _root(self, node):
        while (parent:= self._parent(node)) is not None:
            node = parent
        return node

    def _rotate_left(self, node):
        child = node.right
        node.right = child.left
        if node.right is not None:
            node.right.parent = node
        child.left = node
        child.parent = node.parent
        node.parent = child
        if child.parent is not None:
            if child.parent.left == node:
                child.parent.left = child
            else:
                child.parent.right = child
        return child

    def _rotate_right(self, node):
        child = node.left
        node.left = child.right
        if node.left is not None:
            node.left.parent = node
        child.right = node
        child.parent = node.parent
        node.parent = child
        if child.parent is not None:
            if child.parent.left == node:
                child.parent.left = child
            else:
                child.parent.right = child
        return child

    def get(self, key):
        node = self.root
        while node is not None and node.key != key:
            node = node.left if node.key > key else node.right
        if node is None:
            raise KeyError()
        return node.value

    def pre_order(self, callback, node=True, depth=0):
        if node is True:
            return self.pre_order(callback, self.root)
        if node is None:
            return
        callback(node.key, node.value, depth, node.red)
        self.pre_order(callback, node.left, depth + 1)
        self.pre_order(callback, node.right, depth + 1)

    def in_order(self, callback, node=True, depth=0):
        if node is True:
            return self.in_order(callback, self.root)
        if node is None:
            return
        self.in_order(callback, node.left, depth + 1)
        callback(node.key, node.value, depth, node.red)
        self.in_order(callback, node.right, depth + 1)

    def post_order(self, callback, node=True, depth=0):
        if node is True:
            return self.post_order(callback, self.root)
        if node is None:
            return
        self.post_order(callback, node.left, depth + 1)
        self.post_order(callback, node.right, depth + 1)
        callback(node.key, node.value, depth, node.red)

    def breadth_order(self, callback):
        q = Queue()
        q.offer((self.root, 0))
        while q.size > 0:
            node, depth = q.pool()
            callback(node.key, node.value, depth, node.red)
            if node.left is not None:
                q.offer((node.left, depth + 1))
            if node.right is not None:
                q.offer((node.right, depth + 1))


class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.red = True
        self.parent = None
        self.left = None
        self.right = None


def test():
    t = RBT()
    t.put(-15, -1000)
    t.put(-10)
    t.put(-5)
    t.put(0)
    t.put(5, 1000)
    t.put(10)
    t.put(15)
    print(t.get(5))
    print(t.get(-15))
    print(t)
    t.delete(5)
    print(t)
    t.delete(-10)
    print(t)
    t.delete(0)
    print(t)
    t.pre_order(lambda key, value, depth, red: print(key, end=' '))
    print()
    t.in_order(lambda key, value, depth, red: print(key, end=' '))
    print()
    t.post_order(lambda key, value, depth, red: print(key, end=' '))
    print()
    t.breadth_order(lambda key, value, depth, red: print(key, end=' '))
    print()


if __name__ == '__main__':
    test()
