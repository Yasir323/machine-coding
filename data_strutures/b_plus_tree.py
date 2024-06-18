class Node:
    def __init__(self, keys=None, children=None):
        self.keys = keys or []
        self.children = children or []


class LeafNode:
    def __init__(self, keys=None, next_leaf=None):
        self.keys = keys or []
        self.next_leaf = next_leaf


class BPlusTree:
    def __init__(self, order=3):
        self.root = LeafNode()
        self.order = order
        self.split_threshold = order

    def insert(self, key, value):
        """
        Insert key-value pair into the B+ tree.
        """
        if self.root.keys == []:
            self.root.keys.append(key)
            self.root.children.append(value)
        else:
            if len(self.root.keys) == self.split_threshold:
                new_root = Node()
                new_root.children.append(self.root)
                self._split_child(new_root, 0)
                self.root = new_root

            self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        """
        Insert key-value pair into a non-full node.
        """
        if isinstance(node, LeafNode):
            self._insert_into_leaf(node, key, value)
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.split_threshold:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _insert_into_leaf(self, node, key, value):
        """
        Insert key-value pair into a leaf node.
        """
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        node.keys.insert(i, key)
        node.children.insert(i, value)

    def _split_child(self, parent, index):
        """
        Split a full child node at given index in the parent node.
        """
        child = parent.children[index]
        new_child = LeafNode(keys=child.keys[self.split_threshold:])
        child.keys = child.keys[:self.split_threshold]
        parent.keys.insert(index, new_child.keys[0])
        parent.children.insert(index + 1, new_child)

        if isinstance(child, Node):
            new_child.children = child.children[self.split_threshold:]
            child.children = child.children[:self.split_threshold]

    def search(self, key):
        """
        Search for a key in the B+ tree.
        """
        return self._search(self.root, key)

    def _search(self, node, key):
        """
        Helper function to search for a key in the B+ tree.
        """
        if isinstance(node, LeafNode):
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and key == node.keys[i]:
                return node.children[i]
            return None
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            return self._search(node.children[i], key)

    def range_query(self, start_key, end_key):
        """
        Perform a range query to retrieve values between start_key and end_key.
        """
        results = []
        current = self._find_leaf(self.root, start_key)
        while current is not None:
            for i in range(len(current.keys)):
                if start_key <= current.keys[i] <= end_key:
                    results.append(current.children[i])
                elif current.keys[i] > end_key:
                    return results
            current = current.next_leaf
        return results

    def _find_leaf(self, node, key):
        """
        Helper function to find the leaf node containing the key.
        """
        if isinstance(node, LeafNode):
            return node
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            return self._find_leaf(node.children[i], key)


if __name__ == "__main__":
    bptree = BPlusTree(order=3)

    keys = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    for key, value in zip(keys, values):
        bptree.insert(key, value)

    print("Searching for key 10:", bptree.search(10))
    print("Searching for key 5 (not present):", bptree.search(5))

    print("Range query from 8 to 16:", bptree.range_query(8, 16))
    print("Range query from 15 to 20:", bptree.range_query(15, 20))
