class Board:

    def __init__(self):
        self.grid = [[" "] * 3 for _ in range(3)]

    def display(self):
        for i, row in enumerate(self.grid):
            print(" | ".join(row))
            if i < 2:
                print("- " * 5)

    def make_move(self, x, y, mark):
        if self.grid[x][y] == " ":
            self.grid[x][y] = mark
            return True
        return False

    def is_full(self):
        for row in self.grid:
            if " " in row:
                return False
        return True

    def check_winner(self, mark):
        # Check rows
        for row in self.grid:
            if all(cell == mark for cell in row):
                return True
        # Check columns
        for col in range(3):
            if all(self.grid[row][col] == mark for row in range(3)):
                return True
        # Check top-left to bottom-right diagonal
        if all(self.grid[i][i] == mark for i in range(3)):
            return True
        # Check the bottom-left to top-right diagonal
        if all(self.grid[i][3-i-1] == mark for i in range(3)):
            return True
        return False


class Player:

    current_mark = 1

    def __init__(self, name):
        self.name = name
        self.mark = "X" if Player.current_mark else "0"
        Player.current_mark = 1 - Player.current_mark  # Toggle


class Game:

    def __init__(self, players):
        self.board = Board()
        self.players = players[:2]
        self.current_turn = 0

    def _switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def _get_move(self):
        player = self.players[self.current_turn]
        x, y = map(int, input(f"{player.name} ({player.mark}), enter your move (row and column): ").split())
        return x, y

    def play(self):
        while True:
            self.board.display()
            player = self.players[self.current_turn]
            x, y = self._get_move()
            if self.board.make_move(x, y, player.mark):
                if self.board.check_winner(player.mark):
                    self.board.display()
                    print(f"{player.name} won!")
                    break
                if self.board.is_full():
                    self.board.display()
                    print("Draw!")
                    break
                self._switch_turn()
            else:
                print("Invalid move, try again!")


def main():
    player1 = Player("Mark")
    player2 = Player("John")
    game = Game([player1, player2])
    game.play()


if __name__ == "__main__":
    main()
