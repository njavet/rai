# S = (M, C, B) number of missionaries, cannibals and boats on the left bank

class State:
    """ factored state """
    def __init__(self, left_m, left_c, boat, right_m, right_c):
        self.left_m = left_m
        self.left_c = left_c 
        self.boat = boat
        self.right_m = right_m
        self.right_c = right_c

    def is_valid(self):
        cond0 = self.left_m < self.left_c and self.left_m > 0
        cond1 = self.right_m < self.right_c and self.right_m > 0
        return not (cond0 or cond1)

    def is_goal(self):
        return self.left_m == 0 and self.left_c == 0 and self.boat == 0


# start state
initial_state = State(3, 3, 1, 0, 0)

# valid moves
moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

class Agent:
    def __init__(self):
        pass
    

