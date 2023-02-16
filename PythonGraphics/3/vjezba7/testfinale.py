import pyglet
from pyglet.gl import *
import numpy as np
import math

window = pyglet.window.Window()

screen_width = 640
screen_height = 480

dots = []
polygon_list = []
center = [0, 0, 0]

def parser():
    global dots

    f = open('kocka.obj', 'r')
    for l in f:
        if l[0] == 'v':
            l = l.strip()
            l = l.split(" ")
            x = float(l[1])
            y = float(l[2])
            z = float(l[3])
            dots.append(np.array([x, y, z, 1]))

        if l[0] == 'f':
            l = l.strip()
            l = l.split(" ")
            polygon_list.append((int(l[1]), int(l[2]), int(l[3])))

    Xmax = Xmin = dots[0][0]
    Ymax = Ymin = dots[0][1]
    Zmax = Zmin = dots[0][2]
    for d in dots:
        if d[0] < Xmin:
            Xmin = d[0]
        if d[0] > Xmax:
            Xmax = d[0]

        if d[1] < Ymin:
            Ymin = d[1]
        if d[1] > Ymax:
            Ymax = d[1]

        if d[2] < Zmin:
            Zmin = d[2]
        if d[2] > Zmax:
            Zmax = d[2]

    center[0] = (Xmin + Xmax) / 2
    center[1] = (Ymin + Ymax) / 2
    center[2] = (Zmin + Zmax) / 2

def rescale(dots):
    global center
    Xmax = Xmin = dots[0][0]
    Ymax = Ymin = dots[0][1]
    Zmax = Zmin = dots[0][2]
    center = [0, 0, 0]
    for i in range(len(dots)):
        if dots[i][0] < Xmin:
            Xmin = dots[i][0]
        if dots[i][0] > Xmax:
            Xmax = dots[i][0]

        if dots[i][1] < Ymin:
            Ymin = dots[i][1]
        if dots[i][1] > Ymax:
            Ymax = dots[i][1]

        if dots[i][2] < Zmin:
            Zmin = dots[i][2]
        if dots[i][2] > Zmax:
            Zmax = dots[i][2]

    center[0] = (Xmin + Xmax) / 2
    center[1] = (Ymin + Ymax) / 2
    center[2] = (Zmin + Zmax) / 2

    scaler = abs(Xmax - center[0])
    if scaler < abs(Xmax - center[0]):
        scaler = abs(Xmax - center[0])
    if scaler < abs(Ymax) - center[1]:
        scaler = abs(Ymax - center[1])
    if scaler < abs(Zmax) - center[2]:
        scaler = abs(Zmax - center[2])

    for i in range(len(dots)):
        dots[i][0] -= center[0]
        dots[i][1] -= center[1]
        dots[i][2] -= center[2]

    for i in range(len(dots)):
        dots[i][0] = dots[i][0] / scaler
        dots[i][1] = dots[i][1] / scaler
        dots[i][2] = dots[i][2] / scaler
    return dots

def rotatate_alpha_z(glediste, ociste):
    t2 = np.ndarray((4, 4))
    t2.fill(0)
    sin = 0
    cos = 0
    if glediste[0, 1] != 0:
        sin = (glediste[0, 1] - ociste[0, 1]) / math.sqrt((glediste[0, 0] - ociste[0, 0]) ** 2 + (glediste[0, 1] - ociste[0, 1]) ** 2)
    if glediste[0, 0] != 0:
        cos = (glediste[0, 0] - ociste[0, 0]) / math.sqrt((glediste[0, 0] - ociste[0, 0]) ** 2 + (glediste[0, 1] - ociste[0, 1]) ** 2)
    t2[0, 0] = cos
    t2[0, 1] = (-sin)
    t2[1, 0] = sin
    t2[1, 1] = cos
    t2[2, 2] = 1
    t2[3, 3] = 1
    return t2

