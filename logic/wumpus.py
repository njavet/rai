import random
from rich.text import Text
from rich.console import Console
import itertools


class Wumpus:
    def __init__(self, agent):
        self.grid = None
        self.wumpus_alive = True
        self.agent_alive = True
        self.agent = agent

    def construct_world(self):
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
        for row in self.grid:
            t = Text('| ')
            for cell in row:
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

        i, j = self.agent.location
        cells = self.get_neighbor_cells(i, j)
        ps = set()
        for ci, cj in cells:
            for s in self.grid[ci][cj]:
                ps.add(s)
        percepts = []
        if 'S' in ps:
            percepts.append('S')
        else:
            percepts.append('0')
        if 'B' in ps:
            percepts.append('B')
        else:
            percepts.append('0')
        if 'G' in ps:
            percepts.append('G')
        else:
            percepts.append('0')
        if bump:
            percepts.append('bump')
        else:
            percepts.append('0')
        if self.wumpus_alive:
            percepts.append('0')
        else:
            percepts.append('dead')
        return percepts

    def is_agent_dead(self):
        ai, aj = self.agent.location
        if self.grid[ai][aj] == 'W' or self.grid[ai][aj] == 'P':
            return True
        else:
            return False

    def start_game(self):
        while self.agent_alive:
            percepts = self.construct_percept()
            if self.is_agent_dead():
                print(self.agent.name + ' died!')
                return
            self.agent.agent_program(percepts)


class PropKB:
    def __init__(self, sentence=None):
        self.clauses = []
        if sentence:
            self.tell(sentence)

    def tell(self, sentence):
        self.clauses.extend(s)
        self.safe_cells = [(0, 0)]
        self.sentences = []

    def tell(self, sentence):
        self.sentences.append(sentence)

    def ask(self):
        percept = self.sentences[-1]

        pass

    def inference(self):
        pass


class Agent:
    def __init__(self, name):
        self.name = name
        self.performance = 0
        self.direction = 'EAST'
        self.steps = 0
        self.location = (0, 0)
        self.arrow = True
        self.kb = KB()
        self.actions = {0: self.turn_left,
                        1: self.turn_right,
                        2: self.move_forward,
                        3: self.grab_gold,
                        4: self.shoot,
                        5: self.climb_out}

    def turn_left(self):
        self.steps += 1
        if self.direction == 'EAST':
            self.direction = 'NORTH'
        elif self.direction == 'NORTH':
            self.direction = 'WEST'
        elif self.direction == 'WEST':
            self.direction = 'SOUTH'
        elif self.direction == 'SOUTH':
            self.direction = 'EAST'

    def turn_right(self):
        self.steps += 1
        if self.direction == 'EAST':
            self.direction = 'SOUTH'
        elif self.direction == 'NORTH':
            self.direction = 'EAST'
        elif self.direction == 'WEST':
            self.direction = 'NORTH'
        elif self.direction == 'SOUTH':
            self.direction = 'WEST'

    def move_forward(self):
        self.steps += 1
        i, j = self.location
        if self.direction == 'EAST':
            j += 1
        elif self.direction == 'NORTH':
            i += 1
        elif self.direction == 'WEST':
            j -= 1
        elif self.direction == 'SOUTH':
            i -= 1
        self.location = i, j

    def grab_gold(self):
        self.steps += 1

    def shoot(self):
        self.steps += 1
        self.arrow = False

    def climb_out(self):
        self.steps += 1
        # moves out of the world
        self.location = -1, -1

    def agent_program(self, percept):
        sentence = self.make_percept_sentence(percept)
        self.kb.tell(sentence)
        action = self.kb.ask()
        self.actions[action]()

    def make_percept_sentence(self, percept):
        return percept


agent = Agent('Noe')
wumpus = Wumpus(agent)
wumpus.construct_world()
wumpus.print_board()
