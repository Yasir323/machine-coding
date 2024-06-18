class Node:
    def __init__(self, key):
        self.key = key
        self.children = []


class KaryTree:
    def __init__(self, k):
        self.root = None
        self.k = k

    def insert(self, parent_key, key):
        if self.root is None:
            self.root = Node(key)
        else:
            parent_node = self.search(self.root, parent_key)
            if parent_node and len(parent_node.children) < self.k:
                parent_node.children.append(Node(key))
            else:
                print(f"Cannot insert {key}. Parent not found or maximum children reached.")

    def display(self, node, level=0):
        if node is not None:
            print(" " * (level * 4) + str(node.key))
            for child in node.children:
                self.display(child, level + 1)

    def search(self, node, key):
        if node is None:
            return None
        if node.key == key:
            return node
        for child in node.children:
            result = self.search(child, key)
            if result:
                return result
        return None

    def delete(self, key):
        if self.root is None:
            return
        if self.root.key == key:
            self.root = None
            return
        self._delete(self.root, key)

    def _delete(self, node, key):
        for i, child in enumerate(node.children):
            if child.key == key:
                node.children.pop(i)
                return True
            if self._delete(child, key):
                return True
        return False

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        for i in range(len(node.children) // 2):
            self._inorder(node.children[i], result)
        result.append(node.key)
        for i in range(len(node.children) // 2, len(node.children)):
            self._inorder(node.children[i], result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is None:
            return
        result.append(node.key)
        for child in node.children:
            self._preorder(child, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node is None:
            return
        for child in node.children:
            self._postorder(child, result)
        result.append(node.key)

    def level_order(self):
        if not self.root:
            return []
        queue, result = [self.root], []
        while queue:
            current = queue.pop(0)
            result.append(current.key)
            queue.extend(current.children)
        return result


# Example usage:
if __name__ == "__main__":
    k = 3  # Example for a ternary tree
    k_tree = KaryTree(k)
    k_tree.insert(None, 1)  # Insert root
    k_tree.insert(1, 2)
    k_tree.insert(1, 3)
    k_tree.insert(1, 4)
    k_tree.insert(2, 5)
    k_tree.insert(2, 6)
    k_tree.insert(3, 7)

    print("K-ary Tree:")
    k_tree.display(k_tree.root)

    print("\nInorder Traversal:", k_tree.inorder())
    print("Preorder Traversal:", k_tree.preorder())
    print("Postorder Traversal:", k_tree.postorder())
    print("Level Order Traversal:", k_tree.level_order())

    print("\nSearch for 6:", "Found" if k_tree.search(k_tree.root, 6) else "Not Found")
    print("Search for 10:", "Found" if k_tree.search(k_tree.root, 10) else "Not Found")

    print("\nDelete 2")
    k_tree.delete(2)
    k_tree.display(k_tree.root)

    print("\nDelete 1 (root)")
    k_tree.delete(1)
    k_tree.display(k_tree.root)
