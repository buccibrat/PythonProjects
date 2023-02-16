import pyglet
from pyglet.gl import *
import numpy as np
import math

window = pyglet.window.Window()
batch = pyglet.graphics.Batch()

screen_width = 640
screen_height = 480

#def update(dt):
#    pass

eps = int(input())
m = int(input())
uv = input().strip().split(' ')
for i in range(len(uv)):
    uv[i] = float(uv[i])

for i in range(screen_width):
    for j in range(screen_height):
        u = (uv[1] - uv[0]) / screen_width * i + uv[0]
        v = (uv[3] - uv[2]) / screen_height * j + uv[2]

        k = -1
        creal = u
        cimg = v
        zreal = 0
        zimg = 0
        r = 0 # koliki može bit epsilon
        while(r < eps and k < m):
            k = k + 1
            zr = zreal **2 - zimg**2 + creal
            zim = 2 * zreal * zimg + cimg
            zreal = zr
            zimg = zim
            r = math.sqrt(zreal**2 + zimg**2)

        c1 = k / m
        c2 = 1 -k / m / 2.0
        c3 = 0.8 - k / m / 3.0
        #print(c1, c2, c3)
        batch.add(1, pyglet.gl.GL_POINTS, None,
                    ('v2i', (i, j)),
                    ('c3f', (c1, c2, c3)))




@window.event
def on_show():
    global batch
    batch.draw()
#pyglet.clock.schedule(update)
pyglet.app.run()