import queue
import collections


def is_valid_state(state):
    # cannibals outnumber missionaries on the left side
    if 0 < state[0] < state[1]:
        return False

    # cannibals outnumber missionaries on the right side 
    if state[0] < 3 and state[0] > state[1]:
        return False
    
    if 0 <= state[0] <= 3 and 0 <= state[1] <= 3 and state[2] in [0, 1]:
        return True
    else:
        return False

def is_goal_state(state):
    if state == (0, 0, 0):
        return True
    else:
        return False


moves = [(2, 0, 1), (1, 1, 1), (0, 2, 1), (1, 0, 1), (0, 1, 1)]

start_state = (3, 3, 1)
visited = [start_state]
v = [start_state]
path = []
nodes = [start_state]
n2 = [start_state]


def backtrack(state, visited):
    if is_goal_state(state):
        print('solution found:', state)
        return True

    for move in moves:
        if state[2]:
            new_state = (state[0] - move[0], state[1] - move[1], 0)
        else:
            new_state = (state[0] + move[0], state[1] + move[1], 1)
        nodes.append(new_state)
        
        if not is_valid_state(new_state):
            continue

        if new_state in visited:
            continue

        visited.append(new_state)

        if backtrack(new_state, visited):
            path.append(new_state)
            return True


    return False

def bfs(state, visited):
    if is_goal_state(state):
        print('solution found:', state)
        return True

    level = []
    
    for move in moves:
        if state[2]:
            new_state = (state[0] - move[0], state[1] - move[1], 0)
        else:
            new_state = (state[0] + move[0], state[1] + move[1], 1)
        n2.append(new_state)

        if new_state in visited:
            continue

        if not is_valid_state(new_state):
            continue
        
        level.append(new_state)
        visited.append(new_state)

    for s in level:
        if bfs(s, visited):
            return True






def breath_first_search(node):
    q = [node]
    #q = queue.Queue()
    #q.put(node)

    path = collections.defaultdict(list)
    # for grapsh
    visited = []

    expanded = 0
    while q:
        node = q.pop()
        expanded += 1
        # for graphs
        visited.append(node)
        if is_goal_state(node):
            #print('expanded', expanded)
            path[node] = []
            #for n, c in path.items():
                #print('node', n, 'children', c)
            return node

        for move in moves:
            if node[2] == 1:
                new_node = (node[0] - move[0], node[1] - move[1], 0)
            else:
                new_node = (node[0] + move[0], node[1] + move[1], 1)
            if is_valid_state(new_node) and new_node not in visited:
                path[node].append(new_node)
                q.append(new_node)

        print('expanded', expanded,
              'quue', q)
    
    return path

    
    
backtrack(start_state, visited)
print(len(nodes))
bfs(start_state, v)
print(len(n2))
path = breath_first_search(start_state)
print(path)

