import collections


class TreeNode:

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Tree:

    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
            return
        queue = [self.root]
        while queue:
            curr = queue.pop(0)
            if not curr.left:
                curr.left = TreeNode(val)
                break
            else:
                queue.append(curr.left)
            if not curr.right:
                curr.right = TreeNode(val)
                break
            else:
                queue.append(curr.right)

    def get_height(self):

        def height(node):
            if self.root is None:
                return 0
            else:
                lheight = height(node.left)
                rhright = height(node.right)
                return max(lheight, rhright) + 1

        return height(self.root)

    def display(self):
        pass

    def search(self, val):

        def search_recursively(node, val):
            if node.val == val:
                return node
            left = search_recursively(node.left, val)
            if left:
                return left
            right = search_recursively(node.right, val)
            if right:
                return right

        return search_recursively(self.root, val)

    def delete(self, val):
        if self.root is None:
            return
        if self.root.left is None and self.root.right is None:
            if self.root.val == val:
                return self.root
            else:
                return
        key_node, temp, last = None, None, None
        queue = [self.root]
        while queue:
            temp = queue.pop(0)
            if temp.val == val:
                key_node = temp
            if temp.left:
                last = temp
                queue.append(temp.left)
            if temp.right:
                last = temp
                queue.append(temp.right)

        if key_node:
            key_node.val = temp.val
            if last.right == temp:
                last.right = None
            else:
                last.left = None
        del temp

    def in_order(self):

        def _inorder(curr):
            if not curr:
                return
            _inorder(curr.left)
            print(curr.val)
            _inorder(curr.right)

        _inorder(self.root)

    def pre_order(self):

        def _preorder(curr):
            if not curr:
                return
            print(curr.val)
            _preorder(curr.left)
            _preorder(curr.right)

        _preorder(self.root)

    def post_order(self):

        def _postorder(curr):
            if not curr:
                return
            _postorder(curr.left)
            _postorder(curr.right)
            print(curr.val)

        _postorder(self.root)

    def level_order(self):
        if not self.root:
            return
        queue = [self.root]
        while queue:
            curr = queue.pop(0)
            print(curr.val)
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)

    def zig_zag_traversal(self):
        if not self.root:
            return
        tree = collections.defaultdict(list)
        queue = [(self.root, 1)]
        while queue:
            curr, level = queue.pop(0)
            tree[level].append(curr.val)
            level += 1
            if curr.left:
                queue.append((curr.left, level))
            if curr.right:
                queue.append((curr.right, level))
        result = []
        for level, values in tree.items():
            if level % 2 == 1:
                result.extend(values)
            else:
                result.extend(values[::-1])
        return result
