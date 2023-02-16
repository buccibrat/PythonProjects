from pyglet.gl import *
import numpy as np
import math

vrhovi = []
poligoni = []
brVrhova = 0
brPoligona = 0

f = open("kocka.obj", "r")
for x in f:
    a = x.split()
    if x.startswith('v'):
        brVrhova += 1
        vrhovi.append([float(a[1]), float(a[2]), float(a[3])])
    elif x.startswith('f'):
        brPoligona += 1
        poligoni.append([int(a[1])-1, int(a[2])-1, int(a[3])-1])
f.close()

def sred(vrhovi):
    global x0, y0, z0, srediste, skalVrhovi
    x0=[vrhovi[0][0], vrhovi[0][0]]
    y0=[vrhovi[0][1], vrhovi[0][1]]
    z0=[vrhovi[0][2], vrhovi[0][2]]
    for i in range(len(vrhovi)):
        if vrhovi[i][0] < x0[0]:
            x0[0] = vrhovi[i][0]
        if vrhovi[i][0] > x0[1]:
            x0[1] = vrhovi[i][0]
        if vrhovi[i][1] < y0[0]:
            y0[0] = vrhovi[i][1]
        if vrhovi[i][1] > y0[1]:
            y0[1] = vrhovi[i][1]
        if vrhovi[i][2] < z0[0]:
            z0[0] = vrhovi[i][2]
        if vrhovi[i][2] > z0[1]:
            z0[1] = vrhovi[i][2]
    srediste = [(x0[0]+x0[1])/2, (y0[0]+y0[1])/2, (z0[0]+z0[1])/2]
    for i in range(len(vrhovi)):
        vrhovi[i][0] -= srediste[0]
        vrhovi[i][1] -= srediste[1]
        vrhovi[i][2] -= srediste[2]
    skalX = abs(x0[0] - x0[1])
    skalY = abs(y0[0] - y0[1])
    skalZ = abs(z0[0] - z0[1])
    skaler = max(skalX, skalY, skalZ) / 2
    skalVrhovi = []
    for i in range(len(vrhovi)):
        skalVrhovi.append([vrhovi[i][0] / skaler, vrhovi[i][1] / skaler, vrhovi[i][2] / skaler, 1])
    return skalVrhovi

vrhovi = sred(vrhovi)

o=[5, -5, 7]
g=srediste


xg1 = g[0] - o[0]
yg1 = g[1] - o[1]
zg1 = g[2] - o[2]

sina = yg1 / math.sqrt(xg1 ** 2 + yg1 ** 2)
cosa = xg1 / math.sqrt(xg1 ** 2 + yg1 ** 2)
xg2 = math.sqrt(xg1 ** 2 + yg1 ** 2)
zg2 = zg1
sinb = xg2 / math.sqrt(xg2 ** 2 + zg2 ** 2)
cosb = zg2 / math.sqrt(xg2 ** 2 + zg2 ** 2)
zg3 = math.sqrt(xg2 ** 2 + zg2 ** 2)

t1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-o[0], -o[1], -o[2], 1]])
t2 = np.array([[cosa, -sina, 0, 0], [sina, cosa, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
t3 = np.array([[cosb, 0, sinb, 0], [0, 1, 0, 0], [-sinb, 0, cosb, 0], [0, 0, 0, 1]])
t4 = np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
t5 = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
ttrans = np.matmul(t1, np.matmul(np.matmul(t2, t3), np.matmul(t4, t5)))
tp = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1 / zg3], [0, 0, 0, 0]])
tpvrhovi = []
for vrh in vrhovi:
    tpvrhovi.append(np.matmul(tp, np.matmul(vrh, ttrans)))

tpvrhovi = sred(tpvrhovi)

def getNormala(pol):
    x1 = vrhovi[pol[0]][0]
    x2 = vrhovi[pol[1]][0]
    x3 = vrhovi[pol[2]][0]
    y1 = vrhovi[pol[0]][1]
    y2 = vrhovi[pol[1]][1]
    y3 = vrhovi[pol[2]][1]
    z1 = vrhovi[pol[0]][2]
    z2 = vrhovi[pol[1]][2]
    z3 = vrhovi[pol[2]][2]
    a = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
    b = -(x2 - x1) * (z3 - z1) + (z2 - z1) * (x3 - x1)
    c = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    d = -x1 * a - y1 * b - z1 * c
    normala = [a / math.sqrt(a ** 2 + b ** 2 + c ** 2), b / math.sqrt(a ** 2 + b ** 2 + c ** 2),
               c / math.sqrt(a ** 2 + b ** 2 + c ** 2)]
    return normala

def normaleSusjeda(susjednipoligoni):
    list = []
    for pol2 in susjednipoligoni:
        list.append(getNormala(pol2))
    return list

