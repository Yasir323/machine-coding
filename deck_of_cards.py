import random


class Card:
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    ranks = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "Jack": 11,
        "Queen": 12,
        "King": 13,
        "Ace": 14
    }

    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank:<5} of {self.suit}"


class Deck:

    def __init__(self):
        self.cards = []
        self.initialize_cards()

    def initialize_cards(self):
        self.cards = [
            Card(suit, rank) for suit in Card.suits
            for rank in Card.ranks.keys()
        ]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop(0)

    def reset(self):
        self.initialize_cards()


def main():
    deck = Deck()
    deck.shuffle()

    print("Drawing 5 cards:")
    for _ in range(5):
        print(deck.draw())

    print("\nResetting the deck.")
    deck.reset()
    print(f"Deck has {len(deck.cards)} cards.")


if __name__ == "__main__":
    main()
