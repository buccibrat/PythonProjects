import numpy as np

coordinates = np.ndarray((4, 3))

for i in range(4):
    for j in range(3):
        coordinates[i, j] = int(input())

coordinates_transposed = coordinates.transpose()
xyz = np.concatenate((coordinates[0:1], coordinates[1:2], coordinates[2:3]), axis=0).transpose()
T = np.concatenate((coordinates[3:]), axis=0).transpose()

t = np.dot(np.linalg.inv(xyz), T)
print(t)

