from system import homepage
from system import utils


class TicTacToeGrid:
    def __init__(self, grid=None):
        EMPTY_TTT_GRID = [
            ' ', ' ', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' '
        ]

        if grid is None:
            self.grid = EMPTY_TTT_GRID
        else:
            self.grid = grid

    def add_item(self, symbol, position) -> bool:
        cell = self.grid[position]
        if cell != ' ':
            return False
        self.grid[position] = symbol
        return True

    def determine_winner(self):
        WINNING_COMBINATIONS = {
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        }

        for combination in WINNING_COMBINATIONS:
            x = self.grid[combination[0]]
            y = self.grid[combination[1]]
            z = self.grid[combination[2]]

            if x != ' ' and y == x and z == y:
                return x
        for cell in self.grid:
            if cell == ' ':
                break
        else:
            return 'draw'
        return None

    def get_formatted_grid(self):
        return f'The grid is:\n{self.grid[0]} | {self.grid[1]} | {self.grid[2]}\n--+---+--\n{self.grid[3]} | {self.grid[4]} | {self.grid[5]}\n--+---+--\n{self.grid[6]} | {self.grid[7]} | {self.grid[8]}'


def main():
    grid = TicTacToeGrid()
    symbol = 'O'
    while grid.determine_winner() is None:
        print()
        print(f'You are: {symbol}')
        print(grid.get_formatted_grid())
        index = input('Input an index (0-8):\n>')
        try:
            index = int(index)
        except ValueError:
            print('Invalid answer.')
            continue

        if index < 0 or index > 8:
            print('Invalid answer.')
            continue

        if not grid.add_item(symbol, index):
            print('That index is already taken!')

        symbol = 'O' if symbol == 'X' else 'X'
    print(grid.get_formatted_grid())
    if grid.determine_winner() == 'draw':
        print('Draw between O and X!')
    else:
        print(grid.determine_winner() + ' won!')


def launch():
    while True:
        utils.make_choice_box('Tic Tac Toe', ('play tic tac toe', main), anything_else=('quit', homepage.home), form='left')

