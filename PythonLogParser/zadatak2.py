import sys

f = open(sys.argv[1], 'r').readlines()

d = {}

for l in f:
    a = ["", "", ""]
    index = 0
    for i in range(7):

        if not l[i].isnumeric():
            index += 1
            continue
        a[index] += l[i]

    if (a[0], a[1]) in d.keys():
        d[(a[0], a[1])] += 1
    else:
        d[(a[0], a[1])] =  1

dSorted = [ (v,k) for k,v in d.items() ]
dSorted.sort(reverse=True)
print("--------------------------------\nIP adrese   |  Br. pristupa\n--------------------------------")
for v,k in dSorted:
    print("%3s.%s.*.*     %d" % (k[0], k[1], v))