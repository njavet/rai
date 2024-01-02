import copy
import timeit

import grid
import solver
import sudoku

# grid 55 takes 69175316 assignments with bruteforce backtracking
# grid 55 takes 45267 assignments with mrv instead of greedy

grid_dix = grid.get_grid_dict()

#grid.print_grid(s1.grid)
#s1.solve()
#grid.print_grid(s1.grid)
#print(s1.steps)

for i, g in grid_dix.items():
    print('grid', i)
    #s0 = solver.BackTrack(copy.deepcopy(g))
    s0 = sudoku.Sudoku(copy.deepcopy(g))
    t = timeit.timeit('s0.solve()', setup='from __main__ import s0')
    dix = {'name': 'grid' + str(i),
           'algo': 'csp_backtrack',
           'time': str(t),
           'assignments': str(s0.assignments),
           'recursions': str(s0.n_bt)}
    grid.write_solution(g, s0.to_grid(s0.ass), 'solutions.txt', dix)

#s0 = sudoku.Sudoku(grid_dix[0])
#s0.solve()