def rotate_beta_y(glediste, ociste):
    t3 = np.ndarray((4, 4))
    t3.fill(0)
    sin = 0
    cos = 0
    if glediste[0, 0] != 0:
        sin = (glediste[0, 0] - ociste[0, 0]) / math.sqrt((glediste[0, 0] - ociste[0, 0]) ** 2 + (glediste[0, 2] - ociste[0, 2]) ** 2)
    if glediste[0, 2] != 0:
        cos = (glediste[0, 2] - ociste[0, 2]) / math.sqrt((glediste[0, 0] - ociste[0, 0]) ** 2 + (glediste[0, 2] - ociste[0, 2]) ** 2)
    t3[0, 0] = cos
    t3[0, 2] = sin
    t3[1, 1] = 1
    t3[2, 0] = -sin
    t3[2, 2] = cos
    t3[3, 3] = 1
    return t3

def draw_object():
    global dots, batch, glediste
    batch = pyglet.graphics.Batch()

    glediste = np.ndarray((1, 4))

    glediste[0, 0] = center[0]
    glediste[0, 1] = center[1]
    glediste[0, 2] = center[2]
    glediste[0, 3] = 1

    ociste = np.ndarray((1, 4))

    ociste[0, 0] = 1
    ociste[0, 1] = 1
    ociste[0, 2] = 1
    ociste[0, 3] = 1

    t1 = np.ndarray((4, 4))
    t1.fill(0)
    t1[0, 0] = 1
    t1[1, 1] = 1
    t1[2, 2] = 1
    t1[3, 3] = 1
    t1[3, 0] = - ociste[0, 0]
    t1[3, 1] = - ociste[0, 1]
    t1[3, 2] = - ociste[0, 2]

    t2 = rotatate_alpha_z(glediste, ociste)
    glediste = np.matmul(glediste, t2)
    t3 = rotate_beta_y(glediste, ociste)
    glediste = np.matmul(glediste, t3)

    t4 = np.ndarray((4, 4))
    t4.fill(0)
    t4[0, 1] = -1
    t4[1, 0] = 1
    t4[2, 2] = 1
    t4[3, 3] = 1

    t5 = np.ndarray((4, 4))
    t5.fill(0)
    t5[0, 0] = -1
    t5[1, 1] = 1
    t5[2, 2] = 1
    t5[3, 3] = 1

    t25 = np.matmul(np.matmul(np.matmul(t2, t3), t4), t5)
    t15 = np.matmul(t1, t25)

    h = math.sqrt((ociste[0, 0] - glediste[0, 0]) ** 2 + (ociste[0, 1] - glediste[0, 1]) ** 2 + (
                ociste[0, 2] - glediste[0, 2]) ** 2)
    p = np.ndarray((4, 4))
    p.fill(0)
    p[0, 0] = 1
    p[1, 1] = 1
    p[2, 3] = 1
   # if h != 0:
    #    p[2, 3] = 1 / h

    new_dots = []
    for dot in dots:
        new_dot = np.matmul(dot, t15)
        new_dot = np.matmul(p, new_dot)
        new_dots.append(new_dot)
    new_dots = rescale(new_dots)

    for i in range(len(new_dots)):
        new_dots[i][0] = new_dots[i][0] * screen_height / 2
        new_dots[i][1] = new_dots[i][1] * screen_height / 2

    for i in range(len(new_dots)):
        new_dots[i][0] = int(new_dots[i][0] + screen_width / 2)
        new_dots[i][1] = int(new_dots[i][1] + screen_height / 2)

    for i in polygon_list:
        p1 = new_dots[i[0] - 1]
        p2 = new_dots[i[1] - 1]
        p3 = new_dots[i[2] - 1]
        a = (p2[1] - p1[1]) * (p3[2] - p1[2]) - ((p3[1] - p1[1]) * (p2[2] - p1[2]))
        b = -((p2[0] - p1[0]) * (p3[2] - p1[2])) + (p3[0] - p1[0]) * (p2[2] - p1[2])
        c = (p2[0] - p1[0]) * (p3[1] - p1[1]) - ((p3[0] - p1[0]) * (p2[1] - p1[1]))
        d = -a * p1[0] - b * p1[1] - c * p1[2]
        if ociste[0, 0] * a + ociste[0, 1] * b + ociste[0, 2] * c - d < 0:
            continue
        batch.add(2, pyglet.gl.GL_LINES, None,
                  ('v2i', (int(new_dots[i[0] - 1][0]), int(new_dots[i[0] - 1][1]), int(new_dots[i[1] - 1][0]),
                           int(new_dots[i[1] - 1][1]))))
        batch.add(2, pyglet.gl.GL_LINES, None,
                  ('v2i', (int(new_dots[i[1] - 1][0]), int(new_dots[i[1] - 1][1]), int(new_dots[i[2] - 1][0]),
                           int(new_dots[i[2] - 1][1]))))
        batch.add(2, pyglet.gl.GL_LINES, None,
                  ('v2i', (int(new_dots[i[2] - 1][0]), int(new_dots[i[2] - 1][1]), int(new_dots[i[0] - 1][0]),
                           int(new_dots[i[0] - 1][1]))))

