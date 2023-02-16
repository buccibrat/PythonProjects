import numpy as np
import math

#Zbrajanje
v1 = np.array([2, 3, -4]) + np.array([-1, 4, -1])
print(v1)

#Skalarni produkt
s = np.dot(v1, np.array([-1, 4, -1]))
print(s)

#Vektorski produkt
v2 = np.cross(v1, np.array([2, 2, 4]))
print(v2)

#Normirani vektor
v3 = v2 / (v2**2).sum()**0.5 # v2 / linalg.norm(v2)
print(v3)

#Suprotni vektor
v4 = -v2
print(v4)

#M1
m1 = np.array([[1, 2, 3], [2, 1, 3], [4, 1, 5]]) + np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])
print()
print(m1)

#M2
m2 = np.dot(np.array([[1, 2, 3], [2, 1, 3], [4, 5, 1]]), np.transpose(np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])))
print()
print(m2)

#M3
m3 = np.dot(np.array([[1, 2, 3], [2, 1, 3], [4, 5, 1]]), np.linalg.inv(np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])))
print()
print(m3)