def racNormala(normale):
    sum = [0, 0, 0]
    for nor in normale:
        sum[0] += nor[0]
        sum[1] += nor[1]
        sum[2] += nor[2]
    return [sum[0]/len(normale), sum[1]/len(normale), sum[2]/len(normale)]

def racVektor(vrh):
    vecx = izvor[0] - vrh[0]
    vecy = izvor[1] - vrh[1]
    vecz = izvor[2] - vrh[2]
    vecs = math.sqrt(vecx ** 2 + vecy ** 2 + vecz ** 2)
    return [vecx / vecs, vecy / vecs, vecz / vecs]

visina = 480
sirina = 640
for i in range(len(tpvrhovi)):
    tpvrhovi[i][0] *= (visina / 2 - 50)
    tpvrhovi[i][1] *= (visina / 2 - 50)

for i in range(len(tpvrhovi)):
    tpvrhovi[i][0] += (sirina / 2)
    tpvrhovi[i][1] += (visina / 2)

izvor = [0, 0, 20]

window = pyglet.window.Window()

def draw():
    for pol in poligoni:
        susjednipoligoni1 = []
        susjednipoligoni2 = []
        susjednipoligoni3 = []
        br = 1
        for vrh in pol:
            for pol2 in poligoni:
                if pol != pol2 and vrh in pol2 and br == 1:
                    susjednipoligoni1.append(pol2)
                if pol != pol2 and vrh in pol2 and br == 2:
                    susjednipoligoni2.append(pol2)
                if pol != pol2 and vrh in pol2 and br == 3:
                    susjednipoligoni3.append(pol2)
            br += 1
        normale1 = normaleSusjeda(susjednipoligoni1)
        normale2 = normaleSusjeda(susjednipoligoni2)
        normale3 = normaleSusjeda(susjednipoligoni3)
        x1 = vrhovi[pol[0]][0]
        x2 = vrhovi[pol[1]][0]
        x3 = vrhovi[pol[2]][0]
        y1 = vrhovi[pol[0]][1]
        y2 = vrhovi[pol[1]][1]
        y3 = vrhovi[pol[2]][1]
        z1 = vrhovi[pol[0]][2]
        z2 = vrhovi[pol[1]][2]
        z3 = vrhovi[pol[2]][2]
        a = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
        b = -(x2 - x1) * (z3 - z1) + (z2 - z1) * (x3 - x1)
        c = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        d = -x1 * a - y1 * b - z1 * c
        rac = a * o[0] + b * o[1] + c * o[2] - d
        normala = [a / math.sqrt(a ** 2 + b ** 2 + c ** 2), b / math.sqrt(a ** 2 + b ** 2 + c ** 2),
                   c / math.sqrt(a ** 2 + b ** 2 + c ** 2)]
        normale1.append(normala)
        normale2.append(normala)
        normale3.append(normala)
        normalavrh1 = racNormala(normale1)
        normalavrh2 = racNormala(normale2)
        normalavrh3 = racNormala(normale3)
        vec1 = racVektor(vrhovi[pol[0]])
        vec2 = racVektor(vrhovi[pol[1]])
        vec3 = racVektor(vrhovi[pol[2]])
        kut1 = normalavrh1[0]*vec1[0] + normalavrh1[1]*vec1[1] + normalavrh1[2]*vec1[2]
        kut2 = normalavrh2[0]*vec2[0] + normalavrh2[1]*vec2[1] + normalavrh2[2]*vec2[2]
        kut3 = normalavrh3[0]*vec3[0] + normalavrh3[1]*vec3[1] + normalavrh3[2]*vec3[2]

        if rac > 0:
            id1 = 255 * 0.1 + 255 * 0.7 * kut1
            id2 = 255 * 0.1 + 255 * 0.7 * kut2
            id3 = 255 * 0.1 + 255 * 0.7 * kut3
            if id1 < 0:
                id1 = 0
            if id2 < 0:
                id2 = 0
            if id3 < 0:
                id3 = 0
            glColor3f(0, 0, 0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(tpvrhovi[pol[0]][0], tpvrhovi[pol[0]][1])
            glVertex2f(tpvrhovi[pol[1]][0], tpvrhovi[pol[1]][1])
            glVertex2f(tpvrhovi[pol[2]][0], tpvrhovi[pol[2]][1])
            glEnd()
            glBegin(GL_TRIANGLES)
            glColor3f(id1, 0, 0)
            glVertex2f(tpvrhovi[pol[0]][0], tpvrhovi[pol[0]][1])
            glColor3f(id2, 0, 0)
            glVertex2f(tpvrhovi[pol[1]][0], tpvrhovi[pol[1]][1])
            glColor3f(id3, 0, 0)
            glVertex2f(tpvrhovi[pol[2]][0], tpvrhovi[pol[2]][1])
            glEnd()

@window.event
def on_show():
    draw()

pyglet.app.run()
