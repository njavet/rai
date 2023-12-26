import itertools
import collections


grid0 = [[3, 4, 0, 2, 9, 8, 7, 0, 1],
        [9, 6, 0, 0, 5, 0, 0, 0, 0],
        [8, 7, 0, 6, 0, 1, 5, 9, 3],
        [1, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 7, 8, 0, 0, 0, 4, 9],
        [5, 0, 8, 0, 0, 0, 1, 0, 6],
        [0, 0, 9, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 0, 7, 2, 0, 1, 5],
        [7, 0, 0, 1, 0, 4, 0, 0, 0]]


grid = [[0, 0, 0, 0, 2, 0, 5, 0, 0],
        [0, 0, 8, 5, 0, 9, 0, 0, 2],
        [0, 4, 0, 3, 8, 0, 1, 9, 0],
        [3, 5, 0, 1, 7, 8, 9, 0, 0],
        [7, 6, 0, 0, 0, 3, 8, 5, 1],
        [8, 0, 9, 0, 0, 0, 4, 7, 3],
        [0, 0, 7, 2, 0, 1, 6, 0, 0],
        [1, 2, 0, 8, 9, 5, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0]]

class Agent:
    def __init__(self):
        self.grid = grid
        self.variables = self.get_variables()

    def get_variables(self):
        variables = []
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    variables.append((i, j))
        return variables

    def get_row(self, i):
        return self.grid[i]

    def get_col(self, j):
        return [row[j] for row in self.grid]

    def get_box(self, i, j):
        if 0 <= i < 3:
            row_ind = [0, 1, 2]
        if 3 <= i < 6:
            row_ind = [3, 4, 5]
        if 6 <= i < 9:
            row_ind = [6, 7, 8]

        if 0 <= j < 3:
            col_ind = [0, 1, 2]
        if 3 <= j < 6:
            col_ind = [3, 4, 5]
        if 6 <= j < 9:
            col_ind = [6, 7, 8]
    
        return [self.grid[ri][ci]
                for (ri, ci) in itertools.product(row_ind, col_ind)]

    def get_free_values(self, i, j):
        row = self.get_row(i)
        col = self.get_col(j)
        box = self.get_box(i, j)
        vals = set(row + col + box)
        return [val for val in range(1, 10) if not val in vals]

    def print_board(self):
        print(' | '.join([str(self.grid[0:3]), str(self.grid[3:6]), str(self.grid[6:])]))

    def solve(self):
        for ind, (i, j) in enumerate(self.variables):
            free_values = self.get_free_values(i, j)
            # solution is certain 
            if len(free_values) == 1:
                self.grid[i][j] = free_values[0]
            # simulation
            else:
                for val in free_values:
                    self._simulate(i, j, ind, val)

    def _simulate(self, i, j, ind, val):
        print('board', self.grid)
        print('root: ', i, j, val)
        self.grid[i][j] = val
        branch = [(i, j)]
        for ii, jj in self.variables[ind+1:]:
            free_values = self.get_free_values(ii, jj)
            if len(free_values) == 1:
                self.grid[ii][jj] = free_values[0]
                branch.append((ii, jj))
            elif len(free_values) == 0:
                print('contradiction at', i, j)
                print('zeroing branch', branch)
                for wi, wj in branch:
                    self.grid[wi][wj] = 0
            else:
                for fv in free_values:
                    self._simulate(ii, jj, ind+1, fv)







    


ag = Agent()
#ag.solve()
def solve_sudoku(board):
    empty = find_empty(board)
    
    # If there are no empty cells, the puzzle is solved
    if not empty:
        return True

    row, col = empty

    # Try filling the empty cell with numbers 1 to 9
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            # If the number is safe, assign it to the cell
            board[row][col] = num

            # Recursively attempt to solve the rest of the puzzle
            if solve_sudoku(board):
                return True

            # If the current assignment does not lead to a solution, backtrack
            board[row][col] = 0

    # If no number can be placed, backtrack to the previous cell
    return False

def find_empty(board):
    # Find the first empty cell (with value 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_safe(board, row, col, num):
    # Check if the number is not present in the row, column, and 3x3 subgrid
    return (
        is_safe_row(board, row, num) and
        is_safe_col(board, col, num) and
        is_safe_box(board, row - row % 3, col - col % 3, num)
    )

def is_safe_row(board, row, num):
    return num not in board[row]

def is_safe_col(board, col, num):
    return all(row[col] != num for row in board)

def is_safe_box(board, start_row, start_col, num):
    return all(
        num not in board[i][start_col:start_col + 3]
        for i in range(start_row, start_row + 3)
    )

if solve_sudoku(grid):
    for row in grid:
        print(row)


"""
AIMA problem solving agents 
 a search problem can be defined as follows:

  - set of initial states
  - initial state
  - goal state
  - available actions for the agent 
  - transition model
  - action cost function

"""
