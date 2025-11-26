class Node:
    def __init__(self, key: int, value: int):
        self.key: int = key
        self.value: int = value
        self.left: Node = None
        self.right: Node = None
        self.heigth: int = 0


class AVL_tree:
    def __init__(self):
        self.root: Node = None

    def _update_heigth(node: Node) -> None:
        node.heigth = max(AVL_tree.get_heigth(node.left), AVL_tree.get_heigth(node.right)) + 1

    def get_heigth(node: Node) -> int:
        return -1 if node is None else node.heigth

    def get_balance(node: Node) -> int:
        return 0 if node is None else AVL_tree.get_heigth(node.right) - AVL_tree.get_heigth(node.left)

    def left_rotate(node: Node) -> Node:
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        AVL_tree._update_heigth(node)
        AVL_tree._update_heigth(right_child)
        return right_child

    def right_rotate(node: Node) -> Node:
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        AVL_tree._update_heigth(node)
        AVL_tree._update_heigth(left_child)
        return left_child

    def balance(node: Node) -> Node:
        balance_factor = AVL_tree.get_balance(node)
        if balance_factor == -2:
            if AVL_tree.get_balance(node.left) == 1:
                node.left = AVL_tree.left_rotate(node.left)
            return AVL_tree.right_rotate(node)
        elif balance_factor == 2:
            if AVL_tree.get_balance(node.right) == -1:
                node.right = AVL_tree.right_rotate(node.right)
            return AVL_tree.left_rotate(node)
        return node

    def _insert(node: Node, key: int, value: int) -> Node:
        if node is None:
            return Node(key, value)

        if key < node.key:
            node.left = AVL_tree._insert(node.left, key, value)
        elif key >= node.key:
            node.right = AVL_tree._insert(node.right, key, value)
        else:
            node.value = value
            return node

        AVL_tree._update_heigth(node)
        return AVL_tree.balance(node)

    def insert(self, key, value) -> None:
        self.root = AVL_tree._insert(self.root, key, value)

    def _get_min(node: Node) -> Node:
        if node == None: return None
        if node.left == None: return node
        return AVL_tree._get_min(node.left)

    def _get_max(node: Node) -> Node:
        if node == None: return None
        if node.right == None: return node
        return AVL_tree._get_max(node.right)

    def _delete(node: Node, key: int) -> Node:
        if node == None:
            return None
        elif key < node.key:
            node.left = AVL_tree._delete(node.left, key)
        elif key > node.key:
            node.right = AVL_tree._delete(node.right, key)
        else:
            if node.left is None or node.right is None:
                node = node.right if node.left == None else node.left
            else:
                max_in_left = AVL_tree._get_max(node.left)
                node.key = max_in_left.key
                node.value = max_in_left.value
                node.left = AVL_tree._delete(node.left, max_in_left.key)

        if not node is None:
            AVL_tree._update_heigth(node)
            node = AVL_tree.balance(node)

        return node

    def delete(self, key: int) -> Node:
        self.root = AVL_tree._delete(self.root, key)

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


tree: AVL_tree = AVL_tree()
for i in range(1, 11):
    tree.insert(i, i)
    tree.print_tree()
    print()

tree.print_sym_tree()

print()
tree.delete(8)
tree.print_sym_tree()
tree.print_tree()