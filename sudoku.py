import itertools
import collections


grid = [0, 0, 0, 0, 0, 6, 0, 7, 0,
        8, 0, 1, 4, 7, 3, 0, 0, 0,
        7, 0, 0, 0, 0, 1, 9, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 0, 9,
        0, 5, 0, 0, 0, 0, 0, 0, 0,
        9, 0, 0, 5, 0, 8, 0, 0, 4,
        4, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 6, 2, 0, 3, 0, 0, 0, 0,
        0, 0, 0, 2, 0, 0, 4, 0, 0]

sol = [3, 4, 5, 9, 2, 6, 1, 7, 8,
       8, 9, 1, 4, 7, 3, 6, 5, 2,
       7, 2, 6, 8, 5, 1, 9, 4, 3,
       6, 8, 7, 3, 4, 2, 5, 1, 9,
       2, 5, 4, 1, 9, 7, 3, 8, 6,
       9, 1, 3, 5, 6, 8, 7, 2, 4,
       4, 7, 9, 6, 8, 5, 2, 3, 1,
       1, 6, 2, 7, 3, 4, 8, 9, 5,
       5, 3, 8, 2, 1, 9, 4, 6, 7]


class Sudoku:
    def __init__(self, grid):
        self.state = grid

    def extract_row(self, i):
        s = i*9
        return self.state[s: s+9]

    def extract_col(self, j):
        return [self.state_vector[ind] for ind in range(j, 81, 9)]

    def extract_box(self, n):
    a = state_vector[9*n:9*n+3]
    b = state_vector[9*n+9:9*n+9+3]
    c = state_vector[9*n+18:9*n+18+3]
    return a + b + c


    def compute_position_dix(self):
        dix = collections.defaultdict(list)
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                dix[val].append((i, j))
        return dix



    def update_state(self):
        self.zero_cells = {} 
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    self.zero_cells[i, j] = self.get_free_values(i, j)

    def set_cell_value(self, i, j, value):
        self.grid[i][j] = value
        self.update_state()

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

        vals = set(sorted(row + col + box))
        return [val for val in range(1, 10) if not val in vals]


    def is_solved(self):
        return not self.zero_cells

    def print_board(self):
        print(' | '.join([str(self.grid[0:3]), str(self.grid[3:6]), str(self.grid[6:])]))


class Agent:
    def __init__(self):
        self.sudoku = Sudoku(grid)

    def solve(self):
        state0 = self.sudoku.zero_cells
        print('initial state')
        for (i, j), vals in state0.items():
            print('position', i, j, ' values', vals)

        print('position dict')
        for val, lst in self.sudoku.compute_position_dix().items():
            print(val, lst)
        return 

        dix = self.sudoku.get_free_value_dict()
        self.set_unique_cell_values(dix)
        dix2 = self.sudoku.get_free_value_dict()
        while dix != dix2:
            dix = dix2
            self.set_unique_cell_values(dix)
            dix2 = self.sudoku.get_free_value_dict()
        print('step 0 complete')
        


        for solvec in itertools.product(*dix.values()):
            #print('trial', solvec, 'number', trials)
            for ind, (i, j) in enumerate(dix.keys()):
                self.sudoku.set_cell_value(i, j, solvec[ind])
            if self.sudoku.is_solved():
                print('solution after ', trials, ' trials')
                self.sudoku.print_board()
            else:
                trials += 1
                self.sudoku.set_zeros()
        
    def free_value_processing(self):
        state0 = self.sudoku.zero_cells
        for (i, j), values in state0.items():
            if len(values) == 1:
                self.sudoku.set_cell_value(i, j, values[0])
                # print('set value', values[0], ' at ', i, j)

    


ag = Agent()
ag.solve()


#### 
# AIMA problem solving agents 
