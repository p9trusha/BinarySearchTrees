from bst import BST, Node


class NodeAVL(Node):
    def __int__(self, key, value=None, parent=None):
        super().__init__(key, value, parent)
        self.height = 0

    def get_balance(self):
        if self.is_leaf():
            return 0
        if self.has_both_child():
            return self.left_child.height - self.right_child.height
        if self.left_child:
            return self.left_child.height + 1
        return - self.right_child.height - 1

    def change_height(self):
        if self.is_leaf():
            self.height = 0
        elif self.has_both_child():
            self.height = max(self.left_child.height, self.right_child.height) + 1
        else:
            if self.left_child:
                self.height = self.left_child.height + 1
            else:
                self.height = self.right_child.height + 1


class AVLTree(BST):
    def put(self, key, value=None):
        puted_node = super().put(key, value)
        puted_node.__class__ = NodeAVL
        puted_node.height = 0
        self._insert_fixup(puted_node)

    def _insert_fixup(self, node):
        if node.get_balance() == -2 or node.get_balance == 2:
            self._balancing(node)
        elif node.parent:
            node.parent.change_height()
            if node.parent.get_balance() != 0:
                self._insert_fixup(node.parent)

    def _delete(self, node_to_remove):
        if node_to_remove.is_leaf():
            node_to_update_height = node_to_remove.parent
            node_to_update_height.height = 0
            self.transplant(node_to_remove, None)
        else:
            if node_to_remove.has_both_child():
                successor_node = self.find_min(node_to_remove.right_child)
                if successor_node.right_child:
                    node_to_update_height = successor_node.right_child
                else:
                    node_to_update_height = successor_node.parent
                    successor_node.parent.change_height()
                if successor_node != node_to_remove.right_child:
                    self.transplant(successor_node, successor_node.right_child)
                    successor_node.right_child = node_to_remove.right_child
                    successor_node.right_child.parent = successor_node
                self.transplant(node_to_remove, successor_node)
                successor_node.left_child = node_to_remove.left_child
                successor_node.left_child.parent = successor_node
            else:
                if node_to_remove.left_child:
                    node_to_update_height = node_to_remove.left_child
                    self.transplant(node_to_remove, node_to_remove.left_child)
                else:
                    node_to_update_height = node_to_remove.right_child
                    self.transplant(node_to_remove, node_to_remove.right_child)
        self._delete_fixup(node_to_update_height)

    def _delete_fixup(self, node):
        if node.get_balance() == -2 or node.get_balance == 2:
            self._balancing(node)
        if node.parent:
            node.parent.change_height()
            if node.parent.get_balance() == 0:
                self._insert_fixup(node.parent)

    def _balancing(self, node):
        if node.get_balance() == -2:
            if node.right_child.get_balance() > 0:
                self._right_rotation(node.right_child)
                self._left_rotation(node)
            else:
                self._left_rotation(node)
        elif node.get_balance() == 2:
            if node.left_child.get_balance() < 0:
                self._left_rotation(node.left_child)
                self._right_rotation(node)
            else:
                self._right_rotation(node)

    def _get_height(self, node, height):
        return node.height

    def _left_rotation(self, rot_root):
        super()._left_rotation(rot_root)
        new_root = rot_root.parent
        rot_root.change_height()
        new_root.height = max(rot_root.right_child.height if rot_root.right_child else 0, rot_root.height) + 1

    def _right_rotation(self, rot_root):
        super()._right_rotation(rot_root)
        new_root = rot_root.parent
        rot_root.change_height()
        new_root.height = max(rot_root.left_child.hieght if rot_root.left_child else 0, rot_root.height) + 1
