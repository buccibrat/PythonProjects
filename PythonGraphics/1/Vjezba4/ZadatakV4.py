import pyglet
from pyglet.window import mouse
from pyglet.gl import *


window = pyglet.window.Window()
batch = pyglet.graphics.Batch()

screen_width = 640
screen_height = 480

dots = []
dots_initial = []
polygon_list = []

dot_counter = 0
polygon_counter = 0
hash_counter = 0
Xmin = 3000
Xmax = 0
Ymin = 3000
Ymax = 0
Zmin = 3000
Zmax = 0
center = [0, 0, 0] # center of the object
shift = [0, 0, 0] # values for translating object to coordinates (0,0,0)
scaler = -3000
V = 0
plain_coef = []

def parser():
    global dots, polygon_list, dot_counter, polygon_counter, hash_counter, center, Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, scaler

    f = open('porsche.obj', 'r')
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
            dots.append([x, y, z])
            dots_initial.append([x, y, z])
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

def calculate_plain_coeff():
    global dots, polygon_list, plain_coef
    for i in polygon_list:
        v1 = dots[i[0]-1]
        v2 = dots[i[1]-1]
        v3 = dots[i[2]-1]
        a = (v2[1] - v1[1]) * (v3[2] - v1[2]) - (v2[2] - v1[2]) * (v3[1]-v1[1])
        b = -(v2[0] - v1[0]) * (v3[2] - v1[2]) + (v2[2] - v1[2]) * (v3[0] - v1[0])
        c = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
        d = -v1[0] * a - v1[1] * b - v1[2] * c
        plain_coef.append([a, b, c, d])

def check_v(x, y, z):
    is_inside = True
    for i in plain_coef:
        if i[0] * x + i[1] * y + i[2] * z +  i[3]  > 0:
            is_inside = False
            break
    if is_inside == True:
        print('Točka je unutar tijela')
    else:
        print('Točka je izvan tijela')

#def resize():


def draw_object():
    global dots, screen_width, screen_height, polygon_list
    # needs_resize = false
    # if Xmin < screen_width or Xmin > screen_width:
    #     needs_resize = true
    # if Xmax < screen_width or Xmax > screen_width:
    #     needs_resize = true
    # if Ymin < screen_height or Ymin > screen_height:
    #     needs_resize = true
    # if Ymax < screen_height or Ymax > screen_height:
    #     needs_resize = true

    for i in range(len(dots)):
        dots[i][0] = dots[i][0] * screen_height / 2
        dots[i][1] = dots[i][1] * screen_height / 2

    for i in range(len(dots)):
        dots[i][0] = int(dots[i][0] + screen_width / 2)
        dots[i][1] = int(dots[i][1] + screen_height / 2)


    global batch
    for i in polygon_list:
        batch.add(2, pyglet.gl.GL_LINES, None,
                                  ('v2i', (dots[i[0] - 1][0], dots[i[0] - 1][1], dots[i[1] - 1][0], dots[i[1] - 1][1])))
        batch.add(2, pyglet.gl.GL_LINES, None,
                                  ('v2i', (dots[i[1] - 1][0], dots[i[1] - 1][1], dots[i[2] - 1][0], dots[i[2] - 1][1])))
        batch.add(2, pyglet.gl.GL_LINES, None,
                                  ('v2i', (dots[i[2] - 1][0], dots[i[2] - 1][1], dots[i[0] - 1][0], dots[i[0] - 1][1])))

@window.event
def on_show():
    global batch
    batch.draw()


parser()
calculate_plain_coeff()
V = input('Točka = ').strip().split(" ")
check_v(float(V[0]), float(V[1]), float(V[2]))
print(dots)
draw_object()

pyglet.app.run()





