import sys


def fill(index):
    lines = matrix[index].split("\n")
    dim = lines[0].split(" ")
    dimensions[index] = (int(dim[0]), int(dim[1]))
    matrixDict = {}
    for line in lines[1:]:
        values = line.split(" ")

        matrixDict[(int(values[0]), int(values[1]))] = int(values[2])

    for i in range(int(dimensions[index][0])):
        for j in range(int(dimensions[index][1])):
            if (i, j) in matrixDict:
                continue
            matrixDict[(i, j)] = 0

    return matrixDict

def multipyRow(a, b):
    sum = 0
    for i in range (len(a)):
            sum += a[i] * b[i]
    return sum

def multiplyMatrix(a, b):
    if dimensions[0][1] != dimensions[1][0]:
        return "Not multipliable"
    multiplied = {}
    jIndex = 0
    for i in range(int(dimensions[0][0])):
        for j in range(int(dimensions[1][1])):
            aHelp = []
            bHelp = []
            for m in range (int(dimensions[0][1])):
                aHelp.append(a[(i, m)])
            for n in range (int(dimensions[1][0])):
                bHelp.append(b[(n, j)])
            if jIndex >= int(dimensions[1][1]):
                jIndex = 0
            multiplied[(i, jIndex)] = multipyRow(aHelp, bHelp)
            jIndex += 1

    return multiplied
                    
def prettyPrint(dimI, dimJ, matrix, cond):
    myStr = ""
    for i in range(dimI):
        if cond == True:
            myStr += "  "
        for j in range(dimJ):
            myStr += str(matrix[(i, j)]) + " "
        myStr += "\n"
    return myStr


fileIn = open(sys.argv[1], 'r').read()
matrix = fileIn.split("\n\n")

dimensions = [0, 0]
matrix1 = fill(0)
matrix2 = fill(1)

output = multiplyMatrix(matrix1, matrix2)

fw = open(sys.argv[2], 'w')
myStr = str(dimensions[0][0]) + " " + str(dimensions[1][1]) + "\n"
myStr += prettyPrint(dimensions[0][0], dimensions[1][1], output, False)
fw.write(myStr)

print("A:")
myStr = prettyPrint(dimensions[0][0], dimensions[0][1], matrix1, True)
print(myStr)

print("B:")
myStr = prettyPrint(dimensions[1][0], dimensions[1][1], matrix2, True)
print(myStr)

print("A*B:")
print (prettyPrint(dimensions[0][0], dimensions[1][1], output, True))





