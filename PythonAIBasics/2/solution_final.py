# ovaj je potpuno izmjenjen od prijašnjih, ali se bazira na 4 RADI i ispis isto radi
import sys
from collections import defaultdict

verbose = False
goal = ''
i = 0
j = 0
t = 0
k = 0
sos_clauses = False  # sjeti se čemu ovo služi
counter = 1
visited = defaultdict(list)
clauses = []
st_builder = []


def select_clauses(sos):
    global i, j, k, t, sos_clauses, clauses
    for i in range(len(sos)):
        j = 0  # zbog toga kako mi kod funkcionira(radim sve preko golbalnih indeksa) tu ručno moram postavit j na 0 isto vrijedi za k niže
        for j in range(len(clauses)):
            if visited[str(i) + str(j)] == True:
                continue
            visited[str(i) + str(j)] = True
            for a in sos[i]:
                for b in clauses[j]:
                    if a[0] == '~':
                        if a[1:] == b:
                            sos_clauses = True
                            i += 1  # zbog načina na koji funkcionira for petlja u pythonu tu moram ručno inkrementirat (vrijedi i za druga mjesta u kodu)
                            return True
                    elif a == b[1:]:
                        sos_clauses = True
                        i += 1
                        return True
    for t in range(len(sos)):
        k = 0
        for k in range(len(sos)):
            if visited[str(t) + str(k)] == True:
                continue
            visited[str(t) + str(k)] = True
            for a in sos[t]:
                for b in sos[k]:
                    if a[0] == '~':
                        if a[1:] == b:
                            sos_clauses = False
                            t += 1
                            return True
                    elif a == b[1:]:
                        sos_clauses = False
                        t += 1
                        return True
    return False


def pl_resolve(sos):
    global i, j, t, k, clauses
    c1 = set()
    c2 = set()
    if sos_clauses == True:
        c1 = sos[i - 1]
        c2 = clauses[j]  # tu nije j-1 i nemam pojma zašto nije
    else:
        c1 = sos[t - 1]
        c2 = sos[k]

    elem1 = ''
    elem2 = ''
    for a in c1:
        for b in c2:
            if a[0] == '~':
                if a[1:] == b:
                    elem1 = a
                    elem2 = b
            elif a == b[1:]:
                elem1 = a
                elem2 = b

    r_value = c1.union(c2)  # union of two sets without atom by which it was processed
    r_value.discard(elem1)
    r_value.discard(elem2)
    return r_value


def prvi(goal):
    global i, j, t, k, counter, clauses, st_builder, verbose, visited
    i = 0
    j = 0
    t = 0
    k = 0
    visited = defaultdict(list)
    sos = []
    a = set()
    if goal[0] != '~':
        a.add('~' + goal)
    else:
        a.add(goal[1:])
    sos.append(a)
    if verbose == True:
        st_builder.append(str(counter) + '. ~' + goal)
        st_builder.append('=============')

    counter += 1
    clauses_initial_length = len(clauses)

    while True:
        res = True
        i = 0
        t = 0
        while res:
            res = select_clauses(sos)
            if res == False:
                return False
            resolvents = pl_resolve(sos)

            if len(resolvents) == 0:
                if verbose == True:
                    st_builder.append(
                        str(counter) + '. NIL' + ' (' + str(i - 1 + clauses_initial_length + 1) + ', ' + str(
                            j + 1) + ')')
                counter += 1
                return True

            if sos_clauses == True:
                out = str(counter) + '. '
                out = out + ' v '.join(str(e) for e in resolvents)
                out = out + ' '
                out = out + '(' + str(i - 1 + clauses_initial_length + 1) + ', ' + str(j + 1) + ')'
                if verbose == True:
                    st_builder.append(out)
            else:
                out = str(counter) + '. '
                out = out + ' v '.join(str(e) for e in resolvents)
                out = out + ' '
                out = out + '(' + str(t - 1 + clauses_initial_length + 1) + ', ' + str(k + 1) + ')'
                if verbose == True:
                    st_builder.append(out)

            counter += 1

            sos.append(resolvents)
            for s in range(len(sos)):
                if resolvents.issubset(sos[s]) and sos[s] != resolvents:
                    sos[s] = set()
            # for s in range(len(clauses)):   #bez ovog radi sve
            #   if resolvents.issubset(clauses[s]):
            #       clauses[s] = set()
    return res


