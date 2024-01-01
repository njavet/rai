
import grid
import solver
import sudoku

# grid 55 takes 69175316 assignments with bruteforce backtracking
# grid 55 takes 73482 assignments with mrv instead of greedy

grid_dix = grid.get_grid_dict()

s0 = sudoku.Sudoku(grid_dix[54])
s0.backtrack_search()
s0.print_grid()
#s1 = solver.BackTrack(grid_dix[54])
#s1.solve()
#print(s1.steps)

