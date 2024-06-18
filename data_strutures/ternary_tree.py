class TSTNode:
    def __init__(self, character):
        self.character = character   # Character stored in this node
        self.left = None             # Pointer to the left child node
        self.middle = None           # Pointer to the middle child node
        self.right = None            # Pointer to the right child node
        self.value = None            # Value associated with the key (optional)


class TernarySearchTree:
    def __init__(self):
        self.root = None   # Initialize an empty TST

    def insert(self, key, value=None):
        """
        Insert a key-value pair into the TST.

        :param key: The key to be inserted (a string).
        :param value: The value associated with the key (optional).
        """
        self.root = self._insert(self.root, key, value, 0)

    def _insert(self, node, key, value, index):
        """
        Recursive function to insert a key-value pair into the TST.

        :param node: Current node being processed.
        :param key: The key to be inserted.
        :param value: The value associated with the key.
        :param index: Current index of the character in the key.
        :return: Updated node.
        """
        char = key[index]

        # Create a new node if the current node is None
        if node is None:
            node = TSTNode(char)

        # Insert into the left subtree
        if char < node.character:
            node.left = self._insert(node.left, key, value, index)

        # Insert into the middle subtree (equal case)
        elif char == node.character:
            if index < len(key) - 1:
                node.middle = self._insert(node.middle, key, value, index + 1)
            else:
                node.value = value

        # Insert into the right subtree
        else:
            node.right = self._insert(node.right, key, value, index)

        return node

    def search(self, key):
        """
        Search for a key in the TST and return its associated value.

        :param key: The key to search for.
        :return: The value associated with the key, or None if key not found.
        """
        node = self._search(self.root, key, 0)
        if node is None:
            return None
        return node.value

    def _search(self, node, key, index):
        """
        Recursive function to search for a key in the TST.

        :param node: Current node being processed.
        :param key: The key to search for.
        :param index: Current index of the character in the key.
        :return: Node containing the key-value pair, or None if key not found.
        """
        if node is None:
            return None

        char = key[index]

        # Search in the left subtree
        if char < node.character:
            return self._search(node.left, key, index)

        # Search in the middle subtree (equal case)
        elif char == node.character:
            if index == len(key) - 1:
                return node
            return self._search(node.middle, key, index + 1)

        # Search in the right subtree
        else:
            return self._search(node.right, key, index)

    def delete(self, key):
        """
        Delete a key from the TST.

        :param key: The key to be deleted.
        """
        self.root = self._delete(self.root, key, 0)

    def _delete(self, node, key, index):
        """
        Recursive function to delete a key from the TST.

        :param node: Current node being processed.
        :param key: The key to be deleted.
        :param index: Current index of the character in the key.
        :return: Updated node after deletion.
        """
        if node is None:
            return None

        char = key[index]

        # Delete from the left subtree
        if char < node.character:
            node.left = self._delete(node.left, key, index)

        # Delete from the middle subtree (equal case)
        elif char == node.character:
            if index < len(key) - 1:
                node.middle = self._delete(node.middle, key, index + 1)
            else:
                node.value = None   # Remove the value associated with the key

        # Delete from the right subtree
        else:
            node.right = self._delete(node.right, key, index)

        # Cleanup: If node has no children and no value, it can be pruned
        if node.left is None and node.middle is None and node.right is None and node.value is None:
            return None

        return node

    def traverse(self):
        """
        Traverse the TST and print all keys in lexicographical order.
        """
        keys = []
        self._traverse(self.root, "", keys)
        for key in keys:
            print(key)

    def _traverse(self, node, prefix, keys):
        """
        Recursive function to traverse the TST and collect keys in lexicographical order.

        :param node: Current node being processed.
        :param prefix: Prefix string accumulated during traversal.
        :param keys: List to store collected keys.
        """
        if node is None:
            return

        # Traverse left subtree
        self._traverse(node.left, prefix, keys)

        # Accumulate current character
        prefix += node.character
        if node.value is not None:
            keys.append(prefix)

        # Traverse middle subtree
        self._traverse(node.middle, prefix, keys)

        # Remove last character from prefix for right subtree traversal
        prefix = prefix[:-1]

        # Traverse right subtree
        self._traverse(node.right, prefix, keys)


if __name__ == "__main__":
    tst = TernarySearchTree()

    keys = ["cat", "dog", "car", "card", "care", "cars"]
    values = [1, 2, 3, 4, 5, 6]

    # Insert keys into TST
    for key, value in zip(keys, values):
        tst.insert(key, value)

    # Search for keys
    print("Searching for 'car':", tst.search("car"))
    print("Searching for 'care':", tst.search("care"))
    print("Searching for 'apple':", tst.search("apple"))

    # Traverse and print all keys
    print("All keys in TST:")
    tst.traverse()

    # Delete a key
    tst.delete("card")
    print("\nAfter deleting 'card':")
    tst.traverse()
