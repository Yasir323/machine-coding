class RopeNode:
    def __init__(self, string):
        self.left = None        # Left child node
        self.right = None       # Right child node
        self.string = string    # String fragment stored in this node
        self.length = len(string)  # Length of the string fragment

    def __str__(self):
        return self.string


class Rope:
    def __init__(self, text=""):
        self.root = None
        if text:
            self.build(text)

    def build(self, text):
        """
        Build the rope from a given string.

        :param text: The string to build the rope from.
        """
        self.root = self._build_helper(text)

    def _build_helper(self, text):
        """
        Helper method to recursively build the rope from a given string.

        :param text: The string to build the rope from.
        :return: Root node of the constructed rope.
        """
        if len(text) <= 8:   # Threshold length to determine leaf nodes
            return RopeNode(text)
        mid = len(text) // 2
        left_text = text[:mid]
        right_text = text[mid:]
        node = RopeNode("")
        node.left = self._build_helper(left_text)
        node.right = self._build_helper(right_text)
        node.string = left_text + right_text
        node.length = len(node.string)
        return node

    def _concatenate(self, node):
        """
        Concatenate the string fragments stored in the subtree rooted at the given node.

        :param node: The root node of the subtree to concatenate.
        :return: Concatenated string.
        """
        if node is None:
            return ""
        if node.left is None and node.right is None:
            return node.string
        left_string = self._concatenate(node.left)
        right_string = self._concatenate(node.right)
        return left_string + right_string

    def concatenate(self):
        """
        Concatenate the entire rope into a single string.

        :return: Concatenated string.
        """
        return self._concatenate(self.root)

    def _split(self, node, index):
        """
        Split the rope at the specified index.

        :param node: The root node of the subtree to split.
        :param index: The index at which to split the rope.
        :return: Tuple containing left and right parts of the split.
        """
        if node is None:
            return ("", "")
        if index == 0:
            return ("", node.string)
        if index >= node.length:
            return (node.string, "")
        if node.left is None and node.right is None:
            return (node.string[:index], node.string[index:])
        if index <= node.left.length:
            left_part, right_part = self._split(node.left, index)
            right_part = left_part + right_part
            left_part = node.string[:index]
        else:
            left_part = node.string[:index]
            right_part = node.string[index:]
        return (left_part, right_part)

    def split(self, index):
        """
        Split the rope at the specified index.

        :param index: The index at which to split the rope.
        :return: Tuple containing left and right parts of the split.
        """
        return self._split(self.root, index)

    def _insert(self, node, index, text):
        """
        Insert the specified text into the rope at the given index.

        :param node: The root node of the subtree to insert into.
        :param index: The index at which to insert the text.
        :param text: The text to insert.
        :return: Root node of the updated subtree.
        """
        if node is None:
            return RopeNode(text)
        if index == 0:
            new_node = RopeNode(text)
            new_node.right = node
            new_node.length = len(new_node.string) + node.length
            return new_node
        if index >= node.length:
            new_node = RopeNode(text)
            node.right = new_node
            node.length += len(new_node.string)
            return node
        if node.left is None and node.right is None:
            new_node = RopeNode(node.string[:index] + text + node.string[index:])
            return new_node
        if index <= node.left.length:
            node.left = self._insert(node.left, index, text)
        else:
            node.right = self._insert(node.right, index - node.left.length, text)
        node.string = node.left.string + node.right.string
        node.length = node.left.length + node.right.length
        return node

    def insert(self, index, text):
        """
        Insert the specified text into the rope at the given index.

        :param index: The index at which to insert the text.
        :param text: The text to insert.
        """
        self.root = self._insert(self.root, index, text)

    def _delete(self, node, index, length):
        """
        Delete a substring from the rope starting at the specified index with given length.

        :param node: The root node of the subtree to delete from.
        :param index: The starting index of the substring to delete.
        :param length: The length of the substring to delete.
        :return: Root node of the updated subtree.
        """
        if node is None:
            return None
        if index >= node.length or length <= 0:
            return node
        if index == 0 and length >= node.length:
            return None
        if node.left is None and node.right is None:
            left_part = node.string[:index]
            right_part = node.string[index + length:]
            return RopeNode(left_part + right_part)
        if index < node.left.length:
            if index + length <= node.left.length:
                node.left = self._delete(node.left, index, length)
            else:
                right_length = index + length - node.left.length
                node.left = self._delete(node.left, index, node.left.length - index)
                node.right = self._delete(node.right, 0, right_length)
        else:
            node.right = self._delete(node.right, index - node.left.length, length)
        node.string = node.left.string + node.right.string
        node.length = node.left.length + node.right.length
        return node

    def delete(self, index, length):
        """
        Delete a substring from the rope starting at the specified index with given length.

        :param index: The starting index of the substring to delete.
        :param length: The length of the substring to delete.
        """
        self.root = self._delete(self.root, index, length)

    def _print_helper(self, node, depth):
        """
        Helper method to recursively print the rope structure.

        :param node: Current node in the traversal.
        :param depth: Current depth in the rope structure.
        """
        if node is None:
            return
        self._print_helper(node.left, depth + 1)
        print("  " * depth + node.string)
        self._print_helper(node.right, depth + 1)

    def print_rope(self):
        """
        Print the entire rope structure.
        """
        self._print_helper(self.root, 0)
