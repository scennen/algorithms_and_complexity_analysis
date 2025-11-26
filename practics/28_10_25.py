class Node:
    def __init__(self, key: int, value: int):
        self.key: int = key
        self.value: int = value
        self.left: Node = None
        self.right: Node = None


class Tree:
    def __init__(self, node: Node):
        self.root: Node = node

    def __init__(self):
        self.root: Node = None

    def _insert(self, node: Node, key: int, value: int) -> None:
        if key < node.key:
            if node.left == None:
                node.left = Node(key, value)
            else:
                self._insert(node.left, key, value)

        elif key >= node.key:
            if node.right == None:
                node.right = Node(key, value)
            else:
                self._insert(node.right, key, value)

    def insert(self, key: int, value: int) -> None:
        if self.root == None:
            self.root = Node(key, value)
        else:
            self._insert(self.root, key, value)

    def _search(self, node: Node, key: int) -> Node:
        if node == None: return None
        if node.key == key: return node
        return self._search(node.left) if key < node.left else self._search(node.right, key)

    def _get_min(self, node: Node) -> Node:
        if node == None: return None
        if node.left == None: return node
        return self._get_min(node.left)

    def _get_max(self, node: Node) -> Node:
        if node == None: return None
        if node.right == None: return node
        return self._get_max(node.right)

    def _delete(self, node: Node, key: int) -> Node:
        if node == None:
            return None
        elif key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None or node.right is None:
                node = node.right if node.left == None else node.left
            else:
                max_in_left = self._get_max(node.left)
                node.key = max_in_left.key
                node.value = max_in_left.value
                node.left = self._delete(node.left, max_in_left.key)

        return node

    def delete(self, key: int) -> Node:
        self._delete(self.root, key)

    def _print_sym_tree(self, node: Node) -> None:
        if node == None: return
        self._print_sym_tree(node.left)
        print(node.value, end=' ')
        self._print_sym_tree(node.right)

    def print_sym_tree(self) -> None:
        self._print_sym_tree(self.root)
        print()

    def print_tree(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root
        if node is not None:
            print(" " * (level * 4) + prefix + str(node.key))
            if node.left is not None or node.right is not None:
                if node.left:
                    self.print_tree(node.left, level + 1, "L--- ")
                if node.right:
                    self.print_tree(node.right, level + 1, "R--- ")


tree: Tree = Tree()
tree.insert(7, 7)
tree.insert(5, 5)
tree.insert(6, 6)
tree.insert(8, 8)
tree.insert(4, 4)
tree.insert(2, 2)
tree.insert(3, 3)
tree.print_sym_tree()
tree.print_tree()

print()
tree.delete(5)
tree.print_sym_tree()
tree.print_tree()

print('\nBad time')
tree: Tree = Tree()
for i in range(1, 11):
    tree.insert(i, i)
    tree.print_tree()
    print()

tree.print_sym_tree()

print()
tree.delete(8)
tree.print_sym_tree()
tree.print_tree()


class BSTNode():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Bst:
    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, value):
        if not node:
            return BSTNode(value)

        if value < node.value:
            node.left = self._insert(node.left, value)

        else:
            node.right = self._insert(node.right, value)

        return node

    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.value)
            self._inorder(node.right, res)

    def inorder(self):
        res = []
        self._inorder(self.root, res)
        return res


tree = Bst()
for v in [5, 1, 456, 23, 8, 4534, 87934]:
    tree.insert(v)

print(tree.inorder())


class MinHeap:
    def __init__(self):
        self.heap = []

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return (i * 2) + 1

    def _right(self, i):
        return (i * 2) + 2

    def push(self, value):
        self.heap.append(value)
        self._shift_up(len(self.heap) - 1)

    def _shift_up(self, i):
        while i > 0 and self.heap[self._parent(i)] > self.heap[i]:
            self.heap[i], self.heap[self._parent(i)] = self.heap[self._parent(i)], self.heap[i]
            i = self._parent(i)

    def pop(self):
        if not self.heap:
            return None

        root = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()

        if self.heap:
            self._shift_down(0)
        return root

    def _shift_down(self, i):
        n = len(self.heap)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)
            if l < n and self.heap[l] < self.heap[smallest]:
                smallest = l
            if r < n and self.heap[r] < self.heap[smallest]:
                smallest = r
            if smallest == i:
                break
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

h = MinHeap()
for v in [5, 1, 456, 23, 8, 4534, 87934]:
    h.push(v)

while h.heap:
    print(h.pop())