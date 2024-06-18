class Node:

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BST:

    def __init__(self):
        self.root = None

    def insert(self, value):
        def _insert(node, value):
            if value < node.val:
                if node.left:
                    _insert(node.left, value)
                else:
                    node.left = Node(value)
            else:
                if node.right:
                    _insert(node.right, value)
                else:
                    node.right = Node(value)

        if self.root is None:
            self.root = Node(value)
        else:
            _insert(self.root, value)

    def display(self, node, level=0, prefix="Root: "):
        if node is not None:
            print(" " * (level*4) + prefix + str(node.val))
            if node.left:
                self.display(node.left, level + 1, "L--- ")
            if node.right:
                self.display(node.right, level + 1, "R--- ")

    def search(self, value):

        def _search(node):
            if value < node.val:
                if node.left:
                    return _search(node.left)
                return None
            elif value > node.val:
                if node.right:
                    return _search(node.right)
                return None
            else:
                return node

        if self.root is None:
            return
        else:
            if self.root.val == value:
                return self.root
            else:
                return _search(self.root)

    def delete(self, value):

        def _delete(node, key):
            if node is None:
                return node
            if key < node.val:
                node.left = _delete(node.left, key)
            elif key > node.val:
                node.right = _delete(node.right, key)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                temp = self.min(node.right)
                node.val = temp.val
                node.right = _delete(node.right, temp.val)
            return node

        self.root = _delete(self.root, value)

    @staticmethod
    def min(node):
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    @staticmethod
    def max(node):
        curr = node
        while curr.right is not None:
            curr = curr.right
        return curr

    def print_sorted(self):

        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            print(node.val)
            _inorder(node.right)

        _inorder(self.root)


def main():
    bst = BST()
    keys = [50, 30, 20, 40, 70, 60, 80]
    for key in keys:
        bst.insert(key)

    print("Binary Search Tree:")
    bst.display(bst.root)

    print("Level Order Traversal:", bst.print_sorted())

    print("\nSearch for 60:", "Found" if bst.search(60) else "Not Found")
    print("Search for 25:", "Found" if bst.search(25) else "Not Found")

    print("\nDelete 20")
    bst.delete(20)
    bst.display(bst.root)

    print("\nDelete 30")
    bst.delete(30)
    bst.display(bst.root)

    print("\nDelete 50")
    bst.delete(50)
    bst.display(bst.root)


if __name__ == "__main__":
    main()
