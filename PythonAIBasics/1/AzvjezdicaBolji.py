from collections import defaultdict

# heuristic = {
# 'Baderna': 25,
# 'Barban': 35,
# 'Buje': 21,
# 'GroĹľnjan': 17,
# 'Kanfanar': 30,
# 'Labin': 35,
# 'Lupoglav': 13,
# 'Medulin': 61,
# 'Motovun': 12,
# 'Opatija': 26,
# 'Pazin': 17,
# 'PoreÄŤ': 32,
# 'Pula': 57,
# 'Rovinj': 40,
# 'Umag': 31,
# 'ViĹˇnjan': 20,
# 'Vodnjan': 47,
# 'Ĺ˝minj': 27,
# 'Buzet': 0,
# }

heuristic = {
'enroll_artificial_intelligence': 17,
'fail_lab': 1,
'complete_lab': 10,
'pass_continuous': 20,
'fail_continuous': 6,
'pass_exam': 1,
'fail_exam': 5,
'pass_course': 0,
'fail_course': 0,
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

states = defaultdict(list)
goal = []
start = ''

closed = []
goal_found = False
parent_node = 0
node = 0

def parser(path):
    global start, goal, states
    f = open(path, 'r')
    s = f.readline()
    s = s.strip('\n')
    start = s
    s = f.readline()
    s = s.strip('\n')
    goal = s.split(" ")
    for l in f:
        l = l.split(':')
        k = l[0]
        l[1] = l[1].strip()
        v =  l[1].split(" ")
        for i in v:
            if i == '':
                states[k].append(('', ''))
                continue
            value = i.split(',')
            states[k].append((value[0], int(value[1]), 0))


parser('C:\\Users\\korisnik\\Desktop\\ai.txt')

open_states = [(start, 0, 0)]

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = ''

    def parent_exists(self):
        if self.parent != '':
            return True;


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

    if(n[0] in goal):
        open_states.append(n)
        break

    for k, v in states.items():
        if k == n[0]:
            for i in range(len(v)):
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
while(new_node.parent_exists()):
    output.insert(0, new_node.parent.name)
    for state in states[new_node.parent.name]:
        if state[0] == new_node.name:
            cost +=state[1]
    new_node = new_node.parent
    depth +=1

print(len(closed))
print(output)
print (depth)
print(cost)
print(closed)





