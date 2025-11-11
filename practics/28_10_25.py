class Tree:
    def __init__(self, value = 0, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right


    def preorder(self, node):
        if node:
            print(node.value)
            preorder(node.left)
            preorder(node.right)

    def postorder(self, node):
        if node:
            postorder(node.left)
            postorder(node.right)
            print(node.value)

    def inorder(self, node):
        if node:
            inorder(node.left)
            print(node.value)
            inorder(node.right)


root = Tree(1)
root.left = Tree(2)
root.right = Tree(3)
root.left.right = Tree(4)

preorder(root)
inorder(root)
postorder(root)


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