class Node:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0, 'black')  # Sentinel node representing all leaves
        self.root = self.TNULL

    def insert(self, key):
        """
        Insert a key into the Red-Black Tree and balance the tree.
        """
        node = Node(key)
        node.left = self.TNULL
        node.right = self.TNULL

        parent = None
        current = self.root

        while current != self.TNULL:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        node.color = 'red'
        self._fix_insert(node)

    def _fix_insert(self, k):
        """
        Fix the Red-Black Tree after an insertion.
        """
        while k != self.root and k.parent.color == 'red':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self._right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self._left_rotate(k.parent.parent)
        self.root.color = 'black'

    def delete(self, key):
        """
        Delete a key from the Red-Black Tree and balance the tree.
        """
        node = self._search_tree(self.root, key)
        if node == self.TNULL:
            return False

        self._delete_node(node)
        return True

    def _delete_node(self, node):
        """
        Delete a node from the tree.
        """
        y = node
        y_original_color = y.color
        if node.left == self.TNULL:
            x = node.right
            self._rb_transplant(node, node.right)
        elif node.right == self.TNULL:
            x = node.left
            self._rb_transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._rb_transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._rb_transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == 'black':
            self._fix_delete(x)

    def _fix_delete(self, x):
        """
        Fix the Red-Black Tree after a deletion.
        """
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self._left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self._right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self._right_rotate(x.parent)
                    w = x.parent.left

                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self._left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    def _left_rotate(self, x):
        """
        Perform a left rotation on the subtree rooted with x.
        """
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """
        Perform a right rotation on the subtree rooted with x.
        """
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def _rb_transplant(self, u, v):
        """
        Replace subtree rooted at node u with subtree rooted at node v.
        """
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """
        Get the node with the minimum key in the subtree rooted at node.
        """
        while node.left != self.TNULL:
            node = node.left
        return node

    def _search_tree(self, node, key):
        """
        Search for a node with a specific key in the tree.
        """
        while node != self.TNULL and key != node.key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def inorder(self):
        """
        Inorder traversal of the tree.
        """

        def _inorder(node):
            return _inorder(node.left) + [node.key] + _inorder(node.right) if node != self.TNULL else []

        return _inorder(self.root)

    def pre_order(self):
        """
        Pre-order traversal of the tree.
        """

        def _pre_order(node):
            return [node.key] + _pre_order(node.left) + _pre_order(node.right) if node != self.TNULL else []

        return _pre_order(self.root)


# Example usage:
if __name__ == "__main__":
    tree = RedBlackTree()
    keys = [20, 15, 25, 10, 5, 1]

    for key in keys:
        tree.insert(key)

    print("Inorder traversal of the constructed Red-Black Tree is:")
    print(tree.inorder())

    print("Pre-order traversal of the constructed Red-Black Tree is:")
    print(tree.pre_order())

    tree.delete(10)
    print("Inorder traversal after deletion of 10:")
    print(tree.inorder())

    tree.delete(20)
    print("Inorder traversal after deletion of 20:")
    print(tree.inorder())
