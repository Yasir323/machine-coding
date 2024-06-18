class BinaryHeap:
    def __init__(self):
        self.heap = []

    def insert(self, key):
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def delete_min(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent_index]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        smallest = index
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        if left_index < len(self.heap) and self.heap[left_index] < self.heap[smallest]:
            smallest = left_index
        if right_index < len(self.heap) and self.heap[right_index] < self.heap[smallest]:
            smallest = right_index
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def get_min(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    def size(self):
        return len(self.heap)

    def display(self):
        print(self.heap)


def heap_sort(arr):
    heap = BinaryHeap()
    for elem in arr:
        heap.insert(elem)
    sorted_arr = []
    while heap.size() > 0:
        sorted_arr.append(heap.delete_min())
    return sorted_arr


if __name__ == "__main__":
    bh = BinaryHeap()
    bh.insert(3)
    bh.insert(1)
    bh.insert(6)
    bh.insert(5)
    bh.insert(2)
    bh.insert(4)

    print("Binary Heap:")
    bh.display()

    print("Minimum element:", bh.get_min())

    print("Deleting minimum element:", bh.delete_min())
    bh.display()

    arr = [3, 1, 6, 5, 2, 4]
    print("Original array:", arr)

    sorted_arr = heap_sort(arr)
    print("Sorted array:", sorted_arr)
