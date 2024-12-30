import string


class BackTrack:
    def __init__(self, grid):
        self.grid = grid
        self.n_ass = 0
        self.n_bt = 0

    def get_zero_element_greedy(self):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    return i, j

    def mrv(self):
        lst = []
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    nfv = len(self.get_free_values(i, j))
                    lst.append((i, j, nfv))
        try:
            lst = sorted(lst, key=lambda t: (t[2], t[0], t[1]))
            # print([(string.ascii_uppercase[0:9][ii] + str(jj), kk) for ii, jj, kk in lst])
            i, j = lst[0][0:2]
            return i, j
        except IndexError:
            pass

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
        self.n_bt += 1
        try:
            i, j = self.mrv()
            print(string.ascii_uppercase[0:9][i] + str(j))
        except TypeError:
            return True

        # only the previously assigned value gets removed from the free values list
        # while with AC3 we have potentially more values removed
        values = self.get_free_values(i, j)
        for val in values:
            self.grid[i][j] = val
            self.n_ass += 1

            if self.solve():
                return True

            self.grid[i][j] = 0

