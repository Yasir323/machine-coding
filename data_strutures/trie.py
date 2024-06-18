class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """
        Inserts a word into the trie.
        """
        node = self.root
        for char in word:
            # If the character is not present, add it to the children dictionary.
            if char not in node.children:
                node.children[char] = TrieNode()
            # Move to the next node in the trie.
            node = node.children[char]
        # Mark the end of the word.
        node.is_end_of_word = True

    def search(self, word):
        """
        Searches for a word in the trie.
        Returns True if the word is present, otherwise False.
        """
        node = self.root
        for char in word:
            # If the character is not found, return False.
            if char not in node.children:
                return False
            # Move to the next node in the trie.
            node = node.children[char]
        # Return True if the current node marks the end of the word.
        return node.is_end_of_word

    def starts_with(self, prefix):
        """
        Checks if there is any word in the trie that starts with the given prefix.
        Returns True if there is any such word, otherwise False.
        """
        node = self.root
        for char in prefix:
            # If the character is not found, return False.
            if char not in node.children:
                return False
            # Move to the next node in the trie.
            node = node.children[char]
        # If the prefix is found, return True.
        return True

    def delete(self, word):
        """
        Deletes a word from the trie if it exists.
        """

        def _delete(node, word, depth):
            # Base case: If the end of the word is reached
            if depth == len(word):
                # If the word is not present, return False.
                if not node.is_end_of_word:
                    return False
                # Mark the current node as not the end of the word.
                node.is_end_of_word = False
                # If the current node has no children, it can be deleted.
                return len(node.children) == 0

            char = word[depth]
            # If the character is not found, return False.
            if char not in node.children:
                return False

            # Recur for the child node.
            can_delete_child = _delete(node.children[char], word, depth + 1)

            # If the child can be deleted, remove it from the children dictionary.
            if can_delete_child:
                del node.children[char]
                # Return True if the current node has no other children and is not the end of another word.
                return len(node.children) == 0

            return False

        _delete(self.root, word, 0)

    def display(self):
        """
        Displays all words in the trie.
        """

        def _display(node, word):
            if node.is_end_of_word:
                print(word)
            for char, child_node in node.children.items():
                _display(child_node, word + char)

        _display(self.root, "")


# Example usage:
if __name__ == "__main__":
    trie = Trie()
    words = ["hello", "hell", "heaven", "heavy"]
    for word in words:
        trie.insert(word)

    print("Trie contents:")
    trie.display()

    print("\nSearch for 'hell':", trie.search("hell"))
    print("Search for 'heaven':", trie.search("heaven"))
    print("Search for 'goodbye':", trie.search("goodbye"))

    print("\nWords starting with 'he':", trie.starts_with("he"))
    print("Words starting with 'hea':", trie.starts_with("hea"))
    print("Words starting with 'hello':", trie.starts_with("hello"))
    print("Words starting with 'good':", trie.starts_with("good"))

    print("\nDelete 'hell'")
    trie.delete("hell")
    trie.display()

    print("\nDelete 'heaven'")
    trie.delete("heaven")
    trie.display()

    print("\nDelete 'hello'")
    trie.delete("hello")
    trie.display()
