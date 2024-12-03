from bst import BST, Node
from enum import Enum


class Color(Enum):
    red = 0
    black = 1


class NodeRedBlack(Node):
    def __int__(self, key, value=None, parent=None, color=Color.red):
        super().__init__(key, value, parent)
        self.color = color

    def is_red(self):
        return self.color == Color.red

    def is_black(self):
        return self.color == Color.black


class RedBlackTree(BST):
    def __init__(self):
        super().__init__()
        self.leaf = NodeRedBlack(key=None)
        self.leaf.color = Color.black

    def put(self, key, value=None):
        puted_node = super().put(key, value)
        puted_node.__class__ = NodeRedBlack
        if puted_node is self.root:
            puted_node.color = Color.black
        else:
            puted_node.color = Color.red
        puted_node.left_child = self.leaf
        puted_node.right_child = self.leaf
        self._insert_fixup(puted_node)

    def _insert_fixup(self, node):
        while node.parent and node.parent.parent and node.parent.is_red():
            uncle = node.get_uncle()
            if uncle.is_red():
                node.parent.color = Color.black
                uncle.color = Color.black
                node.parent.parent.color = Color.red
                node = node.parent.parent
            else:
                if node.parent.is_left_child():
                    if node.is_right_child():
                        node = node.parent
                        self._left_rotation(node)
                    node.parent.color = Color.black
                    node.parent.parent.color = Color.red
                    self._right_rotation(node.parent.parent)
                else:
                    if node.is_left_child():
                        node = node.parent
                        self._right_rotation(node)
                    node.parent.color = Color.black
                    node.parent.parent.color = Color.red
                    self._left_rotation(node.parent.parent)
        self.root.color = Color.black

    def _delete(self, node_to_remove):
        removed_node_color = node_to_remove.color
        if node_to_remove.left_child == self.leaf:
            successor_node = node_to_remove.right_child
            self.transplant(node_to_remove, successor_node)
        elif node_to_remove.right_child == self.leaf:
            successor_node = node_to_remove.left_child
            self.transplant(node_to_remove, successor_node)
        else:
            successor_node = self.find_min(node_to_remove.right_child)
            removed_node_color = successor_node.color
            successor_node.parent.left_child = successor_node.right_child
            successor_node.left_child = node_to_remove.left_child
            successor_node.right_child = node_to_remove.right_child
            self.transplant(node_to_remove, successor_node)
            successor_node = successor_node.right_child
        if removed_node_color == Color.black:
            self._delete_fixup(successor_node)

    def _delete_fixup(self, node):
        while node != self.root and node.is_black():
            if node.is_left_child():
                sibling = node.parent.right_child
                if sibling.is_red():
                    sibling.color = Color.black
                    node.parent.color = Color.red
                    self._left_rotation(node.parent)
                    sibling = node.parent.right_child
                if sibling.left_child.is_black() and sibling.right_child.is_black():
                    sibling.color = Color.red
                    node = node.parent
                else:
                    if sibling.right_child.is_black():
                        sibling.left_child.color = Color.black
                        sibling.color = Color.red
                        self._right_rotation(sibling)
                        sibling = node.parent.right_child
                    sibling.color = node.parent.color
                    node.parent.color = Color.black
                    sibling.right_child.color = Color.black
                    self._left_rotation(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left_child
                if sibling.is_red():
                    sibling.color = Color.black
                    node.parent.color = Color.red
                    self._right_rotation(node.parent)
                    sibling = node.parent.left_child
                if sibling.rifht_child.is_black() and sibling.left_child.is_black():
                    sibling.color = Color.red
                    node = node.parent
                else:
                    if sibling.left_child.is_black():
                        sibling.right_child.color = Color.black
                        sibling.color = Color.red
                        self._left_rotation(sibling)
                        sibling = node.parent.left_child
                    sibling.color = node.parent.color
                    node.parent.color = Color.black
                    sibling.left_child.color = Color.black
                    self._right_rotation(node.parent)
                    node = self.root
        node.color = Color.black

    def find_min(self, node):
        while node.left_child != self.leaf:
            node = node.left_child
        return node

    def _depth_traversal(self, node, keys, mode):
        if node.key:
            if mode.upper() == "NLR":
                keys.append(node.key)
                self._depth_traversal(node.left_child, keys, mode)
                self._depth_traversal(node.right_child, keys, mode)
            elif mode.upper() == "LNR":
                self._depth_traversal(node.left_child, keys, mode)
                keys.append(node.key)
                self._depth_traversal(node.right_child, keys, mode)
            elif mode.upper() == "LRN":
                self._depth_traversal(node.left_child, keys, mode)
                self._depth_traversal(node.right_child, keys, mode)
                keys.append(node.key)
        return keys
