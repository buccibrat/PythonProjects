import pyglet
from pyglet.window import mouse
from pyglet.gl import *

dots = []
dot_counter = 0

window = pyglet.window.Window()
glClear(GL_COLOR_BUFFER_BIT)

def draw_function(v1, v2):
    if(v1[0] <= v2[0]):
        if(v1[1] <= v2[1]):
            draw_function2(v1, v2)
        else:
            draw_function3(v1, v2)
    else:
        if(v1[1] >= v2[1]):
            draw_function2(v2, v1)
        else:
            draw_function3(v2, v1)

def draw_function2(v1, v2):
    if(v2[1]- v1[1]<= v2[0]-v1[0]):
        x0 = abs(v2[0] - v1[0])
        y0 = abs(v2[1] - v1[1])
        D = y0/x0 - 0.5
        x = v1[0]
        y = v1[1]
        for i in range(x0):
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (x, y)))
            if(D > 0):
                y += 1
                D -= 1
            x += 1
            D = D + y0/x0
    else:
        y0 = abs(v2[0] - v1[0])
        x0 = abs(v2[1] - v1[1])
        D = y0 / x0 - 0.5
        y = v1[0]
        x = v1[1]
        for i in range(x0):
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (y, x)))
            if (D > 0):
                y += 1
                D -= 1
            x += 1
            D = D + y0 / x0

def draw_function3(v1, v2):
    if(-(v2[1]- v1[1])<= v2[0]-v1[0]):
        x0 = v2[0] - v1[0]
        y0 = v2[1] - v1[1]
        D = y0/x0 + 0.5
        x = v1[0]
        y = v1[1]
        for i in range(x0):
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (x, y)))
            if(D < 0):
                y -= 1
                D += 1
            x += 1
            D = D + y0/x0
    else:
        y0 = v2[0] - v1[0]
        x0 = v2[1] - v1[1]
        D = y0 / x0 + 0.5
        y = v2[0]
        x = v2[1]
        for i in range(-x0):
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (y, x)))
            if (D < 0):
                y -= 1
                D += 1
            x += 1
            D = D + y0 / x0


@window.event
def on_draw():
    glBegin(GL_LINES)
    if (dot_counter == 2):
        glVertex2i(dots[0][0], dots[0][1] + 20)
        glVertex2i(dots[1][0], dots[1][1] + 20)
    glEnd()

@window.event
def on_mouse_press(x, y, button, modifiers):
    global dot_counter
    global dots
    if button == mouse.LEFT:
        if dot_counter < 2 :
            dots.append((x, y))
            dot_counter +=1
        if dot_counter == 2:
            draw_function(dots[0], dots[1])

pyglet.app.run()