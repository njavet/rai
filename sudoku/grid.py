import string
from rich.text import Text
from rich.console import Console


def get_grids(fname='sudoku.txt'):
    with open(fname, 'r') as f:
        lines = f.readlines()
    grids = []
    for i in range(1, len(lines), 10):
        grids.append([[int(c) for c in row] for row in lines[i:i+9]])
    return grids


def print_grid(grid):
    console = Console()
    s = Text('   | 0 1 2 | 3 4 5 | 6 7 8 ', style='bold white')
    console.print(s)
    console.print(' ' + 25 * '-')
    for i, row in enumerate(grid):
        a = string.ascii_uppercase[0:9][i]
        t = Text(' ' + a + ' | ', style='bold white')
        for j, val in enumerate(row):
            t.append(str(val) + ' ', style='bold white')
            if j in [2, 5]:
                t.append('| ')
        console.print(t)
        if i in [2, 5]:
            console.print(' ' + 25 * '-')
