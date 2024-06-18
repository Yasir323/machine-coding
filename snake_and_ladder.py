import random
import time
from enum import Enum
from typing import List


class Color(Enum):
    Red = "RED"
    Yellow = "YELLOW"
    Green = "GREEN"
    Blue = "BLUE"


class Snake:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


class Ladder:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


class Die:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def roll():
        return random.randint(1, 6)


class Player:

    def __init__(self, color: Color):
        self.color = color
        self.position = 0

    @staticmethod
    def roll_dice(die: Die) -> int:
        number = die.roll()
        return number

    def move(self, number: int):
        new_position = self.position + number
        if new_position <= 100:
            self.position = new_position

    def __str__(self) -> str:
        return self.color.value

    def __repr__(self) -> str:
        return self.color.value


class Board:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, snakes: List[Snake], ladders: List[Ladder]):
        self.snakes = snakes
        self.ladders = ladders

    def add_ladders(self, ladders: List[Ladder]):
        self.ladders.extend(ladders)

    def add_snakes(self, snakes: List[Snake]):
        self.snakes.extend(snakes)


class Game:

    def __init__(self, board: Board, die: Die, players: List[Player]):
        self.die = die
        self.board = board
        if len(players) != len(set([player.color.value for player in players])):
            raise Exception("2 players cannot have same same color")
        if len(players) > 4:
            raise Exception("There can be no more than 4 players")
        self.players = players[:4]
        self.winner = None

    def start(self):
        while True:
            for player in self.players:
                number = player.roll_dice(self.die)
                player.move(number)
                self._update_position(player)
                if player.position == 100:
                    self.winner = player
                    return
                print(f"{player.color}: {number} -> {player.position}")
                time.sleep(0.5)

    def _update_position(self, player: Player):
        for snake in self.board.snakes:
            if player.position == snake.start:
                player.position = snake.end
                print(f"Snake: {player.color}: {snake.start} -> {snake.end}")
                time.sleep(1)
                return
        for ladder in self.board.ladders:
            if player.position == ladder.start:
                player.position = ladder.end
                print(f"Ladder: {player.color}: {ladder.start} -> {ladder.end}")
                time.sleep(1)
                return

    def get_winner(self):
        return self.winner


def main():
    player1 = Player(Color.Red)
    player2 = Player(Color.Blue)
    players = [player1, player2]
    die = Die()
    snakes = [Snake(s, e) for s, e in zip([34, 40, 56, 78, 90], [12, 23, 17, 42, 8])]
    ladders = [Ladder(s, e) for s, e in zip([3, 13, 55, 75, 66], [45, 33, 99, 81, 88])]
    board = Board(snakes, ladders)
    game = Game(board, die, players)
    game.start()
    print(game.get_winner())


if __name__ == "__main__":
    main()
