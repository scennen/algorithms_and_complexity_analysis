class AVLNode:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None
        self.height = 1


class  AVLTree:
    def height(self, node):  # счет высоты
        if not node:
            return 0
        return node.height

    def balance_factor(self, node: AVLNode):
        if not node:
            return 0
        return 1 + self.height(node.right) - self.height(node.left)

    def update_height(self, node: AVLNode):  # пересчитываем высоты
        if node:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotate_right(self, z: AVLNode):
        y: AVLNode = z.left
        t3: AVLNode = y.right

        y.right = z  # вращаем
        z.left = t3

        self.update(z)  # обновляем
        self.update(y)

        return y

    def rotate_left(self, y: AVLNode):
        z: AVLNode = y.right
        t2: AVLNode = z.left

        z.left = y
        y.right = t2

        self.update_height(y)
        self.update_height(z)
        return z

    def insert(self, node: AVLNode, value):
        # base insert
        if not node:
            return AVLNode(value)

        if value < node.value:
            node.left = self.insert(node.left, value)

        elif value > node.value:
            node.right = self.insert(node.right, value)

        else:
            return node

        # update height
        self.update_height(node)

        # check balance
        bf = self.balance_factor(node)


        # rotate
        if bf < -1 and value < node.left.value:
            return self.rotate_right(node)

        elif bf > -1 and value < node.right.value:
            return self.rotate_left(node)

        elif bf < -1 and value > node.left.value:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        elif bf > -1 and value < node.right.value:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def inorder(self, node: AVLNode, result):
        if node:
            self.inorder(node.left, result)
            result.append(node.value)
            self.inorder(node.right, result)

    def print_tree_horizontal(self, root, level, prefix="root: "):
        if root is not None:
            print(" " * (level * 4) + prefix + str(root.value))
            if root.left:
                print_tree_horizontal(root.left, level+1, "L---")
            else:
                print(" " * ((level + 1) * 4) + 'L--- None')
            if root.right:
                print_tree_horizontal(root.right, level+1, "R---")
            else:
                print(" " * ((level + 1) * 4) + 'R--- None')


tree = AVLTree()
root = None
for v in [10, 20, 30, 40, 50, 25]:
    root = tree.insert(root, v)

result = []
tree.inorder(root, result)
print(f'inorder: {result}')

print_tree_horizontal(root)


# минхип на основе красночерного дерева -- это задание на звездочку