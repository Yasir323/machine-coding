class BTreeNode:
    def __init__(self, t, leaf=False):
        """
        Initialize a B-Tree node.

        :param t: Minimum degree of the B-Tree.
        :param leaf: Boolean indicating if the node is a leaf.
        """
        self.t = t  # Minimum degree (defines the range for number of keys)
        self.keys = []  # List of keys in the node
        self.children = []  # List of child nodes
        self.leaf = leaf  # True if the node is a leaf, False otherwise


class BTree:
    def __init__(self, t):
        """
        Initialize an empty B-Tree.

        :param t: Minimum degree of the B-Tree.
        """
        self.root = BTreeNode(t, True)
        self.t = t

    def traverse(self):
        """
        Traverse and print all keys in the B-Tree.
        """

        def _traverse(node):
            for i in range(len(node.keys)):
                if not node.leaf:
                    _traverse(node.children[i])
                print(node.keys[i], end=' ')
            if not node.leaf:
                _traverse(node.children[len(node.keys)])

        _traverse(self.root)
        print()

    def search(self, k):
        """
        Search for a key in the B-Tree.

        :param k: Key to search for.
        :return: Tuple (node, index) if found, else None.
        """

        def _search(node, k):
            i = 0
            while i < len(node.keys) and k > node.keys[i]:
                i += 1
            if i < len(node.keys) and k == node.keys[i]:
                return node, i
            if node.leaf:
                return None
            return _search(node.children[i], k)

        return _search(self.root, k)

    def insert(self, k):
        """
        Insert a key into the B-Tree.

        :param k: Key to insert.
        """
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, k)

    def _insert_non_full(self, node, k):
        """
        Insert a key into a non-full node.

        :param node: Node to insert into.
        :param k: Key to insert.
        """
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, parent, i):
        """
        Split a full child node.

        :param parent: Parent node.
        :param i: Index of the child in the parent node.
        """
        t = self.t
        node = parent.children[i]
        new_node = BTreeNode(t, node.leaf)
        parent.children.insert(i + 1, new_node)
        parent.keys.insert(i, node.keys[t - 1])
        new_node.keys = node.keys[t:(2 * t - 1)]
        node.keys = node.keys[0:(t - 1)]
        if not node.leaf:
            new_node.children = node.children[t:(2 * t)]
            node.children = node.children[0:t]

    def delete(self, k):
        """
        Delete a key from the B-Tree.

        :param k: Key to delete.
        """
        self._delete(self.root, k)
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = BTreeNode(self.t, True)

    def _delete(self, node, k):
        """
        Delete a key from a node.

        :param node: Node to delete from.
        :param k: Key to delete.
        """
        t = self.t
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            if node.leaf:
                node.keys.pop(i)
            else:
                if len(node.children[i].keys) >= t:
                    node.keys[i] = self._get_predecessor(node, i)
                    self._delete(node.children[i], node.keys[i])
                elif len(node.children[i + 1].keys) >= t:
                    node.keys[i] = self._get_successor(node, i)
                    self._delete(node.children[i + 1], node.keys[i])
                else:
                    self._merge(node, i)
                    self._delete(node.children[i], k)
        else:
            if node.leaf:
                return
            if len(node.children[i].keys) < t:
                self._fill(node, i)
            if i > len(node.keys):
                self._delete(node.children[i - 1], k)
            else:
                self._delete(node.children[i], k)

    def _get_predecessor(self, node, i):
        """
        Get the predecessor key of the key at index i in the node.

        :param node: Node containing the key.
        :param i: Index of the key in the node.
        :return: Predecessor key.
        """
        current = node.children[i]
        while not current.leaf:
            current = current.children[len(current.keys)]
        return current.keys[len(current.keys) - 1]

    def _get_successor(self, node, i):
        """
        Get the successor key of the key at index i in the node.

        :param node: Node containing the key.
        :param i: Index of the key in the node.
        :return: Successor key.
        """
        current = node.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _merge(self, node, i):
        """
        Merge the child node at index i with the child node at index i+1.

        :param node: Parent node.
        :param i: Index of the first child.
        """
        t = self.t
        child = node.children[i]
        sibling = node.children[i + 1]
        child.keys.append(node.keys[i])
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        node.keys.pop(i)
        node.children.pop(i + 1)

    def _fill(self, node, i):
        """
        Fill the child node at index i which has less than t-1 keys.

        :param node: Parent node.
        :param i: Index of the child node.
        """
        if i != 0 and len(node.children[i - 1].keys) >= self.t:
            self._borrow_from_prev(node, i)
        elif i != len(node.keys) and len(node.children[i + 1].keys) >= self.t:
            self._borrow_from_next(node, i)
        else:
            if i != len(node.keys):
                self._merge(node, i)
            else:
                self._merge(node, i - 1)

    def _borrow_from_prev(self, node, i):
        """
        Borrow a key from the previous child node.

        :param node: Parent node.
        :param i: Index of the child node.
        """
        child = node.children[i]
        sibling = node.children[i - 1]
        child.keys.insert(0, node.keys[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        node.keys[i - 1] = sibling.keys.pop()

    def _borrow_from_next(self, node, i):
        """
        Borrow a key from the next child node.

        :param node: Parent node.
        :param i: Index of the child node.
        """
        child = node.children[i]
        sibling = node.children[i + 1]
        child.keys.append(node.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        node.keys[i] = sibling.keys.pop(0)


# Example usage:
if __name__ == "__main__":
    t = 3  # A B-Tree with minimum degree 3
    tree = BTree(t)

    keys = [10, 20, 5, 6, 12, 30, 7, 17]

    for key in keys:
        tree.insert(key)

    print("Traversal of the constructed B-Tree is:")
    tree.traverse()

    print("\nSearching for key 6:")
    result = tree.search(6)
    print("Found" if result else "Not found")

    print("\nDeleting key 6")
    tree.delete(6)
    print("Traversal after deleting key 6:")
    tree.traverse()

    print("\nDeleting key 13 (not present)")
    tree.delete(13)
    print("Traversal after attempting to delete key 13:")
    tree.traverse()

    print("\nDeleting key 7")
    tree.delete(7)
    print("Traversal after deleting key 7:")
    tree.traverse()
