import pyglet
from pyglet.window import mouse
from pyglet.gl import *


config = pyglet.gl.Config(double_buffer = False)
window = pyglet.window.Window(config=config)

#window = pyglet.window.Window()
#glClear(GL_COLOR_BUFFER_BIT)

dots = []
line_coeff = []
dot_counter = 0
n = 0 #number of dots
Ymin = 30000
Ymax = 0
Xmin = 30000
Xmax = 0


def min_max_values(x, y):
    global Ymin
    global Ymax
    global Xmin
    global Xmax
    if x > Xmax:
        Xmax = x
    if x < Xmin:
        Xmin = x

    if y > Ymax:
        Ymax = y
    if y < Ymin:
        Ymin = y

def draw_function():
    global dots
    global line_coeff
    for i in range(len(dots) - 1) :
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (dots[i][0], dots[i][1], dots[i+1][0], dots[i+1][1])))
        line_coeff.append((dots[i][1] - dots[i+1][1], - dots[i][0] + dots[i+1][0],
                           dots[i][0] * dots[i +1][1] - dots[i+1][0] * dots[i][1]))

def v_relation(x, y):
    is_inside = True
    for i in line_coeff:
        evaluation = x * i[0] + y * i[1] + i[2]
        if evaluation > 0:
            print('TOČKA V JE IZVAN POLIGONA!')
            is_inside = False
            break
    if is_inside == True:
        print('TOČKA V JE UNUTAR POLIGONA!')

def shading():
    global Ymin, Ymax, Xmin, Xmax

    for i in range(Ymin, Ymax):
        L = Xmin
        D = Xmax
        for j in range(n):
            if line_coeff[j][0] == 0:
                break
            x = (-line_coeff[j][1] * i - line_coeff[j][2]) / line_coeff[j][0]
            if dots[j][1] < dots[j+1][1]:
                if x > L:
                    L = int(x)
            if dots[j][1] >= dots[j+1][1]:
                if x < D:
                    D = int(x)
        if L < D:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (L, i, D, i)))



@window.event
def on_mouse_press(x, y, button, modifiers):
    global dot_counter
    global dots
    global n
    if button == mouse.LEFT:
        if dot_counter == n + 1:
            dot_counter +=1
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (x, y)))
            v_relation(x, y)
            shading()
        if dot_counter < n :
            min_max_values(x, y)
            dots.append((x, y))
            dot_counter +=1
        if dot_counter == n:
            dots.append(dots[0])
            dot_counter +=1
            draw_function()


print('Unesi vrhove u smjeru kazaljke na satu!')
n = int(input ('n = \n'))

pyglet.app.run()