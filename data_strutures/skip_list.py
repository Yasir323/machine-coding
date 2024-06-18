import random


class SkipNode:
    def __init__(self, key=None, value=None, level=0):
        self.key = key             # Key of the node (used for sorting and searching)
        self.value = value         # Value associated with the key
        self.forward = [None] * (level + 1)   # Array to hold references to the next nodes at each level


class SkipList:
    def __init__(self, max_levels=16):
        self.max_levels = max_levels    # Maximum number of levels in the skip list
        self.header = SkipNode()        # Header node with key-value None, acting as the entry point
        self.level = 0                  # Current level of the skip list (starts from 0)
        self.header.forward = [None] * (max_levels + 1)   # Initialize forward references of header

    def random_level(self):
        """
        Generate a random level for a new node.

        :return: Random level, ensuring higher levels are less likely.
        """
        level = 0
        while random.random() < 0.5 and level < self.max_levels:
            level += 1
        return level

    def insert(self, key, value):
        """
        Insert a key-value pair into the skip list.

        :param key: Key to be inserted.
        :param value: Value associated with the key.
        """
        update = [None] * (self.max_levels + 1)   # Initialize update array to None
        current = self.header

        # Traverse from top level to bottom level
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        # Move to next level
        current = current.forward[0]

        # If key is already present, update its value
        if current and current.key == key:
            current.value = value
        else:
            new_level = self.random_level()

            # If new level is greater than current level, update update array
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level

            # Create new node with random level
            new_node = SkipNode(key, value, new_level)

            # Update forward references of new node
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def search(self, key):
        """
        Search for a key in the skip list and return its associated value if found.

        :param key: Key to be searched.
        :return: Associated value if key is found, else None.
        """
        current = self.header

        # Traverse from top level to bottom level
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]

        # If key is found, return its value
        if current and current.key == key:
            return current.value
        else:
            return None

    def delete(self, key):
        """
        Delete a key-value pair from the skip list.

        :param key: Key to be deleted.
        """
        update = [None] * (self.max_levels + 1)   # Initialize update array to None
        current = self.header

        # Traverse from top level to bottom level
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # If key is found, delete the node
        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Remove levels with no elements
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
        else:
            print(f"Key '{key}' not found in skip list")

    def display(self):
        """
        Display the skip list level by level.
        """
        print("Skip List:")
        for level in range(self.level + 1):
            print(f"Level {level}: ", end=" ")
            node = self.header.forward[level]
            while node:
                print(f"({node.key}: {node.value})", end=" ")
                node = node.forward[level]
            print()


if __name__ == "__main__":
    skip_list = SkipList()

    # Insert elements into the skip list
    skip_list.insert(10, "A")
    skip_list.insert(20, "B")
    skip_list.insert(15, "C")
    skip_list.insert(5, "D")

    # Display the skip list
    skip_list.display()

    # Search for elements in the skip list
    print("Search Results:")
    print("Key 15:", skip_list.search(15))  # Expected output: C
    print("Key 30:", skip_list.search(30))  # Expected output: None

    # Delete elements from the skip list
    skip_list.delete(20)
    skip_list.delete(5)
    skip_list.delete(25)  # Element not in the skip list

    # Display the skip list after deletion
    skip_list.display()
