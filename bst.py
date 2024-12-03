class Node:
    def __init__(self, key, value=None, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_child = None
        self.right_child = None

    def is_root(self):
        return not self.parent

    def is_leaf(self):
        return (not self.left_child) and (not self.right_child)

    def has_both_child(self):
        return self.left_child and self.right_child

    def is_left_child(self):
        return self.parent and self.parent.left_child == self

    def is_right_child(self):
        return self.parent and self.parent.right_child == self

    def get_sibling(self):
        if self.is_root():
            return None
        if self.is_left_child():
            return self.parent.right_child
        return self.parent.left_child

    def get_uncle(self):
        if self.parent.parent:
            return self.parent.get_sibling()
        return None


class BST:
    def __init__(self):
        self.root = None
        self.size = 0

    def get(self, key):
        if self.root:
            result = self._get(key, self.root)
            if result:
                return result.value
            else:
                return None
        else:
            return None

    def _get(self, key, current_node):
        if current_node is None:
            return None
        if key < current_node.key:
            return self._get(key, current_node.left_child)
        elif key > current_node.key:
            return self._get(key, current_node.right_child)
        return current_node

    def put(self, key, value=None):
        self.size += 1
        if self.size == 1:
            self.root = Node(key, value)
            return self.root
        else:
            return self._put(key, value, self.root)

    def _put(self, key, value, current_node):
        if key < current_node.key:
            if current_node.left_child and current_node.left_child.key:
                return self._put(key, value, current_node.left_child)
            else:
                current_node.left_child = Node(key, value, current_node)
                return current_node.left_child
        elif key > current_node.key:
            if current_node.right_child and current_node.right_child.key:
                return self._put(key, value, current_node.right_child)
            else:
                current_node.right_child = Node(key, value, current_node)
                return current_node.right_child
        else:
            current_node.value = value
            return current_node

    def delete(self, key):
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            if node_to_remove:
                self.size -= 1
                return self._delete(node_to_remove)
            else:
                raise KeyError("key is not in tree")
        elif self.size == 1 and key == self.root.key:
            self.root = None
            self.size = 0
            return None
        else:
            raise KeyError("key is not in tree")

    def _delete(self, node_to_remove):
        if not node_to_remove.left_child:
            self.transplant(node_to_remove, node_to_remove.right_child)
        elif not node_to_remove.right_child:
            self.transplant(node_to_remove, node_to_remove.left_child)
        else:
            successor_node = self.find_min(node_to_remove.right_child)
            if successor_node != node_to_remove.right_child:
                self.transplant(successor_node, successor_node.right_child)
                successor_node.right_child = node_to_remove.right_child
                successor_node.right_child.parent = successor_node
            self.transplant(node_to_remove, successor_node)
            successor_node.left_child = node_to_remove.left_child
            successor_node.left_child.parent = successor_node

    def transplant(self, old_node, new_node):
        if not old_node.parent:
            self.root = new_node
        elif old_node.is_left_child():
            old_node.parent.left_child = new_node
        else:
            old_node.parent.right_child = new_node
        if new_node:
            new_node.parent = old_node.parent

    def find_min(self, node):
        while node.left_child:
            node = node.left_child
        return node

    def get_height(self):
        if not self.root:
            return 0
        return self._get_height(self.root, 0)

    def _get_height(self, node, height):
        if not node:
            return height - 1
        height += 1
        return max(self._get_height(node.left_child, height),
                   self._get_height(node.right_child, height))

    def depth_traversal(self, mode="LNR"):
        if not self.root:
            return []
        return self._depth_traversal(self.root, [], mode)

    def _depth_traversal(self, node, keys, mode):
        if node:
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

    def breadth_traversal(self):
        bst_as_list_of_keys = []
        level = [self.root]
        len_level = 1
        while len(level) != 0:
            level_keys = []
            for i in range(len_level):
                level_keys.append(level[i].key)
                if level[i].left_child:
                    level.append(level[i].left_child)
                if level[i].right_child:
                    level.append(level[i].right_child)
            bst_as_list_of_keys.append(level_keys)
            level = level[len_level:]
            len_level = len(level)
        return bst_as_list_of_keys

    def _left_rotation(self, rot_root):
        new_root = rot_root.right_child
        rot_root.right_child = new_root.left_child
        if new_root.left_child:
            new_root.left_child.parent = rot_root
        new_root.parent = rot_root.parent
        if new_root.is_root():
            self.root = new_root
        else:
            if rot_root.is_left_child():
                rot_root.parent.left_child = new_root
            else:
                rot_root.parent.right_child = new_root
        new_root.left_child = rot_root
        rot_root.parent = new_root

    def _right_rotation(self, rot_root):
        new_root = rot_root.left_child
        rot_root.right_child = new_root.right_child
        if new_root.right_child:
            new_root.right_child.parent = rot_root
        new_root.parent = rot_root.parent
        if new_root.is_root():
            self.root = new_root
        else:
            if rot_root.is_left_child():
                rot_root.parent.left_child = new_root
            else:
                rot_root.parent.right_child = new_root
        new_root.right_child = rot_root
        rot_root.parent = new_root
