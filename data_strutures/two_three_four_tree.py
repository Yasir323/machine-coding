class TreeNode:
    def __init__(self, is_leaf=False):
        self.keys = []             # List of keys in the node
        self.children = []         # List of child nodes
        self.is_leaf = is_leaf     # Boolean indicating if the node is a leaf

    def is_full(self):
        return len(self.keys) == 3  # Check if node is full (has 3 keys)

    def insert_key(self, key):
        self.keys.append(key)
        self.keys.sort()           # Insert key into the node and sort keys


class TwoThreeFourTree:
    def __init__(self):
        self.root = None   # Initialize an empty 2-3-4 tree

    def insert(self, key):
        """
        Insert a key into the 2-3-4 tree.

        :param key: The key to be inserted.
        """
        if self.root is None:
            self.root = TreeNode(is_leaf=True)
            self.root.insert_key(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        """
        Recursive function to insert a key into the 2-3-4 tree.

        :param node: Current node being processed.
        :param key: The key to be inserted.
        """
        if node.is_leaf:
            # If leaf node, insert key directly
            node.insert_key(key)
            self._split(node)
        else:
            # Find appropriate child to insert key
            index = self._find_child_index(node, key)
            self._insert(node.children[index], key)

    def _find_child_index(self, node, key):
        """
        Helper function to find the index of the child node where the key should be inserted.

        :param node: Parent node whose child nodes are being considered.
        :param key: The key to be inserted.
        :return: Index of the child node where key should be inserted.
        """
        for i in range(len(node.keys)):
            if key < node.keys[i]:
                return i
        return len(node.keys)

    def _split(self, node):
        """
        Perform splitting of a node if it is full (has 3 keys).

        :param node: The node to be split.
        """
        if node.is_full():
            mid_key = node.keys[1]

            left_node = TreeNode(is_leaf=node.is_leaf)
            left_node.keys = [node.keys[0]]
            if not node.is_leaf:
                left_node.children = [node.children[0], node.children[1]]

            right_node = TreeNode(is_leaf=node.is_leaf)
            right_node.keys = [node.keys[2]]
            if not node.is_leaf:
                right_node.children = [node.children[2], node.children[3]]

            if node == self.root:
                new_root = TreeNode()
                new_root.keys = [mid_key]
                new_root.children = [left_node, right_node]
                self.root = new_root
            else:
                parent = self._find_parent(self.root, node)
                parent.insert_key(mid_key)
                index = parent.keys.index(mid_key)

                parent.children[index] = left_node
                parent.children.insert(index + 1, right_node)

    def _find_parent(self, parent, node):
        """
        Helper function to find the parent of a node in the 2-3-4 tree.

        :param parent: Current node being processed.
        :param node: The node whose parent is being searched.
        :return: Parent node of the given node.
        """
        if node in parent.children:
            return parent
        for child in parent.children:
            if not child.is_leaf and node in child.children:
                return self._find_parent(child, node)

    def search(self, key):
        """
        Search for a key in the 2-3-4 tree.

        :param key: The key to search for.
        :return: True if key is found, False otherwise.
        """
        return self._search(self.root, key)

    def _search(self, node, key):
        """
        Recursive function to search for a key in the 2-3-4 tree.

        :param node: Current node being processed.
        :param key: The key to search for.
        :return: True if key is found, False otherwise.
        """
        if node is None:
            return False
        if key in node.keys:
            return True
        elif node.is_leaf:
            return False
        else:
            index = self._find_child_index(node, key)
            return self._search(node.children[index], key)

    def delete(self, key):
        """
        Delete a key from the 2-3-4 tree.

        :param key: The key to be deleted.
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """
        Recursive function to delete a key from the 2-3-4 tree.

        :param node: Current node being processed.
        :param key: The key to be deleted.
        :return: Updated node after deletion.
        """
        if node is None:
            return None

        # Find the index of the key in the current node
        index = node.keys.index(key) if key in node.keys else None

        if index is not None:  # Key found in the current node
            if node.is_leaf:
                node.keys.remove(key)
            else:
                # Replace key with predecessor or successor
                if node.children[index].is_leaf:
                    predecessor = self._get_predecessor(node, index)
                    node.keys[index] = predecessor
                    node.children[index] = self._delete(node.children[index], predecessor)
                else:
                    successor = self._get_successor(node, index)
                    node.keys[index] = successor
                    node.children[index + 1] = self._delete(node.children[index + 1], successor)
        else:  # Key not found in the current node
            index = self._find_child_index(node, key)
            if node.children[index].is_leaf:
                return node
            node.children[index] = self._delete(node.children[index], key)

        # Balance the tree after deletion
        if node == self.root and not node.keys and node.children:
            self.root = node.children[0]

        return node

    def _get_predecessor(self, node, index):
        """
        Helper function to find the predecessor key of a given key in the 2-3-4 tree.

        :param node: Current node being processed.
        :param index: Index of the key in the node.
        :return: Predecessor key.
        """
        current = node.children[index]
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node, index):
        """
        Helper function to find the successor key of a given key in the 2-3-4 tree.

        :param node: Current node being processed.
        :param index: Index of the key in the node.
        :return: Successor key.
        """
        current = node.children[index + 1]
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def inorder_traversal(self):
        """
        Perform an inorder traversal of the 2-3-4 tree and print keys in sorted order.
        """
        self._inorder_traversal(self.root)

    def _inorder_traversal(self, node):
        """
        Recursive function to perform inorder traversal of the 2-3-4 tree.

        :param node: Current node being processed.
        """
        if node is None:
            return
        for i in range(len(node.keys)):
            self._inorder_traversal(node.children[i])
            print(node.keys[i], end=" ")
        self._inorder_traversal(node.children[-1])


