class Node:
    def __init__(self, data=None):
        self.data = data   # Initialize the node with data
        self.next = None   # Initialize next as None


class CircularLinkedList:
    def __init__(self):
        self.head = None   # Initialize an empty circular linked list

    def is_empty(self):
        """
        Check if the circular linked list is empty.

        :return: True if the circular linked list is empty, False otherwise.
        """
        return self.head is None

    def append(self, data):
        """
        Append a new node with the given data to the end of the circular linked list.

        :param data: The data to be appended.
        """
        new_node = Node(data)   # Create a new node with the given data

        if self.head is None:
            self.head = new_node   # If the list is empty, set the new node as the head
            self.head.next = self.head   # Point the next of the new node to itself (circular reference)
        else:
            current = self.head
            while current.next != self.head:   # Traverse to the last node
                current = current.next
            current.next = new_node   # Set the next of the last node to the new node
            new_node.next = self.head   # Set the next of the new node to the head (make it circular)

    def prepend(self, data):
        """
        Insert a new node with the given data at the beginning of the circular linked list.

        :param data: The data to be prepended.
        """
        new_node = Node(data)   # Create a new node with the given data

        if self.head is None:
            self.head = new_node   # If the list is empty, set the new node as the head
            self.head.next = self.head   # Point the next of the new node to itself (circular reference)
        else:
            new_node.next = self.head   # Set the next of the new node to the current head

            # Traverse to find the last node to update its next to new node
            current = self.head
            while current.next != self.head:
                current = current.next

            current.next = new_node   # Set the next of the last node to the new node
            self.head = new_node   # Update head to the new node

    def insert_after_node(self, prev_node, data):
        """
        Insert a new node with the given data after a specified node.

        :param prev_node: The node after which the new node is to be inserted.
        :param data: The data to be inserted.
        """
        if not prev_node:
            print("Previous node is not in the list")
            return

        new_node = Node(data)   # Create a new node with the given data

        new_node.next = prev_node.next   # Set new node's next to previous node's next
        prev_node.next = new_node   # Set previous node's next to new node

    def delete_node(self, key):
        """
        Delete a node with the given key from the circular linked list.

        :param key: The data of the node to be deleted.
        """
        if self.head is None:
            return

        if self.head.data == key:
            current = self.head
            while current.next != self.head:   # Find the last node
                current = current.next

            if self.head == self.head.next:   # If only one node is present
                self.head = None
            else:
                current.next = self.head.next   # Skip the head node
                self.head = self.head.next   # Move head to the next node
            return

        current = self.head
        prev_node = None
        while current.next != self.head:
            prev_node = current
            current = current.next
            if current.data == key:
                prev_node.next = current.next   # Skip the current node
                return

        if current.data == key:
            prev_node.next = self.head   # If the last node is to be deleted
            return

    def print_list(self):
        """
        Print all the elements in the circular linked list.
        """
        if self.head is None:
            return

        current = self.head
        while True:
            print(current.data, end=" ")
            current = current.next
            if current == self.head:
                break   # Stop printing when we reach the head again
        print()


if __name__ == "__main__":
    # Create a new circular linked list
    circular_list = CircularLinkedList()

    # Append elements to the circular linked list
    circular_list.append(1)
    circular_list.append(2)
    circular_list.append(3)

    # Print the circular linked list: Expected output: 1 2 3
    circular_list.print_list()

    # Prepend an element to the circular linked list
    circular_list.prepend(0)

    # Print the circular linked list after prepend: Expected output: 0 1 2 3
    circular_list.print_list()

    # Insert 5 after node with data 2
    node = circular_list.head.next.next
    circular_list.insert_after_node(node, 5)

    # Print the circular linked list after insert: Expected output: 0 1 2 5 3
    circular_list.print_list()

    # Delete node with data 1
    circular_list.delete_node(1)

    # Print the circular linked list after delete: Expected output: 0 2 5 3
    circular_list.print_list()
