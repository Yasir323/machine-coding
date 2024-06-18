class XorNode:
    def __init__(self, data=None):
        self.data = data   # Initialize the node with data
        self.npx = 0       # Initialize npx as 0, which will store XOR of previous and next node's addresses


class XorLinkedList:
    def __init__(self):
        self.head = None   # Initialize an empty XOR linked list
        self.tail = None   # Initialize tail as None
        self.node_map = {}  # A dictionary to keep track of node addresses

    def _xor(self, a, b):
        """
        Helper function to compute XOR of two addresses.

        :param a: Address of node a.
        :param b: Address of node b.
        :return: XOR of the two addresses.
        """
        return id(a) ^ id(b) if a and b else id(a) ^ id(b)

    def insert(self, data):
        """
        Insert a new node with the given data at the end of the XOR linked list.

        :param data: The data to be inserted.
        """
        new_node = XorNode(data)
        new_node_address = id(new_node)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.node_map[new_node_address] = None
        else:
            next_address = self._xor(self.tail, None)
            self.node_map[new_node_address] = next_address
            self.tail.npx = self._xor(self.tail.npx, new_node)
            self.tail = new_node
            self.node_map[next_address] = new_node_address

    def delete(self, data):
        """
        Delete the first occurrence of a node with the given data from the XOR linked list.

        :param data: The data of the node to be deleted.
        """
        if self.head is None:
            return

        prev = None
        current = self.head
        prev_address = 0

        while current:
            if current.data == data:
                if prev is None:
                    self.head = self._get_node(self._xor(None, current.npx))
                    if self.head is None:
                        self.tail = None
                    else:
                        self.head.npx = self._xor(None, self._xor(current, self._get_node(self.head.npx)))
                else:
                    prev.npx = self._xor(self._xor(prev.npx, current), self._get_node(self._xor(current.npx, None)))
                    if current == self.tail:
                        self.tail = prev
                del self.node_map[id(current)]
                return
            next_node = self._get_node(self._xor(prev, current.npx))
            prev = current
            current = next_node

    def _get_node(self, address):
        """
        Helper function to get a node by its address.

        :param address: Address of the node.
        :return: Node object.
        """
        for node_address, node in self.node_map.items():
            if id(node) == address:
                return node
        return None

    def print_list(self):
        """
        Print all the elements in the XOR linked list.
        """
        current = self.head
        prev = None
        while current:
            print(current.data, end=" ")
            next_node = self._get_node(self._xor(prev, current.npx))
            prev = current
            current = next_node
        print()


if __name__ == "__main__":
    xor_list = XorLinkedList()

    # Insert elements into the XOR linked list
    xor_list.insert(10)
    xor_list.insert(20)
    xor_list.insert(30)
    xor_list.insert(40)

    print("XOR Linked List after insertions:")
    xor_list.print_list()  # Expected output: 10 20 30 40

    # Delete an element from the XOR linked list
    xor_list.delete(20)
    print("XOR Linked List after deleting 20:")
    xor_list.print_list()  # Expected output: 10 30 40

    # Delete the head element
    xor_list.delete(10)
    print("XOR Linked List after deleting 10:")
    xor_list.print_list()  # Expected output: 30 40

    # Delete the tail element
    xor_list.delete(40)
    print("XOR Linked List after deleting 40:")
    xor_list.print_list()  # Expected output: 30
