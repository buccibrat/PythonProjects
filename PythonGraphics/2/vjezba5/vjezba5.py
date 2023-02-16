import pyglet
from pyglet.window import mouse
from pyglet.gl import *
from pyglet.window import key
import numpy as np
import math

window = pyglet.window.Window()
batch = pyglet.graphics.Batch()

screen_width = 640
screen_height = 480

dots = []
polygon_list = []

dot_counter = 0
polygon_counter = 0
hash_counter = 0
Xmin = 3000
Xmax = -3000
Ymin = 3000
Ymax = -3000
Zmin = 3000
Zmax = -3000
center = [0, 0, 0] # center of the object
shift = [0, 0, 0] # values for translating object to coordinates (0,0,0)
scaler = -3000
V = 0
plain_coef = []

def update(dt):
    pass

def parser():
    global dots, polygon_list, dot_counter, polygon_counter, hash_counter, center, Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, scaler

    f = open('kocka.obj', 'r')
    for l in f:
        x = 0
        y = 0
        z = 0
        if l[0] == 'v':
            l = l.strip()
            l = l.split(" ")
            x = float(l[1])
            y = float(l[2])
            z = float(l[3])
            dots.append(np.array([x, y, z, 1]))
            dot_counter +=1

            if x < Xmin:
                Xmin = x
            if x > Xmax:
                Xmax = x

            if y < Ymin:
                Ymin = y
            if y > Ymax:
                Ymax = y

            if z < Zmin:
                Zmin = z
            if z > Zmax:
                Zmax = z

        if l[0] == 'f':
            l = l.strip()
            l = l.split(" ")
            polygon_list.append((int(l[1]), int(l[2]), int(l[3])))
            polygon_counter +=1
        if l[0] == '#':
            hash_counter += 1
    #Finds center of the picture
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

def rescale(dots):
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



def draw_object(flag):
    global dots, batch

    batch = pyglet.graphics.Batch()

    glediste = np.ndarray((1, 4))

    glediste[0,0] = 1
    glediste[0,1] = 1
    glediste[0,2] = -1
    glediste[0,3] = 1

    ociste = np.ndarray((1, 4))

    ociste[0,0] = 0
    ociste[0,1] = 0
    ociste[0,2] = 0
    ociste[0,3] = 1

    if flag == 'gx+':
        glediste[0, 0] += 1
    if flag == 'gx-':
        glediste[0, 0] -= 1
    if flag == 'gy+':
        glediste[0, 1] += 1
    if flag == 'gy-':
        glediste[0, 1] -= 1
    if flag == 'gz+':
        glediste[0, 2] += 1
    if flag == 'gz-':
        glediste[0, 2] -= 1
    if flag == 'ox+':
        ociste[0, 0] += 1
    if flag == 'ox-':
        ociste[0, 0] -= 1
    if flag == 'oy+':
        ociste[0, 1] += 1
    if flag == 'oy-':
        ociste[0, 1] -= 1
    if flag == 'oz+':
        ociste[0, 2] += 1
    if flag == 'oz-':
        ociste[0, 2] -= 1

    t1 = np.ndarray((4, 4))
    t1. fill(0)
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

    h = math.sqrt((ociste[0, 0] - glediste[0, 0]) ** 2 + (ociste[0, 1] - glediste[0, 1]) ** 2 + (ociste[0, 2] - glediste[0, 2]) ** 2)
    p = np.ndarray((4, 4))
    p.fill(0)
    p[0, 0] = 1
    p[1, 1] = 1
    p[2,3] = 1
    if h != 0:
        p[2, 3] = 1/h

    new_dots = []
    for dot in dots:
        new_dot = np.matmul(dot, t15)
        new_dot = np.matmul(new_dot, p)
        new_dots.append(new_dot)
    new_dots = rescale(new_dots)

    for i in range(len(new_dots)):
        new_dots[i][0] = new_dots[i][0] * screen_height / 2
        new_dots[i][1] = new_dots[i][1] * screen_height / 2

    for i in range(len(new_dots)):
        new_dots[i][0] = int(new_dots[i][0] + screen_width / 2)
        new_dots[i][1] = int(new_dots[i][1] + screen_height / 2)

    for i in polygon_list:

        batch.add(2, pyglet.gl.GL_LINES, None,
                                  ('v2i', (int(new_dots[i[0] - 1][0]), int(new_dots[i[0] - 1][1]), int(new_dots[i[1] - 1][0]), int(new_dots[i[1] - 1][1]))))
        batch.add(2, pyglet.gl.GL_LINES, None,
                                  ('v2i', (int(new_dots[i[1] - 1][0]), int(new_dots[i[1] - 1][1]), int(new_dots[i[2] - 1][0]), int(new_dots[i[2] - 1][1]))))
        batch.add(2, pyglet.gl.GL_LINES, None,
                                  ('v2i', (int(new_dots[i[2] - 1][0]), int(new_dots[i[2] - 1][1]), int(new_dots[i[0] - 1][0]), int(new_dots[i[0] - 1][1]))))

parser()
draw_object('nista')
#
# @window.event
# def on_show():
#     global batch
#     batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    window.clear()
    if symbol == key.Q:
        draw_object('gx+')
    if symbol == key.A:
        draw_object('gx-')
    if symbol == key.W:
        draw_object('gy+')
    if symbol == key.S:
        draw_object('gy-')
    if symbol == key.E:
        draw_object('gz+')
    if symbol == key.D:
        draw_object('gz-')
    if symbol == key.R:
        draw_object('ox+')
    if symbol == key.F:
        draw_object('ox-')
    if symbol == key.T:
        draw_object('oy+')
    if symbol == key.G:
        draw_object('oy-')
    if symbol == key.Z:
        draw_object('oz+')
    if symbol == key.H:
        draw_object('oz-')



@window.event
def on_draw():
    window.clear()
    glClear(GL_COLOR_BUFFER_BIT)
    batch.draw()


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()
