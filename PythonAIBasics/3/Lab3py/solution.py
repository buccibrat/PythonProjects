import sys, itertools, math

def parser(p):
    r_value = []
    f = open(p, 'r')
    for l in f:
        r_value.append(l.strip().split(','))
    return r_value

def cfg_parser(p):
    r_value = []
    f = open(p, 'r')
    for l in f:
        r_value.append(l)
    return r_value

class Node:
    def __init__(self, x, subtrees):
        self.x = x
        self.subtrees = subtrees

class Leaf:
    def __init__(self, value):
        self.value = value


def argmax(d, n, y):
    counter = [0] * n
    for i in d:
        counter[y.index(i[-1])] += 1
    largest = 0
    index = -1
    for i in counter:
        if i > largest:
            largest = i
            index = counter.index(i)
    return y[index]

def get_d(d, v):
    r_value = []
    for i in d:
        if i[-1] == v:
            r_value.append(i)
    return r_value

def argmaxIG(dp, X, y):
    counter = [0] * len(y)
    for i in dp:
        counter[y.index(i[-1])] += 1
    Ed = 0
    for i in range(len(counter)):
        if counter[i] == None:
            continue
        Ed += -counter[i] / len(dp) * math.log2(counter[i] / len(dp))
    ig = []
    for i in range(len(X) - 1):
        if X[i] == None: #ove tri linije sam dodao zbog titanika
            ig.append(0) #
            continue #
        znacajke = [] # zapravo su vrijednosti znacajke
        for j in range(len(dp)):
            if dp[j][i] not in znacajke:
                znacajke.append(dp[j][i])

        znacajke = sorted(znacajke)
        counters = []

        for j in znacajke:
            counters.append([0] * len(y))

        for j in range(len(dp)):
            counters[znacajke.index(dp[j][i])][y.index(dp[j][-1])] += 1

        ed = [0] * len(znacajke)
        for j in range(len(counters)):
            for e in counters[j]:
                if e == 0:
                    continue
                ed[j] += -e / sum(counters[j]) * math.log2(e / sum(counters[j]))
        ig.append(Ed)
        for j in range(len(ed)):
             ig[i] -= sum(counters[j]) / len(dp) * ed[j]
    largest = -1
    currX = None
    for i in X:
        if i != None:
            currX = i
            break
    index = -1
    for i in range(len(X) - 1):
        if X[i] == None:
            continue
        if largest < ig[i]:
            largest = ig[i]
            index = i
    for i in range(len(X) - 1):
        if X[i] == None:
            continue
        if largest == ig[i] and currX > X[i]:
            index = i

    return X[index]
    #return X[ig.index(max(ig))] s ovim je radilo sve osim titanika

def getV(X, x, dp):
    v = []
    for j in range(len(dp)):
        if dp[j][X.index(x)] not in v and dp[j][X.index(x)]:
            v.append(dp[j][X.index(x)])
    return sorted(v)

def getDx(d, x, v, X):
    dp = []
    index = X.index(x)
    for i in range(len(d)):
        if d[i][index] == v:
            dp.append(d[i])
    return dp

dubina = -1

def id3(d, dp, X, y, duboko):
    global dubina

    v = None
    if not dp:
        v = argmax(d, len(y), y)
        return Leaf(v)
    v = argmax(dp, len(y), y)
    is_empty = True
    for i in itertools.islice(X, 0, len(X) - 1):
        if i != None:
            is_empty = False
            break
    if is_empty or get_d(dp, v) == dp:
        return Leaf(v)
    if dubina == duboko:
        counters = [0] * len(y)
        for line in dp:
            counters[y.index(line[-1])] += 1
        return Leaf(y[counters.index(max(counters))])
    x = argmaxIG(dp, X, y)
    V = getV(X, x, dp)
    subtrees = []
    duboko += 1
    for v in V:
        newd = getDx(dp, x, v, X)
        newx = X[:]
        newx[X.index(x)] = None
        t = id3(d, newd, newx, y, duboko)
        subtrees.append([v, t, newd])
    return Node(x, subtrees)

def do_prediction(data, X, node, y, index):
    if isinstance(node, Leaf):
        return node.value
    for t in node.subtrees:
        if t[0] == data[X.index(node.x)]:
            index +=1
            return do_prediction(data, X, t[1], y, index)
    counter = [0] * len(y)
    for t in node.subtrees:
        for line in t[2]:
            counter[y.index(line[-1])] += 1
    return y[counter.index(max(counter))]

def predict(dataset, node):
    s = ''
    d, x, y = [], [], []
    x = dataset[0][0:-1]
    x.append(dataset[0][-1])
    for i in itertools.islice(dataset, 1, len(dataset)):
        d.append(i)
        if i[-1] not in y:
            y.append(i[-1])
    y = sorted(y)
    fault = []
    correct = 0
    for i in range(len(y)):
        fault.append([0] * len(y))
    for data in d:
        v = do_prediction(data[:-1], x, node, y, 0)
        s += str(v) + ' '
        if v == data[-1]:
            fault[y.index(v)][y.index(v)] += 1
            correct += 1
        else:
            fault[y.index(data[-1])][y.index(v)] += 1
    return (s, correct / len(d), fault)



data = parser(sys.argv[1])
test_data = parser(sys.argv[2])
cfg = cfg_parser(sys.argv[3])

for i in cfg:
    if 'max_depth' in i:
        i = i.strip().split('=')
        dubina = int(i[1])


d, x, y = [], [], []
x = data[0][0:-1]
x.append(data[0][-1])
for i in itertools.islice(data , 1, len(data)):
    d.append(i)
    if i[-1] not in y:
        y.append(i[-1])

y = sorted(y)

nodica = id3(d, d, x, y, 0)
s = ''
def idikrozstablo(nodica, d):
    global s
    if isinstance(nodica, Leaf):
        return
    s = s + str(d) + ':' + str(nodica.x) + ', '
    for t in nodica.subtrees:
        idikrozstablo(t[1], d + 1)


idikrozstablo(nodica, 0)
print(s[:-2])
values = predict(test_data, nodica)
print(values[0])
print('{:0.5f}'.format(values[1]))
matrica = values[2]

for i in range(len(matrica)):
    s = ''
    for j in range(len(matrica)):
        s += str(matrica[i][j]) + ' '
    print(s)

