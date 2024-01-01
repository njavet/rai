
class BruteForceBackTracking:
    def __init__(self, grid):
        self.grid = grid

    def get_zero_element_greedy(self):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    return i, j

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

    def solve(self):
        try:
            i, j = self.get_zero_element_greedy()
        except TypeError:
            return True

        values = [val for val in range(1, 10) if self.is_safe(i, j, val)]
        for val in values:
            self.grid[i][j] = val

            if self.solve():
                return True

            self.grid[i][j] = 0
