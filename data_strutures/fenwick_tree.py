class FenwickTree:
    def __init__(self, size):
        """
        Initialize a Fenwick Tree with size `size`.

        :param size: The size of the array for which prefix sums need to be calculated.
        """
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index, value):
        """
        Add `value` to the element at `index` (1-indexed) in the Fenwick Tree.

        :param index: Index (1-indexed) where the value needs to be added.
        :param value: Value to be added.
        """
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def prefix_sum(self, index):
        """
        Compute the prefix sum up to `index` (1-indexed) in the Fenwick Tree.

        :param index: Index (1-indexed) up to which prefix sum needs to be calculated.
        :return: Prefix sum up to the given index.
        """
        sum = 0
        while index > 0:
            sum += self.tree[index]
            index -= index & -index
        return sum

    def range_sum(self, left, right):
        """
        Compute the sum of elements in the range [left, right] (1-indexed) in the Fenwick Tree.

        :param left: Left index of the range (1-indexed).
        :param right: Right index of the range (1-indexed).
        :return: Sum of elements in the range [left, right].
        """
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

    def update(self, index, value):
        """
        Update the element at `index` (1-indexed) in the Fenwick Tree to `value`.

        :param index: Index (1-indexed) where the value needs to be updated.
        :param value: New value to be updated.
        """
        current_value = self.range_sum(index, index)
        delta = value - current_value
        self.add(index, delta)


if __name__ == "__main__":
    # Example usage of Fenwick Tree
    ft = FenwickTree(10)

    # Adding elements to the Fenwick Tree
    for i in range(1, 11):
        ft.add(i, i)

    # Computing prefix sums and range sums
    print("Prefix sum up to index 5:", ft.prefix_sum(5))
    print("Range sum from index 2 to 7:", ft.range_sum(2, 7))

    # Updating an element in the Fenwick Tree
    ft.update(5, 10)
    print("Updated prefix sum up to index 5:", ft.prefix_sum(5))
