import copy
import timeit
import time

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

g = grid_dix[6]
s0 = solver.BackTrack(copy.deepcopy(g))
s1 = sudoku.Sudoku(copy.deepcopy(g))
s1.solve()


def time_functions():
    for i, g in grid_dix.items():
        name = 'grid' + str(i)
        print(name)
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

        dix0 = {'name': name,
               'time': str(t0),
               'assignments': str(s0.n_ass),
               'recursions': str(s0.n_bt)}

        dix1 = {'name': name,
                'time': str(t1),
                'assignments': str(s1.n_ass),
                'recursions': str(s1.n_bt)}

        print('simple', t0)
        print('csp', t1)
        grid.write_solution(name, g, s0.grid, 'solutions.txt')
        grid.write_solution(name, g, s1.to_grid(s1.ass), 'csp_solutions.txt')
        grid.write_info(dix0, 'info.txt')
        grid.write_info(dix1, 'csp_info.txt')

    #s0 = sudoku.Sudoku(grid_dix[0])
    #s0.solve()

