from rich.text import Text
from rich.console import Console
import random
import itertools

import agent



class World:
    def __init__(self, ag, aima=False):
        self.grid = None
        self.wumpus_alive = True
        self.agent_alive = True
        self.agent = ag
        self.construct_world(aima)

    def construct_world(self, aima):
        if aima:
            self.grid = [['A', 'B', 'P', 'B'],
                         ['S', '0', 'B', '0'],
                         ['W', 'GSB', 'P', 'B'],
                         ['S', '0', 'B', 'P']]
            return
        cells = list(itertools.product([0, 1, 2, 3], repeat=2))
        self.grid = [['0', '0', '0', '0'],
                     ['0', '0', '0', '0'],
                     ['0', '0', '0', '0'],
                     ['0', '0', '0', '0']]
        self.grid[0][0] = 'A'
        # delete agent location
        del cells[0]
        # wumpus position
        wi, wj = random.choice(cells)
        del cells[cells.index((wi, wj))]
        self.grid[wi][wj] = 'W'
        # gold position
        gi, gj = random.choice(cells)
        del cells[cells.index((gi, gj))]
        # smelly state around wumpus
        self.grid[gi][gj] = 'G'
        # pits
        self.assign_state(wi, wj, 'S')
        for i, j in cells:
            if random.random() <= 0.2:
                # breeze around pit
                self.grid[i][j] = 'P'
                self.assign_state(i, j, 'B')

    @staticmethod
    def get_neighbor_cells(i, j):
        cells = []
        if i < 3:
            # up
            cells.append((i + 1, j))
        if 0 < i:
            # down
            cells.append((i - 1, j))
        if j < 3:
            # right
            cells.append((i, j + 1))
        if 0 < j:
            # left
            cells.append((i, j - 1))
        assert(2 <= len(cells) <= 4)
        return cells

    def assign_state(self, i, j, state):
        cells = self.get_neighbor_cells(i, j)
        for ci, cj in cells:
            if self.grid[ci][cj] == 'W' or self.grid[ci][cj] == 'P':
                return
            if self.grid[ci][cj] == '0':
                self.grid[ci][cj] = state
            elif state not in self.grid[ci][cj]:
                self.grid[ci][cj] += state

    def print_board(self):
        console = Console()
        console.print('-------------------------')
        ai, aj = self.agent.location
        for i, row in enumerate(self.grid):
            t = Text('| ')
            for j, cell in enumerate(row):
                if cell == 'W' or cell == 'P':
                    t.append(cell.rjust(3), style='red')
                elif 'B' in cell or 'S' in cell:
                    t.append(cell.rjust(3), style='yellow')
                else:
                    t.append(cell.rjust(3))
                t.append(' | ')
            console.print(t)
            console.print('-------------------------')

    def construct_percept(self):
        bump = False
        i, j = self.agent.location
        if self.agent.location[0] < 0:
            self.agent.location = 0, j
            bump = True
        if i > 3:
            self.agent.location = 3, j
            bump = True
        if j < 0:
            self.agent.location = i, 0
            bump = True
        if j > 3:
            self.agent.location = i, 3
            bump = True
        if 'S' in self.grid[i][j]:
            percepts = ['S']
        else:
            percepts = [None]
        if 'B' in self.grid[i][j]:
            percepts.append('B')
        else:
            percepts.append(None)
        if 'G' in self.grid[i][j]:
            percepts.append('G')
        else:
            percepts.append(None)
        if bump:
            percepts.append('H')
        else:
            percepts.append(None)
        if self.wumpus_alive:
            percepts.append(None)
        else:
            percepts.append('D')
        return percepts

    def is_agent_dead(self):
        ai, aj = self.agent.location
        if self.grid[ai][aj] == 'W' or self.grid[ai][aj] == 'P':
            return True
        else:
            return False

    def start_game(self):
        turns = 0
        while self.agent_alive:
            if turns == 4:
                return
            percepts = self.construct_percept()
            i, j = self.agent.location
            print('percepts at ', i, j, percepts)
            if self.is_agent_dead():
                print(self.agent.name + ' died!')
                return
            self.agent.agent_program(percepts)
            turns += 1
            print('kb at ', turns)
            for s in self.agent.kb.sentences:
                print(s)


a = agent.Agent()
world = World(a, aima=True)
world.print_board()
world.start_game()
world.print_board()
