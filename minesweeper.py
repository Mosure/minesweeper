from random import randrange
import re


class Cell:
    def __init__(self, x, y):
        """
        Value of -1 is a mine
        Value greater than -1 is the number of spaces to the nearest mine
        """
        self.x = x
        self.y = y

        self.value = 0
        self.is_hidden = True
        self.flagged = False
    
    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def __str__(self):
        if self.is_hidden:
            return '-'
        
        if self.get_value() == -1:
            return 'x'

        return str(self.get_value())

class Board:
    def __init__(self, m, n, mine_count):
        """
        m - rows (x)
        n - columns (y)

        Board size: m x n (indexed by (x, y))
        """
        self.m = m
        self.n = n
        self.mine_count = mine_count

        self.cells = [[Cell(x, y) for y in range(n)] for x in range(m)]

        self.add_mines()
        self.calculate_mine_neighbors()

    def in_range(self, x, y):
        """
        Check if coordinate is on board
        """
        return x >= 0 and x < self.m and y >= 0 and y < self.n

    def get_neighbors(self, x, y):
        """
        Get the neighbors that are in a '+' formation around the provided cell
        """
        neighbors = []

        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.in_range(i, j):
                    if (i == x) != (j == y):
                        neighbors.append(self.cells[i][j])
        
        return neighbors

    def add_mines(self):
        """
        Fill the board with mines randomly
        """
        for i in range(self.mine_count):
            x = randrange(self.m)
            y = randrange(self.n)

            self.cells[x][y].set_value(-1)
    
    def calculate_mine_neighbors(self):
        """
        Generate number of mines around each open cell
        """
        for x in range(self.m):
            for y in range(self.n):
                if self.cells[x][y].get_value() != -1:
                    neighbors = self.get_neighbors(x, y)

                    mine_count = 0
                    for neighbor in neighbors:
                        if neighbor.get_value() == -1:
                            mine_count += 1
                    
                    self.cells[x][y].set_value(mine_count)
    
    def visit_cell(self, x, y):
        """
        Recursively visit cells (stop if we see a mine or have already visited)
        """
        if self.cells[x][y].get_value() == -1:
            return False
        
        if not self.cells[x][y].is_hidden:
            return True

        self.cells[x][y].is_hidden = False

        neighbors = self.get_neighbors(x, y)

        for neighbor in neighbors:
            self.visit_cell(neighbor.x, neighbor.y)

        return True
    
    def all_cells_complete(self):
        """
        Check if all cells have been visited or flagged
        """
        complete = True
        for x in range(self.m):
            for y in range(self.n):
                complete &= not self.cells[x][y].is_hidden or self.cells[x][y].flagged

def display_board(board):
    """
    Clear the console and print the new board
    """
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')

    for x in range(board.m):
        print(', '.join(map(lambda cell: str(cell), board.cells[x])))

def get_input(board):
    """
    Get the coordinate input for the next cell to visit

    TODO: Allow an option to quit the game
    TODO: Allow an option to flag a cell
    """
    coordinates = ""

    while True:
        coordinates = input("Enter coordinates (x, y): ")

        valid = re.match("[0-9]*,[0-9]*", coordinates)

        if valid:
            split = coordinates.split(",")
            (x, y) = (int(split[0]), int(split[1]))

            if x >= 0 and x < board.m and y >= 0 and y < board.n:
                return (x, y)

# Initialize the board of size 10x10 with 50 mines
board = Board(40, 40, 800)

# Game loop
playing = True
while playing:
    display_board(board)
    (x, y) = get_input(board)

    # If we click a mine directly, we lose
    if not board.visit_cell(x, y):
        print("You lost!")
        playing = False
        exit(0)
    
    # If we run out of items to flag or visit the game ends
    playing = not board.all_cells_complete()

# TODO: Check if the player won or lost via flags
# Note: If there are flags on open spaces the player loses
print("You won!")