def calculate_plain_normals(dots):
    global polygon_list
    normals = []
    for i in polygon_list:
        v1 = dots[i[0]-1]
        v2 = dots[i[1]-1]
        v3 = dots[i[2]-1]
        a = (v2[1] - v1[1]) * (v3[2] - v1[2]) - (v2[2] - v1[2]) * (v3[1]-v1[1])
        b = -(v2[0] - v1[0]) * (v3[2] - v1[2]) + (v2[2] - v1[2]) * (v3[0] - v1[0])
        c = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
        #d = -v1[0] * a - v1[1] * b - v1[2] * c
        length = math.sqrt(a **2 + b **2 + c **2)
        normals.append([a / length, b / length, c / length])
    return normals

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def draw_object2(izvor):
    global dots, batch, glediste, center

    #batch = pyglet.graphics.Batch()


    glediste = np.ndarray((1, 4))

    glediste[0, 0] = center[0]
    glediste[0, 1] = center[1]
    glediste[0, 2] = center[2]
    glediste[0, 3] = 1

    ociste = np.ndarray((1, 4))

    ociste[0, 0] = 3
    ociste[0, 1] = 2
    ociste[0, 2] = 2
    ociste[0, 3] = 1

    t1 = np.ndarray((4, 4))
    t1.fill(0)
    t1[0, 0] = 1
    t1[1, 1] = 1
    t1[2, 2] = 1
    t1[3, 3] = 1
    t1[3, 0] = - ociste[0, 0]
    t1[3, 1] = - ociste[0, 1]
    t1[3, 2] = - ociste[0, 2]

    t2 = rotatate_alpha_z(glediste, ociste)
    glediste = np.matmul(glediste, t2)
    t3 = rotate_beta_y(glediste, ociste)
    glediste = np.matmul(glediste, t3)

    t4 = np.ndarray((4, 4))
    t4.fill(0)
    t4[0, 1] = -1
    t4[1, 0] = 1
    t4[2, 2] = 1
    t4[3, 3] = 1

    t5 = np.ndarray((4, 4))
    t5.fill(0)
    t5[0, 0] = -1
    t5[1, 1] = 1
    t5[2, 2] = 1
    t5[3, 3] = 1

    t25 = np.matmul(np.matmul(np.matmul(t2, t3), t4), t5)
    t15 = np.matmul(t1, t25)

    h = math.sqrt((ociste[0, 0] - glediste[0, 0]) ** 2 + (ociste[0, 1] - glediste[0, 1]) ** 2 + (
            ociste[0, 2] - glediste[0, 2]) ** 2)
    p = np.ndarray((4, 4))
    p.fill(0)
    p[0, 0] = 1
    p[1, 1] = 1
    p[2, 3] = 1
    p[2, 3] = 1 / h

    new_dots = []
    for dot in dots:
        new_dot = np.matmul(dot, t15)
        new_dot = np.matmul(p, new_dot)
        new_dots.append(new_dot)
    new_dots = rescale(new_dots)


    normals = calculate_plain_normals(new_dots)
    plains_of_dot = []
    for i in dots:
        plains_of_dot.append([])
    counter = 0
    for i in polygon_list:
        plains_of_dot[i[0] - 1].append(counter)
        plains_of_dot[i[1] - 1].append(counter)
        plains_of_dot[i[2] - 1].append(counter)
        counter += 1
    dot_normals = []
    for i in plains_of_dot:
        a = 0
        b = 0
        c = 0
        for j in i:
            a += normals[j][0]
            b += normals[j][1]
            c += normals[j][2]
        a = a / len(i)
        b = b / len(i)
        c = c / len(i)
        dot_normals.append([a, b, c])

    for i in range(len(new_dots)):
        new_dots[i][0] = new_dots[i][0] * screen_height / 2
        new_dots[i][1] = new_dots[i][1] * screen_height / 2

    for i in range(len(new_dots)):
        new_dots[i][0] = int(new_dots[i][0] + screen_width / 2)
        new_dots[i][1] = int(new_dots[i][1] + screen_height / 2)

    ia = 177
    ka = 0.3
    ii = 24
    kd = 0.7
    for i in polygon_list:
        n1 = dot_normals[i[0] - 1]
        n2 = dot_normals[i[1] - 1]
        n3 = dot_normals[i[2] - 1]
        # batch.add(2, pyglet.gl.GL_TRIANGLES, None,
        #                     ('v2f', (new_dots[i[0] - 1][0], new_dots[i[0] - 1][1], new_dots[i[1] - 1][0], new_dots[i[1] - 1][1], new_dots[i[2] - 1][0], new_dots[i[2] - 1][1])),
        #                     ('c3f', (ia * ka + ii * kd * angle(izvor, n1), 75, 194, ia * ka + ii * kd * angle(izvor, n1), 75, 194, ia * ka + ii * kd * angle(izvor, n1), 75, 194)))

        d1 = dots[i[0] - 1]
        d2 = dots[i[1] - 1]
        d3 = dots[i[1] - 1]
        pyglet.graphics.glBegin(pyglet.gl.GL_TRIANGLES)
        pyglet.gl.glColor3f(ia * ka + ii * kd * angle([izvor[0] - d1[0], izvor[1] - d1[1], izvor[2] - d1[2]], n1), 75, 194)
        pyglet.gl.glVertex2f(dots[i[0] - 1][0], dots[i[0] - 1][1])
        pyglet.gl.glColor3f(ia * ka + ii * kd * angle([izvor[0] - d2[0], izvor[1] - d2[1], izvor[2] - d2[2]], n2), 75, 194)
        pyglet.gl.glVertex2f(dots[i[1] - 1][0], dots[i[1] - 1][1])
        pyglet.gl.glColor3f(ia * ka + ii * kd * angle([izvor[0] - d3[0], izvor[1] - d3[1], izvor[2] - d3[2]], n3), 75, 194)
        pyglet.gl.glVertex2f(dots[i[2] - 1][0], dots[i[2] - 1][1])
        pyglet.graphics.glEnd()

def update(dt):
    pass

parser()
#draw_object()
izvor = [1, 1, 1]
draw_object2(izvor)
# izvor = input('unesite položaj izvora').strip().split(' ')
# izvor = [int(i) for i in izvor]



@window.event
def on_draw():
    global izvor
    glClear(GL_COLOR_BUFFER_BIT)
    draw_object2(izvor)

pyglet.clock.schedule(update)
pyglet.app.run()



