heuristic = {
'Baderna': 25,
'Barban': 35,
'Buje': 21,
'Grožnjan': 17,
'Kanfanar': 30,
'Labin': 35,
'Lupoglav': 35,
'Medulin': 61,
'Motovun': 12,
'Opatija': 26,
'Pazin': 40,
'Poreč': 32,
'Pula': 57,
'Rovinj': 40,
'Umag': 31,
'Višnjan': 20,
'Vodnjan': 47,
'Žminj': 27,
'Buzet': 0,
}

states = {
'Baderna': [('Višnjan', 13, 0), ('Poreč', 14, 0), ('Pazin', 19, 0), ('Kanfanar', 19, 0) ],
'Barban': [('Pula', 28, 0), ('Labin', 15, 0)],
'Buje': [('Umag', 13, 0), ('Grožnjan', 8, 0)],
'Buzet': [('Lupoglav', 15, 0), ('Motovun',18, 0)],
'Grožnjan': [('Buje', 8, 0), ('Motovun', 15, 0), ('Višnjan', 19, 0),],
'Kanfanar': [('Baderna', 19, 0), ('Rovinj', 18, 0), ('Žminj', 6, 0), ('Vodnjan', 29, 0)],
'Labin': [('Barban', 15, 0), ('Lupoglav', 42, 0)],
'Lupoglav': [('Labin', 42, 0), ('Opatija', 29, 0), ('Pazin', 23, 0), ('Buzet', 15, 0)],
'Medulin': [('Pula', 9, 0)],
'Motovun': [('Buzet', 18, 0), ('Grožnjan', 15, 0), ('Pazin', 20, 0)],
'Opatija': [('Lupoglav', 29, 0)],
'Pazin': [('Baderna', 19, 0), ('Motovun', 20, 0), ('Žminj', 17, 0), ('Lupoglav', 23, 0)],
'Poreč': [('Baderna', 14, 0)],
'Pula': [('Vodnjan', 12, 0), ('Barban', 28, 0), ('Medulin', 9, 0)],
'Rovinj': [('Kanfanar', 18, 0)],
'Umag': [('Buje', 13, 0)],
'Višnjan': [('Grožnjan', 19, 0), ('Baderna', 13, 0)],
'Vodnjan': [('Kanfanar', 29, 0), ('Pula', 12, 0)],
'Žminj': [('Kanfanar', 6, 0), ('Pazin', 17, 0)],
}

def luda_rekurzija(parent_node, new_node):
    for c in states[parent_node.name]:
        if new_node.name == c[0]:
            new_node.parent = parent_node
            parent_node.children.append(new_node)
            return True
    if parent_node.children != []:
        for c in parent_node.children:
            luda_rekurzija(c, new_node)
    return False

def tree_heuristic(parent_node):
    if parent_node.children == []:
        return
    for i in states[parent_node.name]:
            print(i[0])
    for c in parent_node.children:
        tree_heuristic(c)


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = ''

    def parent_exists(self):
        if self.parent != '':
            return True;

goal = 'Pula'
start = 'Buzet'

open_states = [(start, 0, 0)]
closed = []
goal_found = False
parent_node = 0
new_node = ''
h_calculated = []

while open_states != []:
    n = open_states.pop(0)
    if n[0] in closed:
        continue
    if (n[0] == start):
        parent_node = node = Node(start)
    else:
        new_node = Node(n[0])
        luda_rekurzija(parent_node, new_node)
    if not (n[0] in closed):
        closed.append(n[0])

    if(n[0] == goal):
        open_states.append(n)
        break

    for k, v in states.items():
        if k == n[0]:
            for i in range(len(v)):
                if heuristic[n[0]] > heuristic[v[i][0]] + n[1]:
                    if v[i][0] not in h_calculated:
                        h_calculated.append(v[i][0])
                        print('[ERR] h({}) > {}: {} > {}'.format(n[0], v[i][0],heuristic[n[0]], heuristic[v[i][0]] + n[1]))
                if n[0] == start:
                    v[i] = (v[i][0], v[i][1], v[i][2] + v[i][1] + n[2] + heuristic[v[i][0]])
                else:
                    v[i] = (v[i][0], v[i][1], v[i][2] + v[i][1] + n[2] + heuristic[v[i][0]] - heuristic[n[0]])
                open_states.append(v[i])
            break
    open_states = sorted(open_states, key= lambda tup: tup[2])
output = [new_node.name]
depth = 1
cost = 0





