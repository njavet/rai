

graph = {
        'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
        'Zerind': [('Arad', 75), ('Oradea', 71)],
        'Oradea': [('Zerind', 71), ('Sibiu', 151)],
        'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
        'Timisoara': [('Arad', 118), ('Lugoj', 111)],
        'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
        'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
        'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
        'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
        'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
        'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
        'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
        'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Urziceni', 85), ('Giurgiu', 90)],
        'Giurgiu': [('Bucharest', 90)],
        'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
        'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
        'Eforie': [('Hirsova', 86)],
        'Vaslui': [('Urziceni', 142), ('Lasi', 92)],
        'Lasi': [('Vaslui', 92), ('Neamt', 87)],
        'Neamt': [('Lasi', 87)]
}
