class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # New nodes are initially added at the leaf position.


class AVLTree:
    def insert(self, root, key):
        """
        Insert a key into the AVL tree and balance the tree.
        """
        # Step 1: Perform the normal BST insertion.
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # Step 2: Update the height of the ancestor node.
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Step 3: Get the balance factor.
        balance = self.get_balance(root)

        # Step 4: If the node becomes unbalanced, then there are 4 cases.

        # Left Left Case.
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case.
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case.
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case.
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        """
        Delete a key from the AVL tree and balance the tree.
        """
        # Step 1: Perform the normal BST delete.
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Node with only one child or no child.
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Node with two children: Get the inorder successor.
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        # Step 2: Update the height of the ancestor node.
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Step 3: Get the balance factor.
        balance = self.get_balance(root)

        # Step 4: If the node becomes unbalanced, then there are 4 cases.

        # Left Left Case.
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case.
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case.
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left Case.
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        """
        Perform a left rotation on the subtree rooted with z.
        """
        y = z.right
        T2 = y.left

        # Perform rotation.
        y.left = z
        z.right = T2

        # Update heights.
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # Return the new root.
        return y

    def right_rotate(self, y):
        """
        Perform a right rotation on the subtree rooted with y.
        """
        x = y.left
        T2 = x.right

        # Perform rotation.
        x.right = y
        y.left = T2

        # Update heights.
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        # Return the new root.
        return x

    def get_height(self, root):
        """
        Get the height of the node.
        """
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        """
        Get the balance factor of the node.
        """
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        """
        Get the node with the smallest key.
        """
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def pre_order(self, root):
        """
        Pre-order traversal of the tree.
        """
        if not root:
            return []
        result = [root.key]
        result.extend(self.pre_order(root.left))
        result.extend(self.pre_order(root.right))
        return result


# Example usage:
if __name__ == "__main__":
    tree = AVLTree()
    root = None
    keys = [10, 20, 30, 40, 50, 25]

    for key in keys:
        root = tree.insert(root, key)

    print("Pre-order traversal of the constructed AVL tree is:")
    print(tree.pre_order(root))

    root = tree.delete(root, 10)
    print("Pre-order traversal after deletion of 10:")
    print(tree.pre_order(root))
