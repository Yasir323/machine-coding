class Node:
    def __init__(self, data=None):
        self.data = data   # Initialize the node with data
        self.next = None   # Initialize next as None
        self.prev = None   # Initialize prev as None


class DoublyLinkedList:
    def __init__(self):
        self.head = None   # Initialize an empty doubly linked list
        self.tail = None   # Initialize tail as None

    def is_empty(self):
        """
        Check if the doubly linked list is empty.

        :return: True if the doubly linked list is empty, False otherwise.
        """
        return self.head is None

    def append(self, data):
        """
        Append a new node with the given data at the end of the doubly linked list.

        :param data: The data to be appended.
        """
        new_node = Node(data)   # Create a new node with the given data

        if self.head is None:
            self.head = new_node   # If the list is empty, set the new node as both head and tail
            self.tail = new_node
        else:
            new_node.prev = self.tail   # Set new node's prev to current tail
            self.tail.next = new_node   # Set current tail's next to new node
            self.tail = new_node   # Update tail to new node

    def prepend(self, data):
        """
        Insert a new node with the given data at the beginning of the doubly linked list.

        :param data: The data to be prepended.
        """
        new_node = Node(data)   # Create a new node with the given data

        if self.head is None:
            self.head = new_node   # If the list is empty, set the new node as both head and tail
            self.tail = new_node
        else:
            new_node.next = self.head   # Set new node's next to current head
            self.head.prev = new_node   # Set current head's prev to new node
            self.head = new_node   # Update head to new node

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

        new_node.prev = prev_node   # Set new node's prev to prev_node
        new_node.next = prev_node.next   # Set new node's next to prev_node's next

        if prev_node.next:
            prev_node.next.prev = new_node   # Set next node's prev to new node

        prev_node.next = new_node   # Set prev_node's next to new node

        if prev_node == self.tail:
            self.tail = new_node   # Update tail if prev_node is current tail

    def delete_node(self, key):
        """
        Delete the first occurrence of a node with the given key from the doubly linked list.

        :param key: The data of the node to be deleted.
        """
        current_node = self.head

        while current_node:
            if current_node.data == key:
                if current_node == self.head:
                    self.head = current_node.next   # If key is found at head, move head to next node
                    if self.head:
                        self.head.prev = None   # Set new head's prev to None
                    if current_node == self.tail:
                        self.tail = None   # Set tail to None if list becomes empty
                else:
                    prev_node = current_node.prev
                    next_node = current_node.next
                    if prev_node:
                        prev_node.next = next_node   # Set prev node's next to next node
                    if next_node:
                        next_node.prev = prev_node   # Set next node's prev to prev node
                    if current_node == self.tail:
                        self.tail = prev_node   # Update tail if current node is tail
                current_node = None   # Remove reference to current node
                return

            current_node = current_node.next

    def delete_node_at_position(self, position):
        """
        Delete the node at a specified position in the doubly linked list.

        :param position: The position (index) of the node to be deleted (1-based index).
        """
        if self.head is None or position <= 0:
            return

        current_node = self.head

        if position == 1:
            self.head = current_node.next   # If position is 1, move head to next node
            if self.head:
                self.head.prev = None   # Set new head's prev to None
            if current_node == self.tail:
                self.tail = None   # Set tail to None if list becomes empty
            current_node = None   # Remove reference to current node
            return

        count = 1
        while current_node and count != position:
            current_node = current_node.next
            count += 1

        if current_node is None:
            return

        if current_node == self.tail:
            self.tail = current_node.prev   # Update tail if current node is tail

        if current_node.prev:
            current_node.prev.next = current_node.next   # Set prev node's next to next node

        if current_node.next:
            current_node.next.prev = current_node.prev   # Set next node's prev to prev node

        current_node = None   # Remove reference to current node

    def reverse(self):
        """
        Reverse the doubly linked list.
        """
        temp_node = None
        current_node = self.head

        while current_node:
            temp_node = current_node.prev   # Swap prev and next pointers of the current node
            current_node.prev = current_node.next
            current_node.next = temp_node
            current_node = current_node.prev   # Move to next node

        if temp_node:
            self.head = temp_node.prev   # Update head to new head after reversing

    def print_list(self):
        """
        Print all the elements in the doubly linked list.
        """
        current_node = self.head
        while current_node:
            print(current_node.data, end=" ")
            current_node = current_node.next
        print()

    def print_reverse(self):
        """
        Print all the elements in the doubly linked list in reverse order.
        """
        current_node = self.tail
        while current_node:
            print(current_node.data, end=" ")
            current_node = current_node.prev
        print()
