class Node:

    def __init__(self, data=None):
        self.data = data   # Initialize the node with data
        self.next = None   # Initialize next as None


class LinkedList:

    def __init__(self):
        self.head = None   # Initialize an empty linked list

    def is_empty(self):
        """
        Check if the linked list is empty.

        :return: True if the linked list is empty, False otherwise.
        """
        return self.head is None

    def append(self, data):
        """
        Append a new node with the given data at the end of the linked list.

        :param data: The data to be appended.
        """
        new_node = Node(data)   # Create a new node with the given data

        if self.head is None:
            self.head = new_node   # If the list is empty, set the new node as the head
            return

        last_node = self.head
        while last_node.next:   # Traverse to the last node
            last_node = last_node.next

        last_node.next = new_node   # Set the next of the last node to the new node

    def prepend(self, data):
        """
        Insert a new node with the given data at the beginning of the linked list.

        :param data: The data to be prepended.
        """
        new_node = Node(data)   # Create a new node with the given data

        new_node.next = self.head   # Set the next of the new node to the current head
        self.head = new_node   # Set the new node as the new head

    @staticmethod
    def insert_after_node(prev_node, data):
        """
        Insert a new node with the given data after a specified node.

        :param prev_node: The node after which the new node is to be inserted.
        :param data: The data to be inserted.
        """
        if not prev_node:
            print("Previous node is not in the list")
            return

        new_node = Node(data)   # Create a new node with the given data

        new_node.next = prev_node.next   # Set the next of the new node to the next of previous node
        prev_node.next = new_node   # Set the next of previous node to the new node

    def delete_node(self, key):
        """
        Delete the first occurrence of a node with the given key from the linked list.

        :param key: The data of the node to be deleted.
        """
        current_node = self.head

        if current_node and current_node.data == key:
            self.head = current_node.next   # If key is found at the head, move head to next node
            current_node = None   # Remove reference to the node
            return

        prev = None
        while current_node and current_node.data != key:
            prev = current_node
            current_node = current_node.next

        if current_node is None:
            return   # Key not present in the list

        prev.next = current_node.next   # Unlink the node from the linked list
        current_node = None   # Remove reference to the node

    def delete_node_at_position(self, position):
        """
        Delete the node at a specified position in the linked list.

        :param position: The position (index) of the node to be deleted (1-based index).
        """
        if self.head is None:
            return

        temp_node = self.head

        if position == 0:
            self.head = temp_node.next
            temp_node = None
            return

        for i in range(position - 1):
            if temp_node is None:
                break
            temp_node = temp_node.next

        if temp_node is None:
            return

        if temp_node.next is None:
            return

        next_node = temp_node.next.next

        temp_node.next = None

        temp_node.next = next_node

    def reverse(self):
        """
        Reverse the linked list.
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next   # Move next to the next node
            current.next = prev   # Reverse current node's pointer to previous node
            prev = current   # Move pointers one position ahead
            current = next_node
        self.head = prev   # Set the new head

    def print_list(self):
        """
        Print all the elements in the linked list.
        """
        current_node = self.head
        while current_node:
            print(current_node.data, end=" ")
            current_node = current_node.next
        print()


if __name__ == "__main__":
    # Create a new linked list
    linked_list = LinkedList()

    # Append elements to the linked list
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)

    # Print the linked list: Expected output: 1 2 3
    linked_list.print_list()

    # Prepend an element to the linked list
    linked_list.prepend(0)

    # Print the linked list after prepend: Expected output: 0 1 2 3
    linked_list.print_list()

    # Insert 5 after node with data 2
    node = linked_list.head.next.next
    linked_list.insert_after_node(node, 5)

    # Print the linked list after insert: Expected output: 0 1 2 5 3
    linked_list.print_list()

    # Delete node with data 1
    linked_list.delete_node(1)

    # Print the linked list after delete: Expected output: 0 2 5 3
    linked_list.print_list()

    # Reverse the linked list
    linked_list.reverse()

    # Print the linked list after reverse: Expected output: 3 5 2 0
    linked_list.print_list()
