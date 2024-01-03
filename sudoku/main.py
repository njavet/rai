import copy
import time

import grid
import solver
import sudoku

# grid 55 takes 69175316 assignments with bruteforce backtracking
# grid 55 takes 45267 assignments with mrv instead of greedy

grid_dix = grid.get_grid_dict()

g = grid_dix[6]
s0 = solver.BackTrack(copy.deepcopy(g))
s1 = sudoku.Sudoku(copy.deepcopy(g))
s1.solve()
print(s1.n_ass)
grid.print_grid(s1.to_grid(s1.ass))


def time_solvers():
    for i, g in grid_dix.items():
        name = 'grid' + str(i)
        s0 = solver.BackTrack(copy.deepcopy(g))
        s1 = sudoku.Sudoku(copy.deepcopy(g))
        start_time = time.time()
        s0.solve()
        end_time = time.time()
        t0 = end_time - start_time

        start_time = time.time()
        s1.solve()
        end_time = time.time()
        t1 = end_time - start_time
        print(name, 't0 = ', t0, 't1 = ', t1)

#time_solvers()