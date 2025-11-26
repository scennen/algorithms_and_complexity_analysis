# 1 узел либо карсный либо черный
# коренной узел всегда черынй
# все листья (не крайние ноды графа, а null. назвывается nil) черные
# красный узел не может иметь красного ребенка
# черная высота будет всегда одниаковой (чв - сколько черных путей будет до nil)
# n - новый узел, p - родитель, g - дедкшка, u - дядя
from enum import Enum
from typing import Any, Optional


class Color(Enum):
    RED = 0
    BLACK = 1


class Node:
    # __slots__ = ('key', 'color', 'left', 'right', 'parent')

    def __init__(self, key: Any, color: Color):
        self.key: Any = key
        self.color: Color = color
        self.left: 'Node'
        self.right: 'Node'
        self.parent: 'Node'  # ← даже корень ссылается на NIL, поэтому тип 'Node', не Optional


# Создаём глобальный NIL-узел ПОСЛЕ определения класса
# NIL используется вместо null, как заглушка, и используем мы его, потому что не можем проверять null на "черность" и получим exception
NIL = Node(key=None, color=Color.BLACK)
NIL.left = NIL
NIL.right = NIL
NIL.parent = NIL


class RedBlackTree:
    def __init__(self):
        self.root: Node = NIL

    def insert(self, key: Any) -> None:
        new_node = Node(key=key, color=Color.RED)
        new_node.left = NIL
        new_node.right = NIL

        parent: Node = NIL  # ← начинаем с NIL, а не None
        current: Node = self.root

        while current is not NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is NIL:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Если это корень — сразу красим в чёрный
        if new_node.parent is NIL:
            new_node.color = Color.BLACK
            return

        # Если нет деда — ничего не нарушено
        if new_node.parent.parent is NIL:
            return

        self._fix_insert(new_node)

    def _fix_insert(self, node: Node) -> None:
        while node.parent is not NIL and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == Color.RED:
                    # Случай 1: дядя красный
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Случай 2: треугольник
                        node = node.parent
                        self._left_rotate(node)
                    # Случай 3: линия
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._right_rotate(node.parent.parent)
            else:
                # Симметрично для правого ребёнка
                uncle = node.parent.parent.left
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._left_rotate(node.parent.parent)

        self.root.color = Color.BLACK

    def _left_rotate(self, x: Node) -> None:
        y = x.right
        x.right = y.left
        if y.left is not NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y: Node) -> None:
        x = y.left
        y.left = x.right
        if x.right is not NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    def search(self, key: Any) -> bool:
        current = self.root
        while current is not NIL:
            if key == current.key:
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return False

    def _inorder_helper(self, node: Node, result: list) -> None:
        if node is not NIL:
            self._inorder_helper(node.left, result)
            result.append((node.key, 'R' if node.color == Color.RED else 'B'))
            self._inorder_helper(node.right, result)

    def inorder(self) -> list:
        result = []
        self._inorder_helper(self.root, result)
        return result

    def print_tree(self, node: Optional[Node] = None, level: int = 0, prefix: str = "Root: ") -> None:
        """
        Печатает дерево в виде иерархического текста.
        Цвет узла указан в скобках: (R) или (B).
        """
        if node is None:
            node = self.root
            if node is NIL:
                print("Empty tree")
                return

        if node is NIL:
            # Обычно не должно вызываться напрямую, но на всякий случай
            return

        # Определяем цвет для отображения
        color_str = 'R' if node.color == Color.RED else 'B'
        print(" " * (level * 4) + prefix + f"{node.key} ({color_str})")

        # Рекурсивно печатаем детей, только если они не NIL
        if node.left is not NIL or node.right is not NIL:
            if node.left is not NIL:
                self.print_tree(node.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- NIL")

            if node.right is not NIL:
                self.print_tree(node.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- NIL")


# Пример использования
if __name__ == "__main__":
    tree = RedBlackTree()
    for i in range(1, 11):
        tree.insert(i)
        tree.print_tree()
        print()

    print()
    tree.print_tree()
    print("Search 15:", tree.search(15))
    print("Search 100:", tree.search(100))


from enum import Enum
from typing import Any, Optional


class Color(Enum):
    RED = 0
    BLACK = 1


class Node:
    def __init__(self, key: Any, color: Color):
        self.key: Any = key
        self.color: Color = color
        self.left: 'Node'
        self.right: 'Node'
        self.parent: 'Node'


NIL = Node(key=None, color=Color.BLACK)
NIL.left = NIL
NIL.right = NIL
NIL.parent = NIL