def drugi(command):
    global clauses
    if command[len(command) - 1] == '?':
        return prvi(command[0])
    if command[len(command) - 1] == '+':
        command.remove('+')
        clauses.append(set(command))
        return 'added'
    if command[len(command) - 1] == '-':
        command.remove('-')
        command = set(command)
        to_remove = []
        for i in range(len(clauses)):
            if command.issubset(clauses[i]):
                to_remove.append(i)
        clauses = [ele for ele in clauses if clauses.index(ele) not in to_remove]
        return 'removed'
    else:
        exit()
        return


def command_parser(f_path):
    f = open(f_path)
    f = f.readlines()
    r_value = []
    for l in f:
        l = l.lower()
        l = l.strip()
        l = l.split(' ')
        l = [x for x in l if x != 'v']
        r_value.append(l)
    return r_value

def resolution_parser(argv):
    global verbose, goal, counter, clauses, st_builder
    clauses = []
    # Parses clauses file
    f = open(argv[1])
    f = f.readlines()
    for i in range(len(f) - 1):
        l = f[i]
        if l[0] == '#':
            continue
        st_builder.append(str(counter) + '. ' + l.strip())
        #print(str(counter) + '. ' + l.strip())
        l = l.lower()
        l = l.strip()
        l = l.split(' v ')  # get atoms
        c = set()  # remove duplicate atoms
        c.update(l)
        clauses.append(c)  # add caluse to clauses
        counter += 1
    goal = f[len(f) - 1].lower().strip()  # save goal state in a variable
    st_builder.append('=============')


def clauses_parser(argv):
    global verbose, goal, counter, clauses, st_builder
    clauses = []
    f = open(argv[1])
    f = f.readlines()
    for i in range(len(f)):
        l = f[i]
        if l[0] == '#':
            continue
        if verbose == True:
            print(str(counter) + '. ' + l.strip())
        l = l.lower()
        l = l.strip()
        l = l.split(' v ')  # get atoms
        c = set()  # remove duplicate atoms
        c.update(l)
        clauses.append(c)  # add caluse to clauses
        counter += 1
    if verbose == True:
        print('=============')

def main(argv):
    global verbose, goal, counter, clauses, st_builder
    clauses = []


    if argv[0] == 'resolution':
        resolution_parser(argv)
        if len(argv) == 3 and argv[2] == 'verbose':
            verbose = True
        res = prvi(goal)
        if verbose == True and res == True:
            for st in st_builder:
                print(st)
            st_builder = []
            if verbose == True:
                print('=============')
        if res == False:
            print(goal, 'is unknown')
        else:
            print(goal, 'is', res)

    elif argv[0] == 'cooking_test':
        clauses_parser(argv)
        if len(argv) == 4 and argv[3] == 'verbose':
            verbose = True
        commands = command_parser(argv[2])
        for c in commands:
            res = drugi(c)
            if res == False:
                print(c[0], 'is unknown')
            elif res == 'added' or res == 'removed':
                continue
            else:
                if verbose == True:
                    for st in st_builder:
                        print(st)
                    st_builder = []
                if verbose == True:
                    print('=============')
                print(c[0], 'is', res)
            if verbose == True:
                print()

    elif argv[0] == 'cooking_interactive':
        clauses_parser(argv)
        if len(argv) == 3:
            if (argv[2] == 'verbose'):
                verbose = True
        while True:
            user_input = input()
            user_input = user_input.lower()
            user_input = user_input.strip()
            user_input = user_input.split(' ')
            user_input = [x for x in user_input if x != 'v']
            res = drugi(user_input)
            if res == False:
                print(user_input[0], 'is unknown')
            else:
                if verbose == True:
                    for st in st_builder:
                        print(st)
                    st_builder = []
                if verbose == True:
                    print('=============')
                print(user_input[0], 'is', res)
                print()

    else:
        print('Nisam rješio dodatni zadatak.')


if __name__ == "__main__":
    main(sys.argv[1:])
