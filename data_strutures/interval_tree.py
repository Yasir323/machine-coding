class IntervalTreeNode:
    def __init__(self, interval):
        self.interval = interval   # Interval [low, high]
        self.max_high = interval[1]  # Maximum high value of intervals in subtree
        self.left = None           # Left child node
        self.right = None          # Right child node


class IntervalTree:
    def __init__(self):
        self.root = None   # Initialize an empty interval tree

    def insert(self, interval):
        """
        Insert a new interval into the interval tree.

        :param interval: The interval to be inserted, represented as a tuple (low, high).
        """
        self.root = self._insert(self.root, interval)

    def _insert(self, node, interval):
        """
        Recursive function to insert an interval into the interval tree.

        :param node: Current node being processed.
        :param interval: The interval to be inserted, represented as a tuple (low, high).
        :return: Updated node after insertion.
        """
        if node is None:
            return IntervalTreeNode(interval)

        # Compare intervals based on their low endpoints
        if interval[0] < node.interval[0]:
            node.left = self._insert(node.left, interval)
        else:
            node.right = self._insert(node.right, interval)

        # Update the maximum high value in the subtree rooted at 'node'
        if node.max_high < interval[1]:
            node.max_high = interval[1]

        return node

    def delete(self, interval):
        """
        Delete an interval from the interval tree.

        :param interval: The interval to be deleted, represented as a tuple (low, high).
        """
        self.root = self._delete(self.root, interval)

    def _delete(self, node, interval):
        """
        Recursive function to delete an interval from the interval tree.

        :param node: Current node being processed.
        :param interval: The interval to be deleted, represented as a tuple (low, high).
        :return: Updated node after deletion.
        """
        if node is None:
            return None

        # Compare intervals based on their low endpoints
        if interval[0] < node.interval[0]:
            node.left = self._delete(node.left, interval)
        elif interval[0] > node.interval[0]:
            node.right = self._delete(node.right, interval)
        elif interval[1] < node.interval[1]:
            node.left = self._delete(node.left, interval)
        elif interval[1] > node.interval[1]:
            node.right = self._delete(node.right, interval)
        else:
            # Node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Node has two children
                successor = self._find_min(node.right)
                node.interval = successor.interval
                node.right = self._delete(node.right, successor.interval)

        # Update the maximum high value in the subtree rooted at 'node'
        if node:
            node.max_high = max(node.interval[1], self._get_max_high(node.left), self._get_max_high(node.right))

        return node

    def _find_min(self, node):
        """
        Helper function to find the minimum interval in the subtree rooted at 'node'.

        :param node: Root of the subtree.
        :return: Node with the minimum interval.
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _get_max_high(self, node):
        """
        Helper function to get the maximum high value in the subtree rooted at 'node'.

        :param node: Root of the subtree.
        :return: Maximum high value in the subtree.
        """
        if node is None:
            return float('-inf')
        return node.max_high

    def overlap_search(self, interval):
        """
        Search for intervals that overlap with the given interval.

        :param interval: The interval to search for overlaps, represented as a tuple (low, high).
        :return: List of intervals that overlap with the given interval.
        """
        result = []
        self._overlap_search(self.root, interval, result)
        return result

    def _overlap_search(self, node, interval, result):
        """
        Recursive function to search for intervals that overlap with the given interval.

        :param node: Current node being processed.
        :param interval: The interval to search for overlaps, represented as a tuple (low, high).
        :param result: List to store intervals that overlap with the given interval.
        """
        if node is None:
            return

        # Check if 'node.interval' overlaps with 'interval'
        if self._do_overlap(node.interval, interval):
            result.append(node.interval)

        # If left child's maximum high value is greater than 'interval[0]', go to left subtree
        if node.left is not None and node.left.max_high >= interval[0]:
            self._overlap_search(node.left, interval, result)

        # Otherwise, search in the right subtree
        self._overlap_search(node.right, interval, result)

    def _do_overlap(self, interval1, interval2):
        """
        Helper function to check if two intervals overlap.

        :param interval1: First interval represented as a tuple (low, high).
        :param interval2: Second interval represented as a tuple (low, high).
        :return: True if intervals overlap, False otherwise.
        """
        return interval1[0] <= interval2[1] and interval2[0] <= interval1[1]

    def inorder_traversal(self):
        """
        Perform an inorder traversal of the interval tree and print intervals in sorted order.
        """
        self._inorder_traversal(self.root)

    def _inorder_traversal(self, node):
        """
        Recursive function to perform inorder traversal of the interval tree.

        :param node: Current node being processed.
        """
        if node is None:
            return
        self._inorder_traversal(node.left)
        print(f"Interval: [{node.interval[0]}, {node.interval[1]}], Max High: {node.max_high}")
        self._inorder_traversal(node.right)


if __name__ == "__main__":
    it = IntervalTree()

    intervals = [(15, 20), (10, 30), (17, 19), (5, 20), (12, 15), (30, 40)]

    # Insert intervals into interval tree
    for interval in intervals:
        it.insert(interval)
