import numpy as np

variables = np.ndarray((3, 4))

for i in range(3):
    for j in range(4):
        variables[i, j] = int(input())

#variables = np.array([[1, 1, 1, 6], [-1, -2, 1, -2], [2, 1, 3, 13]])
variables = variables.transpose()

x = np.linalg.det(np.concatenate((variables[3:], variables[1:3]), axis=0).transpose())/np.linalg.det(np.array(variables[0:3]).transpose())
y = np.linalg.det(np.concatenate((variables[:1], variables[3:], variables[2:3]), axis=0).transpose())/np.linalg.det(np.array(variables[0:3]).transpose())
z = np.linalg.det(np.concatenate((variables[:2], variables[3:]), axis=0).transpose())/np.linalg.det(np.array(variables[0:3]).transpose())
print()
print('[x y z] = [{} {} {}]'.format(int(round(x)), int(round(y)), int(round(z))))

