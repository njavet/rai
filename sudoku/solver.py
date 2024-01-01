
class BackTrack:
    def __init__(self, grid):
        self.grid = grid
        self.steps = 0

    def get_zero_element_greedy(self):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    return i, j

    def mrv(self):
        fv = 9
        r, c = 0, 0
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    nfv = len(self.get_free_values(i, j))
                    if nfv < fv:
                        fv = nfv
                        r = i
                        c = j
        return r, c

    def is_safe(self, i, j, val):
        rs = i - i % 3
        cs = j - j % 3
        if val in self.grid[i]:
            return False
        if val in [row[j] for row in self.grid]:
            return False
        for ii in range(rs, rs+3):
            for jj in range(cs, cs+3):
                if val == self.grid[ii][jj]:
                    return False
        return True

    def get_free_values(self, i, j):
        rs = i - i % 3
        cs = j - j % 3
        row = self.grid[i]
        col = [row[j] for row in self.grid]
        box = []
        for ii in range(rs, rs+3):
            for jj in range(cs, cs+3):
                box.append(self.grid[ii][jj])
        values = set(row + col + box)
        return [n for n in range(1, 10) if n not in values]


    def solve(self):
        try:
            # i, j = self.get_zero_element_greedy()
            i, j = self.mrv()
        except TypeError:
            return True

        values = [val for val in range(1, 10) if self.is_safe(i, j, val)]
        for val in values:
            self.grid[i][j] = val
            self.steps += 1

            if self.solve():
                return True

            self.grid[i][j] = 0
